---
name: context-cartography
description: Use when designing what goes into an agent's context window — system prompts, tool definitions, retrieval results, or any context artifact assembled before the agent runs. Triggers on "what should I put in the system prompt?", "how do I structure my context?", "the agent loses track of...", "my context window is full", "how do I decide what to include?", "designing a new harness", "the agent ignores my instructions". Do NOT use for one-off prompts, runtime conversation management, or when the problem is model capability rather than context design.
---

# Context Cartography

Design what goes into an agent's context window — and what stays out.

Every context window is a lossy projection of a larger information space. You can't include everything. The skill is in choosing *which* information serves the task and *which* distortions are acceptable.

## The Boundary Rule

```
Designing or redesigning a context window?     →  Use this skill.
Context window is full and you need to cut?    →  Start at the TRIAGE entry point.
Need to validate whether your design works?    →  Use EDD after this skill.
One-off prompt or exploratory prototyping?     →  Don't use this skill.
```

---

## Two Entry Points

### Entry A — Full Design (greenfield or major redesign)

Follow all six steps: TASK → SURVEY → PRIORITIZE → SIZE → STRUCTURE → CUT.

### Entry B — Triage (context is too big, need to trim)

Start at CUT. If cuts reveal that the wrong information is prioritized, work backwards through PRIORITIZE and SIZE. This serves the 80% case: "my context window is too full."

---

## The Flow

### Step 1 — TASK

What will the agent do with this context?

Be specific. Not "code assistance" but "review pull requests for a Python microservices codebase, checking style, correctness, and security." The task definition determines every downstream decision.

Write it as a single sentence. If you need two sentences, you may need two context configurations.

**Output**: One-sentence task definition.

### Step 2 — SURVEY

What information exists that *could* be relevant?

Enumerate all candidate context sources. Don't filter yet — just list them. Common sources:

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

**Output**: Complete list of candidate context sources with estimated token cost for each.

### Step 3 — PRIORITIZE

Which information matters most for this task?

Consult the pattern catalog below. For each candidate source from the SURVEY, assign a priority:

| Priority | Meaning | Rule |
|----------|---------|------|
| **P0 — Essential** | Agent cannot do the task without this | Always include |
| **P1 — Important** | Significantly improves quality | Include if token budget allows |
| **P2 — Useful** | Helps with edge cases or polish | Include only if space remains |
| **P3 — Irrelevant** | Does not affect this task | Never include |

**The non-obvious call**: P1 items that *seem* essential but aren't (false P0), and P2 items that turn out to be load-bearing (hidden P0). The pattern catalog below highlights these for common task types.

**Output**: Prioritized list of context sources with P0/P1/P2/P3 ratings.

### Step 4 — SIZE

How much detail for each source?

For each P0 and P1 source, choose a detail level:

```
Will the agent MODIFY this content?
  → Full source (every line matters)

Will the agent CALL or REFERENCE this content?
  → Signatures + docstrings (interface, not implementation)

Does the agent need to know this EXISTS and what it does?
  → One-line summary

Does the agent need to know the SHAPE of the system?
  → Structural overview (file tree, dependency graph, architecture diagram)
```

**Common mistakes**:
- Including full source for files the agent only references (wastes tokens, adds noise)
- Including only summaries for files the agent needs to modify (insufficient detail)
- Including everything at the same detail level (no signal hierarchy)

**Output**: Each P0/P1 source with its size decision and rationale.

### Step 5 — STRUCTURE

How should the context be organized so the agent can navigate it?

**Model-general principles** (these hold across current LLMs):

1. **Task-relevant context goes closest to the instruction.** Models attend more strongly to context near the query/instruction. Put the most important information last (closest to the user message) or first (system prompt opening).

2. **Label sections explicitly.** Use clear headers that describe WHAT the section contains and WHY it's there. Not `## Code` but `## Source code to review — check for style, correctness, and security issues`.

3. **Separate instructions from reference.** Instructions (what to do) should be distinct from reference material (information to use). Mixing them causes the agent to treat reference as instructions or vice versa.

4. **Use consistent formatting.** Pick one structure (markdown headers, XML tags, delimiters) and use it throughout. Inconsistent formatting creates ambiguity about section boundaries.

5. **Make the context self-documenting.** If a reviewer can't tell why a piece of context is included by reading the section header, the structure needs work.

**Output**: Structured layout of the context window with section headers and ordering.

### Step 6 — CUT

Remove everything that doesn't earn its tokens.

**The CUT protocol**:

1. List every context element (from STRUCTURE output)
2. For each element, state the specific agent behavior it supports
3. If you can't state the behavior in one sentence → **cut candidate**
4. If two elements support the same behavior → keep the more token-efficient one, **cut the other**
5. For each cut candidate, verify via EDD ablation: remove it, run evals, check if any assertion regresses

**Additive alternative**: If starting from an existing bloated context, try the inverse — start with ONLY P0 items and add P1 items one at a time, measuring each addition's impact. This sidesteps loss aversion and often produces leaner contexts than subtractive cutting.

**Shadow context**: Don't delete cut items permanently. Move them to a shadow set. When production anomalies occur, re-test with shadow items restored — a cut item may be load-bearing for edge cases your evals don't cover.

**Output**: Final context window + shadow context list.

---

## Pattern Catalog

Concrete prioritization patterns for common agent task types. Each pattern lists what matters more and less than developers typically expect.

### Code Generation

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| Task specification / requirements | P0 | Expected |
| Files the new code will interact with (full) | P0 | Expected |
| Existing test patterns in the project | P0 | **Often missed** — without these, generated code follows generic patterns, not project conventions |
| Naming conventions / style guide | P1 | **Often missed** — models default to their training distribution, not your conventions |
| Type definitions / interfaces | P1 | Expected |
| Architectural constraints / patterns | P1 | Expected |
| Unrelated modules | P3 | **Often included unnecessarily** — adds noise without changing output |
| Full git history | P3 | **Often included unnecessarily** — recent diff may be P1, but full log is noise |

### Code Review

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| The diff / changed files (full) | P0 | Expected |
| Style guide / linting rules | P0 | **Often P1'd** — but without this, reviews are generic, not project-specific |
| Test files for changed code | P0 | **Often missed** — reviewer can't assess test coverage without seeing tests |
| Architectural constraints | P1 | Expected |
| Related files the changes affect | P1 | Expected |
| PR description / ticket context | P1 | **Often missed** — reviewer lacks intent, reviews syntax instead of semantics |
| Unrelated codebase modules | P3 | Expected |
| Build / CI configuration | P3 | **Often included unnecessarily** |

### Debugging

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| Error output / stack trace | P0 | Expected |
| Source file(s) referenced in trace (full) | P0 | Expected |
| Recent changes to those files (git diff) | P0 | **Often missed** — "what changed?" is the #1 debugging question |
| Related test files | P1 | Expected |
| Dependency versions / environment | P1 | **Often missed** — version mismatches cause subtle bugs |
| Reproduction steps | P1 | Expected |
| Unrelated source files | P3 | Expected |
| Full git log | P3 | Recent diff is P0; full history is noise |

### Multi-Step Planning / Architecture

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| High-level architecture description | P0 | Expected |
| File/directory structure | P0 | **Often missed** — the agent needs the shape of the system, not file contents |
| Constraints (performance, compatibility, deadlines) | P0 | **Often missed** — plans without constraints are wish lists |
| Dependency graph | P1 | Expected |
| Existing patterns / conventions | P1 | Expected |
| Full source code of any file | P2 | **Often included at P0** — planning needs structure, not implementation details |
| Test files | P2 | Not relevant until implementation |

### Q&A Over Documentation

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| Relevant documentation sections | P0 | Expected |
| Glossary / terminology definitions | P0 | **Often missed** — domain jargon without definitions causes hallucination |
| Examples from the docs | P1 | Expected |
| Source code | P2 | **Often included at P0** — only relevant if the question is about implementation |
| Full documentation corpus | P3 | **Often included** — retrieval should select, not dump |

### Test Writing

| Source | Priority | Surprise factor |
|--------|----------|----------------|
| Implementation under test (full) | P0 | Expected |
| Existing test files in the project (patterns) | P0 | **Often missed** — without these, tests follow generic framework patterns |
| Test framework docs / helpers | P1 | Expected |
| Edge cases from specs or tickets | P1 | **Often missed** — tests cover happy path without spec-derived edge cases |
| Mock/fixture patterns used in project | P1 | **Often missed** — agent invents new patterns instead of following existing ones |
| Unrelated source files | P3 | Expected |

---

## The Context Manifest

The skill's output artifact. This is what feeds into EDD for validation.

```yaml
# Context Manifest
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
    reason_cut: "Recent diff (included in PR diff) was sufficient"

structure:
  order:
    - "System instructions (role + review criteria)"
    - "Style guide"
    - "Architecture summary"
    - "PR description"
    - "Test files"
    - "PR diff (closest to instruction)"
  rationale: "Task-relevant content (diff) placed last, near user message. Reference material (style guide, architecture) placed earlier for lookup."
```

This manifest is:
- **Versionable** — commit it alongside the harness
- **Diffable** — changes to context design are reviewable
- **Testable** — EDD writes assertions against the agent behavior this manifest claims to support
- **Auditable** — the `supports` field for each source explains why it's included

---

## Integration with EDD and Context-Eval

| Phase | Skill | What happens |
|-------|-------|-------------|
| **Design** | context-cartography | Produce a context manifest |
| **Validate** | EDD | Write assertions based on the manifest's `supports` claims. Run evals. |
| **Measure** | context-eval | Measure pass rates, benefit-per-kilotoken, identify deadwood |
| **Iterate** | Loop back | Eval failures → update manifest → re-run |

**The handoff**: Each source in the manifest has a `supports` field stating what behavior it enables. These claims become EDD assertions directly. If a source claims "Agent checks project-specific conventions" but the eval shows the agent uses generic conventions anyway, that source isn't earning its tokens — redesign or cut it.

---

## Maintenance: When to Resurvey

Context designs drift as tasks evolve and models change. Resurvey when:

- **Task scope changes** — the agent is asked to do things the manifest wasn't designed for
- **Model upgrade** — a new model may need less context (stronger baseline) or different structure
- **Eval scores plateau or regress** — the current design may have reached its ceiling
- **Token budget changes** — model context windows grow; what was cut may now fit

Don't let the manifest become stale documentation. Treat it like code: review it, version it, test it.

---

## Anti-Patterns

| Anti-pattern | Symptom | Fix |
|-------------|---------|-----|
| **Context stuffing** | Include everything "just in case" | Start with P0 only, add P1 items one at a time with measurement |
| **Uniform sizing** | Every file included at full detail | Use the SIZE decision tree — most files need signatures or summaries, not full source |
| **Missing legend** | Context sections have no headers or labels | Agent wastes tokens figuring out what it's looking at. Label everything. |
| **Priority inversion** | P2 items included while P0 items are summarized | Check: is the most important information at the highest detail level? |
| **Stale manifest** | Design was done 6 months ago, task has evolved | Resurvey. The map should match the territory. |
| **Solo without validation** | Context designed but never tested | Always follow with EDD. Design without eval is guesswork. |
| **Cargo-culting patterns** | Copying a pattern from the catalog without adapting | Patterns are starting points. Your codebase and task may need different priorities. |
