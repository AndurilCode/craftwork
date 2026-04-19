---
name: agent-instruction-forge
description: "Guide humans through creating effective instruction rules for coding agents (Copilot, Claude Code, Cursor, Windsurf, Aider, AGENTS.md, CLAUDE.md, .cursorrules, copilot-instructions.md). Trigger when someone asks to create, improve, or write agent instructions, copilot rules, AI coding guidelines, context files, or anything shaping agent behavior. Also trigger on 'agent keeps making mistakes', 'make Copilot follow our conventions', 'write rules for repo', 'set up agent context'. Runs an interactive extraction process — reads codebase first, then guides the human through targeted questions to surface implicit knowledge (past failures, non-obvious conventions, architectural decisions) that code alone can't tell an agent. For analyzing gaps in existing context, use context-gap-analyzer. This skill *creates* the rules."
---

# Agent Instruction Forge

Exceptional agent instructions encode *specific implicit knowledge*, not generic advice. Generic rules ("write clean code") hurt performance (ETH Zurich 2024: LLM-generated context files reduce success ~3%). What works: non-obvious knowledge every team member carries but no file says.

**Modes** (detected in Phase 1):
- **Greenfield**: No instruction files. Read codebase, extract, synthesize.
- **Augment**: Files exist. Audit, validate against code, fill gaps, strengthen.
- **Interview-Only**: No codebase access. Skip Phase 1 Steps 2-4. Lean on Failure Round + Resource Ingestion. Flag: "Can't validate against code — file paths need manual verification."

---

## Seven Properties of a Great Rule

1. **Specific & falsifiable** — agent can verify compliance. Unfailable = not a rule.
   `"Write clean code"` → `"Every external API call must return Result<T, AppError>, never throw."`

2. **Encodes WHY** — without rationale, agents optimize around rules.
   `"Don't use console.log"` → `"Use src/lib/logger.ts — console.log bypasses Datadog correlation IDs."`

3. **Born from real failure** — past pain produces specificity.
   `"Never add indexes to reservations table without DBA approval — Q2 2024 compound index locked table 47min."`

4. **Scoped correctly** — highest directory where universally true. Test: "Applies to ALL code agent sees in this directory?" If not, push deeper.

5. **Points to canonical example**.
   `"New endpoints follow src/api/reservations/create.ts — handler → validation → service → response."`

6. **Includes anti-pattern** — overrides training priors when codebase deviates.
   `"We do NOT use repository pattern. Services call Prisma directly."`

7. **Token-efficient**.
   `"When writing tests, please make sure to use Vitest and not Jest."` → `"Tests: Vitest, never Jest."`

### Rules Should NOT Contain

- Things fixable in code (better type signature, clearer name, linter rule)
- Things linting already enforces
- Language documentation (agent knows the language)
- Obvious patterns derivable from reading the code
- Aspirational rules nobody follows (document reality unless explicitly marked aspirational)

---

## PHASE 1 — Codebase Discovery (Automated)

Read codebase before asking anything. Don't ask what code already answers.

### Step 1: Discover instruction infrastructure

Scan: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `.github/prompts/*.prompt.md`, `.context/`, `.ctx`, `README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, ADR dirs, formatter/linter configs, `tsconfig`/`pyproject.toml`, `Makefile`/`justfile`, CI/Docker configs.

For each file: topics, staleness, format/tone.

### Step 2: Codebase topology

Map: languages, frameworks, package managers, directory structure (2-3 levels), entry points, test structure, external integrations.

### Step 3: Pattern extraction

Sample 3-5 files from most-modified directories (`git log --stat` or inferred from size/complexity). Detect: naming, error handling, import organization, logging, test patterns.

### Step 3b: History mining (if git/PR available)

`git log` for reverts, migrations, convention enforcement, hotfixes — each encodes an implicit rule. Keywords: convention, instead, revert, breaking, deprecated, don't.

PR access (`gh pr list --state merged --limit 30`): scan review corrections ("nit:", "use X instead"), architectural rationale in descriptions, repeated feedback. Capture: source, candidate rule, category (C1-C9), confidence.

If unavailable: ask in Phase 2: "Patterns you correct repeatedly in reviews but aren't documented?"

### Step 4: Rule Audit (Augment Mode Only)

For each existing rule:

- **Seven Properties Score** (0-7). Flag <=2. P1 failure (specific/falsifiable) = noise regardless of other scores.
- **Code Alignment**: Confirmed | Stale | Aspirational | Contradicted | Unverifiable
- **Coverage**: C1 Architecture, C2 Domain/Business, C3 Conventions, C4 Integrations, C5 Operations, C6 Testing, C7 Security, C8 Performance, C9 Historical Decisions
- **Redundancy**: duplicated by lint/types/CI? Contradicts other rules?
- **Scope**: over-scoped (push down), under-scoped (pull up), wildcard abuse, missing intermediate levels

Output:
```
Rule | Score | Alignment | Scope | Verdict (Keep/Rewrite/Verify/Remove/Re-scope)
Summary: N total → keep[n] rewrite[n] verify[n] remove[n] re-scope[n]
Coverage: C1[●/◐/○] ... C9[●/◐/○]
Token budget: ~[current] / [limit] — headroom: [remaining]
Scope health: [N] correct, [N] over-scoped, [N] under-scoped
```

### Step 5: Discovery Brief

- **Greenfield**: target system, what code reveals, top candidate rules from history, highest-value gaps
- **Augment**: rule health summary, top issues, undocumented rules from history, coverage gaps

Verify: any "remove" rules actually important? "Confirmed" rules outdated? Which history-surfaced rules are real conventions? Which gaps matter most?

---

## PHASE 2 — Knowledge Extraction (Interactive)

2-4 questions per round. Don't dump 20.

**In Augment mode**, weave three workstreams:
1. **Verify** flagged rules: "This rule says [X]. Still accurate?"
2. **Fill** coverage gaps: skip well-covered categories, focus on empty ones
3. **Strengthen** weak rules: "Why? What goes wrong otherwise?" / "File that best exemplifies this?"

**Prioritize** areas where (a) agent writes code most often, (b) code is most ambiguous, (c) existing rules are weakest.

### Round 1 — Failures (Always Start Here)

Highest-signal source. Ask 2-4:
- "Last time a developer (human or AI) made a frustrating mistake — what happened, what should they have done?"
- "Landmines where the obvious approach leads to subtle bugs?"
- "Most common mistake from new team members?"
- "Recurring annoyances in agent-generated code you fix every time?"

Probe: "Point me to a file?" / "Correct version?" / "Why this way?"

### Round 2 — Conventions
Where codebase deviates from framework defaults — where agent training priors mislead.
- "Where does your codebase intentionally deviate from the framework's recommended approach?"
- "Patterns you enforce in code review that linting/CI doesn't catch?"
- "One rule that eliminates 50% of review nit-picks?"

### Round 3 — Architecture
Module boundaries, data flow, where new code goes.
- "How should an agent decide which module/directory new code goes in?"
- "Files that shouldn't be modified without extra caution?"
- "How does data flow for the most common operation?"

### Round 4 — Integrations (if external services detected)
API quirks, dependency approval process, wrapper conventions.

### Round 5 — Testing
Philosophy, patterns to follow/avoid, mock boundaries.

### Round 6 — Resource Ingestion (optional)
"Any existing resource I should read? (Wiki, ADR, Slack thread, postmortem)" — extract using Seven Properties.

**Adapt** by: codebase type (frontend→components, backend→endpoints), team size (solo→future-self, large→consistency), agent system (Copilot→completion-level, Claude Code→task-level), human energy (target 15-20 min).

---

## PHASE 3 — Synthesis

### Greenfield Mode
```markdown
# [Project] — Agent Instructions
## Philosophy — [2-3 sentences anchoring judgment]
## Critical Rules — [violations break things: what + why + anti-pattern]
## Conventions — [review friction: pattern + example file]
## Architecture — [boundaries, data flow, where new code goes]
## Testing — [philosophy + patterns + mock boundaries]
```

### Augment Mode
Do NOT rewrite from scratch. Produce a reviewable changeset:
1. **Remove** low-signal rules
2. **Rewrite** rules in place, preserving grouping/tone
3. **Add** rules for coverage gaps
4. **Re-scope** rules to appropriate directory
5. Show delta from Phase 1

Per edit: what changed, why. Include before/after example.

### Both Modes
- Scope: root=universal, package-level=local, `applyTo` globs only when truly file-type-specific
- Every rule specific and falsifiable (P1)
- Order by impact (critical first — long files may truncate)
- Match existing format/tone in augment mode

### Token Budgets

| System | Unit | Root limit | Notes |
|--------|------|-----------|-------|
| Copilot | chars | <1000 lines | Code review reads first 4000 chars/file |
| Claude Code | tokens | <4000 | Subdir: <1000 tokens |
| Cursor/Windsurf/AGENTS.md | tokens | ~4000 | Similar to Claude Code |

When WHY and brevity conflict, keep WHY. Main lever: scope rules down to reduce root file size.

---

## PHASE 3b — Adversarial Validation

Before showing rules, stress-test with three isolated subagents receiving ONLY the synthesized file. Read `references/adversarial-validation.md` for prompts.

Run in parallel:
1. **Newcomer** — finds gaps
2. **Prior Override** — checks rules beat common training priors
3. **Contradiction Finder** — finds conflicts and ambiguities

Update rules. Include summary of gaps, weak spots, resolved contradictions.

---

## PHASE 4 — Review & Delivery

Present rules. Iterate on feedback.

**Write to target:**

| System | Files |
|--------|-------|
| Copilot | `.github/copilot-instructions.md` (repo-wide) + `.github/instructions/NAME.instructions.md` (scoped) + `.github/prompts/NAME.prompt.md` |
| Claude Code | `CLAUDE.md` (root + subdirs) |
| Cursor | `.cursorrules` |
| Windsurf | `.windsurfrules` |
| Generic | `AGENTS.md` (root + subdirs) |

If target unclear, ask. If multiple, generate for primary. Copilot always uses three-layer structure.

After delivery: suggest running agent on a real task. Next mistake = next rule. Revisit monthly.
