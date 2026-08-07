#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import hmac
import json
import pathlib
import socket
import sqlite3
import statistics
import tempfile
import time
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)
CANDIDATE = json.loads((ROOT / "execution_candidate.json").read_text())
PROFILE = json.loads((ROOT / "production-burden-profile.json").read_text())
ITERATIONS = int(PROFILE["iterations"])
RUNNER_RATE = float(PROFILE["runner_rate_usd_per_minute"])
STORAGE_RATE = float(PROFILE["storage_rate_usd_per_gb_month"])
SECRET = b"steggate-bounded-benchmark-key-v1"
MEMBERS = [b"quorum-a", b"quorum-b", b"quorum-c"]


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha(value: Any) -> str:
    return sha_bytes(canon(value))


def mac(data: bytes, key: bytes = SECRET) -> str:
    return hmac.new(key, data, hashlib.sha256).hexdigest()


def base_checks(candidate: dict[str, Any]) -> tuple[bool, dict[str, bool]]:
    expected = candidate["expected"]
    decisions = candidate["decisions"]
    applied = sum(x["status"] == "ALLOW" for x in decisions)
    denied = sum(x["status"] == "DENY" for x in decisions)
    checks = {
        "authority_valid": candidate["actor"].get("authority_class") == "BOUNDED_TEST_EXECUTION",
        "delegation_present": bool(candidate["actor"].get("delegation_ref")),
        "policy_bound": bool(candidate.get("policy_ref")),
        "evidence_present": bool(candidate.get("evidence_refs")),
        "task_identity_valid": candidate.get("task_id") == expected.get("task_id"),
        "successor_matches": candidate.get("proposed_successor_state") == expected.get("final_state"),
        "decision_counts_match": applied == expected.get("applied_count") and denied == expected.get("denied_count"),
    }
    return all(checks.values()), checks


def build_receipt(candidate: dict[str, Any], checks: dict[str, bool], decision: str) -> dict[str, Any]:
    receipt = {
        "receipt_schema_version": "2.0.0",
        "candidate_id": candidate["candidate_id"],
        "task_id": candidate["task_id"],
        "candidate_hash": sha(candidate),
        "actor_id": candidate["actor"]["actor_id"],
        "delegation_ref": candidate["actor"]["delegation_ref"],
        "policy_ref": candidate["policy_ref"],
        "evidence_refs": candidate["evidence_refs"],
        "decision": decision,
        "checks": checks,
        "successor_state_hash": sha(candidate["proposed_successor_state"]),
    }
    return receipt


def verify_reconstruction(receipt: dict[str, Any], candidate: dict[str, Any]) -> bool:
    return (
        receipt["candidate_hash"] == sha(candidate)
        and receipt["successor_state_hash"] == sha(candidate["proposed_successor_state"])
        and receipt["task_id"] == candidate["task_id"]
    )


def proof_bundle(candidate: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    candidate_bytes = canon(candidate)
    receipt_bytes = canon(receipt)
    return {
        "candidate_mac": mac(candidate_bytes),
        "receipt_proofs": [mac(receipt_bytes, member) for member in MEMBERS],
    }


def verify_proofs(candidate: dict[str, Any], receipt: dict[str, Any], proofs: dict[str, Any]) -> bool:
    candidate_ok = hmac.compare_digest(proofs["candidate_mac"], mac(canon(candidate)))
    expected = [mac(canon(receipt), member) for member in MEMBERS]
    proof_ok = all(hmac.compare_digest(a, b) for a, b in zip(proofs["receipt_proofs"], expected))
    return candidate_ok and proof_ok


def lookup_artifacts(tmp: pathlib.Path, candidate: dict[str, Any]) -> bool:
    policy = {
        "ref": candidate["policy_ref"],
        "status": "ACTIVE",
        "allowed_authority_class": "BOUNDED_TEST_EXECUTION",
    }
    delegation = {
        "ref": candidate["actor"]["delegation_ref"],
        "status": "ACTIVE",
        "actor_id": candidate["actor"]["actor_id"],
    }
    policy_path = tmp / "policy.json"
    delegation_path = tmp / "delegation.json"
    policy_path.write_bytes(canon(policy))
    delegation_path.write_bytes(canon(delegation))
    expected_policy_hash = sha_bytes(policy_path.read_bytes())
    expected_delegation_hash = sha_bytes(delegation_path.read_bytes())
    loaded_policy = json.loads(policy_path.read_text())
    loaded_delegation = json.loads(delegation_path.read_text())
    return (
        loaded_policy["status"] == "ACTIVE"
        and loaded_delegation["status"] == "ACTIVE"
        and loaded_policy["ref"] == candidate["policy_ref"]
        and loaded_delegation["ref"] == candidate["actor"]["delegation_ref"]
        and sha_bytes(policy_path.read_bytes()) == expected_policy_hash
        and sha_bytes(delegation_path.read_bytes()) == expected_delegation_hash
    )


def persist_receipt(db: sqlite3.Connection, receipt: dict[str, Any]) -> bool:
    payload = canon(receipt)
    digest = sha_bytes(payload)
    db.execute(
        "INSERT OR REPLACE INTO receipts(candidate_id, payload, digest) VALUES(?,?,?)",
        (receipt["candidate_id"], payload, digest),
    )
    db.commit()
    row = db.execute(
        "SELECT payload, digest FROM receipts WHERE candidate_id=?",
        (receipt["candidate_id"],),
    ).fetchone()
    return bool(row) and row[1] == sha_bytes(row[0]) and row[1] == digest


def quorum_ok(receipt: dict[str, Any], approvals: int = 3) -> bool:
    payload = canon(receipt)
    proofs = [mac(payload, member) for member in MEMBERS[:approvals]]
    verified = 0
    for idx, proof in enumerate(proofs):
        if hmac.compare_digest(proof, mac(payload, MEMBERS[idx])):
            verified += 1
    return verified >= 2


def boundary_roundtrip(receipt: dict[str, Any]) -> bool:
    left, right = socket.socketpair()
    try:
        request = canon({"receipt": receipt, "digest": sha(receipt)})
        left.sendall(len(request).to_bytes(4, "big") + request)
        header = right.recv(4)
        size = int.from_bytes(header, "big")
        chunks = bytearray()
        while len(chunks) < size:
            chunks.extend(right.recv(size - len(chunks)))
        received = json.loads(bytes(chunks))
        response = canon({"accepted": received["digest"] == sha(received["receipt"]), "digest": received["digest"]})
        right.sendall(len(response).to_bytes(4, "big") + response)
        response_header = left.recv(4)
        response_size = int.from_bytes(response_header, "big")
        response_chunks = bytearray()
        while len(response_chunks) < response_size:
            response_chunks.extend(left.recv(response_size - len(response_chunks)))
        decoded = json.loads(bytes(response_chunks))
        return bool(decoded["accepted"]) and decoded["digest"] == sha(receipt)
    finally:
        left.close()
        right.close()


def execute_tier(tier: int, candidate: dict[str, Any], tmp: pathlib.Path, db: sqlite3.Connection) -> dict[str, Any]:
    start = time.perf_counter_ns()
    base_ok, checks = base_checks(candidate)
    receipt = build_receipt(candidate, checks, "ALLOW" if base_ok else "DENY")
    reconstruction_ok = verify_reconstruction(receipt, candidate)
    stage = {"core": base_ok and reconstruction_ok}

    proofs = None
    if tier >= 1:
        proofs = proof_bundle(candidate, receipt)
        stage["proof"] = verify_proofs(candidate, receipt, proofs)
    if tier >= 2:
        stage["lookup"] = lookup_artifacts(tmp, candidate)
    if tier >= 3:
        stage["persistence"] = persist_receipt(db, receipt)
    if tier >= 4:
        stage["quorum"] = quorum_ok(receipt, approvals=3)
    if tier >= 5:
        stage["boundary"] = boundary_roundtrip(receipt)

    admissible = all(stage.values()) and receipt["decision"] == "ALLOW"
    elapsed = time.perf_counter_ns() - start
    serialized = canon({"receipt": receipt, "proofs": proofs})
    return {
        "admissible": admissible,
        "stage_checks": stage,
        "elapsed_ns": elapsed,
        "receipt_bytes": len(serialized),
        "receipt_hash": sha(receipt),
    }


def negative_tests(tmp: pathlib.Path, db: sqlite3.Connection) -> dict[str, bool]:
    revoked = json.loads(json.dumps(CANDIDATE))
    revoked["actor"]["delegation_ref"] = ""
    revoked_result = execute_tier(5, revoked, tmp, db)

    tampered_state = json.loads(json.dumps(CANDIDATE))
    tampered_state["proposed_successor_state"]["balance"] = 999
    tampered_state_result = execute_tier(5, tampered_state, tmp, db)

    base_ok, checks = base_checks(CANDIDATE)
    receipt = build_receipt(CANDIDATE, checks, "ALLOW" if base_ok else "DENY")
    proofs = proof_bundle(CANDIDATE, receipt)
    proofs["candidate_mac"] = "0" * len(proofs["candidate_mac"])
    tampered_proof_denied = not verify_proofs(CANDIDATE, receipt, proofs)

    insufficient_quorum_denied = not quorum_ok(receipt, approvals=1)

    return {
        "revoked_delegation_denied": not revoked_result["admissible"],
        "tampered_successor_denied": not tampered_state_result["admissible"],
        "tampered_proof_denied": tampered_proof_denied,
        "insufficient_quorum_denied": insufficient_quorum_denied,
    }


def summary(values: list[int]) -> dict[str, float]:
    ordered = sorted(values)
    return {
        "mean_ns": statistics.fmean(ordered),
        "p50_ns": ordered[len(ordered) // 2],
        "p95_ns": ordered[int(len(ordered) * 0.95)],
        "min_ns": ordered[0],
        "max_ns": ordered[-1],
    }


rows = []
with tempfile.TemporaryDirectory(prefix="steggate-burden-") as temp_dir:
    tmp = pathlib.Path(temp_dir)
    db = sqlite3.connect(tmp / "receipts.sqlite")
    db.execute("CREATE TABLE receipts(candidate_id TEXT PRIMARY KEY, payload BLOB NOT NULL, digest TEXT NOT NULL)")

    for tier_def in PROFILE["tiers"]:
        tier = int(tier_def["tier"])
        samples = []
        reference = execute_tier(tier, CANDIDATE, tmp, db)
        assert reference["admissible"], (tier, reference)
        for _ in range(ITERATIONS):
            result = execute_tier(tier, CANDIDATE, tmp, db)
            assert result["admissible"], (tier, result)
            samples.append(result["elapsed_ns"])
        stats = summary(samples)
        mean_seconds = stats["mean_ns"] / 1e9
        compute_cost = mean_seconds * (RUNNER_RATE / 60)
        storage_cost = (reference["receipt_bytes"] / 1e9) * STORAGE_RATE
        rows.append({
            "tier": tier,
            "tier_id": tier_def["id"],
            "label": tier_def["label"],
            "components": tier_def["components"],
            "iterations": ITERATIONS,
            "admissible": True,
            "receipt_bytes": reference["receipt_bytes"],
            "latency": stats,
            "modeled_compute_cost_usd": compute_cost,
            "modeled_receipt_storage_cost_usd_per_month": storage_cost,
            "modeled_local_cost_usd_per_governed_action": compute_cost + storage_cost,
        })

    negatives = negative_tests(tmp, db)
    db.close()

assert all(negatives.values()), negatives
core_cost = rows[0]["modeled_local_cost_usd_per_governed_action"]
for row in rows:
    row["cost_multiple_vs_core"] = row["modeled_local_cost_usd_per_governed_action"] / core_cost if core_cost else None
    row["latency_multiple_vs_core"] = row["latency"]["mean_ns"] / rows[0]["latency"]["mean_ns"] if rows[0]["latency"]["mean_ns"] else None

result = {
    "schema_version": "1.0.0",
    "experiment_id": "SV-GOVERNED-AI-PRODUCTION-BURDEN-001",
    "profile_id": PROFILE["profile_id"],
    "candidate_id": CANDIDATE["candidate_id"],
    "operation_class": "post_inference_governance_production_burden_curve",
    "provider_inference_included": False,
    "tiers": rows,
    "negative_tests": negatives,
    "all_tiers_admissible": all(row["admissible"] for row in rows),
    "all_negative_cases_fail_closed": all(negatives.values()),
    "lowest_local_cost_tier": min(rows, key=lambda row: row["modeled_local_cost_usd_per_governed_action"])["tier_id"],
    "highest_local_cost_tier": max(rows, key=lambda row: row["modeled_local_cost_usd_per_governed_action"])["tier_id"],
    "claim_boundary": PROFILE["claim_boundary"],
}

(OUT / "production_burden_results.json").write_text(json.dumps(result, indent=2) + "\n")
report = [
    "# StegGate Production-Burden Curve",
    "",
    "Provider inference is excluded from every tier.",
    "",
    "| Tier | Path | Mean latency ms | p95 ms | Local modeled cost/action | Cost multiple vs core |",
    "|---:|---|---:|---:|---:|---:|",
]
for row in rows:
    report.append(
        f"| {row['tier']} | {row['label']} | {row['latency']['mean_ns']/1e6:.6f} | {row['latency']['p95_ns']/1e6:.6f} | "
        f"${row['modeled_local_cost_usd_per_governed_action']:.12f} | {row['cost_multiple_vs_core']:.3f}x |"
    )
report += [
    "",
    "## Fail-closed negative cases",
    "",
    *[f"- {name}: {'PASS' if passed else 'FAIL'}" for name, passed in negatives.items()],
    "",
    "The BOUNDARY tier is a local production-like approximation only. It uses local artifact retrieval, SQLite persistence, HMAC proof checks, a deterministic 2-of-3 quorum, and socketpair transport. It does not represent remote cloud/KMS/database/network/human-quorum latency or commercial operating expense.",
]
(OUT / "production_burden_report.md").write_text("\n".join(report) + "\n")
print("STEGGATE_PRODUCTION_BURDEN_READY")
