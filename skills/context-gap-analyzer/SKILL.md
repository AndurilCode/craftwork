---
name: context-gap-analyzer
description: "Identify implicit context missing from a codebase that would most improve agent performance. Use whenever someone asks to audit, assess, or improve context for a codebase; asks 'what context is my codebase missing?', 'why do agents keep making mistakes here?', 'what should I put in my CLAUDE.md?', 'audit my codebase context', 'context gaps', or any variation. Also trigger when setting up agent context infrastructure for the first time, or when agent-generated code keeps violating implicit conventions."
---

# Context Gap Analyzer

Code is necessary but insufficient context. The delta between "what the code says" and "what a competent team member knows" is where agents fail most expensively. This skill identifies that delta, prioritizes by agent impact, and surfaces focused questions a human can answer.

What agents **cannot** derive from code alone: **Why** (rationale), **What** conventions aren't enforced by tooling, **How** things interact beyond repo boundaries, **When** to break vs. follow a pattern, **Who** owns what.

---

## PHASE 1 — Context Harness Discovery

Discover all context infrastructure already in place. Actively explore — don't rely on a checklist.

**Layer 1: File-level** — Scan repo root + 2-3 levels deep for anything that reads like "instructions for someone working here." For each: read it, inventory topics, note scope (repo/dir/module), format, audience.

**Layer 2: Toolchain** — MCP servers (context delivery channels), skills/plugins, hooks/middleware (git hooks, CI, pre-commit, linting), IDE/editor configs. These are implicit context delivery mechanisms.

**Layer 3: Runtime** — Connected services (Drive, Notion, Confluence, Slack), env/secrets management, package manager metadata (dependency choices signal patterns).

**Layer 4: Delivery classification**

| Delivery | Examples | Implication |
|----------|----------|-------------|
| **Static** | `AGENTS.md`, `.cursorrules`, system prompts | Token cost; must be concise |
| **On-demand** | MCP servers, search, skill files | Richer; agent must know *when* to fetch |
| **Triggered** | Git hooks, CI checks, pre-commit | Enforcement without *why* |
| **Implicit** | Types, tests, linter configs | Partial; rationale missing |

Output: inventory of static files (path, topics, scope, format), toolchain context (MCP servers, skills, hooks), runtime context (connected services, config injection), delivery map with counts, already-documented topics, and primary delivery format (determines Phase 6 output).

Be thorough before concluding "nothing exists" — `.eslintrc`, `Makefile`, `docker-compose.yml` are all context. The question is *sufficiency*.

---

## PHASE 2 — Codebase Topology Scan

Map: directory structure (modules, depth), technology fingerprint (languages, frameworks, build tools), complexity indicators (file counts, nesting depth, config variety), integration surface (external services, APIs, DBs, queues), entry points (routes, CLI commands, event handlers).

Output: codebase type, languages, framework, top-level modules ranked by complexity, integration surface, high-traffic areas for agents.

---

## PHASE 3 — Gap Analysis

Cross-reference Phase 1 (documented) against Phase 2 (code). Evaluate nine categories:

| Cat | Name | Agent needs | Gap indicator |
|-----|------|------------|---------------|
| C1 | Architecture & Boundaries | Component topology, data flow, module dependency rules | Cross-boundary imports, code in wrong module |
| C2 | Domain Model & Business Rules | Business logic rationale, domain vocabulary, invariants | Technically correct but domain-wrong code |
| C3 | Conventions & Patterns | Naming, file organization, error handling, logging | Code that works but "feels wrong" to the team |
| C4 | Integration & External Deps | API calling patterns, retry/fallback, rate limits, auth | Incorrect service calls, missing retry logic |
| C5 | Operations & Deployment | CI/CD, feature flags, rollback, monitoring conventions | Code that breaks CI, unmonitored failure modes |
| C6 | Testing Philosophy | Unit vs. integration boundaries, mocking, fixtures | Wrong test type, mocks at wrong boundaries |
| C7 | Security Model | Auth patterns, data classification, secret management | Auth bypasses, logged sensitive data |
| C8 | Performance Constraints | Bottlenecks, caching, query patterns, pagination | N+1 queries, skipped caching, unbounded queries |
| C9 | Historical Decisions & Debt | Why things are this way, migrations, deprecated patterns | Extending deprecated patterns, building on doomed code |

### Scoring

| Factor | Range | Meaning |
|--------|-------|---------|
| Documentation coverage | 0-3 | 0=nothing, 1=mentioned, 2=partial, 3=thorough |
| Code complexity | 1-3 | 1=simple, 2=moderate, 3=complex/non-obvious |
| Agent exposure | 1-3 | 1=rarely touched, 2=sometimes, 3=frequently modified |

**Gap severity** = Complexity x Exposure - Doc coverage (range: -2 to 9)

| Score | Priority |
|-------|----------|
| >= 5 | Critical |
| 3-4 | Significant |
| <= 2 | Acceptable |

Output: table with all 9 categories scored, overall coverage percentage (Doc sum / 27 x 100), critical gaps listed.

---

## PHASE 4 — Prioritized Question Generation

For each gap >= 3, generate focused questions answerable in 2-5 minutes. Each targets exactly one piece of implicit knowledge, and the answer must be directly usable as agent context.

```
Q[N] — [Category] — Priority: [Critical/High/Medium]
[Specific, focused question]

Why this matters: [what goes wrong without this context]
Good answer example: [3-5 sentence template showing detail level needed]
```

Generate 10-20 questions. At least 2 per critical gap, 1 per significant gap. Order by gap severity x actionability.

---

## PHASE 5 — Coverage Map

Visualize current state as baseline:

```
CONTEXT COVERAGE MAP — [repo] — [date]

C1 Architecture      [████░░░░░░]  40%  ⚠️ Significant
C2 Domain Model      [█░░░░░░░░░]  10%  🔴 Critical
...
OVERALL: [X]% | Questions: [N] | Est. time to close critical gaps: ~[N] min
```

Use interactive visualization (radar chart, heatmap) when environment supports it.

---

## PHASE 6 — Tracking & Integration

Create `.context-coverage.json` at repo root with: version, repo, dates, harness info (primary format, static sources, toolchain, delivery summary), per-category scores, questions (id, category, priority, question, status, answer, integrated_to), overall coverage.

**When the user answers a question**:
1. Store the answer, mark as `"answered"`
2. Write into the harness matching existing conventions (tone, structure, format, scope)
3. Record `integrated_to` path, recalculate coverage, show updated map

**Integration principle**: Adapt to the harness, never prescribe. Match the existing file's voice and format. If no writable harness exists, ask the user where they want context written.

---

## Incremental Modes

- **First run**: Full Phases 1-6, baseline coverage + all questions
- **Answer session**: Integrate answers, update coverage
- **Re-audit**: Re-run Phases 2-5 after significant codebase changes
- **Coverage check**: Phase 5 only from existing `.context-coverage.json`

Detect mode from whether `.context-coverage.json` exists and what the user asks.

---

## Calibration

1. **Agent-first**: Frame every question as "what would an agent get wrong?" not "what's undocumented?"
2. **Precision over completeness**: 10 high-impact questions beat 50 thorough ones. Human time is the bottleneck.
3. **Respect existing context**: Cross-reference before asking — don't duplicate what's already documented.
4. **Harness humility**: Detect and work within existing systems. Don't prescribe.
5. **Actionable answers**: The example answer in each question prevents both one-word and novel-length responses.
6. **Coverage honesty**: Score based on what an agent would find useful, not what technically exists.
