---
name: topic-explainer
description: "Apply this skill whenever the user asks to have a topic, concept, technology, or idea explained to them. Triggers on phrases like 'explain X to me', 'what is X?', 'how does X work?', 'teach me about X', 'help me understand X', 'break down X', 'ELI5', 'explain like I'm five', 'give me an overview of X', 'I don't understand X', 'walk me through X', or any situation where the user wants to learn or understand something rather than produce an artifact. Also trigger when someone pastes a concept and asks for clarification, when they ask 'why' something works a certain way, or when they need a refresher on a topic they've encountered before. This skill does NOT apply to 'write documentation about X' (use technical-writing) or 'analyze X' (use reasoning skills). This skill is for when the human is the learner."
---

# Topic Explainer

**Core principle**: An explanation succeeds when the learner can use the concept. Match style to topic shape; produce the shortest explanation that changes the learner's mental model.

---

## STEP 1 — Analyze the Topic (internal)

Classify silently along:

```
Topic, Domain (technical / scientific / conceptual / practical / business / creative),
Abstraction (concrete / mixed / abstract),
Prerequisites (none / light / moderate / heavy),
Core challenge (jargon / counterintuitive / hidden complexity / many parts /
  needs prior concepts / no physical analogy)
```

Drives Step 2. Do not show.

---

## STEP 2 — Recommend Style and Depth

### Explanation Styles

| Style | How it works | Best for | Avoid when |
|-------|-------------|----------|------------|
| **Feynman** | Strip jargon, use simple words and everyday analogies, build from fundamentals outward. | Abstract/complex topics where jargon masks understanding (quantum mechanics, monads, eventual consistency) | Topic already simple; learner is expert needing precision |
| **Socratic** | Guide via questions until learner discovers the concept. Never state answer until they arrive. | Topics where *why* matters more than *what*; correcting misconceptions; design/philosophy | Quick factual answer needed; purely procedural topic |
| **Example-First** | Concrete working example first; show in action before theory; generalize specific → abstract. | Programming concepts, practical skills, tools, APIs, anything the learner will use | Highly abstract topics with no natural concrete example |
| **Layered** | One-sentence version; add layers; each layer is complete on its own. | Broad topics with natural depth (how the internet works, ML, compilers) | Narrow topics where layering adds nothing |
| **Analogy Bridge** | Map entire explanation to a domain the learner knows; note where it breaks. | Unfamiliar domains with structural parallels (databases ↔ libraries, networking ↔ postal system, Git ↔ video-game save points) | No good analogy exists, or analogy misleads |
| **Visual-Spatial** | Build a mental picture/diagram; describe relationships spatially. | Systems, architectures, processes, interacting components (microservices, state machines, org structures) | Linear/sequential concepts with no spatial structure |

### Verbosity Levels

| Level | Output | Length | When |
|-------|--------|--------|------|
| **TL;DR** | Definition + why-it-matters | 2-3 sentences | Casual ask, quick anchor, evaluating depth |
| **Brief** | Concept + one example/analogy + key implication | 1-2 paragraphs | Adjacent knowledge, filling specific gap |
| **Standard** | Full explanation with examples, analogies, common pitfalls | 3-6 paragraphs | Default |
| **Deep Dive** | Edge cases, nuances, history, trade-offs, connections | 8+ paragraphs, sectioned | Explicit deep request, or topic too complex for standard |
| **Tutorial** | Hands-on walkthrough; learner does + sees results; theory woven in | Structured steps | Learner wants to *do*, not just understand |

### Recommendation Logic

```
abstract + counterintuitive       → Feynman + Standard
design/philosophy / misconception → Socratic + Standard
tool / language / API / skill     → Example-First + Standard (Tutorial if hands-on)
broad with depth layers           → Layered + Standard
unfamiliar + strong analogy       → Analogy Bridge + Brief
interacting components / system   → Visual-Spatial + Standard
"ELI5" / "simply"                 → Feynman + Brief
"quick overview" / "in a nutshell"→ Layered + TL;DR
user states preference            → use it; do not override
```

### Incompatible Combinations

- **Socratic + TL;DR**: Socratic needs dialogue. → Feynman + TL;DR, or upgrade to Brief.
- **Tutorial + TL;DR/Brief**: Tutorial can't be brief. → Example-First + Brief, or upgrade to Tutorial verbosity.
- **Feynman + Deep Dive**: Tension. → Layered + Deep Dive, or Feynman + Standard.

---

## STEP 3 — Present Options

```
I'd recommend explaining [topic] using [style] at [verbosity] depth.
[1-sentence reason.]

Want me to adjust?
  Style: [recommended] / [alt 1] / [alt 2]
  Depth: TL;DR / Brief / Standard / Deep Dive / Tutorial
```

Use ask_user_input if available. **Skip this step entirely** for simple questions ("what is Redis?") — default Example-First + Brief and deliver.

---

## STEP 4 — Deliver

#### Feynman
1. Identify the ONE core idea
2. Use words a smart 12-year-old knows
3. Ground abstractions in physical analogies
4. Define any term immediately, in simple language
5. Connect back to why it matters

**Check**: Any sentence requiring domain expertise to parse? Rewrite.

#### Socratic
1. Open with a question activating prior knowledge
2. Chain questions where each answer leads to the next
3. Let learner "discover" the concept
4. State concept directly only after questions laid groundwork
5. Close with a test question

**Check**: Could the learner arrive at the concept from these questions alone?

#### Example-First
1. Show concrete example immediately (code, scenario, real case)
2. Walk through what happens, step by step
3. Highlight the surprising/non-obvious part
4. Introduce the general principle
5. Show a second example in a different context

**Check**: Without theory, would examples teach 70% of the concept?

#### Layered
1. **Layer 0**: One sentence. "X is [definition]."
2. **Layer 1 — shape**: What/problem/relation to known things (1 paragraph)
3. **Layer 2 — mechanism**: Key moving parts (2-3 paragraphs)
4. **Layer 3 — nuances**: Edge cases, trade-offs, misconceptions, when NOT to use (2-3 paragraphs)
5. **Layer 4 — connections**: Related concepts, where to go deeper (1 paragraph)

Each layer is complete; layers add but never contradict.

**Check**: Read only Layer 0+1. Valid explanation?

#### Analogy Bridge
1. State analogy: "X is like Y, because..."
2. Map components: "[A in X] plays the role of [B in Y]"
3. Walk through analogy in action
4. **State where it breaks down** explicitly
5. Transition from analogy to precise understanding

**Check**: Holds for the core mechanism? Any property it would mislead about? If so, switch.

#### Visual-Spatial
1. Describe the overall shape ("Three boxes connected by arrows...")
2. Name each component and its responsibility
3. Walk through a scenario: input enters → what happens?
4. Highlight boundaries, bottlenecks, critical connections
5. Provide actual diagram if possible (ASCII, Mermaid, SVG)

**Check**: Could the learner draw the system from your words?

---

## STEP 5 — Verify Understanding

Offer one based on style:

- **Feynman**: "Can you rephrase this in your own words?"
- **Socratic**: "What would happen if [novel scenario]?"
- **Example-First**: "Want to try applying this to a different case?"
- **Layered**: "Want me to go one layer deeper?"
- **Analogy Bridge**: "Does the analogy hold, or is there a part that feels off?"
- **Visual-Spatial**: "Want me to zoom into any component?"

Optional. Skip if user signals completion ("got it", "thanks").

---

## Calibration

1. **Speed over ceremony.** Simple topic? Skip the analyze-recommend dance. Pick Example-First + Brief and deliver.
2. **Explicit request overrides recommendation.** "ELI5" → Feynman + Brief. "Walk me through" → Tutorial. Never argue.
3. **Analogies are powerful and dangerous.** A bad analogy creates a wrong model that's hard to dislodge. Always state where it breaks; switch styles if no analogy holds.
4. **Socratic needs patience.** Gauge first; switch to Feynman/Example-First if user wants speed.
5. **Match precision to expertise.** Domain experts get precise technical language, not "imagine a Google Doc."
6. **End with door open.** Implicit invitation to go deeper or follow up.

---

## Thinking Triggers

- *"What does this LOOK LIKE in the learner's head now? What should it look like after?"*
- *"What's the ONE thing — if they understood nothing else — most worth knowing?"*
- *"Am I explaining what this IS, or why it MATTERS? They need 'why' first."*
- *"Would an example do more work than three paragraphs of theory?"*
- *"What misconception is most likely? Can I preempt it?"*
- *"If I used only this analogy, would the learner be misled or enlightened?"*
