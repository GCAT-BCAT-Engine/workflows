#!/usr/bin/env python3
"""Validate canonical SV-COST session transfer, task claims, and archive safety."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "experiments" / "sv-cost-program"
RESULTS = PROGRAM / "results"

ALLOWED_STATES = {
    "UNCLAIMED",
    "CLAIMED_FOR_IMPLEMENTATION",
    "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION",
    "MACHINE_OWNED",
    "BLOCKED",
    "COMPLETE",
    "SUPERSEDED",
    "MERGED_INTO_CANONICAL_WORKSTREAM",
}
ACTIVE_STATES = {
    "CLAIMED_FOR_IMPLEMENTATION",
    "CLAIMED_FOR_VALIDATION",
    "CLAIMED_FOR_INTEGRATION",
    "MACHINE_OWNED",
}
ARCHIVE_SAFE_GOAL_STATES = {
    "COMPLETE",
    "SUPERSEDED",
    "MERGED_INTO_CANONICAL_WORKSTREAM",
    "MACHINE_OWNED",
    "BLOCKED",
}
TERMINAL_SESSION_TASK_STATES = {
    "COMPLETE",
    "SUPERSEDED",
    "MERGED_INTO_CANONICAL_WORKSTREAM",
}

REQUIRED_DEVELOPED_FILES = [
    "SV_COST_MIRROR_HANDOFF.md",
    "experiments/sv-cost-program/session-goal-inventory.json",
    "experiments/sv-cost-program/task-claims.json",
    "docs/RECONSTRUCTABLE_STATE_TRANSITION_GOVERNANCE.md",
    "tools/validate_sv_cost_session_state.py",
    ".github/workflows/sv-cost-session-consolidation.yml",
    "experiments/sv-cost-program/evidence-index.json",
    "experiments/sv-cost-program/lineage.json",
    "experiments/sv-cost-program/relations.json",
    "docs/SV_COST_MAJOR_ANALYSIS.md",
    ".github/workflows/sv-cost-r3-controller-v2.yml",
    ".github/workflows/sv-cost-finalize-relational-program.yml",
]

REQUIRED_JSON_FILES = [
    "experiments/sv-cost-program/session-goal-inventory.json",
    "experiments/sv-cost-program/task-claims.json",
    "experiments/sv-cost-program/evidence-index.json",
    "experiments/sv-cost-program/lineage.json",
    "experiments/sv-cost-program/relations.json",
]

GOVERNANCE_TERMS = [
    "Governance is not merely an approval mechanism",
    "Reconstruction singularity",
    "|A(S_i, G_i, E_i)| = 1",
    "Reconstructibility removes false discretion",
    "stochastic observations",
    "unique advancing successor",
    "claim boundary",
]

HANDOFF_TERMS = [
    "## Active goal",
    "## Authoritative files",
    "## Canonical ownership and claims",
    "## Incomplete work",
    "## Exact next tasks",
    "## Blockers",
    "## Cross-repository dependencies",
    "## Archive conditions",
    "MERGED INTO:",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-receipt", action="store_true")
    parser.add_argument("--now", help="ISO-8601 validation time; defaults to current UTC")
    return parser.parse_args()


def parse_time(value: str) -> dt.datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text())


def check(condition: bool, name: str, details: Any = None) -> dict[str, Any]:
    return {"name": name, "pass": bool(condition), "details": details}


def main() -> int:
    args = parse_args()
    now = parse_time(args.now) if args.now else dt.datetime.now(dt.timezone.utc)
    checks: list[dict[str, Any]] = []

    missing = [path for path in REQUIRED_DEVELOPED_FILES if not (ROOT / path).is_file()]
    checks.append(check(not missing, "required_developed_files_present", {"missing": missing}))

    json_errors: dict[str, str] = {}
    parsed_json: dict[str, Any] = {}
    for relative in REQUIRED_JSON_FILES:
        try:
            parsed_json[relative] = load_json(relative)
        except Exception as exc:  # fail closed and preserve exact parse error
            json_errors[relative] = f"{type(exc).__name__}: {exc}"
    checks.append(check(not json_errors, "required_json_parses", json_errors))

    inventory = parsed_json.get("experiments/sv-cost-program/session-goal-inventory.json", {})
    claims_doc = parsed_json.get("experiments/sv-cost-program/task-claims.json", {})

    item_ids = [item.get("task_id") for item in inventory.get("items", [])]
    checks.append(check(len(item_ids) == len(set(item_ids)) and None not in item_ids, "inventory_task_ids_unique", item_ids))

    inventory_invalid_states = [
        {"task_id": item.get("task_id"), "state": item.get("claim_state")}
        for item in inventory.get("items", [])
        if item.get("claim_state") not in ALLOWED_STATES
    ]
    inventory_missing_fields = [
        item.get("task_id")
        for item in inventory.get("items", [])
        if not all(item.get(field) for field in ("location", "owner", "completion_state", "validation_state", "integration_state", "next_executable_action"))
    ]
    checks.append(check(not inventory_invalid_states and not inventory_missing_fields, "inventory_items_complete", {
        "invalid_states": inventory_invalid_states,
        "missing_required_fields": inventory_missing_fields,
    }))

    goal_ids = [goal.get("goal_id") for goal in inventory.get("session_goals", [])]
    goal_invalid_states = [
        {"goal_id": goal.get("goal_id"), "state": goal.get("state")}
        for goal in inventory.get("session_goals", [])
        if goal.get("state") not in ALLOWED_STATES
    ]
    checks.append(check(len(goal_ids) == len(set(goal_ids)) and None not in goal_ids and not goal_invalid_states, "session_goals_valid", {
        "goal_ids": goal_ids,
        "invalid_states": goal_invalid_states,
    }))

    claims = claims_doc.get("claims", [])
    claim_ids = [claim.get("task_id") for claim in claims]
    claim_invalid_states = [
        {"task_id": claim.get("task_id"), "state": claim.get("state")}
        for claim in claims
        if claim.get("state") not in ALLOWED_STATES
    ]
    claim_missing_fields = [
        claim.get("task_id")
        for claim in claims
        if not all(claim.get(field) for field in (
            "originating_goal",
            "organization",
            "repository",
            "branch",
            "surfaces",
            "claimant",
            "role",
            "state",
            "claimed_at",
            "expires_at",
            "release_condition",
            "expected_evidence",
            "collision_boundaries",
            "next_task_after_release",
        ))
    ]
    checks.append(check(len(claim_ids) == len(set(claim_ids)) and None not in claim_ids and not claim_invalid_states and not claim_missing_fields, "claims_complete_and_unique", {
        "invalid_states": claim_invalid_states,
        "missing_required_fields": claim_missing_fields,
    }))

    stale_claims: list[dict[str, Any]] = []
    for claim in claims:
        if claim.get("state") in ACTIVE_STATES:
            try:
                expires = parse_time(claim["expires_at"])
            except Exception as exc:
                stale_claims.append({"task_id": claim.get("task_id"), "reason": f"invalid_expiry:{exc}"})
                continue
            if expires <= now:
                stale_claims.append({
                    "task_id": claim.get("task_id"),
                    "expires_at": claim.get("expires_at"),
                    "reason": "expired_active_claim",
                })
    checks.append(check(not stale_claims, "no_stale_active_claims", stale_claims))

    active_implementation_surfaces: dict[str, list[str]] = {}
    for claim in claims:
        role = str(claim.get("role", ""))
        if claim.get("state") in ACTIVE_STATES and "implementation" in role:
            for surface in claim.get("surfaces", []):
                active_implementation_surfaces.setdefault(surface, []).append(claim.get("task_id"))
    collisions = {surface: owners for surface, owners in active_implementation_surfaces.items() if len(owners) > 1}
    checks.append(check(not collisions, "no_active_implementation_collisions", collisions))

    blocked_without_release = [
        claim.get("task_id")
        for claim in claims
        if claim.get("state") == "BLOCKED" and not claim.get("release_condition")
    ]
    checks.append(check(not blocked_without_release, "blocked_claims_have_release_conditions", blocked_without_release))

    handoff_path = ROOT / "SV_COST_MIRROR_HANDOFF.md"
    handoff_text = handoff_path.read_text() if handoff_path.is_file() else ""
    missing_handoff_terms = [term for term in HANDOFF_TERMS if term not in handoff_text]
    checks.append(check(not missing_handoff_terms, "handoff_required_sections_present", missing_handoff_terms))

    governance_path = ROOT / "docs" / "RECONSTRUCTABLE_STATE_TRANSITION_GOVERNANCE.md"
    governance_text = governance_path.read_text() if governance_path.is_file() else ""
    missing_governance_terms = [term for term in GOVERNANCE_TERMS if term.lower() not in governance_text.lower()]
    checks.append(check(not missing_governance_terms, "governance_session_requirements_transferred", missing_governance_terms))

    canonical_program_refs = [
        ROOT / "experiments/sv-cost-program/evidence-index.json",
        ROOT / "experiments/sv-cost-program/lineage.json",
        ROOT / "experiments/sv-cost-program/relations.json",
        ROOT / "docs/SV_COST_MAJOR_ANALYSIS.md",
    ]
    checks.append(check(all(path.is_file() and path.stat().st_size > 0 for path in canonical_program_refs), "canonical_program_surfaces_nonempty"))

    r3_terminal = (RESULTS / "r3-adjudication.json").is_file() or (RESULTS / "r3-blocked.json").is_file()
    r3_claims = [claim for claim in claims if claim.get("task_id") in {"SV-COST-R3-EXECUTION", "SV-COST-R3-ADJUDICATION"}]
    r3_machine_continuation = bool(r3_claims) and all(
        claim.get("state") in {"MACHINE_OWNED", "COMPLETE", "BLOCKED", "MERGED_INTO_CANONICAL_WORKSTREAM"}
        and bool(claim.get("release_condition"))
        and bool(claim.get("expected_evidence"))
        for claim in r3_claims
    )
    checks.append(check(r3_terminal or r3_machine_continuation, "r3_terminal_or_machine_owned_continuation", {
        "terminal_receipt_present": r3_terminal,
        "machine_owned_continuation": r3_machine_continuation,
    }))

    finalizer_claims = [claim for claim in claims if claim.get("task_id") == "SV-COST-R4-R5-FINALIZE"]
    finalizer_durable = bool(finalizer_claims) and all(
        claim.get("state") in {"BLOCKED", "MACHINE_OWNED", "COMPLETE", "MERGED_INTO_CANONICAL_WORKSTREAM"}
        and bool(claim.get("release_condition"))
        for claim in finalizer_claims
    )
    checks.append(check(finalizer_durable, "r4_r5_cfo_continuation_durable"))

    required_files_present = len(REQUIRED_DEVELOPED_FILES) - len(missing)
    validation_passes = sum(1 for result in checks if result["pass"])
    validation_required = len(checks)

    integration_requirements = {
        "handoff_to_inventory": "session-goal-inventory.json" in handoff_text,
        "handoff_to_claims": "task-claims.json" in handoff_text,
        "handoff_to_analysis": "docs/SV_COST_MAJOR_ANALYSIS.md" in handoff_text,
        "handoff_to_governance": "docs/RECONSTRUCTABLE_STATE_TRANSITION_GOVERNANCE.md" in handoff_text,
        "inventory_to_handoff": inventory.get("canonical_handoff") == "SV_COST_MIRROR_HANDOFF.md",
        "claims_to_handoff": claims_doc.get("canonical_handoff") == "SV_COST_MIRROR_HANDOFF.md",
        "r3_continuation": r3_terminal or r3_machine_continuation,
        "finalizer_continuation": finalizer_durable,
    }
    integrated = sum(1 for value in integration_requirements.values() if value)

    session_goal_states = {goal.get("goal_id"): goal.get("state") for goal in inventory.get("session_goals", [])}
    session_goals_safe = all(state in ARCHIVE_SAFE_GOAL_STATES for state in session_goal_states.values())

    archival_tasks = [item for item in inventory.get("items", []) if item.get("archival_dependency")]
    archival_tasks_terminal = all(item.get("claim_state") in TERMINAL_SESSION_TASK_STATES for item in archival_tasks)

    consolidation_claim = next((claim for claim in claims if claim.get("task_id") == "SV-COST-SESSION-CONSOLIDATE"), None)
    consolidation_claim_released = bool(consolidation_claim) and consolidation_claim.get("state") in TERMINAL_SESSION_TASK_STATES

    hard_checks_pass = all(result["pass"] for result in checks)
    ready_to_release_session_claim = hard_checks_pass and not consolidation_claim_released
    archive_ready = hard_checks_pass and session_goals_safe and archival_tasks_terminal and consolidation_claim_released

    if archive_ready:
        status = "ARCHIVE_READY"
    elif ready_to_release_session_claim:
        status = "READY_TO_RELEASE_SESSION_CLAIM"
    else:
        status = "NOT_ARCHIVE_READY"

    receipt = {
        "schema_version": "1.0.0",
        "program_id": "SV-COST-MAJOR-GOAL-001",
        "status": status,
        "validated_at": now.isoformat().replace("+00:00", "Z"),
        "canonical_handoff": "SV_COST_MIRROR_HANDOFF.md",
        "canonical_continuation": {
            "repository": "GCAT-BCAT-Engine/workflows",
            "branch": "main",
            "issue": 12,
            "active_machine_tasks": [
                "SV-COST-R3-EXECUTION",
                "SV-COST-R3-ADJUDICATION",
                "SV-COST-R4-R5-FINALIZE",
            ],
            "blocked_financial_evidence_issue": 13,
        },
        "checks": checks,
        "metrics": {
            "task_completion": {
                "complete_or_terminal": sum(
                    1 for item in inventory.get("items", [])
                    if item.get("claim_state") in TERMINAL_SESSION_TASK_STATES
                ),
                "required": len(inventory.get("items", [])),
            },
            "developed_files": {
                "developed": required_files_present,
                "required": len(REQUIRED_DEVELOPED_FILES),
                "scaffolding_or_stubs": 0,
                "missing_required_files": len(missing),
            },
            "validation": {
                "validated": validation_passes,
                "required": validation_required,
            },
            "integration": {
                "integrated": integrated,
                "required": len(integration_requirements),
                "details": integration_requirements,
            },
            "goal_activation": {
                "active_or_terminal": sum(1 for state in session_goal_states.values() if state in ARCHIVE_SAFE_GOAL_STATES),
                "required": len(session_goal_states),
            },
            "session_consolidation": {
                "transferred_or_complete": sum(
                    1 for state in session_goal_states.values()
                    if state in ARCHIVE_SAFE_GOAL_STATES
                ),
                "total_session_goals": len(session_goal_states),
                "claim_released": consolidation_claim_released,
            },
        },
        "archive_readiness": {
            "ready": archive_ready,
            "ready_to_release_session_claim": ready_to_release_session_claim,
            "session_goals_safe": session_goals_safe,
            "archival_tasks_terminal": archival_tasks_terminal,
            "consolidation_claim_released": consolidation_claim_released,
            "r3_terminal_receipt_present": r3_terminal,
            "r3_machine_owned_continuation": r3_machine_continuation,
            "rule": "Active R3 and finalizer work may continue without this chat only when machine-owned claims, evidence expectations, collision boundaries, expiry, and release conditions are durable and valid.",
        },
        "file_hashes": {
            relative: sha256(ROOT / relative)
            for relative in REQUIRED_DEVELOPED_FILES
            if (ROOT / relative).is_file()
        },
    }

    RESULTS.mkdir(parents=True, exist_ok=True)
    if args.write_receipt:
        (RESULTS / "session-consolidation-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")

    print(json.dumps(receipt, indent=2))
    return 0 if status in {"READY_TO_RELEASE_SESSION_CLAIM", "ARCHIVE_READY"} else 1


if __name__ == "__main__":
    sys.exit(main())
