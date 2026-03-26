---
name: process-design
description: "Apply process-design whenever the user needs to create, improve, or streamline a workflow or operational process. Triggers on phrases like \"design a workflow\", \"improve this process\", \"streamline this\", \"too many handoffs\", \"the process is too slow\", \"automate or not?\", \"how should we structure this pipeline?\". Use proactively when a user describes repeated operational friction, bottlenecks, or unclear ownership in how work moves through a system."
---

# Process Design

**Core principle**: A good process makes the right thing easy and the wrong thing visible. Map reality before designing the future — most process problems come from optimizing a process nobody actually follows.

---

## When to Use This Skill

- A workflow exists but is slow, error-prone, or frustrating
- A new capability needs an operational process built from scratch
- Handoffs between teams or systems are causing delays or errors
- Someone asks whether to automate a step or keep it manual
- Work moves through multiple stages and nobody owns the end-to-end flow

---

## Core Methodology

### Step 1: Map the Current State

Document the process as it actually works, not as it's documented. For each step, capture:

- **What happens** (the action)
- **Who does it** (role, not person)
- **What triggers it** (input or event)
- **What it produces** (output)
- **How long it takes** (cycle time) and how long work waits before it starts (wait time)

Talk to the people who do the work, not just the people who designed it. If this is a new process with no current state, skip to Step 3 and use the waste categories as design constraints instead.

### Step 2: Identify Waste

Examine each step through Lean's eight waste categories:

- **Waiting** — work sitting idle between steps (the most common process waste)
- **Handoffs** — each transfer between people or systems risks information loss and adds delay
- **Overprocessing** — steps that add effort but not value (excessive approvals, redundant reviews)
- **Defects** — errors that cause rework downstream
- **Overproduction** — producing more than the next step can consume
- **Motion** — unnecessary context-switching or tool-switching
- **Transport** — moving information between systems unnecessarily
- **Unused talent** — skilled people doing work that doesn't require their expertise

For each step, classify it as: **value-creating** (the customer would pay for it), **necessary non-value** (required but not value-adding, like compliance), or **pure waste** (eliminable).

### Step 3: Design the Future State

Redesign the process applying these principles in order:

1. **Eliminate** — remove pure waste steps entirely
2. **Combine** — merge steps that share the same owner or context to reduce handoffs
3. **Parallelize** — identify steps with no dependency on each other and run them simultaneously
4. **Simplify** — reduce variability in remaining steps with checklists, templates, or defaults
5. **Add feedback loops** — insert quality checks close to where errors originate, not at the end

For each remaining step, decide the automation level:
- **Fully automate** — low variability, clear rules, high volume, low error cost
- **Augment with tools** — moderate variability, benefits from human judgment but can be tool-assisted
- **Keep manual** — high variability, requires expertise or judgment, low volume

### Step 4: Define Ownership and SLAs

Assign clear ownership for each step and for the end-to-end process:

- **Step owner** — accountable for that step's throughput and quality
- **Process owner** — accountable for end-to-end cycle time and outcome
- **SLAs** — target cycle time per step and maximum wait time between steps

Where handoffs remain, define the contract: what format the output takes, what "done" means, and how the downstream step signals problems back upstream.

### Step 5: Plan the Transition

Moving from current state to future state is itself a process. Define:

- **Sequencing** — which changes to make first (prefer changes that reduce the most waste with the least disruption)
- **Parallel run period** — run old and new processes simultaneously until the new one proves reliable
- **Metrics to track** — end-to-end cycle time, defect rate, throughput, and wait time at each handoff
- **Review cadence** — schedule a process review after 2-4 weeks of operation to catch design flaws early

---

## Output Format

### 🎯 Process Objective
- **Process name**: [name]
- **Goal**: [what this process produces and for whom]
- **Current end-to-end cycle time**: [if redesign — measured, not estimated]
- **Target end-to-end cycle time**: [goal]

### 📋 Current State Map
| Step | Action | Owner | Trigger | Output | Cycle Time | Wait Time | Value Class |
|------|--------|-------|---------|--------|------------|-----------|-------------|
| 1 | [action] | [role] | [input/event] | [output] | [time] | [time] | Value / Necessary / Waste |
| 2 | ... | | | | | | |

### 🔍 Waste Analysis
| Waste Type | Where Found | Impact | Recommendation |
|------------|-------------|--------|----------------|
| [e.g., Waiting] | [step or handoff] | [delay/cost/error rate] | [eliminate/reduce/accept] |

### 📊 Future State Map
| Step | Action | Owner | Automation Level | Cycle Time | SLA |
|------|--------|-------|-----------------|------------|-----|
| 1 | [action] | [role] | Full / Augmented / Manual | [time] | [max wait] |
| 2 | ... | | | | |

### ✅ Transition Plan
- **Phase 1**: [first changes — highest waste reduction, lowest disruption]
- **Phase 2**: [next changes]
- **Parallel run**: [duration and success criteria]
- **Review date**: [when to assess and iterate]

### ⚠️ Risks and Metrics
- **Key risk**: [what could go wrong in transition]
- **Metrics to track**: [cycle time, defect rate, throughput, wait time]
- **Process owner**: [who owns end-to-end performance]

---

## Thinking Triggers

- *"Am I designing from how the process actually works, or how it's documented?"*
- *"Which steps are waiting vs. working — and can I eliminate the waiting?"*
- *"If I automate this step, am I automating value or automating waste?"*
- *"Who owns the end-to-end outcome, not just their individual step?"*
- *"What happens when this process runs on a bad day — with interruptions, absences, and ambiguity?"*

---

## Common Traps

**Designing from documentation**: The documented process is always wrong. Map what people actually do, then improve that.

**Automating waste**: Automating a bad process makes it fail faster. Eliminate waste first, then automate what remains.

**Ignoring the humans**: A process that looks optimal on paper but requires heroic effort, perfect handoffs, or zero context-switching will fail. Design for real humans with interruptions and bad days.

**No feedback loops**: A process without feedback degrades silently. Build in signals that surface problems close to where they originate.

**Big-bang transitions**: Switching everything at once maximizes risk. Sequence changes, run in parallel, and iterate.
