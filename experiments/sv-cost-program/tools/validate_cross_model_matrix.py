#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MATRIX = ROOT / "experiments/sv-cost-program/results/governance-cross-model-matrix.json"
REGISTRY = ROOT / "experiments/sv-cost-program/cost-model/model-registry.json"
TASKS = ROOT / "experiments/sv-cost-program/cost-model/canonical-task-set.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    matrix = json.loads(MATRIX.read_text())
    registry = json.loads(REGISTRY.read_text())
    tasks = json.loads(TASKS.read_text())

    rows = matrix.get("rows", [])
    if not rows:
        fail("matrix has no rows")

    admitted = [r for r in rows if r.get("admissible_for_bounded_cost_comparison")]
    rejected = [r for r in rows if not r.get("admissible_for_bounded_cost_comparison")]
    if not admitted:
        fail("matrix has no admitted lanes")
    if not rejected:
        fail("matrix does not demonstrate a rejected lane")

    selected = matrix.get("bounded_selection", {})
    selected_lane = selected.get("lane_id")
    selected_row = next((r for r in rows if r.get("lane_id") == selected_lane), None)
    if not selected_row or not selected_row.get("admissible_for_bounded_cost_comparison"):
        fail("selected lane is not admitted")

    minimum = min(float(r["observed_cost_usd"]) for r in admitted)
    if abs(float(selected_row["observed_cost_usd"]) - minimum) > 1e-12:
        fail("selected lane is not the least-cost admitted lane")

    for row in rejected:
        if not row.get("gate_failures"):
            fail(f"rejected lane {row.get('lane_id')} lacks rejection reasons")

    zero_cost = [r for r in rows if float(r.get("observed_cost_usd", 0)) == 0]
    for row in zero_cost:
        if not row.get("admissible_for_bounded_cost_comparison") and row.get("lane_id") == selected_lane:
            fail("zero-cost failed lane was selected")

    registered = {(m.get("provider"), m.get("model_id")) for m in registry.get("models", [])}
    for row in rows:
        model = row.get("model") or row.get("lane_id")
        if (row.get("provider"), model) not in registered and row.get("provider") != "stegverse":
            fail(f"unregistered observed model: {row.get('provider')}/{model}")

    task = next((t for t in tasks.get("tasks", []) if t.get("task_id") == "SV-MATH-001-CALIBRATION"), None)
    if not task:
        fail("canonical observed calibration task is missing")
    if task.get("ranking_permission") != "BOUNDED_STRUCTURAL_COST_COMPARISON_ONLY":
        fail("calibration ranking boundary changed")

    if matrix.get("token_boundary") is None:
        fail("token boundary missing")
    if not matrix.get("governance_demonstration", {}).get("cheapest_is_not_automatically_accepted"):
        fail("governance refusal invariant missing")

    print(json.dumps({
        "valid": True,
        "rows": len(rows),
        "admitted": len(admitted),
        "rejected": len(rejected),
        "selected_lane": selected_lane,
        "selected_cost_usd": selected_row["observed_cost_usd"]
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
