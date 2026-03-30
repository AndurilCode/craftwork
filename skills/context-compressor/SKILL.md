---
name: context-compressor
description: >
  Maximize signal-per-token in agent context windows. Use whenever context is being
  assembled for a task and the question is "what to include, what to cut, and how
  to encode it." Triggers on: "optimize context", "context window too full", "token
  budget", "which files in context?", "rank context by importance", "deduplicate
  context", "context triage", "compress this for the agent", or any curation of
  context under a finite token budget. Also trigger when assembling CLAUDE.md,
  AGENTS.md, .ctx files, system prompts, or skill files and deciding what earns
  its token cost. Unlike summarization (which compresses uniformly for human
  readers), this skill triages context by task-relative information value — scoring
  each fragment's entropy, redundancy, and efficiency, then cutting or compressing
  selectively. If tokens are scarce and context is abundant, always use this skill.
---

# Context Compressor

Finite channel (context window) must carry maximum decision-relevant signal.
Score fragments by entropy and redundancy, cut or compress accordingly.

## Vocabulary

| Info Theory | Context Engineering |
|-------------|-------------------|
| Channel / Capacity | Context window / window minus system prompt overhead |
| Entropy | Information per token |
| Self-information | How much a fragment reduces agent uncertainty |
| Redundancy | Tokens carrying no new info given other context |
| Lossy compression | Summarize at lower fidelity to save tokens |
| Lossless compression | Reformulate more densely, same facts |

## Phase 1 — Budget

Calculate: window - system_prompt - tools - history - output_reserve = **available**.
Compare available vs. candidate context:

| Regime | Ratio | Strategy |
|--------|-------|----------|
| Abundant | >3x | Include all. Stop. |
| Comfortable | 1.5-3x | Cut obvious redundancy |
| Tight | 0.5-1.5x | Active compression |
| Starved | <0.5x | Aggressive triage. Every token justifies itself. |

## Phase 2 — Entropy Scoring

Score every candidate fragment on three dimensions:

**Self-Information** (0-4): 0=derivable from training, 1=agent would guess right,
2=meaningfully reduces uncertainty, 3=changes behavior substantially,
4=without this agent produces wrong output.

**Redundancy**: Unique / Partial overlap / Mostly redundant / Fully redundant.

**Token Efficiency**: Dense / Normal / Bloated / Wasteful.

**Decision rules:**
- Self-Info 0 -> CUT always
- Self-Info 4 -> KEEP always at full fidelity
- Self-Info 1 + Mostly/Fully redundant -> CUT
- Self-Info 2-3 + Bloated -> COMPRESS
- Self-Info 2-3 + Unique + Dense -> KEEP

Output as table: Fragment | Tokens | Self-Info | Redundancy | Efficiency | Action.

## Phase 3 — Compress

**Lossless** (Self-Info 3+, low efficiency):
Telegram rewrite, structure extraction, reference elimination, dedup merge.

**Lossy** (budget Tight/Starved, lossless insufficient):
Fidelity reduction (drop rationale, keep rule), scope narrowing (only task-relevant
subsection), abstraction raising (drop detail, keep default), probabilistic
pruning (cut edge-case-only context, accept risk).

**Always log lossy losses:**
```
Fragment: [name] ([before] -> [after] tokens)
Kept: [what survived]
Lost: [what was cut]
Risk: [what agent may get wrong]
```

## Phase 4 — Assemble & Verify

Order by descending self-information (critical first — attention degrades).

Verify:
- Fits budget? Total tokens <= available.
- Agent could complete task with ONLY this context?
- All Self-Info 4 fragments present at full fidelity?
- Any cut fragment that would change agent behavior?

## Calibration

1. **No task = no compression.** Always audit against a specific task.
2. **80/20.** ~20% of context carries ~80% of signal. Find it, keep it full fidelity.
3. **Compression taxes flexibility.** Leave slack for multi-turn needs.
4. **When in doubt, keep.** Wrong output costs more than extra tokens.
5. **Empirics > theory.** Compare agent output with full vs. compressed context when possible.
