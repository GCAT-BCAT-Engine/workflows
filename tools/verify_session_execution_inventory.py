#!/usr/bin/env python3
"""Validate durable session execution inventory and claim assignment."""

from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "stegverse.session.execution_inventory.v1"
RECEIPT = "stegverse.session.execution_inventory_verification.v1"
ALLOWED = {
    "UNCLAIMED", "CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED", "BLOCKED", "COMPLETE",
    "SUPERSEDED", "MERGED_INTO_CANONICAL_WORKSTREAM",
}
ACTIVE = {"CLAIMED_FOR_IMPLEMENTATION", "CLAIMED_FOR_VALIDATION", "CLAIMED_FOR_INTEGRATION", "MACHINE_OWNED", "BLOCKED"}
REQUIRED_FIELDS = {
    "task_id", "originating_session_goal", "destination_repository", "branch",
    "location", "owner", "claim_state", "completion_state", "validation_state",
    "integration_state", "archival_dependency", "evidence_location",
    "next_executable_action",
}

def canonical_hash(payload: dict[str, Any], field: str) -> str:
    clean = dict(payload); clean.pop(field, None)
    return hashlib.sha256(json.dumps(clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def verify(payload: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    if payload.get("schema") != SCHEMA:
        failures.append("inventory_schema_invalid")
    if payload.get("inventory_hash") != canonical_hash(payload, "inventory_hash"):
        failures.append("inventory_hash_mismatch")
    tasks = payload.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        failures.append("tasks_invalid"); tasks = []
    ids: set[str] = set()
    counts = {"COMPLETE": 0, "ACTIVE": 0, "MERGED": 0}
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            failures.append(f"task_{index}_invalid"); continue
        missing = sorted(REQUIRED_FIELDS - set(task))
        if missing:
            failures.append(f"{task.get('task_id', index)}_missing_fields:{','.join(missing)}")
        task_id = task.get("task_id")
        if task_id in ids:
            failures.append("duplicate_task_id")
        if isinstance(task_id, str):
            ids.add(task_id)
        state = task.get("claim_state")
        if state not in ALLOWED:
            failures.append(f"{task_id}_claim_state_invalid")
        if state == "UNCLAIMED":
            failures.append(f"{task_id}_unassigned")
        if state in ACTIVE:
            counts["ACTIVE"] += 1
            for field in ("claim_timestamp", "claim_expiration_or_release_condition", "expected_evidence", "collision_boundaries", "next_task_after_release"):
                if not task.get(field):
                    failures.append(f"{task_id}_{field}_missing")
        elif state == "COMPLETE":
            counts["COMPLETE"] += 1
        elif state == "MERGED_INTO_CANONICAL_WORKSTREAM":
            counts["MERGED"] += 1
        if not task.get("next_executable_action"):
            failures.append(f"{task_id}_next_action_missing")
        if "/" not in str(task.get("destination_repository", "")):
            failures.append(f"{task_id}_destination_invalid")
        if not task.get("location"):
            failures.append(f"{task_id}_location_missing")

    summary = payload.get("summary")
    if not isinstance(summary, dict):
        failures.append("summary_invalid")
    else:
        if summary.get("total_session_goals") != len(tasks):
            failures.append("summary_total_mismatch")
        if summary.get("complete") != counts["COMPLETE"]:
            failures.append("summary_complete_mismatch")
        if summary.get("active_distinct_support") != counts["ACTIVE"]:
            failures.append("summary_active_mismatch")
        if summary.get("merged_into_canonical_workstream") != counts["MERGED"]:
            failures.append("summary_merged_mismatch")
        if summary.get("unassigned") != 0:
            failures.append("summary_unassigned_nonzero")

    if counts["ACTIVE"] and payload.get("archive_state") == "READY":
        failures.append("archive_ready_with_active_claims")
    decision = "ALLOW" if not failures else "DENY"
    receipt = {
        "receipt_type": RECEIPT,
        "session_id": payload.get("session_id"),
        "inventory_hash": payload.get("inventory_hash"),
        "task_count": len(tasks),
        "active_claim_count": counts["ACTIVE"],
        "unassigned_count": 0 if not any(x.endswith("_unassigned") for x in failures) else 1,
        "terminal_decision": decision,
        "failures": sorted(set(failures)),
    }
    receipt["receipt_hash"] = canonical_hash(receipt, "receipt_hash")
    return receipt

def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=Path("data/session-consolidation/handoff-orchestration-session-20260804.json"))
    parser.add_argument("--output", type=Path, default=Path("data/session-consolidation/handoff-orchestration-session-20260804.verification-receipt.json"))
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.inventory.read_text(encoding="utf-8"))
        receipt = verify(payload)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        receipt = {"receipt_type": RECEIPT, "terminal_decision": "FAIL_CLOSED", "failures": [f"{type(exc).__name__}:{exc}"]}
        receipt["receipt_hash"] = canonical_hash(receipt, "receipt_hash")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("SESSION_EXECUTION_INVENTORY=" + receipt["terminal_decision"])
    return 0 if receipt["terminal_decision"] == "ALLOW" else 1

if __name__ == "__main__":
    raise SystemExit(main())
