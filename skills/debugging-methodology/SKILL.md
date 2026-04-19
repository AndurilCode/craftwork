---
name: debugging-methodology
description: "Apply debugging methodology whenever the user faces a software failure they cannot explain — a broken test, unexpected behavior, a regression, or an intermittent bug. Triggers on phrases like \"why is this broken?\", \"how do I debug this?\", \"the test fails but I don't know why\", \"intermittent failure\", \"works on my machine\", \"this used to work\", \"regression\". Use proactively when the user describes a symptom and jumps straight to a fix without isolating the root cause."
---

# Debugging Methodology

Reproduce, observe, hypothesize, isolate, verify. Resist guess-and-patch. Goal is root cause — fixing the wrong cause means it breaks again.

---

## When to Use

- Test fails for non-obvious reason
- Behavior changed; cause unknown
- Bug is intermittent or environment-dependent
- User pattern-matches to a fix without root-cause evidence
- A fix was applied but the problem recurred or shifted

---

## Core Methodology

### Step 1: Reproduce the Failure

A bug you can't trigger is a bug you can't verify fixed.

- Record exact steps, inputs, environment
- For intermittent failures, characterize frequency and conditions (load, timing, data shape, concurrency)
- If it doesn't repro locally, identify the environmental delta (OS, deps, config, data volume, network)
- **No reproduction, no diagnosis.** If impossible, instrument code to capture state on next occurrence and proceed to Step 2 with available data

### Step 2: Observe Before Theorizing

Premature hypotheses cause confirmation bias. Collect evidence first:

- Full error messages and stack traces (exact text, not paraphrased)
- Relevant log output around the failure
- System state: memory, CPU, disk, connections, queue depth
- Recent changes: commits, config, dependency updates, infra
- Data state: what input triggered it? Valid?

Separate facts ("NullPointerException on line 42") from interpretations ("the object must not be initialized").

### Step 3: Generate and Rank Hypotheses

List every plausible cause. Rank by:

1. **Likelihood** given evidence
2. **Testability** — how fast to confirm/rule out
3. **Impact** — severity if true

Prioritize likely + fast-to-test. A 30-second elimination check is always worth it.

**Differential diagnosis — what changed?**
- **Code**: recent commits, merges, refactors
- **Configuration**: env vars, feature flags, settings
- **Data**: new patterns, schema changes, edge cases
- **Dependencies**: version bumps, transitive changes
- **Infrastructure**: deployments, resource limits, network

### Step 4: Isolate with Binary Search

Halve the search space; don't read line by line.

- **Bisect commits**: `git bisect`
- **Bisect code**: stub components until failure disappears, re-enable one by one
- **Bisect input**: minimize failing input
- **Bisect environment**: swap one env variable at a time

Each step should halve the space. If not, change dimension.

### Step 5: Confirm Root Cause and Fix

1. **Explain the mechanism** — full causal chain from cause to symptom. Can't explain? It's proximate, not root.
2. **Predict** — if this is the cause, what else should be true? Check.
3. **Fix at the root** — not the symptom. A null check that suppresses a crash isn't a fix if the object should never be null.
4. **Verify** — original repro resolved + run broader tests for regressions
5. **Write a regression test** — encode the failure so it can't silently return

Feed root cause to `five-whys-root-cause` if systemic, or `causal-inference` if the claim needs rigorous validation.

---

## Output Format

### 🔍 Symptom
- **What fails**: [exact error/behavior/test]
- **When it fails**: [always / intermittent / after action]
- **Since when**: [date/commit, or "unknown"]

### 📋 Observations
| Category | Finding |
|----------|---------|
| Error message | [exact text] |
| Logs | [relevant lines] |
| Recent changes | [commits, config, deps, infra] |
| Environment | [OS, versions, resources] |
| Data | [input, edge cases] |

### 🧠 Hypotheses
| # | Hypothesis | Likelihood | Test | Time |
|---|-----------|------------|------|------|
| 1 | [Most likely] | High | [check] | [min] |
| 2 | [Second] | Medium | [check] | [min] |
| 3 | [Third] | Low | [check] | [min] |

### 🎯 Isolation
- **Dimension**: [commits / code / input / environment]
- **Method**: [git bisect / stubbing / input reduction / env swap]
- **Result**: [what was isolated]

### 🏆 Root Cause
- **Cause**: [precise]
- **Mechanism**: [full causal chain]
- **Fix**: [what to change]
- **Verification**: [how to confirm + regression test]

### ⚠️ Follow-Up
- **Systemic?**: [Yes → five-whys-root-cause / No]
- **Causal claim?**: [Yes → causal-inference / No]
- **Other areas at risk**: [shared pattern/assumption]

---

## Common Traps

- **Guess-and-patch**: fix without confirmed root cause; symptom resurfaces or shifts
- **Confirmation bias**: only seeking supporting evidence; force yourself to *disprove*
- **Fixing the symptom**: null check / retry / try-catch suppressing without understanding
- **Skipping reproduction**: diving in before you can trigger; can't verify the fix
- **Changing multiple things**: bug gone, but you don't know which change fixed it

---

## Thinking Triggers

- *"Can I reproduce this on demand right now?"*
- *"What have I observed vs. what am I assuming?"*
- *"What changed between working and broken?"*
- *"What's the fastest test that eliminates my top hypothesis?"*
- *"Am I fixing the root cause or suppressing a symptom?"*
