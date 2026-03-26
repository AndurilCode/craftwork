---
name: argument-craft
description: "Apply argument-craft whenever the user needs to communicate a recommendation, persuade stakeholders, or structure a case for a decision. Triggers on phrases like \"help me make the case for\", \"structure this argument\", \"write an executive summary\", \"how do I present this?\", \"convince the team\", \"frame this for leadership\", \"what's the narrative?\", \"how do I pitch this?\". Use proactively when the user has completed analysis via decision-synthesis or scenario-planning but hasn't yet structured the communication."
---

# Argument Craft

**Core principle**: Analysis that cannot be communicated effectively did not happen. Argument craft bridges the gap between having the right answer and getting the right people to act on it. The structure of the argument matters as much as its content — the same evidence, framed differently, produces different outcomes.

---

## When to Use This Skill

- The user has a recommendation or position and needs to present it to stakeholders
- A decision-synthesis output needs to become a memo, presentation, email, or conversation
- The user needs to justify a resource ask, scope change, or strategic pivot
- Someone needs to be convinced and the user is unsure how to frame the argument
- An execution-planning output reveals resource needs that require stakeholder buy-in (Contract C handoff)

---

## Core Methodology

### Step 1: Define the Audience

Before structuring a single argument, map who will receive it.

- **Who are they?** Role, seniority, function (e.g., "VP Engineering", "the board", "cross-functional team leads")
- **What do they care about?** Their success metrics, priorities, and constraints. A CFO cares about ROI and risk; an engineering lead cares about technical debt and team capacity.
- **What is their prior belief?** Do they already lean toward your position, lean against it, or have no opinion? This determines whether you're reinforcing, converting, or educating.
- **What would change their mind?** Data, authority, precedent, narrative, risk framing? Different audiences respond to different evidence types.
- **What is their identity stake?** If your recommendation implies they were wrong about something, expect resistance proportional to how public their prior position was.

When the audience comes from stakeholder-power-mapping, use the stakeholder motivations directly. When it comes from scenario-planning (Contract O), identify which stakeholders care about which scenarios.

### Step 2: Formulate the Core Claim

Compress the entire argument into one sentence. This sentence must be:

- **Specific**: "We should migrate to Kubernetes by Q3" not "We should modernize our infrastructure"
- **Actionable**: It names what someone should do, approve, or fund
- **Falsifiable**: Someone could disagree with it — if they can't, it's not a claim, it's a platitude

If the input comes from decision-synthesis (Contract A), the core claim is the recommended option plus the primary reason. If it comes from scenario-planning (Contract O), the core claim is the robust strategy that works across scenarios.

### Step 3: Build the Argument Structure

Use the **Pyramid Principle** (Minto): lead with the answer, then supporting reasons, then evidence.

```
Core Claim
├── Reason 1 (strongest for this audience)
│   ├── Evidence A
│   └── Evidence B
├── Reason 2
│   ├── Evidence C
│   └── Evidence D
└── Reason 3 (addresses likely objection)
    ├── Evidence E
    └── Evidence F
```

**Structuring rules**:
- **2-4 supporting reasons** — fewer than two looks unsupported; more than four loses focus
- **Order by audience priority**, not by logical sequence. Lead with what matters most to *them*, not what matters most to you.
- **Each reason must independently support the claim** — if removing one collapses the argument, the structure is a chain (fragile), not a pyramid (robust)
- **Evidence types**: data (quantitative), precedent (who else did this), authority (expert endorsement), narrative (concrete example), risk (what happens if we don't)

When building from a decision-synthesis scoring matrix (Contract A), translate the top-weighted criteria into reasons and use the scores as evidence.

### Step 4: Map and Pre-empt Objections

Anticipate the strongest counterarguments and address them *within* the argument, not as an afterthought.

For each likely objection:
- **State it honestly** — steelmanning the objection builds credibility. A strawman version insults the audience.
- **Classify it**: Is it a factual dispute (resolve with data), a values difference (acknowledge the trade-off), or a fear (address with risk mitigation)?
- **Respond**: Concede what's true, then redirect. "Yes, the upfront cost is higher — which is why the 18-month payback period matters."

If the input comes from decision-synthesis, the main trade-off from the recommendation section becomes the primary objection to pre-empt. If from scenario-planning (Contract O), the scenario where the position is weakest becomes the objection.

### Step 5: Select the Framing

The same argument, framed differently, lands differently. Choose deliberately.

| Frame | When to use | Example |
|-------|------------|---------|
| **Gain** | Audience is risk-tolerant, opportunity-seeking | "This unlocks $2M in new revenue" |
| **Loss** | Audience is risk-averse, protective | "Without this, we lose $2M to competitors" |
| **Narrative** | Audience values stories over data | "Here's what happened when Company X faced this" |
| **Data-first** | Audience is analytical, skeptical of rhetoric | "The numbers show a 3:1 return" |
| **Vision** | Audience is strategic, long-horizon | "In three years, this positions us to..." |
| **Problem-urgency** | Audience doesn't yet agree there's a problem | "Every week we delay costs us..." |

Match the frame to the audience's decision-making style identified in Step 1. When in doubt, lead with problem-urgency (establishes need) then pivot to gain (establishes value).

### Step 6: Adapt to the Medium

Structure changes based on how the argument will be delivered.

- **Executive memo** (1-2 pages): Core claim in the first paragraph. Reasons as section headers. Evidence as supporting bullets. Recommendation and ask at the end.
- **Presentation** (slides): One claim per slide. Evidence as visuals, not paragraphs. Build the argument slide-by-slide; each slide answers "so what?"
- **Email** (3-5 paragraphs): Subject line = core claim. First paragraph = context + claim. Middle = strongest reason + evidence. Close = specific ask with deadline.
- **Conversation** (verbal): Lead with context-setting ("I want to discuss X because Y"). State the claim. Pause for reaction. Adapt based on response.
- **Slack message** (< 200 words): Bolded claim first. 2-3 bullet reasons. One-line ask. Link to the full memo for details.

### Step 7: Draft the Opening and Close

The opening earns attention. The close drives action.

**Opening patterns**:
- **Context-claim**: "We've been evaluating X. The recommendation is Y, because Z."
- **Problem-solution**: "We're facing [problem]. The path forward is [solution]."
- **Shared goal**: "We all want [goal]. Here's how to get there."

**Closing patterns**:
- **Specific ask**: "I'm requesting approval for X by [date]."
- **Decision frame**: "The choice is between A and B. I recommend A."
- **Next step**: "If you agree, the next step is [action]."

Never close with a summary. Close with what you need the audience to do.

### Step 8: Prepare the Handoff

If the argument succeeds, it produces a committed decision that feeds downstream work.

Capture for execution-planning (Contract B):
- **The committed decision**: What was agreed, in precise terms
- **Stakeholder alignment**: Who is on board, who has residual objections, who was not in the room
- **Constraints surfaced**: Any new constraints that emerged from the audience's feedback (budget caps, timeline requirements, scope limits)

If the argument surfaces a resource need, prepare the Contract C handoff back to execution-planning: what's needed, why, and what fails without it.

---

## Output Format

### 🎯 Audience Profile

- **Audience**: [who — role and function]
- **They care about**: [their priorities and success metrics]
- **Prior belief**: [supportive / neutral / opposed / uninformed]
- **Persuaded by**: [data / narrative / authority / risk framing]

### 📋 Core Claim

[One sentence: specific, actionable, falsifiable]

### ⚖️ Argument Structure

| # | Reason | Evidence | Evidence type |
|---|--------|----------|---------------|
| 1 | [strongest reason for this audience] | [supporting evidence] | [data / precedent / authority / narrative / risk] |
| 2 | [second reason] | [supporting evidence] | [type] |
| 3 | [reason addressing likely objection] | [supporting evidence] | [type] |

### 🛡️ Objection Map

| Objection | Type | Response |
|-----------|------|----------|
| [steelmanned objection 1] | [factual / values / fear] | [concede + redirect] |
| [steelmanned objection 2] | [type] | [response] |

### 🧠 Framing & Medium

- **Frame**: [gain / loss / narrative / data-first / vision / problem-urgency]
- **Medium**: [memo / presentation / email / conversation / Slack]
- **Rationale**: [why this frame + medium fits this audience]

### 🏆 Draft Opening

[2-3 sentence opening paragraph or slide structure]

### 📋✅ Downstream Handoff (Contract B)

- **Committed decision**: [what was decided]
- **Stakeholder alignment**: [who agreed, who has reservations]
- **Constraints surfaced**: [new constraints from audience feedback]

---

## Thinking Triggers

- *"If I had 30 seconds with this audience, what one sentence would I say?"*
- *"What is the strongest version of the argument against my position?"*
- *"Am I leading with what matters to them, or what matters to me?"*
- *"Does every reason independently support the claim, or does the argument collapse if one falls?"*
- *"What does the audience stand to lose if they accept my recommendation?"*

---

## Common Traps

| Trap | What goes wrong |
|------|----------------|
| **Leading with process** | "We evaluated 5 options and scored them on 8 criteria..." — the audience wants the answer, not the journey |
| **Burying the claim** | Building up to the recommendation instead of stating it first. Executives stop reading before you get there. |
| **Strawmanning objections** | Weak counterarguments undermine credibility. Steelman the strongest objection. |
| **One-size framing** | Using the same frame for every audience. A data frame for a narrative thinker wastes the strongest evidence. |
| **Missing the ask** | Presenting analysis without a clear request. The audience nods and moves on. Always close with what you need. |
| **Chain arguments** | Each point depends on the previous one. If the audience rejects step 2, steps 3-5 collapse. Use a pyramid instead. |
| **Advocacy without analysis** | Using argument-craft to sell a position that hasn't been through decision-synthesis or equivalent analysis. This skill structures communication of a conclusion — it does not validate the conclusion itself. If the underlying analysis is weak, a well-structured argument makes it harder to challenge, which is harmful. |
