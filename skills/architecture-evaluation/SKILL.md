---
name: architecture-evaluation
description: "Apply architecture evaluation whenever the user faces a system design decision — choosing between architectures, evaluating trade-offs, or documenting a technical direction. Triggers on phrases like \"evaluate this architecture\", \"should we use microservices?\", \"what are the trade-offs?\", \"is this design scalable?\", \"architecture decision\", \"ADR\", \"system design review\", \"which database should we use?\". Use proactively when the user is about to commit to a technical direction without explicit trade-off analysis."
---

# Architecture Evaluation

**Core principle**: Every architecture decision is a trade-off between quality attributes — optimizing for one degrades another. Make the trade-offs explicit, document the decision in an ADR, and assess how reversible the choice is. The best architecture is not the most elegant; it is the one whose trade-offs the team can live with.

---

## When to Use This Skill

- The user is choosing between system architectures or technology stacks
- A design review needs structured evaluation rather than opinion
- Someone is about to make a commitment (database, messaging pattern, deployment model) without documenting trade-offs
- An Architecture Decision Record (ADR) needs to be produced
- The user asks "should we use X?" where X is an architecture pattern or technology
- A `systems-thinking` analysis has surfaced structural concerns that need architecture-level resolution

---

## Core Methodology

### Step 1: Establish Decision Context

Define what is being decided, why now, and what constrains the decision.

- **Decision scope**: What specific architecture choice is on the table? (e.g., "monolith vs. microservices for the order system" — not "system design" in general)
- **Decision driver**: Why is this decision being made now? (new requirement, scaling problem, tech debt, team growth)
- **Constraints**: What is non-negotiable? Budget ceiling, team size and skills, compliance requirements, existing infrastructure that must be preserved, timeline
- **Stakeholders**: Who is affected by this decision? (engineering, ops, product, security, finance)

### Step 2: Assess Quality Attributes

For each quality attribute relevant to the system, assess the current state and how each option affects it.

Key quality attributes (evaluate only those relevant — not every system cares about all of these):
- **Scalability**: Can the system handle 10x load? What is the scaling unit?
- **Reliability**: What is the failure mode? What is the blast radius of a component failure?
- **Performance**: Latency, throughput, resource efficiency under expected and peak load
- **Security**: Attack surface, data protection, authentication/authorization boundaries
- **Maintainability**: How easy is it to change? How many teams need to coordinate for a typical change?
- **Operability**: Deployment complexity, observability, incident response, on-call burden
- **Cost**: Infrastructure cost, development cost, operational cost over the time horizon

Rate each option against each relevant attribute. Use a simple scale: Strong / Adequate / Weak — with a one-sentence justification for each rating.

### Step 3: Map Trade-Offs

Identify which quality attributes are in tension for this decision. Architecture trade-offs are rarely "good vs. bad" — they are "more of X means less of Y."

Common trade-off pairs:
- Consistency vs. availability (CAP theorem)
- Simplicity vs. flexibility
- Performance vs. maintainability
- Development speed vs. operational complexity
- Cost vs. reliability

For each trade-off, state which direction each option leans and why. This is the core of architecture evaluation — surfacing the tensions that make the decision hard.

### Step 4: Evaluate Architecture Options

For each candidate architecture, assess:

- **Fit to constraints**: Does it satisfy all non-negotiables from Step 1?
- **Quality attribute profile**: Where is it strong and where is it weak (from Step 2)?
- **Adoption preconditions**: What must be true for this option to succeed? (e.g., microservices require CI/CD maturity, observability tooling, team autonomy)
- **Migration path**: If replacing an existing system, what does the migration look like? Can it be incremental or does it require a big-bang cutover?

Eliminate options that violate constraints. For remaining options, the comparison is between their quality attribute profiles and trade-off positions.

### Step 5: Assess Evolutionary Characteristics

Evaluate how this decision ages over time — what gets locked in and what stays flexible.

- **Reversibility**: How hard is it to change this decision in 1 year? 3 years? What is the cost of switching?
- **Lock-in vectors**: Vendor lock-in, data model lock-in, API contract lock-in, team knowledge lock-in
- **Migration cost**: If the decision proves wrong, what does unwinding it cost in time and money?
- **Optionality**: Does this option open or close future architectural moves? Prefer options that preserve optionality when the decision is uncertain

### Step 6: Write the Architecture Decision Record

Produce a structured ADR that serves as both documentation and handoff to `execution-planning` via Contract E.

The ADR follows a standard format:
- **Title**: Short, descriptive name for the decision
- **Status**: Proposed / Accepted / Deprecated / Superseded
- **Context**: The situation, constraints, and forces driving the decision (from Steps 1-3)
- **Decision**: The chosen option and the primary reasons for choosing it
- **Consequences**: What follows from this decision — both positive and negative. Include operational implications, team implications, and known risks
- **Alternatives rejected**: What was considered and why it was not chosen

---

## Output Format

### 🎯 Decision Context
- **Decision**: [what is being decided]
- **Driver**: [why this decision is being made now]
- **Constraints**: [non-negotiables — budget, team, compliance, timeline, existing systems]

### ⚖️ Quality Attribute Assessment
| Quality Attribute | Option A | Option B | Option C |
|------------------|----------|----------|----------|
| Scalability | [Strong/Adequate/Weak — reason] | [rating — reason] | [rating — reason] |
| Reliability | [rating — reason] | [rating — reason] | [rating — reason] |
| Maintainability | [rating — reason] | [rating — reason] | [rating — reason] |
| Operability | [rating — reason] | [rating — reason] | [rating — reason] |
| Cost | [rating — reason] | [rating — reason] | [rating — reason] |

### ⚖️ Trade-Off Map
| Trade-Off | Option A leans toward | Option B leans toward |
|-----------|----------------------|----------------------|
| [e.g., Simplicity vs. Flexibility] | [direction + why] | [direction + why] |
| [e.g., Cost vs. Reliability] | [direction + why] | [direction + why] |

### 📋 Architecture Decision Record
- **Title**: [ADR-NNN: Decision title]
- **Status**: [Proposed / Accepted]
- **Context**: [situation, forces, constraints — from Steps 1-3]
- **Decision**: [chosen option + primary reasons]
- **Consequences**:
  - Positive: [what improves]
  - Negative: [what degrades or becomes harder]
  - Operational: [deployment, monitoring, on-call implications]
- **Alternatives rejected**:
  - [Option name]: rejected because [reason]

### 🔄 Evolutionary Assessment
- **Reversibility**: [Easy / Moderate / Difficult — with justification]
- **Lock-in risks**: [vendor, data model, API, team knowledge]
- **Migration cost if wrong**: [estimated effort to switch]
- **Optionality**: [what future moves does this enable or foreclose?]

### 📋 Execution-Planning Handoff (Contract E)
- **Decision**: [the architecture decision from the ADR]
- **Constraints**: [non-negotiable quality attributes, budget, team size, compliance]
- **Lock-in risks**: [from evolutionary assessment — what is hard to change later]
- **Migration requirements**: [if replacing existing architecture, what must be migrated]
- **Sequencing hints**: [what should be built first based on dependencies]
- **Known risks**: [from inversion-premortem stress test, if run]

---

## Common Traps

**Resume-Driven Architecture**: Choosing a technology because the team wants to learn it, not because it fits the problem. Microservices, Kubernetes, and event sourcing are powerful — and unnecessary for most systems.

**Ignoring adoption preconditions**: Microservices require CI/CD maturity, observability, and team autonomy. Event-driven architecture requires idempotency discipline and debugging tooling. Evaluate whether the team can operate the architecture, not just build it.

**Optimizing for the wrong attribute**: Designing for millions of users when you have hundreds. Scalability is not the most important quality attribute for most systems — maintainability and operability usually matter more.

**Irreversibility blindness**: Treating all decisions as equally weighted. A database choice locks in for years; a caching strategy can be changed in a sprint. Spend evaluation effort proportional to reversibility cost.

**Comparison without constraints**: Evaluating options in the abstract instead of against the specific constraints of this team, this budget, and this timeline. The best architecture in theory is irrelevant if the team cannot build or operate it.

---

## Thinking Triggers

- *"What quality attributes are in tension here, and which side are we choosing?"*
- *"What must be true about our team and infrastructure for this option to succeed?"*
- *"How hard is it to reverse this decision in two years?"*
- *"Am I choosing this because it fits the problem, or because it is intellectually interesting?"*
- *"What does the migration path look like — incremental or big-bang?"*
