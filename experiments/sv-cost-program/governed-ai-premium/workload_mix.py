#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)
BURDEN = json.loads((OUT / "production_burden_results.json").read_text())
SCENARIOS = json.loads((ROOT / "workload-mix-scenarios.json").read_text())
TIERS = {row["tier_id"]: row for row in BURDEN["tiers"]}
UNIT = int(SCENARIOS["unit_actions"])

rows = []
for scenario in SCENARIOS["scenarios"]:
    weights = scenario["weights"]
    total_weight = sum(float(v) for v in weights.values())
    assert abs(total_weight - 1.0) < 1e-9, (scenario["id"], total_weight)

    expected_cost = 0.0
    expected_latency_ns = 0.0
    expected_storage = 0.0
    contributions = []
    for tier_id, weight in weights.items():
        tier = TIERS[tier_id]
        w = float(weight)
        cost = float(tier["modeled_local_cost_usd_per_governed_action"])
        latency = float(tier["latency"]["mean_ns"])
        storage = float(tier["modeled_receipt_storage_cost_usd_per_month"])
        expected_cost += w * cost
        expected_latency_ns += w * latency
        expected_storage += w * storage
        contributions.append({
            "tier_id": tier_id,
            "weight": w,
            "weighted_cost_usd_per_action": w * cost,
            "weighted_latency_ns_per_action": w * latency,
        })

    rows.append({
        "scenario_id": scenario["id"],
        "description": scenario["description"],
        "weights": weights,
        "expected_local_governance_cost_usd_per_action": expected_cost,
        "expected_local_governance_cost_usd_per_million_actions": expected_cost * UNIT,
        "expected_mean_latency_ms_per_action": expected_latency_ns / 1e6,
        "expected_receipt_storage_usd_per_million_actions_month": expected_storage * UNIT,
        "tier_contributions": contributions,
    })

result = {
    "schema_version": "1.0.0",
    "experiment_id": "SV-GOVERNED-AI-WORKLOAD-MIX-001",
    "source_burden_experiment": BURDEN["experiment_id"],
    "unit_actions": UNIT,
    "scenarios": rows,
    "lowest_modeled_cost_scenario": min(rows, key=lambda row: row["expected_local_governance_cost_usd_per_action"])["scenario_id"],
    "highest_modeled_cost_scenario": max(rows, key=lambda row: row["expected_local_governance_cost_usd_per_action"])["scenario_id"],
    "claim_boundary": SCENARIOS["claim_boundary"] + " Costs inherit the local synthetic burden limitations of the source experiment and exclude provider inference, remote infrastructure, labor, support, compliance, and commercial margin."
}

(OUT / "workload_mix_results.json").write_text(json.dumps(result, indent=2) + "\n")
report = [
    "# Governed AI Workload-Mix Sensitivity",
    "",
    "| Scenario | Local governance cost/action | Local governance cost/1M actions | Mean latency/action |",
    "|---|---:|---:|---:|",
]
for row in rows:
    report.append(
        f"| {row['scenario_id']} | ${row['expected_local_governance_cost_usd_per_action']:.12f} | "
        f"${row['expected_local_governance_cost_usd_per_million_actions']:.6f} | "
        f"{row['expected_mean_latency_ms_per_action']:.6f} ms |"
    )
report += [
    "",
    "Scenario mixes are deliberately illustrative. Their purpose is to test whether Governed AI economics should be modeled as a workload-weighted mix of governance classes rather than one universal per-action premium.",
]
(OUT / "workload_mix_report.md").write_text("\n".join(report) + "\n")
print("GOVERNED_AI_WORKLOAD_MIX_READY")
