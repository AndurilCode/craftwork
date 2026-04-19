---
name: fermi-estimation
description: Apply Fermi estimation whenever the user needs a quantitative answer but lacks precise data — or when a number is needed quickly to inform a decision, sanity-check a plan, or evaluate feasibility. Triggers on phrases like "how long will this take?", "how much will this cost?", "is this feasible?", "how many X are there?", "what's the order of magnitude?", "rough estimate?", "ballpark this for me", "how many tokens does this use?", "how does this scale?", or any situation requiring a quantitative judgment under uncertainty. Also trigger to sanity-check existing estimates — a Fermi calculation that disagrees with an official estimate by an order of magnitude is a signal worth investigating. Don't refuse to estimate because you lack data. Decompose and calculate.
---

# Fermi Estimation

**Core principle**: Almost any quantity can be estimated to within an order of magnitude by decomposing it into estimable factors and multiplying. Goal is the right number of zeros, not precision. A 10× error is informative; a 1000× error changes the decision.

---

## The Core Process

### Step 1: Define the Target Quantity Precisely
Specify what, over what period, for what scope, in what units.

*"How many tokens does this use?"* → *"Total token count of one Constellation pipeline run, medium-complexity feature, across all agent turns?"*

### Step 2: Decompose into Estimable Factors

```
Target = Factor_1 × Factor_2 × Factor_3 × ...
```

Each factor independently estimable; units cancel correctly; no factor is the original unknown in disguise.

**Patterns**: Rate × Time · Count × Average · Population × Fraction · Flow × Duration

### Step 3: Estimate Each Factor
Explicit reasoning per factor. Round numbers — order of magnitude, not false precision.

### Step 4: Compute and Sanity-Check
Multiply through. Does it pass common sense? Match reference points? Which factor, if wrong, most changes the result?

### Step 5: Bound the Estimate
Low (each factor at low) / Central (best guess) / High (each at high). High/low within ~3× each side = well-bounded. Orders of magnitude apart = one factor too uncertain (validate it).

---

## Output Format

### Target Quantity
- **Estimating**: [Precisely defined quantity]
- **Units**: [What we're counting in]

### Decomposition
| Factor | Estimate | Reasoning |
|--------|----------|-----------|
| [Factor 1] | [Value] | [Why] |
| [Factor 2] | [Value] | [Why] |
| **Product** | **= [Result]** | |

### Range
| Scenario | Estimate | Key driver |
|----------|----------|-----------|
| Low | [Value] | [Factor at low] |
| Central | [Value] | Best guess |
| High | [Value] | [Factor at high] |

### Key Driver
- Which factor contributes most?
- If you could validate one, which?
- A 2× error in [key factor] produces a 2× error in result — worth checking.

### Sanity Checks
- Reference point: [comparable known value]
- Common sense pass? [If no, which factor is suspect?]
- Order-of-magnitude conclusion: [zeros that matter]

---

## Reference Points

**Time**
- Person-hour engineering: ~1–4 hrs focused
- Working hours/week: ~40 (effective ~25–30)
- Working days/month: ~22

**Compute / LLM**
- Token density: ~750 words / 1,000 tokens
- GPT-4-class input: ~$2–10 / M tokens
- LLM response time: 1–10s
- Code file: 50–500 lines; ~100–2,000 tokens

**Scale**
- Small SaaS: 1k–10k MAU
- Mid-size: 100k–1M MAU
- Large platform: 10M+ MAU

**Money**
- Fully-loaded engineer (EU/US): €80k–€200k/yr
- Per-hour: €40–€100
- AWS small instance: ~$10–50/month

---

## Anti-Patterns

- **False precision**: Reporting "42,381 tokens" for an order-of-magnitude estimate. Use round numbers.
- **Single-path decomposition**: Cross-check with an independent decomposition.
- **Forgetting units**: If they don't cancel, the decomposition is wrong.
- **Treating estimate as answer**: Starting point and sanity check, not a substitute for measurement when measurement is warranted.
- **Refusing to estimate**: *"I don't have enough data"* is rarely right when a decision needs to be made. Decompose what you can; flag what you can't.

---

## Thinking Triggers

- *"What does this equal as a product of things I can estimate?"*
- *"What's the right number of zeros?"*
- *"Which single factor, if wrong by 10×, changes my conclusion?"*
- *"What reference point can I sanity-check against?"*
- *"If off by 2×, does the decision change? By 10×?"*

---

## Example: Token Budget for an Agent Pipeline

**Question**: How many tokens does one Constellation run consume?

| Factor | Estimate | Reasoning |
|--------|----------|-----------|
| Agent turns | 8 | 6 agents + orchestrator + review |
| Avg input tokens/turn | 4,000 | System ~1k + context ~2k + task ~1k |
| Avg output tokens/turn | 1,000 | Structured response |
| **Total per run** | **= 8 × 5,000 = 40,000** | |

**Range**: 20k (simple, short context) to 120k (complex, full history).

**Key driver**: Input context size dominates. Compressing context is highest-leverage.

**Sanity check**: 40k @ $5/M = $0.20/run. 100 runs/day = $20/day = ~$600/month. Plausible for a dev tool.
