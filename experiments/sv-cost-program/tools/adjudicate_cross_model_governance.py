#!/usr/bin/env python3
"""Adjudicate model cost only after task and evidence gates pass.

This first integration consumes the existing observed five-lane calibration and
preserves the ten-advances estimates as a separate, non-observed evidence class.
The workflow is activated by changes to this governed adjudication surface.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CALIBRATION = ROOT / "experiments/five-lane-calibration/results/calibration.json"
CONTRACT = ROOT / "experiments/sv-cost-program/cost-model/governance-vs-no-governance-contract.json"
OUT = ROOT / "experiments/sv-cost-program/results/governance-cross-model-matrix.json"
REPORT = ROOT / "reports/governance-cross-model-matrix.md"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def classify(row: dict) -> dict:
    executed = row.get("status") == "EXECUTED"
    same_task = row.get("task_identity_preserved") is True
    output_present = row.get("output_type") not in {None, "no_generated_proof"}
    receipt_present = isinstance(row.get("receipt_hash"), str) and row["receipt_hash"].startswith("sha256:")
    admissible = executed and same_task and output_present and receipt_present
    failures = []
    if not executed:
        failures.append("NOT_EXECUTED")
    if not same_task:
        failures.append("TASK_IDENTITY_NOT_PRESERVED")
    if not output_present:
        failures.append("REQUIRED_OUTPUT_NOT_PRESENT")
    if not receipt_present:
        failures.append("RECEIPT_MISSING")
    return {
        **row,
        "evidence_class": "OBSERVED_CALIBRATION",
        "quality_gate_status": "PARTIAL_STRUCTURAL_ONLY",
        "admissible_for_bounded_cost_comparison": admissible,
        "gate_failures": failures,
    }


def main() -> int:
    rows = [classify(r) for r in json.loads(CALIBRATION.read_text())]
    admissible = [r for r in rows if r["admissible_for_bounded_cost_comparison"]]
    cheapest = min(admissible, key=lambda r: r["observed_cost_usd"]) if admissible else None

    provider_pairs = []
    for provider in ("openai", "anthropic"):
        raw = next((r for r in rows if r.get("provider") == provider and r["lane_id"].endswith("-raw")), None)
        governed = next((r for r in rows if r.get("provider") == provider and r["lane_id"].endswith("-governed")), None)
        if not raw or not governed:
            continue
        premium = governed["observed_cost_usd"] - raw["observed_cost_usd"]
        provider_pairs.append({
            "provider": provider,
            "raw_lane": raw["lane_id"],
            "governed_lane": governed["lane_id"],
            "raw_admissible": raw["admissible_for_bounded_cost_comparison"],
            "governed_admissible": governed["admissible_for_bounded_cost_comparison"],
            "observed_governance_cost_delta_usd": round(premium, 9),
            "observed_governance_cost_delta_percent": round((premium / raw["observed_cost_usd"] * 100), 6) if raw["observed_cost_usd"] else None,
            "decision": (
                "GOVERNED_LANE_ONLY_ADMISSIBLE"
                if governed["admissible_for_bounded_cost_comparison"] and not raw["admissible_for_bounded_cost_comparison"]
                else "BOTH_ADMISSIBLE_RAW_LOWER_COST"
                if governed["admissible_for_bounded_cost_comparison"] and raw["admissible_for_bounded_cost_comparison"] and premium > 0
                else "BOTH_ADMISSIBLE_GOVERNED_NOT_HIGHER_COST"
                if governed["admissible_for_bounded_cost_comparison"] and raw["admissible_for_bounded_cost_comparison"]
                else "NO_ADMISSIBLE_PAIR"
            ),
        })

    result = {
        "schema_version": "1.0.0",
        "experiment_id": "SV-COST-GOVERNANCE-CROSS-MODEL-001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "comparison_unit": "successful equivalent admissible outcome",
        "source_evidence": {
            "calibration_path": str(CALIBRATION.relative_to(ROOT)),
            "calibration_sha256": sha256(CALIBRATION),
            "contract_path": str(CONTRACT.relative_to(ROOT)),
            "contract_sha256": sha256(CONTRACT),
        },
        "scope_boundary": "Observed SV-MATH-001 calibration only. Structural output and task-identity gates are available; full proof correctness was not independently established by this integration.",
        "selection_rule": "Minimize observed cost only among executed lanes that preserve task identity, produce the required output type, and retain a receipt.",
        "rows": rows,
        "provider_pairs": provider_pairs,
        "bounded_selection": {
            "lane_id": cheapest["lane_id"] if cheapest else None,
            "provider": cheapest.get("provider") if cheapest else None,
            "observed_cost_usd": cheapest.get("observed_cost_usd") if cheapest else None,
            "status": "SELECTED_AMONG_STRUCTURALLY_ADMISSIBLE_CALIBRATION_LANES" if cheapest else "NO_SELECTION",
        },
        "governance_demonstration": {
            "cheapest_is_not_automatically_accepted": True,
            "rejected_lanes": [
                {"lane_id": r["lane_id"], "observed_cost_usd": r["observed_cost_usd"], "reasons": r["gate_failures"]}
                for r in rows if not r["admissible_for_bounded_cost_comparison"]
            ],
            "interpretation": "Governance is demonstrated by applying task and evidence gates before price comparison. A low or zero observed charge does not become a winning result when the required operation was not completed or task identity was not preserved.",
        },
        "token_boundary": "Provider-reported tokens are retained as interface observations and do not determine selection.",
        "next_evidence": [
            "Run the same adjudicator over additional observed tasks and model versions.",
            "Add independent correctness and quality-equivalence verdicts before general model ranking.",
            "Measure local StegVerse governance cost where it is not included in provider charge.",
            "Keep ten-advances prospective estimates separate from observed execution results."
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")

    lines = [
        "# Cross-Model Governance Cost Matrix",
        "",
        "Status: **BOUNDED OBSERVED CALIBRATION ADJUDICATED**",
        "",
        "> Cost is compared only after task identity, execution, output, and receipt gates pass.",
        "",
        "| Lane | Provider | Executed | Task preserved | Output present | Admissible | Observed cost | Decision |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['lane_id']} | {r.get('provider','')} | {r.get('status') == 'EXECUTED'} | "
            f"{r.get('task_identity_preserved') is True} | {r.get('output_type') != 'no_generated_proof'} | "
            f"{r['admissible_for_bounded_cost_comparison']} | ${r.get('observed_cost_usd',0):.6f} | "
            f"{'PASS TO COST COMPARISON' if r['admissible_for_bounded_cost_comparison'] else ', '.join(r['gate_failures'])} |"
        )
    lines += ["", "## Provider-pair findings", ""]
    for pair in provider_pairs:
        lines.append(
            f"- **{pair['provider']}**: {pair['decision']}; governed-minus-raw observed provider charge "
            f"`${pair['observed_governance_cost_delta_usd']:.6f}` ({pair['observed_governance_cost_delta_percent']:.3f}%)."
        )
    if cheapest:
        lines += [
            "",
            "## Bounded selection",
            "",
            f"`{cheapest['lane_id']}` is the lowest observed-cost lane among the structurally admissible calibration lanes at `${cheapest['observed_cost_usd']:.6f}`.",
            "",
            "This is not a general model ranking. Full proof correctness and complete StegVerse local cost remain outside this bounded receipt.",
        ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")
    print(json.dumps({"matrix": str(OUT), "report": str(REPORT), "selected": cheapest["lane_id"] if cheapest else None}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
