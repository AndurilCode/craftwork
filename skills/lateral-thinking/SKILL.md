---
name: lateral-thinking
description: Apply lateral thinking whenever the user is stuck on a problem, has tried the obvious solutions without success, needs to generate new ideas or alternatives, or wants to break out of conventional thinking patterns. Triggers on phrases like "we're out of ideas", "nothing seems to work", "what else could we try?", "how do we innovate here?", "we keep thinking about it the same way", "what if we approached this differently?", "brainstorm alternatives", "we need a creative solution", or any situation where analytical thinking has hit a ceiling. Also trigger when a proposed solution is merely an incremental improvement on the existing approach — lateral thinking looks sideways, not just forward. Don't keep digging in the same direction when the hole isn't working.
---

# Lateral Thinking

**Core principle**: Vertical thinking digs deeper in the same direction. Lateral thinking moves *sideways* — escaping the dominant pattern to find a different place to dig. Goal: a different solution, not a better version of the current one.

> *"You cannot dig a hole in a different place by digging the same hole deeper."* — Edward de Bono

---

## When Vertical Thinking Fails

Stop digging and move laterally when:
- The problem keeps recurring despite fixes (frame is wrong)
- All solutions feel like variations of the same idea
- The best option is "least bad"
- Everyone agrees on the approach (groupthink + vertical)
- The problem is genuinely novel

---

## Core Techniques

### 1. Random Entry
Inject an unrelated stimulus and force a connection.

1. Pick a random word (*bridge / fog / anchor / seed / mirror / friction*)
2. List its properties/associations
3. Force-connect each to the problem
4. Don't filter

**Example:** *Reduce agent pipeline errors?* + *filter* → passive validation layer between agents that flags but never blocks.

### 2. Provocation (Po)
Make a deliberately absurd or reversed statement. The "Po" operator signals provocation, not claim.

- *Po: the agent has no memory at all*
- *Po: users pay us to make mistakes*
- *Po: the bottleneck is the solution*

1. State the provocation (extreme — mild ones produce mild ideas)
2. Ask *"What would have to be true for this to work?"*
3. Ask *"What intermediate ideas does this generate?"*
4. Extract usable concepts even when the provocation is impossible

**Example:** *Onboarding too long* + *Po: users onboard themselves before they meet us* → pre-onboarding flow completed async.

### 3. Challenge
Question every assumption about *why* things are done this way:

- *"Why is it done this way?"*
- *"Does it have to be done at all?"*
- *"Does it have to be done in this order?"*
- *"Does it have to be done by this person/system?"*
- *"Does it have to be done at this point in the process?"*

Distinguish:
- **Necessary constraints** — remove them and the goal disappears
- **Arbitrary constraints** — historical, habitual, inherited (fertile ground)

### 4. Alternatives (Fixed Point)
Fix the goal, change everything else.

1. State fixed point: *"The goal is [outcome]"*
2. Generate 10+ routes — obvious, strange, impractical
3. Evaluate only after the full list exists
4. Look for hybrids between non-obvious options

**Quota thinking**: set a number first ("we need 15") — forces past the obvious 3–4.

### 5. Concept Extraction
Abstract current solution to its concept; find other implementations.

1. Describe current solution in one sentence
2. Extract the underlying concept
3. List other implementations
4. Develop the most promising

**Example:** *Weekly sync meeting* → concept: *shared awareness of state* → async status page, ambient dashboard, daily digest, visual kanban, automated diff reports.

### 6. Reversal
Reverse the problem; work backwards.

1. State problem: *"How do we get more users to complete onboarding?"*
2. Reverse: *"How do we get users to abandon onboarding?"*
3. List everything that would cause the reversed outcome
4. Invert back into ideas

---

## Output Format

### Dominant Pattern
Name it before generating alternatives:
- *"Current thinking: [frame/assumption/direction]"*
- *"The rut: [what keeps pulling solutions back]"*

### Generated Alternatives
Group by technique. For each:
- **Idea**: one-sentence description
- **Origin**: which technique generated it
- **Kernel**: useful concept inside, even if the idea is impractical

Quantity first, quality second.

### Most Promising Concepts
Select 2–4 with most potential:
- Why worth developing?
- What would need to be true?
- Next concrete test?

### Pattern Traps
Flag ideas that are vertical disguised as new (refined versions of the existing approach).

---

## Session Rules

1. **Suspend judgment** during generation
2. **Welcome the absurd** — impractical ideas contain useful kernels
3. **Quantity before quality** — past the first 3 obvious answers
4. **Build, don't reject** — "yes, and..." before "yes, but..."
5. **Name the dominant pattern first** — can't escape a rut you haven't identified

---

## Thinking Triggers

- *"What would this look like if we had no history with the problem?"*
- *"Who solves a completely different problem in a way that could apply here?"*
- *"What's the most counterintuitive thing we could do?"*
- *"If we couldn't use the current approach at all, what would we do?"*
- *"What would a 10-year-old suggest? Someone from a completely different industry?"*
- *"What are we not allowed to question — and why?"*

---

## Example Applications
- **"We've tried everything to reduce churn"** → Challenge assumptions; Reversal to find what causes people to *want* to leave, inverted into retention ideas
- **"Pipeline is slow, don't know how to speed it up"** → Random Entry + Provocation to break out of "optimize each step"
- **"New feature but everything feels incremental"** → Concept Extraction on what users hire current features to do
- **"Team keeps proposing the same retro solutions"** → Fixed Point with quota of 15
