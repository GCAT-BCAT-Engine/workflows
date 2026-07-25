#!/usr/bin/env python3
"""Deterministic cost estimator for governed research plans.

This module estimates stage and total cost from explicit unit assumptions. It does
not call providers, authorize spending, or treat estimates as invoices.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def money(value: float) -> float:
    return round(float(value) + 1e-12, 6)


def estimate(plan: dict[str, Any]) -> dict[str, Any]:
    stages = plan.get("stages", [])
    if not stages:
        raise ValueError("Plan must contain at least one stage.")

    stage_results: list[dict[str, Any]] = []
    total_expected = 0.0
    total_variance = 0.0

    for stage in stages:
        stage_id = str(stage["stage_id"])
        units = float(stage.get("units", 0))
        unit_cost = float(stage.get("unit_cost_usd", 0))
        retry_rate = float(stage.get("retry_rate", 0))
        uncertainty_fraction = float(stage.get("uncertainty_fraction", 0))
        fixed_cost = float(stage.get("fixed_cost_usd", 0))

        if min(units, unit_cost, retry_rate, uncertainty_fraction, fixed_cost) < 0:
            raise ValueError(f"Negative cost input in stage {stage_id}.")

        expected = fixed_cost + units * unit_cost * (1.0 + retry_rate)
        sigma = expected * uncertainty_fraction
        total_expected += expected
        total_variance += sigma * sigma

        stage_results.append({
            "stage_id": stage_id,
            "expected_cost_usd": money(expected),
            "sigma_cost_usd": money(sigma),
            "assumptions": {
                "units": units,
                "unit_cost_usd": unit_cost,
                "retry_rate": retry_rate,
                "uncertainty_fraction": uncertainty_fraction,
                "fixed_cost_usd": fixed_cost,
            },
        })

    z = float(plan.get("confidence_z", 1.96))
    sigma_total = math.sqrt(total_variance)
    high_confidence = total_expected + z * sigma_total
    hard_limit = float(plan.get("hard_limit_usd", 0))
    within_limit = hard_limit > 0 and high_confidence <= hard_limit

    result = {
        "schema": "stegverse.research.cost_estimate.v1",
        "research_id": plan.get("research_id"),
        "currency": "USD",
        "stage_estimates": stage_results,
        "expected_cost_usd": money(total_expected),
        "sigma_cost_usd": money(sigma_total),
        "confidence_z": z,
        "high_confidence_cost_usd": money(high_confidence),
        "hard_limit_usd": money(hard_limit),
        "within_hard_limit": within_limit,
        "decision": "PLAN_WITHIN_BUDGET" if within_limit else "REVISE_OR_REAUTHORIZE",
        "execution_authority": False,
        "boundary": "Estimate only. No provider call or spending authority is granted.",
    }
    result["estimate_hash"] = sha256(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--out", type=Path, default=Path("cost-estimate.json"))
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    result = estimate(plan)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
