#!/usr/bin/env python3
"""Aggregate grading results into benchmark.json for the context eval viewer.

Reads grading.json and timing.json from each eval directory in an iteration,
produces benchmark.json compatible with both the context eval viewer and the
skill-creator's viewer format.

Usage:
    python aggregate_benchmark.py <workspace>/iteration-N --harness-name "my-harness" --harness-tokens 1500
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, stdev


def load_json(path: Path) -> dict | None:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return None
    return None


def compute_stats(values: list[float]) -> dict:
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    m = mean(values)
    s = stdev(values) if len(values) > 1 else 0.0
    return {
        "mean": round(m, 3),
        "stddev": round(s, 3),
        "min": round(min(values), 3),
        "max": round(max(values), 3),
    }


def aggregate(iteration_dir: Path, harness_name: str, harness_tokens: int) -> dict:
    runs = []
    with_pass_rates = []
    without_pass_rates = []
    with_times = []
    without_times = []
    with_tokens_list = []
    without_tokens_list = []
    notes = []

    eval_dirs = sorted([
        d for d in iteration_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])

    for eval_dir in eval_dirs:
        meta = load_json(eval_dir / "eval_metadata.json") or {}
        grading = load_json(eval_dir / "grading.json")

        eval_id = meta.get("eval_id", 0)
        eval_name = meta.get("eval_name", eval_dir.name)

        for config in ["with_harness", "without_harness"]:
            run_dir = eval_dir / config
            timing = load_json(run_dir / "timing.json") if run_dir.exists() else None

            # Get pass rate from grading
            if grading:
                summary = grading.get("summary", {})
                config_summary = summary.get(config, {})
                pr = config_summary.get("pass_rate", 0.0)
                passed = config_summary.get("passed", 0)
                failed = summary.get("total", 0) - passed if "total" in summary else config_summary.get("failed", 0)
                total = config_summary.get("total", passed + failed)
            else:
                pr = 0.0
                passed = 0
                total = 0

            time_s = timing.get("total_duration_seconds", 0) if timing else 0
            tokens = timing.get("total_tokens", 0) if timing else 0

            # Get assertion details
            expectations = []
            if grading:
                for a in grading.get("assertions", []):
                    a_config = a.get(config, {})
                    expectations.append({
                        "text": a.get("text", ""),
                        "passed": a_config.get("passed", False),
                        "evidence": a_config.get("evidence", ""),
                    })

            run = {
                "eval_id": eval_id,
                "eval_name": eval_name,
                "configuration": config,
                "run_number": 1,
                "result": {
                    "pass_rate": pr,
                    "passed": passed,
                    "failed": total - passed,
                    "total": total,
                    "time_seconds": time_s,
                    "tokens": tokens,
                    "errors": 0,
                },
                "expectations": expectations,
            }
            runs.append(run)

            if config == "with_harness":
                with_pass_rates.append(pr)
                if time_s > 0:
                    with_times.append(time_s)
                if tokens > 0:
                    with_tokens_list.append(tokens)
            else:
                without_pass_rates.append(pr)
                if time_s > 0:
                    without_times.append(time_s)
                if tokens > 0:
                    without_tokens_list.append(tokens)

    # Analyze patterns for notes
    if grading:
        for a in grading.get("assertions", []):
            disc = a.get("discrimination", "")
            if disc == "non_discriminating_both_pass":
                notes.append(f"Assertion '{a.get('text','')[:60]}' passes in both configs — does not differentiate harness value")
            elif disc == "inverse":
                notes.append(f"WARNING: Assertion '{a.get('text','')[:60]}' passes WITHOUT harness but fails WITH — harness may be hurting")

    # Compute deltas
    wh_mean = mean(with_pass_rates) if with_pass_rates else 0
    woh_mean = mean(without_pass_rates) if without_pass_rates else 0
    delta_pr = wh_mean - woh_mean

    time_delta = (mean(with_times) - mean(without_times)) if with_times and without_times else 0
    token_delta = (mean(with_tokens_list) - mean(without_tokens_list)) if with_tokens_list and without_tokens_list else 0

    benefit_per_kt = round(delta_pr / (harness_tokens / 1000), 3) if harness_tokens > 0 else 0

    if delta_pr > 0:
        notes.append(f"Harness improves pass rate by {delta_pr:.0%} at a cost of {harness_tokens} tokens ({benefit_per_kt}/kT)")
    elif delta_pr < 0:
        notes.append(f"WARNING: Harness DECREASES pass rate by {abs(delta_pr):.0%}")

    benchmark = {
        "metadata": {
            "harness_name": harness_name,
            "harness_token_cost": harness_tokens,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "evals_run": [d.name for d in eval_dirs if d.is_dir()],
            "runs_per_configuration": 1,
        },
        "runs": runs,
        "run_summary": {
            "with_harness": {
                "pass_rate": compute_stats(with_pass_rates),
                "time_seconds": compute_stats(with_times),
                "tokens": compute_stats(with_tokens_list),
            },
            "without_harness": {
                "pass_rate": compute_stats(without_pass_rates),
                "time_seconds": compute_stats(without_times),
                "tokens": compute_stats(without_tokens_list),
            },
            "delta": {
                "pass_rate": f"{delta_pr:+.2f}",
                "time_seconds": f"{time_delta:+.1f}",
                "tokens": f"{token_delta:+.0f}",
                "benefit_per_kilotoken": benefit_per_kt,
            },
        },
        "notes": notes,
    }

    return benchmark


def main():
    parser = argparse.ArgumentParser(description="Aggregate context eval benchmark")
    parser.add_argument("iteration_dir", help="Path to iteration directory")
    parser.add_argument("--harness-name", required=True, help="Name of the harness")
    parser.add_argument("--harness-tokens", type=int, default=1000, help="Estimated token cost")
    parser.add_argument("--output", help="Output path (default: iteration_dir/benchmark.json)")
    args = parser.parse_args()

    iteration_dir = Path(args.iteration_dir)
    if not iteration_dir.exists():
        print(f"Error: {iteration_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    benchmark = aggregate(iteration_dir, args.harness_name, args.harness_tokens)

    output_path = Path(args.output) if args.output else iteration_dir / "benchmark.json"
    output_path.write_text(json.dumps(benchmark, indent=2))

    # Print summary
    rs = benchmark["run_summary"]
    d = rs["delta"]
    print(f"\n  Benchmark: {args.harness_name}")
    print(f"  {'='*40}")
    print(f"  With harness:    {rs['with_harness']['pass_rate']['mean']:.0%} ± {rs['with_harness']['pass_rate']['stddev']:.0%}")
    print(f"  Without harness: {rs['without_harness']['pass_rate']['mean']:.0%} ± {rs['without_harness']['pass_rate']['stddev']:.0%}")
    print(f"  Delta:           {d['pass_rate']}")
    print(f"  Benefit/kToken:  {d['benefit_per_kilotoken']}")
    print(f"\n  Notes:")
    for n in benchmark["notes"]:
        print(f"    • {n}")
    print(f"\n  Saved to: {output_path}")


if __name__ == "__main__":
    main()
