---
name: architecture-evaluation
description: "Apply architecture evaluation whenever the user faces a system design decision — choosing between architectures, evaluating trade-offs, or documenting a technical direction. Triggers on phrases like \"evaluate this architecture\", \"should we use microservices?\", \"what are the trade-offs?\", \"is this design scalable?\", \"architecture decision\", \"ADR\", \"system design review\", \"which database should we use?\". Use proactively when the user is about to commit to a technical direction without explicit trade-off analysis."
---

# Architecture Evaluation

**Core principle**: Every architecture decision trades quality attributes — optimizing one degrades another. Make trade-offs explicit, document in an ADR, and assess reversibility. The best architecture is the one whose trade-offs the team can live with.

---

## When to Use This Skill

- Choosing between system architectures or technology stacks
- Design review needs structured evaluation, not opinion
- About to commit (database, messaging pattern, deployment model) without documenting trade-offs
- An ADR needs to be produced
- "Should we use X?" where X is an architecture pattern or technology
- A `systems-thinking` analysis surfaced structural concerns needing architecture-level resolution

---

## Core Methodology

### Step 1: Establish Decision Context

- **Decision scope**: Specific choice on the table (e.g., "monolith vs. microservices for the order system" — not "system design" generally)
- **Decision driver**: Why now? (new requirement, scaling problem, tech debt, team growth)
- **Constraints**: Non-negotiables — budget, team size and skills, compliance, existing infra to preserve, timeline
- **Stakeholders**: engineering, ops, product, security, finance

### Step 2: Assess Quality Attributes

For each relevant attribute, assess current state and how each option affects it.

Key attributes (evaluate only those relevant):
- **Scalability**: 10x load? Scaling unit?
- **Reliability**: Failure mode? Blast radius?
- **Performance**: Latency, throughput, resource efficiency under expected and peak load
- **Security**: Attack surface, data protection, auth boundaries
- **Maintainability**: Change effort? How many teams must coordinate for a typical change?
- **Operability**: Deployment complexity, observability, incident response, on-call burden
- **Cost**: Infra, development, operational over the time horizon

Rate each option per attribute: Strong / Adequate / Weak — with one-sentence justification.

### Step 3: Map Trade-Offs

Architecture trade-offs are rarely "good vs. bad" — they are "more X = less Y."

Common pairs:
- Consistency vs. availability (CAP)
- Simplicity vs. flexibility
- Performance vs. maintainability
- Development speed vs. operational complexity
- Cost vs. reliability

For each, state which way each option leans and why. This is the core of the evaluation.

### Step 4: Evaluate Architecture Options

For each candidate:
- **Fit to constraints**: Satisfies all non-negotiables from Step 1?
- **Quality attribute profile**: Strong/weak where (from Step 2)?
- **Adoption preconditions**: What must be true to succeed? (microservices need CI/CD maturity, observability, team autonomy)
- **Migration path**: Incremental or big-bang cutover?

Eliminate options that violate constraints. Compare remaining via attribute profiles and trade-off positions.

### Step 5: Assess Evolutionary Characteristics

How does this decision age?

- **Reversibility**: Hard to change in 1 year? 3 years? Switching cost?
- **Lock-in vectors**: Vendor, data model, API contract, team knowledge
- **Migration cost if wrong**: Time and money to unwind
- **Optionality**: Does this open or close future moves? Prefer optionality-preserving when uncertain

### Step 6: Write the Architecture Decision Record

Produce an ADR — also serves as handoff to `execution-planning` via Contract E.

Standard format:
- **Title**: Short, descriptive
- **Status**: Proposed / Accepted / Deprecated / Superseded
- **Context**: Situation, constraints, forces (Steps 1-3)
- **Decision**: Chosen option + primary reasons
- **Consequences**: Positive, negative, operational, team, known risks
- **Alternatives rejected**: What was considered, why not chosen

---

## Output Format

### 🎯 Decision Context
- **Decision**: [what's being decided]
- **Driver**: [why now]
- **Constraints**: [non-negotiables]

### ⚖️ Quality Attribute Assessment

| Attribute | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Scalability | [Strong/Adequate/Weak — reason] | [rating — reason] | [rating — reason] |
| Reliability | [rating — reason] | [rating — reason] | [rating — reason] |
| Maintainability | [rating — reason] | [rating — reason] | [rating — reason] |
| Operability | [rating — reason] | [rating — reason] | [rating — reason] |
| Cost | [rating — reason] | [rating — reason] | [rating — reason] |

### ⚖️ Trade-Off Map

| Trade-Off | Option A leans toward | Option B leans toward |
|-----------|----------------------|----------------------|
| [Simplicity vs. Flexibility] | [direction + why] | [direction + why] |
| [Cost vs. Reliability] | [direction + why] | [direction + why] |

### 📋 Architecture Decision Record
- **Title**: [ADR-NNN: title]
- **Status**: Proposed / Accepted
- **Context**: [from Steps 1-3]
- **Decision**: [chosen option + reasons]
- **Consequences**:
  - Positive: [what improves]
  - Negative: [what degrades]
  - Operational: [deployment, monitoring, on-call]
- **Alternatives rejected**:
  - [Option]: rejected because [reason]

### 🔄 Evolutionary Assessment
- **Reversibility**: Easy / Moderate / Difficult — [justification]
- **Lock-in risks**: [vendor, data model, API, team knowledge]
- **Migration cost if wrong**: [estimated effort]
- **Optionality**: [future moves enabled or foreclosed]

### 📋 Execution-Planning Handoff (Contract E)
- **Decision**: [from ADR]
- **Constraints**: [non-negotiable attributes, budget, team, compliance]
- **Lock-in risks**: [from evolutionary assessment]
- **Migration requirements**: [if replacing existing]
- **Sequencing hints**: [build-first based on dependencies]
- **Known risks**: [from inversion-premortem stress test, if run]

---

## Common Traps

**Resume-Driven Architecture**: Choosing tech because the team wants to learn it, not because it fits. Microservices, Kubernetes, event sourcing are powerful — and unnecessary for most systems.

**Ignoring adoption preconditions**: Microservices need CI/CD, observability, team autonomy. Event-driven needs idempotency discipline and debugging tooling. Evaluate whether the team can *operate* it, not just build it.

**Optimizing for the wrong attribute**: Designing for millions when you have hundreds. Maintainability and operability usually matter more than scalability.

**Irreversibility blindness**: Treating all decisions as equally weighted. Database choice locks in for years; caching strategy changes in a sprint. Spend evaluation effort proportional to reversibility cost.

**Comparison without constraints**: Evaluating in the abstract instead of against this team, this budget, this timeline. The best architecture in theory is irrelevant if the team can't build or operate it.

---

## Thinking Triggers

- *"What quality attributes are in tension, and which side are we choosing?"*
- *"What must be true about our team and infra for this option to succeed?"*
- *"How hard is it to reverse this in two years?"*
- *"Am I choosing this because it fits the problem, or because it's intellectually interesting?"*
- *"Migration path — incremental or big-bang?"*
