---
name: ethical-reasoning
description: "Apply ethical reasoning whenever the user faces a decision, design, or action with moral implications — especially when someone could be harmed, rights could be violated, or values are in tension. Triggers on phrases like \"is this the right thing to do?\", \"what are the ethical implications?\", \"who could this harm?\", \"should we build this?\", \"is this fair?\", \"what are our obligations?\", \"value trade-off\", \"responsible AI\". Use proactively when reviewing any high-stakes decision, product design affecting vulnerable populations, or action where the beneficiaries and those bearing costs are different groups."
---

# Ethical Reasoning

**Core principle**: Apply three independent moral lenses (consequentialist, deontological, virtue) to surface obligations, harms, rights, and value trade-offs that purely analytical frameworks miss — then synthesize where they agree and where they conflict.

---

## When to Use This Skill

- A decision could cause harm to identifiable people or groups
- Someone asks whether an action is right, fair, or responsible
- Benefits and costs fall on different groups — especially when those bearing costs have less power
- A technology, product, or policy could be misused or have unintended consequences at scale
- Values are in tension and no option is cleanly "good"
- Regulatory, compliance, or reputational risk has an ethical dimension
- An analysis feels complete but hasn't asked "who gets hurt?"

---

## Core Methodology

### Step 1: Frame the Ethical Question

State the decision in neutral terms. Identify:
- **What is being decided**: the specific action, not a vague category
- **Who decides**: the agent with power to act
- **Who is affected**: all parties who bear consequences, especially those with no voice
- **What's at stake**: the specific harms, benefits, rights, and obligations in play

Avoid framings that pre-load the answer. "Should we deploy this AI system?" beats "How can we responsibly deploy this AI system?" — the second assumes deployment.

### Step 2: Apply Consequentialist Analysis

Evaluate the action by its outcomes. For each option:

- **Benefits**: What good outcomes? For whom? How likely? How large?
- **Harms**: What bad outcomes? For whom? How likely? How severe? How reversible?
- **Distribution**: Who captures benefits? Who bears costs? Are costs concentrated on vulnerable groups while benefits are diffuse?
- **Scale**: At 10x or 100x, do small harms become systemic?
- **Uncertainty**: Where are predictions weakest? What's the worst plausible outcome?

Pay attention to *who* is harmed and whether they consented to the risk, not just the aggregate sum.

### Step 3: Apply Deontological Analysis

Evaluate by adherence to duties, rights, and rules:

- **Rights**: Does this respect autonomy, privacy, dignity, informed consent, due process for all affected parties?
- **Duties**: What obligations does the decision-maker have, and to whom? (fiduciary, duty of care, promises, professional)
- **Universalizability**: If everyone in this position did this, would the system still function?
- **Means vs. ends**: Is anyone being treated merely as a means — used, deceived, or coerced?
- **Categorical constraints**: Are there actions wrong regardless of consequences? (torture, deception, violation of consent)

Flag rights violations as potential ethical red lines — eliminated regardless of other merits.

### Step 4: Apply Virtue Ethics Analysis

Evaluate by the character it reflects and the norms it sets:

- **Character test**: Would a person of integrity do this?
- **Precedent**: If this becomes standard practice, what world do we get?
- **Virtues at stake**: Does this reflect or erode honesty, fairness, courage, compassion, prudence, justice?
- **Role-specific obligations**: What does excellence look like in this role? (engineer, leader, fiduciary, public servant)
- **Transparency test**: Would the decision-maker be comfortable if action and reasoning were fully public?

### Step 5: Map Stakeholder Harms

For each affected party:

- **Who**: Be specific (not "users" but "users who rely on accessibility features")
- **What could go wrong**: The specific harm, not a vague category
- **Severity**: Minor inconvenience to existential threat
- **Reversibility**: Can it be undone? At what cost?
- **Voice**: Do they have input? Can they opt out? Do they even know?
- **Power asymmetry**: Is the decision-maker in a position of power over them?

Pay special attention to those who cannot advocate for themselves — future generations, children, marginalized communities, non-human stakeholders.

### Step 6: Assess Power Asymmetries

- Who holds decision-making power, and who is subject to it?
- Does the action exploit an existing imbalance or correct one?
- Are there information asymmetries?
- Could the powerful party's interests be distorting the analysis itself?

Asymmetry doesn't make an action wrong, but raises the burden of justification.

### Step 7: Synthesize and Assess Framework Convergence

- **Convergence**: If all three frameworks point the same direction, confidence is high. State the shared conclusion.
- **Divergence**: Name conflicts explicitly (e.g., good outcomes but rights violated). Don't resolve by ignoring one framework.
- **Weighting judgment**: Which framework's concerns are most salient here? Rights violations under power asymmetry weigh heavily; aggregate consequences matter more when all parties consented.
- **Confidence level**: High (frameworks converge) / Medium (mostly agree, some tension) / Low (genuine moral dilemma).

### Step 8: Formulate Recommendation with Red Lines

- State the recommended action
- Identify red lines — options eliminated on moral grounds regardless of benefits
- Specify safeguards that would make a borderline action acceptable
- Flag where moral imagination is needed — unintended consequences, worst cases, scale effects
- If feeding into decision-synthesis, format ethical criteria and scores per Contract F

---

## Output Format

### 🎯 Ethical Question
- **Action under review**: [specific decision, design, or action]
- **Decision-maker**: [who has the power to act]
- **Affected parties**: [all stakeholders who bear consequences]

### 🧠 Framework Analysis

**Consequentialist**:
- Benefits: [who gains, what, how much]
- Harms: [who is harmed, what, how severe, how reversible]
- Distribution: [who bears costs vs. who captures benefits]
- Scale risk: [what happens at 10x-100x]

**Deontological**:
- Rights at stake: [which rights, for whom]
- Duties: [obligations of the decision-maker]
- Universalizability: [would this work as a universal principle?]
- Red lines: [any categorical violations]

**Virtue**:
- Character reflection: [what does this say about the actor?]
- Precedent set: [what norm does this establish?]
- Transparency test: [would this withstand public scrutiny?]

### 👥 Stakeholder Harm Map

| Stakeholder | Potential Harm | Severity | Reversibility | Voice in Decision | Power Asymmetry |
|-------------|---------------|----------|---------------|-------------------|-----------------|
| [party] | [specific harm] | High/Med/Low | High/Med/Low | Yes/Limited/None | [description] |

### ⚖️ Framework Convergence

| Dimension | Consequentialist | Deontological | Virtue | Agree? |
|-----------|-----------------|---------------|--------|--------|
| [key question] | [verdict] | [verdict] | [verdict] | Yes/No |

- **Convergence areas**: [where all three agree]
- **Divergence areas**: [where they conflict and why]

### 🏆 Ethical Recommendation
- **Recommendation**: [course of action]
- **Ethical confidence**: High / Medium / Low
- **Red lines**: [options eliminated on ethical grounds]
- **Safeguards required**: [conditions that make the action acceptable]
- **Escalation**: Feed ethical criteria and scores to decision-synthesis via Contract F

---

## Common Traps

- **Confident conclusions from thin context** — if the user provided minimal context, state your assumptions and flag that the analysis may shift. A verdict on assumed facts is worse than no verdict.
- **Ethics washing** — performing analysis to justify a decision already made. The analysis must be able to change the outcome.
- **Framework shopping** — picking whichever lens supports the preferred conclusion. Apply all three; report conflicts honestly.
- **Abstraction escape** — reasoning about "users" abstractly to avoid confronting specific harms to specific people. Name parties concretely.
- **Consequentialist capture** — defaulting to "greatest good" because it's quantifiable while dismissing rights and character as soft. All three frameworks carry weight.
- **False symmetry** — treating "both sides" as equally valid when one involves clear harm to vulnerable people. Moral seriousness requires proportion, not balance.

---

## Thinking Triggers

- *"Who bears the cost of this decision, and did they agree to it?"*
- *"If this scales 100x, does the ethical picture change?"*
- *"Would I be comfortable if the people most affected could see my full reasoning?"*
- *"Am I doing this analysis to find the right answer, or to justify the convenient one?"*
- *"What would I want someone to do if I were the vulnerable party here?"*
