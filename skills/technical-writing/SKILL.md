---
name: technical-writing
description: "Apply whenever the user needs to write, draft, review, or improve technical documents — RFCs, design docs, ADRs, runbooks, postmortems, one-pagers, announcements, Slack threads, PR descriptions. Triggers on 'write a design doc', 'draft an RFC', 'help me write this up', 'write a runbook', 'review my doc', 'make this clearer', 'write a postmortem', or when technical information must be communicated to a specific audience. Also trigger when the user pastes a draft for feedback or needs to explain technical decisions to non-technical stakeholders."
---

# Technical Writing

Writing isn't about explaining what you think — it's about changing what the reader thinks. Most readers skim. Every document must frontload its point, omit what doesn't serve the reader's decision, and respect attention as the scarcest resource.

The goal: give the reader enough to (a) trust your judgment, (b) make a decision, or (c) take a specific action — nothing more.

---

## The Three Laws

**Law 1 — Lead with the point.** First sentence = conclusion, recommendation, or request. If a reader stops after one sentence, they should still know what you want.

**Law 2 — Write less than you think you should.** Cut context that doesn't change the reader's decision. One sentence > one paragraph when both work.

**Law 3 — Match depth to audience size.** Slack to your team: one sentence. ADR for 3-5 reviewers: deep trade-offs. Company-wide announcement: scannable in 30 seconds.

**Slack/short messages**: Skip all ceremony. Open with the ask, include only context needed for the decision, close with explicit request. Don't run the full Step 1-5 process.

---

## STEP 1 — Classify the Document

**If the user provides a template**: Preserve its structure exactly. Apply the Three Laws within each section. Flag gaps as suggestions, don't insert.

**Otherwise**, classify:

| Type | Purpose | Audience | Length |
|------|---------|----------|--------|
| **RFC / Design Doc** | Propose approach, surface trade-offs, get alignment | 5-20 engineers | 2-8 pages |
| **ADR** | Record decision + rationale for future reference | 3-10 now, unlimited later | 0.5-2 pages |
| **One-Pager** | Pitch project, get buy-in/resources | Leadership + stakeholders | 1 page strict |
| **Runbook** | Enable someone to perform unfamiliar task | On-call engineers | Step-by-step |
| **Postmortem** | Learn from incident, prevent recurrence | Broad engineering org | 1-3 pages |
| **Announcement** | Inform about change, decision, or event | Team → org → company | 3-10 sentences |
| **PR Description** | Give reviewers context for effective review | 1-5 reviewers | 5-20 lines |
| **Slack / Async** | Get a decision or response quickly | 1-20 people | 1-5 sentences |

If it doesn't fit: ask "What decision or action should the reader take?" — the answer determines structure.

## STEP 2 — Audience Brief

Before writing:

```
Who reads this: [specific roles, not "engineers"]
What they already know: [shared context — don't repeat it]
What decision they'll make: [approve? understand? execute?]
What they'll do after: [specific action]
Attention budget: [seconds? minutes? deep read?]
```

If you can't fill this in, the document will fail.

## STEP 3 — Write the Key Sentence

One sentence capturing the entire document. Must: state the conclusion (not the topic), be understandable with zero context, survive being the only thing read.

"We should use Redis for session caching" — not "This document evaluates caching options."

This becomes the opening line / TL;DR / subject prefix. If you can't write it, you haven't thought clearly enough to write the document.

---

## STEP 4 — Draft Using Template

### RFC / Design Doc

```markdown
# [Key Sentence as Title]
**Author(s)**: | **Approvers**: | **Status**: Draft | In Review | Approved | Superseded
**Date**: | **Last updated**:

## TL;DR
[Key Sentence expanded to 2-3 sentences.]

## Background
[Objective facts only — no opinions. Current state, problem, prior art.
Write for someone who has never seen this codebase.]

## Goals and Non-Goals
### Goals
- [Specific, measurable. Tied to OKRs where relevant.]
### Non-Goals
- [Explicitly excluded scope. Prevents scope creep during review.]

## Proposed Design
[High-level overview, then detail. Focus on trade-offs, not implementation steps.
If you're writing steps with no trade-off discussion, you don't need an RFC.]

## Alternatives Considered
**First alternative MUST be "Do Nothing" (status quo).** An RFC that can't explain
why "do nothing" is worse hasn't justified its existence.

Each alternative: what is it, trade-offs, why not selected.

## Cross-Cutting Concerns
[Security, privacy, observability, accessibility, cost. "N/A" shows you considered it.]

## Risks and Mitigations
[What could go wrong? Rollback plan? Be specific.]

## Open Questions
[Questions for reviewers to contribute knowledge, not just opinions.]
```

If there are no real alternatives or trade-offs, write an ADR instead.

### ADR

```markdown
# ADR-[N]: [Decision — verb phrase]
**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-[N]
**Date**: | **Deciders**:

## Context
[Situation, constraints, forces. Write for someone who has never seen this codebase.]

## Decision
[1-2 sentences. "We will use PostgreSQL for user data storage."]

## Consequences
### Positive — [what becomes easier]
### Negative — [what becomes harder — be honest]
### Neutral — [what changes without clear valence]
```

Should take 15-30 minutes. If you're spending hours, you need an RFC or you're over-detailing.

### One-Pager

```markdown
# [Project]: [Key Sentence]
**Author**: | **Date**: | **Ask**: [approval, resources, headcount, time]

## Problem — [2-3 sentences. Quantify impact.]
## Proposal — [3-5 sentences. Highest-level approach.]
## Expected Impact — [Quantified. Tied to metrics the audience cares about.]
## Cost — [Time, people, infrastructure. Be specific.]
## Risks — [Top 2-3, one sentence each with mitigation.]
## Timeline — [Key milestones only. 3-5 lines.]
```

Reader should finish thinking "worth doing" or "not worth doing" — never "I need more information."

### Runbook

```markdown
# Runbook: [Action phrase]
**Last verified**: [date] | **Owner**: [team/person] | **Est. time**: [duration]

## When to Use
[Specific triggers — alert names, dashboard thresholds.]

## Prerequisites
[Access, tools, context needed.]

## Steps
### 1. [Action verb] — [what and why]
`[exact command]`
Expected output: [what to see]
If this fails: [what to do instead]
[Repeat pattern for each step.]

## Verification — [How to confirm it worked.]
## Rollback — [How to undo.]
## Escalation — [Who to contact. Slack, PagerDuty, phone.]
```

"Last verified" is the most important metadata. An untested runbook creates false confidence.

### Postmortem

```markdown
# Postmortem: [What happened — not why]
**Date**: | **Duration**: | **Severity**: | **Author**: | **Reviewers**:

## Summary — [3-5 sentences for someone uninvolved.]
## Timeline — [Time (UTC) | Event]
## Root Cause — [Specific. "Migration added index on 500M rows without CONCURRENTLY" not "configuration error."]
## Impact — [Quantified: users, revenue, SLA, data integrity.]
## What Went Well
## What Went Poorly
## Action Items

| Action | Owner | Priority | Due Date |
|--------|-------|----------|----------|

## Lessons Learned — [1-3 broader lessons.]
```

**Action item rules** (where postmortems succeed or fail):
- **Verifiable**: "Add alert when P99 > 3s for 5min" not "Improve monitoring"
- **Owned**: person (not team) + priority + due date. Missing any = aspirational.
- **No exploratory items**: "Investigate..." is not an action. Commit to findings by a date, or drop it.
- **3-5 items**. More than 7 = not prioritized.

### Announcement

```markdown
**Subject**: [Key Sentence — what changed + what reader should do]

[Key Sentence expanded. 1-2 sentences.]
**What's changing**: [2-3 sentences]
**Why**: [1-2 sentences. Connect to a goal the reader cares about.]
**What you need to do**: [Specific action, or "Nothing — informational"]
**Timeline**: [When this takes effect]
**Questions?**: [Where to ask]
```

If longer than 10 sentences, it should be a linked document, not inline.

### PR Description

```markdown
## What — [1-2 sentences. The change.]
## Why — [1-2 sentences. Link to issue/ticket.]
## How — [Approach. Only what reviewer needs to understand the diff.]
## Testing — [How tested. What to verify.]
## Risks / Rollback — [Only if risky.]
```

### Slack / Async

```
[What you need.]
[1-2 sentences context — only what's needed for the decision.]
[Explicit ask — "Can you approve by EOD?" / "Which option: A or B?"]
```

Never start with context before stating what you need.

---

## STEP 5 — Review Checks

- **First-Sentence Test**: Read only first sentences of each section. Does the doc still make sense?
- **So-What Test**: Every paragraph — "what should the reader do with this?" If nothing, cut it.
- **Stranger Test**: Could someone who just joined understand this?
- **Compression Test**: Can you cut 30%? Almost always yes on first draft.
- **Decision Test**: After reading, does the reader know what to decide or do?

---

## Calibration

1. **Structure ≠ thinking.** A perfect RFC format with no trade-off analysis wastes everyone's time.
2. **Don't write what should be a conversation.** 2-3 people + uncontroversial = Slack or call.
3. **Every doc has a shelf life.** Write for when it'll be read (RFC: during review, ADR: 6 months later, runbook: 3am).
4. **The writing is the thinking.** If you can't write the Key Sentence, you haven't thought clearly enough.
5. **Adapt to the org.** These templates are starting points. The principles apply regardless of format.
