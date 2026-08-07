#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import statistics
import time
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)
CANDIDATE = json.loads((ROOT / "execution_candidate.json").read_text())

ITERATIONS = 20000
LOCAL_RUNNER_USD_PER_MINUTE = 0.008
LOCAL_STORAGE_USD_PER_GB_MONTH = 0.008


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(value)).hexdigest()


def steg_gate_once(candidate: dict[str, Any]) -> dict[str, Any]:
    t0 = time.perf_counter_ns()
    candidate_hash = sha(candidate)
    t1 = time.perf_counter_ns()

    expected = candidate["expected"]
    decisions = candidate["decisions"]
    applied_count = sum(item["status"] == "ALLOW" for item in decisions)
    denied_count = sum(item["status"] == "DENY" for item in decisions)

    authority_valid = (
        candidate["actor"]["authority_class"] == "BOUNDED_TEST_EXECUTION"
        and bool(candidate["actor"].get("delegation_ref"))
    )
    policy_bound = bool(candidate.get("policy_ref"))
    evidence_present = bool(candidate.get("evidence_refs"))
    successor_matches = candidate["proposed_successor_state"] == expected["final_state"]
    counts_match = applied_count == expected["applied_count"] and denied_count == expected["denied_count"]
    task_identity_valid = candidate["task_id"] == expected["task_id"]
    admissible = all([
        authority_valid,
        policy_bound,
        evidence_present,
        successor_matches,
        counts_match,
        task_identity_valid,
    ])
    t2 = time.perf_counter_ns()

    receipt = {
        "receipt_schema_version": "1.0.0",
        "candidate_id": candidate["candidate_id"],
        "task_id": candidate["task_id"],
        "candidate_hash": candidate_hash,
        "actor_id": candidate["actor"]["actor_id"],
        "authority_class": candidate["actor"]["authority_class"],
        "delegation_ref": candidate["actor"]["delegation_ref"],
        "policy_ref": candidate["policy_ref"],
        "evidence_refs": candidate["evidence_refs"],
        "decision": "ALLOW" if admissible else "DENY",
        "checks": {
            "authority_valid": authority_valid,
            "policy_bound": policy_bound,
            "evidence_present": evidence_present,
            "successor_matches": successor_matches,
            "counts_match": counts_match,
            "task_identity_valid": task_identity_valid,
        },
        "successor_state_hash": sha(candidate["proposed_successor_state"]),
    }
    receipt_hash = sha(receipt)
    t3 = time.perf_counter_ns()

    serialized = canon({"receipt": receipt, "receipt_hash": receipt_hash})
    t4 = time.perf_counter_ns()

    reconstructed = json.loads(serialized)
    reconstruction_valid = (
        reconstructed["receipt_hash"] == sha(reconstructed["receipt"])
        and reconstructed["receipt"]["candidate_hash"] == candidate_hash
        and reconstructed["receipt"]["decision"] == ("ALLOW" if admissible else "DENY")
    )
    t5 = time.perf_counter_ns()

    return {
        "admissible": admissible,
        "reconstruction_valid": reconstruction_valid,
        "receipt_bytes": len(serialized),
        "candidate_hash": candidate_hash,
        "receipt_hash": receipt_hash,
        "timings_ns": {
            "canonicalize_and_hash": t1 - t0,
            "authority_policy_admissibility": t2 - t1,
            "receipt_generation_and_hash": t3 - t2,
            "serialization": t4 - t3,
            "reconstruction_verification": t5 - t4,
            "total": t5 - t0,
        },
    }


samples = []
reference = steg_gate_once(CANDIDATE)
assert reference["admissible"] is True
assert reference["reconstruction_valid"] is True

for _ in range(ITERATIONS):
    sample = steg_gate_once(CANDIDATE)
    assert sample["admissible"] is True
    assert sample["reconstruction_valid"] is True
    samples.append(sample)


def summarize(key: str) -> dict[str, float]:
    values = sorted(sample["timings_ns"][key] for sample in samples)
    p50 = values[len(values) // 2]
    p95 = values[int(len(values) * 0.95)]
    mean = statistics.fmean(values)
    return {
        "mean_ns": mean,
        "p50_ns": p50,
        "p95_ns": p95,
        "min_ns": values[0],
        "max_ns": values[-1],
    }

stage_summary = {
    key: summarize(key)
    for key in [
        "canonicalize_and_hash",
        "authority_policy_admissibility",
        "receipt_generation_and_hash",
        "serialization",
        "reconstruction_verification",
        "total",
    ]
}

mean_total_seconds = stage_summary["total"]["mean_ns"] / 1e9
compute_cost_usd = mean_total_seconds * (LOCAL_RUNNER_USD_PER_MINUTE / 60)
storage_cost_usd = (reference["receipt_bytes"] / 1e9) * LOCAL_STORAGE_USD_PER_GB_MONTH
isolated_cost_usd = compute_cost_usd + storage_cost_usd

result = {
    "schema_version": "1.0.0",
    "experiment_id": "SV-GOVERNED-AI-STEGGATE-ISOLATION-001",
    "candidate_id": CANDIDATE["candidate_id"],
    "operation_class": "post_inference_governance_control_path",
    "iterations": ITERATIONS,
    "admissibility_result": reference["admissible"],
    "reconstruction_verification": reference["reconstruction_valid"],
    "candidate_hash": reference["candidate_hash"],
    "receipt_hash": reference["receipt_hash"],
    "receipt_bytes": reference["receipt_bytes"],
    "stage_latency": stage_summary,
    "modeled_cost": {
        "runner_rate_usd_per_minute": LOCAL_RUNNER_USD_PER_MINUTE,
        "storage_rate_usd_per_gb_month": LOCAL_STORAGE_USD_PER_GB_MONTH,
        "mean_compute_cost_usd_per_control_path": compute_cost_usd,
        "receipt_storage_cost_usd_per_receipt_month": storage_cost_usd,
        "isolated_modeled_steggate_core_cost_usd": isolated_cost_usd,
        "status": "MEASURED_RUNTIME_WITH_VERSIONED_DECLARED_INFRASTRUCTURE_RATES"
    },
    "included_components": [
        "canonicalization",
        "hashing",
        "bounded authority check",
        "policy binding presence check",
        "evidence presence check",
        "successor-state admissibility checks",
        "receipt generation",
        "receipt hashing",
        "serialization",
        "reconstruction verification"
    ],
    "excluded_components": [
        "provider inference",
        "provider adapter/network overhead",
        "remote policy retrieval",
        "remote delegation retrieval",
        "external signature verification",
        "database/network persistence latency",
        "multi-party quorum",
        "enterprise operations/support",
        "provider commercial margin"
    ],
    "claim_boundary": "This isolates one synthetic in-process StegGate core control path on a canonical post-inference candidate. It is not a production wholesale price, full StegGate service cost, enterprise ROI, or provider integration cost."
}

(OUT / "steggate_isolation_results.json").write_text(json.dumps(result, indent=2) + "\n")

report = [
    "# StegGate Core Isolation Test",
    "",
    f"Iterations: {ITERATIONS}",
    f"Admissible: {reference['admissible']}",
    f"Reconstruction valid: {reference['reconstruction_valid']}",
    f"Receipt bytes: {reference['receipt_bytes']}",
    f"Mean core-path latency: {mean_total_seconds:.12f} s",
    f"Modeled compute cost: ${compute_cost_usd:.12f}",
    f"Modeled receipt storage/month: ${storage_cost_usd:.12f}",
    f"Modeled isolated core-path cost: ${isolated_cost_usd:.12f}",
    "",
    "This result excludes provider inference, network/service integration, external policy/delegation retrieval, signatures, quorum, persistence/network latency, support, and commercial margin.",
]
(OUT / "steggate_isolation_report.md").write_text("\n".join(report) + "\n")
print("STEGGATE_ISOLATION_READY")
