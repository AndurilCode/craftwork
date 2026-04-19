---
name: evidence-synthesis
description: "Apply evidence-synthesis whenever the user has multiple sources of evidence and needs to reach a conclusion — especially when sources conflict, vary in quality, or come from different methodologies. Triggers on phrases like \"what does the evidence say?\", \"synthesize these findings\", \"are these studies consistent?\", \"literature review\", \"conflicting data\", \"what can we conclude from all this?\", \"meta-analysis\", \"weigh the evidence\". Use proactively after causal-inference or learning-strategy produce findings that need integration with other evidence before a decision."
---

# Evidence Synthesis

Individual pieces of evidence are unreliable. Synthesis across sources — weighting by quality, identifying convergence and divergence, resolving conflicts — produces conclusions worth acting on. Conclusion quality is bounded by the quality of the weakest evidence it leans on most heavily.

---

## When to Use

- Multiple sources need integration into a single conclusion
- causal-inference produced experimental findings to weigh against other data
- learning-strategy produced summaries from multiple sources
- Sources disagree and the user needs to know what to believe and why
- A decision requires a "state of the evidence" assessment
- deep-document-processor extracted findings from several documents

---

## Core Methodology

### Step 1: Frame the Synthesis Question

State the specific question to prevent scope creep and keep synthesis decision-relevant.

- **Question**: what specific claim, recommendation, or understanding should emerge?
- **Decision context**: what will be done with the conclusion? (Stakes determine rigor.)
- **Scope boundaries**: inclusion criteria — time period, domain, methodology type, minimum quality threshold

A synthesis without a clear question becomes a literature dump.

### Step 2: Inventory All Evidence Sources

List every piece with provenance. Accept inputs from upstream skills:

- **From causal-inference (Contract J)**: primary experimental data; includes quality grade, causal claim with confidence, limitations
- **From learning-strategy (Contract L)**: varies (book, paper, expert opinion, course); per-source quality grade, key findings, gaps
- **From deep-document-processor or direct input**: document/dataset/report; assess quality during this step

For each source, record:
- **Source identifier**: name, author, date
- **Source type**: primary data (experimental/observational), systematic review, expert opinion, anecdote, proxy metric, model output
- **Key finding**: main claim or data point
- **Methodology**: how the finding was produced (brief)
- **Relevance**: how directly it addresses the synthesis question

### Step 3: Grade Evidence Quality

Use the GRADE-adapted framework:

| Grade | Criteria | Typical sources |
|-------|----------|-----------------|
| **High** | Well-designed study, adequate sample, consistent results, directly relevant | RCTs, large observational studies with controls, systematic reviews |
| **Moderate** | Sound methodology with some limitations, moderate inconsistency, mostly relevant | Smaller studies, quasi-experiments, well-reasoned expert analysis |
| **Low** | Observational without controls, small samples, significant limitations, indirect | Case studies, uncontrolled observations, adjacent-domain analogies |
| **Very Low** | Expert opinion without data, anecdote, biased source, tangential | Individual opinions, single anecdotes, motivated reasoning, outdated |

**Upgrade**: large effect size, dose-response, all plausible confounders would reduce the effect (conservative bias).

**Downgrade**: risk of bias, inconsistency across studies, indirectness (different population/setting), imprecision (wide CIs), publication bias.

A "High" grade you can't justify is really "Moderate."

### Step 4: Identify Convergent Findings

Claims supported by multiple independent sources are the strongest signal.

- Group sources by claims they support
- Convergence from diverse methodologies (experiment + observation + expert agreeing) is stronger than three experiments by the same team
- Check whether convergent sources are truly independent or share data, assumptions, authors
- Weight by source quality — three High-grade converging beats five Very Low agreeing

Record: finding, supporting sources, combined quality, confidence.

### Step 5: Analyze Divergent Findings

Diagnose disagreement before choosing sides:

- **Methodology differences**: different designs legitimately produce different results (survey vs. experiment measure different things)
- **Context differences**: enterprise software finding may not apply to consumer apps; 2019 result may not hold in 2026
- **Scope differences**: sources may measure different aspects of the same phenomenon — not actually contradicting
- **Genuine disagreement**: after accounting for the above, sources still disagree. Most informative — the question is harder than it looks, or one side has an unidentified flaw.

For each divergence: state the conflicting claims, diagnose likely cause, assess which to weight more (and why), flag remaining uncertainty.

### Step 6: Identify Evidence Gaps

What evidence is *missing* that would matter?

- Questions the synthesis needs answered but no source addresses
- Quality gaps — only Very Low or Low evidence on the topic
- Perspective gaps — all sources share methodology, geography, or theoretical lens
- Recency gaps — all evidence predates a significant context change

For each gap: what evidence would fill it, importance, feasibility (feeds back to experimental-design or learning-strategy).

### Step 7: Produce the Synthesis Conclusion

Integrate into a confidence-weighted conclusion:

- **Primary conclusion**: plain language; lead with what's most supported
- **Confidence level**: High (multiple High-grade converge, no significant divergence) / Moderate (some convergence with caveats) / Low (limited or conflicting) / Very Low (mostly opinion or indirect)
- **Key caveats**: conditions where the conclusion might not hold
- **What would change the conclusion**: pre-commit to revision triggers (synthesis equivalent of epistemic-mapping's mind-change conditions)

The conclusion should be decision-ready — downstream skills like decision-synthesis can take it as a criterion with the confidence level indicating weight.

---

## Output Format

### 🔍 Synthesis Question
- **Question**: [What does the evidence say about X?]
- **Decision context**: [What will be decided based on this synthesis?]
- **Scope**: [Inclusion criteria — time, domain, methodology, quality floor]

### 📋 Evidence Inventory

| # | Source | Type | Key Finding | Quality | Relevance |
|---|--------|------|-------------|---------|-----------|
| 1 | [Source] | [Experimental/Observational/Review/Expert/Anecdote] | [Main claim] | [High/Moderate/Low/Very Low] | [Direct/Indirect] |

### ✅ Convergent Findings
- **Finding 1**: [Claim supported by multiple sources]
  - Supported by: [Source #s], combined quality: [grade]
  - Independence: [Are sources truly independent?]

### ⚠️ Divergent Findings
- **Disagreement 1**: [Source A says X, Source B says Y]
  - Likely cause: [Methodology/Context/Scope/Genuine]
  - Resolution: [Which to weight more, why]
  - Remaining uncertainty: [What we still can't resolve]

### 🕳️ Evidence Gaps
- [Gap 1]: [What's missing, why it matters, how to fill it]

### 🏆 Synthesis Conclusion
- **Finding**: [Plain-language conclusion]
- **Confidence**: [High/Moderate/Low/Very Low]
- **Key caveats**: [Conditions where this might not hold]
- **Would change conclusion if**: [Pre-committed revision triggers]

---

## Thinking Triggers

- *"Am I weighting this source because it's good, or because it agrees with what I already believe?"*
- *"If I removed the weakest source, would the conclusion change? If so, it's resting on thin evidence."*
- *"Are these sources truly independent, or do they share data, methods, or authors?"*
- *"What evidence, if it existed, would make me conclude the opposite?"*
- *"Am I treating absence of evidence as evidence of absence?"*
- *"Would a critic point to a source I'm underweighting?"*

---

## Common Traps

- **Vote counting**: "3 say yes, 1 says no, so yes." Quality and effect size matter more than count. One rigorous experiment outweighs five poorly designed surveys.
- **Confirmation weighting**: Grading sources that support your prior as higher quality. Grade by methodology, not by agreement with your hypothesis.
- **Narrative smoothing**: Presenting synthesis as more coherent than evidence warrants. Real evidence is messy — acknowledge it.
- **Anchoring on the first source**: First evidence read disproportionately shapes the conclusion. Read challenging counter-evidence early.
- **Ignoring base rates**: A surprising finding from one source doesn't override strong prior evidence. Update proportionally.

---

## Example Applications

| Trigger | Application |
|---------|-------------|
| "A/B test and survey data disagree" | Inventory both, grade quality (experiment usually higher than survey for behavioral claims), diagnose divergence (stated vs. revealed preference), synthesize with appropriate weighting |
| learning-strategy produced summaries from 6 papers on microservice migration | Inventory per Contract L, grade each, identify convergent strategies, flag gaps (no papers from companies at our scale), produce confidence-weighted recommendation |
| "Three team members have different opinions on root cause" | Treat each as expert opinion (Very Low–Moderate depending on backing), look for convergence, identify what data would resolve, recommend the investigation that would upgrade quality |
| causal-inference found "probable" causation + two industry reports | Integrate experimental evidence (Contract J) with reports, assess independence, note timing relative to experiment, produce combined confidence level |
