---
name: limit-thinking
description: "Apply limit thinking when the user wants to understand what happens when a variable or condition is pushed toward its extreme — zero, infinity, 100%, or any boundary. Triggers on 'what happens if we scale this?', 'where does this break?', 'what's the ceiling?', 'what does this converge to?', or when evaluating a system by exploring its trajectory rather than its current state. Also trigger when a decision is based on a snapshot but hasn't examined what it converges to at scale. Use before any scaling decision, rollout plan, or growth strategy."
---

# Limit Thinking

Don't ask "what is the value at this point?" — ask "what does this converge to as we push the variable toward its extreme?" Most planning failures evaluate a snapshot instead of a trajectory. The mathematical concept of a limit — what a function *approaches* rather than where it *is* — exposes asymptotes, phase transitions, and convergence traps hiding inside seemingly linear plans.

---

## How to Execute This Skill

### STEP 1 — Identify the Variables

For the system or decision being evaluated, identify the key variables that could be pushed toward an extreme.

```
LIMIT ANALYSIS SETUP
System: [what's being evaluated]
Variables to push:
  - Variable 1: [what is it?] → Push toward: [0 / ∞ / 100% / boundary]
  - Variable 2: [what is it?] → Push toward: [0 / ∞ / 100% / boundary]
  - Variable 3: [what is it?] → Push toward: [0 / ∞ / 100% / boundary]

For each: What does intuition say happens? (Naive expectation to test.)
```

Good variables to push:
- **Adoption rate** → 100% ("what if everyone uses this?")
- **Automation level** → total ("what if no human is in the loop?")
- **Scale** → orders of magnitude ("what if we 10x or 100x this?")
- **Time** → long horizon ("what does this look like in 5 years?")
- **Cost** → zero ("what if this becomes free?")
- **Speed** → instant ("what if latency drops to zero?")
- **Volume** → extreme ("what if input grows without bound?")

#### Selecting Variables: The 2-3 Rule

Vague prompts ("scale AI across the org") generate 5+ candidates. Tracing all is exhaustive but overwhelming. Identify candidates, then select 2-3 using:

1. **Highest leverage**: pushing it produces the most consequential or irreversible outcome
2. **Most hidden**: limit behavior would most surprise decision-makers (variables where naive ≈ actual teach nothing)
3. **Most coupled**: limit behavior affects other variables (trace upstream first — its limit may redefine the others)

List all candidates, mark the 2-3 you'll trace, briefly note why others were deprioritized.

---

### STEP 2 — Trace the Convergence

Don't jump to the extreme — *approach incrementally* and watch what happens.

```
CONVERGENCE TRACE: [Variable] → [Extreme]

Current state: [where things are now]
  ↓ Push slightly...
Incremental: [what improves or changes — usually positive]
  ↓ Push further...
Midpoint: [secondary effects — first sign of non-linearity]
  ↓ Push toward extreme...
Near-limit: [what breaks, saturates, or reverses — the real finding]
  ↓ At the limit...
Convergence: [variable] → [extreme] means [outcome] → [what it converges to]

Does outcome converge to what intuition predicted? YES / NO
If NO — what's the actual limit, why is it counterintuitive?
```

**Patterns to watch for:**

| Pattern | What it looks like | Example |
|---|---|---|
| **Asymptotic ceiling** | Returns diminish and flatten. Approach a max but never reach it. | More engineers: productivity asymptotes, then declines (Brooks's Law) |
| **Phase transition** | System changes state entirely at a threshold. No incremental change prepares for the discontinuity. | Water at 100°C: more heat → steam, not "hotter water". Org maturity at L4: tools don't help, structural change needed |
| **Reversal / collapse** | Variable's effect flips sign. What helped starts hurting. | Context in an agent: more helps until it doesn't, then success drops (ETH Zurich finding). Review automation: reduces burden until reviewers disengage |
| **Convergence to zero** | A human quality (attention, responsibility, skill) atrophies as the system takes over. | Pilots and autopilot: more autopilot → less manual skill. Limit of pilot skill as automation → 100% is dangerously low |
| **Divergence** | No stable limit. System oscillates or explodes. | Feedback loops without damping: over-correction → under-correction → chaos |

---

### STEP 3 — Extract the Insight

The value of limit thinking is the delta between naive expectation and actual convergence. State it explicitly:

```
LIMIT INSIGHT

Naive expectation: "If we push [variable] toward [extreme], [outcome] will [improve]."

Actual convergence: As [variable] → [extreme], [outcome] → [surprising result].

The delta: [Why actual differs from expectation. What force, feedback loop, or
            phase transition causes the divergence?]

Implication for the decision: [What should change about plan/strategy/design
                               given the trajectory leads somewhere unexpected?]
```

---

### STEP 4 — Find the Optimal Operating Point

If the convergence trace shows diminishing returns, reversal, or collapse past a point, that inflection is the practical operating target.

```
OPERATING POINT ANALYSIS

Variable: [what we're tuning]
Benefit curve: [how benefit changes as variable increases]
Inflection point: [where marginal benefit starts declining significantly]
Recommended range: [where to operate — range, not precise number]
Signal to watch: [early indicator you've pushed past optimal]
```

---

## Output Format

### Variables and Extremes
Each variable being pushed and toward what extreme.

### Convergence Traces
For each variable, the incremental trace from current state to limit:
- What naive trajectory predicts
- Where secondary effects appear
- What the system actually converges to

### Limit Insights
For each trace where actual ≠ expected:
- The delta between expectation and reality
- The mechanism causing the divergence
- Why this matters for the decision

### Optimal Operating Points
Where to operate if the limit reveals diminishing returns or reversal:
- Recommended range
- Early warning signal

### Implications
What changes about plan/strategy/design given these convergence findings.

---

## Thinking Triggers

- *"If we push this all the way, what does the outcome actually converge to?"*
- *"Linear improvement, or does it hit a ceiling / flip / collapse?"*
- *"We're reasoning about a snapshot — what does the trajectory look like?"*
- *"What human quality atrophies as we automate this further?"*
- *"Phase transition hiding between here and the extreme?"*
- *"Everyone is debating the current state — but where is this heading?"*
- *"What would a mathematician say the limit of this function is?"*

---

## Example Applications

- **"Roll out AI code review to 100% of PRs"** → automation → 100%: reviewer attention → 0, critical thinking atrophies, review becomes a checkbox
- **"Add more context to the AI agent"** → context → ∞: performance improves then degrades, signal-to-noise collapses past optimum
- **"Hire more engineers to go faster"** → team → large: communication overhead grows quadratically, velocity per engineer → 0 (Brooks's Law)
- **"Reduce meeting time to maximize focus"** → meetings → 0: alignment gaps emerge, decisions in silos, rework increases until net productivity worse
- **"Make the product free for adoption"** → price → 0: adoption explodes, perceived value → 0, support costs diverge, unit economics collapse
- **"Keep investing monthly regardless of market"** → time → long: dollar-cost averaging smooths volatility, compounding dominates, limit of disciplined PAC is wealth accumulation

---

## Relationship to Other Skills

- **Second-order thinking**: complementary — second-order asks "and then what?" for one step; limit thinking asks "where does this end up?" across the trajectory. Limit sets the destination, second-order traces the path.
- **First principles**: if limit thinking reveals a ceiling/collapse, first-principles can question whether the variable being pushed is the right one.
- **Scenario planning**: limit thinking identifies extremes that define the scenario space.
- **Theory of constraints**: if a variable hits an asymptotic ceiling, TOC identifies the constraint creating it.
