---
name: professional-orchestrator
description: Entry point for professional skills — architecture, communication, process design, ethics, and leadership. Routes to the right skill based on what the user needs. Use this when the user's goal involves a professional discipline but they haven't named a specific skill.
---

# Professional Orchestrator

**Routes — does not reason.** Match user intent to an entry point, then execute that skill's SKILL.md.

---

## Step 1 — Match Intent

If ambiguous, ask one clarifying question.

| User wants to... | Start with | Then |
|---|---|---|
| **Architecture & Engineering** | | |
| Evaluate or choose between architectures | `architecture-evaluation` | → `execution-planning` |
| Debug a software failure systematically | `debugging-methodology` | → `casual-inference` if causal |
| Design or run an experiment | `experimental-design` | → `casual-inference` after results |
| Review code or a PR | `code-review-amplifier` | done |
| Find incremental improvements, tech debt, code hygiene | `kaizen` | → `execution-planning` or `process-design` |
| Understand why code is the way it is, audit undocumented fixes | `kintsugi` | → `knowledge-architect` or `technical-writing` |
| **Planning & Execution** | | |
| Break a decision into an action plan | `execution-planning` | done |
| Design or improve a workflow/process | `process-design` | → `execution-planning` |
| Build a financial model or business case | `financial-modeling` | → `argument-craft` |
| **Writing & Communication** | | |
| Write an RFC, design doc, ADR, runbook, postmortem, one-pager, announcement | `technical-writing` | → `narrative-construction` if storytelling |
| Summarize a document, article, transcript, meeting notes | `summarizer` | → `technical-writing` or `argument-craft` if needed |
| Structure a recommendation or argument | `argument-craft` | → `technical-writing` to write up |
| Tell a compelling story from analysis | `narrative-construction` | → `presentation-craft` if presenting |
| Create, structure, or improve a presentation/talk/pitch | `presentation-craft` | done |
| Prepare for a negotiation | `negotiation-strategy` | → `difficult-conversations` if high stakes |
| Navigate a difficult conversation | `difficult-conversations` | done |
| Design a meeting or workshop | `facilitation-design` | done |
| **People & Organizations** | | |
| Map stakeholder influence and blockers | `stakeholder-power-mapping` | → `negotiation-strategy` or `difficult-conversations` |
| Ramp up on a new domain | `learning-strategy` | → `topic-explainer` for specific concepts |
| Understand or learn a concept, technology, idea | `topic-explainer` | → `technical-writing` to document |
| **Ethics & Fairness** | | |
| Surface moral implications of a decision | `ethical-reasoning` | → `fairness-auditing` if systemic |
| Audit a system for equitable outcomes | `fairness-auditing` | → `argument-craft` to present |
| Determine causation vs correlation | `casual-inference` | done |
| **Knowledge Management** | | |
| Capture a decision, learning, or tribal knowledge | `knowledge-architect` | → `technical-writing` if formal doc needed |
| Set up or improve a team's knowledge system | `knowledge-architect` | done (produces architecture) |
| Someone is leaving / joining | `knowledge-architect` | detect mode for departures, audit for joiners |
| **Meta** | | |
| Scan all skills to find the right one(s) | `skill-router` | → matched skill(s) |

---

## Step 2 — Execute

1. Read `skills/[skill-name]/SKILL.md`
2. Apply that skill's full methodology
3. Check the "Then" column for follow-ups

## Step 3 — Propose Next Steps

Do NOT auto-execute. Propose:

```
Based on [what the skill produced], a natural next step would be:
→ [skill-name]: [1-sentence reason]

Want me to continue, or is this what you needed?
```

Multiple follow-ups → list as options. User chooses.

---

## Canonical Chains

**Architecture decision:**
`architecture-evaluation → argument-craft → execution-planning`
Making and implementing a system design choice.

**Building a business case:**
`financial-modeling → argument-craft → execution-planning`
Numbers → narrative → action.

**Navigating organizational resistance:**
`stakeholder-power-mapping → negotiation-strategy → difficult-conversations`
People blocking progress; understand why and how to move them.

**Process improvement:**
`process-design → execution-planning`
Workflow is slow or broken.

**Documenting a technical decision:**
`architecture-evaluation → technical-writing (ADR or RFC)`
Architecture decision needs write-up.

**Ethics review:**
`ethical-reasoning → fairness-auditing → argument-craft`
Moral and equity analysis, then communication of findings.

---

## Skill Registry

| Skill | Purpose |
|-------|---------|
| `architecture-evaluation` | Evaluate system design decisions, produce ADRs |
| `code-review-amplifier` | Structured pre-scanning for human code reviewers |
| `debugging-methodology` | Systematic debugging: reproduce, observe, hypothesize, isolate |
| `execution-planning` | Decompose decisions into executable plans |
| `experimental-design` | Design rigorous experiments to validate assumptions |
| `process-design` | Design workflows using Lean and value stream analysis |
| `financial-modeling` | Unit economics, cost-benefit, NPV/IRR, scenario modeling |
| `argument-craft` | Structure recommendations into persuasive arguments |
| `narrative-construction` | Turn analysis into compelling stories |
| `negotiation-strategy` | Prepare for negotiations with BATNA, ZOPA, concession planning |
| `difficult-conversations` | Navigate conflict, feedback, emotionally charged discussions |
| `facilitation-design` | Design meetings and workshops that produce decisions |
| `stakeholder-power-mapping` | Map influence networks and design engagement strategies |
| `ethical-reasoning` | Surface moral implications using multiple ethical frameworks |
| `fairness-auditing` | Audit systems for equitable outcomes across groups |
| `learning-strategy` | Build structured plans for closing knowledge gaps |
| `casual-inference` | Distinguish causation from correlation |
| `technical-writing` | Write RFCs, design docs, ADRs, runbooks, postmortems, announcements |
| `topic-explainer` | Explain concepts, technologies, ideas using the best style |
| `summarizer` | Summarize documents, articles, transcripts, multi-source content |
| `presentation-craft` | Presentation scripts: narrative arc, slide visuals, speaker notes |
| `kaizen` | Continuous improvement audit: waste, unevenness, overburden |
| `kintsugi` | Repair visibility audit: undocumented fixes, context gold |
| `skill-router` | Exhaustive skill scan and composition planning |
| `knowledge-architect` | Capture decisions, context, learnings; design team knowledge systems |
