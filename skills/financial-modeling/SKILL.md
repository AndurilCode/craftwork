---
name: financial-modeling
description: "Apply financial modeling whenever the user needs quantitative rigor for a business decision — evaluating an investment, pricing a product, comparing costs and benefits, or assessing profitability. Triggers on phrases like \"what's the unit economics?\", \"build a financial model\", \"is this profitable?\", \"what's the ROI?\", \"pricing strategy\", \"cost-benefit analysis\", \"what's the NPV?\", \"should we invest in this?\". Use proactively when a decision has financial implications that the user has not quantified."
---

# Financial Modeling

**Core principle**: Decompose the decision into revenue drivers, cost drivers, and timing — then stress-test the assumptions that swing the outcome. The model isn't the answer; the sensitivity analysis is.

---

## When to Use This Skill

- Evaluating whether to invest in a project, product, or initiative
- A pricing decision needs analytical backing
- "Is this profitable?" or "what's the ROI?" without a structured model
- A decision-synthesis analysis needs financial criteria and scores
- A fermi-estimation output needs refining into a rigorous model
- Comparing options with different cost structures or revenue timelines

---

## Core Methodology

### Step 1: Frame the Financial Question

- What's the decision? (invest/don't, A vs. B, price X vs. Y)
- Time horizon? (match to decision's natural lifecycle)
- Who bears costs, who captures value?
- Discount rate? (cost of capital, opportunity cost, or stated hurdle rate)

If inputs are rough, accept them from `fermi-estimation` via Contract M and flag what needs validation.

### Step 2: Map Unit Economics

Decompose to the smallest repeatable economic unit — per customer, transaction, unit sold, API call.

- **Revenue per unit**: price × volume, or recurring revenue × retention
- **Cost per unit**: direct (COGS, marginal) + allocated indirect
- **Contribution margin**: revenue − cost per unit
- **Break-even volume**: fixed costs / contribution margin

If clean unit economics don't exist (e.g., platform with network effects), identify the value driver (users, transactions, data volume) and model around it.

### Step 3: Build the Cost-Benefit Table

Enumerate explicitly. Categorize each:

- **Direct costs**: engineering time, infrastructure, licensing, materials
- **Indirect costs**: opportunity cost, coordination overhead, technical debt
- **Direct benefits**: revenue, cost savings, efficiency gains
- **Indirect benefits**: option value, learning, strategic positioning

Discount future to present using Step 1's rate. Compute:
- **NPV**: sum of discounted net cash flows
- **IRR**: discount rate at which NPV = 0
- **Payback period**: when cumulative net cash flow turns positive

### Step 4: Model Scenarios

Three cases by varying key assumptions:

- **Base**: most likely
- **Upside**: optimistic but plausible (not best-case fantasy)
- **Downside**: pessimistic but plausible (not worst-case catastrophe)

Recompute NPV, payback, contribution margin per scenario. Wide upside-downside spread = high uncertainty, lower confidence.

### Step 5: Run Sensitivity Analysis

Identify which assumption, if wrong, changes the decision.

- Vary each key assumption ±25% and ±50%
- Record the largest NPV swing
- That's the **key financial risk** — deserves the most validation effort

If two assumptions interact (e.g., price and volume), model the interaction explicitly.

### Step 6: Produce Financial Criteria for Decision-Synthesis

Feeding `decision-synthesis` via Contract G, translate findings into criteria:

- Convert thresholds to must-have or want-to-have ("NPV > $0" must-have; "payback < 18 months" want-to-have)
- Score each option 1-5 on financial performance
- Flag key financial risk and scenario spread as confidence modifiers
- Suggest weights based on how financially dominant the decision is

---

## Output Format

### 🎯 Decision Under Evaluation
- **Decision**: [what's being decided]
- **Time horizon**: [N years/months]
- **Discount rate**: [X% — with justification]

### 📋 Key Financial Assumptions

| Assumption | Value | Source | Confidence |
|-----------|-------|--------|------------|
| [Monthly active users Y1] | [value] | [fermi/market/internal] | H/M/L |
| [Price per unit] | [value] | [source] | H/M/L |
| [Infra cost per user] | [value] | [source] | H/M/L |

### 📊 Unit Economics
- **Revenue per unit**: [value]
- **Cost per unit**: [value]
- **Contribution margin**: [value] ([%])
- **Break-even volume**: [value]

### ⚖️ Cost-Benefit Summary

| Category | Item | Y1 | Y2 | Y3 | NPV |
|----------|------|----|----|----|-----|
| Cost | [item] | [value] | [value] | [value] | [value] |
| Benefit | [item] | [value] | [value] | [value] | [value] |
| **Net** | | [value] | [value] | [value] | **[NPV]** |

- **IRR**: [value]%
- **Payback period**: [N months/years]

### 📊 Scenario Analysis

| Scenario | NPV | Payback | Key Assumption Changed |
|----------|-----|---------|----------------------|
| Downside | [value] | [value] | [assumption at pessimistic] |
| Base | [value] | [value] | Most likely values |
| Upside | [value] | [value] | [assumption at optimistic] |

### ⚠️ Sensitivity Analysis

| Assumption | -50% | -25% | Base | +25% | +50% | NPV Swing |
|-----------|------|------|------|------|------|-----------|
| [key 1] | [NPV] | [NPV] | [NPV] | [NPV] | [NPV] | [max-min] |
| [key 2] | [NPV] | [NPV] | [NPV] | [NPV] | [NPV] | [max-min] |

- **Key financial risk**: [the assumption that, if wrong, changes the answer]

### 🏆 Recommendation
- **Financial verdict**: [invest / don't / conditional on validating X]
- **Confidence**: H/M/L — informed by scenario spread and sensitivity
- **Decision-synthesis criteria** (Contract G):
  - ["NPV > $X over 3 years"] — type: must/want, weight: [N]
  - ["Payback < 18 months"] — type: must/want, weight: [N]
- **Financial scores per option** (if comparing):
  - Option A: NPV = $X, payback = Y months, score = [1-5]
  - Option B: NPV = $X, payback = Y months, score = [1-5]

---

## Common Traps

**False precision**: Reporting NPV to the dollar when inputs are order-of-magnitude. Match output precision to input precision.

**Ignoring opportunity cost**: Comparing investment to zero instead of next-best use of the same resources. The baseline is "do the next-best thing," not "do nothing."

**Hockey stick projections**: Revenue grows exponentially, costs stay flat. Challenge any model where margins improve dramatically without a structural reason.

**Sunk cost inclusion**: Already-spent costs in forward-looking analysis. Only future cash flows matter.

**Single-scenario thinking**: Only the base case. Without upside/downside, stakeholders can't assess risk.

**Trusting LLM arithmetic**: An LLM applying this skill structures the model correctly but may compute NPV/IRR/sensitivity inaccurately. Verify in a spreadsheet. Use this skill for structure, assumptions, and logic — not as a real financial model replacement.

---

## Thinking Triggers

- *"What are the unit economics at the atomic level?"*
- *"Which single assumption, if wrong by 2x, flips this decision?"*
- *"What's the opportunity cost — what else could these resources do?"*
- *"Does the upside-downside spread change my confidence?"*
- *"Am I modeling what I hope, or what's most likely?"*
