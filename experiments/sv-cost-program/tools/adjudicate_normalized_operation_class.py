#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "experiments/sv-cost-normalized/results/result.json"
OUT = ROOT / "experiments/sv-cost-program/results/normalized-operation-class-matrix.json"
REPORT = ROOT / "reports/normalized-operation-class-matrix.md"


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    source = json.loads(SOURCE.read_text())
    rows = []
    for lane in source.get("lanes", []):
        attempts = lane.get("attempts", [])
        structural_ok = bool(attempts) and all(
            a.get("classification") == "comparable"
            and not a.get("missing_obligations")
            and not a.get("structural_errors")
            for a in attempts
        )
        receipt_ok = isinstance(lane.get("native_output_hash"), str) and lane["native_output_hash"].startswith("sha256:")
        comparable = lane.get("classification") == "comparable" and structural_ok and receipt_ok
        local_unmeasured = lane.get("local_cost_status") == "UNMEASURED_LOCAL_RUNTIME"
        selectable = comparable and not local_unmeasured
        rows.append({
            **lane,
            "task_id": "SV-COST-NORMALIZED-001",
            "operation_class": "bounded_abstract_characterization_or_admitted_reconstruction",
            "evidence_class": "OBSERVED",
            "comparable_within_operation_class": comparable,
            "fully_burdened_cost_known": not local_unmeasured,
            "eligible_for_observed_cost_selection": selectable,
            "selection_exclusions": (["LOCAL_RUNTIME_COST_UNMEASURED"] if local_unmeasured else []),
        })

    eligible = [r for r in rows if r["eligible_for_observed_cost_selection"]]
    selected = min(eligible, key=lambda r: r["observed_provider_cost_usd"]) if eligible else None
    stegverse = next((r for r in rows if r["lane_id"] == "stegverse-only"), None)

    result = {
        "schema_version": "1.0.0",
        "experiment_id": "SV-COST-NORMALIZED-001",
        "task_id": "SV-COST-NORMALIZED-001",
        "operation_class": "bounded_abstract_characterization_or_admitted_reconstruction",
        "evidence_class": "OBSERVED",
        "source_path": str(SOURCE.relative_to(ROOT)),
        "source_sha256": digest(SOURCE),
        "rows": rows,
        "bounded_selection": {
            "lane_id": selected["lane_id"] if selected else None,
            "observed_provider_cost_usd": selected["observed_provider_cost_usd"] if selected else None,
            "basis": "lowest observed provider charge among comparable lanes with known fully burdened cost status"
        },
        "governance_demonstration": {
            "stegverse_zero_provider_charge_selected": bool(stegverse and selected and selected["lane_id"] == "stegverse-only"),
            "stegverse_zero_provider_charge_rejected_from_cost_ranking": bool(stegverse and not stegverse["eligible_for_observed_cost_selection"]),
            "reason": "StegVerse-only reconstruction has zero external provider charge but unmeasured local runtime cost, so it cannot be ranked as the cheapest fully burdened lane.",
            "operation_class_boundary": "This matrix applies only when bounded reconstruction or abstract characterization is the requested operation. It does not compare reconstruction against fresh inference."
        },
        "counterfactual_boundary": "Batch-normalized values are retained but excluded from observed selection because no actual native batch receipt is present.",
        "token_boundary": "Tokens are retained as provider interface observations and do not determine selection."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")

    lines = [
        "# Normalized Operation-Class Cost Matrix",
        "",
        "Status: **OBSERVED, OPERATION-CLASS SEPARATED**",
        "",
        "> Reconstruction is compared only when reconstruction is the requested operation. Zero provider charge is not treated as zero total cost when local runtime cost is unmeasured.",
        "",
        "| Lane | Model/runtime | Comparable | Fully burdened cost known | Eligible | Observed provider charge | Decision |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        decision = "PASS TO COST COMPARISON" if row["eligible_for_observed_cost_selection"] else ", ".join(row["selection_exclusions"])
        lines.append(
            f"| {row['lane_id']} | {row['model']} | {row['comparable_within_operation_class']} | "
            f"{row['fully_burdened_cost_known']} | {row['eligible_for_observed_cost_selection']} | "
            f"${row['observed_provider_cost_usd']:.6f} | {decision} |"
        )
    if selected:
        lines += ["", "## Bounded selection", "", f"`{selected['lane_id']}` is the least observed-cost eligible lane at `${selected['observed_provider_cost_usd']:.6f}`."]
    lines += ["", "## Governance result", "", "The StegVerse-only lane is not selected merely because its external provider charge is zero. Its local runtime cost remains unmeasured."]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n")
    print(json.dumps({"valid": True, "selected": selected["lane_id"] if selected else None, "rows": len(rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
