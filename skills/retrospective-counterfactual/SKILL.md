---
name: retrospective-counterfactual
description: Apply retrospective and counterfactual reasoning whenever something has already happened and the user needs to understand why — or learn from it to improve future decisions. Triggers on phrases like "what went wrong?", "why did this fail?", "post-mortem", "incident review", "we just shipped and it didn't go well", "let's debrief", "what would we have done differently?", "should we have seen this coming?", "what did we miss?", "what would have happened if we'd done X instead?", or any after-the-fact analysis of a completed event. Also trigger to prevent survivorship bias in success analyses — "what made this succeed?" deserves as much causal scrutiny as failure. Look backwards with as much rigor as you look forward.
---

# Retrospective & Counterfactual Reasoning

Looking backwards extracts signal, not blame. Separate predictable from unforeseeable, identify conditions that made failure likely, generate changes that prevent the same failure mode from recurring under different surface conditions. Counterfactual reasoning ("what would have happened if we'd done X?") is the backward-looking complement to the pre-mortem — both require rigorous causal thinking, not post-hoc narrative.

---

## Two Modes

### Mode 1: Post-Mortem / Retrospective
*Something happened. What caused it, what do we change?* Focus: causal reconstruction, systemic learning, forward-looking change.

### Mode 2: Counterfactual Analysis
*What would have happened with a different decision?* Focus: decision quality, calibration, learning from near-misses and successes.

---

## Mode 1: Post-Mortem Process

### Step 1: Reconstruct the Timeline
Establish what happened in sequence with timestamps where possible:
- State before the event
- Triggering conditions
- Sequence of events
- Decision points where the outcome could have diverged

**Separate facts from interpretations**. "Deployment failed at 14:32" is a fact. "Team didn't notice in time" is interpretation — needs evidence.

### Step 2: Identify Contributing Causes
Layered causal analysis:
- **Immediate cause**: the direct trigger
- **Enabling conditions**: what made the system vulnerable
- **Root causes**: systemic conditions that produced the enabling conditions
- **Contributing factors**: context that increased probability/severity

Don't stop at immediate cause — it's almost always the least actionable finding.

**Avoid blame by design**: Replace "person X failed to do Y" with "the system didn't ensure Y happened." People operate within systems.

### Step 3: Classify What Was Knowable
For each cause:
- **Predictable**: foreseeable given available information? Foreseen by anyone?
- **Detectable**: could monitoring/process have surfaced this earlier?
- **Preventable**: was there a plausible intervention?
- **Unforeseeable**: genuinely novel or outside reasonable expectation?

Classification determines corrective action quality:
- Predictable + Preventable = highest-priority systemic fix
- Predictable + Not Prevented = process/incentive problem
- Detectable but Not Detected = monitoring/observability problem
- Genuinely Unforeseeable = resilience/recovery design problem

### Step 4: Generate Corrective Actions
For each systemic finding: what changes, what "done" looks like, who owns it, how to verify it worked.

**Quality test**: Same team, same system, same situation — does this change prevent the same failure? If yes only for this exact scenario, the action is too narrow.

---

## Mode 2: Counterfactual Analysis

### The Core Question
*"What would have happened if decision D had been different?"*

Requires:
1. Identifying the specific decision or condition to vary
2. Reasoning about the causal chain that would have followed
3. Honesty about uncertainty — counterfactuals are inherently speculative

### Counterfactual Validity Rules
Useful counterfactual:
- **Tractable**: alternative was actually available (not hindsight-only)
- **Isolated**: one factor varied at a time
- **Causal**: alternative path follows from the changed decision through a plausible mechanism

Poor counterfactual:
- Assumes information unavailable at decision time
- Changes multiple things simultaneously
- Constructed to justify a preferred conclusion

### Decision Quality vs. Outcome Quality

| Decision | Outcome | Lesson |
|----------|---------|--------|
| Bad | Good | Survivorship bias risk. "It worked" doesn't validate the process. |
| Good | Bad | Process right, outcome unlucky. Don't over-update. |
| Bad | Bad | Outcome was predictable. |
| Good | Bad (systematic) | Model of the world was wrong — update the model. |

Evaluate decisions by quality of reasoning *at the time*, not by outcome.

---

## Output Format

### 📋 Event Summary
- **What happened**: [Factual, sequenced description]
- **Impact**: [Quantified where possible]
- **Timeline**: [Key moments from precondition to resolution]

### 🔍 Causal Analysis

**Immediate cause**: [The direct trigger]

**Enabling conditions**: [What made the system vulnerable]

**Root causes**: [Systemic conditions]

**Contributing factors**: [Context that amplified probability or severity]

### 🗂️ Knowability Classification
| Cause | Predictable? | Detectable? | Preventable? | Classification |
|-------|-------------|------------|--------------|----------------|
| [Cause 1] | Yes/No/Partially | Yes/No | Yes/No | [Type] |

### 🔄 Counterfactual Scenarios (if applicable)
For each decision point worth examining:
- **Decision made**: [What was decided]
- **Alternative considered**: [What could have been done instead]
- **Counterfactual path**: [What would plausibly have followed]
- **Confidence in counterfactual**: [High / Medium / Low — and why]
- **Decision quality assessment**: [Was the original decision reasonable given available information?]

### 🛠️ Corrective Actions
| Finding | Action | Owner | Verification | Timeline |
|---------|--------|-------|-------------|---------|
| [Systemic finding] | [Specific change] | [Who] | [How we know it worked] | [When] |

### 📚 Learning Extraction
- **What does this tell us about the system** (beyond this specific event)?
- **What assumption was wrong** — and should be updated?
- **What category of problem does this represent** — and are there other instances?
- **What early warning signal existed** that we should have been monitoring?

---

## Anti-Patterns to Avoid

- **Hindsight bias**: "We should have known" — without asking whether the information was actually available and acted on.
- **Blame focus**: Naming people as causes rather than systemic conditions that made their actions likely.
- **Single-cause narrative**: Incidents have multiple contributing causes. A neat single story is usually incomplete.
- **Action theater**: Long lists of corrective actions, few of which get done. Better: 2–3 high-quality, owned, verified changes.
- **Success blindness**: Only running retros on failures. Lucky successes are as worth examining as failures.
- **Stopping at immediate cause**: Fixing the last link without addressing what made the chain possible.

---

## Thinking Triggers

- *"Was this predictable? By whom? Why wasn't it acted on?"*
- *"What systemic condition made this failure possible — not just probable?"*
- *"If the same situation arose next month with a different person, would the outcome be different? Why?"*
- *"What's the difference between the decision process and the decision outcome here?"*
- *"What would we have needed to know, at decision time, to choose differently?"*
- *"Are we fixing the last event, or the class of events?"*
