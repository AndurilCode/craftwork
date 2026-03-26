---
name: debugging-methodology
description: "Apply debugging methodology whenever the user faces a software failure they cannot explain — a broken test, unexpected behavior, a regression, or an intermittent bug. Triggers on phrases like \"why is this broken?\", \"how do I debug this?\", \"the test fails but I don't know why\", \"intermittent failure\", \"works on my machine\", \"this used to work\", \"regression\". Use proactively when the user describes a symptom and jumps straight to a fix without isolating the root cause."
---

# Debugging Methodology

**Core principle**: Systematic debugging outperforms intuition. Resist the urge to guess-and-patch. Instead: reproduce, observe, hypothesize, isolate, verify. The goal is root cause, not symptom suppression — a fix that addresses the wrong cause will break again.

---

## When to Use This Skill

- A test fails and the reason is not immediately obvious
- Behavior changed and nobody knows what caused it
- A bug is intermittent or environment-dependent
- The user is pattern-matching to a fix without evidence for the root cause
- A fix was applied but the problem recurred or shifted

---

## Core Methodology

### Step 1: Reproduce the Failure

Establish a reliable reproduction before doing anything else. A bug you cannot trigger on demand is a bug you cannot verify you have fixed.

- Record the exact steps, inputs, and environment that produce the failure
- If the failure is intermittent, characterize its frequency and conditions (load level, timing, data shape, concurrency)
- If you cannot reproduce locally, identify the environmental difference — OS, dependency version, configuration, data volume, network conditions
- **No reproduction, no diagnosis.** If reproduction is impossible, instrument the code to capture state on next occurrence and move to Step 2 with the data you have

### Step 2: Observe Before Theorizing

Collect evidence without forming conclusions yet. Premature hypotheses create confirmation bias — you look for evidence that supports your theory and ignore evidence that contradicts it.

Gather:
- Full error messages and stack traces (not paraphrased — exact text)
- Relevant log output surrounding the failure
- System state: memory, CPU, disk, open connections, queue depth
- Recent changes: commits, config changes, dependency updates, infrastructure changes
- Data state: what input triggered the failure? Is the data valid?

Write down what you observe. Separate facts ("the error is a NullPointerException on line 42") from interpretations ("the object must not be initialized").

### Step 3: Generate and Rank Hypotheses

Based on observations, list every plausible cause. Then rank by:

1. **Likelihood** — given the evidence, how probable is this cause?
2. **Testability** — how quickly can you confirm or rule it out?
3. **Impact** — if this is the cause, how severe is it?

Prioritize hypotheses that are both likely and fast to test. A 30-second check that eliminates a candidate is always worth running first.

**Differential diagnosis**: What changed? Walk through each category:
- **Code**: recent commits, merge conflicts, refactors
- **Configuration**: environment variables, feature flags, settings files
- **Data**: new data patterns, schema changes, edge cases
- **Dependencies**: version bumps, transitive dependency changes
- **Infrastructure**: deployment changes, resource limits, network topology

### Step 4: Isolate with Binary Search

Narrow the search space systematically rather than reading code line by line.

- **Bisect commits**: use `git bisect` to find the exact commit that introduced the failure
- **Bisect code**: comment out or stub components until the failure disappears, then re-enable them one by one
- **Bisect input**: reduce the failing input to the minimal case that still triggers the bug
- **Bisect environment**: swap one environmental variable at a time between working and broken environments

Each bisection step should halve the remaining search space. If it does not, choose a different dimension to bisect.

### Step 5: Confirm Root Cause and Fix

Once you have a candidate root cause:

1. **Explain the mechanism** — articulate exactly how this cause produces the observed symptom. If you cannot explain the full causal chain, you may have a proximate cause, not the root cause
2. **Predict** — if this is the root cause, what else should be true? Check those predictions
3. **Fix at the root** — address the underlying cause, not the surface symptom. A null check that suppresses a crash is not a fix if the object should never be null
4. **Verify** — confirm the fix resolves the original reproduction case. Run the broader test suite to check for regressions
5. **Write a regression test** — encode the failure as a test so it cannot silently return

Feed the confirmed root cause to `five-whys-root-cause` if the failure is systemic, or to `causal-inference` if the root cause involves a causal claim that needs rigorous validation.

---

## Output Format

### 🔍 Symptom Description
- **What fails**: [exact error, behavior, or test name]
- **When it fails**: [conditions — always, intermittently, after specific action]
- **Since when**: [first observed date/commit, or "unknown"]

### 📋 Observations Collected
| Category | Finding |
|----------|---------|
| Error message | [exact text] |
| Logs | [relevant log lines] |
| Recent changes | [commits, config, deps, infra] |
| Environment | [OS, versions, resource state] |
| Data | [input characteristics, edge cases] |

### 🧠 Hypothesis List
| # | Hypothesis | Likelihood | Test to confirm/rule out | Time to test |
|---|-----------|------------|--------------------------|-------------|
| 1 | [Most likely cause] | High | [What to check] | [Minutes] |
| 2 | [Second candidate] | Medium | [What to check] | [Minutes] |
| 3 | [Third candidate] | Low | [What to check] | [Minutes] |

### 🎯 Isolation Strategy
- **Dimension**: [commits / code / input / environment]
- **Method**: [git bisect / component stubbing / input reduction / env swap]
- **Result**: [what was isolated]

### 🏆 Root Cause
- **Cause**: [precise description of what went wrong and why]
- **Mechanism**: [how the cause produces the symptom — full causal chain]
- **Fix**: [what to change]
- **Verification**: [how to confirm the fix works + regression test added]

### ⚠️ Follow-Up
- **Systemic?**: [Yes → feed to five-whys-root-cause / No → done]
- **Causal claim?**: [Yes → feed to causal-inference / No → done]
- **Other areas at risk**: [code that shares the same pattern or assumption]

---

## Common Traps

**Guess-and-patch**: Applying a fix based on intuition without confirming the root cause. The symptom disappears temporarily, then resurfaces or shifts to a different failure.

**Confirmation bias**: Forming a hypothesis early and only looking for evidence that supports it. Force yourself to try to *disprove* each hypothesis, not prove it.

**Fixing the symptom**: Adding a null check, retry loop, or try-catch that suppresses the error without understanding why the error occurs. The underlying cause remains and will manifest differently.

**Skipping reproduction**: Diving into code before confirming you can trigger the failure. Without a reproduction case, you cannot verify your fix.

**Changing multiple things at once**: Making several changes simultaneously, then finding the bug is gone. You do not know which change fixed it — or whether they interact to mask the real problem.

---

## Thinking Triggers

- *"Can I reproduce this failure right now, on demand?"*
- *"What have I observed vs. what am I assuming?"*
- *"What changed between the working state and the broken state?"*
- *"What is the fastest test that would eliminate my top hypothesis?"*
- *"Am I fixing the root cause or suppressing a symptom?"*
