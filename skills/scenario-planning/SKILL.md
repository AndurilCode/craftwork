---
name: scenario-planning
description: Apply scenario planning whenever the user is making long-term decisions, building roadmaps, evaluating strategies, or operating in an environment with significant uncertainty about how the future will unfold. Triggers on phrases like "what should our roadmap look like?", "how do we plan for the future?", "what if things change?", "we're not sure which direction the market will go", "how do we make this strategy resilient?", "what's our plan B?", "what are the different futures we could face?", or when a plan assumes a single future state. Also trigger when someone is over-committed to one expected outcome and hasn't stress-tested the strategy against alternative futures. Don't plan for one future — plan for multiple.
---

# Scenario Planning

**Core principle**: The future is uncertain. Don't predict which future happens — map plausible futures and test strategies against each. Robust strategies perform reasonably across multiple scenarios. Fragile strategies only work if one specific future occurs.

---

## The Core Process

### Step 1: Define the Decision or Strategy
- Time horizon (6 months / 2 years / 5 years)?
- Decision needed now?
- What does "good" look like across futures?

### Step 2: Identify Key Uncertainties
The 2–3 factors that are both:
- **Highly uncertain** (we genuinely don't know how they'll unfold)
- **Highly impactful** (they'd significantly change the right strategy)

These are the **scenario axes**. Skip certainties and minor factors.

### Step 3: Build the Scenarios
3–4 distinct, internally consistent futures. Each:
- **Plausible**: not science fiction
- **Distinct**: meaningfully different from the others
- **Challenging**: at least one uncomfortable for the current plan

**Two-axis matrix** (two key uncertainties):
```
         High market adoption
              |
Slow tech  ──┼── Fast tech
 change       |     change
              |
         Low market adoption
```
→ 4 quadrant scenarios.

**Three narrative scenarios**:
- **Expected**: the future most are implicitly planning for
- **Optimistic**: uncertainties resolve favorably
- **Pessimistic**: uncertainties resolve adversarially
- **Wild card**: low-probability, high-impact disruption

### Step 4: Stress-Test the Strategy
For each scenario:
- Current strategy: well / adequately / poorly?
- What would need to change to work in this scenario?
- Cost of being wrong about which scenario occurs?

### Step 5: Identify Robust Actions
Actions that perform well across *multiple* scenarios — highest-confidence regardless of future.

Plus **hedging options** — small bets that preserve flexibility, cost little in expected case, pay off in unlikely ones.

---

## Output Format

### Key Uncertainties
| Uncertainty | Why it matters | Range |
|------------|----------------|-------|
| [Factor 1] | [Strategy impact] | [X to Y] |
| [Factor 2] | [Strategy impact] | [A to B] |

### The Scenarios

For each (3–4 total):

**Scenario Name** *(memorable)*
- **Description**: 2–3 sentences
- **Key conditions**: what's true here?
- **Probability estimate**: rough (sum to ~100%)
- **Key signals**: early indicators we're in this scenario

### Strategy Stress Test
| Scenario | Strategy performs | Why | What must change |
|----------|------------------|-----|------------------|
| A | Well | [Reason] | Nothing |
| B | Adequately | [Reason] | [Adjustment] |
| C | Poorly | [Reason] | [Major pivot] |
| D | Catastrophically | [Reason] | [Fundamental rethink] |

### Robust Actions
Cross-scenario actions:
- [Action 1] — works because [cross-scenario reason]
- [Action 2] — works because [cross-scenario reason]

### Scenario-Specific Actions
| Scenario | Trigger signal | Response |
|----------|---------------|----------|
| B | [Leading indicator] | [Action] |
| C | [Leading indicator] | [Action] |

### Fragility Assessment
- Worst-handled scenario for current plan?
- Single assumption the plan most depends on?
- Cheapest hedge against the worst scenario?

---

## Pitfalls

- **Too many scenarios**: 3–4 is ideal.
- **Scenarios too similar**: each must require different strategies.
- **Anchoring on the expected**: give real attention to uncomfortable ones.
- **No early warning signals**: every scenario needs leading indicators.
- **Planning for the scenario, not the strategy**: goal is resilience, not prediction.

---

## Thinking Triggers

- *"What are we implicitly assuming about the future?"*
- *"What's the world where this strategy fails completely — how likely?"*
- *"What would we do differently if we knew we were in Scenario C?"*
- *"What signals tell us which future we're heading into?"*
- *"What's the cheapest move that protects us in bad scenarios without sacrificing good ones?"*

---

## Example Applications

- **Product roadmap**: AI commoditizes the core feature? Regulation shifts? Major platform behavior change?
- **Architecture**: Traffic 10x? Third-party API sunsets? Team doubles?
- **Business strategy**: Funding tightens? Competitor undercuts? Adoption 5x faster?
- **Agent pipeline**: LLM costs drop 90%? Unlimited context? Single agent replaces pipeline?
