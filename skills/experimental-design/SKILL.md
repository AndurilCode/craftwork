---
name: experimental-design
description: "Apply experimental-design whenever the user needs to test a hypothesis, validate an assumption, or determine whether something actually works. Triggers on phrases like \"how do we test this?\", \"design an experiment\", \"what would prove this?\", \"set up an A/B test\", \"how do we validate this hypothesis?\", \"what's the right control?\", \"is this result significant?\", \"what sample size do we need?\". Use proactively when decisions rest on untested assumptions — designing the test before collecting data prevents post-hoc rationalization."
---

# Experimental Design

**Core principle**: Define what counts as evidence *before* you collect it. A well-designed experiment eliminates alternative explanations so that only one conclusion survives. Pre-registration is not bureaucracy — it is the firewall between discovery and self-deception.

---

## When to Use This Skill

- A decision hinges on a factual claim no one has tested
- Someone proposes an A/B test but hasn't defined success criteria
- epistemic-mapping flagged a dangerous assumption that needs validation
- A team is about to invest resources based on an unvalidated hypothesis
- Results from a prior experiment were inconclusive and need a better design

---

## Core Methodology

### Step 1: Convert the Question into a Testable Hypothesis

Take the vague question ("Does feature X improve retention?") and produce a precise, falsifiable hypothesis pair.

- **H₀ (null hypothesis)**: The default — no effect. "Feature X has no effect on 30-day retention."
- **H₁ (alternative hypothesis)**: The claim to test. "Feature X increases 30-day retention by ≥ 2 percentage points."

State the direction (one-tailed vs. two-tailed). One-tailed when you only care about improvement. Two-tailed when you also need to detect harm. Default to two-tailed unless there is a strong prior reason to expect only one direction.

If a hypothesis isn't falsifiable — if no observable outcome could disprove it — rewrite it until it is.

### Step 2: Identify Variables

Map the experimental structure explicitly:

- **Independent variable (IV)**: What you manipulate. One IV per experiment unless you have a factorial design with sufficient power.
- **Dependent variable (DV)**: What you measure. Choose the metric closest to the actual outcome you care about. Proxy metrics introduce noise.
- **Controlled variables**: Factors held constant across conditions.
- **Potential confounders**: Factors that could vary between groups and affect the DV independently. List them all — then design controls for each.

For each confounder, specify the mitigation: randomization, stratification, matching, or statistical control.

### Step 3: Select the Experimental Design

Choose the design that maximizes internal validity given real-world constraints.

**Randomized Controlled Trial (RCT / A/B test)** — Gold standard. Random assignment eliminates confounding. Use when you can randomize and have sufficient sample size.

**Quasi-experimental designs** — When randomization is impossible:
- **Difference-in-differences**: Compare treated vs. untreated groups before and after intervention. Requires parallel trends assumption.
- **Regression discontinuity**: Exploit a threshold (e.g., users above/below a score cutoff). Strong internal validity near the cutoff.
- **Interrupted time series**: Track the outcome over time and look for a level or slope change at the intervention point.

**Within-subjects vs. between-subjects** — Within-subjects (same users experience both conditions) eliminates individual differences but introduces order effects. Use counterbalancing or washout periods.

**Factorial design** — Test multiple IVs simultaneously to detect interactions. Requires multiplicatively more sample. Only use when interactions are the research question.

Justify the choice: state what design you picked and why alternatives were rejected.

### Step 4: Determine Sample Size

Run a power analysis *before* data collection. Specify:

- **Minimum detectable effect (MDE)**: The smallest effect that would be practically meaningful. Not "statistically significant" — practically significant.
- **Significance level (α)**: Probability of false positive. Standard: 0.05. Adjust downward for high-stakes decisions.
- **Power (1-β)**: Probability of detecting a real effect. Standard: 0.80. Use 0.90 for critical experiments.
- **Baseline rate**: Current value of the DV (e.g., current retention = 40%).
- **Variance estimate**: From historical data or pilot study.

If the required sample size exceeds what's feasible, you have three options: accept a larger MDE, run longer, or redesign for a more sensitive metric. Do not run an underpowered experiment and hope for the best.

### Step 5: Pre-Register Success Criteria

Before any data collection, commit in writing to:

- **Primary metric**: The one metric that determines success or failure.
- **Secondary metrics**: Supporting metrics that should move if the hypothesis is correct (and shouldn't move if the effect is spurious).
- **Success threshold**: The effect size and statistical significance required to declare the experiment a success.
- **Guardrail metrics**: Metrics that must *not* degrade (e.g., error rate, latency, revenue).
- **Decision rules**: "If primary metric improves by ≥ MDE at p < α, ship. If guardrail degrades by > X%, halt regardless."
- **Stopping rules**: When to stop early (sequential testing with adjusted thresholds) or when to extend.

Pre-registration prevents the garden of forking paths — the temptation to redefine success after seeing results.

### Step 6: Mitigate Threats to Validity

Assess each threat category and design mitigations:

**Internal validity** (did X actually cause Y?):
- Selection bias → randomization or matching
- Attrition → intent-to-treat analysis
- Maturation → control group captures natural change
- History → concurrent control group experiences same external events
- Instrumentation → consistent measurement across conditions

**External validity** (does the result generalize?):
- Sample representativeness → stratified sampling
- Temporal validity → run through full business cycles
- Setting validity → test in production, not staging

**Construct validity** (are we measuring what we think?):
- Metric validity → does the DV actually capture the construct?
- Treatment fidelity → did participants actually experience the treatment?

For each identified threat, state whether it is mitigated, partially mitigated, or unmitigated (and what that means for interpretation).

### Step 7: Specify the Analysis Plan

Define the exact analytical approach before data arrives:

- **Statistical test**: t-test, chi-squared, regression, Bayesian analysis — chosen to match the data type and design.
- **Multiple comparison correction**: Bonferroni, Holm, or False Discovery Rate if testing multiple hypotheses.
- **Segmentation plan**: Pre-specified subgroups to analyze (e.g., new vs. returning users). Exploratory segments are labeled as such.
- **Sensitivity analysis**: Re-run under different assumptions (e.g., excluding outliers, different attribution windows).
- **Effect size reporting**: Report practical effect size (Cohen's d, relative lift, absolute difference) alongside p-values. Statistical significance without practical significance is noise.

### Step 8: Define Timeline and Resources

Specify:

- **Ramp-up plan**: Traffic allocation schedule (e.g., 5% → 20% → 50%).
- **Minimum run duration**: Based on sample size requirements and business cycles.
- **Maximum run duration**: When to call it if the effect hasn't materialized.
- **Resource requirements**: Engineering effort, data pipeline needs, stakeholder reviews.
- **Go/no-go checkpoints**: Dates to review interim data for safety (not for peeking at results).

---

## Output Format

### 🎯 Research Question
- **Plain language**: [What are we trying to find out?]
- **H₀**: [Null hypothesis — no effect]
- **H₁**: [Alternative hypothesis — specific, falsifiable, directional]

### 📋 Variables
| Role | Variable | Measurement |
|------|----------|-------------|
| Independent (IV) | [What we manipulate] | [How treatment is defined] |
| Dependent (DV) | [What we measure] | [Metric definition and source] |
| Controlled | [Held constant] | [How controlled] |
| Confounder | [Potential threat] | [Mitigation approach] |

### 🔬 Design
- **Type**: [RCT / quasi-experimental / observational — with specific variant]
- **Justification**: [Why this design, what alternatives were rejected]
- **Assignment**: [Random / stratified / threshold — mechanism described]

### 📊 Sample Size
- **MDE**: [Minimum detectable effect]
- **Power**: [Target power level]
- **α**: [Significance level]
- **Required n**: [Per group and total]
- **Feasibility**: [Can we reach this? If not, what changes?]

### ✅ Pre-Registered Criteria
- **Primary metric**: [Metric name] — success if [condition]
- **Secondary metrics**: [List with expected direction]
- **Guardrail metrics**: [List with degradation thresholds]
- **Decision rule**: [If...then ship / halt / extend]
- **Stopping rule**: [Early stop conditions]

### ⚠️ Threats to Validity

| Threat | Category | Severity | Mitigation | Residual Risk |
|--------|----------|----------|------------|---------------|
| [Threat 1] | Internal | [H/M/L] | [Approach] | [What remains] |
| [Threat 2] | External | [H/M/L] | [Approach] | [What remains] |
| [Threat 3] | Construct | [H/M/L] | [Approach] | [What remains] |

### 📊 Analysis Plan
- **Test**: [Statistical test with justification]
- **Correction**: [Multiple comparison method, if applicable]
- **Segments**: [Pre-specified subgroups]
- **Sensitivity**: [Alternative analyses planned]

### 📋 Timeline and Resources
- **Duration**: [Minimum — maximum]
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

- **Post-hoc hypothesis**: Formulating the hypothesis after seeing the data. The entire point of pre-registration is to prevent this. If you discover something unexpected, label it exploratory and design a new experiment to confirm.
- **Underpowered experiments**: Running a test too small to detect realistic effects, then concluding "no effect." Absence of evidence is not evidence of absence — especially with n=47.
- **Peeking**: Checking results daily and stopping when they look good. This inflates false positive rates dramatically. Use sequential testing with adjusted thresholds if you need interim looks.
- **Surrogate metrics**: Measuring clicks when you care about retention. The surrogate must have a validated causal link to the outcome that matters.
- **Multiple testing without correction**: Testing 20 metrics and celebrating the one that's significant at p=0.05 is finding noise, not signal.
- **Ignoring practical significance**: A statistically significant 0.01% improvement with p=0.03 is not worth shipping if the engineering cost exceeds the value.

---

## Example Applications

| Trigger | Application |
|---------|-------------|
| "Does this new onboarding flow improve activation?" | Design an A/B test with randomized assignment, activation rate as primary DV, power analysis for minimum detectable lift, and pre-registered 14-day measurement window |
| "We think the bottleneck is the database" | Design an observational study: measure latency with and without DB load, control for concurrent traffic, pre-register the latency threshold that confirms the hypothesis |
| "Should we invest in this training program?" | Quasi-experimental design using difference-in-differences: compare trained vs. untrained teams' productivity before and after, controlling for team composition and project difficulty |
| epistemic-mapping flagged "We assume users prefer simplicity" | Design a within-subjects preference test: show both simple and complex versions (counterbalanced), measure task completion + stated preference, pre-register which signal wins on conflict |
