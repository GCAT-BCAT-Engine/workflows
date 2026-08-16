#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import time
from typing import Any

ROOT = pathlib.Path(__file__).parent
TASK = json.loads((ROOT / "task.json").read_text())
INPUTS = ROOT / "candidate-inputs"
OUT = ROOT / "results" / "generation-2-output-boundary"
RECEIPTS = OUT / "receipts"
OUT.mkdir(parents=True, exist_ok=True)
RECEIPTS.mkdir(parents=True, exist_ok=True)

PROVIDERS = ("openai", "anthropic", "deepseek")


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(value).encode()).hexdigest()


def reconstruct() -> dict[str, Any]:
    state = dict(TASK["initial_state"])
    decisions: list[dict[str, str]] = []
    reasons = {
        "credit": "CREDIT_APPLIED",
        "debit_allow": "DEBIT_WITHIN_BOUNDARY",
        "debit_deny": "MINIMUM_BALANCE_VIOLATION",
        "risk_allow": "RISK_WITHIN_BOUNDARY",
        "risk_deny": "MAXIMUM_RISK_VIOLATION",
    }
    for event in TASK["events"]:
        op, amount, eid = event["operation"], event["amount"], event["event_id"]
        if op == "credit":
            state["balance"] += amount
            status, reason = "ALLOW", reasons["credit"]
        elif op == "debit":
            allowed = (
                state["standing"] == TASK["policy"]["standing_required_for_debit"]
                and state["balance"] - amount >= TASK["policy"]["minimum_balance"]
            )
            status = "ALLOW" if allowed else "DENY"
            reason = reasons["debit_allow"] if allowed else reasons["debit_deny"]
            if allowed:
                state["balance"] -= amount
        elif op == "risk_add":
            allowed = state["risk_score"] + amount <= TASK["policy"]["maximum_risk_score"]
            status = "ALLOW" if allowed else "DENY"
            reason = reasons["risk_allow"] if allowed else reasons["risk_deny"]
            if allowed:
                state["risk_score"] += amount
        else:
            raise ValueError(f"unsupported operation {op}")
        decisions.append({"event_id": eid, "status": status, "reason": reason})
    return {
        "task_id": TASK["task_id"],
        "final_state": state,
        "decisions": decisions,
        "applied_count": sum(x["status"] == "ALLOW" for x in decisions),
        "denied_count": sum(x["status"] == "DENY" for x in decisions),
        "claim_boundary": "DETERMINISTIC_RECONSTRUCTION_ONLY",
    }


EXPECTED = reconstruct()
EXPECTED_HASH = sha(EXPECTED)


def normalize(answer: dict[str, Any]) -> dict[str, Any]:
    final_state = answer.get("final_state") or {
        "balance": answer.get("final_balance"),
        "risk_score": answer.get("final_risk_score"),
        "standing": answer.get("final_standing"),
    }
    raw_decisions = answer.get("decisions") or answer.get("event_decisions") or []
    decisions = []
    reason_by_event = {x["event_id"]: x["reason"] for x in EXPECTED["decisions"]}
    for item in raw_decisions:
        if not isinstance(item, dict):
            continue
        eid = item.get("event_id") or item.get("id")
        decisions.append({
            "event_id": eid,
            "status": str(item.get("status") or item.get("decision") or "").upper(),
            "reason": item.get("reason") or reason_by_event.get(eid),
        })
    return {
        "task_id": answer.get("task_id") or TASK["task_id"],
        "final_state": final_state,
        "decisions": decisions,
        "applied_count": answer.get("applied_count", sum(x["status"] == "ALLOW" for x in decisions)),
        "denied_count": answer.get("denied_count", sum(x["status"] == "DENY" for x in decisions)),
        "claim_boundary": answer.get("claim_boundary", "DETERMINISTIC_RECONSTRUCTION_ONLY"),
    }


def validate(normalized: dict[str, Any]) -> tuple[bool, list[str]]:
    failures = []
    for key in ("task_id", "final_state", "decisions", "applied_count", "denied_count"):
        if normalized.get(key) != EXPECTED.get(key):
            failures.append("MISMATCH_" + key.upper())
    return not failures, failures


def provider_cost(provider: str, usage: dict[str, Any]) -> float | None:
    in_tokens = usage.get("input_tokens")
    out_tokens = usage.get("output_tokens")
    if in_tokens is None or out_tokens is None:
        return usage.get("reported_cost_usd")
    card = TASK["price_card"]
    in_rate = card.get(f"{provider}_input_usd_per_million")
    out_rate = card.get(f"{provider}_output_usd_per_million")
    if in_rate is None or out_rate is None:
        return usage.get("reported_cost_usd")
    return round((int(in_tokens) * float(in_rate) + int(out_tokens) * float(out_rate)) / 1_000_000, 12)


def write_receipt(name: str, receipt: dict[str, Any]) -> str:
    path = RECEIPTS / f"{name}.json"
    path.write_text(json.dumps(receipt, indent=2) + "\n")
    return str(path.relative_to(ROOT))


def ingest(provider: str, payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if payload.get("provider") != provider:
        raise ValueError(f"provider mismatch: expected {provider}")
    if payload.get("task_id") != TASK["task_id"]:
        raise ValueError("task identity mismatch")
    if payload.get("provider_api_key_transferred_to_stegverse") is not False:
        raise ValueError("candidate must assert provider_api_key_transferred_to_stegverse=false")
    candidate = payload.get("candidate_output")
    if not isinstance(candidate, dict):
        raise ValueError("candidate_output must be an object")

    candidate_hash = sha(candidate)
    normalized = normalize(candidate)
    raw_ok, raw_failures = validate(normalized)
    cost = provider_cost(provider, payload.get("provider_usage", {}))

    raw_row = {
        "lane_id": f"{provider}-raw",
        "provider": provider,
        "model": payload.get("model"),
        "source_mode": "EXTERNAL_PROVIDER_CANDIDATE",
        "stegverse_provider_credential_possession": False,
        "candidate_hash": candidate_hash,
        "provider_response_id": payload.get("provider_response_id"),
        "provider_response_hash": payload.get("provider_response_hash"),
        "provider_latency_seconds": payload.get("provider_latency_seconds"),
        "provider_usage": payload.get("provider_usage", {}),
        "provider_cost_usd": cost,
        "admissible_against_test_contract": raw_ok,
        "gate_failures": raw_failures,
        "required_output_hash": EXPECTED_HASH,
        "normalized_output_hash": sha(normalized),
    }

    started = time.perf_counter()
    governed_ok, governed_failures = validate(normalized)
    decision = "ALLOW" if governed_ok else "DENY"
    governance_latency = time.perf_counter() - started
    governance_receipt = {
        "schema": "stegverse.output-boundary-governance-receipt.v1",
        "experiment_id": TASK["experiment_id"],
        "task_id": TASK["task_id"],
        "provider": provider,
        "candidate_hash": candidate_hash,
        "normalized_candidate_hash": sha(normalized),
        "required_output_hash": EXPECTED_HASH,
        "decision": decision,
        "failures": governed_failures,
        "provider_api_key_observed_by_stegverse": False,
        "credential_authority": "EXTERNAL_PROVIDER_RELATIONSHIP_OR_TV_TVC",
        "governance_latency_seconds": governance_latency,
    }
    receipt_path = write_receipt(f"{provider}-governance", governance_receipt)

    replay_started = time.perf_counter()
    replay_normalized = normalize(candidate)
    replay_ok, replay_failures = validate(replay_normalized)
    replay_latency = time.perf_counter() - replay_started
    replay_receipt = {
        "schema": "stegverse.replay-receipt.v1",
        "source_governance_receipt_hash": sha(governance_receipt),
        "candidate_hash": candidate_hash,
        "replay_output_hash": sha(replay_normalized),
        "required_output_hash": EXPECTED_HASH,
        "replay_match": replay_ok,
        "failures": replay_failures,
        "latency_seconds": replay_latency,
    }
    replay_path = write_receipt(f"{provider}-replay", replay_receipt)

    reconstruction_started = time.perf_counter()
    reconstructed = reconstruct()
    reconstruction_latency = time.perf_counter() - reconstruction_started
    reconstruction_receipt = {
        "schema": "stegverse.reconstruction-receipt.v1",
        "task_contract_hash": sha({k: TASK[k] for k in ("task_id", "initial_state", "policy", "events", "decision_rules")}),
        "reconstructed_output_hash": sha(reconstructed),
        "required_output_hash": EXPECTED_HASH,
        "reconstruction_match": reconstructed == EXPECTED,
        "latency_seconds": reconstruction_latency,
    }
    reconstruction_path = write_receipt(f"{provider}-reconstruction", reconstruction_receipt)

    receipt_bytes = sum((ROOT / p).stat().st_size for p in (receipt_path, replay_path, reconstruction_path))
    local_rate = float(TASK["price_card"]["local_linux_runner_usd_per_minute"])
    storage_rate = float(TASK["price_card"]["local_storage_usd_per_gb_month"])
    governance_compute_cost = (governance_latency + replay_latency + reconstruction_latency) * (local_rate / 60)
    governance_storage_cost = (receipt_bytes / 1_000_000_000) * storage_rate
    governance_cost = governance_compute_cost + governance_storage_cost

    governed_row = {
        "lane_id": f"{provider}-governed",
        "provider": provider,
        "model": payload.get("model"),
        "source_mode": "SAME_EXTERNAL_PROVIDER_CANDIDATE_PLUS_STEGVERSE_OUTPUT_BOUNDARY",
        "stegverse_provider_credential_possession": False,
        "candidate_hash": candidate_hash,
        "decision": decision,
        "admissible": governed_ok,
        "gate_failures": governed_failures,
        "provider_cost_usd": cost,
        "governance_compute_cost_usd": round(governance_compute_cost, 12),
        "governance_storage_cost_usd": round(governance_storage_cost, 12),
        "governance_incremental_cost_usd": round(governance_cost, 12),
        "total_cost_usd": round(cost + governance_cost, 12) if cost is not None else None,
        "governance_receipt": receipt_path,
        "replay_receipt": replay_path,
        "reconstruction_receipt": reconstruction_path,
        "replay_match": replay_ok,
        "reconstruction_match": reconstructed == EXPECTED,
        "required_output_hash": EXPECTED_HASH,
        "normalized_output_hash": sha(normalized),
    }
    return raw_row, governed_row


rows: list[dict[str, Any]] = []
blockers: list[str] = []
for provider in PROVIDERS:
    source = INPUTS / f"{provider}.json"
    if not source.exists():
        blockers.append(f"MISSING_EXTERNAL_CANDIDATE:{source.relative_to(ROOT)}")
        continue
    try:
        raw_row, governed_row = ingest(provider, json.loads(source.read_text()))
        rows.extend((raw_row, governed_row))
    except Exception as exc:
        blockers.append(f"INVALID_EXTERNAL_CANDIDATE:{provider}:{exc}")

started = time.perf_counter()
stegverse_output = reconstruct()
stegverse_latency = time.perf_counter() - started
stegverse_bytes = len(canon(stegverse_output).encode())
stegverse_compute = stegverse_latency * (float(TASK["price_card"]["local_linux_runner_usd_per_minute"]) / 60)
stegverse_storage = (stegverse_bytes / 1_000_000_000) * float(TASK["price_card"]["local_storage_usd_per_gb_month"])
rows.append({
    "lane_id": "stegverse-only",
    "provider": "stegverse",
    "model": "deterministic-state-reconstructor-v2",
    "source_mode": "STEGVERSE_ONLY_RECONSTRUCTION",
    "stegverse_provider_credential_possession": False,
    "admissible": stegverse_output == EXPECTED,
    "required_output_hash": EXPECTED_HASH,
    "normalized_output_hash": sha(stegverse_output),
    "provider_cost_usd": 0.0,
    "governance_incremental_cost_usd": round(stegverse_compute + stegverse_storage, 12),
    "total_cost_usd": round(stegverse_compute + stegverse_storage, 12),
})

complete = not blockers and len(rows) == 7
result = {
    "schema_version": "2.0.0",
    "experiment_id": TASK["experiment_id"],
    "generation": "GENERATION_2_CREDENTIALLESS_OUTPUT_BOUNDARY",
    "comparison_unit": TASK["comparison_unit"],
    "credential_invariant": "NO_PROVIDER_API_KEY_POSSESSED_OR_CONSUMED_BY_STEGVERSE_TEST_WORKLOAD",
    "production_artifact_reference": TASK["production_artifact_reference"],
    "required_output_hash": EXPECTED_HASH,
    "rows": rows,
    "blockers": blockers,
    "all_seven_present": complete,
    "publication_status": "RESULTS_READY_FOR_BOUNDED_PUBLICATION" if complete and all(row.get("admissible", row.get("admissible_against_test_contract")) for row in rows) else "PUBLICATION_BLOCKED",
    "claim_boundary": TASK["claim_boundary"],
}
(OUT / "seven_lane_generation_2_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(result["publication_status"])
raise SystemExit(0 if complete else 3)
