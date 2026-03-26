---
name: ethical-reasoning
description: "Apply ethical reasoning whenever the user faces a decision, design, or action with moral implications — especially when someone could be harmed, rights could be violated, or values are in tension. Triggers on phrases like \"is this the right thing to do?\", \"what are the ethical implications?\", \"who could this harm?\", \"should we build this?\", \"is this fair?\", \"what are our obligations?\", \"value trade-off\", \"responsible AI\". Use proactively when reviewing any high-stakes decision, product design affecting vulnerable populations, or action where the beneficiaries and those bearing costs are different groups."
---

# Ethical Reasoning

**Core principle**: Analytical reasoning answers "can we?" and "should we, given the numbers?" but only ethical reasoning answers "should we, given what's right?" Apply three independent moral lenses to surface obligations, harms, rights, and value trade-offs that purely analytical frameworks miss — then synthesize where they agree and where they conflict.

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

State the decision, action, or design under review in neutral terms. Identify:
- **What is being decided or done**: the specific action, not a vague category
- **Who decides**: the agent with power to act
- **Who is affected**: all parties who bear consequences, especially those with no voice in the decision
- **What's at stake**: the specific harms, benefits, rights, and obligations in play

Resist framing the question in a way that pre-loads the answer. "Should we deploy this AI system?" is better than "How can we responsibly deploy this AI system?" — the second assumes deployment is the right choice.

### Step 2: Apply Consequentialist Analysis

Evaluate the action by its outcomes. For each option:

- **Benefits**: What good outcomes result? For whom? How likely? How large?
- **Harms**: What bad outcomes result? For whom? How likely? How severe? How reversible?
- **Distribution**: Who captures the benefits? Who bears the costs? Are costs concentrated on vulnerable groups while benefits are diffuse?
- **Scale**: What happens if this action scales 10x or 100x? Do small harms become systemic?
- **Uncertainty**: Where are outcome predictions most uncertain? What's the worst plausible outcome?

The goal is not a simple utilitarian sum. Pay attention to *who* is harmed and whether they consented to the risk, not just the aggregate.

### Step 3: Apply Deontological Analysis

Evaluate the action by its adherence to duties, rights, and rules:

- **Rights**: Does this action respect the rights of all affected parties? (autonomy, privacy, dignity, informed consent, due process)
- **Duties**: What obligations does the decision-maker have? To whom? (fiduciary duty, duty of care, promises made, professional obligations)
- **Universalizability**: Could this action be adopted as a universal principle? If everyone in this position did this, would the system still function?
- **Means vs. ends**: Does this treat anyone merely as a means to someone else's benefit? Are people being used, deceived, or coerced?
- **Categorical constraints**: Are there actions that are wrong regardless of consequences? (torture, deception, violation of consent)

Flag any rights violations as potential ethical red lines — outcomes that should be eliminated from consideration regardless of their other merits.

### Step 4: Apply Virtue Ethics Analysis

Evaluate the action by the character it reflects and the norms it establishes:

- **Character test**: What kind of person or organization does this action reflect? Would a person of integrity do this?
- **Precedent**: What norm does this set? If this becomes standard practice, what world do we get?
- **Virtues at stake**: Does this action reflect or erode honesty, fairness, courage, compassion, prudence, justice?
- **Role-specific obligations**: What does excellence look like in the decision-maker's specific role? (engineer, leader, fiduciary, public servant)
- **Transparency test**: Would the decision-maker be comfortable if this action and its reasoning were fully public?

### Step 5: Map Stakeholder Harms

For each affected party, systematically assess potential harm:

- **Who**: Identify the stakeholder — be specific (not "users" but "users who rely on accessibility features")
- **What could go wrong**: The specific harm, not a vague risk category
- **Severity**: How bad is the harm if it occurs? (minor inconvenience to existential threat)
- **Reversibility**: Can the harm be undone? At what cost?
- **Voice**: Does this stakeholder have input into the decision? Can they opt out? Do they even know the decision is being made?
- **Power asymmetry**: Is the decision-maker in a position of power over the affected party?

Pay special attention to harms that fall on people who cannot advocate for themselves — future generations, children, marginalized communities, non-human stakeholders.

### Step 6: Assess Power Asymmetries

Examine the power dynamics of the situation:

- Who holds decision-making power and who is subject to it?
- Does the action exploit an existing power imbalance or correct one?
- Are there information asymmetries — does one party know things the other doesn't?
- Could the powerful party's interests be unconsciously distorting the ethical analysis itself?

Power asymmetry does not automatically make an action wrong, but it raises the burden of justification. The greater the asymmetry, the more scrutiny the action deserves.

### Step 7: Synthesize and Assess Framework Convergence

Compare the three ethical frameworks:

- **Where they converge**: If consequentialist, deontological, and virtue analyses all point the same direction, confidence is high. State the shared conclusion.
- **Where they diverge**: If frameworks conflict (e.g., good outcomes but rights violated), name the tension explicitly. Do not resolve it by ignoring one framework.
- **Weighting judgment**: In this specific context, which framework's concerns are most salient? (Rights violations in contexts of power asymmetry weigh heavily; aggregate consequences matter more when all parties consented to the risk.)
- **Ethical confidence level**: High (frameworks converge, clear recommendation), Medium (frameworks mostly agree, some tension), Low (frameworks conflict, genuine moral dilemma).

### Step 8: Formulate Recommendation with Red Lines

Produce a clear ethical assessment:

- State the recommended course of action
- Identify ethical red lines — options or actions that should be eliminated on moral grounds regardless of other benefits
- Specify conditions or safeguards that would make a borderline action acceptable
- Flag where moral imagination is needed — unintended consequences, worst-case scenarios, scale effects
- If feeding into decision-synthesis, format ethical criteria and scores per Contract F

---

## Output Format

### 🎯 Ethical Question
- **Action under review**: [specific decision, design, or action]
- **Decision-maker**: [who has the power to act]
- **Affected parties**: [all stakeholders who bear consequences]

### 🧠 Framework Analysis

**Consequentialist Assessment**:
- Benefits: [who gains, what, how much]
- Harms: [who is harmed, what, how severe, how reversible]
- Distribution: [who bears costs vs. who captures benefits]
- Scale risk: [what happens at 10x-100x]

**Deontological Assessment**:
- Rights at stake: [which rights, for whom]
- Duties: [obligations of the decision-maker]
- Universalizability: [would this work as a universal principle?]
- Red lines: [any categorical violations]

**Virtue Assessment**:
- Character reflection: [what does this action say about the actor?]
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
- **Escalation**: Feed ethical criteria and scores to decision-synthesis via Contract F when integrating with analytical criteria

---

## Common Traps

- **Confident conclusions from thin context** — ethical analysis requires understanding who is affected, how, and why. If the user has provided minimal context, state what assumptions you are making and flag that the analysis may shift substantially with more information. An ethical verdict based on assumed facts is worse than no verdict.
- **Ethics washing** — performing ethical analysis to justify a decision already made. The analysis must be able to change the outcome, or it is theater.
- **Framework shopping** — picking whichever ethical lens supports the preferred conclusion. Apply all three frameworks and report honestly where they conflict.
- **Abstraction escape** — reasoning about "users" or "stakeholders" in the abstract to avoid confronting specific harms to specific people. Name the affected parties concretely.
- **Consequentialist capture** — defaulting to "greatest good for the greatest number" because it is quantifiable, while dismissing rights and character concerns as soft. All three frameworks carry weight.
- **False symmetry** — treating "both sides" as equally valid when one side involves clear harm to vulnerable people. Moral seriousness requires proportion, not balance.

---

## Thinking Triggers

- *"Who bears the cost of this decision, and did they agree to it?"*
- *"If this scales 100x, does the ethical picture change?"*
- *"Would I be comfortable if the people most affected by this could see my full reasoning?"*
- *"Am I doing this analysis to find the right answer, or to justify the convenient one?"*
- *"What would I want someone to do if I were the vulnerable party in this situation?"*
