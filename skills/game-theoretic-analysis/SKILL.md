---
name: game-theoretic-analysis
description: "Apply game-theoretic analysis whenever multiple agents, actors, teams, or systems interact strategically — where each party's best move depends on what the others do. Triggers on \"what's their incentive?\", \"why would they cooperate?\", \"how do we align incentives?\", \"coordination problem\", \"trust problem\", or any situation involving negotiation, competition, cooperation under self-interest, or multi-agent interaction. Also trigger when designing multi-agent AI systems, agent negotiation protocols, or when a design fails because agents optimize for own payoffs rather than the system goal."
---

# Game-Theoretic Analysis

When multiple agents interact and each agent's outcome depends on others' choices, you have a game. Map players, strategies, payoffs, and equilibria — the only reliable way to predict behavior and design rules where rational self-interest produces good outcomes.

---

## When to Use

- Multiple agents (people, teams, companies, AI agents) whose choices affect each other's outcomes
- Suspected incentive misalignment — system should work but doesn't because participants optimize locally
- Designing rules, protocols, scoring systems, allocation mechanisms
- Cooperation needed but not happening (or fragile)
- Negotiation strategy
- Multi-agent AI systems being designed, debugged, evaluated
- Tragedy-of-the-commons pattern (shared resources degrading)
- "Why would they do X?" where X seems irrational — usually rational given their payoffs

---

## The Core Process

### Step 1: Define the Game

Identify each component explicitly:

- **Players**: Actual decision-makers, not just teams
- **Strategies**: Concrete actions ("share full context," "hoard information," "ship fast and cut corners," "undercut on price")
- **Payoffs**: What each player gains/loses for each strategy combination — even rough quantification
- **Information**: What each player knows about others' strategies, payoffs, past actions
- **Timing**: Simultaneous or sequential? One-shot or repeated? Finite or indefinite horizon?

### Step 2: Classify the Game Type

| Game type | Structure | Real-world pattern |
|-----------|-----------|-------------------|
| **Prisoner's Dilemma** | Individual rationality → collective harm | Code shortcuts, context hoarding, tech debt, arms races |
| **Coordination Game** | Multiple good equilibria, miscoordination risk | Standard adoption, API design, conventions, migration timing |
| **Chicken / Hawk-Dove** | Mutual aggression = worst outcome | Deadline negotiations, resource contention, who blinks first |
| **Stag Hunt** | High reward needs trust; safe option exists | Ambitious refactors, team tool adoption, shared infrastructure |
| **Public Goods / Commons** | Contributing benefits all, free-riding tempts | Shared docs, code reviews, context enrichment, OSS |
| **Auction / Allocation** | Scarce resources, competing claims | Token budget, context window, CI priority |
| **Principal-Agent** | One acts on behalf of another with different incentives | Manager-engineer, company-contractor, user-AI delegation |
| **Signaling Game** | One party has private info, the other observes actions | Interviews, PR descriptions, agent confidence reporting |
| **Bargaining / Negotiation** | Surplus to divide, disagreement point exists | Salary, scope, resource sharing |

### Step 3: Find the Equilibrium

Ask: **If every player optimizes for their own payoff, what's the stable outcome?**

- **Dominant strategy**: Best regardless of what others do? Predict they'll play it.
- **Nash Equilibrium**: No player can improve by unilaterally changing. May be multiple — identify all.
- **Pareto optimality**: Is the equilibrium also the best collective outcome? If not, **social dilemma** — game structure produces a suboptimal result.
- **Mixed strategies**: No pure equilibrium → players randomize. Shows up as unpredictable or oscillating behavior.

**Critical diagnostic**: If Nash Equilibrium ≠ Pareto Optimum, the game is broken by design. No persuasion or "alignment" fixes it — the rules must change.

### Step 4: Analyze Dynamics (Repeated Games)

- **Shadow of the future**: Higher value on future interactions → more cooperation. Finite known endpoints kill cooperation (backward induction).
- **Reputation effects**: Can players build/observe reputations? Reputation is the enforcement mechanism in repeated games.
- **Tit-for-tat**: Can defection be detected and punished? Cooperation rewarded?
- **Equilibrium selection**: Many equilibria exist (Folk Theorem). Question shifts to "which equilibrium does the system select for?" — depends on norms, history, focal points.

### Step 5: Design the Mechanism

If you can change the rules, apply **mechanism design** — reverse game theory:

**Goal**: Define the desired outcome (efficiency, fairness, truthfulness, cooperation).

- **Lever 1 — Payoffs**: Make cooperation pay more, defection cost more. Bonuses for shared context, penalties for hoarding.
- **Lever 2 — Information**: Make actions observable. Transparency kills defection strategies. Dashboards, audit trails, public commits.
- **Lever 3 — Timing**: Sequential moves with commitment change equilibria. First-mover with visible commitment can break coordination deadlocks.
- **Lever 4 — Rules**: Enforcement (automated checks, reviews), contracts (SLAs, DoD), restructure who plays with whom.
- **Lever 5 — Eliminate the game**: Centralize the decision, automate the allocation, remove the resource contention. Kanban-as-truth eliminates the context-hoarding game by making externalization the only path forward.

**Mechanism properties to aim for**:
- **Incentive compatibility**: Truth-telling and cooperation are dominant, not just optional
- **Individual rationality**: Every player better off participating than not
- **Budget balance**: No external subsidy required to run
- **Robustness**: Works even when players are strategic, not just cooperative

---

## Multi-Agent AI Applications

- **Context as strategic resource**: Shared token budget allocation is a game. An agent claiming more context performs better individually but degrades the system. Design allocation mechanisms, not just budgets.
- **Negotiation protocols**: When agents must agree on a plan/contract/design, the protocol determines the outcome. Bad protocols produce deadlocks, oscillation, mediocre convergence.
- **Scoring as incentive design**: The metric IS the incentive function. Score on speed → quality drops. Score on coverage → output padded. Goodhart's Law is a game-theoretic prediction.
- **Topology as game design**: Pipeline = principal-agent chain. Committee = coordination game. Debate = zero-sum game.
- **Emergent equilibria in loops**: Iterative refinement can converge on locally stable but globally suboptimal patterns. Detect via convergence-without-improvement monitoring.

---

## Output Format

### 🎮 Game Definition
- **Players**: roles and decision authority
- **Strategies**: available actions per player
- **Payoffs**: gains/losses — matrix for 2-player games
- **Information**: who knows what, when
- **Timing**: simultaneous/sequential, one-shot/repeated

### 🏷️ Game Classification
- **Type**: Prisoner's Dilemma / Coordination / Stag Hunt / etc.
- **Why**: what structural feature maps to this archetype

### ⚖️ Equilibrium Analysis
- **Nash Equilibrium**: stable outcome under self-interested play
- **Pareto Optimum**: best collective outcome
- **Gap**: if these differ — the core problem to solve
- **Dynamics**: cooperation sustainability, reputation effects (repeated games)

### 🔧 Mechanism Design Recommendations
- Ranked interventions — which lever and why
- For each: what changes, what new equilibrium emerges, what could go wrong
- Flag perverse incentives the mechanism might create

### ⚠️ Strategic Risks
- Exploit potential in the mechanism?
- Where might coalitions form?
- What information asymmetry could be weaponized?

---

## Thinking Triggers

- *"Why would a rational agent NOT cooperate here?"*
- *"What game are they actually playing?"* — stated and real games often differ
- *"If I were optimizing selfishly, what would I do?"*
- *"Can I make the desired behavior also the self-interested behavior?"*
- *"What information would change the equilibrium?"*
- *"One-shot or repeated? Does the end date matter?"*
- *"Who's the residual claimant?"* — bears cost of bad outcomes, has incentive to fix

---

## Interaction with Other Skills

- **systems-thinking**: shows *how* the system behaves; game theory shows *why* rational agents make it behave that way.
- **stakeholder-power-mapping**: identifies players and influence; game theory formalizes what they'll *do* given incentives.
- **second-order-thinking**: traces consequence chains; game theory adds strategic anticipation.
- **theory-of-constraints**: identifies bottlenecks; game theory asks whether the bottleneck persists because someone benefits.
- **mechanism design is the constructive application**: other skills diagnose — game theory diagnoses *and* designs incentive-compatible rules.

---

## Example Application Triggers

- "Agents converging on mediocre solutions" → check if scoring function creates a Prisoner's Dilemma where safe-but-mediocre is dominant
- "Nobody contributes to shared docs" → Public Goods game, design contribution incentives or make non-contribution visible
- "Two teams can't agree on API contract" → Bargaining game, identify disagreement point, design fair division
- "How to allocate context window across agents?" → Auction/allocation, design for truthful reporting of needs
- "Auto-review keeps getting gamed" → Principal-Agent with information asymmetry
- "Great process but nobody follows it" → Following the process isn't a dominant strategy. Process design is the bug.
