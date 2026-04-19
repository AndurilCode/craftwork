---
name: context-eval
description: Evaluate whether a context engineering harness actually improves agent outcomes. Use when the user wants to measure, benchmark, compare, or validate any context artifact — rules, instructions, guidelines, docs, retrieval pipelines, tool setups. Triggers on "does this context help?", "benchmark my context", "evaluate my prompt", "A/B test my context", "is this worth the tokens?", "eval my context", or when someone wants empirical evidence their context engineering produces better outcomes than baseline.
---

# Context Eval

Run the same tasks with and without the harness, grade outputs, measure the delta. No measurable improvement → token tourism.

## The Eval Loop

```
1. Define what you're evaluating (the harness)
2. Write 3-5 realistic task prompts
3. Define success criteria (assertions)
4. Run tasks WITH and WITHOUT (you MUST actually run — see Step 4)
5. Grade both against assertions
6. Compare: did the harness help?
7. If iterating: modify, repeat from step 4
```

**Use tasks to track progress** — multi-step; tracking prevents skipping.

## Companion Files

In the same directory as this SKILL.md:

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

If missing, the skill works manually — scripts automate Steps 5-7.

---

## Step 1: Define the Harness Under Test

1. **What is it?** Format, structure, delivery. Read it.
2. **What does it claim to do?**
3. **What tasks should benefit?**
4. **What's the baseline?** Agent without this context.
5. **What does it cost?** Use `estimate_tokens.py`.

Assess **Specificity**, **Actionability**, **Freshness**. Record harness type as a descriptive string (e.g., "project coding guidelines").

## Step 2: Write Eval Prompts

3-5 realistic prompts:
- **Realistic**: messy phrasing, personal context, specifics
- **Diverse**: covering different aspects of the harness's claims
- **Challenging**: trivial tasks won't differentiate

Save to `evals/evals.json` (see `schemas.md`). Each eval: `id`, `prompt`, `expected_output`, `files`, `assertions`. Present prompts to user before proceeding.

## Step 3: Define Assertions

Three dimensions per eval:

- **Outcome**: Did output meet the bar? ("includes the retry schedule")
- **Precision**: More precise? ("didn't hallucinate endpoints", "correct terminology")
- **Efficiency**: Less waste? ("didn't ask clarifying questions for info in harness", "fewer tool calls")

Update `evals/evals.json`. Explain each assertion to the user.

## Step 4: Run the Evaluations

**You MUST actually run them.** Post-hoc analysis is rationalization, not evaluation.

### Determine eval mode

**Repo-specific harness** (coding guidelines, project docs): subagents in real codebase — one with harness, one without.

**Methodology harness** (skills, frameworks): synthesize realistic scenarios; subagents role-play. **CRITICAL**: do not reuse prior conversation outputs — fresh, independent only.

### Running with subagents (default)

Per eval, launch a pair:

- **Without-harness**: scenario only. "Respond as you naturally would. Describe your approach step by step."
- **With-harness**: harness + scenario. "You have access to the following skill/methodology. Follow it if applicable. Respond step by step."

Launch in parallel. Save to:
```
workspace/iteration-N/eval-{id}-{name}/with_harness/outputs/
workspace/iteration-N/eval-{id}-{name}/without_harness/outputs/
workspace/iteration-N/eval-{id}-{name}/eval_metadata.json
```

`eval_metadata.json` contains: `eval_id`, `eval_name`, `prompt`, `harness_path`, `assertions`. See `schemas.md`.

### Fallback (no subagents)

Sequentially: without-harness FIRST (before reading harness — you can't un-know it), then with-harness. **Flag this in the report** — significantly weaker.

### Metrics

Record `timing.json` per run: `total_tokens`, `duration_ms`, `total_duration_seconds`, `configuration`. Capture immediately — may not persist.

## Step 5: Grade the Results

**Read `grader.md` first.**

Per assertion, grade BOTH outputs:
- **PASS**: cite evidence. **FAIL**: no evidence, contradicting, or superficial compliance.
- Default FAIL when uncertain.

Classify **discrimination power**:
- **Discriminating**: passes with, fails without → measures harness value
- **Non-discriminating (both pass)**: baseline handles this
- **Non-discriminating (both fail)**: too hard or gap in both
- **Inverse**: passes without, fails with → harness hurting

Save `grading.json` per eval directory (see `schemas.md`).

**Critique assertions too**: flag non-discriminating, missing important outcomes, or unverifiable from outputs.

## Step 6: Compute the Delta

```bash
python3 <this-skill-dir>/generate_report.py \
  workspace/iteration-N \
  --harness-name "my-harness" \
  --harness-type "harness type" \
  --harness-tokens 1500
```

Manual: `benefit = with_pass_rate - without_pass_rate`, `efficiency = mean_benefit / (token_cost / 1000)`.

Generates `context_eval_report.json` with metadata, per-condition pass rates (mean/stddev), delta, per-eval breakdown, diagnosis. See `schemas.md`.

### Verdict Thresholds

| Verdict | Condition |
|---|---|
| **EFFECTIVE** | mean_benefit ≥ 0.25 AND majority of evals improve |
| **MARGINAL** | 0.05 ≤ mean_benefit < 0.25 OR inconsistent improvement |
| **INEFFECTIVE** | mean_benefit < 0.05 |
| **HARMFUL** | mean_benefit < 0 (more common than expected) |

Adjust for domain — 10% in safety-critical may be worth more than 30% in convenience.

## Step 7: Present Results

Headline ("Your [harness] improved pass rates by X% at Y tokens/invocation"), per-eval breakdown, diagnosis (verdict + reasoning + recommendations), raw outputs for qualitative review.

### Generate the viewer

```bash
python3 <this-skill-dir>/aggregate_benchmark.py workspace/iteration-N --harness-name "my-harness" --harness-tokens 1500
python3 <this-skill-dir>/generate_report.py workspace/iteration-N --harness-name "my-harness" --harness-type "type" --harness-tokens 1500
python3 <this-skill-dir>/generate_viewer.py workspace/iteration-N --harness-name "my-harness"  # add --static report.html for headless
```

If no filesystem viewer, present in conversation.

## Step 8: Iterate (Optional)

1. Analyze failed with-harness assertions (weak spots) and non-discriminating ones (no value)
2. Read harness — identify missing, vague, counterproductive content
3. Suggest edits, rerun into `iteration-N+1/`, compare

### Blind Comparison (optional, requires subagents)

Randomly assign with/without outputs as "A"/"B"; spawn comparator (reads `comparator.md`) that judges blind. Then analyzer (reads `analyzer.md`) unblinds and maps section-level impact. Adds **Context Signal** rubric for domain terminology, specificity, edge case handling.

Use when: assertion-based isn't sufficient, need to understand *why*, or presenting to stakeholders.

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
| **Stale Context** | Agent follows outdated instructions | Add freshness management |
| **Vague Guidance** | Agent reads context, doesn't change behavior | Make instructions actionable/imperative |
| **Contradictory Instructions** | High variance in with-harness runs | Resolve contradictions, add priority ordering |
| **Redundant with Training** | No benefit delta on any eval | Focus on proprietary/specific/recent info |
| **Over-Constraining** | With-harness fails on novel tasks baseline handles | Explain *why* not mandate *how* |
