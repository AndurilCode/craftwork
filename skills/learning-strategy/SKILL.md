---
name: learning-strategy
description: "Apply learning-strategy whenever the user needs to close a knowledge gap, ramp up on a new domain, or build a structured plan for acquiring understanding. Triggers on phrases like \"how do I learn this?\", \"I'm new to this domain\", \"ramp up on\", \"knowledge gap\", \"what should I study?\", \"learning plan\", \"how do I get up to speed?\", \"teach me about\", \"onboarding plan\". Use proactively when epistemic-mapping reveals gaps that block decisions — knowing what you don't know is only useful if you then learn it efficiently."
---

# Learning Strategy

**Core principle**: Learning is not consuming — it is restructuring what you know. Efficient learning targets the specific gap, selects the right mode for the knowledge type, and tests understanding before moving on. A reading list is not a learning plan.

---

## When to Use This Skill

- epistemic-mapping identified knowledge gaps blocking a decision or analysis
- Someone is entering an unfamiliar domain and needs to ramp up fast
- A team needs to build shared understanding of a new technology, market, or method
- Prior learning attempts stalled — consuming material without retaining or applying it
- An onboarding plan is needed for a new team member or role transition

---

## Core Methodology

### Step 1: Define the Knowledge Gap Precisely

Vague goals ("learn machine learning") produce vague learning. Specify:

- **What you need to know**: The specific questions you need to answer or capabilities you need to perform. Frame as concrete outcomes: "Evaluate whether a transformer architecture fits our latency requirements" not "understand transformers."
- **Why it matters**: What decision, action, or deliverable is blocked by this gap. This determines depth — you don't need PhD-level understanding to make a procurement decision.
- **Current knowledge level**: What you already know in this area and adjacent domains. Prior knowledge is the scaffold for new knowledge. Identify it explicitly so you build on it rather than starting from scratch.
- **Target depth**: Awareness (know it exists), comprehension (explain it), application (use it), or mastery (teach it and handle edge cases). Most professional learning targets application.

### Step 2: Map Prerequisites

Knowledge has dependencies. Learning X before Y is sometimes impossible.

Build a dependency tree:
1. List the key concepts in the target domain
2. For each concept, ask: "What must I understand before this makes sense?"
3. Identify which prerequisites you already have (mark as satisfied)
4. The unsatisfied prerequisites closest to your current knowledge are where learning starts

Common prerequisite failure modes:
- Jumping to advanced material without foundational concepts → confusion and surface-level memorization
- Spending too long on prerequisites that aren't actually needed for your target depth
- Missing a conceptual prerequisite while having the technical one (or vice versa)

### Step 3: Select Learning Modes

Different knowledge types require different learning approaches:

**Declarative knowledge** (facts, concepts, frameworks) → Reading, lectures, structured summaries. Test with explanation: can you teach it to someone else without notes?

**Procedural knowledge** (how to do things) → Hands-on practice, tutorials with exercises, deliberate repetition. Test with performance: can you do it without following instructions?

**Conditional knowledge** (when to apply what) → Case studies, worked examples with variation, exposure to edge cases. Test with transfer: can you apply it to a novel situation?

**Tacit knowledge** (judgment, intuition) → Apprenticeship, observation of experts, reflection on your own practice. Test with prediction: can you anticipate what will happen before it does?

For each topic in your plan, specify the primary learning mode. Mismatching mode to knowledge type is the most common source of wasted learning time — reading about how to negotiate teaches concepts but not skill.

### Step 4: Sequence the Learning Plan

Order topics to maximize understanding and motivation:

1. **Start with orientation**: A 30-minute survey of the entire domain — read a good overview, watch an introductory talk. Goal: build a mental map of the territory before diving into any region.
2. **Follow the prerequisite tree**: Bottom-up from unsatisfied prerequisites to target concepts.
3. **Interleave theory and practice**: Alternate between conceptual understanding and hands-on application. Pure theory without practice doesn't consolidate; pure practice without theory doesn't transfer.
4. **Increase difficulty progressively**: Start with clean, prototypical examples. Introduce complexity and edge cases after fundamentals are solid.

For each topic, specify:
- Source(s) to use (book chapter, documentation section, course module, expert to consult)
- Learning mode (read, do, observe, discuss)
- Time estimate
- Output to produce (notes, exercise completion, explanation draft)

### Step 5: Build Verification Checkpoints

Learning without testing understanding is just exposure. Build checkpoints that reveal genuine understanding vs. familiarity:

**Feynman Test**: Explain the concept in plain language as if teaching a non-expert. Where your explanation gets vague, hand-wavy, or requires jargon — that's where understanding breaks down. Go back and study that part.

**Application Test**: Solve a problem you haven't seen before using the concept. If you can only solve problems identical to the examples, you've memorized patterns, not learned principles.

**Prediction Test**: Before reading the next section or running the next experiment, predict what you'll find. Surprise indicates a gap in your model.

**Teaching Test**: Explain to a colleague or write it up. If you can handle their questions, you've learned it. If you can't, you know exactly where to focus next.

Place a checkpoint after each major topic. Define the specific test and the minimum bar for "understood well enough to proceed."

### Step 6: Plan for Retention

Understanding today doesn't guarantee recall next month. Build retention into the plan:

- **Spaced repetition**: Review key concepts at increasing intervals — day 1, day 3, day 7, day 14, day 30. Focus reviews on material you got wrong at the last checkpoint.
- **Active recall**: Don't re-read notes. Close them and try to reconstruct the key points from memory. Re-reading feels like learning but produces minimal retention.
- **Connection-building**: Link new knowledge to things you already know. Analogies, comparisons to adjacent domains, integration into existing mental models. Isolated knowledge decays fastest.
- **Application schedule**: Plan real uses of the knowledge within the first week. Knowledge used in context is retained; knowledge that sits idle fades.

---

## Output Format

### 🧠 Knowledge Gap
- **What to learn**: [Specific knowledge or capability needed]
- **Why it matters**: [Decision or action blocked by this gap]
- **Current level**: [What you already know in this and adjacent areas]
- **Target depth**: [Awareness / Comprehension / Application / Mastery]

### 🗺️ Prerequisite Map
```
[Target Concept]
├── [Prerequisite A] ✅ (already known)
├── [Prerequisite B] ❌ (must learn)
│   ├── [Sub-prerequisite B1] ✅
│   └── [Sub-prerequisite B2] ❌ (start here)
└── [Prerequisite C] ❌ (must learn)
```

### 📋 Learning Plan

| # | Topic | Mode | Source | Time | Output |
|---|-------|------|--------|------|--------|
| 1 | [Topic — start with prerequisites] | [Read/Do/Observe/Discuss] | [Specific source] | [Estimate] | [What you'll produce] |
| 2 | [Next topic] | [Mode] | [Source] | [Estimate] | [Output] |
| ... | | | | | |

### 🎯 Key Concepts to Master
For each core concept, write the Feynman-style plain-language explanation target:
- **[Concept 1]**: [Plain-language explanation you should be able to give when you've learned it]
- **[Concept 2]**: [Plain-language explanation target]

### ✅ Progress Checkpoints

| After | Test | Pass criteria |
|-------|------|---------------|
| [Topic/module 1] | [Feynman / Application / Prediction / Teaching] | [Specific bar for "understood"] |
| [Topic/module 2] | [Test type] | [Specific bar] |

### ⏱️ Time Investment
- **Total estimated hours**: [Sum of learning plan]
- **Calendar schedule**: [Recommended pacing — e.g., 2 hours/day for 5 days]
- **First application date**: [When to use the knowledge in real work]

### 🔄 Retention Plan
- **Spaced review schedule**: [Day 1, 3, 7, 14, 30]
- **Active recall method**: [Flashcards / self-quizzing / whiteboard reconstruction]
- **Application opportunities**: [Real tasks where this knowledge will be used]

---

## Thinking Triggers

- *"Am I consuming material or actually understanding it? Can I explain this without looking at my notes?"*
- *"What's the minimum I need to learn to unblock the decision — and what can wait?"*
- *"Am I starting at the right level, or am I missing prerequisites I don't know I'm missing?"*
- *"Is reading the right mode here, or do I need to learn by doing?"*
- *"What would surprise me about this topic? Where are my predictions wrong?"*
- *"A week from now, what from today's learning will I actually remember?"*

---

## Common Traps

- **Collector's fallacy**: Gathering resources (bookmarking articles, buying courses, saving papers) and mistaking that for learning. Collecting is not understanding. A reading list with nothing read is zero knowledge.
- **Tutorial hell**: Completing guided exercises but never building anything without instructions. Tutorials teach following; practice teaches doing.
- **Depth mismatch**: Spending weeks reaching mastery depth when application depth was all that was needed. Match learning investment to the actual requirement.
- **Linear completion**: Working through a textbook front-to-back when only chapters 3, 7, and 12 are relevant. Use the prerequisite map to skip what you don't need.
- **Passive review**: Re-reading highlighted notes feels productive but produces minimal retention. Active recall (testing yourself) is 3-5x more effective per hour invested.

---

## Example Applications

| Trigger | Application |
|---------|-------------|
| "I need to evaluate whether to adopt Kubernetes" | Target depth: application (make the decision, not operate clusters). Prerequisite map: container basics → orchestration concepts → K8s architecture → operational requirements. Mode: read overview + talk to an operator (tacit knowledge about operational burden). |
| epistemic-mapping flagged "We don't understand our users' workflow" | Target depth: comprehension. Mode: observation (watch users work), then discussion (interview for tacit knowledge). Checkpoint: predict a user's next action correctly 70% of the time. |
| "New team member needs to onboard to our codebase" | Map prerequisite domains (language, framework, domain concepts). Sequence: architecture overview → guided code walkthrough → small bug fix → feature implementation. Checkpoints at each stage. |
| "I keep reading about distributed systems but nothing sticks" | Diagnose the mode mismatch: reading alone doesn't build procedural knowledge. Redesign: read one chapter, then implement a simplified version, then predict failure modes before reading about them. |
