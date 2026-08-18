#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


class TestLaneEvidenceError(ValueError):
    pass


READY_STATES = {"READY_LOCAL_PRIMARY", "READY_FOR_TVC_EXECUTION"}
SKIP_STATES = {"SKIPPED_OPTIONAL_CREDENTIAL_UNBOUND"}

_PROHIBITED_FIELD_NAMES = {
    "api_key",
    "apikey",
    "authorization",
    "bearer_token",
    "credential",
    "credential_ref",
    "credential_value",
    "password",
    "secret",
    "secret_value",
    "token",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise TestLaneEvidenceError(message)


def _reject_secret_fields(value: Any, path: str = "evidence") -> None:
    if isinstance(value, Mapping):
        for raw_key, child in value.items():
            key = str(raw_key).strip().lower().replace("-", "_")
            if key in _PROHIBITED_FIELD_NAMES:
                raise TestLaneEvidenceError(f"credential-bearing evidence field prohibited: {path}.{raw_key}")
            _reject_secret_fields(child, f"{path}.{raw_key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_secret_fields(child, f"{path}[{index}]")


def output_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def validate_lane_evidence(request: Mapping[str, Any], evidence: Mapping[str, Any]) -> dict[str, Any]:
    _reject_secret_fields(evidence)
    _require(evidence.get("schema") == "stegverse.test-lane-evidence.v1", "lane evidence schema mismatch")
    for field in ("test_id", "lane_id", "request_hash", "provider", "provider_role", "mode", "task_source_blob_sha"):
        _require(evidence.get(field) == request.get(field if field != "task_source_blob_sha" else "task_source_blob_sha"), f"lane evidence/request mismatch: {field}")
    _require(evidence.get("credential_material_present") is False, "credential material prohibited in lane evidence")
    _require(evidence.get("execution_authority_granted") is False, "lane evidence cannot grant execution authority")
    text = evidence.get("output")
    _require(isinstance(text, str), "lane output must be string")
    _require(evidence.get("output_hash") == output_hash(text), "lane output hash mismatch")
    latency = evidence.get("latency_ms")
    _require(isinstance(latency, (int, float)) and latency >= 0, "non-negative latency_ms required")
    if request.get("model") is not None:
        _require(evidence.get("model") == request.get("model"), "lane model mismatch")
    if request.get("mode") == "GOVERNED":
        governance = evidence.get("governance")
        _require(isinstance(governance, Mapping), "governed lane requires governance evidence")
        _require(governance.get("profile") == request.get("governance_profile"), "governance profile mismatch")
        _require(isinstance(governance.get("outcome"), str) and governance.get("outcome"), "governance outcome required")
    return dict(evidence)


def compare(plan: Mapping[str, Any], evidence_bundle: Mapping[str, Any]) -> dict[str, Any]:
    _require(plan.get("schema") == "stegverse.test-lanes-plan.v1", "plan schema mismatch")
    _require(plan.get("credential_material_present") is False, "credential-bearing plan prohibited")
    _require(plan.get("primary_provider") == "stegverse_local", "StegVerse local must remain primary")
    _require(plan.get("state") == "READY", "comparison requires fully resolved READY plan")

    _reject_secret_fields(evidence_bundle)
    _require(evidence_bundle.get("schema") == "stegverse.test-lanes-evidence-bundle.v1", "evidence bundle schema mismatch")
    _require(evidence_bundle.get("test_id") == plan.get("test_id"), "evidence bundle test_id mismatch")
    _require(evidence_bundle.get("plan_hash") == plan.get("plan_hash"), "evidence bundle plan_hash mismatch")
    _require(evidence_bundle.get("credential_material_present") is False, "credential material prohibited in evidence bundle")
    evidence_items = evidence_bundle.get("lanes")
    _require(isinstance(evidence_items, list), "evidence bundle lanes must be list")

    evidence_by_lane: dict[str, Mapping[str, Any]] = {}
    for item in evidence_items:
        _require(isinstance(item, Mapping), "lane evidence must be object")
        lane_id = item.get("lane_id")
        _require(isinstance(lane_id, str) and lane_id, "lane evidence lane_id required")
        _require(lane_id not in evidence_by_lane, f"duplicate lane evidence: {lane_id}")
        evidence_by_lane[lane_id] = item

    results: list[dict[str, Any]] = []
    blockers: list[str] = []
    for request in plan.get("lanes") or []:
        _require(isinstance(request, Mapping), "plan lane request must be object")
        lane_id = request.get("lane_id")
        state = request.get("state")
        item = evidence_by_lane.get(lane_id)
        if state in READY_STATES:
            if item is None:
                blockers.append(f"MISSING_READY_LANE_EVIDENCE:{lane_id}")
                continue
            validated = validate_lane_evidence(request, item)
            results.append({
                "lane_id": lane_id,
                "provider": validated["provider"],
                "provider_role": validated["provider_role"],
                "mode": validated["mode"],
                "model": validated.get("model"),
                "output_hash": validated["output_hash"],
                "latency_ms": validated["latency_ms"],
                "usage": validated.get("usage"),
                "cost": validated.get("cost"),
                "governance_outcome": (validated.get("governance") or {}).get("outcome") if isinstance(validated.get("governance"), Mapping) else None,
            })
        elif state in SKIP_STATES:
            if item is not None:
                blockers.append(f"EVIDENCE_PRESENT_FOR_SKIPPED_LANE:{lane_id}")
            results.append({
                "lane_id": lane_id,
                "provider": request.get("provider"),
                "provider_role": request.get("provider_role"),
                "mode": request.get("mode"),
                "state": state,
            })
        else:
            blockers.append(f"PLAN_LANE_NOT_EXECUTION_FINAL:{lane_id}:{state}")

    extra = sorted(set(evidence_by_lane) - {str(item.get("lane_id")) for item in (plan.get("lanes") or []) if isinstance(item, Mapping)})
    blockers.extend(f"UNPLANNED_LANE_EVIDENCE:{lane_id}" for lane_id in extra)

    primary_results = [item for item in results if item.get("provider_role") == "PRIMARY" and "output_hash" in item]
    _require(len(primary_results) == 1, "exactly one executed PRIMARY lane required")
    primary_hash = primary_results[0]["output_hash"]
    for item in results:
        if "output_hash" in item:
            item["matches_primary_output"] = item["output_hash"] == primary_hash

    state = "PASS" if not blockers else "BLOCKED"
    summary = {
        "schema": "stegverse.test-lanes-comparison.v1",
        "state": state,
        "test_id": plan.get("test_id"),
        "plan_hash": plan.get("plan_hash"),
        "primary_provider": "stegverse_local",
        "credential_material_present": False,
        "lane_count_planned": len(plan.get("lanes") or []),
        "lane_evidence_count": len(evidence_items),
        "blockers": blockers,
        "results": results,
    }
    summary["comparison_hash"] = canonical_hash(summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate sanitized StegVerse Test Lanes evidence and produce a deterministic comparison.")
    parser.add_argument("plan")
    parser.add_argument("evidence")
    parser.add_argument("--output")
    args = parser.parse_args()
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    result = compare(plan, evidence)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["state"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
