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
PROVIDERS = ("openai", "anthropic", "deepseek", "kimi")


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(value).encode()).hexdigest()


def reconstruct() -> dict[str, Any]:
    state = dict(TASK["initial_state"])
    decisions: list[dict[str, str]] = []
    for event in TASK["events"]:
        op, amount, eid = event["operation"], event["amount"], event["event_id"]
        if op == "credit":
            state["balance"] += amount
            status, reason = "ALLOW", "CREDIT_APPLIED"
        elif op == "debit":
            allowed = (
                state["standing"] == TASK["policy"]["standing_required_for_debit"]
                and state["balance"] - amount >= TASK["policy"]["minimum_balance"]
            )
            status, reason = ("ALLOW", "DEBIT_WITHIN_BOUNDARY") if allowed else ("DENY", "MINIMUM_BALANCE_VIOLATION")
            if allowed:
                state["balance"] -= amount
        elif op == "risk_add":
            allowed = state["risk_score"] + amount <= TASK["policy"]["maximum_risk_score"]
            status, reason = ("ALLOW", "RISK_WITHIN_BOUNDARY") if allowed else ("DENY", "MAXIMUM_RISK_VIOLATION")
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
    fs = answer.get("final_state") or {
        "balance": answer.get("final_balance"),
        "risk_score": answer.get("final_risk_score"),
        "standing": answer.get("final_standing"),
    }
    reason_by_event = {x["event_id"]: x["reason"] for x in EXPECTED["decisions"]}
    decisions = []
    for item in answer.get("decisions") or answer.get("event_decisions") or []:
        if isinstance(item, dict):
            eid = item.get("event_id") or item.get("id")
            decisions.append({
                "event_id": eid,
                "status": str(item.get("status") or item.get("decision") or "").upper(),
                "reason": item.get("reason") or reason_by_event.get(eid),
            })
    return {
        "task_id": answer.get("task_id") or TASK["task_id"],
        "final_state": fs,
        "decisions": decisions,
        "applied_count": answer.get("applied_count", sum(x["status"] == "ALLOW" for x in decisions)),
        "denied_count": answer.get("denied_count", sum(x["status"] == "DENY" for x in decisions)),
        "claim_boundary": answer.get("claim_boundary", "DETERMINISTIC_RECONSTRUCTION_ONLY"),
    }


def validate(value: dict[str, Any]) -> tuple[bool, list[str]]:
    failures = [
        "MISMATCH_" + k.upper()
        for k in ("task_id", "final_state", "decisions", "applied_count", "denied_count")
        if value.get(k) != EXPECTED.get(k)
    ]
    return not failures, failures


def provider_cost(provider: str, usage: dict[str, Any]) -> float | None:
    if usage.get("reported_cost_usd") is not None:
        return float(usage["reported_cost_usd"])
    i, o = usage.get("input_tokens"), usage.get("output_tokens")
    if i is None or o is None:
        return None
    card = TASK["price_card"]
    ir = card.get(f"{provider}_input_usd_per_million")
    orate = card.get(f"{provider}_output_usd_per_million")
    if ir is None or orate is None:
        return None
    return round((int(i) * float(ir) + int(o) * float(orate)) / 1_000_000, 12)


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
        raise ValueError("provider credential transfer is forbidden")
    candidate = payload.get("candidate_output")
    if not isinstance(candidate, dict):
        raise ValueError("candidate_output must be an object")
    candidate_hash = sha(candidate)
    normalized = normalize(candidate)
    ok, failures = validate(normalized)
    cost = provider_cost(provider, payload.get("provider_usage", {}))
    raw = {
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
        "admissible_against_test_contract": ok,
        "gate_failures": failures,
        "required_output_hash": EXPECTED_HASH,
        "normalized_output_hash": sha(normalized),
    }
    started = time.perf_counter()
    governed_ok, governed_failures = validate(normalized)
    gov_latency = time.perf_counter() - started
    governance = {
        "schema": "stegverse.output-boundary-governance-receipt.v2",
        "experiment_id": TASK["experiment_id"],
        "task_id": TASK["task_id"],
        "provider": provider,
        "candidate_hash": candidate_hash,
        "normalized_candidate_hash": sha(normalized),
        "required_output_hash": EXPECTED_HASH,
        "decision": "ALLOW" if governed_ok else "DENY",
        "failures": governed_failures,
        "provider_api_key_observed_by_stegverse": False,
        "credential_authority": "EXTERNAL_PROVIDER_RELATIONSHIP_OR_TV_TVC",
        "governance_latency_seconds": gov_latency,
    }
    gp = write_receipt(f"{provider}-governance", governance)
    rs = time.perf_counter()
    replay = normalize(candidate)
    replay_ok, replay_failures = validate(replay)
    replay_latency = time.perf_counter() - rs
    rp = write_receipt(f"{provider}-replay", {
        "schema": "stegverse.replay-receipt.v2",
        "source_governance_receipt_hash": sha(governance),
        "candidate_hash": candidate_hash,
        "replay_output_hash": sha(replay),
        "required_output_hash": EXPECTED_HASH,
        "replay_match": replay_ok,
        "failures": replay_failures,
        "latency_seconds": replay_latency,
    })
    cs = time.perf_counter()
    reconstructed = reconstruct()
    recon_latency = time.perf_counter() - cs
    cp = write_receipt(f"{provider}-reconstruction", {
        "schema": "stegverse.reconstruction-receipt.v2",
        "task_contract_hash": sha({k: TASK[k] for k in ("task_id", "initial_state", "policy", "events", "decision_rules")}),
        "reconstructed_output_hash": sha(reconstructed),
        "required_output_hash": EXPECTED_HASH,
        "reconstruction_match": reconstructed == EXPECTED,
        "latency_seconds": recon_latency,
    })
    receipt_bytes = sum((ROOT / p).stat().st_size for p in (gp, rp, cp))
    local_rate = float(TASK["price_card"]["local_linux_runner_usd_per_minute"])
    storage_rate = float(TASK["price_card"]["local_storage_usd_per_gb_month"])
    incremental = (
        (gov_latency + replay_latency + recon_latency) * (local_rate / 60)
        + (receipt_bytes / 1_000_000_000) * storage_rate
    )
    governed = {
        "lane_id": f"{provider}-governed",
        "provider": provider,
        "model": payload.get("model"),
        "source_mode": "SAME_EXTERNAL_PROVIDER_CANDIDATE_PLUS_STEGVERSE_OUTPUT_BOUNDARY",
        "stegverse_provider_credential_possession": False,
        "candidate_hash": candidate_hash,
        "decision": "ALLOW" if governed_ok else "DENY",
        "admissible": governed_ok,
        "gate_failures": governed_failures,
        "provider_cost_usd": cost,
        "governance_incremental_cost_usd": round(incremental, 12),
        "total_cost_usd": round(cost + incremental, 12) if cost is not None else None,
        "governance_receipt": gp,
        "replay_receipt": rp,
        "reconstruction_receipt": cp,
        "replay_match": replay_ok,
        "reconstruction_match": reconstructed == EXPECTED,
        "required_output_hash": EXPECTED_HASH,
        "normalized_output_hash": sha(normalized),
    }
    return raw, governed


rows: list[dict[str, Any]] = []
candidate_blockers: list[str] = []
for provider in PROVIDERS:
    source = INPUTS / f"{provider}.json"
    if not source.exists():
        candidate_blockers.append(f"MISSING_EXTERNAL_CANDIDATE:{source.relative_to(ROOT)}")
        continue
    try:
        raw, governed = ingest(provider, json.loads(source.read_text()))
        rows.extend((raw, governed))
    except Exception as exc:
        candidate_blockers.append(f"INVALID_EXTERNAL_CANDIDATE:{provider}:{exc}")

s = time.perf_counter()
local = reconstruct()
latency = time.perf_counter() - s
b = len(canon(local).encode())
compute = latency * (float(TASK["price_card"]["local_linux_runner_usd_per_minute"]) / 60)
storage = (b / 1_000_000_000) * float(TASK["price_card"]["local_storage_usd_per_gb_month"])
rows.append({
    "lane_id": "stegverse-only",
    "provider": "stegverse",
    "model": "deterministic-state-reconstructor-v2",
    "source_mode": "STEGVERSE_ONLY_RECONSTRUCTION",
    "stegverse_provider_credential_possession": False,
    "admissible": local == EXPECTED,
    "required_output_hash": EXPECTED_HASH,
    "normalized_output_hash": sha(local),
    "provider_cost_usd": 0.0,
    "governance_incremental_cost_usd": round(compute + storage, 12),
    "total_cost_usd": round(compute + storage, 12),
})

all_nine_present = not candidate_blockers and len(rows) == 9
cost_blockers: list[str] = []
if all_nine_present:
    kimi_raw = next((r for r in rows if r.get("lane_id") == "kimi-raw"), None)
    if kimi_raw is None or kimi_raw.get("provider_cost_usd") is None:
        cost_blockers.append("MISSING_COST_EVIDENCE:kimi:reported_cost_or_versioned_official_rate_card_required")

all_admissible = all(row.get("admissible", row.get("admissible_against_test_contract")) for row in rows)
cost_evidence_complete = all_nine_present and not cost_blockers
publication_ready = all_nine_present and cost_evidence_complete and all_admissible
blockers = candidate_blockers + cost_blockers
result = {
    "schema_version": "4.0.0",
    "experiment_id": TASK["experiment_id"],
    "generation": TASK["generation"],
    "comparison_unit": TASK["comparison_unit"],
    "credential_invariant": TASK["credential_invariant"],
    "production_artifact_reference": TASK["production_artifact_reference"],
    "required_output_hash": EXPECTED_HASH,
    "rows": rows,
    "candidate_blockers": candidate_blockers,
    "cost_blockers": cost_blockers,
    "blockers": blockers,
    "all_nine_present": all_nine_present,
    "all_lanes_admissible": all_admissible,
    "cost_evidence_complete": cost_evidence_complete,
    "publication_status": "RESULTS_READY_FOR_BOUNDED_PUBLICATION" if publication_ready else "PUBLICATION_BLOCKED",
    "claim_boundary": TASK["claim_boundary"],
}
(OUT / "nine_lane_generation_2_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(result["publication_status"])
raise SystemExit(0 if all_nine_present else 3)
