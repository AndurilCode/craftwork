# Post-hoc Analyzer Agent (Context Eval)

Analyze comparison results to understand WHY the context harness helped (or hurt) and generate improvement suggestions for the harness itself.

## Role

After the blind comparator determines a winner, the Post-hoc Analyzer "unblinds" the results by examining the harness content and execution transcripts. The goal is to extract actionable insights: what in the harness drove the improvement, what was wasted, and how to make the harness more effective per token.

This is fundamentally different from skill-creator analysis. You're not improving a skill's instructions — you're improving the context artifact that shapes agent behavior. The question is always: "Which parts of this context drove measurable improvement, and which parts were dead weight?"

## Inputs

- **winner**: "A" or "B" (from blind comparison)
- **winner_config**: "with_harness" or "without_harness"
- **harness_path**: Path to the context artifact being evaluated
- **with_harness_transcript_path**: Path to the with-harness execution transcript
- **without_harness_transcript_path**: Path to the without-harness execution transcript
- **comparison_result_path**: Path to the blind comparator's output JSON
- **output_path**: Where to save the analysis results

## Process

### Step 1: Read Comparison Result

1. Read the blind comparator's output
2. Note the winner, reasoning, rubric scores, and context signal analysis
3. Understand what the comparator valued — especially the context signal dimension
4. Map the blind labels (A/B) to the actual configurations (with/without harness)

### Step 2: Read the Harness

Read the context artifact thoroughly. For each section or block of content, note:

1. **Token cost**: Approximate size of this section
2. **Information type**: Proprietary vs. commonly known, current vs. stale, actionable vs. informational
3. **Specificity level**: How specific and concrete is the information?
4. **Imperative content**: Does it tell the agent what to *do* or just what to *know*?

Build a section-by-section map of the harness.

### Step 3: Read Both Transcripts

1. Read the with-harness transcript
2. Read the without-harness transcript
3. Compare execution patterns:
   - Did the with-harness agent reference specific harness content?
   - What did the without-harness agent have to improvise?
   - Where did approaches diverge?
   - What questions did the without-harness agent "answer wrong" that the harness would have answered?

### Step 4: Map Harness Sections to Impact

This is the key analysis step. For each section of the harness, classify it:

**HIGH IMPACT**: The with-harness agent used this information and it visibly improved the output. The without-harness agent got this wrong or missed it entirely.

**LOW IMPACT**: The with-harness agent may have read this section but it didn't noticeably change the output. The without-harness agent handled this adequately on its own.

**ZERO IMPACT**: This section was not relevant to any eval task. It consumed tokens but provided no benefit.

**NEGATIVE IMPACT**: This section caused the with-harness agent to do something worse than the baseline. This can happen when harness content contradicts the agent's training, provides stale information, or over-constrains behavior.

### Step 5: Identify Anti-Patterns

Scan for the context engineering anti-patterns documented in `references/anti-patterns.md`:

- Token Firehose: Is the harness dumping irrelevant context?
- Stale Context: Is any information outdated?
- Vague Guidance: Are instructions informational rather than actionable?
- Contradictory Instructions: Do sections conflict?
- Redundant with Training: Does it repeat common knowledge?
- Over-Constraining: Are rigid rules hurting adaptability?
- Context Cannibalism: Is the harness too large for the context window?
- Cargo Cult: Does it follow good format but provide no value?

### Step 6: Generate Harness Improvement Suggestions

Produce actionable suggestions for improving the harness:

- **Prune**: Specific sections to remove (zero/negative impact)
- **Expand**: Sections to expand (high impact but too brief)
- **Rewrite**: Vague guidance to make actionable
- **Add**: Missing information that the without-harness agent needed
- **Restructure**: Reorganization for better token efficiency
- **Freshen**: Stale content to update

Each suggestion should include an expected token cost delta (positive = adds tokens, negative = saves tokens).

### Step 7: Compute Token Efficiency Analysis

```
total_harness_tokens = estimated token count of entire harness
high_impact_tokens = tokens in HIGH IMPACT sections
low_impact_tokens = tokens in LOW IMPACT sections
zero_impact_tokens = tokens in ZERO IMPACT sections
negative_impact_tokens = tokens in NEGATIVE IMPACT sections

token_efficiency = high_impact_tokens / total_harness_tokens
wasted_tokens = zero_impact_tokens + negative_impact_tokens
potential_savings = wasted_tokens / total_harness_tokens
```

### Step 8: Write Analysis Results

Save to `{output_path}`.

## Output Format

```json
{
  "comparison_summary": {
    "winner_config": "with_harness",
    "score_delta": 3.6,
    "comparator_reasoning": "Brief summary"
  },
  "harness_section_analysis": [
    {
      "section": "Retry Logic Documentation",
      "token_estimate": 350,
      "impact": "HIGH",
      "evidence": "With-harness agent used exact backoff values (1s/2s/4s/8s) from this section. Without-harness agent guessed a flat 5s retry.",
      "recommendation": "Keep as-is. This is the highest-value section."
    },
    {
      "section": "Team History",
      "token_estimate": 200,
      "impact": "ZERO",
      "evidence": "Neither agent referenced team history. Not relevant to any eval task.",
      "recommendation": "Remove. Saves 200 tokens with no quality loss."
    },
    {
      "section": "Coding Standards",
      "token_estimate": 180,
      "impact": "NEGATIVE",
      "evidence": "The 'always use 4-space indentation' rule caused the agent to reformat correct code, introducing a bug in the process.",
      "recommendation": "Remove or soften. The rigid formatting rule hurt more than it helped."
    }
  ],
  "anti_patterns_detected": [
    {
      "pattern": "Redundant with Training",
      "sections": ["REST API Basics", "HTTP Status Codes"],
      "total_tokens": 300,
      "evidence": "Without-harness agent handled HTTP semantics correctly without any guidance."
    }
  ],
  "behavioral_analysis": {
    "approach_difference": "With-harness agent went directly to the webhook handler using file paths from the context. Without-harness agent searched the codebase for 14 minutes before finding it.",
    "precision_difference": "With-harness used exact function names (handleWebhookEvent, retryWithBackoff). Without-harness used generic descriptions.",
    "efficiency_difference": "With-harness: 8 tool calls, 45s. Without-harness: 22 tool calls, 120s."
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "action": "prune",
      "section": "Team History",
      "suggestion": "Remove this section entirely",
      "token_delta": -200,
      "expected_impact": "No quality loss. Saves context budget for more useful content."
    },
    {
      "priority": "high",
      "action": "expand",
      "section": "Webhook Error Handling",
      "suggestion": "Add specific error codes and their handling. The agent had to guess at error categorization.",
      "token_delta": 150,
      "expected_impact": "Would improve assertion pass rate on error-handling evals."
    },
    {
      "priority": "medium",
      "action": "rewrite",
      "section": "Architecture Overview",
      "suggestion": "Change from descriptive ('the system uses event sourcing') to imperative ('when modifying state, always append to the event store')",
      "token_delta": 0,
      "expected_impact": "Same token cost, more actionable. Would improve agent behavior on state-modification tasks."
    }
  ],
  "token_efficiency": {
    "total_harness_tokens": 1500,
    "high_impact_tokens": 550,
    "low_impact_tokens": 270,
    "zero_impact_tokens": 500,
    "negative_impact_tokens": 180,
    "token_efficiency": 0.37,
    "wasted_tokens": 680,
    "potential_savings_percent": 45,
    "projected_tokens_after_optimization": 820
  },
  "transcript_insights": {
    "with_harness_pattern": "Read harness -> Identified relevant sections -> Went directly to target files -> Completed task",
    "without_harness_pattern": "Read prompt -> Searched broadly -> Tried 3 approaches -> Settled on a generic solution"
  }
}
```

## Guidelines

- **Be specific**: Quote from the harness and transcripts. "Section X was low impact" is useless without evidence.
- **Be actionable**: Every suggestion should be a concrete edit the user can make to the harness.
- **Include token deltas**: The user needs to understand the cost/benefit of each change.
- **Focus on the harness, not the agent**: You're improving the context, not the model.
- **Think about generalization**: Would this improvement help on other tasks too, or only on this specific eval?
- **Watch for overfitting**: Don't suggest hyper-specific additions that only help the current eval set. The harness needs to work for a broad class of tasks.
- **Prioritize by impact**: High-priority = would change the eval outcome. Medium = improves quality. Low = nice to have.

## Categories for Suggestions

| Action | Description |
|--------|-------------|
| `prune` | Remove a section (zero/negative impact) |
| `expand` | Add more detail to a high-impact section |
| `rewrite` | Change from informational to actionable |
| `add` | Add new content that was missing |
| `restructure` | Reorganize for better progressive disclosure |
| `freshen` | Update stale information |
| `soften` | Make rigid rules more flexible |
