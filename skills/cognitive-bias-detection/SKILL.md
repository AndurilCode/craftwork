---
name: cognitive-bias-detection
description: Apply cognitive bias detection whenever the user (or Claude itself) is making an evaluation, recommendation, or decision that could be silently distorted by systematic thinking errors. Triggers on phrases like "I'm pretty sure", "obviously", "everyone agrees", "we already invested so much", "this has always worked", "just one more try", "I knew it", "the data confirms what we thought", "we can't go back now", or when analysis feels suspiciously aligned with what someone wanted to hear. Also trigger proactively when evaluating high-stakes decisions, plans with significant sunk costs, or conclusions that conveniently support the evaluator's existing position. The goal is not to paralyze — it's to flag where reasoning may be compromised so it can be corrected.
---

# Cognitive Bias Detection

**Core**: Reasoning is systematically distorted by predictable errors operating below conscious awareness. The most dangerous analyses are the ones that *feel* most certain. This skill audits the reasoning process, not just conclusions.

---

## Highest-Impact Biases

### Evaluation & Decision

**Confirmation Bias** — Seeking/interpreting/remembering info that confirms existing beliefs; disconfirming evidence is dismissed.
- *Signal*: "The data confirms what we suspected." Counter-evidence underweighted.
- *Fix*: Seek the strongest case *against*. Assign someone to argue opposite.

**Anchoring** — Overweighting the first number/estimate/framing.
- *Signal*: Estimates cluster around an initial figure; comparisons against an unvalidated reference.
- *Fix*: Generate estimates independently first. "What would this look like without the anchor?"

**Availability Heuristic** — Overweighting recent/vivid events.
- *Signal*: "We just had this incident" → overestimating its probability. Quiet failures ignored.
- *Fix*: Use base rates. "How often does this happen over a long period?"

**Sunk Cost Fallacy** — Continuing because of past investment, not future value.
- *Signal*: "We've put 6 months into this." Reluctance to abandon despite evidence.
- *Fix*: "If we hadn't invested anything, would we start this today?"

**Planning Fallacy** — Systematic underestimation of time/cost/risk.
- *Signal*: Optimistic estimates, no buffer, past overruns treated as exceptions.
- *Fix*: Reference class forecasting — how long did similar projects actually take?

### Social & Group

**Groupthink** — Group harmony overrides realistic appraisal; dissent suppressed.
- *Signal*: Quick agreement, no devil's advocate, contrarian views dismissed socially.
- *Fix*: Assign formal devil's advocate. Independent written opinions before discussion.

**Authority Bias** — Overweighting authority's opinion independent of actual expertise.
- *Signal*: "The CTO thinks X, so it must be right." Analysis stops when authority speaks.
- *Fix*: Evaluate argument on merits. "What's the evidence, separate from who said it?"

**In-group Bias** — Favoring own group's people/ideas/solutions.
- *Signal*: Internal solutions evaluated more generously than identical external ones.
- *Fix*: Blind evaluation. "Would we accept this from a competitor?"

### Framing & Perception

**Framing Effect** — Same info → different decisions based on presentation (gain vs. loss).
- *Signal*: "90% success" vs. "10% failure" trigger different reactions.
- *Fix*: Reframe every option multiple ways. Does the decision change?

**Survivorship Bias** — Conclusions from visible successes, ignoring invisible failures.
- *Signal*: "Company X did Y and succeeded" — but how many tried Y and failed?
- *Fix*: Seek failure cases. "What don't we see because they didn't survive?"

**Dunning-Kruger** — Low competence → overconfidence; high competence → underconfidence.
- *Signal*: Extreme certainty in novel/complex domain, or excessive expert hedging.
- *Fix*: Calibrate confidence against demonstrated track record in this domain.

**Recency Bias** — Overweighting recent data, underweighting long-term patterns.
- *Signal*: Last quarter dominates analysis; historical base rates ignored.
- *Fix*: Extend the time window. Multi-year trends, not just recent.

---

## Output Format

### 🔍 Bias Scan
| Bias | Present? | Signal Observed | Severity |
|------|----------|----------------|----------|
| Confirmation | Y/Possible/N | [Evidence] | L/M/H |
| Sunk Cost | Y/Possible/N | [Evidence] | L/M/H |
| ... | | | |

### ⚠️ High-Risk Findings
For each high-severity bias:
- **Bias**: Name + brief description
- **How it shows up**: Specific evidence
- **What it distorts**: Conclusion/estimate skewed, in which direction
- **Debiasing move**: Concrete corrective action

### 🧹 Debiased Re-evaluation
- What changes if the bias is removed?
- What evidence is actually strong vs. inflated by bias?
- Does the conclusion still hold?

### 🎯 Confidence Calibration
- Actual warranted confidence absent bias?
- What needs to be true for higher confidence?
- Most important thing to validate before committing?

---

## Meta-Check: Is Claude Biased Here?

When generating evaluations, check:
- Confirming what the user wants to hear? (sycophancy / confirmation)
- Anchoring to the user's first framing?
- Overweighting most vivid/recent example?
- Assuming user's group/team/approach is better without evidence?

If yes — flag and correct.

---

## Triggers

- *"How would this look if we'd concluded the opposite from the start?"*
- *"What's the strongest evidence against the current conclusion?"*
- *"Are we continuing because it's right, or because we've invested too much to stop?"*
- *"Who benefits from this conclusion, and are they evaluating it?"*
- *"If a stranger reviewed this reasoning, what would they say we're missing?"*
