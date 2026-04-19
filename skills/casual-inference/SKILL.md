---
name: causal-inference
description: Apply causal inference whenever the user is interpreting metrics, debugging system behavior, reading A/B test results, or trying to understand whether an observed change was caused by an action or by something else. Triggers on phrases like "X caused Y", "since we deployed this, metrics changed", "the A/B test showed a lift", "why did this metric move?", "is this correlation or causation?", "we changed X and Y improved", "how do we know this worked?", "the data shows…", or any situation where conclusions are being drawn from observational data. Also trigger before any decision based on metric interpretation — confusing correlation with causation leads to interventions that don't work and misattribution of credit. Never assume causation without applying this skill.
---

# Causal Inference

**Core principle**: Correlation is not causation — but sometimes it is, and knowing which matters enormously. Use counterfactuals, confounders, and causal structure to ask "did X actually cause Y?" rigorously before acting on data.

---

## The Core Distinction

**Correlation**: X and Y move together.
**Causation**: Changing X changes Y — and we know *why*.

Why it matters:
- Intervening on a correlate with no causal path wastes effort
- Missing a confounder leads to attributing effects to the wrong cause
- Acting on spurious correlation can make things worse

---

## Key Concepts

### Counterfactual Reasoning
The fundamental question:
> *"What would have happened to Y if X had been different, all else equal?"*

You never observe both the treated and untreated state of the same unit at the same time — the **fundamental problem of causal inference**. Every causal claim is implicitly counterfactual; make it explicit.

### Confounders
A third variable Z that causally affects both X and Y, creating correlation between them without a direct causal path.

```
Z → X
Z → Y
```

X and Y correlate, but X doesn't cause Y. Intervening on X does nothing.

**Example**: Ice cream sales and drowning rates correlate. Confounder: hot weather → more ice cream AND more swimming → more drowning. Banning ice cream doesn't reduce drowning.

**Common confounders in product/engineering work**:
- Seasonality (feature adoption and engagement move together)
- Selection bias (users who adopt are already more engaged)
- External events (a competitor shut down the same week you shipped)
- Time trends (both metrics were already moving before intervention)

### Mediators vs. Confounders
A mediator is *on the causal path* — X → M → Y. Blocking it blocks the effect.
A confounder is *upstream of both* — control for it.

Confusing them causes overcorrection (controlling for a mediator removes the effect you're looking for).

### Simpson's Paradox
An observed trend can reverse when data is aggregated. A treatment can appear harmful in aggregate but beneficial in every subgroup (or vice versa) due to unequal group sizes.

**Always ask**: Does disaggregating change the conclusion?

---

## Tools for Establishing Causation

### Randomized Controlled Experiment (Gold Standard)
Random assignment eliminates confounding by making treatment independent of all other variables.

**In product work**: A/B tests are RCTs. Validity depends on:
- Random assignment (not self-selection)
- Sufficient sample size (statistical power)
- Single treatment change (no simultaneous changes)
- No interference between units (SUTVA)
- Correct metric selection

**A/B test failure modes**:
- Novelty effect: early lift decays as users habituate
- Sample Ratio Mismatch: unequal group sizes indicating randomization failure
- Multiple comparisons: 20 metrics gives 1 false positive by chance at p=0.05
- Peeking: stopping early when results look good inflates false positive rate

### Difference-in-Differences (DiD)
Compare the change for a treated group vs. control over time.

```
Effect = (Treated_after - Treated_before) - (Control_after - Control_before)
```

**Assumes**: Without treatment, both groups would have followed parallel trends.
**Use when**: You have pre/post data and a natural control group but couldn't randomize.

### Natural Experiments
External factors create quasi-random treatment variation — policy changes, geographic boundaries, system outages, cohort-based rollouts.

**Example**: Feature rolled out by sign-up date — early users are treatment, later users are control (if no self-selection in timing).

### Causal Graph (DAG)
Map all variables and their causal relationships. Makes confounders and mediators explicit and determines what to control for.

```
[Confounder Z] → [Treatment X] → [Mediator M] → [Outcome Y]
      ↓___________________________________↑
```

Reading the DAG: control for Z (confounder), don't control for M (mediator).

---

## Output Format

### 🔍 Causal Claim Under Examination
- **Stated claim**: [What is asserted to cause what]
- **Reformulated as counterfactual**: *"Would Y have been different if X had not occurred, all else equal?"*

### 🕸️ Causal Structure
Sketch the causal graph:
- Proposed causal paths?
- Potential confounders?
- Mediators (on the causal path)?
- Colliders (caused by both X and Y — controlling opens spurious paths)?

### ⚠️ Threats to Causal Interpretation
For each: **Present / Possible / Unlikely**

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
- **Assumption violations**: [Any signs assumptions don't hold]

### 🎯 Conclusion
- **Causal claim warranted?**: [Yes / Probably / Unclear / No]
- **If yes**: Estimated effect size and confidence
- **If unclear**: What evidence would resolve it?
- **If no**: What alternative explanation better fits the data?

### 🔬 Next Steps
- What experiment would establish causation most efficiently?
- What natural variation in the data could be exploited?
- What confounders should be measured and controlled for?

---

## Causal Inference Checklist for A/B Tests

Before trusting a result:
- [ ] Was assignment truly random? Check Sample Ratio Mismatch.
- [ ] Was only one thing changed?
- [ ] Is sample size sufficient for the expected effect?
- [ ] Was the test run for a full weekly cycle?
- [ ] Is the primary metric pre-specified?
- [ ] Do secondary metrics that should move actually move?
- [ ] Is there a plausible mechanism explaining *why* X would cause Y?
- [ ] Is the effect consistent across segments? (Check Simpson's Paradox)

---

## Thinking Triggers

- *"What's the counterfactual? What would have happened without this change?"*
- *"What else changed at the same time that could explain this?"*
- *"Are the units we're comparing actually comparable?"*
- *"Is there a third variable that could explain the correlation?"*
- *"Does the mechanism make sense — why would X cause Y?"*
- *"Does disaggregating the data change the conclusion?"*
- *"Would we see the same result if we ran this experiment again?"*
