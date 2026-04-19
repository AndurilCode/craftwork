---
name: epistemic-mapping
description: Apply epistemic mapping whenever the user is starting an analysis, entering unknown territory, or needs to understand the limits of their own knowledge before acting. Triggers on phrases like "what do we know?", "what are we missing?", "what would change our minds?", "what are our assumptions?", "where are the blind spots?", "we don't know what we don't know", "what should we validate first?", "what's the riskiest assumption?", or at the start of any complex investigation, design, or decision. Also trigger before other analysis frameworks when the knowledge landscape hasn't been mapped — running diagnosis without knowing what you don't know is a common failure mode. Map your knowledge before you reason with it.
---

# Epistemic Mapping

**Core**: Before reasoning about a problem, map the quality and completeness of what you actually know. Unknown unknowns are more dangerous than known unknowns. Confusing belief for knowledge is more dangerous than both.

Distinct from Cognitive Bias Detection (audits *how* you reason) — epistemic mapping audits *what* you know and don't know.

---

## The Knowledge Quadrants

```
                    YOU KNOW IT        YOU DON'T KNOW IT
                 ┌──────────────────┬──────────────────────┐
  IT'S TRUE      │  Known Knowns    │  Unknown Knowns      │
  (reality)      │  (foundation)    │  (blind spots)       │
                 ├──────────────────┼──────────────────────┤
  IT'S NOT TRUE  │  Known Unknowns  │  Unknown Unknowns    │
  (gaps)         │  (open questions)│  (surprises)         │
                 └──────────────────┴──────────────────────┘
```

**Known Knowns** — Facts you hold that are true. Foundation for reasoning. *Risk*: Mistaking belief for fact. Ask: "How do I know this? What's the evidence?"

**Known Unknowns** — Gaps you're aware of. Actionable — go find out.

**Unknown Knowns** — Things true but you don't realize you know, or don't realize they're relevant. Things the team collectively knows but individuals don't. *Risk*: Reinventing the wheel, missing relevant context. *Fix*: Wider consultation, explicit knowledge-sharing.

**Unknown Unknowns** — Most dangerous. Can't enumerate, but reduce by:
- Outside perspectives
- Examining assumptions explicitly
- Prior failures in analogous situations
- "What would surprise me here?"

---

## The DIKW Stack

Knowledge quality isn't binary. Place claims on the stack:

| Level | Description | Example |
|-------|-------------|---------|
| **Wisdom** | Knowing what to do with knowledge | "Given X, prioritize Y" |
| **Knowledge** | Synthesized understanding | "Pipeline degrades under concurrent load" |
| **Information** | Interpreted data | "Latency increases 3× with 5+ parallel agents" |
| **Data** | Raw observations | "Latency: 340, 420, 890, 1200, 980 ms" |
| **Belief** | Held without clear basis | "Bottleneck is probably the DB" |

Most analyses mix levels without labeling. Surface where you're reasoning from data vs. belief.

---

## Pre-Analysis Questions

**1. What do we know with high confidence?** Direct evidence, measurement, reliable sources. "Everyone thinks" is not high confidence.

**2. What do we believe but haven't validated?** Assumptions held as truths. Prior experiences applied to current context. Intuitions.

**3. What are our open questions?** Known unknowns, ranked: which, if answered, would most change our approach?

**4. Where might we have blind spots?** Who's not in the room? Whose perspective are we missing? Analogous situations that surprised others?

**5. What would change our minds?** Pre-commit before analysis. If nothing could change your mind — that's belief, not reasoning.

**6. What's the most dangerous assumption?** The one whose failure most undermines the plan.

---

## Output Format

### 🗺️ Knowledge Map

**Known Knowns** (high-confidence facts)
- [Fact] — Source: [how we know]

**Working Beliefs** (assumed true, not validated)
- [Belief] — Risk if wrong: H/M/L

**Known Unknowns** (open questions, ranked)
1. [Most important gap] — Why it matters

**Suspected Blind Spots**
- Areas where we might not know what we don't know
- Outside perspectives not consulted
- Historical analogues not examined

### ⚠️ Most Dangerous Assumption
- **Assumption**: [Critical belief]
- **If wrong**: [What breaks]
- **How to validate**: [Cheapest/fastest check]
- **Cost of being wrong late**: [If it surfaces after commitment]

### 🔄 Mind-Change Conditions
Pre-committed:
- *"If we observe X, we revise view on Y"*
- *"If [assumption] is false, we [response]"*

### 📋 Investigation Priority
Rank Known Unknowns by Importance × Feasibility:
| Question | Importance | Feasibility | Priority |
|----------|-----------|-------------|---------|
| Q1 | High | High | 1 — answer now |
| Q2 | High | Low | 2 — reduce incrementally |
| Q3 | Low | High | 3 — opportunistic |

---

## Epistemic Hygiene

- **Label claims**: Data, information, knowledge, or belief?
- **Source facts**: "We know X" without source = belief in fact's clothes.
- **Pre-commit to falsifiability**: Can't say what would change your mind → rationalizing, not reasoning.
- **Name the room**: Who's not here? Whose knowledge are we missing?
- **Absence of evidence ≠ evidence of absence**: "Haven't seen it fail" ≠ "won't fail."

---

## Triggers

- *"Are we treating this belief as a fact?"*
- *"Who has relevant knowledge we haven't consulted?"*
- *"What would a skeptic say we're missing?"*
- *"What happened last time someone approached this without knowing X?"*
- *"If this analysis is wrong, what's the most likely reason?"*
- *"What question, if answered, would most change our approach now?"*
