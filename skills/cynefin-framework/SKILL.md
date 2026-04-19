---
name: cynefin-framework
description: Apply the Cynefin framework whenever the user is deciding how to approach a problem, choosing between solutions, or asking why a previous solution didn't work. Triggers on phrases like "how should we approach this?", "which solution is better?", "we tried X but it didn't work", "this is complicated", "this feels unpredictable", "we don't know what to do", "what's the right process here?", or when evaluating whether to apply best practices, run experiments, or call in experts. Also trigger when the user is applying a structured/rigid process to something that might be complex or chaotic — this is a common mismatch that Cynefin catches. Use this skill before recommending any solution approach.
---

# Cynefin Framework

**Core**: Classify the problem domain before applying any solution. The right action in one domain is wrong in another. Misclassification is one of the most common causes of failed interventions.

---

## The Five Domains

### 1. 🟢 Clear (formerly "Simple")
- **Cause/effect**: Obvious to everyone.
- **Approach**: **Sense → Categorize → Respond.** Apply known best practice. Automate.
- **Signs**: Answer is obvious; any competent person would do the same.
- **Danger**: Complacency — Clear can shift to Chaotic if conditions change unnoticed.
- **Examples**: Resetting a password, deploying a known-working config, following a checklist.

### 2. 🔵 Complicated
- **Cause/effect**: Exists but requires analysis or expertise.
- **Approach**: **Sense → Analyze → Respond.** Engage experts; evaluate trade-offs between valid options.
- **Signs**: Need an expert, but once analyzed, the answer becomes clear. There's a knowable right answer.
- **Danger**: Expert overconfidence — mistaking Complicated for Clear.
- **Examples**: Software architecture, performance tuning, medical diagnosis, legal strategy.

### 3. 🟡 Complex
- **Cause/effect**: Visible only **in retrospect**. Outcomes unpredictable.
- **Approach**: **Probe → Sense → Respond.** Run safe-to-fail experiments (small, reversible, parallel). Amplify what works, dampen what doesn't. Embrace emergence.
- **Signs**: Experts disagree. Past data unreliable. Human behavior, social dynamics, high interconnectedness.
- **Danger**: Applying Clear/Complicated approaches (best practices, big-bang plans) — the most common mistake.
- **Examples**: Product-market fit, culture change, user behavior, AI behavior, team dynamics.

### 4. 🔴 Chaotic
- **Cause/effect**: None discernible. System in crisis.
- **Approach**: **Act → Sense → Respond.** Immediate stabilizing action. Don't wait for analysis. Move to Complex/Complicated once stable.
- **Signs**: Crisis. Active failure. No time for deliberation.
- **Danger**: Staying in chaotic mode too long.
- **Examples**: Production outage, security breach, public crisis, team breakdown.

### 5. ⚫ Disorder (center)
You don't know which domain you're in. Break the situation into parts and classify each. Multiple people will interpret it through their own domain lens — get clarity before acting.

---

## Output Format

### 🗺️ Domain Classification
- **Domain**: Clear / Complicated / Complex / Chaotic / Disorder
- **Confidence**: High / Medium / Low
- **Key signals** for this classification
- **Alternative interpretation**: Could it be misclassified? Implications?

### ⚠️ Domain Mismatch Check
Is the current plan applying a **wrong-domain** approach?

| Current approach | Actual domain | Mismatch risk |
|-----------------|---------------|---------------|
| Best practice playbook | Complex | High — will fail |
| Big analysis, single solution | Chaotic | High — too slow |
| Experiments / probing | Clear | Waste of time |

### 🎯 Recommended Approach
- **Clear**: Apply best practice [name]. Consider automating.
- **Complicated**: Engage experts. Evaluate trade-offs between [A] and [B].
- **Complex**: Design 2–3 safe-to-fail experiments. Define amplify/dampen signals.
- **Chaotic**: Act immediately on [stabilizing action]. Reassess once stable.

### 🔁 Domain Transitions
Is the domain **shifting**? What pushes it to chaos? Path back to clear?

---

## Heuristics

- Experts disagree → probably Complex
- People and behavior at scale → probably Complex
- Urgent and breaking → probably Chaotic; act first
- Known playbook → probably Clear or Complicated
- Past solutions stopped working → domain may have shifted

---

## The Most Common Mistake
Treating **Complex** as **Complicated**: hire a consultant, define "the right answer", execute a big plan — when the system is emergent. Plan fails, more consultants, bigger plan, still fails.

**Fix**: Run small experiments. Let patterns emerge. Amplify what works.
