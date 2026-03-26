---
name: evidence-synthesis
description: "Apply evidence-synthesis whenever the user has multiple sources of evidence and needs to reach a conclusion — especially when sources conflict, vary in quality, or come from different methodologies. Triggers on phrases like \"what does the evidence say?\", \"synthesize these findings\", \"are these studies consistent?\", \"literature review\", \"conflicting data\", \"what can we conclude from all this?\", \"meta-analysis\", \"weigh the evidence\". Use proactively after causal-inference or learning-strategy produce findings that need integration with other evidence before a decision."
---

# Evidence Synthesis

**Core principle**: Individual pieces of evidence are unreliable. Synthesis across multiple sources — weighting by quality, identifying convergence and divergence, and resolving conflicts — produces conclusions worth acting on. The quality of a conclusion is bounded by the quality of the weakest evidence it leans on most heavily.

---

## When to Use This Skill

- Multiple sources of evidence exist and need to be integrated into a single conclusion
- causal-inference produced experimental findings that must be weighed against other data
- learning-strategy produced summaries from multiple sources that need synthesis
- Sources disagree and the user needs to understand why and what to believe
- A decision requires a "state of the evidence" assessment before proceeding
- deep-document-processor extracted findings from several documents that need integration

---

## Core Methodology

### Step 1: Frame the Synthesis Question

State the specific question the synthesis must answer. This prevents scope creep and keeps the synthesis decision-relevant.

- **Question**: What specific claim, recommendation, or understanding should emerge?
- **Decision context**: What will be done with the conclusion? (The stakes determine how rigorous the synthesis needs to be.)
- **Scope boundaries**: What counts as relevant evidence? Define inclusion criteria — time period, domain, methodology type, minimum quality threshold.

A synthesis without a clear question becomes a literature dump. Start with what you need to conclude, then gather and assess.

### Step 2: Inventory All Evidence Sources

List every piece of evidence, including its provenance. Accept inputs from multiple upstream skills:

**From causal-inference** (Contract J):
- Source type: primary data (experimental)
- Includes: quality grade, causal claim with confidence, limitations

**From learning-strategy** (Contract L):
- Source type: varies (book, paper, expert opinion, course)
- Includes: per-source quality grade, key findings, remaining gaps

**From deep-document-processor or direct input**:
- Source type: document analysis, dataset, report
- Requires: quality assessment during this step

For each source, record:
- **Source identifier**: Name, author, date
- **Source type**: Primary data (experimental), primary data (observational), systematic review, expert opinion, anecdote, proxy metric, model output
- **Key finding**: The main claim or data point this source contributes
- **Methodology**: How the finding was produced (brief)
- **Relevance**: How directly does this address the synthesis question?

### Step 3: Grade Evidence Quality

Assess each source using the GRADE-adapted framework:

| Grade | Criteria | Typical sources |
|-------|----------|-----------------|
| **High** | Well-designed study/experiment, adequate sample, consistent results, directly relevant | RCTs, large observational studies with controls, systematic reviews |
| **Moderate** | Sound methodology with some limitations, moderate inconsistency, mostly relevant | Smaller studies, quasi-experiments, well-reasoned expert analysis |
| **Low** | Observational data without controls, small samples, significant limitations, indirect relevance | Case studies, uncontrolled observations, analogies from adjacent domains |
| **Very Low** | Expert opinion without data, anecdote, heavily biased source, tangential relevance | Individual opinions, single anecdotes, motivated reasoning, outdated data |

**Factors that upgrade quality**: Large effect size, dose-response relationship, all plausible confounders would reduce the effect (conservative bias).

**Factors that downgrade quality**: Risk of bias, inconsistency across studies, indirectness (different population/setting), imprecision (wide confidence intervals), publication bias.

Grade each source and record the reasoning. A source graded "High" that you can't justify is really "Moderate."

### Step 4: Identify Convergent Findings

Look for claims that multiple independent sources support. Convergence is the strongest signal in synthesis.

- Group sources by the claims they support
- Note when convergence comes from diverse methodologies (experiment + observation + expert opinion agreeing is stronger than three experiments by the same team)
- Assess whether convergent sources are truly independent or share common data, assumptions, or authors
- Weight convergence by source quality — three High-grade sources converging is far more informative than five Very Low-grade sources agreeing

Record: the finding, which sources support it, the combined quality level, and confidence.

### Step 5: Analyze Divergent Findings

When sources disagree, diagnose why before choosing sides:

**Methodology differences**: Different study designs can produce different results legitimately. A survey and an experiment measure different things.

**Context differences**: A finding from enterprise software may not apply to consumer apps. A result from 2019 may not hold in 2026.

**Scope differences**: Sources may be measuring different aspects of the same phenomenon and not actually contradicting each other.

**Genuine disagreement**: After accounting for methodology, context, and scope — the sources still disagree. This is the most informative divergence. It means the question is harder than it looks, or one side has a flaw not yet identified.

For each divergence: state the conflicting claims, diagnose the most likely cause, assess which source to weight more heavily (and why), and flag remaining uncertainty.

### Step 6: Identify Evidence Gaps

What evidence is *missing* that would matter?

- Questions the synthesis needs answered but no source addresses
- Quality gaps — the topic has only Very Low or Low evidence
- Perspective gaps — all sources share the same methodology, geography, or theoretical lens
- Recency gaps — all evidence predates a significant change in context

For each gap: state what evidence would fill it, how important it is, and whether it's feasible to obtain (this can feed back to experimental-design or learning-strategy for another cycle).

### Step 7: Produce the Synthesis Conclusion

Integrate everything into a confidence-weighted conclusion:

- **Primary conclusion**: State the finding in plain language. Lead with what is most supported by the evidence.
- **Confidence level**: High (multiple High-grade sources converge, no significant divergence), Moderate (some convergence with caveats), Low (limited or conflicting evidence), Very Low (mostly opinion or indirect evidence).
- **Key caveats**: Conditions under which the conclusion might not hold.
- **What would change the conclusion**: Pre-commit to the evidence that would cause revision. This is the synthesis equivalent of epistemic-mapping's mind-change conditions.

The conclusion should be decision-ready: a downstream skill like decision-synthesis can take it as an input criterion with the confidence level indicating how much weight to assign.

---

## Output Format

### 🔍 Synthesis Question
- **Question**: [What does the evidence say about X?]
- **Decision context**: [What will be decided based on this synthesis?]
- **Scope**: [Inclusion criteria — time, domain, methodology, quality floor]

### 📋 Evidence Inventory

| # | Source | Type | Key Finding | Quality | Relevance |
|---|--------|------|-------------|---------|-----------|
| 1 | [Source name] | [Experimental / Observational / Review / Expert / Anecdote] | [Main claim] | [High / Moderate / Low / Very Low] | [Direct / Indirect] |
| 2 | [Source name] | [Type] | [Main claim] | [Grade] | [Relevance] |

### ✅ Convergent Findings
- **Finding 1**: [Claim supported by multiple sources]
  - Supported by: [Source #s], combined quality: [grade]
  - Independence: [Are sources truly independent?]
- **Finding 2**: [Next convergent claim]
  - Supported by: [Source #s], combined quality: [grade]

### ⚠️ Divergent Findings
- **Disagreement 1**: [Source A says X, Source B says Y]
  - Likely cause: [Methodology / Context / Scope / Genuine disagreement]
  - Resolution: [Which to weight more, and why]
  - Remaining uncertainty: [What we still can't resolve]

### 🕳️ Evidence Gaps
- [Gap 1]: [What's missing, why it matters, how to fill it]
- [Gap 2]: [What's missing, why it matters, how to fill it]

### 🏆 Synthesis Conclusion
- **Finding**: [Plain-language conclusion]
- **Confidence**: [High / Moderate / Low / Very Low]
- **Key caveats**: [Conditions where this might not hold]
- **Would change conclusion if**: [Pre-committed revision triggers]

---

## Thinking Triggers

- *"Am I weighting this source because it's good, or because it agrees with what I already believe?"*
- *"If I removed the weakest source, would the conclusion change? If so, it's resting on thin evidence."*
- *"Are these sources truly independent, or do they share data, methods, or authors?"*
- *"What evidence, if it existed, would make me conclude the opposite?"*
- *"Am I treating absence of evidence as evidence of absence?"*
- *"Would a critic of this conclusion point to a source I'm underweighting?"*

---

## Common Traps

- **Vote counting**: Concluding "3 studies say yes and 1 says no, so yes." Quality and effect size matter more than count. One rigorous experiment outweighs five poorly designed surveys.
- **Confirmation weighting**: Grading sources that support your prior belief as higher quality than sources that challenge it. Grade quality based on methodology, not agreement with your hypothesis.
- **Narrative smoothing**: Presenting the synthesis as more coherent than the evidence warrants. Real evidence is messy. Acknowledge the mess — don't hide it behind a clean story.
- **Anchoring on the first source**: The first piece of evidence read disproportionately shapes the conclusion. Deliberately read the most challenging counter-evidence early.
- **Ignoring base rates**: A surprising finding from a single source doesn't override strong prior evidence. Update beliefs proportionally to the strength of new evidence.

---

## Example Applications

| Trigger | Application |
|---------|-------------|
| "We ran an A/B test and also have survey data — they disagree" | Inventory both sources, grade quality (experiment likely higher than survey for behavioral claims), diagnose divergence (stated preference vs. revealed preference), synthesize with appropriate weighting |
| learning-strategy produced summaries from 6 papers on microservice migration | Inventory per Contract L format, grade each paper, identify convergent migration strategies, flag gaps (no papers from companies at our scale), produce confidence-weighted recommendation |
| "Three team members have different opinions on root cause" | Treat each as expert opinion (Very Low-Moderate depending on evidence backing each claim), look for convergence, identify what data would resolve the disagreement, recommend the investigation that would upgrade evidence quality |
| causal-inference found "probable" causation + two industry reports available | Integrate experimental evidence (Contract J) with industry reports, assess independence, note if reports are pre- or post-experiment, produce combined confidence level |
