---
name: execution-planning
description: "Apply execution-planning whenever the user has made a decision and needs to turn it into action — decomposing work, sequencing tasks, estimating timelines, and assigning ownership. Triggers on phrases like \"how do we execute this?\", \"break this into tasks\", \"what's the project plan?\", \"create a roadmap\", \"what are the dependencies?\", \"who does what by when?\", \"how long will this take to build?\". Use proactively after decision-synthesis or architecture-evaluation produces a committed decision that requires coordinated implementation."
---

# Execution Planning

**Core principle**: A decision without a plan is a wish. Execution planning bridges the gap between "we've decided" and "it's done" by decomposing work into tasks with dependencies, owners, timelines, and risk buffers. The plan's job is not to predict the future perfectly — it's to make the critical path visible and the risks explicit.

---

## When to Use This Skill

- A decision has been made (via decision-synthesis, architecture-evaluation, or direct commitment) and needs to be implemented
- Work involves multiple people, teams, or phases that must be coordinated
- Someone asks "how long will this take?" and the honest answer requires decomposition
- A project is underway but has no visible critical path or dependency map
- An architecture decision (via Contract E from architecture-evaluation) needs to be turned into a build plan

---

## Core Methodology

### Step 1: Frame the Execution Context

Before decomposing work, establish what you're working with:

- **Decision being executed**: State the committed decision. If it came from decision-synthesis, reference the recommendation. If from architecture-evaluation (Contract E), capture the ADR decision, constraints, lock-in risks, migration requirements, and sequencing hints.
- **Constraints**: Non-negotiable boundaries — budget, team size, compliance requirements, hard deadlines, technology lock-ins.
- **Stakeholder alignment**: Who has bought in? Who hasn't? Residual objections from the argument phase (Contract B) become execution risks.
- **Definition of done**: What observable outcome proves this is complete? Not activity ("we built it") but result ("users can do X, metric Y improved").

### Step 2: Build the Work Breakdown Structure

Decompose the work recursively: **deliverables → work packages → tasks**.

- **Deliverables**: The 3-7 major outputs that, together, constitute "done"
- **Work packages**: Groupings of related tasks that produce a deliverable (assignable to one owner)
- **Tasks**: The smallest unit of work that produces a verifiable output (typically 1-5 days of effort)

Rules for good decomposition:
- Every task has a **verifiable output** — something you can inspect, demo, or test
- No task is larger than one person-week. If it is, decompose further.
- Include tasks people forget: documentation, testing, migration, rollback planning, stakeholder communication
- Include integration tasks explicitly — "build component A" and "build component B" need a "integrate A with B" task

### Step 3: Map Dependencies

For every task, identify:
- **What must finish before this can start?** (predecessor)
- **What can't start until this finishes?** (successor)
- **What can run in parallel?** (no dependency)

Represent dependencies as a directed acyclic graph (DAG). Look for:
- **Sequential chains** that force serialization — can any be parallelized with a different design?
- **Convergence points** where multiple streams must merge — these are high-risk coordination moments
- **External dependencies** — approvals, vendor deliveries, other teams' work — flag these as risks

### Step 4: Identify the Critical Path

The **critical path** is the longest chain of dependent tasks from start to finish. It determines the minimum possible timeline.

- Highlight the critical path explicitly — every task on it is a schedule risk
- Tasks not on the critical path have **float** (slack time). Quantify the float.
- If the critical path is too long, the only options are: parallelize work, reduce scope, add resources to critical-path tasks, or accept the timeline

### Step 5: Estimate Durations

Use **reference-class estimation**: estimate based on how long similar work has taken before, not how long you hope it will take.

For each task, produce three estimates:
- **Optimistic** (O): everything goes right, no surprises (10th percentile)
- **Most likely** (M): realistic with normal friction (50th percentile)
- **Pessimistic** (P): significant obstacles, but not catastrophic (90th percentile)

Calculate the **expected duration**: (O + 4M + P) / 6 (PERT formula). Use the pessimistic estimate for critical-path tasks and external dependencies.

Common estimation failures to guard against:
- **Planning fallacy**: people underestimate by 50-100% on average. Calibrate against actuals from past projects.
- **Anchoring on the optimistic case**: the most likely estimate is not the optimistic estimate
- **Ignoring integration time**: individual tasks are estimated well but the time to make them work together is missed

### Step 6: Assign Ownership

For each work package, assign:
- **Owner**: One person accountable for delivery (not a committee)
- **Contributors**: Who else is needed
- **Decision authority**: Can the owner make scope/approach decisions, or must they escalate?

Use the RACI pattern where coordination is complex:
- **Responsible**: Does the work
- **Accountable**: Owns the outcome (one person only)
- **Consulted**: Provides input before the work
- **Informed**: Notified after completion

### Step 7: Design Milestones and Risk Buffers

Place milestones at points where progress is **objectively observable** — not "50% complete" but "API endpoints deployed and passing integration tests."

Add risk buffers:
- **Task-level buffers**: Add to individual high-uncertainty tasks (use the gap between most-likely and pessimistic estimates)
- **Project buffer**: Add 15-25% of the critical path duration as a project-level buffer at the end. This absorbs the accumulated variance that individual task estimates miss.
- **Feeding buffers**: Where a non-critical-path stream feeds into the critical path, add a buffer at the merge point

### Step 8: Surface Execution Risks and Resource Asks

Identify the top risks to execution and pair each with a mitigation:

- **Dependency risks**: External teams, vendor delays, approval bottlenecks
- **Capability risks**: Skills the team doesn't have, unfamiliar technology
- **Scope risks**: Requirements that are likely to change or expand
- **Integration risks**: Components that must work together but are being built separately

For each risk that requires resources, time, or scope changes beyond what's been approved, produce a resource ask in Contract C format for argument-craft:
- **What's needed**: The specific resource, time extension, or scope change
- **Why**: The execution risk or critical-path constraint that drives the ask
- **Consequence of not getting it**: What fails, degrades, or gets delayed

---

## Output Format

### 🎯 Execution Objective
- **Decision being executed**: [the committed decision — reference source analysis if applicable]
- **Definition of done**: [observable outcome that proves completion]
- **Hard constraints**: [budget, team, deadline, compliance, technology lock-ins]
- **Stakeholder alignment status**: [who's bought in, residual objections]

### 📋 Work Breakdown Structure
| # | Deliverable | Work Package | Task | Output | Owner | Est. Duration |
|---|-------------|-------------|------|--------|-------|---------------|
| 1.1.1 | [Deliverable 1] | [Package 1.1] | [Task description] | [Verifiable output] | [Person] | [O/M/P → Expected] |
| 1.1.2 | | | [Task description] | [Verifiable output] | [Person] | [O/M/P → Expected] |
| 1.2.1 | | [Package 1.2] | [Task description] | [Verifiable output] | [Person] | [O/M/P → Expected] |

### ⚖️ Dependency Map
```
[Task 1.1.1] → [Task 1.1.2] → [Task 2.1.1]  ← CRITICAL PATH
[Task 1.2.1] → [Task 1.2.2] ─────────────→ [Task 2.1.1]
                              (float: X days)
[Task 3.1.1] (parallel, no dependencies)
```

### 📊 Timeline and Milestones
| Milestone | Date | Proof of Completion | On Critical Path? |
|-----------|------|--------------------|--------------------|
| [Milestone 1] | [date] | [observable output] | Yes / No |
| [Milestone 2] | [date] | [observable output] | Yes / No |
| **Project buffer** | [date range] | — | — |

### 👥 Ownership Matrix
| Work Package | Responsible | Accountable | Consulted | Informed |
|-------------|------------|-------------|-----------|----------|
| [Package] | [who] | [who] | [who] | [who] |

### ⚠️ Top Execution Risks
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| [risk] | H / M / L | [what breaks] | [action] | [who] |

### 🔄 Resource Asks (Contract C → argument-craft)
| What's Needed | Why | Consequence of Not Getting It |
|--------------|-----|-------------------------------|
| [resource/time/scope change] | [execution risk or critical path constraint] | [what fails or degrades] |

---

## Thinking Triggers

- *"What's on the critical path that I'm not seeing?"*
- *"Where are the integration points, and who owns the handoff?"*
- *"Am I estimating based on how long this took last time, or how long I wish it would take?"*
- *"What external dependency could blow up this timeline?"*
- *"If I had to cut scope to hit the deadline, which deliverables would I protect?"*

---

## Common Traps

**Activity-based milestones**: "Design phase complete" is not a milestone. "API schema reviewed and approved by consuming teams" is. Milestones must be observable from the outside.

**Estimating without decomposing**: "The project will take 3 months" is a guess. Break it down, estimate the pieces, and let the critical path tell you the timeline.

**Ignoring the planning fallacy**: Every team thinks they're the exception. They're not. Use reference-class data from past projects, not gut feel.

**No project buffer**: Individual task estimates absorb individual variance. Project buffers absorb correlated risk — the things that affect multiple tasks simultaneously (team member leaves, requirements change, integration is harder than expected).

**Single-point estimates**: A task "takes 5 days" hides all uncertainty. Three-point estimates force you to confront what could go wrong.

**Phantom parallelism**: The plan shows tasks running in parallel, but the same three people are assigned to all of them. Resource-constrained scheduling is different from dependency-constrained scheduling.
