---
name: first-principles-thinking
description: Apply first principles thinking whenever the user is questioning whether a design, strategy, or solution is fundamentally right — not just well-executed. Triggers on phrases like "are we solving the right problem?", "why do we do it this way?", "is this the best approach?", "everyone does X but should we?", "we've always done it this way", "challenge our assumptions", "start from scratch", "is there a better way?", or when the user seems to be iterating on a flawed premise rather than questioning the premise itself. Also trigger when a proposed solution feels like an incremental improvement on something that may be fundamentally broken. Don't optimize a flawed foundation — question it first.
---

# First Principles Thinking

**Core principle**: Strip away assumptions, conventions, and analogies. Reduce to fundamental truths you *know*, then rebuild. Most thinking is by analogy — *"we do it this way because that's how it's done."* First principles asks: *why is it done that way at all?*

---

## Core Process

### Step 1: Identify the Current Belief
- What's the existing approach?
- What problem is it solving?
- What does everyone in this space assume?

### Step 2: Challenge Every Assumption
For each element ask:
- *"Is this actually true, or do we believe it because we've always believed it?"*
- *"Constraint of reality, or constraint of convention?"*
- *"What would have to be true for this assumption to be wrong?"*

Distinguish:
- **Physical constraints** — laws of nature, math, physics — real
- **Resource constraints** — time, money, people — real but changeable
- **Conventional constraints** — "you can't do X" meaning "nobody has yet"
- **Inherited assumptions** — decisions made for past conditions

### Step 3: Identify the Fundamental Truths
Stripped of convention:
- Core need being served?
- Irreducible requirements?
- What if designed from zero, knowing only what's physically true?

### Step 4: Rebuild From the Ground Up
- Simplest approach that satisfies the real requirements?
- What if invented today, with today's capabilities?
- What constraints can be eliminated now that you're not inheriting them?

---

## Output Format

### Current Belief / Approach
- Existing design, strategy, or assumption
- Why it exists (historical/conventional)
- Problem it was meant to solve

### Assumption Deconstruction
| Assumption | Type | Actually true? | Evidence |
|-----------|------|---------------|----------|
| "We need X to do Y" | Conventional | Maybe not | Reason |
| "This requires Z" | Physical | Yes | Because... |
| "Users expect A" | Inherited | Unvalidated | Never tested |

### Fundamental Truths
- Core need
- Hard constraints (genuinely immovable)
- Validated facts (empirically confirmed)

### Rebuilt Solution
- Solution without inherited assumptions
- What changes dramatically?
- What stays the same (and which fundamental truth supports it)?
- What's now possible that wasn't?

### Assumption Risks
- If any single assumption proves wrong, what breaks?
- Which to validate before committing?

---

## Thinking Triggers

- *"What is this actually trying to accomplish at the most basic level?"*
- *"If we were building this today with no legacy, what would we do?"*
- *"Law of nature or law of habit?"*
- *"Who decided this was the right way, and what were their constraints?"*
- *"What would a brilliant outsider — who doesn't know our conventions — suggest?"*
- *"Are we solving the problem, or our version of the problem?"*

---

## Analogy vs. First Principles

Most thinking is analogy: *"company X does it this way" / "industry standard is Y" / "always been done."* Fast and usually adequate, but **inherits the constraints and mistakes of the original**. For genuinely novel solutions or step-change improvements, only first principles gets you there.

---

## Example Applications
- **"Should our agent pipeline be sequential?"** → Why sequential? Ordering of dependencies, or convention from waterfall?
- **"We need a dedicated QA team"** → Necessary function, or historical artifact when testing was slow and manual?
- **"Our API needs versioning"** → Actual need is backward compatibility — minimum mechanism from scratch?
- **"We need standups every day"** → Need is coordination — all the ways to achieve it, unconstrained by "meeting" as a format?
