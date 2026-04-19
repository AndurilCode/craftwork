---
name: decision-intelligence
description: "Apply when ALL THREE conditions hold: (1) a single decision or belief is evaluated — not comparing multiple options; (2) probability and outcome magnitude are estimable; (3) human bias likely distorts reasoning — sunk costs, survivorship bias, intuition vs. math, or real money/time at stake. Triggers on 'should I do this?', 'is this worth it?', 'I've already put so much into this', or single-path decisions involving financial bets, career moves, or long-term commitments. NOT for comparing options (decision-synthesis), probability estimation (probabilistic-thinking), or estimation (fermi-estimation). Mandatory-process: applies all 6 models without exception."
---

# Decision Intelligence — 6-Model Framework

**Core principle**: Every decision is a probability problem. Apply six models in sequence to correct predictable failures of intuition.

**MANDATORY**: Apply all 6 models to every input. Never skip. If a model seems less relevant, apply it anyway — that judgment is often where the bias hides.

---

## Step 0: Clarify the Core Question

Restate the decision in one sentence: *"The real question is: [single clear question]."* Sharpen if fuzzy.

---

## Step 1 — Expected Value (EV)

**Mechanic**: EV = Σ (probability × payoff)

**Process**:
1. List all meaningful outcomes (not just best/worst — include most likely)
2. Assign probabilities summing to 100%
3. Estimate payoff per outcome (financial, time, opportunity, emotional — units explicit)
4. Calculate EV = Σ (p × payoff)
5. Flag if loss aversion is inflating perceived cost of negatives

**Output**:
| Outcome | Probability | Payoff | EV contribution |
|---------|------------|--------|----------------|
| [A] | X% | +€Y | +€Z |
| [B] | X% | -€Y | -€Z |
| **Total EV** | 100% | | **€[sum]** |

**Bias**: Loss aversion — losses feel ~2× gains. Positive EV + hesitation = loss aversion likely.

---

## Step 2 — Base Rate Neglect

**Mechanic**: Anchor on the historical rate for this category before adjusting for specifics.

**Process**:
1. Identify the reference class
2. Find/estimate the base rate for success/failure
3. Only then apply specific adjustments
4. Flag if user is reasoning from vivid anecdotes rather than rates

**Common base rates**:
- Startups reaching profitability: ~10–20%
- New restaurants surviving year 1: ~40% (year 5: ~20%)
- New products achieving PMF: ~5–15%
- Day traders beating market consistently: ~1–5%
- New habits maintained 6 months: ~20%
- Projects on time + budget: ~30–35%

**Bias**: Availability — we hear successes; the silent majority of failures is invisible.

---

## Step 3 — Sunk Cost Fallacy

**Mechanic**: Ignore everything already spent. Evaluate as if starting today.

**Process**:
1. Identify all sunk costs (money, time, emotion, public statements)
2. Set them to zero
3. Re-evaluate using only future costs/benefits/probabilities
4. If the answer changes when zeroed → fallacy is active

**Diagnostic**: *"If I had not already invested [X], would I start this today?"*
- Yes → proceed for the right reasons
- No → sunk cost is the only reason to continue

**Bias**: Escalation of commitment — the more invested, the harder to walk away.

---

## Step 4 — Bayesian Thinking

**Mechanic**: Update beliefs proportionally to evidence strength.

```
P(belief | evidence) = P(evidence | belief) × P(belief) / P(evidence)
```

- **Prior**: belief before evidence
- **Likelihood**: P(evidence | true) vs P(evidence | false)
- **Posterior**: belief after evidence

**Process**:
1. State prior as a probability, not impression
2. Identify the new evidence
3. Estimate likelihood ratio (true vs. false)
4. Update proportionally — never to 0%/100%, never ignore the prior
5. State posterior

**Bias**: Overreaction to single data points — a single anecdote rarely shifts a prior more than a few points unless highly diagnostic.

---

## Step 5 — Survivorship Bias

**Mechanic**: When seeing successes, estimate the invisible denominator.

**Process**:
1. Count visible successes
2. Estimate hidden total: *"How many tried this? How many am I not hearing from?"*
3. Implied success rate = visible / total attempts
4. Check consistency with Step 2 base rate

**Diagnostic**: *"What would I need to see to hear about the failures? Why don't I?"*

**Bias**: Narrative — successes have arcs and lessons; failures are quiet and diffuse.

---

## Step 6 — Kelly Criterion

**Mechanic**: When you have an edge, size the bet for long-term growth without ruin.

```
f* = (p × b - q) / b
```

- `f*` = fraction of capital to bet
- `p` = win probability
- `q` = lose probability (1 − p)
- `b` = net odds (win per unit risked)

**Use fractional Kelly** (¼ to ½ f*) for real decisions. Half-Kelly gives ~75% of the growth with much less volatility.

**Process**:
1. Estimate p from Steps 1–5
2. Estimate b
3. Calculate f*
4. Recommend ½f* (moderate confidence) or ¼f* (high uncertainty)
5. If f* ≤ 0: no edge — do not bet
6. If f* > 1: extreme edge — recheck probabilities

**Bias**: Overbetting — humans size positions too large for their actual edge, especially after wins.

---

## Final: Synthesized Recommendation

```
DECISION INTELLIGENCE SYNTHESIS

Core question: [from Step 0]

Model verdicts:
- EV: [positive/negative/marginal, key number]
- Base rate: [X% success for this category]
- Sunk cost: [active / not — does decision change when zeroed?]
- Bayesian update: [prior → evidence → posterior]
- Survivorship bias: [true rate vs. observed stories]
- Kelly sizing: [f* = X%, allocation = Y%]

Primary bias in play: [the one most distorting this decision]

Recommendation: [clear action]
Confidence: [0–100%]
Key risks: [top 2–3]
What would change this view: [specific evidence]
```

If math contradicts intuition, say so. Discomfort with the conclusion often signals the analysis is working.

---

## Relationship to Other Skills

- Run **before** `decision-synthesis` when stakes are quantifiable — provides probabilistic inputs to weigh
- Complements `probabilistic-thinking` (Bayesian depth) and `cognitive-bias-detection` (broad audit) — this skill applies both to decision sizing and commitment
- When `scenario-planning` produces multiple futures, run this skill on the decision within each
- `fermi-estimation` feeds Step 1 (EV) and Step 2 (base rates) when numbers aren't ready
