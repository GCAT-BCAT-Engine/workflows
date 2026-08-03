#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "experiments/sv-cost-program/cross-model-session-inventory.json"
FRESH = ROOT / "experiments/sv-cost-program/results/governance-cross-model-matrix.json"
NORMALIZED = ROOT / "experiments/sv-cost-program/results/normalized-operation-class-matrix.json"
HANDOFF = ROOT / "SV_COST_MIRROR_HANDOFF.md"
RECEIPT = ROOT / "experiments/sv-cost-program/results/cross-model-session-receipt.json"


def main() -> int:
    errors: list[str] = []
    inventory = json.loads(INVENTORY.read_text())
    fresh = json.loads(FRESH.read_text()) if FRESH.exists() else None
    normalized = json.loads(NORMALIZED.read_text()) if NORMALIZED.exists() else None
    handoff = HANDOFF.read_text()

    if inventory.get("session_goal_id") != "SV-COST-CROSS-MODEL-SESSION-001":
        errors.append("inventory goal ID mismatch")
    if fresh is None:
        errors.append("fresh cross-model matrix missing")
    else:
        if not fresh.get("governance_demonstration", {}).get("cheapest_is_not_automatically_accepted"):
            errors.append("fresh matrix governance refusal invariant missing")
        selected = fresh.get("bounded_selection", {}).get("lane_id")
        admitted = {r.get("lane_id") for r in fresh.get("rows", []) if r.get("admissible_for_bounded_cost_comparison")}
        if selected not in admitted:
            errors.append("fresh selected lane is not admitted")
    if normalized is None:
        errors.append("normalized operation-class matrix missing")
    else:
        if normalized.get("operation_class") != "bounded_abstract_characterization_or_admitted_reconstruction":
            errors.append("normalized operation-class boundary mismatch")
        gd = normalized.get("governance_demonstration", {})
        if gd.get("stegverse_zero_provider_charge_selected") is not False:
            errors.append("zero provider charge was improperly selected")
        if gd.get("stegverse_zero_provider_charge_rejected_from_cost_ranking") is not True:
            errors.append("unmeasured local-cost exclusion missing")
    for required in [
        "cross-model-session-inventory.json",
        "governance-cross-model-matrix.json",
        "normalized-operation-class-matrix.json",
        "issue #13",
    ]:
        if required not in handoff:
            errors.append(f"handoff missing reference: {required}")

    status = "ARCHIVE_READY" if not errors else "BLOCKED"
    receipt = {
        "schema_version": "1.0.0",
        "program_id": "SV-COST-MAJOR-GOAL-001",
        "session_goal_id": "SV-COST-CROSS-MODEL-SESSION-001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "errors": errors,
        "canonical_continuation": "GCAT-BCAT-Engine/workflows/SV_COST_MIRROR_HANDOFF.md and issue #13",
        "next_executable_action": "None; repository-native workflows own future model additions." if not errors else "Resolve each named error and rerun this validator.",
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
