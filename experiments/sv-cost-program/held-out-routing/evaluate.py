#!/usr/bin/env python3
"""Offline, source-only adjudication of separately supplied routing observations.

Does not choose production routes, confer admission or verify remote custody.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

VALID_DISPOSITIONS = {"ALLOW", "DENY", "FAIL_CLOSED", "REVIEW_REQUIRED", "QUARANTINE"}
NON_ALLOW = VALID_DISPOSITIONS - {"ALLOW"}


def adjudicate(case: dict, observation: dict) -> dict:
    expected = case["oracle"]
    task = case["router_input"]["task_id"]
    errors: list[str] = []
    # The independent oracle is evaluator-only; it may never be echoed by
    # the routed system or smuggled into a purported runtime observation.
    if "oracle" in observation or "expected_final_result" in observation:
        errors.append("HELD_OUT_ORACLE_LEAKAGE")
    if observation.get("task_id") != task:
        errors.append("TASK_ID_MISMATCH")
    if observation.get("route") != expected["permitted_route"]:
        errors.append("ROUTE_ORACLE_MISMATCH")
    disposition = observation.get("disposition")
    if disposition not in VALID_DISPOSITIONS:
        errors.append("INVALID_OR_MISSING_DISPOSITION")
    elif disposition != expected["required_disposition"]:
        errors.append("DISPOSITION_ORACLE_MISMATCH")
    if disposition in NON_ALLOW:
        if not observation.get("reason_code") or not observation.get("corrective_next_action"):
            errors.append("NON_ALLOW_NOT_ACTIONABLE")
        if expected.get("reason_code") and observation.get("reason_code") != expected["reason_code"]:
            errors.append("REASON_CODE_MISMATCH")
        if disposition == "FAIL_CLOSED" and observation.get("retry_authorized"):
            errors.append("TERMINAL_FAIL_CLOSED_RETRY_FORBIDDEN")
    if expected.get("needs_predecessor") and disposition == "ALLOW":
        if not observation.get("predecessor_receipt_hash"):
            errors.append("MISSING_PREDECESSOR_LINK")
    if not observation.get("manifest_sha256") or not observation.get("route_decision_receipt_id"):
        errors.append("MISSING_MANIFEST_OR_DECISION_RECEIPT")
    elapsed = observation.get("route_decision_elapsed_seconds")
    if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or not math.isfinite(elapsed) or elapsed < 0:
        errors.append("MISSING_OR_INVALID_ROUTE_DECISION_LATENCY")
    cost = observation.get("full_lifecycle_cost")
    if cost is None:
        errors.append("COST_BASIS_UNDECLARED")
    elif not isinstance(cost, dict) or cost.get("status") not in {"UNKNOWN", "OBSERVED_COMPLETE", "PARTIAL"}:
        errors.append("INVALID_COST_STATUS")
    elif cost["status"] == "UNKNOWN" and cost.get("total_usd") is not None:
        errors.append("UNKNOWN_COST_MUST_NOT_BE_ZERO_OR_NUMERIC")
    elif cost["status"] == "PARTIAL" and cost.get("total_usd") is not None:
        errors.append("PARTIAL_COST_MUST_NOT_CLAIM_FULL_TOTAL")
    elif cost["status"] == "OBSERVED_COMPLETE":
        total = cost.get("total_usd")
        if (not isinstance(total, (int, float)) or isinstance(total, bool)
                or not math.isfinite(total) or total < 0):
            errors.append("COMPLETE_COST_REQUIRES_NONNEGATIVE_MEASUREMENT")
        if not cost.get("basis_refs"):
            errors.append("COMPLETE_COST_MISSING_PROVENANCE")
    # An observation can pass oracle/schema adjudication without real runtime proof.
    # Only independently verified Master Records custody and runtime receipts
    # can elevate it; this tool never performs such verification.
    return {
        "case_id": case["id"],
        "source_adjudication": "PASS" if not errors else "FAIL",
        "errors": errors,
        "authentic_runtime_state": "NOT_VERIFIED_BY_OFFLINE_ADJUDICATOR",
        "cost_status": cost.get("status") if isinstance(cost, dict) else "UNDECLARED",
    }


def evaluate(dataset: dict, observations: dict) -> dict:
    if dataset.get("schema") != "stegverse.sv-cost-held-out-cases/v1":
        raise ValueError("unsupported held-out dataset schema")
    cases = dataset.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("no held-out cases")
    if len({case["id"] for case in cases}) != len(cases):
        raise ValueError("duplicate held-out case identity")
    if not isinstance(observations, dict):
        raise ValueError("observation map must be an object")
    rows = [adjudicate(case, observations.get(case["id"], {})) for case in cases]
    return {
        "schema": "stegverse.sv-cost-held-out-offline-adjudication/v1",
        "claim_boundary": "SOURCE_ONLY_NO_LIVE_ROUTING_OR_MASTER_RECORDS_PROOF",
        "evaluated": len(rows),
        "passed": sum(row["source_adjudication"] == "PASS" for row in rows),
        "cases": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observations", type=Path, help="Separate offline route-observation map keyed by case ID")
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(json.loads(args.cases.read_text()), json.loads(args.observations.read_text()))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0 if result["passed"] == result["evaluated"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
