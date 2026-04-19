---
name: rule-quality-evaluator
description: "Evaluate the quality of existing agent instruction rule sets — CLAUDE.md, AGENTS.md, .cursorrules, copilot-instructions.md, or any coding-agent context file. Use this skill whenever someone asks to audit, score, or improve their agent rules; wants to know if their instructions are effective; or describes rules that aren't changing agent behavior. Trigger on phrases like 'are my rules good?', 'why is the agent ignoring my instructions?', 'score my CLAUDE.md', 'audit my agent rules', 'are these instructions effective?', 'review my copilot-instructions.md', 'my rules aren't working', 'evaluate my context file', or any situation where a human has an existing instruction file and wants to know whether it will actually improve agent behavior. Also trigger when someone has just run agent-instruction-forge and wants to verify the output before committing."
---

# Rule Quality Evaluator

A rule that cannot be violated cannot be followed. Most instruction files fail because of unfalsifiable guidance, redundant noise, and implicit knowledge that never made it to paper. Score rules against seven properties, identify structural weaknesses, optionally verify with live tasks.

## Two-Phase Overview

- **Phase 1 — Static Critic** (always): Read rules, score against Seven Properties, detect structural issues, produce scorecard. No agent execution.
- **Phase 2 — Behavioral Test** (opt-in): Generate coding tasks, derive assertions, hand off to context-eval, synthesize report.

**Interview-only fallback**: If no instruction file accessible, ask user to paste rules. Flag at end: "I can't verify codebase alignment — code pattern checks need manual verification."

---

## Phase 1 — Static Critic

### Step 1: Ingest

Read instruction file(s). Detect format (Markdown prose, structured rules list, YAML front matter, fenced sections). Parse into individual rules — one rule = one discrete behavioral instruction. Split on bullets, numbered items, or paragraph breaks starting an imperative.

Optionally scan codebase for linter configs (`.eslintrc`, `pyproject.toml`, `ruff.toml`), type configs (`tsconfig.json`), CI configs (`.github/workflows/`). Enables redundancy detection.

### Step 2: Score Each Rule — The Seven Properties

Score 0–7 by counting properties satisfied (each binary).

| Property | ID | Score 0 | Score 1 |
|---|---|---|---|
| Specific and falsifiable | P1 | "Write clean code" | "Every API handler must return `Result<T, AppError>`, never throw" |
| Encodes WHY | P2 | "Don't use console.log" | "Don't use console.log — use `src/lib/logger.ts`. Bypasses correlation IDs, breaks Datadog traces" |
| Born from real failure | P3 | "Handle errors carefully" | "Never add indexes to `reservations` without DBA approval — compound index locked table 47 min in Q2 2024" |
| Scoped to right level | P4 | Rule about billing API in root file | Same rule in `src/billing/CLAUDE.md` |
| Points to canonical example | P5 | "Follow our API patterns" | "New endpoints follow `src/api/reservations/create.ts` — handler → validation → service → response" |
| Includes anti-pattern | P6 | "Use the service layer" | "We do NOT use the repository pattern. Each service calls Prisma directly" |
| Token-efficient | P7 | "When writing tests, please make sure to always use Vitest and not Jest" | "Tests: Vitest, never Jest. Config: `vitest.config.ts`" |

**Score ≤ 2 = weak** — rewrite/remove candidate.
**P1 = 0 = noise** — agent can't verify, can't steer.

### Step 3: Structural Analysis

**Redundancy**: Flag rules duplicating linter (ESLint, Ruff, Pylint), type system (TypeScript strict, mypy), or CI (test gates, build gates). Redundant rules waste budget and dilute signal.

**Scope**: "Does this rule apply to ALL code agent will see in this directory?" Flag:
- **Over-scoped**: package-specific rule in root file
- **Under-scoped**: identical rules duplicated across subdirs that should move up

**Coverage** — map to nine categories:
- C1 Architecture & Boundaries
- C2 Domain Model & Business Rules
- C3 Conventions & Patterns
- C4 Integrations & External Dependencies
- C5 Operations & Deployment
- C6 Testing Philosophy & Strategy
- C7 Security Model
- C8 Performance Constraints
- C9 Historical Decisions & Tech Debt

Mark `●` (covered), `◐` (partial), `○` (missing).

**Token budget**:
- Claude Code: root <4,000 tokens, subdir <1,000
- Copilot: root <1,000 lines, first 4,000 chars read per code review
- Cursor / Windsurf / AGENTS.md: similar to Claude Code

### Step 4: Produce Scorecard

Output, then ask whether to run Phase 2.

---

#### Rule Scorecard — `[file path]`

| Rule (truncated) | Score | Weakest Property | Flags |
|---|---|---|---|
| "…" | N/7 | P? | weak / noise / redundant / over-scoped |

#### Summary Stats

- Total rules: N
- Mean score: X.X / 7
- Strong (5–7): N | Adequate (3–4): N | Weak (0–2): N
- Noise rules (P1 = 0): N
- Redundant with linter/CI/types: N
- Over-scoped: N | Under-scoped: N

#### Coverage Map

```
C1[●] C2[○] C3[●] C4[○] C5[◐] C6[●] C7[○] C8[○] C9[○]
● covered  ◐ partial  ○ missing
```

#### Token Budget

- Current: ~N tokens / N chars
- Limit: [system-appropriate]
- Headroom: [remaining / over by N]

#### Top 3 Improvements

1. [Most impactful — which rule, which property, what to add]
2. [Second]
3. [Third]

#### Phase 1 Verdict

| Threshold | Verdict |
|---|---|
| Mean ≥ 5 | **STRONG** — specific, grounded, efficient |
| Mean 3–4 | **ADEQUATE** — usable but with gaps |
| Mean < 3 | **WEAK** — won't reliably steer behavior |

---

**Run Phase 2 — Behavioral Testing?** Generates real coding tasks, measures whether rules change agent behavior. Requires context-eval.

---

## Phase 2 — Behavioral Test

### Step 5: Generate Coding Tasks

Generate 3 coding tasks. Each:
- ~50 lines of code to produce
- Touches 2+ rules (discriminating grading)
- Prioritize: rules scoring 3-5 (uncertain), C7 Security or C2 Domain (high-stakes), incident-born rules (P3 = 1)

Per task: which rules exercised, what correct behavior looks like.

### Step 6: Generate Assertions

One testable assertion per rule:
- Observable in agent output (no execution required)
- Pass/fail check

Write to `evals/evals.json`:

```json
{
  "harness_name": "[instruction file name]",
  "harness_type": "coding agent instruction rules",
  "harness_path": "[path to instruction file]",
  "evals": [
    {
      "id": 1,
      "prompt": "[the coding task prompt]",
      "expected_output": "[description of correct output under the rules]",
      "files": [],
      "assertions": [
        "[rule → assertion, e.g., 'Uses src/lib/logger.ts, not console.log']",
        "[second rule → assertion]"
      ]
    }
  ]
}
```

### Step 7: Hand Off to context-eval

Harness under test = instruction file. Baseline = same tasks without the file.

```
→ context-eval: evaluate harness at [instruction file path] using evals/evals.json
```

context-eval runs with/without harness, grades, computes benefit delta.

### Step 8: Synthesize Report

---

#### Combined Report

**Phase 1 Static**: [mean] / 7 → [STRONG / ADEQUATE / WEAK]

**Phase 2 Behavioral Delta**: +[delta] pass rate over baseline

#### Per-Rule Behavioral Confirmation

| Rule | P1 Verdict | P2 Delta | Confirmed? |
|---|---|---|---|
| "…" | score/7 | +X% | yes / partial / no |

#### Final Verdict

| Condition | Verdict |
|---|---|
| Static ≥ 5 AND delta ≥ 0.25 | **STRONG** — well-formed, measurable improvement |
| Static ≥ 3 AND delta ≥ 0.10 | **ADEQUATE** — works, room to improve |
| Static < 3 OR delta < 0.10 | **WEAK** — not reliably changing behavior |
| Delta < 0 | **HARMFUL** — degrading performance |

Delta = pass-rate diff between with-rules and without-rules (0.0–1.0; 0.25 = 25 pp).

#### Discrepancies

Rules high in Phase 1 with no behavioral delta (or vice versa) — most actionable findings. High-score + no delta = either not reachable in eval tasks or not being read. Low-score + high delta = encodes something valuable scoring missed.

---

## Calibration Rules

1. **Phase 1 always first.** Scorecard catches most failures without tooling.
2. **P1 is the gatekeeper.** Unfalsifiable rules can't be improved by other properties. Fix specificity first.
3. **Redundancy is the easiest win.** Lint/type/CI duplicates can be deleted immediately.
4. **Behavioral testing is gold standard, not default.** Phase 2 needs infrastructure and time. Most rule sets benefit more from targeted Phase 1 rewrites.
5. **Score what you see.** Literal text, not charitable interpretation. Rules requiring generous reading fail in practice.

---

## Composes With

`context-gap-analyzer` → `agent-instruction-forge` → `rule-quality-evaluator` → `context-eval`
