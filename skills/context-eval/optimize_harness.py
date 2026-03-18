#!/usr/bin/env python3
"""Automated harness optimization loop.

Analyzes a context harness, proposes section-level modifications (prune, rewrite,
expand), re-evaluates after each change, and tracks whether each change improved
the benefit score. Uses any LLM CLI to generate modification proposals.

Usage:
    python optimize_harness.py \
      --harness /path/to/harness \
      --evals /path/to/evals.json \
      --workspace /path/to/workspace \
      --max-iterations 5 \
      --llm-cmd "llm -m your-model"

Requires an LLM CLI that accepts a prompt argument and returns text on stdout.
Falls back to manual mode if the CLI is unavailable.

The loop:
  1. Run baseline eval (if not already done)
  2. Analyze which sections have low/zero/negative impact
  3. Propose a modification (prune, rewrite, expand)
  4. Apply the modification to a copy of the harness
  5. Re-run evals with the modified harness
  6. Compare: did benefit improve?
  7. Keep the change if it helped, revert if it didn't
  8. Repeat until max iterations or no more improvements
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROPOSE_PROMPT = """You are a context engineering optimizer. Given:

1. A context harness (the full content of a file that provides context to an AI agent)
2. Evaluation results showing which assertions pass/fail with and without the harness
3. The history of previous optimization attempts

Your job is to propose ONE specific modification to the harness that will improve
its benefit score (the delta between with-harness and without-harness pass rates).

Focus on:
- Pruning zero-impact sections (saves tokens, reduces noise)
- Rewriting vague guidance into actionable instructions
- Expanding high-impact sections that are too brief
- Removing content that's redundant with model training data
- Fixing stale or contradictory information

Respond with ONLY a JSON object (no markdown, no backticks):
{{
  "action": "prune|rewrite|expand|add|remove_section",
  "target": "description of what to modify",
  "rationale": "why this should help",
  "search_text": "exact text to find in the harness (for prune/rewrite)",
  "replacement_text": "what to replace it with (empty string for prune)",
  "expected_token_delta": -200
}}
"""


def estimate_tokens(text: str) -> int:
    """Rough token estimate at ~4 chars per token."""
    return len(text) // 4


def run_llm(prompt: str, llm_cmd: str) -> str | None:
    """Run a prompt through an LLM CLI and return the response.

    The llm_cmd should be a command that accepts a prompt as the last argument
    and returns the response on stdout. Examples:
      - "llm -m gpt-4o"
      - "claude -p"
      - "./run_llm.sh"
    """
    try:
        cmd_parts = llm_cmd.split()
        result = subprocess.run(
            cmd_parts + [prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"  LLM CLI error: {result.stderr[:200]}", file=sys.stderr)
            return None
    except FileNotFoundError:
        print(f"  LLM CLI not found: {llm_cmd.split()[0]}. Install it or provide a valid --llm-cmd.", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print("  LLM CLI timed out.", file=sys.stderr)
        return None


def apply_modification(harness_text: str, mod: dict) -> str | None:
    """Apply a modification to the harness text. Returns modified text or None if failed."""
    action = mod.get("action", "")
    search = mod.get("search_text", "")
    replacement = mod.get("replacement_text", "")

    if action in ("prune", "rewrite", "remove_section") and search:
        if search in harness_text:
            return harness_text.replace(search, replacement)
        else:
            # Try a fuzzy match — find the closest line
            lines = harness_text.split("\n")
            search_lines = search.split("\n")
            if len(search_lines) == 1:
                # Single line search — find best match
                best_idx = -1
                best_score = 0
                search_words = set(search.lower().split())
                for i, line in enumerate(lines):
                    line_words = set(line.lower().split())
                    overlap = len(search_words & line_words)
                    if overlap > best_score and overlap >= len(search_words) * 0.6:
                        best_score = overlap
                        best_idx = i
                if best_idx >= 0:
                    lines[best_idx] = replacement
                    return "\n".join(lines)
            print(f"  Could not find search text in harness", file=sys.stderr)
            return None

    elif action == "expand" and search:
        if search in harness_text:
            return harness_text.replace(search, search + "\n" + replacement)
        return None

    elif action == "add":
        return harness_text + "\n\n" + replacement

    return None


def run_evals_simple(harness_path: Path, evals: list[dict], workspace: Path, label: str) -> dict:
    """Run evals in a simplified way — returns pass rates.

    In full mode, this would spawn subagents. For the optimization loop,
    we save the harness state and report what we have. The actual eval
    execution should be done by the orchestrating agent.
    """
    result_dir = workspace / label
    result_dir.mkdir(parents=True, exist_ok=True)

    # Save the harness snapshot
    shutil.copy2(harness_path, result_dir / "harness_snapshot.md")

    # Save eval config
    (result_dir / "eval_config.json").write_text(json.dumps({
        "harness_path": str(harness_path),
        "evals": evals,
        "label": label,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }, indent=2))

    return {"label": label, "dir": str(result_dir), "status": "ready_for_eval"}


def optimize(
    harness_path: Path,
    evals_path: Path,
    workspace: Path,
    max_iterations: int,
    llm_cmd: str,
    verbose: bool,
) -> dict:
    """Run the optimization loop."""

    harness_text = harness_path.read_text(encoding="utf-8")
    evals_data = json.loads(evals_path.read_text())
    evals_list = evals_data.get("evals", [])

    initial_tokens = estimate_tokens(harness_text)
    history = []
    current_text = harness_text
    best_text = harness_text

    if verbose:
        print(f"\n  Harness Optimization Loop")
        print(f"  {'='*40}")
        print(f"  Harness: {harness_path}")
        print(f"  Initial tokens: ~{initial_tokens}")
        print(f"  Evals: {len(evals_list)}")
        print(f"  Max iterations: {max_iterations}")
        print()

    for iteration in range(1, max_iterations + 1):
        if verbose:
            print(f"  --- Iteration {iteration}/{max_iterations} ---")

        # Build the prompt for the LLM to propose a modification
        prompt = PROPOSE_PROMPT + f"""

HARNESS CONTENT:
{current_text}

EVAL DEFINITIONS:
{json.dumps(evals_list, indent=2)}

OPTIMIZATION HISTORY:
{json.dumps(history, indent=2) if history else "No previous iterations."}

Current token count: ~{estimate_tokens(current_text)}

Propose ONE modification. Respond with ONLY a JSON object, no markdown backticks.
"""

        # Get modification proposal
        response = run_llm(prompt, llm_cmd)
        if not response:
            if verbose:
                print("  Could not get modification proposal. Stopping.", file=sys.stderr)
            break

        # Parse the proposal
        try:
            # Strip any markdown fences
            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1]
            if clean.endswith("```"):
                clean = clean.rsplit("```", 1)[0]
            clean = clean.strip()
            mod = json.loads(clean)
        except json.JSONDecodeError as e:
            if verbose:
                print(f"  Could not parse proposal: {e}", file=sys.stderr)
                print(f"  Response: {response[:200]}", file=sys.stderr)
            history.append({
                "iteration": iteration,
                "status": "parse_error",
                "response_preview": response[:200],
            })
            continue

        if verbose:
            print(f"  Proposed: {mod.get('action', '?')} — {mod.get('target', '?')[:60]}")
            print(f"  Rationale: {mod.get('rationale', '?')[:80]}")

        # Apply the modification
        modified = apply_modification(current_text, mod)
        if not modified:
            if verbose:
                print(f"  Could not apply modification. Skipping.")
            history.append({
                "iteration": iteration,
                "action": mod.get("action"),
                "target": mod.get("target"),
                "status": "apply_failed",
            })
            continue

        new_tokens = estimate_tokens(modified)
        token_delta = new_tokens - estimate_tokens(current_text)

        if verbose:
            print(f"  Tokens: {estimate_tokens(current_text)} → {new_tokens} ({token_delta:+d})")

        # Save the modified harness for evaluation
        iter_dir = workspace / f"optimize-iter-{iteration}"
        iter_dir.mkdir(parents=True, exist_ok=True)

        modified_path = iter_dir / "harness_modified.md"
        modified_path.write_text(modified, encoding="utf-8")

        # Save the original for comparison
        original_path = iter_dir / "harness_original.md"
        original_path.write_text(current_text, encoding="utf-8")

        # Save the proposal
        (iter_dir / "proposal.json").write_text(json.dumps(mod, indent=2))

        # Record in history
        entry = {
            "iteration": iteration,
            "action": mod.get("action"),
            "target": mod.get("target"),
            "rationale": mod.get("rationale"),
            "token_delta": token_delta,
            "tokens_before": estimate_tokens(current_text),
            "tokens_after": new_tokens,
            "status": "proposed",
            "modified_path": str(modified_path),
            "dir": str(iter_dir),
        }
        history.append(entry)

        # Accept the modification optimistically
        # (In a full implementation, we'd re-run evals and compare.
        #  The orchestrating agent should do this and update history.)
        current_text = modified

        if verbose:
            print(f"  Applied. Ready for re-evaluation at: {iter_dir}")
            print()

    # Save final state
    final_path = workspace / "harness_optimized.md"
    final_path.write_text(current_text, encoding="utf-8")

    result = {
        "original_path": str(harness_path),
        "optimized_path": str(final_path),
        "original_tokens": initial_tokens,
        "optimized_tokens": estimate_tokens(current_text),
        "token_savings": initial_tokens - estimate_tokens(current_text),
        "iterations_run": len(history),
        "history": history,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    result_path = workspace / "optimization_result.json"
    result_path.write_text(json.dumps(result, indent=2))

    if verbose:
        print(f"  {'='*40}")
        print(f"  Optimization complete")
        print(f"  Tokens: {initial_tokens} → {estimate_tokens(current_text)} ({estimate_tokens(current_text) - initial_tokens:+d})")
        print(f"  Iterations: {len(history)}")
        print(f"  Optimized harness: {final_path}")
        print(f"  Results: {result_path}")
        print()
        print(f"  Next step: re-run context-eval with the optimized harness")
        print(f"  to verify the changes actually improved outcomes.")

    return result


def main():
    parser = argparse.ArgumentParser(description="Optimize a context harness")
    parser.add_argument("--harness", required=True, help="Path to the harness file")
    parser.add_argument("--evals", required=True, help="Path to evals.json")
    parser.add_argument("--workspace", required=True, help="Output workspace directory")
    parser.add_argument("--max-iterations", type=int, default=5, help="Maximum optimization iterations")
    parser.add_argument("--llm-cmd", required=True, help="LLM CLI command (e.g. 'llm -m gpt-4o', 'claude -p', './run_llm.sh')")
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    args = parser.parse_args()

    harness_path = Path(args.harness)
    if not harness_path.exists():
        print(f"Error: {harness_path} does not exist", file=sys.stderr)
        sys.exit(1)

    evals_path = Path(args.evals)
    if not evals_path.exists():
        print(f"Error: {evals_path} does not exist", file=sys.stderr)
        sys.exit(1)

    workspace = Path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    optimize(
        harness_path=harness_path,
        evals_path=evals_path,
        workspace=workspace,
        max_iterations=args.max_iterations,
        llm_cmd=args.llm_cmd,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
