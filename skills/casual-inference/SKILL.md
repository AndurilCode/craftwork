---
name: causal-inference
description: Apply causal inference whenever the user is interpreting metrics, debugging system behavior, reading A/B test results, or trying to understand whether an observed change was caused by an action or by something else. Triggers on phrases like "X caused Y", "since we deployed this, metrics changed", "the A/B test showed a lift", "why did this metric move?", "is this correlation or causation?", "we changed X and Y improved", "how do we know this worked?", "the data shows…", or any situation where conclusions are being drawn from observational data. Also trigger before any decision based on metric interpretation — confusing correlation with causation leads to interventions that don't work and misattribution of credit. Never assume causation without applying this skill.
---

# Causal Inference

**Core principle**: Correlation is not causation — but also, correlation is sometimes causation, and knowing which matters enormously. This skill provides the tools to ask "did X actually cause Y?" rigorously — using counterfactuals, confounders, and causal structure before acting on data.

---

## The Core Distinction

**Correlation**: X and Y move together.
**Causation**: Changing X changes Y — and we know *why*.

The difference matters because:
- Intervening on a correlate with no causal path wastes effort and money
- Missing a confounder leads to attributing effects to the wrong cause
- Acting on spurious correlation can make things worse

---

## Key Concepts

### Counterfactual Reasoning
The fundamental question of causation:
> *"What would have happened to Y if X had been different, all else equal?"*

This is harder than it sounds — you never observe both the treated and untreated state of the same unit at the same time. This is the **fundamental problem of causal inference**.

Every causal claim is implicitly a counterfactual claim. Make it explicit.

### Confounders
A confounder is a third variable Z that causally affects both X and Y, creating a correlation between them that isn't a direct causal path.

```
Z → X
Z → Y
```
X and Y are correlated, but X doesn't cause Y. Intervening on X does nothing.

**Example**: Ice cream sales and drowning rates are correlated. Confounder: hot weather → more ice cream AND more swimming → more drowning. Banning ice cream doesn't reduce drowning.

**Common confounders in product/engineering work**:
- Seasonality (both feature adoption and engagement move together)
- Selection bias (users who adopt a feature are already more engaged)
- External events (a competitor shut down the same week you shipped the feature)
- Time trends (both metrics were already moving before the intervention)

### Mediators vs. Confounders
A mediator is *on the causal path* — X → M → Y. Blocking a mediator blocks the effect.
A confounder is *upstream of both* — you should control for it.

Confusing them leads to overcorrection (controlling for a mediator removes the effect you're looking for).

### Simpson's Paradox
An observed trend can reverse when data is aggregated. A treatment can appear harmful in aggregate but beneficial in every subgroup (or vice versa), due to unequal group sizes.

**Always ask**: Does disaggregating the data change the conclusion?

---

## Tools for Establishing Causation

### Randomized Controlled Experiment (Gold Standard)
Randomly assign units to treatment and control. Randomization eliminates confounding by making treatment independent of all other variables.

**In product work**: A/B tests are RCTs. Their validity depends on:
- Random assignment (not self-selection)
- Sufficient sample size (statistical power)
- Single treatment change (no simultaneous changes)
- No interference between units (SUTVA)
- Correct metric selection (measuring the right thing)

**A/B test failure modes**:
- Novelty effect: early lift decays as users habituate
- Sample Ratio Mismatch: unequal group sizes indicating randomization failure
- Multiple comparisons: testing 20 metrics gives 1 false positive by chance at p=0.05
- Peeking: stopping early when results look good inflates false positive rate

### Difference-in-Differences (DiD)
Compare the change in an outcome for a treated group vs. a control group over time.

```
Effect = (Treated_after - Treated_before) - (Control_after - Control_before)
```

**Assumes**: In the absence of treatment, both groups would have followed parallel trends.

**When to use**: When you have pre/post data and a natural control group but couldn't randomize.

### Natural Experiments
Look for situations where external factors created quasi-random variation in treatment — policy changes, geographic boundaries, system outages, feature rollouts by cohort.

**Example**: Feature rolled out to users by sign-up date — early users are treatment, later users are control (if no self-selection bias in timing).

### Causal Graph (DAG)
Draw the Directed Acyclic Graph — map all variables and their causal relationships. This makes confounders and mediators explicit and determines what to control for.

```
[Confounder Z] → [Treatment X] → [Mediator M] → [Outcome Y]
      ↓___________________________________↑
```

Reading the DAG: control for Z (confounder), don't control for M (mediator).

---

## Output Format

### 🔍 Causal Claim Under Examination
- **Stated claim**: [What is being asserted caused what]
- **Reformulated as counterfactual**: *"Would Y have been different if X had not occurred, all else equal?"*

### 🕸️ Causal Structure
Sketch the causal graph:
- What are the proposed causal paths?
- What are the potential confounders?
- What are the mediators (variables on the causal path)?
- What are the colliders (variables caused by both X and Y — controlling for these opens spurious paths)?

### ⚠️ Threats to Causal Interpretation
For each threat, assess: **Present / Possible / Unlikely**

| Threat | Present? | Evidence | Impact on Conclusion |
|--------|----------|----------|---------------------|
| Confounding | | | |
| Selection bias | | | |
| Reverse causation (Y → X) | | | |
| Common cause (Z → X, Z → Y) | | | |
| Seasonality / time trend | | | |
| Coincidental timing | | | |
| Simpson's Paradox | | | |

### 📊 Evidence Quality
- **Design used**: [RCT / DiD / Natural experiment / Observational]
- **Evidence strength**: [Strong / Moderate / Weak]
- **Key assumptions**: [What must be true for the design to be valid]
- **Assumption violations**: [Any signs the assumptions don't hold]

### 🎯 Conclusion
- **Causal claim warranted?**: [Yes / Probably / Unclear / No]
- **If yes**: Estimated effect size and confidence
- **If unclear**: What evidence would resolve it?
- **If no**: What alternative explanation better fits the data?

### 🔬 Next Steps
- What experiment would establish causation most efficiently?
- What natural variation exists in the data that could be exploited?
- What confounders should be measured and controlled for?

---

## Causal Inference Checklist for A/B Tests

Before trusting a result:
- [ ] Was assignment truly random? Check Sample Ratio Mismatch.
- [ ] Was only one thing changed?
- [ ] Is the sample size sufficient for the expected effect size?
- [ ] Was the test run for a full weekly cycle (day-of-week effects)?
- [ ] Is the primary metric pre-specified? (Not chosen after seeing results)
- [ ] Are there secondary metrics that should move if the hypothesis is right — and do they?
- [ ] Is there a plausible mechanism explaining *why* X would cause Y?
- [ ] Is the effect consistent across segments? (Check for Simpson's Paradox)

---

## Thinking Triggers

- *"What's the counterfactual? What would have happened without this change?"*
- *"What else changed at the same time that could explain this?"*
- *"Are the users/units we're comparing actually comparable?"*
- *"Is there a third variable that could explain the correlation?"*
- *"Does the mechanism make sense — why would X cause Y?"*
- *"Does disaggregating the data change the conclusion?"*
- *"Would we see the same result if we ran this experiment again?"*
