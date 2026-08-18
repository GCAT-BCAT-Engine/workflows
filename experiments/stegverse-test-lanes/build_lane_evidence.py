#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


class LaneEvidenceBuildError(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_json(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def digest_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise LaneEvidenceBuildError(message)


def load(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, Mapping), f"JSON object required: {path}")
    return value


def normalize_sv_recon(candidate_text: str, task: Mapping[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        answer = json.loads(candidate_text)
    except Exception:
        return None, ["CANDIDATE_NOT_JSON"]
    if not isinstance(answer, Mapping):
        return None, ["CANDIDATE_NOT_OBJECT"]
    required = task.get("required_output")
    require(isinstance(required, Mapping), "SV-RECON task required_output missing")
    fs = answer.get("final_state") or {
        "balance": answer.get("final_balance"),
        "risk_score": answer.get("final_risk_score"),
        "standing": answer.get("final_standing"),
    }
    reason_by_event = {
        str(item.get("event_id")): item.get("reason")
        for item in required.get("decisions") or []
        if isinstance(item, Mapping)
    }
    decisions = []
    for item in answer.get("decisions") or answer.get("event_decisions") or []:
        if isinstance(item, Mapping):
            event_id = item.get("event_id") or item.get("id")
            decisions.append({
                "event_id": event_id,
                "status": str(item.get("status") or item.get("decision") or "").upper(),
                "reason": item.get("reason") or reason_by_event.get(str(event_id)),
            })
    normalized = {
        "task_id": answer.get("task_id") or task.get("task_id"),
        "final_state": fs,
        "decisions": decisions,
        "applied_count": answer.get("applied_count", sum(item.get("status") == "ALLOW" for item in decisions)),
        "denied_count": answer.get("denied_count", sum(item.get("status") == "DENY" for item in decisions)),
        "claim_boundary": answer.get("claim_boundary", "DETERMINISTIC_RECONSTRUCTION_ONLY"),
    }
    failures = [
        "MISMATCH_" + key.upper()
        for key in ("task_id", "final_state", "decisions", "applied_count", "denied_count")
        if normalized.get(key) != required.get(key)
    ]
    return normalized, failures


def governance_for(request: Mapping[str, Any], candidate_text: str, task: Mapping[str, Any]) -> Mapping[str, Any] | None:
    if request.get("mode") != "GOVERNED":
        return None
    profile = request.get("governance_profile")
    require(profile == "stegverse.default-governed.v1", "unsupported governance profile")
    require(task.get("task_id") == "SV-RECON-001", "default governed profile currently requires SV-RECON-001")
    normalized, failures = normalize_sv_recon(candidate_text, task)
    return {
        "profile": profile,
        "outcome": "ALLOW" if not failures else "DENY",
        "failures": failures,
        "candidate_hash": digest_text(candidate_text),
        "normalized_output_hash": digest_json(normalized) if normalized is not None else None,
        "required_output_hash": digest_json(task["required_output"]),
        "credential_material_observed": False,
        "execution_authority_granted": False,
    }


def external_latency_ms(candidate: Mapping[str, Any]) -> float:
    receipt = candidate.get("use_receipt")
    if isinstance(receipt, Mapping):
        start = receipt.get("started_ns")
        finish = receipt.get("finished_ns")
        if isinstance(start, int) and isinstance(finish, int) and finish >= start:
            return (finish - start) / 1_000_000
    return 0.0


def request_index(plan: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    lanes = plan.get("lanes")
    require(isinstance(lanes, list), "plan lanes required")
    result: dict[str, Mapping[str, Any]] = {}
    for lane in lanes:
        require(isinstance(lane, Mapping), "plan lane must be object")
        lane_id = lane.get("lane_id")
        require(isinstance(lane_id, str) and lane_id, "lane_id required")
        require(lane_id not in result, f"duplicate lane_id: {lane_id}")
        result[lane_id] = lane
    return result


def build_bundle(
    *,
    plan: Mapping[str, Any],
    task: Mapping[str, Any],
    primary_candidate: Mapping[str, Any],
    external_candidates: list[Mapping[str, Any]],
) -> dict[str, Any]:
    require(plan.get("schema") == "stegverse.test-lanes-plan.v1", "plan schema mismatch")
    require(plan.get("state") == "READY", "evidence build requires READY plan")
    require(plan.get("primary_provider") == "stegverse_local", "StegVerse local must remain primary")
    require(plan.get("credential_material_present") is False, "credential-bearing plan prohibited")
    requests = request_index(plan)

    candidates_by_provider: dict[str, Mapping[str, Any]] = {}
    for candidate in external_candidates:
        require(candidate.get("schema") == "stegverse.tvc.test-lane-external-candidate.v1", "external candidate schema mismatch")
        require(candidate.get("plan_hash") == plan.get("plan_hash"), "external candidate plan mismatch")
        require(candidate.get("provider_role") == "CONTROL_OR_FALLBACK_ONLY", "external provider role drift")
        require(candidate.get("credential_material_present") is False, "external candidate credential material present")
        provider = candidate.get("provider")
        require(isinstance(provider, str) and provider and provider != "stegverse_local", "external provider identity invalid")
        require(provider not in candidates_by_provider, f"duplicate external provider candidate: {provider}")
        candidates_by_provider[provider] = candidate

    require(primary_candidate.get("schema") == "stegverse.test-lanes-primary-candidate.v1", "primary candidate schema mismatch")
    require(primary_candidate.get("plan_hash") == plan.get("plan_hash"), "primary candidate plan mismatch")
    require(primary_candidate.get("provider") == "stegverse_local", "primary candidate provider mismatch")
    require(primary_candidate.get("provider_role") == "PRIMARY", "primary candidate role mismatch")
    require(primary_candidate.get("credential_material_present") is False, "primary candidate credential material present")
    require(primary_candidate.get("third_party_inference_required") is False, "primary candidate used third-party inference")

    lane_evidence: list[dict[str, Any]] = []
    for lane_id, request in requests.items():
        state = request.get("state")
        require(state in {"READY_LOCAL_PRIMARY", "READY_FOR_TVC_EXECUTION"}, f"canonical 9/9 evidence cannot include non-ready lane: {lane_id}:{state}")
        if request.get("provider") == "stegverse_local":
            candidate = primary_candidate
            output = str(candidate.get("candidate_output") or "")
            latency_ms = float(candidate.get("latency_ms") or 0.0)
            usage = dict(candidate.get("provider_usage") or {})
            provider_evidence = {
                "model_hash": candidate.get("model_hash"),
                "credential_requirement": "NONE",
                "third_party_inference_required": False,
            }
        else:
            provider = str(request.get("provider"))
            candidate = candidates_by_provider.get(provider)
            require(isinstance(candidate, Mapping), f"missing external candidate: {provider}")
            require(lane_id in (candidate.get("lane_ids") or []), f"candidate does not bind lane: {lane_id}")
            output = str(candidate.get("candidate_output") or "")
            latency_ms = external_latency_ms(candidate)
            usage = dict(candidate.get("provider_usage") or {})
            provider_evidence = {
                "provider_response_id": candidate.get("provider_response_id"),
                "lease_receipt_sha256": candidate.get("lease_receipt_sha256"),
                "secret_material_returned": False,
            }
        require(output != "", f"candidate output missing: {lane_id}")
        governance = governance_for(request, output, task)
        evidence = {
            "schema": "stegverse.test-lane-evidence.v1",
            "test_id": plan.get("test_id"),
            "lane_id": lane_id,
            "request_hash": request.get("request_hash"),
            "provider": request.get("provider"),
            "provider_role": request.get("provider_role"),
            "mode": request.get("mode"),
            "model": candidate.get("model"),
            "task_source_blob_sha": request.get("task_source_blob_sha"),
            "output": output,
            "output_hash": digest_text(output),
            "latency_ms": latency_ms,
            "usage": usage,
            "cost": None,
            "governance": dict(governance) if governance is not None else None,
            "provider_evidence": provider_evidence,
            "credential_material_present": False,
            "execution_authority_granted": False,
        }
        lane_evidence.append(evidence)

    require(len(lane_evidence) == 9, "canonical run must produce exactly nine lane evidence records")
    bundle = {
        "schema": "stegverse.test-lanes-evidence-bundle.v1",
        "test_id": plan.get("test_id"),
        "plan_hash": plan.get("plan_hash"),
        "primary_provider": "stegverse_local",
        "credential_authority": "TV/TVC",
        "credential_material_present": False,
        "lane_count": 9,
        "lanes": lane_evidence,
    }
    bundle["evidence_bundle_sha256"] = digest_json(bundle)
    return bundle


def main() -> int:
    parser = argparse.ArgumentParser(description="Build nine sanitized Test Lanes evidence records from one StegVerse primary candidate and four TVC external candidates.")
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--task-json", required=True, type=Path)
    parser.add_argument("--primary-candidate", required=True, type=Path)
    parser.add_argument("--external-candidate", action="append", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = build_bundle(
            plan=load(args.plan),
            task=load(args.task_json),
            primary_candidate=load(args.primary_candidate),
            external_candidates=[load(path) for path in args.external_candidate],
        )
    except Exception as exc:
        print(json.dumps({"state": "FAIL_CLOSED", "reason": str(exc), "credential_material_present": False}, sort_keys=True))
        return 2
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"state": "EVIDENCE_BUNDLE_COMPLETE", "lane_count": result["lane_count"], "credential_material_present": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
