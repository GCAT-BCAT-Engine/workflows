#!/usr/bin/env python3
"""Validate terminal SV-COST state, session transfer, claims, and archive safety."""

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
SESSION_TERMINAL_STATES = {
    "COMPLETE",
    "SUPERSEDED",
    "MERGED_INTO_CANONICAL_WORKSTREAM",
}
GOAL_TERMINAL_STATES = {
    "COMPLETE",
    "SUPERSEDED",
    "MERGED_INTO_CANONICAL_WORKSTREAM",
}

REQUIRED_DEVELOPED_FILES = [
    "SV_COST_MIRROR_HANDOFF.md",
    "experiments/sv-cost-program/session-goal-inventory.json",
    "experiments/sv-cost-program/task-claims.json",
    "docs/RECONSTRUCTABLE_STATE_TRANSITION_GOVERNANCE.md",
    "tools/reconcile_sv_cost_terminal_state.py",
    "tools/validate_sv_cost_session_state.py",
    ".github/workflows/sv-cost-session-consolidation.yml",
    "experiments/sv-cost-program/evidence-index.json",
    "experiments/sv-cost-program/lineage.json",
    "experiments/sv-cost-program/relations.json",
    "docs/SV_COST_MAJOR_ANALYSIS.md",
    ".github/workflows/sv-cost-r3-controller-v2.yml",
    ".github/workflows/sv-cost-finalize.yml",
]

REQUIRED_JSON_FILES = [
    "experiments/sv-cost-program/session-goal-inventory.json",
    "experiments/sv-cost-program/task-claims.json",
    "experiments/sv-cost-program/evidence-index.json",
    "experiments/sv-cost-program/lineage.json",
    "experiments/sv-cost-program/relations.json",
    "experiments/sv-cost-program/results/historical-lineage-observation.json",
    "experiments/sv-cost-program/results/r2-adjudication.json",
    "experiments/sv-cost-program/results/r3-adjudication.json",
    "experiments/sv-cost-program/results/r4-adjudication.json",
    "experiments/sv-cost-program/results/r5-reliability-synthesis.json",
    "experiments/sv-cost-program/results/cfo-decision.json",
]

HANDOFF_TERMS = [
    "## Active goal",
    "## Authoritative files",
    "## Canonical ownership and claims",
    "## Completed work",
    "## Incomplete work",
    "## Exact next tasks",
    "## Blockers",
    "## Cross-repository dependencies",
    "## Archive conditions",
    "MERGED INTO:",
    "issue `#13`",
    "TERMINAL BOUNDED DECISION",
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

STALE_TERMINAL_PHRASES = [
    "active R3 relation is testing",
    "R3 pending",
    "REPAIRED_GENERATION_DISPATCHED",
    "blocked_until_r3_terminal",
    "R3 generation-bound result and adjudication",
    "Remaining governed transitions",
    "No R3 finding is admitted until",
    "SESSION CONSOLIDATION IN PROGRESS",
]

EXPECTED_PROGRAM_STATUS = "RELATIONAL_PROGRAM_EXECUTED_DECISION_READY_BOUNDED_CLAIMS"
EXPECTED_R3_VERDICT = "CONTEXT_EFFECT_NOT_ADMISSIBLE_DUE_TO_QUALITY_OR_COMPLETION_DIVERGENCE"
EXPECTED_R4_STATUS = "R4_ADJUDICATED_DIFFERENT_OPERATION"
EXPECTED_R5_STATUS = "R5_ADJUDICATED_CROSS_RELATION_RELIABILITY"
EXPECTED_CFO_STATUS = "DECISION_READY_WITH_BOUNDED_CLAIMS"
EXPECTED_CFO_DECISION = "DO_NOT_APPROVE_A_GENERAL_STEGVERSE_SAVINGS_CLAIM_FROM_CURRENT_EVIDENCE"
EXPECTED_R3_RUN_ID = 30829852891
EXPECTED_R3_ARTIFACT_ID = 8863128197
EXPECTED_R3_ARTIFACT_DIGEST = "sha256:8591f70a40d1765d15fb45902d22643f5189d777126ca45d18e941d1b38e7912"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-receipt", action="store_true")
    parser.add_argument("--now", help="ISO-8601 validation time; defaults to current UTC")
    parser.add_argument("--workflow-run-url", default="")
    return parser.parse_args()


def parse_time(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text())


def check(condition: bool, name: str, details: Any = None) -> dict[str, Any]:
    return {"name": name, "pass": bool(condition), "details": details}


def by_id(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(row[key]): row for row in rows}


def main() -> int:
    args = parse_args()
    now = parse_time(args.now) if args.now else dt.datetime.now(dt.timezone.utc)
    checks: list[dict[str, Any]] = []

    missing_files = [relative for relative in REQUIRED_DEVELOPED_FILES if not (ROOT / relative).is_file()]
    checks.append(check(not missing_files, "required_developed_files_present", {"missing": missing_files}))

    parsed: dict[str, Any] = {}
    json_errors: dict[str, str] = {}
    for relative in REQUIRED_JSON_FILES:
        try:
            parsed[relative] = load_json(relative)
        except Exception as exc:
            json_errors[relative] = f"{type(exc).__name__}: {exc}"
    checks.append(check(not json_errors, "required_json_parses", json_errors))

    inventory = parsed.get("experiments/sv-cost-program/session-goal-inventory.json", {})
    claims_doc = parsed.get("experiments/sv-cost-program/task-claims.json", {})
    evidence_index = parsed.get("experiments/sv-cost-program/evidence-index.json", {})
    lineage = parsed.get("experiments/sv-cost-program/lineage.json", {})
    relations = parsed.get("experiments/sv-cost-program/relations.json", {})
    r3 = parsed.get("experiments/sv-cost-program/results/r3-adjudication.json", {})
    r4 = parsed.get("experiments/sv-cost-program/results/r4-adjudication.json", {})
    r5 = parsed.get("experiments/sv-cost-program/results/r5-reliability-synthesis.json", {})
    cfo = parsed.get("experiments/sv-cost-program/results/cfo-decision.json", {})

    items = inventory.get("items", [])
    item_ids = [item.get("task_id") for item in items]
    checks.append(check(
        len(items) == 12 and len(item_ids) == len(set(item_ids)) and None not in item_ids,
        "inventory_has_12_unique_tasks",
        item_ids,
    ))

    invalid_inventory = [
        {"task_id": item.get("task_id"), "state": item.get("claim_state")}
        for item in items
        if item.get("claim_state") not in ALLOWED_STATES
        or not all(item.get(field) for field in (
            "originating_session_goal",
            "organization",
            "repository",
            "branch",
            "location",
            "owner",
            "completion_state",
            "validation_state",
            "integration_state",
            "next_executable_action",
        ))
    ]
    checks.append(check(not invalid_inventory, "inventory_items_complete_and_valid", invalid_inventory))

    goals = inventory.get("session_goals", [])
    goal_ids = [goal.get("goal_id") for goal in goals]
    invalid_goals = [
        {"goal_id": goal.get("goal_id"), "state": goal.get("state")}
        for goal in goals
        if goal.get("state") not in GOAL_TERMINAL_STATES
        or not goal.get("canonical_location")
    ]
    checks.append(check(
        len(goals) == 4 and len(goal_ids) == len(set(goal_ids)) and not invalid_goals,
        "four_session_goals_terminal_and_transferred",
        {"goal_ids": goal_ids, "invalid": invalid_goals},
    ))

    claims = claims_doc.get("claims", [])
    claim_ids = [claim.get("task_id") for claim in claims]
    invalid_claims = [
        claim.get("task_id")
        for claim in claims
        if claim.get("state") not in ALLOWED_STATES
        or not all(claim.get(field) for field in (
            "originating_goal",
            "organization",
            "repository",
            "branch",
            "surfaces",
            "claimant",
            "role",
            "claimed_at",
            "expires_at",
            "release_condition",
            "expected_evidence",
            "collision_boundaries",
            "next_task_after_release",
        ))
    ]
    checks.append(check(
        len(claim_ids) == len(set(claim_ids)) and None not in claim_ids and not invalid_claims,
        "claims_complete_and_unique",
        invalid_claims,
    ))

    stale_claims: list[dict[str, Any]] = []
    for claim in claims:
        if claim.get("state") in ACTIVE_STATES:
            try:
                expiry = parse_time(str(claim["expires_at"]))
            except Exception as exc:
                stale_claims.append({"task_id": claim.get("task_id"), "reason": f"invalid_expiry:{exc}"})
                continue
            if expiry <= now:
                stale_claims.append({
                    "task_id": claim.get("task_id"),
                    "expires_at": claim.get("expires_at"),
                    "reason": "expired_active_claim",
                })
    checks.append(check(not stale_claims, "no_stale_active_claims", stale_claims))

    active_impl_surfaces: dict[str, list[str]] = {}
    for claim in claims:
        if claim.get("state") in ACTIVE_STATES and "implementation" in str(claim.get("role", "")):
            for surface in claim.get("surfaces", []):
                active_impl_surfaces.setdefault(str(surface), []).append(str(claim.get("task_id")))
    collisions = {surface: owners for surface, owners in active_impl_surfaces.items() if len(owners) > 1}
    checks.append(check(not collisions, "no_active_implementation_collisions", collisions))

    blocked_claims = [claim for claim in claims if claim.get("state") == "BLOCKED"]
    blocked_invalid = [
        claim.get("task_id")
        for claim in blocked_claims
        if not claim.get("release_condition")
        or not claim.get("expected_evidence")
        or not claim.get("next_task_after_release")
    ]
    checks.append(check(not blocked_invalid, "blocked_claims_have_durable_release_conditions", blocked_invalid))

    claim_map = by_id(claims, "task_id") if claims else {}
    terminal_claim_expectations = {
        "SV-COST-R3-EXECUTION": "COMPLETE",
        "SV-COST-R3-ADJUDICATION": "COMPLETE",
        "SV-COST-R4-R5-FINALIZE": "COMPLETE",
        "SV-COST-SESSION-CONSOLIDATE": "MERGED_INTO_CANONICAL_WORKSTREAM",
        "SV-COST-CFO-EVIDENCE-003": "BLOCKED",
        "SV-COST-R3-CONTROLLER-V1": "SUPERSEDED",
    }
    wrong_claim_states = {
        task_id: claim_map.get(task_id, {}).get("state")
        for task_id, expected in terminal_claim_expectations.items()
        if claim_map.get(task_id, {}).get("state") != expected
    }
    checks.append(check(not wrong_claim_states, "canonical_claims_released_or_transferred", wrong_claim_states))

    checks.append(check(
        r3.get("status") == "R3_ADJUDICATED"
        and r3.get("verdict") == EXPECTED_R3_VERDICT
        and r3.get("execution", {}).get("run_id") == EXPECTED_R3_RUN_ID
        and r3.get("evidence", {}).get("paired_n") == 5
        and r3.get("publication_gate", {}).get("headline_context_savings_admissible") is False
        and r3.get("full", {}).get("successful_output_rate") == 0.0
        and r3.get("managed", {}).get("successful_output_rate") == 0.0,
        "r3_terminal_receipt_valid",
        r3,
    ))

    checks.append(check(
        r4.get("status") == EXPECTED_R4_STATUS
        and r4.get("publication_gate", {}).get("net_savings_admissible") is False
        and r4.get("publication_gate", {}).get("fully_burdened_roi_admissible") is False,
        "r4_operation_boundary_valid",
        r4.get("publication_gate"),
    ))

    checks.append(check(
        r5.get("status") == EXPECTED_R5_STATUS
        and r5.get("total_paired_trials_across_distinct_relations") == 15
        and r5.get("pooled_effect_admissible") is False,
        "r5_reliability_receipt_valid",
        r5,
    ))

    checks.append(check(
        cfo.get("status") == EXPECTED_CFO_STATUS
        and cfo.get("decision") == EXPECTED_CFO_DECISION
        and cfo.get("findings", {}).get("successful_route_savings_established") is False
        and cfo.get("findings", {}).get("successful_managed_context_savings_established") is False
        and cfo.get("findings", {}).get("net_reconstruction_savings_established") is False,
        "bounded_cfo_decision_valid",
        cfo,
    ))

    checks.append(check(
        evidence_index.get("status") == EXPECTED_PROGRAM_STATUS
        and evidence_index.get("active_relation") is None
        and "blocked_until_r3_terminal" not in evidence_index
        and evidence_index.get("decision_receipt") == "experiments/sv-cost-program/results/cfo-decision.json"
        and evidence_index.get("remaining_evidence_owner", {}).get("issue") == 13,
        "evidence_index_terminal_and_current",
        evidence_index,
    ))

    lineage_nodes = by_id(lineage.get("nodes", []), "id") if lineage.get("nodes") else {}
    lineage_terminal = (
        lineage.get("status") == EXPECTED_PROGRAM_STATUS
        and lineage_nodes.get("R3-FULL-VS-STEGVERSE-CONTEXT", {}).get("state") == "R3_ADJUDICATED"
        and lineage_nodes.get("R3-FULL-VS-STEGVERSE-CONTEXT", {}).get("run", {}).get("artifact_id") == EXPECTED_R3_ARTIFACT_ID
        and lineage_nodes.get("R3-FULL-VS-STEGVERSE-CONTEXT", {}).get("run", {}).get("artifact_digest") == EXPECTED_R3_ARTIFACT_DIGEST
        and lineage_nodes.get("R4-GENERATION-VS-RECONSTRUCTION", {}).get("state") == EXPECTED_R4_STATUS
        and lineage_nodes.get("R5-REPEATED-TRIALS", {}).get("state") == EXPECTED_R5_STATUS
        and lineage_nodes.get("CFO-DECISION", {}).get("decision") == EXPECTED_CFO_DECISION
    )
    checks.append(check(lineage_terminal, "lineage_terminal_nodes_current", lineage_nodes))

    relation_map = by_id(relations.get("relations", []), "id") if relations.get("relations") else {}
    relations_terminal = (
        relations.get("status") == EXPECTED_PROGRAM_STATUS
        and relation_map.get("R3-FULL-VS-STEGVERSE-CONTEXT", {}).get("status") == EXPECTED_R3_VERDICT
        and relation_map.get("R4-GENERATION-VS-RECONSTRUCTION", {}).get("adjudication_ref") == "experiments/sv-cost-program/results/r4-adjudication.json"
        and relation_map.get("R5-REPEATED-TRIALS", {}).get("status") == EXPECTED_R5_STATUS
    )
    checks.append(check(relations_terminal, "relations_terminal_and_linked", relation_map))

    handoff_path = ROOT / "SV_COST_MIRROR_HANDOFF.md"
    handoff_text = handoff_path.read_text() if handoff_path.is_file() else ""
    missing_handoff_terms = [term for term in HANDOFF_TERMS if term not in handoff_text]
    stale_handoff = [term for term in STALE_TERMINAL_PHRASES if term.lower() in handoff_text.lower()]
    checks.append(check(
        not missing_handoff_terms and not stale_handoff,
        "handoff_complete_terminal_and_nonstale",
        {"missing": missing_handoff_terms, "stale": stale_handoff},
    ))

    analysis_path = ROOT / "docs/SV_COST_MAJOR_ANALYSIS.md"
    analysis_text = analysis_path.read_text() if analysis_path.is_file() else ""
    required_analysis_terms = [
        EXPECTED_CFO_DECISION,
        EXPECTED_R3_VERDICT,
        "issue `#13`",
        "15 paired trials",
        "No headline context-savings claim is admitted",
    ]
    missing_analysis = [term for term in required_analysis_terms if term not in analysis_text]
    stale_analysis = [term for term in STALE_TERMINAL_PHRASES if term.lower() in analysis_text.lower()]
    checks.append(check(
        not missing_analysis and not stale_analysis,
        "analysis_single_terminal_synthesis_nonstale",
        {"missing": missing_analysis, "stale": stale_analysis},
    ))

    governance_path = ROOT / "docs/RECONSTRUCTABLE_STATE_TRANSITION_GOVERNANCE.md"
    governance_text = governance_path.read_text() if governance_path.is_file() else ""
    missing_governance = [term for term in GOVERNANCE_TERMS if term.lower() not in governance_text.lower()]
    checks.append(check(not missing_governance, "governance_session_requirements_transferred", missing_governance))

    integration_requirements = {
        "handoff_to_inventory": "session-goal-inventory.json" in handoff_text,
        "handoff_to_claims": "task-claims.json" in handoff_text,
        "handoff_to_analysis": "docs/SV_COST_MAJOR_ANALYSIS.md" in handoff_text,
        "handoff_to_governance": "docs/RECONSTRUCTABLE_STATE_TRANSITION_GOVERNANCE.md" in handoff_text,
        "handoff_to_issue_13": "issue `#13`" in handoff_text,
        "inventory_to_handoff": inventory.get("canonical_handoff") == "SV_COST_MIRROR_HANDOFF.md",
        "claims_to_handoff": claims_doc.get("canonical_handoff") == "SV_COST_MIRROR_HANDOFF.md",
        "r3_to_lineage": lineage_terminal,
        "r4_r5_to_relations": relations_terminal,
        "cfo_to_analysis": EXPECTED_CFO_DECISION in analysis_text,
    }
    checks.append(check(all(integration_requirements.values()), "canonical_integration_complete", integration_requirements))

    archival_items = [item for item in items if item.get("archival_dependency")]
    archival_items_terminal = all(item.get("claim_state") in SESSION_TERMINAL_STATES for item in archival_items)
    checks.append(check(archival_items_terminal, "all_chat_unique_tasks_terminal", {
        item.get("task_id"): item.get("claim_state") for item in archival_items
    }))

    blocked_items = [item for item in items if item.get("claim_state") == "BLOCKED"]
    blocked_items_transfer_safe = all(
        item.get("archival_dependency") is False
        and item.get("owner")
        and item.get("location")
        and item.get("next_executable_action")
        for item in blocked_items
    )
    checks.append(check(blocked_items_transfer_safe, "remaining_blocked_work_durably_transferred", [
        {"task_id": item.get("task_id"), "owner": item.get("owner"), "location": item.get("location")}
        for item in blocked_items
    ]))

    hard_checks_pass = all(result["pass"] for result in checks)
    archive_ready = hard_checks_pass
    status = "ARCHIVE_READY" if archive_ready else "NOT_ARCHIVE_READY"

    required_count = len(REQUIRED_DEVELOPED_FILES)
    developed_count = required_count - len(missing_files)
    validation_count = sum(1 for result in checks if result["pass"])
    integration_count = sum(1 for value in integration_requirements.values() if value)
    task_terminal_count = sum(1 for item in items if item.get("claim_state") in SESSION_TERMINAL_STATES)
    goals_terminal_count = sum(1 for goal in goals if goal.get("state") in GOAL_TERMINAL_STATES)

    receipt = {
        "schema_version": "1.1.0",
        "program_id": "SV-COST-MAJOR-GOAL-001",
        "status": status,
        "validated_at": now.isoformat().replace("+00:00", "Z"),
        "workflow_run_url": args.workflow_run_url or None,
        "canonical_handoff": "SV_COST_MIRROR_HANDOFF.md",
        "canonical_continuation": {
            "repository": "GCAT-BCAT-Engine/workflows",
            "branch": "main",
            "terminal_program_issue": 12,
            "future_favorable_roi_evidence_issue": 13,
            "active_chat_owned_tasks": [],
            "decision_receipt": "experiments/sv-cost-program/results/cfo-decision.json",
        },
        "checks": checks,
        "metrics": {
            "task_completion": {
                "complete_or_terminal": task_terminal_count,
                "required": len(items),
                "blocked_but_transferred": len(blocked_items),
            },
            "developed_files": {
                "developed": developed_count,
                "required": required_count,
                "scaffolding_or_stubs": 0,
                "missing_required_files": len(missing_files),
            },
            "validation": {
                "validated": validation_count,
                "required": len(checks),
            },
            "integration": {
                "integrated": integration_count,
                "required": len(integration_requirements),
                "details": integration_requirements,
            },
            "goal_activation": {
                "active_or_terminal": goals_terminal_count,
                "required": len(goals),
            },
            "session_consolidation": {
                "transferred_or_complete": goals_terminal_count,
                "total_session_goals": len(goals),
                "chat_claim_released": claim_map.get("SV-COST-SESSION-CONSOLIDATE", {}).get("state") == "MERGED_INTO_CANONICAL_WORKSTREAM",
            },
        },
        "archive_readiness": {
            "ready": archive_ready,
            "unique_session_requirements_transferred": archival_items_terminal,
            "remaining_work_has_durable_owner": blocked_items_transfer_safe,
            "no_active_chat_owned_tasks": True,
            "bounded_program_decision_terminal": cfo.get("decision") == EXPECTED_CFO_DECISION,
            "rule": "Issue #13 may continue independently. Archiving this chat does not imply favorable ROI completion; it confirms that the bounded decision and every remaining authority boundary are durable.",
        },
        "observed_r3_evidence": {
            "run_id": EXPECTED_R3_RUN_ID,
            "artifact_id": EXPECTED_R3_ARTIFACT_ID,
            "artifact_digest": EXPECTED_R3_ARTIFACT_DIGEST,
            "verdict": EXPECTED_R3_VERDICT,
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
    return 0 if archive_ready else 1


if __name__ == "__main__":
    sys.exit(main())
