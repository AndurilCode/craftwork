---
name: game-theoretic-analysis
description: "Apply game-theoretic analysis whenever multiple agents, actors, teams, or systems interact strategically — where each party's best move depends on what the others do. Triggers on phrases like \"what's their incentive?\", \"why would they cooperate?\", \"how do we prevent free-riding?\", \"design the rules so that...\", \"what happens if everyone acts selfishly?\", \"how do we align incentives?\", \"who benefits from defecting?\", \"why does nobody go first?\", \"we need a fair allocation\", \"auction design\", \"pricing game\", \"coordination problem\", \"trust problem\", or any situation involving negotiation, competition, cooperation under self-interest, or multi-agent interaction. Also trigger when designing multi-agent AI systems, token/resource allocation between agents, agent negotiation protocols, or when a technically sound design is failing because agents (human or AI) are optimizing for their own payoffs rather than the system goal. Don't diagnose incentive problems with systems-thinking alone — if strategic choice is involved, this skill must be consulted."
---

# Game-Theoretic Analysis

**Core principle**: When multiple agents interact and each agent's outcome depends on the choices of others, you have a game. Understanding the game's structure — who the players are, what strategies they have, what payoffs result, and what equilibria emerge — is the only reliable way to predict behavior and design systems where rational self-interest produces good outcomes.

---

## When to Use This Skill

Trigger whenever:
- Multiple agents (people, teams, companies, AI agents) interact and their choices affect each other's outcomes
- Incentive misalignment is suspected — the system should work but doesn't because participants optimize locally
- Designing rules, protocols, scoring systems, or allocation mechanisms
- Cooperation is needed but not happening (or is fragile)
- Negotiation strategy is being planned
- Multi-agent AI systems are being designed, debugged, or evaluated
- A "tragedy of the commons" pattern is observed (shared resources degrading)
- Someone asks "why would they do X?" where X seems irrational — it's probably rational given their payoffs

---

## The Core Process

### Step 1: Define the Game

Every strategic interaction has these components. Identify each explicitly before analyzing:

**Players**: Who are the decision-making agents? (Don't just list teams — identify the actual decision-makers whose choices matter.)

**Strategies**: What are each player's available actions? Be precise — "cooperate" and "defect" are archetypes, but real strategies are concrete: "share full context," "hoard information," "invest in quality," "ship fast and cut corners," "match competitor's price," "undercut."

**Payoffs**: What does each player gain or lose for each combination of strategies? This is where most analyses fail — people skip quantifying (even roughly) what's at stake. Map the payoff structure even if approximate.

**Information**: What does each player know about the other players' strategies, payoffs, and past actions? Information asymmetry fundamentally changes the game.

**Timing**: Are moves simultaneous or sequential? One-shot or repeated? Finite or indefinite horizon?

### Step 2: Classify the Game Type

Identify which archetype(s) best fit the situation:

| Game type | Structure | Real-world pattern |
|-----------|-----------|-------------------|
| **Prisoner's Dilemma** | Individual rationality → collective harm | Code quality shortcuts, context hoarding, tech debt accumulation, arms races |
| **Coordination Game** | Multiple good equilibria, risk of miscoordination | Standard adoption, API design, team conventions, migration timing |
| **Chicken / Hawk-Dove** | Mutual aggression = worst outcome | Deadline negotiations, resource contention, who blinks first |
| **Stag Hunt** | High reward requires trust; safe option exists | Ambitious refactors, adopting new tools as a team, investing in shared infrastructure |
| **Public Goods / Commons** | Contributing benefits all, but free-riding tempts each | Shared documentation, code reviews, context enrichment, open-source contribution |
| **Auction / Allocation** | Scarce resources, competing claims | Token budget distribution, context window allocation, CI pipeline priority |
| **Principal-Agent** | One party acts on behalf of another with different incentives | Manager-engineer, company-contractor, user-AI agent delegation |
| **Signaling Game** | One party has private info, the other observes actions | Job interviews, PR descriptions, agent confidence reporting, status updates |
| **Bargaining / Negotiation** | Surplus to divide, disagreement point exists | Salary negotiation, scope negotiation, resource sharing between teams |

### Step 3: Find the Equilibrium

Ask: **If every player optimizes for their own payoff, what's the stable outcome?**

- **Dominant strategy**: Does any player have a strategy that's best regardless of what others do? If so, predict they'll play it.
- **Nash Equilibrium**: Is there a strategy profile where no player can improve by unilaterally changing? There may be multiple — identify all of them.
- **Pareto optimality**: Is the equilibrium also the best collective outcome? If not, there's a **social dilemma** — the game's structure is producing a suboptimal result.
- **Mixed strategies**: If there's no pure equilibrium, players may randomize. This shows up as unpredictable or oscillating behavior in practice.

**The critical diagnostic**: If the Nash Equilibrium ≠ Pareto Optimum, the game is broken by design. No amount of persuasion or "alignment" fixes it — the rules must change.

### Step 4: Analyze Dynamics (for Repeated Games)

If the interaction repeats over time:

- **Shadow of the future**: How much do players value future interactions? Higher value → more cooperation. Finite known endpoints kill cooperation (backward induction).
- **Reputation effects**: Can players build and observe reputations? Reputation is the enforcement mechanism in repeated games.
- **Tit-for-tat dynamics**: Does the system support reciprocity? Can defection be detected and punished? Can cooperation be rewarded?
- **Equilibrium selection**: In repeated games, many equilibria exist (Folk Theorem). The question shifts from "what's the equilibrium?" to "which equilibrium does the system select for?" — and that depends on norms, history, and focal points.

### Step 5: Design the Mechanism (if you can change the rules)

If you have power to redesign the game, apply **mechanism design** — reverse game theory:

**Goal**: Define the outcome you want (efficiency, fairness, truthfulness, cooperation).

**Lever 1 — Change the payoffs**: Make cooperation pay more or defection cost more. Bonuses for shared context, penalties for hoarded information, rewards tied to collective outcomes.

**Lever 2 — Change the information structure**: Make actions observable. Transparency kills many defection strategies. Dashboards, audit trails, public commits, shared kanban boards.

**Lever 3 — Change the timing**: Sequential moves with commitment change equilibria. Letting one player move first (and commit visibly) can break coordination deadlocks.

**Lever 4 — Change the rules**: Introduce enforcement (automated checks, reviews), create contracts (SLAs, definitions of done), or restructure who plays with whom (team composition, agent topology).

**Lever 5 — Eliminate the game**: Sometimes the best mechanism design is making the strategic interaction disappear. Centralize the decision, automate the allocation, or remove the resource contention entirely. Your kanban-as-truth architecture does this — it eliminates the context-hoarding game by making externalization the only path forward.

**Key mechanism design properties to aim for**:
- **Incentive compatibility**: Truth-telling and cooperation are the dominant strategy, not just one option
- **Individual rationality**: Every player is better off participating than not
- **Budget balance**: The mechanism doesn't require external subsidy to run
- **Robustness**: The mechanism works even if players are strategic, not just when they're cooperative

---

## Multi-Agent AI Applications

Game theory is especially critical when designing AI agent systems:

**Context as a strategic resource**: When agents share a token budget or context window, allocation is a game. An agent that claims more context may perform better individually but degrades the system. Design allocation mechanisms, not just budgets.

**Agent negotiation protocols**: When agents must agree (on a plan, an API contract, a code design), the negotiation protocol determines the outcome. Poorly designed protocols produce deadlocks, oscillation, or convergence on mediocre solutions.

**Scoring and evaluation as incentive design**: The metric you score agents on IS the incentive function. If you score on speed, agents sacrifice quality. If you score on coverage, agents pad output. Goodhart's Law is a game-theoretic prediction: agents optimize for the metric, not the goal behind the metric.

**Cooperative vs. competitive agent topologies**: A pipeline (sequential agents) creates a principal-agent chain. A committee (parallel agents voting) creates a coordination game. A debate (adversarial agents) creates a zero-sum game. The topology choice IS a game design choice.

**Emergent equilibria in agent loops**: When agents interact repeatedly (iterative refinement, review cycles), they can converge on locally stable but globally suboptimal patterns — a bad equilibrium. Detecting this requires monitoring for convergence without improvement.

---

## Output Format

Structure the analysis as follows:

### 🎮 Game Definition
- **Players**: [List with their roles and decision authority]
- **Strategies**: [Available actions per player]
- **Payoffs**: [What each player gains/loses — use a matrix for 2-player games]
- **Information**: [Who knows what, and when]
- **Timing**: [Simultaneous/sequential, one-shot/repeated]

### 🏷️ Game Classification
- **Type**: [Prisoner's Dilemma / Coordination / Stag Hunt / etc.]
- **Why**: [What structural feature maps to this archetype]

### ⚖️ Equilibrium Analysis
- **Nash Equilibrium**: [The stable outcome under self-interested play]
- **Pareto Optimum**: [The best collective outcome]
- **Gap**: [If these differ — the core problem to solve]
- **Dynamics**: [For repeated games — cooperation sustainability, reputation effects]

### 🔧 Mechanism Design Recommendations
- [Ranked interventions — which lever to pull and why]
- [For each: what changes, what new equilibrium emerges, what could go wrong]
- [Flag perverse incentives the mechanism might create]

### ⚠️ Strategic Risks
- What happens if a player discovers an exploit in the mechanism?
- Where might coalitions form to game the system?
- What information asymmetry could be weaponized?

---

## Thinking Triggers

- *"Why would a rational agent NOT cooperate here?"* — find the defection incentive
- *"What game are they actually playing?"* — the stated game and the real game often differ
- *"If I were optimizing selfishly, what would I do?"* — reveals the equilibrium
- *"Can I make the desired behavior also the self-interested behavior?"* — the mechanism design question
- *"What information would change the equilibrium?"* — transparency as a design lever
- *"Is this a one-shot game or repeated? Does the end date matter?"* — finite vs. infinite horizon changes everything
- *"Who's the residual claimant?"* — who bears the cost of bad outcomes? That's who has the incentive to fix things

---

## Interaction with Other Skills

- **systems-thinking**: Maps dynamics and feedback loops. Game theory adds strategic agency — systems thinking shows *how* the system behaves; game theory shows *why* rational agents make it behave that way.
- **stakeholder-power-mapping**: Identifies the players and their influence. Game theory formalizes what those players will *do* given their incentives.
- **second-order-thinking**: Traces consequence chains. Game theory adds strategic anticipation — "what will they do in response to what I do in response to what they do?"
- **theory-of-constraints**: Identifies the bottleneck. Game theory asks whether the bottleneck persists because someone benefits from it.
- **mechanism design is the constructive application**: Other skills diagnose. Game theory both diagnoses *and* designs — it's the only skill that lets you engineer incentive-compatible rules.

---

## Example Application Triggers

- "Our agents keep converging on mediocre solutions" → identify the equilibrium, check if the scoring function creates a Prisoner's Dilemma where safe-but-mediocre is dominant
- "Nobody contributes to shared documentation" → Public Goods game, design contribution incentives or make non-contribution visible
- "Two teams can't agree on the API contract" → Bargaining game with outside options, identify the disagreement point and design a fair division
- "How should we allocate context window across agents?" → Auction/allocation mechanism, design for truthful reporting of agent needs
- "Why does the Copilot auto-review keep getting gamed?" → Principal-Agent problem with information asymmetry, agents know more about code than the review metric captures
- "We set up a great process but nobody follows it" → Check if following the process is a dominant strategy. If not, the process design is the bug.
