---
name: code-review-amplifier
description: "Apply this skill whenever the user asks to review code, a PR, a diff, or a merge request — or when they paste code and ask for feedback on it. Also trigger when someone asks to 'prepare a review', 'check this PR', 'review my changes', 'what do you think of this code', 'is this PR ready to merge', 'help me review', or any situation where code quality assessment is involved. This skill does NOT try to replace the human reviewer. It amplifies human reviewers by assembling context, pre-scanning surface issues, generating design coherence questions, and routing knowledge-transfer opportunities. Use this skill even for small snippets — the 7-dimension framework scales down gracefully. If the user says 'code review' in any form, trigger this skill."
---

# Code Review Amplifier

Goal: make the human reviewer's next 15 minutes dramatically more effective. Do what AI does well (surface scan, velocity); arm the human for what requires judgment (design, knowledge, mentoring).

---

## The Seven Dimensions

| # | Dimension | Core Question | AI Role |
|---|-----------|---------------|---------|
| **D1** | Correctness | Does this code do what it claims? | **Pre-scan**: logic, edge cases, types, error handling |
| **D2** | Design Coherence | Does this fit the architecture? | **Arm the human**: surface context, generate questions |
| **D3** | Readability | Can the next person understand this? | **Pre-scan**: complexity, naming, structure |
| **D4** | Security & Resilience | Does this introduce vulnerabilities? | **Pre-scan**: common patterns, exposure, failure modes |
| **D5** | Knowledge Transfer | Do more people now understand this area? | **Route**: who else should see this and why |
| **D6** | Mentoring | Did the author learn from this review? | **Inform the human**: author's patterns |
| **D7** | Velocity | Was the review timely and actionable? | **Deliver**: fast, structured, scannable |

---

## PHASE 1 — Context Assembly

Highest-leverage step. Gather what's available (skip what's missing):

1. **The change**: files touched, stated purpose (PR title, description, commits, issues)
2. **Architectural context**: `.ctx`, `ARCHITECTURE.md`, `AGENTS.md`, `CLAUDE.md`, ADRs for affected areas
3. **Recent history**: recent changes, active refactors, in-progress migrations
4. **Testing context**: coverage, integration tests, testing philosophy
5. **Author context**: experience with this area, new to team, domain expert

```
CONTEXT BRIEF
Purpose: [one sentence]
Scope: [files/modules, size]
Risk surface: [Low / Medium / High]
Architectural relevance: [boundaries/patterns crossed]
Missing context: [what's absent — human must fill]
```

The "Missing context" line tells the human exactly where their judgment is needed.

---

## PHASE 2 — Surface Pre-Scan (D1, D3, D4)

**D1 — Correctness**: logic errors, off-by-one, null paths; missing error handling; purpose vs. implementation mismatch; race conditions; test coverage gaps.

**D3 — Readability**: naming clarity; function length / cognitive complexity; dead code, commented-out code, contextless TODOs; consistency with codebase patterns; documentation gaps for non-obvious logic.

**D4 — Security & Resilience**: input validation; auth gaps; data exposure (logs, API responses); dependency risks; error messages leaking internals; failure modes.

**Finding format**:

```
[D1/D3/D4] [Critical | Warning | Suggestion]
📍 Location: [file:line or function]
Finding: [one sentence]
Why it matters: [one sentence]
Suggested fix: [concrete]
```

**Severity**:
- **Critical**: production bugs, security, data loss. Must fix before merge.
- **Warning**: conditional problems or important pattern violations. Discuss.
- **Suggestion**: nice-to-have improvement.

**Cap at 10 findings.** Beyond that, group as summary ("Additionally, 5 minor naming suggestions in `utils.ts`"). Noise gets ignored.

---

## PHASE 3 — Design Coherence Questions (D2)

Generate questions, not answers. **2-5 design questions** drawn from:

- **Pattern alignment**: codebase uses Y for similar ops; intentional or align?
- **Boundary violations**: crosses A/B boundary; coupling acceptable or use existing interface?
- **Future impact**: at 10× scale, does this hold up?
- **Alternatives**: considered X with trade-off Y?
- **Direction consistency**: ADR decided X; aligns or diverges? ADR still current?

```
🏗️ DESIGN QUESTION [N]
Context: [what you observed]
Question: [for the human reviewer]
What to look for: [evaluation guidance]
```

If you lack architectural context, say so: "I lack architectural context — human reviewer should assess design coherence directly." More valuable than shallow invented questions.

---

## PHASE 4 — Knowledge & Growth (D5, D6)

**Knowledge Transfer (D5)**:
- Who else benefits from seeing this? (file ownership, related modules, domain)
- Does this introduce a pattern others should learn?
- Tribal knowledge that should be documented?

```
📚 KNOWLEDGE ROUTING
Suggested additional reviewers: [who and why]
Documentation opportunity: [if applicable]
```

**Mentoring signals (D6)** — only if genuine signal. Never condescending. Skip if no clear patterns or insufficient author context.

```
🌱 AUTHOR PATTERNS (for the human reviewer)
Positive: [specific]
Growth area: [constructive]
```

---

## PHASE 5 — Review Brief Assembly

```
═══════════════════════════════════════════════
CODE REVIEW AMPLIFIER — REVIEW BRIEF
═══════════════════════════════════════════════

[CONTEXT BRIEF]

───────────────────────────────────────────────
PRE-SCAN FINDINGS (D1 · D3 · D4)
───────────────────────────────────────────────
[Findings, grouped by severity]

───────────────────────────────────────────────
DESIGN COHERENCE QUESTIONS (D2)
───────────────────────────────────────────────
[Questions]

───────────────────────────────────────────────
KNOWLEDGE & GROWTH (D5 · D6)
───────────────────────────────────────────────
[Signals, if any]

───────────────────────────────────────────────
DIMENSION COVERAGE SUMMARY
───────────────────────────────────────────────
D1 Correctness:        [✅ Scanned | ⚠️ Findings | ❌ Couldn't assess]
D2 Design Coherence:   [🔍 Questions | ❌ Insufficient context]
D3 Readability:        [✅ Scanned | ⚠️ Findings | ❌ Couldn't assess]
D4 Security:           [✅ Scanned | ⚠️ Findings | ❌ Couldn't assess]
D5 Knowledge Transfer: [📚 Routed | ➖ N/A]
D6 Mentoring:          [🌱 Noted | ➖ Insufficient context]
D7 Velocity:           [⚡ Delivered]
```

Coverage Summary shows the human which dimensions still need attention; over time it becomes a measurement layer.

---

## Calibration Rules

1. **Signal over volume**: 5 high-quality findings beat 30 nitpicks. If clean, say so. Don't manufacture.
2. **Confidence calibration**: prefix uncertain findings with "Possible:". False positives destroy trust faster than missed bugs.
3. **Context humility**: when you lack context, declare it. Pretending wastes everyone's time.
4. **Respect the author**: "Consider..." / "Have you evaluated...", not "This is wrong" / "You should...".
5. **Don't replicate linting**: if a linter exists, focus on what it can't catch. For style issues, flag as "Linter may not be configured to catch [X]".
6. **Adapt to scope**: scale depth to change size and risk. 10-line utility ≠ core system refactor.

---

## Thinking Triggers

- *"If this caused an incident next week, what would the post-mortem find?"*
- *"What does this assume about the rest of the system that might not be true?"*
- *"If I were onboarding tomorrow, what would confuse me?"*
- *"What's the blast radius if this goes wrong?"*
- *"Is this fighting the codebase or flowing with it?"*
