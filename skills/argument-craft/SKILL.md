---
name: argument-craft
description: "Apply argument-craft whenever the user needs to communicate a recommendation, persuade stakeholders, or structure a case for a decision. Triggers on phrases like \"help me make the case for\", \"structure this argument\", \"write an executive summary\", \"how do I present this?\", \"convince the team\", \"frame this for leadership\", \"what's the narrative?\", \"how do I pitch this?\". Use proactively when the user has completed analysis via decision-synthesis or scenario-planning but hasn't yet structured the communication."
---

# Argument Craft

Same evidence, framed differently, produces different outcomes. Structure the case so the right people act on it.

---

## When to Use

- User has a recommendation needing stakeholder presentation
- decision-synthesis output must become memo, deck, email, or conversation
- Justifying resource ask, scope change, or strategic pivot
- Someone needs convincing and framing is unclear
- execution-planning surfaces resource needs requiring buy-in (Contract C handoff)

---

## Core Methodology

### Step 1: Define the Audience

- **Who**: role, seniority, function
- **What they care about**: success metrics, priorities, constraints (CFO = ROI/risk; eng lead = tech debt/capacity)
- **Prior belief**: leaning toward, against, or no opinion — determines reinforce/convert/educate
- **What changes their mind**: data, authority, precedent, narrative, risk framing
- **Identity stake**: if recommendation implies they were wrong, expect resistance proportional to public commitment

When audience comes from stakeholder-power-mapping, use those motivations directly. From scenario-planning (Contract O), identify which stakeholders care about which scenarios.

### Step 2: Formulate the Core Claim

One sentence. Must be:
- **Specific**: "Migrate to Kubernetes by Q3" not "modernize infrastructure"
- **Actionable**: names what to do, approve, or fund
- **Falsifiable**: someone could disagree — otherwise it's a platitude

From decision-synthesis (Contract A): recommended option + primary reason. From scenario-planning (Contract O): the robust strategy.

### Step 3: Build the Argument Structure

**Pyramid Principle** (Minto): claim, then reasons, then evidence.

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

**Rules**:
- 2-4 reasons (fewer = unsupported; more = unfocused)
- Order by audience priority, not your logical sequence
- Each reason must independently support the claim — if removing one collapses it, that's a chain (fragile), not a pyramid
- **Evidence types**: data, precedent, authority, narrative, risk

From decision-synthesis scoring matrix: top criteria → reasons; scores → evidence.

### Step 4: Map and Pre-empt Objections

Address counterarguments *within* the argument, not after.

For each objection:
- **Steelman it** — strawmen insult the audience
- **Classify**: factual (resolve with data), values (acknowledge trade-off), or fear (mitigate risk)
- **Respond**: concede + redirect. "Yes, upfront cost is higher — which is why the 18-month payback matters."

From decision-synthesis: main trade-off becomes primary objection. From scenario-planning (Contract O): weakest scenario becomes the objection.

### Step 5: Select the Framing

| Frame | When to use | Example |
|-------|------------|---------|
| **Gain** | Risk-tolerant, opportunity-seeking | "Unlocks $2M in new revenue" |
| **Loss** | Risk-averse, protective | "Without this, we lose $2M to competitors" |
| **Narrative** | Values stories over data | "When Company X faced this..." |
| **Data-first** | Analytical, skeptical of rhetoric | "Numbers show 3:1 return" |
| **Vision** | Strategic, long-horizon | "In three years, this positions us to..." |
| **Problem-urgency** | Doesn't yet agree there's a problem | "Every week we delay costs us..." |

When in doubt: problem-urgency (establish need) → gain (establish value).

### Step 6: Adapt to the Medium

- **Memo (1-2 pages)**: claim in first paragraph; reasons as headers; evidence as bullets; ask at end
- **Presentation**: one claim per slide; visuals not paragraphs; each slide answers "so what?"
- **Email (3-5 paragraphs)**: subject = claim; opener = context + claim; middle = strongest reason + evidence; close = ask + deadline
- **Conversation**: context-set ("I want to discuss X because Y"), state claim, pause, adapt
- **Slack (<200 words)**: bolded claim, 2-3 bullet reasons, one-line ask, link to memo

### Step 7: Draft Opening and Close

Opening earns attention. Close drives action.

**Openings**:
- Context-claim: "We've been evaluating X. The recommendation is Y, because Z."
- Problem-solution: "We're facing [problem]. The path forward is [solution]."
- Shared goal: "We all want [goal]. Here's how to get there."

**Closings**:
- Specific ask: "I'm requesting approval for X by [date]."
- Decision frame: "The choice is between A and B. I recommend A."
- Next step: "If you agree, the next step is [action]."

Never close with a summary. Close with what you need them to do.

### Step 8: Prepare the Handoff

Capture for execution-planning (Contract B):
- **Committed decision**: what was agreed, precisely
- **Stakeholder alignment**: who's on board, who has reservations, who wasn't there
- **Constraints surfaced**: new constraints from feedback (budget, timeline, scope)

If argument surfaces resource need: prepare Contract C handoff back to execution-planning — what's needed, why, what fails without it.

---

## Output Format

### 🎯 Audience Profile

- **Audience**: [who — role and function]
- **They care about**: [priorities and metrics]
- **Prior belief**: [supportive / neutral / opposed / uninformed]
- **Persuaded by**: [data / narrative / authority / risk framing]

### 📋 Core Claim

[One sentence: specific, actionable, falsifiable]

### ⚖️ Argument Structure

| # | Reason | Evidence | Evidence type |
|---|--------|----------|---------------|
| 1 | [strongest reason for this audience] | [evidence] | [data / precedent / authority / narrative / risk] |
| 2 | [second reason] | [evidence] | [type] |
| 3 | [reason addressing likely objection] | [evidence] | [type] |

### 🛡️ Objection Map

| Objection | Type | Response |
|-----------|------|----------|
| [steelmanned objection 1] | [factual / values / fear] | [concede + redirect] |
| [steelmanned objection 2] | [type] | [response] |

### 🧠 Framing & Medium

- **Frame**: [gain / loss / narrative / data-first / vision / problem-urgency]
- **Medium**: [memo / presentation / email / conversation / Slack]
- **Rationale**: [why this fits the audience]

### 🏆 Draft Opening

[2-3 sentence opening paragraph or slide structure]

### 📋✅ Downstream Handoff (Contract B)

- **Committed decision**: [what was decided]
- **Stakeholder alignment**: [who agreed, who has reservations]
- **Constraints surfaced**: [new constraints]

---

## Thinking Triggers

- *"If I had 30 seconds, what one sentence would I say?"*
- *"What's the strongest version of the argument against me?"*
- *"Am I leading with what matters to them, or to me?"*
- *"Does every reason independently support the claim?"*
- *"What does the audience stand to lose if they accept this?"*

---

## Common Traps

| Trap | What goes wrong |
|------|----------------|
| **Leading with process** | "We evaluated 5 options on 8 criteria..." — they want the answer, not the journey |
| **Burying the claim** | Building up instead of stating first. Executives stop reading. |
| **Strawmanning objections** | Weak counterarguments destroy credibility. Steelman the strongest. |
| **One-size framing** | Same frame for every audience wastes the strongest evidence. |
| **Missing the ask** | Analysis without request. Audience nods and moves on. Always close with what you need. |
| **Chain arguments** | Each point depends on the previous. Reject step 2, steps 3-5 collapse. Use a pyramid. |
| **Advocacy without analysis** | Structuring weak conclusions makes them harder to challenge — harmful. This skill structures communication of a sound conclusion; it does not validate it. |
