---
name: experimental-design
description: "Apply experimental-design whenever the user needs to test a hypothesis, validate an assumption, or determine whether something actually works. Triggers on phrases like \"how do we test this?\", \"design an experiment\", \"what would prove this?\", \"set up an A/B test\", \"how do we validate this hypothesis?\", \"what's the right control?\", \"is this result significant?\", \"what sample size do we need?\". Use proactively when decisions rest on untested assumptions — designing the test before collecting data prevents post-hoc rationalization."
---

# Experimental Design

**Core principle**: Define what counts as evidence *before* you collect it. A well-designed experiment eliminates alternative explanations so only one conclusion survives. Pre-registration is the firewall between discovery and self-deception.

---

## When to Use This Skill

- A decision hinges on a factual claim no one has tested
- Someone proposes an A/B test but hasn't defined success criteria
- epistemic-mapping flagged a dangerous assumption needing validation
- A team is about to invest resources based on an unvalidated hypothesis
- Prior experiment results were inconclusive and need a better design

---

## Core Methodology

### Step 1: Convert the Question into a Testable Hypothesis

Take the vague question ("Does feature X improve retention?") and produce a precise, falsifiable hypothesis pair.

- **H₀ (null)**: The default — no effect. "Feature X has no effect on 30-day retention."
- **H₁ (alternative)**: The claim. "Feature X increases 30-day retention by ≥ 2 percentage points."

State the direction. One-tailed when you only care about improvement; two-tailed when you also need to detect harm. Default two-tailed unless strong prior reason to expect one direction.

If a hypothesis isn't falsifiable — if no observable outcome could disprove it — rewrite it.

### Step 2: Identify Variables

- **Independent variable (IV)**: What you manipulate. One per experiment unless factorial design with sufficient power.
- **Dependent variable (DV)**: What you measure. The metric closest to the outcome you care about. Proxies introduce noise.
- **Controlled variables**: Held constant across conditions.
- **Potential confounders**: Could vary between groups and affect DV independently. List them all, then design controls (randomization, stratification, matching, statistical control).

### Step 3: Select the Experimental Design

**Randomized Controlled Trial (RCT / A/B test)** — Gold standard. Random assignment eliminates confounding. Use when you can randomize and have sample size.

**Quasi-experimental** — When randomization is impossible:
- **Difference-in-differences**: Treated vs. untreated, before vs. after. Requires parallel trends.
- **Regression discontinuity**: Exploit a threshold (users above/below a score cutoff). Strong validity near cutoff.
- **Interrupted time series**: Track outcome over time, look for level/slope change at intervention.

**Within- vs. between-subjects** — Within-subjects eliminates individual differences but introduces order effects (counterbalance or use washout periods).

**Factorial** — Multiple IVs to detect interactions. Multiplicatively more sample. Only when interactions are the research question.

State what design you picked and why alternatives were rejected.

### Step 4: Determine Sample Size

Run a power analysis *before* data collection:

- **Minimum detectable effect (MDE)**: Smallest practically meaningful effect — not statistically significant, *practically* significant.
- **Significance level (α)**: False positive rate. Standard 0.05; lower for high-stakes.
- **Power (1-β)**: Probability of detecting a real effect. Standard 0.80; use 0.90 for critical experiments.
- **Baseline rate**: Current DV value (e.g., retention = 40%).
- **Variance estimate**: From historical data or pilot.

If required n exceeds feasible: accept larger MDE, run longer, or redesign for a more sensitive metric. Do not run underpowered and hope.

### Step 5: Pre-Register Success Criteria

Before any data collection, commit in writing to:

- **Primary metric**: The one metric that determines success.
- **Secondary metrics**: Should move if hypothesis is correct (and shouldn't if effect is spurious).
- **Success threshold**: Effect size and significance required.
- **Guardrail metrics**: Must *not* degrade (error rate, latency, revenue).
- **Decision rules**: "If primary improves by ≥ MDE at p < α, ship. If guardrail degrades by > X%, halt."
- **Stopping rules**: Early stop conditions (sequential testing with adjusted thresholds) and extension criteria.

Pre-registration prevents the garden of forking paths — redefining success after seeing results.

### Step 6: Mitigate Threats to Validity

**Internal validity** (did X actually cause Y?):
- Selection bias → randomization or matching
- Attrition → intent-to-treat analysis
- Maturation → control group captures natural change
- History → concurrent control experiences same external events
- Instrumentation → consistent measurement across conditions

**External validity** (does it generalize?):
- Sample representativeness → stratified sampling
- Temporal validity → run through full business cycles
- Setting validity → test in production, not staging

**Construct validity** (are we measuring what we think?):
- Metric validity → does the DV capture the construct?
- Treatment fidelity → did participants actually experience the treatment?

For each threat, state mitigated / partially mitigated / unmitigated and what that means for interpretation.

### Step 7: Specify the Analysis Plan

Define the exact analytical approach before data arrives:

- **Statistical test**: t-test, chi-squared, regression, Bayesian — matched to data type and design.
- **Multiple comparison correction**: Bonferroni, Holm, or FDR if testing multiple hypotheses.
- **Segmentation plan**: Pre-specified subgroups (new vs. returning users). Exploratory segments labeled as such.
- **Sensitivity analysis**: Re-run under different assumptions (excluding outliers, different attribution windows).
- **Effect size reporting**: Practical effect size (Cohen's d, relative lift, absolute difference) alongside p-values. Statistical without practical significance is noise.

### Step 8: Define Timeline and Resources

- **Ramp-up plan**: Traffic allocation schedule (5% → 20% → 50%).
- **Minimum run duration**: From sample size and business cycles.
- **Maximum run duration**: When to call it.
- **Resource requirements**: Engineering, data pipeline, stakeholder reviews.
- **Go/no-go checkpoints**: Dates to review interim data for safety (not for peeking at results).

---

## Output Format

### 🎯 Research Question
- **Plain language**: [What are we trying to find out?]
- **H₀**: [Null — no effect]
- **H₁**: [Alternative — specific, falsifiable, directional]

### 📋 Variables
| Role | Variable | Measurement |
|------|----------|-------------|
| Independent (IV) | [What we manipulate] | [How treatment is defined] |
| Dependent (DV) | [What we measure] | [Metric definition and source] |
| Controlled | [Held constant] | [How controlled] |
| Confounder | [Potential threat] | [Mitigation approach] |

### 🔬 Design
- **Type**: [RCT / quasi-experimental / observational — with variant]
- **Justification**: [Why, and what alternatives were rejected]
- **Assignment**: [Random / stratified / threshold — mechanism]

### 📊 Sample Size
- **MDE**: [Minimum detectable effect]
- **Power**: [Target]
- **α**: [Significance level]
- **Required n**: [Per group and total]
- **Feasibility**: [Can we reach this? If not, what changes?]

### ✅ Pre-Registered Criteria
- **Primary metric**: [name] — success if [condition]
- **Secondary metrics**: [List with expected direction]
- **Guardrail metrics**: [List with degradation thresholds]
- **Decision rule**: [If...then ship / halt / extend]
- **Stopping rule**: [Early stop conditions]

### ⚠️ Threats to Validity

| Threat | Category | Severity | Mitigation | Residual Risk |
|--------|----------|----------|------------|---------------|
| [Threat] | Internal | [H/M/L] | [Approach] | [What remains] |
| [Threat] | External | [H/M/L] | [Approach] | [What remains] |
| [Threat] | Construct | [H/M/L] | [Approach] | [What remains] |

### 📊 Analysis Plan
- **Test**: [Statistical test with justification]
- **Correction**: [Multiple comparison method, if applicable]
- **Segments**: [Pre-specified subgroups]
- **Sensitivity**: [Alternative analyses]

### 📋 Timeline and Resources
- **Duration**: [Min — max]
- **Ramp plan**: [Traffic allocation schedule]
- **Checkpoints**: [Go/no-go review dates]
- **Resources**: [What's needed]

---

## Thinking Triggers

- *"What would we need to observe to abandon this hypothesis?"*
- *"If we saw this result, could we explain it without the hypothesis being true?"*
- *"Are we testing what we think we're testing, or a proxy?"*
- *"What's the smallest effect that would actually change our decision?"*
- *"If we can't randomize, what's the best natural experiment available?"*
- *"What would a skeptic say is wrong with this design?"*

---

## Common Traps

- **Post-hoc hypothesis**: Formulating after seeing data. If you discover something unexpected, label it exploratory and design a new experiment to confirm.
- **Underpowered experiments**: Running too small to detect realistic effects, then concluding "no effect." Absence of evidence is not evidence of absence — especially with n=47.
- **Peeking**: Checking daily and stopping when results look good. Inflates false positives dramatically. Use sequential testing with adjusted thresholds for interim looks.
- **Surrogate metrics**: Measuring clicks when you care about retention. The surrogate must have a validated causal link to what matters.
- **Multiple testing without correction**: Testing 20 metrics and celebrating the one significant at p=0.05 is finding noise.
- **Ignoring practical significance**: A statistically significant 0.01% improvement at p=0.03 isn't worth shipping if engineering cost exceeds value.

---

## Example Applications

| Trigger | Application |
|---------|-------------|
| "Does this new onboarding flow improve activation?" | A/B test, randomized assignment, activation rate as primary DV, power analysis for minimum lift, pre-registered 14-day window |
| "We think the bottleneck is the database" | Observational study: latency with and without DB load, control for concurrent traffic, pre-register the latency threshold that confirms |
| "Should we invest in this training program?" | Difference-in-differences: trained vs. untrained teams' productivity before and after, controlling for team composition and project difficulty |
| epistemic-mapping flagged "We assume users prefer simplicity" | Within-subjects preference test: simple and complex versions (counterbalanced), measure task completion + stated preference, pre-register which signal wins on conflict |
