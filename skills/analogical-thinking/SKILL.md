---
name: analogical-thinking
description: Apply analogical thinking whenever the user is designing a system, architecture, or process and would benefit from structural patterns that already exist in other domains — or when a problem feels novel but may have been solved elsewhere under a different name. Triggers on phrases like "how should we structure this?", "has anyone solved this before?", "we're designing from scratch", "what's a good model for this?", "I keep feeling like this resembles something", "what patterns apply here?", or when facing architecture, organizational, or process design decisions. Also trigger when a problem has been analyzed thoroughly but no good solution has emerged — the answer may exist in an adjacent domain. Don't reinvent what's been solved. Recognize the shape of the problem first.
---

# Analogical Thinking

**Core principle**: Most genuinely hard problems have structural analogues elsewhere — often solved long ago under a different name. Recognize the *shape* of the problem beneath surface details, then transfer the solution structure.

> The ctx harness as OS memory management. Blackboard pattern from speech recognition (1977) re-emerging in multi-agent AI. TCP congestion control inspiring rate-limiting. Evolution as search algorithm.

The risk: **false analogies** — surface similarity masking structural difference. This skill is as much about knowing when an analogy breaks as when it applies.

---

## Core Process

### Step 1: Abstract the Problem Structure
Strip domain vocabulary:
- What needs to coordinate with what?
- What needs to be stored, retrieved, prioritized, transformed, routed?
- What's the flow? What are the constraints?
- What failure modes are you preventing?

The more abstract, the wider the search space.

**Example:** *"How do agents share intermediate results without stepping on each other?"* → *"Multiple concurrent writers contribute partial results to a shared workspace, with coordination to prevent conflicts and allow selective reading."* Now sounds like distributed systems, DB concurrency, collaborative editing.

### Step 2: Search for Structural Analogues
Look across:

- **Natural systems** — evolution, immune response, neural networks, ant colonies, ecosystems, markets
- **Engineering** — civil, mechanical, electrical, chemical (centuries of patterns)
- **CS classics** — OS design, compiler theory, networking, DB internals, distributed systems
- **Organizational theory** — military command, jazz improvisation, surgical teams, ATC
- **Biology** — cell signaling, protein folding, predator-prey, homeostasis
- **Physics / Information theory** — entropy, signal/noise, conservation laws, phase transitions

### Step 3: Evaluate Strength
Useful when:
- **Relationships** between components map cleanly (not just the components)
- **Constraints** are similar in kind (even if not in degree)
- **Failure modes** of the source are informative

Breaks when:
- Key properties of the original don't hold here
- Scale difference produces different emergent behavior
- Analogy explains structure but not dynamics (or vice versa)

**Always ask:** *"Where does this analogy fail? What's different that matters?"*

### Step 4: Transfer the Solution Pattern
- What's the core mechanism (not implementation)?
- What adaptations are needed?
- What accumulated refinements can you inherit?

---

## High-Value Source Domains

| Domain | Solved | Useful for |
|--------|--------|-----------|
| Operating Systems | Resource allocation, memory management, scheduling, concurrency, isolation, caching, virtual addressing | Agent orchestration, multi-tenancy, LLM context, pipelines |
| Distributed Systems | Consensus under failure, eventual consistency, partition tolerance, idempotency, log-structured storage, leader election | Multi-agent coordination, resilient pipelines, sync |
| Ecology / Evolution | Adaptation under selection, niche differentiation, resource competition, co-evolution, resilience via diversity | Adversarial systems, red teams, org adaptation, market strategy |
| Control Theory | Feedback loops, stability, overshoot, damping, PID, observability | Monitoring, auto-scaling, goal-seeking systems |
| Military / Logistics | Command under uncertainty, supply chains, mission planning under partial info, combined arms | Incident response, large-scale planning, agent coordination |
| Jazz / Improvisation | Structured improvisation, real-time coordination without central control, shared vocabulary enabling emergence | Team autonomy with alignment, agents under ambiguity |

---

## Output Format

### Abstracted Problem Structure
Re-stated in domain-neutral terms: core dynamic, key constraints, failure modes.

### Structural Analogues Found
For each candidate:
- **Source domain**: where the pattern comes from
- **Analogue structure**: how the source solved it
- **Fit**: Strong / Partial / Weak
- **Where it holds**: specific correspondences
- **Where it breaks**: key differences

### Transferred Solution Pattern
- Structure of the solution
- Adaptations needed
- Refinements worth inheriting
- Failure modes to avoid (source domain learned the hard way)

### False Analogy Risks
- Surface similarity that suggests stronger fit than exists
- Properties of the source that don't hold here

---

## Classic Analogies in Software / AI

| Problem | Source | What transferred |
|---------|--------|-----------------|
| Agent context management | OS virtual memory + paging | Active context = RAM; long-term storage = disk; page faults = retrievals |
| Multi-agent coordination | Blackboard architecture (Hearsay-II, 1977) | Shared workspace; specialists read/write; no direct communication |
| LLM token limits | CPU cache hierarchy | Working memory vs. storage; cache misses as retrievals |
| Agent pipeline | Scientific method | Hypothesis → experiment → observation → update → repeat |
| Prompt compression | Data compression / entropy coding | Lossless vs. lossy; semantic entropy as measure |
| AI red teaming | Security pentest | Adversarial mindset, kill chains, surface enumeration |

---

## Thinking Triggers

- *"What's the shape of this problem, stripped of its domain vocabulary?"*
- *"Who has solved a problem with this structure before, in any field?"*
- *"Where does this analogy feel strong? Where strained?"*
- *"What did the source domain learn the hard way that we can inherit for free?"*
- *"If this were a networking problem / biology problem / physics problem, what would the answer look like?"*
