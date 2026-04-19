---
name: red-teaming
description: Apply red teaming whenever the user wants to stress-test a system, plan, architecture, security model, or decision against adversarial conditions — or when they want to find the weakest points before someone else does. Triggers on phrases like "where are the weak points?", "how would someone break this?", "is this secure?", "find the holes in this plan", "play devil's advocate", "what are we not seeing?", "challenge this", "attack this design", "where could this be exploited?", or when the user is about to launch or commit to something significant. Also trigger for any system where trust, security, incentives, or adversarial actors are relevant — don't wait for the user to ask for a red team explicitly.
---

# Red Teaming

**Core principle**: Assume the system will be attacked, gamed, or stressed by an intelligent adversary. Think like the attacker. Find weaknesses before they're exploited.

---

## Red Team Mindset

Actively try to **break** the system, not validate it.

- **Hostile intent** — How would a bad actor abuse this?
- **Assume failure** — Start from "this has failed" — what enabled it?
- **Partial information** — What does the adversary know that defenders don't?
- **Creativity** — Attackers aren't constrained by intended use
- **Asymmetry** — Defenders protect everything; attackers need one opening

---

## Red Team Dimensions

### 1. Technical Attack Surface
- Inputs that could be manipulated
- Assumptions about data validity
- Edge cases, limits, unexpected inputs
- Trust boundaries — can they be crossed?
- Failure under load, partial failure, poisoned input

### 2. Incentive & Game Theory
- Who has incentive to game/subvert this?
- What does the incentive structure actually reward (vs. intends to)?
- Maximum-extraction / minimum-contribution path?
- Collusion risks between actors?

### 3. Process & Human
- Reliance on human judgment, discipline, vigilance
- Social engineering vectors
- Insider acting against the system
- Process ambiguity enabling inconsistent/exploitable behavior

### 4. Assumption Attacks
- What must be true — and what if each is false?
- Information asymmetry between parties
- Dependencies that could be weaponized

### 5. Cascade & Systemic
- Single failure that propagates most widely
- Highest-impact, lowest-effort attack
- What a sophisticated attacker would do that a naive one wouldn't
- Kill chain — sequence to catastrophic failure

---

## Output Format

### Attack Surface Map
- Entry points (inputs, interfaces, dependencies)
- Trust boundaries (one actor's output → another's input)
- High-value targets

### Top Attack Scenarios
For each:
- **Name** | **Actor** (external/insider/automated/accidental) | **Method** | **Impact** (CIA + reputation/financial) | **Likelihood** (L/M/H) | **Current defenses** | **Defense gaps**

### Highest-Risk Findings
Ranked: **(Likelihood × Impact) / Existing Defenses**. Top 3 to fix first.

### Kill Chain Analysis
For the most critical scenario:
```
[Initial access] → [Lateral movement] → [Exploitation] → [Impact]
```
At each step: what stops the attacker? what's missing?

### Hardening Recommendations
For each high-risk finding:
- **Short-term** — reduce exposure now, even imperfectly
- **Long-term** — eliminate or fundamentally reduce the surface
- **Detection** — if prevention fails, how do we know?

---

## Red Team Questions by Domain

### Software / Architecture
- Malformed, empty, enormous, or adversarial input?
- Dependency returns unexpected data or fails silently?
- Two requests race?
- Credential or token leaked?
- Component compromised from within?

### AI / Agent Systems
- Prompt injection in input?
- Context poisoned by a prior step?
- Tool the agent calls is compromised or returns false data?
- Agent asked to act outside intended scope?
- Two agents give conflicting instructions to a third?

### Product / Business
- User extracts value without paying?
- User reverse-engineers to game metrics?
- Competitor copies model and undercuts?
- Key partner defects or changes terms?
- Regulatory conditions change?

### Organization / Process
- Key person leaves?
- Incentives push people to hide info from each other?
- Process followed to the letter but not the spirit?
- Deadline pressure causes safeguards to be skipped?

---

## Levels of Depth

| Level | Description | When |
|-------|-------------|------|
| Opportunistic | Surface checks, low effort | Quick validation, early design |
| Systematic | Full surface enumeration | Pre-launch, major arch changes |
| Adversarial | Deep creative attack — sophisticated threat actor | High-stakes, security-critical |

---

## Asymmetric Paranoia
The red team doesn't need every flaw — it needs **the one that matters most**. Always prioritize: *highest-impact attack that currently has no defense*.
