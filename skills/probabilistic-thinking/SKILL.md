---
name: probabilistic-thinking
description: Apply probabilistic and Bayesian thinking whenever the user needs to reason under uncertainty, compare risks, prioritize between options, update beliefs based on new evidence, or make decisions without complete information. Triggers on phrases like "what are the odds?", "how likely is this?", "should I be worried about X?", "which risk is bigger?", "does this data change anything?", "is this a signal or noise?", "what's the probability?", "how confident are we?", or any situation where decisions are being made based on incomplete or ambiguous evidence. Also trigger when someone is treating uncertain outcomes as certainties, or when probability language is being used loosely ("probably", "unlikely", "very likely") without quantification. Don't leave uncertainty unexamined.
---

# Probabilistic & Bayesian Thinking

**Core principle**: Probabilistic thinking replaces vague confidence with calibrated estimates. Bayesian thinking updates those estimates as evidence arrives — neither clinging to priors nor overreacting to new data.

---

## Core Concepts

### Probability as Degree of Belief
"Will probably work" → 60%? 90%? Forcing a number exposes vague confidence and creates a baseline for updating.

### Base Rates
Find the **base rate** before estimating a specific event — how often does this event type occur in a reference class?

*"Will this feature succeed?"* → What % of similar features in similar products succeeded?

Ignoring base rates (**base rate fallacy**) is a top reasoning error.

### Bayesian Updating
Update proportionally — not by ignoring priors, not by overwriting them.

```
New Belief = Prior Belief × Weight of New Evidence
```

- **Prior**: belief before evidence
- **Likelihood**: P(evidence | hypothesis true) vs. false
- **Posterior**: belief after evidence

### Expected Value
```
EV = Probability × Value
```
A 10% chance of +€100 (EV = €10) beats a 90% chance of +€5 (EV = €4.50).

### Confidence Intervals
Point estimates are usually wrong. Ranges are honest.
- "4 weeks" → "3–7 weeks (80% confidence)"
- Wide intervals on uncertain things = calibration, not weakness.

---

## Output Format

### Probability Estimates
| Claim | Prior | Evidence | Updated | Confidence |
|-------|-------|----------|---------|------------|
| "Feature will succeed" | 30% (base rate) | Strong user signal | 55% | Medium |
| "Will ship on time" | 40% (historical) | Experienced team | 50% | Low |

### Base Rate Check
- Reference class for this situation?
- Historical base rate for this outcome?
- How does this case differ from base rate (and does that justify adjustment)?

### Bayesian Update
- **Prior**: belief before
- **New evidence**: what we now know
- **Likelihood ratio**: more consistent with hypothesis true or false?
- **Posterior**: belief now
- **Update size**: did evidence move the needle? (Strong evidence → large; weak → small.)

### Expected Value Comparison
| Option | Probability | Value if succeeds | Value if fails | EV |
|--------|------------|------------------|----------------|----|
| A | 70% | +€50k | -€10k | +€32k |
| B | 30% | +€200k | -€20k | +€46k |

### Confidence Ranges
- **Optimistic** (10th pct): [value]
- **Expected** (50th pct): [value]
- **Pessimistic** (90th pct): [value]
- **Black swan**: [tail scenario]

### Probability Hygiene Flags
- Probabilities treated as certainties (0%/100%)? Almost nothing is certain.
- Base rate ignored for the specific case?
- Overreaction to latest evidence (anchoring)?
- Conjunction fallacy? (P(A and B) < P(A) — more specific = lower probability)

---

## Calibration Heuristics

**Fermi Estimation** — break unknowns into estimable parts:
- "How many users?" → market size × awareness % × conversion % × retention %

**Reference Class Forecasting** — historical data from similar projects:
- "This feature type took 4–8 weeks for 80% of teams in our class"

**Outside View vs. Inside View**:
- Inside: "We're special, we'll beat the average"
- Outside: "What does the data say for projects like this?"
- Default outside. Adjust only with specific, strong evidence.

**Pre-commit to what would change your mind**:
- "If we see X, I'll move probability from 60% to below 30%"
- Prevents post-hoc rationalization.

---

## Thinking Triggers

- *"What's the base rate?"*
- *"Are we treating 70% like certainty?"*
- *"What's the EV of each option, not just the upside?"*
- *"How much should this evidence actually move our belief?"*
- *"What would change our mind significantly?"*
- *"Are we in the reference class we think we're in?"*
- *"What's the downside, and are we weighting it correctly?"*

---

## Example Applications

- **"Should we build this?"** → % of similar features that drove retention? Cost if it fails?
- **"A/B test showed a lift"** → Sample size sufficient? Prior for this change type?
- **"We'll ship in 2 weeks"** → Historical distribution? 80th percentile?
- **"Agent failed once — bug?"** → Base rate of one-off failures? Evidence that would confirm systematic?
