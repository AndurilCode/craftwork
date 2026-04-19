---
name: context-engineering-orchestrator
description: Entry point for context engineering work. Routes to the right skill based on what the user needs — creating instructions, debugging agent failures, building documentation, or measuring outcomes. Use this when the user's goal involves agent context but they haven't named a specific skill.
---

# Context Engineering Orchestrator

**This skill routes — it does not reason.** Read the user's intent, match it to an entry point below, then execute that skill's SKILL.md.

---

## Step 1 — Match the User's Intent

Read what the user wants to do and match it to the closest entry below. If ambiguous, ask one clarifying question.

| User wants to... | Start with | Then |
|---|---|---|
| Find what context is missing from a codebase | `context-gap-analyzer` | → `agent-instruction-forge` if gaps need rules |
| Create or improve agent instruction files (CLAUDE.md, .cursorrules, etc.) | `agent-instruction-forge` | → `rule-quality-evaluator` → `edd` |
| Score or audit existing agent instructions | `rule-quality-evaluator` | → `agent-instruction-forge` if score is low |
| Measure whether agent context actually helps | `context-eval` | → `agent-instruction-forge` if regression found |
| Iterate on a context harness with tests | `edd` | → `context-eval` for measurement |
| Design what goes into a context window | `context-cartography` | → `context-gap-analyzer` to validate coverage |
| Debug why an agent is failing / ignoring instructions | `context-debugging` | → `context-gap-analyzer` or `edd` based on findings |
| Extract business logic or domain rules from code | `business-logic-extractor` | → `llms-txt-generator` or `agent-instruction-forge` |
| Process a large document for LLM consumption | `deep-document-processor` | → `llms-txt-generator` |
| Generate an llms.txt or LLM-friendly reference | `llms-txt-generator` | → `context-compressor` if over budget |
| Optimize / compress context to fit a token budget | `context-compressor` | → `context-eval` to verify compressed context works |
| Find false positives in AI-generated tests | `test-challenger` | → `edd` if better assertions needed |

---

## Step 2 — Execute

1. Read `skills/[skill-name]/SKILL.md`
2. Apply that skill's full methodology
3. On completion, check the "Then" column for follow-ups

## Step 3 — Propose Next Steps

Do NOT auto-execute the "Then" skill. Propose it:

```
Based on [what the skill produced], a natural next step would be:
→ [skill-name]: [1-sentence reason]

Want me to continue with that, or is this what you needed?
```

Multiple follow-ups → list as options. User chooses; orchestrator never chains automatically.

---

## Canonical Chains

These are the most common multi-skill sequences in this group:

**Full context engineering lifecycle:**
```
context-gap-analyzer → agent-instruction-forge → rule-quality-evaluator → context-eval → edd
```
Use when building agent context from scratch or doing a comprehensive audit.

**Creating agent instructions:**
```
context-gap-analyzer → agent-instruction-forge → rule-quality-evaluator → edd
```
Use when the goal is specifically to create or improve instruction files.

**Debugging agent failures:**
```
context-debugging → context-gap-analyzer → agent-instruction-forge → edd
```
Use when an agent is behaving incorrectly and you suspect the context layer.

**Building documentation:**
```
business-logic-extractor → llms-txt-generator
deep-document-processor → llms-txt-generator
```
Use when creating LLM-consumable reference material.

---

## Skill Registry

| Skill | Purpose |
|-------|---------|
| `context-gap-analyzer` | Find implicit context missing from a codebase |
| `agent-instruction-forge` | Create instruction rules for coding agents |
| `rule-quality-evaluator` | Score rules on Seven Properties, detect redundancies |
| `context-cartography` | Design what goes into an agent's context window |
| `context-debugging` | Diagnose agent failures originating in the context layer |
| `context-eval` | Measure whether context changes improve outcomes |
| `edd` | Eval-Driven Development — TDD for context |
| `llms-txt-generator` | Generate token-efficient context documents |
| `deep-document-processor` | Multi-pass reading of large documents |
| `business-logic-extractor` | Extract domain rules from code |
| `context-compressor` | Maximize signal-per-token under a finite budget |
| `test-challenger` | Find false positives in AI-generated tests |
