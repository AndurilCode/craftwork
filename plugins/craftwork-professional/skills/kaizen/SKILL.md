---
name: kaizen
description: "Apply kaizen continuous improvement philosophy to any codebase — identifying waste, unevenness, and overburden at the code level and producing small, actionable improvement opportunities. Triggers on '/kaizen', 'kaizen this codebase', 'continuous improvement audit', 'find waste in this code', 'what small improvements can we make?', 'improve this codebase incrementally', 'code health check', 'codebase hygiene', 'tech debt sweep', or any request to find incremental improvement opportunities in code. Also trigger when the user says 'clean up', 'tidy up', 'make this codebase better', or expresses frustration about code quality without wanting a full rewrite. This is NOT a code review skill for PRs or diffs — kaizen operates on the codebase as a whole or a focus area, looking for systemic improvement opportunities. Use this skill even for small codebases — the philosophy scales down gracefully."
---

# Kaizen (改善) — Codebase Continuous Improvement

Smallest changes compounding into significant quality. Every file you touch leaves better than found.

---

## Input Modes

### `/kaizen`
Run all seven dimensions across the codebase. Full improvement map.

### `/kaizen "focus description"`
All dimensions, **weighted and prioritized** through user's lens.

Examples:
- `/kaizen "file sizes — nothing should exceed 500 LOC"`
- `/kaizen "naming consistency across the API layer"`
- `/kaizen "dead code and unused imports"`
- `/kaizen "error handling patterns"`

When focused:
1. Still scan all seven dimensions (critical issues may lie outside focus)
2. Lead the report with focus-specific findings
3. Mark non-focus findings as `[ALSO NOTED]` — keep brief
4. Issues matching focus are severity-promoted one level

---

## The Three Wastes (三大ムダ)

Every finding maps to one. Classification taxonomy.

### Muda (無駄) — Waste
Code consuming effort without adding value.

| Type | Code manifestation |
|---|---|
| Defects | Bugs, broken tests, swallowed errors |
| Overproduction | Dead code, unused exports, premature abstractions |
| Waiting | Slow builds, blocking I/O without async |
| Transportation | Unnecessary data transformations, excessive layer mapping |
| Inventory | Stale TODOs (>6mo), commented-out code, stale branches |
| Motion | Excessive indirection, 5+ layer call chains for simple ops |
| Over-processing | Over-engineered abstractions, config for hypothetical flexibility |

### Mura (斑) — Unevenness
Inconsistency forcing context-switching and guessing.

| Signal | Example |
|---|---|
| Naming | `getUserData()` vs `fetchUserInfo()` vs `loadUserProfile()` for same pattern |
| Mixed paradigms | Callbacks + promises + async/await in same codebase |
| Structure | Different folder layouts across features |
| Error handling | Some throw, some return null, some use Result types |
| Test style | Mixed assertion libs, inconsistent AAA |

### Muri (無理) — Overburden
Code units carrying too much.

| Signal | Default threshold |
|---|---|
| God files | > 400 LOC |
| God functions | > 40 LOC or cyclomatic complexity > 10 |
| Too many params | > 5 parameters |
| God modules | > 15 exports/public methods |
| Coupling | Imported by > 60% of codebase |
| Deep nesting | > 3 levels |

---

## Seven Dimensions — Execute in Order

### Shared Output Format

Findings in D2–D4:

```
[MUDA|MURA|MURI] [subtype]
📍 [file:line or pattern]
Finding: [one sentence]
Kaizen: [specific small change]
Effort: [trivial | small | medium]
```

---

### D1 — Gemba Walk (現場): See the Actual State

*Observe the real state, not the idealized version.*

1. Map directory structure (2 levels deep)
2. Count files by type, measure LOC distribution
3. Identify largest files, deepest nesting, most-imported modules
4. Read existing context files (README, ARCHITECTURE.md, .ctx, CLAUDE.md)
5. Note language, framework, build system

```
GEMBA SNAPSHOT
Languages:      [detected]
Framework:      [detected]
Total files:    [N] | Total LOC: [N]
Largest file:   [path] ([N] lines)
Deepest nest:   [path] ([N] levels)
Most imported:  [module] (by [N] files)
Test coverage:  [detected or unknown]
Context files:  [list found]
```

---

### D2 — Muda Scan: Waste

Scan each waste type. Prioritize:
1. Dead code (unused functions, unreachable branches, orphan exports)
2. Over-engineering (single-impl abstractions, one-setting config systems)
3. Stale artifacts (undated TODOs, deprecated code, outdated comments)
4. Redundancy (duplicated logic, copy-paste, overlapping utilities)
5. Unnecessary complexity (fewer lines without losing clarity)

---

### D3 — Mura Scan: Unevenness

For each inconsistency, identify the **dominant pattern** (most common variant) — standardize on it.

Additional fields:
```
Variants found: [list observed]
Dominant pattern: [most common — standardize on this]
```

---

### D4 — Muri Scan: Overburden

Scan against Muri thresholds. Honor user-specified thresholds. Adjust upward where longer files are conventional (Java).

Additional fields:
```
Metric: [what] = [measured] (threshold: [N])
Impact: [why this hurts — "hard to test", "merge conflict magnet"]
```

---

### D5 — 5S Audit (整理・整頓・清掃・清潔・躾)

| 5S | Code equivalent | Check |
|---|---|---|
| Sort (整理) | Remove unneeded | Dead files, unused deps, orphaned configs |
| Set in Order (整頓) | Everything in its place | Correct directories, logical boundaries, organized imports |
| Shine (清掃) | Clean regularly | Lint errors, formatting, stale comments, debug artifacts |
| Standardize (清潔) | Consistent practices | Documented patterns, enforced conventions |
| Sustain (躾) | Maintain discipline | CI checks, pre-commit hooks, quality gates |

Score each `🟢 Good | 🟡 Partial | 🔴 Needs work` with one-line evidence.

---

### D6 — Improvement Backlog (改善バックログ)

**Primary deliverable.** Synthesize D2–D5, prioritized:
- **Impact** (1–3): waste/unevenness/overburden removed
- **Effort** (1=trivial, 2=small, 3=medium): time
- **Risk** (1=safe, 2=needs tests, 3=risky): can it break
- **Score**: Impact / (Effort × Risk) — higher better

```
改善 IMPROVEMENT BACKLOG
#  Type  Score  Effort   Description                    Location
1  MUDA  3.0    trivial  Remove 12 unused imports        src/utils/*.ts
2  MURI  1.5    small    Extract validation from handler  src/api/orders.ts:45-120
3  MURA  1.5    small    Standardize error returns        src/services/*
...
```

**Cap at 15 items.** If more, note "N additional — run `/kaizen` with a focus to drill in."

---

### D7 — PDCA Compass

```
PLAN:  [Top 3 improvements to tackle first and why]
DO:    [Concrete next steps — "In your next PR, ..."]
CHECK: [How to verify improvements landed]
ACT:   [Systemic prevention — linter rules, CI, conventions to document]
```

---

## Report Assembly

1. **Header**: Codebase, focus (or "Full scan"), date
2. **Gemba Snapshot** (D1)
3. **5S Scorecard** (D5)
4. **Improvement Backlog** (D6) — hero section
5. **Detailed Findings**: Muda (D2), Mura (D3), Muri (D4)
6. **PDCA Compass** (D7)

Close with: *"改善の精神: 今日の最善は、明日の出発点。"*

---

## Calibration Rules

1. **Single-PR scope**: every suggestion achievable in one PR. Multi-day refactors need decomposition or "requires planning" flag.
2. **Respect existing decisions**: don't contradict ADRs/conventions. Note tensions instead.
3. **Evidence over opinion**: every finding cites file/line/pattern. No vague "could be cleaner."
4. **Compound priority**: prefer changes improving many files over isolated fixes.
5. **Don't manufacture findings**: if priority is one thing, say so. Honest beats padded.
6. **Focus discipline**: focus findings lead. Non-focus is brief bonus context.
7. **Threshold flexibility**: state thresholds used. Honor user-specified. Adjust for language conventions.
