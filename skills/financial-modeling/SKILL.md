---
name: financial-modeling
description: "Apply financial modeling whenever the user needs quantitative rigor for a business decision — evaluating an investment, pricing a product, comparing costs and benefits, or assessing profitability. Triggers on phrases like \"what's the unit economics?\", \"build a financial model\", \"is this profitable?\", \"what's the ROI?\", \"pricing strategy\", \"cost-benefit analysis\", \"what's the NPV?\", \"should we invest in this?\". Use proactively when a decision has financial implications that the user has not quantified."
---

# Financial Modeling

**Core principle**: Every business decision has a financial structure that can be made explicit. Decompose the decision into revenue drivers, cost drivers, and timing — then stress-test the assumptions that swing the outcome. The model is not the answer; the sensitivity analysis is.

---

## When to Use This Skill

- The user is evaluating whether to invest in a project, product, or initiative
- A pricing decision needs analytical backing
- Someone asks "is this profitable?" or "what's the ROI?" without a structured model
- A decision-synthesis analysis needs financial criteria and scores
- A fermi-estimation output needs to be refined into a rigorous financial model
- The user is comparing options with different cost structures or revenue timelines

---

## Core Methodology

### Step 1: Frame the Financial Question

Define precisely what financial outcome is being evaluated and for whom.

- What is the decision? (invest/don't invest, option A vs. B, price at X vs. Y)
- What is the time horizon? (months, years — match to the decision's natural lifecycle)
- Who bears the costs and who captures the value?
- What discount rate is appropriate? (cost of capital, opportunity cost, or a stated hurdle rate)

If the inputs are rough estimates, accept them from `fermi-estimation` via Contract M and flag which ones need validation.

### Step 2: Map Unit Economics

Decompose to the smallest repeatable economic unit — per customer, per transaction, per unit sold, per API call.

- **Revenue per unit**: price × volume, or recurring revenue × retention
- **Cost per unit**: direct costs (COGS, marginal cost) + allocated indirect costs
- **Contribution margin**: revenue per unit minus cost per unit
- **Break-even volume**: fixed costs divided by contribution margin

If the business model does not have clean unit economics (e.g., platform with network effects), identify the value driver (e.g., users, transactions, data volume) and model economics around that driver.

### Step 3: Build the Cost-Benefit Table

Enumerate all costs and benefits explicitly. Categorize each:

- **Direct costs**: engineering time, infrastructure, licensing, materials
- **Indirect costs**: opportunity cost of the team, coordination overhead, technical debt
- **Direct benefits**: revenue, cost savings, efficiency gains
- **Indirect benefits**: option value (enables future moves), learning value, strategic positioning

Discount future values to present using the rate from Step 1. Compute:
- **NPV** (Net Present Value): sum of discounted net cash flows
- **IRR** (Internal Rate of Return): the discount rate at which NPV = 0
- **Payback period**: when cumulative net cash flow turns positive

### Step 4: Model Scenarios

Build three cases by varying key assumptions:

- **Base case**: most likely values for each assumption
- **Upside case**: optimistic but plausible values (not best-case fantasy)
- **Downside case**: pessimistic but plausible values (not worst-case catastrophe)

For each scenario, recompute NPV, payback, and contribution margin. The spread between upside and downside is itself informative — a wide spread means high uncertainty and lower confidence.

### Step 5: Run Sensitivity Analysis

Identify which assumption, if wrong, changes the decision.

- Vary each key assumption independently by +/- 25% and +/- 50%
- Record which assumption produces the largest swing in NPV
- That assumption is the **key financial risk** — it deserves the most validation effort

If two assumptions interact (e.g., price and volume are correlated), model the interaction explicitly rather than treating them as independent.

### Step 6: Produce Financial Criteria for Decision-Synthesis

When this analysis feeds into `decision-synthesis` via Contract G, translate the financial findings into decision criteria:

- Convert financial thresholds into must-have or want-to-have criteria (e.g., "NPV > $0" is must-have; "payback < 18 months" is want-to-have)
- Score each option on a 1-5 scale based on financial performance
- Flag the key financial risk and the scenario spread as confidence modifiers
- Assign weight suggestions based on how financially dominant the decision is

---

## Output Format

### 🎯 Decision Under Evaluation
- **Decision**: [what is being decided]
- **Time horizon**: [N years/months]
- **Discount rate**: [X% — with justification]

### 📋 Key Financial Assumptions
| Assumption | Value | Source | Confidence |
|-----------|-------|--------|------------|
| [e.g., Monthly active users Y1] | [value] | [fermi-estimation / market data / internal] | [H/M/L] |
| [e.g., Price per unit] | [value] | [source] | [H/M/L] |
| [e.g., Infrastructure cost per user] | [value] | [source] | [H/M/L] |

### 📊 Unit Economics
- **Revenue per unit**: [value]
- **Cost per unit**: [value]
- **Contribution margin**: [value] ([percentage]%)
- **Break-even volume**: [value]

### ⚖️ Cost-Benefit Summary
| Category | Item | Year 1 | Year 2 | Year 3 | NPV |
|----------|------|--------|--------|--------|-----|
| Cost | [item] | [value] | [value] | [value] | [value] |
| Benefit | [item] | [value] | [value] | [value] | [value] |
| **Net** | | [value] | [value] | [value] | **[NPV]** |

- **IRR**: [value]%
- **Payback period**: [N months/years]

### 📊 Scenario Analysis
| Scenario | NPV | Payback | Key Assumption Changed |
|----------|-----|---------|----------------------|
| Downside | [value] | [value] | [assumption at pessimistic value] |
| Base | [value] | [value] | Most likely values |
| Upside | [value] | [value] | [assumption at optimistic value] |

### ⚠️ Sensitivity Analysis
| Assumption | -50% | -25% | Base | +25% | +50% | NPV Swing |
|-----------|------|------|------|------|------|-----------|
| [key assumption 1] | [NPV] | [NPV] | [NPV] | [NPV] | [NPV] | [max-min] |
| [key assumption 2] | [NPV] | [NPV] | [NPV] | [NPV] | [NPV] | [max-min] |

- **Key financial risk**: [the assumption that, if wrong, changes the answer]

### 🏆 Recommendation
- **Financial verdict**: [invest / do not invest / conditional on validating X]
- **Confidence**: [High / Medium / Low — informed by scenario spread and sensitivity]
- **Decision-synthesis criteria** (Contract G):
  - [criterion, e.g., "NPV > $X over 3 years"] — type: [must-have/want-to-have], weight suggestion: [N]
  - [criterion, e.g., "Payback < 18 months"] — type: [must-have/want-to-have], weight suggestion: [N]
- **Financial scores per option** (if comparing):
  - Option A: NPV = $X, payback = Y months, score = [1-5]
  - Option B: NPV = $X, payback = Y months, score = [1-5]

---

## Common Traps

**False precision**: Reporting NPV to the dollar when inputs are order-of-magnitude estimates. Match output precision to input precision — if costs are +/- 50%, the NPV is too.

**Ignoring opportunity cost**: Comparing an investment to zero instead of to the next-best use of the same resources. The baseline is not "do nothing" — it is "do the next-best thing."

**Hockey stick projections**: Revenue grows exponentially while costs stay flat. Challenge any model where margins improve dramatically over time without a structural reason.

**Sunk cost inclusion**: Including already-spent costs in forward-looking analysis. Only future cash flows matter for the decision. Past spending is irrelevant to whether continuing is worthwhile.

**Single-scenario thinking**: Presenting only the base case. Without upside/downside, stakeholders cannot assess risk. The scenario spread is as important as the point estimate.

**Trusting LLM arithmetic**: An LLM applying this skill will structure the model correctly but may compute NPV, IRR, or sensitivity figures inaccurately. Always verify calculations in a spreadsheet or calculator. Use this skill for structure, assumptions, and logic — not as a replacement for a real financial model.

---

## Thinking Triggers

- *"What are the unit economics of this at the atomic level?"*
- *"Which single assumption, if wrong by 2x, flips this decision?"*
- *"What is the opportunity cost — what else could these resources do?"*
- *"Does the upside-downside spread change my confidence in the recommendation?"*
- *"Am I modeling what I hope will happen, or what is most likely to happen?"*
