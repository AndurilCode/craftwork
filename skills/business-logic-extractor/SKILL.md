---
name: business-logic-extractor
description: "Extract and document business logic, domain models, and product rules from a codebase into a structured llms.txt-style reference. Use this skill whenever someone asks to 'document the business logic', 'extract domain rules', 'what are the business rules in this codebase', 'map the domain model', 'document product behavior', 'what does this system actually do', 'reverse-engineer the business rules', 'create a domain reference', 'what are the invariants', 'how does pricing work in this codebase', 'what validations exist', 'document entity relationships', or any request to make implicit product knowledge explicit from code. Also trigger when an agent or developer is onboarding to a codebase and needs to understand what the system does (not how it's built). This is the context engineer's domain knowledge extraction tool — it turns code into a product behavior reference."
---

# Business Logic Extractor

Produces a single Markdown doc capturing the *product and domain knowledge* embedded in a codebase — entities, relationships, business rules, invariants. Same llms.txt format (H2 sections, annotated code, token-budgeted) but focused on *what the system does*, not *how to use its APIs*.

**Difference from llms-txt-generator**: that skill documents a library's *public API* from its docs; this one documents a codebase's *product behavior* from its source. Input is code, not docs. Sections are domain concepts, not API topics.

---

## Execution

Operates on the current codebase. Requires filesystem access.

**Pre-flight**: Confirm codebase root. Look for manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `*.csproj`). If missing, ask user to confirm root.

---

## PHASE 1 — Domain Surface Scan

Find where business logic lives. Focus on high-signal locations.

### High-signal locations

| Look for | Why | Typical paths |
|---|---|---|
| **ORM models / schemas** | Entities, fields, relationships, constraints | `models/`, `entities/`, `schema/`, `prisma/schema.prisma`, `**/models.py`, `**/*Entity.java` |
| **Validation logic** | Business rules as code | `validators/`, `rules/`, `guards/`, `**/validate*`, `**/*.guard.ts` |
| **Service / use-case layer** | Business operations | `services/`, `usecases/`, `domain/`, `**/service*`, `**/*Service.*` |
| **Tests (esp. integration)** | Assert expected behavior — goldmine | `test/`, `spec/`, `__tests__/`, `**/test_*`, `**/*.spec.*` |
| **Constants and config** | Thresholds, limits, feature flags, pricing tiers | `constants/`, `config/`, `**/*constants*`, `**/*config*`, `.env.example` |
| **Enums and status types** | Lifecycle states, categories, permissions | `types/`, `enums/`, `**/status*`, `**/state*` |
| **Migration files** | Schema evolution → domain decisions | `migrations/`, `db/migrate/`, `alembic/versions/` |
| **API routes / controllers** | The verbs of the system | `routes/`, `controllers/`, `api/`, `app/api/` |
| **Middleware / interceptors** | Cross-cutting rules (auth, rate limits, tenancy) | `middleware/`, `interceptors/`, `pipes/` |

### Scan procedure

```bash
# 1. Tech stack
cat package.json 2>/dev/null || cat pyproject.toml 2>/dev/null || cat go.mod 2>/dev/null || cat Cargo.toml 2>/dev/null

# 2. Models/entities
find . -type f \( -name "*.model.*" -o -name "*.entity.*" -o -name "*.schema.*" \
  -o -name "models.py" -o -name "schema.prisma" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" | head -50

# 3. Business logic layers
find . -type f \( -name "*.service.*" -o -name "*.usecase.*" -o -name "*.rule.*" \
  -o -name "*.validator.*" -o -name "*.guard.*" -o -name "*.policy.*" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" | head -50

# 4. Tests (prioritize integration/e2e)
find . -type f \( -name "*.spec.*" -o -name "*.test.*" -o -name "test_*" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" | head -50

# 5. Constants, enums, config
find . -type f \( -name "*constant*" -o -name "*enum*" -o -name "*config*" \
  -o -name "*status*" -o -name "*types*" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/dist/*" | head -50
```

Read what you find. Build a mental inventory of domain concepts before proceeding.

**Output**: file inventory by signal type, plus first-pass list of entities and operations spotted.

---

## PHASE 2 — Domain Model Extraction

For each **entity** (model, aggregate, value object):

1. **Name and purpose**: What real-world concept does it represent?
2. **Fields and semantics**: Not `status: string` — what are valid values, what do they mean?
3. **Relationships**: belongs to / has many / references
4. **Invariants** — what must always be true. Look for:
   - DB constraints (unique, not null, FK, check)
   - Validations before persistence
   - Rules in setters / lifecycle hooks
   - Test assertions that check "this should never happen"
5. **Lifecycle**: states + allowed transitions (status enums, state machines, workflow logic)

### Where invariants hide

- **Model validations**: `@IsNotEmpty()`, `validates :email, presence: true`, Zod/Yup schemas
- **DB constraints**: `NOT NULL`, `UNIQUE`, `CHECK`, FK cascades
- **Guard clauses**: `if (!user.isActive) throw ...`, early returns
- **Test assertions**: `expect(order.total).toBeGreaterThan(0)` IS a business rule
- **Comments with "must"/"should"**: informal invariant annotations
- **Migrations**: `ALTER TABLE ... ADD CONSTRAINT` — rules added post-design

### Entity section format

```markdown
## {Entity Name}

{1-3 sentences: what it represents, its purpose, its most important invariant or lifecycle characteristic.}

```{language}
// Key fields with business-relevant annotations
// Relationships indicated by comments
// Invariants and constraints called out explicitly

type Order = {
  id: string
  userId: string                    // belongs to User
  status: OrderStatus               // lifecycle: draft → confirmed → shipped → delivered | cancelled
  items: OrderItem[]                // has many OrderItems, min 1
  total: number                     // invariant: must equal sum of items × prices, must be > 0
  currency: Currency                // set at creation, immutable after
  createdAt: Date
  confirmedAt: Date | null          // set when status → 'confirmed'
}

// Valid status transitions (from state machine or service logic)
// draft → confirmed (requires: items.length > 0, total > 0)
// confirmed → shipped (requires: payment.status === 'captured')
// confirmed → cancelled (allowed within 24h of confirmation)
// shipped → delivered (external trigger from logistics)
```
```

---

## PHASE 3 — Business Rule Extraction

Behavioral constraints beyond the data model. Answer: "Under what conditions can X happen?"

### What qualifies

- **Validation**: input constraints beyond type safety (min length, format, allowed values, cross-field deps)
- **Authorization**: who can do what when (role, ownership, time-based)
- **Calculation**: pricing, tax, discount, scoring formulas
- **Eligibility**: preconditions ("can this user place an order?")
- **Rate limits / thresholds**: max orders/day, min balance, cooling-off
- **Side effects / triggers**: when X happens, Y must too (email on signup, audit log on delete, external sync)

### Where rules hide

- **Service methods**: if/else chains in `createOrder()`, `processRefund()`, `upgradeSubscription()`
- **Middleware/guards**: auth/authz logic
- **Validators**: schemas with business constraints (not just type validation)
- **Test descriptions**: `it('should not allow checkout with empty cart')` — test name IS the rule
- **Constants**: `MAX_ITEMS_PER_ORDER = 50`, `REFUND_WINDOW_DAYS = 30`
- **Feature flags**: `ENABLE_LOYALTY_DISCOUNT`, `MIN_ORDER_AMOUNT`
- **Error messages**: `'Cannot cancel order after shipment'` — error string states the rule

### Rule section format

Group related rules by domain operation or cluster:

```markdown
## {Operation / Rule Cluster Name}

{1-3 sentences: what business operation this covers and why these rules exist.}

```{language}
// Extracted and annotated from the actual codebase
// Each rule is called out with a comment explaining the business reason

async function processRefund(orderId: string, reason: string) {
  const order = await getOrder(orderId)

  // Rule: only refund completed orders
  if (order.status !== 'delivered') throw new Error('Order not eligible')

  // Rule: refund window is 30 days from delivery
  const daysSinceDelivery = daysBetween(order.deliveredAt, now())
  if (daysSinceDelivery > REFUND_WINDOW_DAYS) throw new Error('Refund window expired')

  // Rule: refund amount cannot exceed original total
  const refundAmount = Math.min(requestedAmount, order.total)

  // Rule: refunds over €500 require manager approval
  if (refundAmount > 500) {
    await requestManagerApproval(orderId, refundAmount)
    return { status: 'pending_approval' }
  }

  // Side effect: trigger payment provider reversal
  await paymentProvider.refund(order.paymentId, refundAmount)

  // Side effect: update inventory (restock)
  await restockItems(order.items)
}
```
```

### Extraction technique: read tests first

Tests are the best source of business rules — they state behavior as assertions.

| Test pattern | Extracted rule |
|---|---|
| `it('should reject orders with 0 items')` | Order must have ≥1 item |
| `it('should apply 10% discount for premium users')` | Premium users get 10% discount |
| `it('should not allow cancellation after shipping')` | Cancellation blocked after shipment |
| `expect(user.loginAttempts).toBeLessThan(5)` | Account locks after 5 failed logins |

Cross-reference rules from tests with service/model code to confirm and add detail.

---

## PHASE 4 — Assembly

### Document structure

```markdown
# {Project Name} — Domain & Business Logic Reference

{2-3 sentence overview: what this system does as a product, who uses it, what the core domain is.}

## Domain Model

### {Entity 1}
{fields, relationships, invariants, lifecycle}

### {Entity 2}
...

## Business Rules

### {Rule Cluster 1}
{rules + annotated code}

### {Rule Cluster 2}
...

## Summary

{1-2 paragraphs: how entities and rules compose into actual product behavior. Key workflows, cross-entity invariants, top "gotchas".}
```

**Heading structure**: two-level — `## Domain Model` and `## Business Rules` as top groupings, `###` for individual entities and rule clusters. Differs from flat-H2 library llms.txt because domain knowledge has natural grouping that aids RAG (a query about "order validation" should retrieve the Order entity AND order-related rules — grouping headers help retrievers).

### Assembly rules

1. H1 includes project name + "Domain & Business Logic Reference" qualifier (distinguishes from API references).
2. Entity sections before rule sections — nouns before verbs.
3. Order entities by centrality: core domain (e.g., `Order` in e-commerce) first, then related, then supporting.
4. Order rules by frequency: most-triggered first, edge cases last.
5. Cross-reference using entity names — same name as in domain model section.
6. Summary ties model and rules: "Orders go through these states, governed by these rules, interacting with these entities."

### Token budget

Same as llms-txt-generator:
- Overview: ~200 tokens
- Domain model: ~40% of remaining
- Business rules: ~50% of remaining
- Summary: ~200 tokens
- Default total: 10K. 5K small / 15-20K complex domains.

---

## PHASE 5 — Output

### File naming

- Default: `{project-name}.business-logic.md`
- Alt: `{project-name}.domain.md`
- User-specified: use it

### Save location

- In codebase: repo root or `docs/`
- Always copy to `/mnt/user-data/outputs/` for download

---

## Quality Checklist

- [ ] Every entity section: purpose, key fields with semantics, relationships, ≥1 invariant
- [ ] Every business rule stated as plain-English condition, not just code
- [ ] Code from actual codebase, annotated — not synthetic
- [ ] Lifecycle/state transitions documented for entities that have them
- [ ] Test-extracted rules cross-referenced with implementation
- [ ] Doc answers "what does this system do" not "how is it built"
- [ ] No framework/infra details unless they encode business rules (Prisma `@unique` IS a business rule)
- [ ] Summary connects entities and rules into coherent product behavior
- [ ] Cross-references use consistent naming

---

## Edge Cases

- **No tests**: Lean on service layer, validation files, constants. Warn user that confidence is lower.
- **Anemic domain model**: If models are data bags and logic is in services, document services as primary source. Note the architecture pattern.
- **Microservices**: Focus on current service's bounded context. Document integration contracts (what this service expects from others) as a separate section if relevant.
- **Heavy ORM magic**: Surface hidden logic (ActiveRecord callbacks, Hibernate hooks, Prisma middleware) — invisible business rules.
- **Feature flags**: Document behavior under each flag state. Flags ARE business rules.
- **Legacy / no clear structure**: Find densest clusters of conditionals and validation. Trace core transaction flow ("what happens when a user pays?") and document along the way.
