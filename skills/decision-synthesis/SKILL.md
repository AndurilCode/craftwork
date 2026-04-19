---
name: decision-synthesis
description: Apply decision synthesis whenever the user has completed analysis — run multiple frameworks, mapped the problem, identified options — and now needs to actually choose. Triggers on phrases like "so what should we do?", "how do we decide between these?", "we have too many options", "everything seems equally valid", "how do we weigh these trade-offs?", "we can't agree on which direction", "given all this, what's the call?", or when a rich diagnostic phase has produced competing insights without a clear winner. Also trigger when a decision involves multiple stakeholders with different priorities, multiple criteria that pull in different directions, or significant irreversibility. This skill bridges analysis to action — don't leave a decision unmade because the map is rich.
---

# Decision Synthesis

**Core principle**: Analysis produces options and criteria. Synthesis produces a decision. Most frameworks diverge — generate possibilities, map complexity. This skill converges: makes a defensible, traceable choice. A good decision process maximizes reasoning quality given available information and is transparent enough to learn from.

---

## When to Use

After other frameworks have done their work — Systems Thinking mapped structure, 5 Whys found root causes, Scenario Planning produced futures, Red Teaming attacked options, Stakeholder Mapping identified alignment needs. Now: a rich picture, multiple options, time to land.

---

## The Core Process

### Step 1: Clarify What's Being Decided
- Exact choice?
- Decision horizon (reversible 3 months? irreversible?)?
- Final authority?
- Cost of delay?

Many processes fail because people are evaluating different questions without realizing it.

### Step 2: Surface All Options
List every viable option, including:
- Status quo (always an option)
- Hybrid approaches
- Sequenced approaches (do A now, revisit B in 6 months)
- Options dismissed early but worth a formal look

### Step 3: Define Criteria
- **Must-haves** (binary — failing = eliminated)
- **Want-to-haves** (graded — options compared)

Good criteria: specific enough to score ("error rate < 1%"), independent (no double-counting), tied to actual goal not proxies.

### Step 4: Weight the Criteria
Distribute 100 points. The allocation is the conversation — exposes hidden disagreements between stakeholders.

### Step 5: Score the Options
Score each option × criterion 1–5 (or 1–10) with explicit reasoning. Scores without reasoning can't be challenged.

### Step 6: Compute and Challenge
Weighted scores = signal, not verdict:
- Top scorer match intuition? If not, why?
- Which criteria drive the result? Right ones?
- Swap top-two weights — does the answer change?
- Comfortable defending this to a critic?

---

## Output Format

### Decision Statement
- **Decision**: [Exact choice]
- **Horizon**: [Reversible / Partially / Irreversible]
- **Decider**: [Authority]
- **Deadline**: [When resolved]

### Options
| # | Option | Brief description |
|---|--------|------------------|
| 1 | [Name] | [One line] |

### Criteria & Weights
| Criterion | Type | Weight | Rationale |
|-----------|------|--------|-----------|
| [C1] | Must-have | — | [Why binary] |
| [C2] | Want-to-have | 35 | [Why this weight] |
| [C3] | Want-to-have | 25 | |
| | | **100** | |

### Scoring Matrix
| Option | C1 | C2 (×35) | C3 (×25) | **Weighted Total** |
|--------|----|----------|----------|--------------------|
| A | Pass | 4 → 140 | 3 → 75 | **X** |
| B | Pass | 2 → 70 | 5 → 125 | **Y** |
| C | Fail | — | — | **Eliminated** |

### Recommendation
- **Recommended**: [Name]
- **Primary reason**: [1–2 criteria driving result]
- **Main trade-off**: [What it sacrifices]
- **Confidence**: [High/Med/Low — based on info quality, not preference strength]

### Sensitivity Check
- If [top criterion] changes weight, does answer change?
- Which assumption, if wrong, most undermines this?
- What new info would re-open the decision?

### Reversibility & Regret
- Can it be undone? At what cost?
- **Regret minimization**: which choice produces least regret if situation shifts?
- Low confidence + irreversible → flag explicitly before committing.

---

## Decision Traps

- **False consensus**: Everyone nods but criteria weights were never explicit — different people solving different things.
- **Analysis paralysis**: More analysis rarely resolves value disagreements. Name the disagreement and call it.
- **Criteria inflation**: More criteria adds noise, not signal. Keep the list short and honest.
- **Anchoring on first option**: Evaluate all options in parallel, not sequentially.
- **Score laundering**: Working backwards from a preferred conclusion. The matrix is a thinking tool, not a legitimacy machine.

---

## Thinking Triggers

- *"If I decided alone, no politics, what would I choose?"*
- *"Are we weighting what matters or what's easy to measure?"*
- *"Is there a hybrid we haven't named?"*
- *"What would a regret minimizer choose? A risk minimizer? A maximizer?"*
- *"Are we delaying because we need information, or because we don't want to own the decision?"*
