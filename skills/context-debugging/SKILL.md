---
name: context-debugging
description: Use when an agent is failing, producing wrong output, ignoring instructions, hallucinating, or behaving unexpectedly — and the cause isn't an obvious code bug. Triggers on "my agent keeps failing", "the agent ignores my instructions", "it hallucinates even though I told it not to", "I fixed one thing but something else broke", "the agent used to work but now it doesn't", "why is the agent doing X instead of Y?". Do NOT use for infrastructure errors (API 500s, timeouts), code bugs in the harness (use systematic-debugging), or when the agent has never worked (use context-cartography to design first).
---

# Context Debugging

**Check context first. It's the highest-ROI debugging target for agent failures.**

## The Boundary Rule

```
Agent failing, not an obvious code bug?         →  Use this skill.
Agent has never worked (greenfield)?            →  Use context-cartography.
Infrastructure error (API 500, timeout)?        →  Not a context problem.
Code bug in the harness (template, parsing)?    →  Use systematic-debugging.
```

---

## The Triage Flow

### Step 0 — VERIFY ACTUAL CONTEXT

Confirm you can see what the model actually receives. Actual ≠ intended is common.

1. Log/dump the full assembled context (system prompt + tools + retrieved docs + history)
2. Compare to expectations: all sections present? Right order? Expected size?
3. If actual ≠ intended → bug is in context assembly. Use systematic-debugging.

Skip this step and every diagnosis below could be wrong.

### Step 1 — OBSERVE

- **What did you expect?**
- **What happened instead?**
- **How often?** (every time / sometimes / rarely)
- **When did it start?** (always / after a change / gradually)

"Sometimes" failures strongly signal a context problem — stochastic behavior means the model is on the boundary.

### Step 2 — CLASSIFY

Run **all** diagnostic questions. Mark every "yes." Multiple categories often co-occur. Investigate matches in order, but **don't stop at the first match**.

| # | Question | If yes → | Quick test |
|---|----------|----------|------------|
| 1 | Was context recently changed? | **REGRESSION** | Revert. Fixed? |
| 2 | Does the agent lack info it needs? | **MISSING CONTEXT** | Add manually. Fixed? |
| 3 | Are tool definitions ambiguous/overlapping? | **TOOL PROBLEM** | Read each cold. Ambiguous? |
| 4 | Can agent find info in the context? | **BURIED CONTEXT** | Move instruction to top. Fixed? |
| 5 | Are instructions contradictory? | **CONFLICTING CONTEXT** | Remove one. Fixed? |
| 6 | Does less context fix it? | **CONTEXT OVERFLOW** | Keep only essential. Fixed? |
| 7 | None of the above? | **REASONING FAILURE** | Try ideal minimal context. Still fails? |

### Step 3 — LOCATE & FIX

Each category has a **quick fix** (under 10 min, no other skills) and a **full fix** (thorough, may use companion skills).

---

## Failure Categories

### REGRESSION — "It used to work"

**Diagnostic:**
1. Diff current context against last known-good version
2. For each change: "could this affect the failing behavior?"
3. Revert and confirm failure disappears
4. Re-apply changes one at a time until failure reappears

**Common causes:**
- New instructions competing with existing ones for attention
- Restructured sections moving critical instructions to lower-attention positions
- Removed text that was load-bearing without being obviously important
- Added examples anchoring on wrong patterns

**Quick fix:** Revert. Ship the revert.

**Full fix:** Re-introduce incrementally, validate each step with EDD. Check for BURIED CONTEXT or CONFLICTING CONTEXT as secondary causes.

---

### MISSING CONTEXT — "The agent doesn't know"

**Diagnostic:**
1. What info would the agent need to get this right?
2. Is it in the assembled context (Step 0)?
3. If RAG: was the right document retrieved? Check retrieval results, not source data.

**Common causes:**
- Assumed the model "knows" something it doesn't (project conventions, internal terminology)
- Retrieval returned irrelevant docs (query mismatch, bad embeddings, wrong chunking)
- Conversation history truncated
- Info exists but wasn't included

**Signals:**
- Generic/default behavior instead of project-specific
- Agent asks questions the context should answer
- Plausible-but-wrong details (filling gaps with training data)

**Quick fix:** Add missing info directly to system prompt. If fixed, diagnosis confirmed.

**Full fix:** Use context-cartography for proper priority and sizing. If retrieval was the problem, fix the pipeline — manual add is a band-aid.

---

### TOOL DEFINITION PROBLEM — "The agent can't use its tools"

**Diagnostic:**
1. Read each tool def cold. Unambiguous?
2. Two tools with overlapping descriptions?
3. Parameter names/descriptions match what the tool expects?
4. Does the prompt explain WHEN to use each tool?
5. Compare schema model receives (Step 0) with code — serialization bugs silently drop fields.

**Common causes:**
- Two tools with similar descriptions — agent picks randomly
- Description says what tool IS but not WHEN to use it
- Ambiguous parameter names (`data`, `input`, `value`)
- Schema changed but description wasn't
- Serialization bug drops a parameter description

**Signals:**
- Wrong tool consistently
- Plausible but incorrect parameters
- Manual work for something a tool handles
- Agent invents a tool name

**Quick fix:** Add "WHEN to use" to each description. For overlaps, add "Use X for [scenario], Y for [other]" to the system prompt.

**Full fix:** Rewrite all tool descriptions: one-line purpose, when to use, when NOT to use, parameters with types/constraints. Validate with EDD.

---

### BURIED CONTEXT — "It's there but the agent ignores it"

**Diagnostic — concrete tests, not judgment:**
1. Move instruction to first 200 tokens of system prompt. Behavior change? → Position problem.
2. Remove 50% of surrounding context (keep instruction). Change? → Signal-to-noise.
3. Add explicit section header. Change? → Labeling problem.

**Common causes:**
- **Lost in the middle** — info in the middle gets less attention
- **Unlabeled** — raw text without headers
- **Drowned by volume** — 50 tokens of critical instruction in 5,000 tokens of reference
- **Overshadowed** — more prominent or recent instruction takes priority

**Signals:**
- Follows some instructions but not others
- Moving to top fixes it
- Removing unrelated context fixes it
- Intermittent

**Quick fix:** Move ignored instruction to last 500 tokens of system prompt (closest to user message).

**Full fix:** Restructure with context-cartography STRUCTURE step. Label sections (WHAT, WHY). Reduce noise. Validate with EDD.

---

### CONFLICTING CONTEXT — "The agent gets mixed signals"

**Diagnostic:**
1. Read the full context for any two contradictory statements
2. Check if examples contradict instructions
3. Check if tool descriptions conflict with system instructions
4. Check **emergent interactions** — instructions reasonable alone but conflict combined (e.g., "always respond formally" + "mirror the user's tone")
5. Same term meaning different things across sections

**Common causes:**
- Instructions evolved without removing old versions
- Examples from earlier version don't match current rules
- Implicit vs. explicit: example demonstrates a pattern that contradicts an instruction
- Two reasonable rules producing impossible combinations

**Signals:**
- High variance — sometimes rule A, sometimes B
- Output is a blend/compromise
- Follows the instruction closest to the task

**Quick fix:** Identify the two conflicting instructions. Remove or comment out one. Stable? Decide winner, update other.

**Full fix:** Audit for conflicts — examples-vs-instructions, emergent interactions. Choose a winner per conflict, remove or update loser. Examples override instructions more than developers expect.

---

### CONTEXT OVERFLOW — "Too much context drowns the signal"

**Diagnostic:**
1. Total token count?
2. % directly relevant to failing task?
3. Remove all non-essential. Resolves?

**Common causes:**
- Kitchen-sink — everything "just in case"
- Retrieval returning too many results without re-ranking
- Conversation history growing without summarization
- Too many or too-long few-shot examples

**Signals:**
- Better with less context
- Ignores recent instructions, follows old ones
- Adding relevant context paradoxically makes output worse

**Quick fix:** Strip to bare minimum — role, task, most critical reference. If improved, re-add sections one at a time. Stop when quality plateaus or drops.

**Full fix:** Apply context-cartography (PRIORITIZE + CUT). Measure each addition with EDD. Consider dynamic context (retrieve per-task instead of including everything).

---

### REASONING FAILURE — "The model just can't do this"

The only category that ISN'T a context problem.

**Diagnostic:**
1. Construct minimal, ideal context — exactly what the model needs, perfectly structured
2. Run task 5+ times with this ideal context
3. Still fails → genuine capability limitation
4. Succeeds → one of the above categories was the real cause

**Before concluding reasoning failure:**
- Verified actual context (Step 0)?
- Tried moving instructions to a more prominent position?
- Tried chain-of-thought?
- Tried decomposing the task?
- Tried a more capable model?

**Quick fix:** Decompose into smaller steps, or add explicit chain-of-thought ("Think step by step: first identify X, then check Y, then decide Z").

**Full fix:** Redesign decomposition, upgrade model, or add tools that compensate (e.g., calculator for math).

---

## Compound Failures

| Primary | Often co-occurs with | Why |
|---------|---------------------|-----|
| REGRESSION | BURIED CONTEXT | New content pushes existing instructions to low-attention positions |
| MISSING CONTEXT | CONFLICTING CONTEXT | Adding info introduces contradictions |
| TOOL PROBLEM | CONTEXT OVERFLOW | Ambiguous tool descriptions harder to parse in bloated context |
| BURIED CONTEXT | CONTEXT OVERFLOW | More content = more attention competition |

**Rule:** If fixing the first category doesn't resolve the failure, continue to the next match.

---

## Quick Triage Checklist

```
0. Can you see the full assembled context?    →  If not, log it
1. Was context recently changed?              →  Revert and confirm
2. Is needed info present?                    →  Add it manually
3. Are tool definitions clear?                →  Read them cold
4. Is info findable (well-positioned)?        →  Move it to the top
5. Are instructions contradictory?            →  Remove one
6. Does less context fix it?                  →  Strip to essentials
7. None of the above?                         →  Minimal context test
```

Most resolve at steps 1-4. Regularly reaching step 7 → revisit design with context-cartography.

---

## Integration with the Context Skill Suite

| Situation | Skill |
|-----------|-------|
| Diagnose why agent is failing | **context-debugging** (this skill) |
| Diagnosis points to design problem | → context-cartography to redesign |
| Validate fix didn't break other things | → EDD to run assertions |
| Measure if the fix helped | → context-eval to compare before/after |

---

## Anti-Patterns

| Anti-pattern | Symptom | Fix |
|-------------|---------|-----|
| **Blaming the model first** | "The model is stupid" before checking context | Check context before concluding reasoning failure |
| **Symptom chasing** | Adding instructions to fix symptoms | Classify first, then fix the category |
| **Context band-aids** | Adding "IMPORTANT: DO NOT..." instead of fixing structure | Restructure, don't shout |
| **Debug by adding** | Every failure → more context | Sometimes the fix is removing |
| **Skipping Step 0** | Debugging intended context, not actual | Always verify what the model receives |
| **Single-cause assumption** | Fixing one and declaring victory | Check remaining categories if not fully resolved |
| **One-shot debugging** | Test fix once, ship | Stochastic systems need multiple runs — use EDD |
