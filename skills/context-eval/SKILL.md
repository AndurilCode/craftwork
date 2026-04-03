---
name: context-eval
description: Evaluate whether a context engineering harness actually improves agent outcomes. Use when the user wants to measure, benchmark, compare, or validate any context artifact — rules, instructions, guidelines, docs, retrieval pipelines, tool setups. Triggers on "does this context help?", "benchmark my context", "evaluate my prompt", "A/B test my context", "is this worth the tokens?", "eval my context", or when someone wants empirical evidence their context engineering produces better outcomes than baseline.
---

# Context Eval

Evaluate whether context engineering artifacts actually improve agent outcomes.

Every context harness costs tokens and claims to produce better results. This skill answers: **does it?** Run the same tasks with and without the context, grade the outputs, measure the delta. If no measurable improvement, it's token tourism.

## The Eval Loop

```
1. Define what you're evaluating (the harness)
2. Write 3-5 realistic task prompts
3. Define success criteria (assertions)
4. Run tasks WITH and WITHOUT the harness (you MUST actually run them — see Step 4)
5. Grade both against assertions
6. Compare: did the harness help?
7. If iterating: modify the harness, repeat from step 4
```

**Use tasks to track progress.** Create a task for each step and update status as you go — this eval is multi-step and task tracking prevents skipping steps or losing track.

## Companion Files

All files are in the same directory as this SKILL.md. Verify these exist before starting:

| File | Purpose | Used in |
|------|---------|---------|
| `grader.md` | Grading protocol | Step 5 |
| `schemas.md` | JSON schemas for eval artifacts | Steps 2-6 |
| `generate_report.py` | Generates eval report with verdict | Step 6 |
| `aggregate_benchmark.py` | Aggregates grading results | Step 7 |
| `estimate_tokens.py` | Estimates harness token cost | Step 1 |
| `generate_viewer.py` | HTML viewer (server or static mode) | Step 7 |
| `comparator.md` | Blind comparison agent | Step 8 |
| `analyzer.md` | Impact analysis agent | Step 8 |
| `anti-patterns.md` | Extended anti-pattern guide with metric signatures | Step 5 |
| `optimize_harness.py` | Automated harness optimization loop (requires LLM CLI) | Step 8 |

If any are missing, the skill still works manually — scripts automate Steps 5-7.

---

## Step 1: Define the Harness Under Test

Read the artifact and characterize it:

1. **What is it?** Format, structure, delivery mechanism. Don't assume — read it.
2. **What does it claim to do?** Expected behavior improvement.
3. **What tasks should benefit?** Target domain.
4. **What's the baseline?** Agent without this context.
5. **What does it cost?** Use `estimate_tokens.py`.

Assess: **Specificity** (precise vs. vague), **Actionability** (what to do vs. what to know), **Freshness** (current vs. stale). Record harness type as a descriptive string (e.g., "project coding guidelines").

## Step 2: Write Eval Prompts

Create 3-5 realistic task prompts the harness should help with. Requirements:
- **Realistic**: messy phrasing, personal context, specifics (not "Write a document")
- **Diverse**: covering different aspects of the harness's claims
- **Challenging**: trivial tasks won't differentiate

Save to `evals/evals.json` — see `schemas.md` for the full schema. Each eval has: `id`, `prompt`, `expected_output`, `files`, `assertions`.

Present prompts to the user for review before proceeding.

## Step 3: Define Assertions

Draft assertions for each eval across three dimensions:

- **Outcome**: Did the output meet the bar? ("includes the retry schedule", "handles the edge case")
- **Precision**: Did context make the agent more precise? ("didn't hallucinate endpoints", "used correct terminology")
- **Efficiency**: Did context reduce waste? ("didn't ask clarifying questions for info in harness", "fewer tool calls")

Update `evals/evals.json`. Explain each assertion to the user.

## Step 4: Run the Evaluations

**You MUST actually run the evals, not just reason about them.** Post-hoc analysis is rationalization, not evaluation.

### Determine eval mode

**Repo-specific harness** (coding guidelines, project docs): Subagents work within the real codebase — one with harness loaded, one without.

**Methodology harness** (skills, reasoning frameworks): Synthesize realistic scenarios. Dispatch subagents that role-play the scenario. **CRITICAL**: Do not reuse prior conversation outputs — fresh, independent outputs only.

### Running with subagents (default)

For each eval, launch a pair:

- **Without-harness**: receives scenario prompt only. Instruction: "Respond to this scenario as you naturally would. Describe your approach step by step."
- **With-harness**: receives harness content + scenario prompt. Instruction: "You have access to the following skill/methodology. Follow it if applicable. Respond step by step."

Launch pairs in parallel. Save to workspace:
```
workspace/iteration-N/eval-{id}-{name}/with_harness/outputs/
workspace/iteration-N/eval-{id}-{name}/without_harness/outputs/
workspace/iteration-N/eval-{id}-{name}/eval_metadata.json
```

The `eval_metadata.json` contains: `eval_id`, `eval_name`, `prompt`, `harness_path`, `assertions`. See `schemas.md`.

### Fallback (no subagents)

Run sequentially: without-harness FIRST (before reading the harness — you can't un-know it), then with-harness. **Flag this limitation in the report** — it's significantly weaker.

### Metrics

Record `timing.json` per run: `total_tokens`, `duration_ms`, `total_duration_seconds`, `configuration`. Capture immediately — this data may not persist.

## Step 5: Grade the Results

**Read `grader.md` first** — it defines the full grading protocol.

For each assertion, grade BOTH outputs:
- **PASS**: Clear evidence — cite it. **FAIL**: No evidence, contradicting, or superficial compliance.
- Default to FAIL when uncertain.

Classify **discrimination power** per assertion:
- **Discriminating**: passes with, fails without → measures harness value
- **Non-discriminating (both pass)**: baseline handles this
- **Non-discriminating (both fail)**: too hard or gap in both
- **Inverse**: passes without, fails with → harness hurting

Save to `grading.json` per eval directory (see `schemas.md`).

**Critique assertions too**: Flag assertions that pass regardless (non-discriminating), important outcomes no assertion covers, and assertions unverifiable from outputs.

## Step 6: Compute the Delta

**Use `generate_report.py`:**
```bash
python3 <this-skill-dir>/generate_report.py \
  workspace/iteration-N \
  --harness-name "my-harness" \
  --harness-type "harness type" \
  --harness-tokens 1500
```

If unavailable, compute manually: `benefit = with_pass_rate - without_pass_rate`, `efficiency = mean_benefit / (token_cost / 1000)`.

The script generates `context_eval_report.json` with metadata, per-condition pass rates (mean/stddev), delta, per-eval breakdown, and diagnosis. See `schemas.md` for the full schema.

### Verdict Thresholds

| Verdict | Condition |
|---|---|
| **EFFECTIVE** | mean_benefit ≥ 0.25 AND majority of evals improve |
| **MARGINAL** | 0.05 ≤ mean_benefit < 0.25 OR inconsistent improvement |
| **INEFFECTIVE** | mean_benefit < 0.05 |
| **HARMFUL** | mean_benefit < 0 (more common than expected) |

Adjust for domain — 10% in safety-critical may be worth more than 30% in convenience.

## Step 7: Present Results

Show: headline ("Your [harness] improved pass rates by X% at Y tokens/invocation"), per-eval breakdown, diagnosis (verdict + reasoning + recommendations), and raw outputs for qualitative review.

### Generate the viewer

```bash
python3 <this-skill-dir>/aggregate_benchmark.py workspace/iteration-N --harness-name "my-harness" --harness-tokens 1500
python3 <this-skill-dir>/generate_report.py workspace/iteration-N --harness-name "my-harness" --harness-type "type" --harness-tokens 1500
python3 <this-skill-dir>/generate_viewer.py workspace/iteration-N --harness-name "my-harness"  # add --static report.html for headless
```

If no filesystem viewer available, present results directly in conversation.

## Step 8: Iterate (Optional)

If improving the harness:
1. Analyze failed with-harness assertions (weak spots) and non-discriminating assertions (no value)
2. Read the harness — identify what's missing, vague, or counterproductive
3. Suggest specific edits, rerun into `iteration-N+1/`, compare

### Blind Comparison (optional, requires subagents)

For rigorous comparison: randomly assign with/without outputs as "A"/"B", spawn a comparator (reads `comparator.md`) that judges without knowing which used the harness. Then spawn an analyzer (reads `analyzer.md`) that unblinds and maps section-level harness impact. Adds a **Context Signal** rubric for domain terminology, specificity, and edge case handling.

Use when: assertion-based eval isn't sufficient, you need to understand *why* the harness helped, or presenting evidence to stakeholders.

### Automated Optimization (optional, requires LLM CLI)

```bash
python3 <this-skill-dir>/optimize_harness.py \
  --harness /path/to/harness --evals /path/to/evals.json \
  --workspace /path/to/optimize-workspace --max-iterations 5 \
  --llm-cmd "your-llm-cli --prompt"
```

Proposes ONE section-level modification per iteration (prune/rewrite/expand/add), applies to a copy, saves for re-evaluation. Without LLM CLI, saves prompts for manual application.

Workflow: eval → diagnose → optimize → re-eval → repeat until EFFECTIVE or benefit stabilizes.

---

## Anti-Patterns to Flag

See `anti-patterns.md` for the extended guide with metric signatures.

| Anti-Pattern | Signal | Fix |
|---|---|---|
| **Token Firehose** | With-harness slower, no more accurate | Prune to high-signal content |
| **Stale Context** | Agent follows outdated instructions → wrong outputs | Add freshness management |
| **Vague Guidance** | Agent reads context, doesn't change behavior | Make instructions actionable/imperative |
| **Contradictory Instructions** | High variance in with-harness runs | Resolve contradictions, add priority ordering |
| **Redundant with Training** | No benefit delta on any eval | Focus on proprietary/specific/recent info |
| **Over-Constraining** | With-harness fails on novel tasks baseline handles | Explain *why* not mandate *how* |
