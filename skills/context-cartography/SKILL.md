---
name: context-cartography
description: Use when designing what goes into an agent's context window — system prompts, tool definitions, retrieval results, or any context artifact assembled before the agent runs. Triggers on "what should I put in the system prompt?", "how do I structure my context?", "the agent loses track of...", "my context window is full", "how do I decide what to include?", "designing a new harness", "the agent ignores my instructions". Do NOT use for one-off prompts, runtime conversation management, or when the problem is model capability rather than context design.
---

# Context Cartography

Design what goes into an agent's context window — and what stays out.

## The Boundary Rule

```
Designing or redesigning a context window?     →  Use this skill.
Context window is full and you need to cut?    →  Start at the TRIAGE entry point.
Need to validate whether your design works?    →  Use EDD after this skill.
One-off prompt or exploratory prototyping?     →  Don't use this skill.
```

## Two Entry Points

**Entry A — Full Design** (greenfield/major redesign): All six steps: TASK → SURVEY → PRIORITIZE → SIZE → STRUCTURE → CUT.

**Entry B — Triage** (context too big): Start at CUT. If cuts reveal the wrong information is prioritized, work backwards through PRIORITIZE and SIZE.

---

## The Flow

### Step 1 — TASK

What will the agent do with this context? Be specific. Not "code assistance" but "review pull requests for a Python microservices codebase, checking style, correctness, and security."

Write it as a single sentence. If you need two, you may need two context configurations.

**Output**: One-sentence task definition.

### Step 2 — SURVEY

Enumerate all candidate context sources. Don't filter yet. Common sources:

- System instructions / role definition
- Tool definitions and schemas
- Code files (source, tests, configs)
- Documentation (internal, API docs, specs)
- Style guides / conventions
- Architecture descriptions
- Git history / recent changes
- Conversation history
- Retrieved documents (RAG)
- Examples (few-shot)
- Error logs / stack traces
- External references (URLs, schemas)

**Output**: Complete list with estimated token cost for each.

### Step 3 — PRIORITIZE

| Priority | Meaning | Rule |
|----------|---------|------|
| **P0 — Essential** | Agent cannot do the task without this | Always include |
| **P1 — Important** | Significantly improves quality | Include if budget allows |
| **P2 — Useful** | Helps with edge cases or polish | Include only if space remains |
| **P3 — Irrelevant** | Does not affect this task | Never include |

**The non-obvious call**: P1 items that *seem* essential but aren't (false P0), and P2 items that turn out to be load-bearing (hidden P0). The pattern catalog flags these.

**Output**: Prioritized list with P0/P1/P2/P3 ratings.

### Step 4 — SIZE

For each P0 and P1 source, choose detail level:

```
Will the agent MODIFY this content?      → Full source
Will the agent CALL or REFERENCE it?     → Signatures + docstrings
Need to know it EXISTS and what it does? → One-line summary
Need the SHAPE of the system?            → Structural overview
```

**Common mistakes**: full source for files only referenced (waste); only summaries for files being modified (insufficient); uniform detail level (no signal hierarchy).

**Output**: Each P0/P1 source with size decision.

### Step 5 — STRUCTURE

1. **Task-relevant context goes closest to the instruction.** Most important info last (near user message) or first (system prompt opening).
2. **Label sections explicitly.** Headers describe WHAT and WHY. Not `## Code` but `## Source code to review — check style, correctness, security`.
3. **Separate instructions from reference.** Mixing causes agent to treat reference as instructions or vice versa.
4. **Use consistent formatting.** One structure (markdown, XML, delimiters) throughout.
5. **Self-documenting.** A reviewer should be able to tell why each section is included from its header.

**Output**: Structured layout with section headers and ordering.

### Step 6 — CUT

1. List every context element (from STRUCTURE)
2. State the specific agent behavior each supports
3. Can't state behavior in one sentence → **cut candidate**
4. Two elements support same behavior → keep more token-efficient one
5. For each cut candidate, verify via EDD ablation

**Additive alternative**: Start with ONLY P0, add P1 one at a time, measure each. Sidesteps loss aversion.

**Shadow context**: Don't delete cut items. Move to a shadow set; re-test when production anomalies occur — a cut item may be load-bearing for edge cases evals don't cover.

**Output**: Final context window + shadow context list.

---

## Pattern Catalog

Concrete prioritization patterns. Each lists what matters more/less than developers expect.

### Code Generation

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| Task specification | P0 | Expected |
| Files new code interacts with (full) | P0 | Expected |
| Existing test patterns | P0 | **Often missed** — without these, code follows generic patterns |
| Naming conventions / style guide | P1 | **Often missed** — models default to training distribution |
| Type definitions / interfaces | P1 | Expected |
| Architectural constraints | P1 | Expected |
| Unrelated modules | P3 | **Often included** — adds noise |
| Full git history | P3 | **Often included** — recent diff may be P1, full log is noise |

### Code Review

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| Diff / changed files (full) | P0 | Expected |
| Style guide / linting rules | P0 | **Often P1'd** — without it, reviews are generic |
| Test files for changed code | P0 | **Often missed** — can't assess coverage without seeing tests |
| Architectural constraints | P1 | Expected |
| Related affected files | P1 | Expected |
| PR description / ticket | P1 | **Often missed** — reviewer lacks intent, reviews syntax not semantics |
| Unrelated modules | P3 | Expected |
| Build / CI config | P3 | **Often included** |

### Debugging

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| Error output / stack trace | P0 | Expected |
| Source files in trace (full) | P0 | Expected |
| Recent changes (git diff) | P0 | **Often missed** — "what changed?" is the #1 question |
| Related test files | P1 | Expected |
| Dependency versions / env | P1 | **Often missed** — version mismatches cause subtle bugs |
| Reproduction steps | P1 | Expected |
| Unrelated source files | P3 | Expected |
| Full git log | P3 | Recent diff is P0; full history is noise |

### Multi-Step Planning / Architecture

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| High-level architecture | P0 | Expected |
| File/directory structure | P0 | **Often missed** — needs system shape, not file contents |
| Constraints (perf, compat, deadlines) | P0 | **Often missed** — plans without constraints are wish lists |
| Dependency graph | P1 | Expected |
| Existing patterns | P1 | Expected |
| Full source of any file | P2 | **Often P0'd** — planning needs structure, not implementation |
| Test files | P2 | Not relevant until implementation |

### Q&A Over Documentation

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| Relevant doc sections | P0 | Expected |
| Glossary / terminology | P0 | **Often missed** — domain jargon causes hallucination |
| Examples from docs | P1 | Expected |
| Source code | P2 | **Often P0'd** — only relevant if question is about implementation |
| Full doc corpus | P3 | **Often included** — retrieval should select, not dump |

### Test Writing

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| Implementation under test (full) | P0 | Expected |
| Existing test files (patterns) | P0 | **Often missed** — without these, tests follow generic framework patterns |
| Test framework docs / helpers | P1 | Expected |
| Edge cases from specs/tickets | P1 | **Often missed** — happy path only without spec-derived edges |
| Mock/fixture patterns | P1 | **Often missed** — agent invents new patterns |
| Unrelated source files | P3 | Expected |

---

## The Context Manifest

The skill's output artifact. Feeds into EDD for validation.

```yaml
task: "Review pull requests for Python microservices — style, correctness, security"
token_budget: 8000
date: 2026-03-19

sources:
  - name: "PR diff"
    priority: P0
    size: full
    tokens_est: 2000
    supports: "Agent can see what changed"
  - name: "Style guide"
    priority: P0
    size: full
    tokens_est: 800
    supports: "Agent checks project-specific conventions, not generic ones"
  - name: "Test files for changed code"
    priority: P0
    size: full
    tokens_est: 1500
    supports: "Agent can assess test coverage of changes"
  - name: "PR description / ticket"
    priority: P1
    size: full
    tokens_est: 300
    supports: "Agent reviews intent, not just syntax"
  - name: "Architecture doc"
    priority: P1
    size: summary
    tokens_est: 400
    supports: "Agent catches architectural violations"

shadow:
  - name: "CI config"
    reason_cut: "Did not change review assertions in ablation test"
  - name: "Full git log"
    reason_cut: "Recent diff (in PR diff) was sufficient"

structure:
  order:
    - "System instructions (role + review criteria)"
    - "Style guide"
    - "Architecture summary"
    - "PR description"
    - "Test files"
    - "PR diff (closest to instruction)"
  rationale: "Task-relevant content (diff) placed last, near user message. Reference material earlier for lookup."
```

The manifest is **versionable**, **diffable**, **testable** (EDD writes assertions against `supports` claims), **auditable**.

---

## Integration with EDD and Context-Eval

| Phase | Skill | What happens |
|-------|-------|-------------|
| **Design** | context-cartography | Produce a context manifest |
| **Validate** | EDD | Write assertions from `supports` claims, run evals |
| **Measure** | context-eval | Pass rates, benefit-per-kilotoken, deadwood |
| **Iterate** | Loop back | Eval failures → update manifest → re-run |

If a source claims "Agent checks project-specific conventions" but the eval shows generic conventions, that source isn't earning its tokens — redesign or cut.

---

## Maintenance: When to Resurvey

- **Task scope changes** — agent asked to do things the manifest wasn't designed for
- **Model upgrade** — new model may need less or differently-structured context
- **Eval scores plateau or regress** — current design hit ceiling
- **Token budget changes** — what was cut may now fit

Treat the manifest like code: review, version, test.

---

## Anti-Patterns

| Anti-pattern | Symptom | Fix |
|-------------|---------|-----|
| **Context stuffing** | Include everything "just in case" | Start P0 only, add P1 one at a time with measurement |
| **Uniform sizing** | Every file at full detail | Use SIZE decision tree |
| **Missing legend** | No headers or labels | Label everything with WHAT and WHY |
| **Priority inversion** | P2 items at full detail while P0 summarized | Highest detail to most important info |
| **Stale manifest** | Designed 6 months ago, task evolved | Resurvey |
| **Solo without validation** | Designed but never tested | Always follow with EDD |
| **Cargo-culting patterns** | Copying catalog patterns without adapting | Patterns are starting points |
