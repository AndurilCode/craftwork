---
name: knowledge-architect
description: "Apply whenever knowledge is at risk of being lost, needs to be captured, or a team needs to design how knowledge flows and persists. Triggers on 'document this decision', 'we should write this down', 'someone is leaving the team', 'why did we do it this way?', 'we keep re-debating this', 'set up our knowledge system', 'our docs are a mess', 'onboarding is painful', or any situation where implicit knowledge needs to become explicit and discoverable. Also trigger after incidents, migrations, vendor choices, or finished spikes — high-value capture moments."
---

# Knowledge Architect

**Core principle**: Knowledge that isn't discoverable isn't captured — it's just written down. Capture must happen close to the moment (context is fresh) but serve a reader far from the moment (months later, different person). Every design decision resolves that tension.

---

## STEP 1 — Detect the Mode

| Mode | Trigger | Output |
|------|---------|--------|
| **Capture** | User has something specific to capture | Knowledge artifact at the right format and depth |
| **Detect** | Workflow moment puts knowledge at risk | Capture prompt + draft artifact |
| **Design** | User wants to set up/improve knowledge systems | Knowledge architecture: where, how found, who owns |

Default to **Capture** if unclear.

---

## MODE 1: CAPTURE

### STEP C1 — Classify the Knowledge Type

| Type | Core question it answers | Audience | Shelf life |
|------|------------------------|----------|------------|
| **Decision** | "Why did we choose X over Y?" | Future-self, new team members | Long — until superseded |
| **Context** | "What would I wish someone told me?" | New team member | Medium — periodic refresh |
| **Learning** | "What did we learn the hard way?" | Anyone facing same situation | Variable — until system changes |

```
"why did we do it this way?" → Decision
"I wish someone had told me" → Context
"we learned this the hard way" → Learning
Multiple types → match the PRIMARY reader need
```

### STEP C2 — Choose the Capture Depth

| Depth | Time | What you produce | When |
|-------|------|-----------------|------|
| **Seed** | 2 min | 2-5 sentences: what, why, one insight | Default. A seed that exists beats a doc that doesn't. |
| **Grow** | 15 min | Structured artifact with discovery header | Reusable, multi-person, significant consequences |
| **Curate** | 30 min | Polished reference with examples + edge cases | Architectural decisions, critical procedures, cross-team rules |

Always start at Seed. Promote only when someone needs more.

### STEP C3 — Produce the Artifact

#### DECISION — Seed
```
## Decision: [What was decided — verb phrase]
**Date**: [date] | **By**: [who] | **Status**: Active

[What we decided, why, and the "why not" for the most obvious alternative.]
```

#### DECISION — Grow
```
## Decision: [What was decided]
**Date**: [date] | **Deciders**: [who] | **Status**: Active | Superseded by [link]
**Tags**: [discovery tags] | **Review trigger**: [when to revisit]

### Context
[Situation and constraints. Write for someone with ZERO context.]
### Decision
[1-2 sentences.]
### Alternatives Considered
- **[Alt A]**: [Why not] | **[Alt B]**: [Why not] | **Do nothing**: [Why not]
### Consequences
[What becomes easier / harder / risks accepted]
### Related
[Links to decisions, PRs, docs, threads]
```

**Curate adds**: Decision History (supersession chain), Applicability (when it applies/doesn't), Verification (how to check compliance).

#### CONTEXT — Seed
```
## Context: [What this is about]
**Area**: [system/domain/team] | **Owner**: [who knows most]

[The thing a new person needs to know. Prioritize the non-obvious.]
```

#### CONTEXT — Grow
```
## Context: [What this is about]
**Area**: [scope] | **Owner**: [who] | **Last verified**: [date] | **Tags**: [tags]

### The Rule — [one paragraph max]
### Why This Exists — [what goes wrong if ignored; use real examples]
### Common Mistakes — [misconceptions, reasonable-looking shortcuts that break things]
### Exceptions — [when it doesn't apply]
### Who to Ask — [primary + backup]
### Related
```

#### LEARNING — Seed
```
## Learning: [One-sentence summary]
**Date**: [date] | **Source**: [incident / migration / spike]

[What happened, what we discovered, what to do differently. Transferable insight, not narrative.]
```

#### LEARNING — Grow
```
## Learning: [One-sentence summary]
**Date**: [date] | **Source**: [link] | **Applicability**: [systems/situations]
**Tags**: [tags] | **Confidence**: High / Medium / Low

### What Happened — [3-5 sentences, not a full post-mortem]
### What We Learned — [principle, not story: "X causes Y" not "last Tuesday X happened"]
### Recommendation — [specific, actionable: "Do X" not "Be careful with X"]
### Caveats — [when this doesn't apply]
### Evidence — [links to incidents, dashboards, PRs]
```

### STEP C4 — Discovery Header

Every Grow+ artifact gets this frontmatter:

```yaml
type: decision | context | learning
tags: [flat, consistent vocabulary — nouns/domains, not adjectives]
area: [system/domain/team]
owner: [person/team]
created: [date]
last_verified: [date]
review_trigger: [condition or date]
status: active | superseded | archived
related: [links]
```

Tags answer: "what would someone search for when they need this?"

---

## MODE 2: DETECT

### Capture Moments

| Moment | Knowledge at risk | Suggested capture |
|--------|------------------|-------------------|
| PR merged (significant design) | Why approach was chosen | Decision — Seed |
| Incident resolved | Debugging insights, root cause | Learning — Grow |
| Team member leaving | Tribal knowledge, conventions | Context — Grow (multiple) |
| New member joining | Gaps in docs | Context audit (run context-gap-analyzer) |
| Vendor/tool selected | Criteria, trade-offs, rejections | Decision — Grow |
| Migration completed | Gotchas, unexpected behaviors | Learning — Grow |
| Spike finished | Findings, dead ends | Learning — Seed/Grow |
| Repeated Slack question | Undocumented common knowledge | Context — Seed |
| Decision re-debated | Original reasoning lost | Decision — Grow (retroactive) |
| Workaround established | Why it exists, removal trigger | Context — Seed |
| Process changed | Why old failed, how new differs | Decision — Grow |

### Detection Prompt

```
CAPTURE MOMENT DETECTED
I notice [what happened].
Knowledge at risk: [what might be lost]
Suggested: [Type] — [Depth] (~[time])
Want me to draft it from available context?
```

Draft from available signals (PRs, incidents, conversation). User edits rather than writes from scratch.

---

## MODE 3: DESIGN

### STEP D1 — Audit Current State

Assess: where knowledge lives today, what's discoverable, what's broken ("I can never find..."), team size, existing tools. Inventory which capture moments produce artifacts vs. don't. Estimate knowledge debt volume.

### STEP D2 — Design the Architecture

Four components:

**1. Location** — Knowledge lives closest to where it's used.
- Decisions → repo `/docs/decisions/` (travels with code)
- System context → repo (consumed by humans + agents)
- Domain/team context → wiki/Notion (spans repos)
- Learnings → repo for single-system, wiki for cross-system
- Onboarding → curated index that LINKS (not duplicates)

Adapt to team's actual tools. Best location = the one people already go to.

**2. Discovery** — Three channels:
- **Search**: flat tag vocabulary, README indexes, platform search
- **Browse**: directory structure mirrors team/domain boundaries, area indexes
- **Stumble**: link artifacts from PRs/incidents/code comments, "Related" links in every Grow+ artifact

**3. Ownership** — Every artifact has exactly one owner. Ownerless artifacts rot.
- Assign per team/area. Learnings owned by capturer until transferred.
- Departing members: knowledge transfer session + Detect mode run.
- Quarterly orphan audit: flag unowned artifacts for adoption or archival.

**4. Freshness** — Outdated knowledge is worse than none.
- Time-based: context reviewed every 6 months
- Event-based: decisions reviewed when system changes
- Query-based: readers flag inaccuracies
- Every artifact has `last_verified`. >12 months = STALE warning → refresh, archive, or delete.

### STEP D3 — Bootstrap Plan

| Phase | What | Effort |
|-------|------|--------|
| Week 1-2 | Seed top 10 undocumented decisions + 5 common new-hire questions. Set up directories. | ~2 hours |
| Week 3-4 | Add capture to incident definition-of-done + retro agendas. Grow 3-5 highest-value seeds. | ~1 hr/week |
| Month 2-3 | Assign owners. First quarterly health check. Create onboarding index. | ~2 hours |
| Ongoing | Capture at workflow moments (2 min). Grow when reused (15 min). Quarterly health check (30 min). | Maintenance |

---

## Calibration

1. **Existence beats quality.** A rough seed > no record. Seeds are permanent artifacts, not drafts.
2. **Capture now, curate later.** Messy and immediate > polished and never.
3. **Discoverable > comprehensive.** Invest in tags/links/indexes over content completeness.
4. **Don't duplicate code.** Artifacts capture what code CANNOT say: the why, the rejected alternatives, the gotchas.
5. **Design for the question.** Every artifact findable by the question someone would ask.
6. **Ownerless knowledge rots.** Grow+ needs a human who answers "is this still true?"
7. **Measure questions answered, not documents written.** If people still ask Slack, discoverability is failing.
8. **Use the team's tools.** Best knowledge system = the one people already use.
