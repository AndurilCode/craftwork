---
name: systems-thinking
description: Apply systems thinking frameworks whenever the user asks to evaluate, assess, audit, review, or analyze anything — a product, process, architecture, feature, team structure, business model, workflow, or strategy. Triggers on words like "evaluate", "assess", "analyze", "review", "is this working?", "what's wrong with", "how can we improve", "should we change", or any request to understand why something isn't performing as expected. Use this skill even when the user doesn't explicitly say "systems thinking" — if they're asking Claude to understand how something works and where it might fail, this skill should be consulted. Don't wait to be asked twice.
---

# Systems Thinking Evaluation Skill

Evaluate **what's working, what isn't, and why** in any system — technical, organizational, product, or process.

---

## Core Mental Models

### 1. System Boundary
What's **inside** (in scope), **outside** (environment, dependencies, constraints), where does it begin and end?

### 2. Stocks and Flows
- **Stocks**: What accumulates? (users, debt, trust, knowledge, bugs, revenue)
- **Flows**: What changes those stocks? (acquisition, churn, learning, entropy)
- Where are flows **blocked**, **broken**, or **leaking**?

### 3. Feedback Loops
- **Reinforcing (R)**: Self-amplifying — virtuous or vicious cycles
  - More users → more content → more users; more bugs → less trust → fewer contributors → more bugs
- **Balancing (B)**: Self-correcting, goal-seeking
  - High load → auto-scale → stable performance; complaints → support → satisfaction
- Which loops **dominate** current behavior?

### 4. Delays
Time lags between cause and effect. Delays cause **oscillation**, **overcorrection**, or **invisible failures**. Example: hiring takes 3 months → team overloads → burnout → attrition.

### 5. System Archetypes

| Archetype | Pattern | Signal |
|-----------|---------|--------|
| **Limits to Growth** | Growth hits a constraint and stalls | Plateau despite investment |
| **Fixes that Fail** | Quick fix creates new problems | Recurring issues after "solutions" |
| **Shifting the Burden** | Symptomatic fixes erode fundamental ones | Team always firefighting |
| **Tragedy of the Commons** | Shared resources depleted | Quality degrades over time |
| **Escalation** | Competing actors amplify each other | Bidding wars, arms races |
| **Drifting Goals** | Gap closed by lowering standards | "Good enough" keeps declining |
| **Accidental Adversaries** | Well-meaning actors undermine each other | Misaligned team incentives |

### 6. Leverage Points (low → high)
1. Numbers (parameters, budgets, quotas)
2. Buffer sizes and stock capacities
3. Flow rates and delays
4. Feedback loop strength
5. Information flows (who has access to what, when)
6. Rules and incentives
7. Goals of the system
8. Power to change the system's structure
9. **Mindsets and paradigms** — highest

---

## Output Format

### 🟢 Where the System Works
Functioning loops, healthy stocks, aligned incentives. Call out strengths to know what to protect.

### 🔴 Where the System Breaks Down
Broken loops, leaking flows, missing feedback, misaligned incentives. Name the **archetype** if one applies. Identify **delays** that hide problems.

### ⚠️ Key Risks and Failure Modes
What tips the system into bad equilibrium? Which reinforcing loop could go negative? Which constraint is hit next?

### 🎯 High-Leverage Interventions
Ranked list. For each: what changes, what loop/flow it affects, expected result. Flag **quick fixes that might backfire** (Fixes that Fail).

### 📊 System Diagram (when helpful)
```
[A] → (+) [B] → (+) [A]  ← Reinforcing R1
[A] → (+) [C] → (-) [A]  ← Balancing B1
```

---

## Approach

- Be **direct** about what's broken — not diplomacy.
- Use **concrete examples** in the user's context.
- Prioritize **systemic causes** over symptoms — explain *why the system produces the outcome*.
- Recurring problem? Suspect a **reinforcing loop** or **Shifting the Burden**.
- Always suggest **at least one high-leverage intervention** — not just diagnosis.
