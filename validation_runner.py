#!/usr/bin/env python3
"""
StegVerse Validation Run Manual Executor

Runs the local validation plan from validation_run_v1.yml.
This script does not call Anthropic. It tracks planned phases and budget guardrails.

Run:
  python3 validation_runner.py
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml


SPEC_PATH = Path("validation_run_v1.yml")
RESULTS_PATH = Path("validation_results_VAL-001.json")


def main() -> int:
    if not SPEC_PATH.exists():
        print(f"ERROR: {SPEC_PATH} not found")
        return 1

    spec = yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))
    run = spec["validation_run_v1"]

    print(f"=== StegVerse Validation Run: {run['run_id']} ===")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print(f"Budget ceiling: ${float(run['budget_ceiling_usd']):.2f}")
    print(f"Total estimated: ${float(run['total_estimated_cost_usd']):.2f}")
    print()

    cumulative_cost = 0.0
    results = {}

    for phase in run["phases"]:
        phase_id = phase["phase_id"]
        name = phase["name"]
        est_cost = float(phase["estimated_cost_usd"])

        print(f"\n--- Phase {phase_id}: {name} ---")
        print(f"Estimated cost: ${est_cost:.4f}")

        if cumulative_cost + est_cost > float(run["budget_ceiling_usd"]):
            print(f"HALT: would exceed budget ceiling (${float(run['budget_ceiling_usd']):.2f})")
            print(f"Current spend: ${cumulative_cost:.4f}")
            results[name] = {
                "status": "halted_budget_guard",
                "estimated_cost": est_cost,
                "actual_cost": 0.0,
                "cumulative_cost": cumulative_cost,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            break

        duration = min(float(phase.get("max_reasoning_time_minutes", 1)), 2.0)
        print("Executing local placeholder phase...")
        print(f"Duration cap: ~{duration:.1f} minutes")
        time.sleep(0.2)

        actual_cost = est_cost
        cumulative_cost += actual_cost

        results[name] = {
            "status": "completed",
            "estimated_cost": est_cost,
            "actual_cost": actual_cost,
            "cumulative_cost": cumulative_cost,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        print(f"Completed. Actual cost: ${actual_cost:.4f}")
        print(f"Cumulative: ${cumulative_cost:.4f}")

    print("\n=== Validation Run Complete ===")
    print(f"Total spend: ${cumulative_cost:.4f}")
    print(f"Budget remaining: ${float(run['budget_ceiling_usd']) - cumulative_cost:.4f}")

    RESULTS_PATH.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Results saved: {RESULTS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
