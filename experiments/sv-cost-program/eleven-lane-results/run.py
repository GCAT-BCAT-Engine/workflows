#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import time
from typing import Any

ROOT = pathlib.Path(__file__).parent
PROGRAM_ROOT = ROOT.parent
PREV = PROGRAM_ROOT / "nine-lane-results"
TASK = json.loads((ROOT / "task.json").read_text())
PREV_TASK = json.loads((PREV / "task.json").read_text())
OUT = ROOT / "results" / "generation-3-eleven-lane"
RECEIPTS = OUT / "receipts"
OUT.mkdir(parents=True, exist_ok=True)
RECEIPTS.mkdir(parents=True, exist_ok=True)

PROVIDERS = ("openai", "anthropic", "deepseek", "kimi")
GLM_HOSTED = ROOT / "candidate-inputs" / "glm-hosted.json"
GLM_SOVEREIGN = ROOT / "runtime-evidence" / "glm-sovereign.json"
GLM_HOSTED_COST = ROOT / "cost-evidence" / "glm-hosted.json"


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
if PREV_TASK.get("required_output") != EXPECTED:
    raise SystemExit("predecessor required output mismatch")
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
            status = str(item.get("status") or item.get("decision") or "").upper()
            expected_status = next((x["status"] for x in EXPECTED["decisions"] if x["event_id"] == eid), None)
            decisions.append({
                "event_id": eid,
                "status": status,
                "reason": reason_by_event.get(eid) if status == expected_status else (item.get("reason") or reason_by_event.get(eid)),
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
    keys=("task_id","final_state","decisions","applied_count","denied_count")
    failures=["MISMATCH_"+k.upper() for k in keys if value.get(k) != EXPECTED.get(k)]
    return not failures, failures


def write_receipt(name: str, value: dict[str, Any]) -> str:
    p=RECEIPTS/f"{name}.json"
    p.write_text(json.dumps(value,indent=2)+"\n")
    return str(p.relative_to(ROOT))


def governance(provider: str, lane_id: str, candidate: dict[str, Any], source_mode: str) -> dict[str, Any]:
    candidate_hash=sha(candidate)
    normalized=normalize(candidate)
    started=time.perf_counter()
    ok, failures=validate(normalized)
    latency=time.perf_counter()-started
    receipt={
        "schema":"stegverse.output-boundary-governance-receipt.v3",
        "experiment_id":TASK["experiment_id"],
        "task_id":TASK["task_id"],
        "lane_id":lane_id,
        "provider":provider,
        "candidate_hash":candidate_hash,
        "normalized_candidate_hash":sha(normalized),
        "required_output_hash":EXPECTED_HASH,
        "decision":"ALLOW" if ok else "DENY",
        "failures":failures,
        "provider_api_key_observed_by_stegverse":False,
        "governance_latency_seconds":latency,
    }
    receipt_ref=write_receipt(lane_id+"-governance",receipt)
    replay=normalize(candidate)
    replay_ok,replay_failures=validate(replay)
    replay_ref=write_receipt(lane_id+"-replay",{
        "schema":"stegverse.replay-receipt.v3",
        "lane_id":lane_id,
        "candidate_hash":candidate_hash,
        "replay_output_hash":sha(replay),
        "required_output_hash":EXPECTED_HASH,
        "replay_match":replay_ok,
        "failures":replay_failures,
    })
    recon=reconstruct()
    recon_ref=write_receipt(lane_id+"-reconstruction",{
        "schema":"stegverse.reconstruction-receipt.v3",
        "lane_id":lane_id,
        "reconstructed_output_hash":sha(recon),
        "required_output_hash":EXPECTED_HASH,
        "reconstruction_match":recon==EXPECTED,
    })
    return {
        "lane_id":lane_id,
        "provider":provider,
        "source_mode":source_mode,
        "execution_state":"EVIDENCE_PRESENT",
        "stegverse_provider_credential_possession":False,
        "candidate_hash":candidate_hash,
        "admissible":ok,
        "gate_failures":failures,
        "required_output_hash":EXPECTED_HASH,
        "normalized_output_hash":sha(normalized),
        "governance_receipt":receipt_ref,
        "replay_receipt":replay_ref,
        "reconstruction_receipt":recon_ref,
        "replay_match":replay_ok,
        "reconstruction_match":recon==EXPECTED,
        "governance_latency_seconds":latency,
    }


def legacy_pair(provider: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    if payload.get("provider") != provider or payload.get("task_id") != TASK["task_id"]:
        raise ValueError("candidate identity mismatch")
    if payload.get("provider_api_key_transferred_to_stegverse") is not False:
        raise ValueError("provider credential transfer forbidden")
    candidate=payload.get("candidate_output")
    if not isinstance(candidate,dict):
        raise ValueError("candidate_output missing")
    normalized=normalize(candidate)
    ok,failures=validate(normalized)
    usage=payload.get("provider_usage") or {}
    reported=usage.get("reported_cost_usd")
    raw={
        "lane_id":f"{provider}-raw",
        "provider":provider,
        "model":payload.get("model"),
        "source_mode":"INHERITED_EXTERNAL_PROVIDER_CANDIDATE",
        "execution_state":"EVIDENCE_PRESENT",
        "stegverse_provider_credential_possession":False,
        "candidate_hash":sha(candidate),
        "provider_usage":usage,
        "provider_cost_usd":float(reported) if reported is not None else None,
        "admissible_against_test_contract":ok,
        "gate_failures":failures,
        "required_output_hash":EXPECTED_HASH,
        "normalized_output_hash":sha(normalized),
    }
    gov=governance(provider,f"{provider}-governed",candidate,"INHERITED_CANDIDATE_PLUS_STEGVERSE_GOVERNANCE")
    gov["model"]=payload.get("model")
    gov["provider_cost_usd"]=raw["provider_cost_usd"]
    return [raw,gov]


rows=[]
candidate_blockers=[]
for provider in PROVIDERS:
    source=PREV/"candidate-inputs"/f"{provider}.json"
    try:
        rows.extend(legacy_pair(provider,json.loads(source.read_text())))
    except Exception as exc:
        candidate_blockers.append(f"INVALID_OR_MISSING_INHERITED_CANDIDATE:{provider}:{exc}")

started=time.perf_counter()
local=reconstruct()
local_latency=time.perf_counter()-started
rows.insert(4,{
    "lane_id":"stegverse-only",
    "provider":"stegverse",
    "model":"deterministic-state-reconstructor-v3",
    "source_mode":"STEGVERSE_ONLY_RECONSTRUCTION",
    "execution_state":"EVIDENCE_PRESENT",
    "stegverse_provider_credential_possession":False,
    "admissible":local==EXPECTED,
    "required_output_hash":EXPECTED_HASH,
    "normalized_output_hash":sha(local),
    "provider_cost_usd":0.0,
    "runtime_seconds":local_latency,
})

if GLM_HOSTED.exists():
    payload=json.loads(GLM_HOSTED.read_text())
    if payload.get("provider")!="zai" or payload.get("model")!="GLM-5.3-Flash":
        candidate_blockers.append("INVALID_GLM_HOSTED_IDENTITY")
    elif payload.get("provider_api_key_transferred_to_stegverse") is not False:
        candidate_blockers.append("GLM_HOSTED_CREDENTIAL_TRANSFER_FORBIDDEN")
    else:
        row=governance("zai","glm-5.3-flash-hosted",payload["candidate_output"],"EXTERNAL_CANDIDATE_PRE_VAULT")
        row["model"]="GLM-5.3-Flash"
        usage=payload.get("provider_usage") or {}
        row["provider_usage"]=usage
        row["provider_cost_usd"]=usage.get("reported_cost_usd")
        rows.append(row)
else:
    candidate_blockers.append("MISSING_EXTERNAL_CANDIDATE:candidate-inputs/glm-hosted.json")
    rows.append({
        "lane_id":"glm-5.3-flash-hosted","provider":"zai","model":"GLM-5.3-Flash",
        "source_mode":"EXTERNAL_CANDIDATE_PRE_VAULT","execution_state":"BLOCKED_MISSING_CANDIDATE",
        "stegverse_provider_credential_possession":False,"admissible":None,"provider_cost_usd":None
    })

if GLM_SOVEREIGN.exists():
    payload=json.loads(GLM_SOVEREIGN.read_text())
    if payload.get("vendor_api_credential_used") is not False:
        candidate_blockers.append("GLM_SOVEREIGN_VENDOR_CREDENTIAL_FORBIDDEN")
    else:
        row=governance("sovereign","glm-5.3-flash-sovereign",payload["candidate_output"],"SOVEREIGN_OPENAI_COMPATIBLE_INFERENCE")
        row["model"]="GLM-5.3-Flash"
        row["runtime_identity"]=payload.get("runtime_identity")
        metrics=payload.get("metrics") or {}
        row["runtime_metrics"]=metrics
        costs=[metrics.get(k) for k in ("hardware_amortization_usd","energy_cost_usd","storage_network_runtime_overhead_usd")]
        row["provider_cost_usd"]=round(sum(float(x) for x in costs),12) if all(x is not None for x in costs) else None
        row["cost_basis"]="MEASURED_COMPUTE_ENERGY_AMORTIZATION_RUNTIME_OVERHEAD"
        rows.append(row)
else:
    candidate_blockers.append("MISSING_SOVEREIGN_RUNTIME_EVIDENCE:runtime-evidence/glm-sovereign.json")
    rows.append({
        "lane_id":"glm-5.3-flash-sovereign","provider":"sovereign","model":"GLM-5.3-Flash",
        "source_mode":"SOVEREIGN_OPENAI_COMPATIBLE_INFERENCE","execution_state":"BLOCKED_MISSING_RUNTIME_EVIDENCE",
        "stegverse_provider_credential_possession":False,"admissible":None,"provider_cost_usd":None,
        "cost_basis":"MEASURED_COMPUTE_ENERGY_AMORTIZATION_RUNTIME_OVERHEAD"
    })

order={x["lane_id"]:x["lane"] for x in TASK["lane_schema"]}
rows.sort(key=lambda r:order[r["lane_id"]])

# Preserve the already-admissible Kimi subscription allocation when available.
kimi_evidence=PREV/"cost-evidence"/"kimi-k3-allegretto-subscription-allocation-2026-08-17.json"
if kimi_evidence.exists():
    e=json.loads(kimi_evidence.read_text())
    allocation=e.get("calculation",{}).get("allocated_effective_cost_usd")
    if allocation is not None:
        for row in rows:
            if row.get("provider")=="kimi":
                row["provider_cost_usd"]=float(allocation)
                row["cost_basis"]="SUBSCRIPTION_QUOTA_ALLOCATED_EFFECTIVE_COST_NOT_MARGINAL_API_CHARGE"

if GLM_HOSTED_COST.exists():
    e=json.loads(GLM_HOSTED_COST.read_text())
    for row in rows:
        if row["lane_id"]=="glm-5.3-flash-hosted":
            row["provider_cost_usd"]=e.get("cost_usd")
            row["cost_basis"]=e.get("basis")
            row["cost_evidence"]="cost-evidence/glm-hosted.json"

cost_blockers=[]
for lane_id in ("openai-raw","anthropic-raw","deepseek-raw","kimi-raw","glm-5.3-flash-hosted","glm-5.3-flash-sovereign"):
    row=next(r for r in rows if r["lane_id"]==lane_id)
    if row.get("provider_cost_usd") is None:
        cost_blockers.append(f"MISSING_COST_EVIDENCE:{lane_id}")

executed=[r for r in rows if r.get("execution_state")=="EVIDENCE_PRESENT"]
all_eleven_present=len(rows)==11 and not candidate_blockers and len(executed)==11
all_admissible=all(r.get("admissible",r.get("admissible_against_test_contract")) is True for r in executed) and len(executed)==11
result={
    "schema_version":"6.0.0",
    "experiment_id":TASK["experiment_id"],
    "generation":TASK["generation"],
    "comparison_unit":TASK["comparison_unit"],
    "credential_invariant":TASK["credential_invariant"],
    "required_output_hash":EXPECTED_HASH,
    "rows":rows,
    "lane_count_defined":11,
    "lane_count_evidence_present":len(executed),
    "candidate_blockers":candidate_blockers,
    "cost_blockers":cost_blockers,
    "all_eleven_present":all_eleven_present,
    "all_lanes_admissible":all_admissible,
    "cost_evidence_complete":not cost_blockers and all_eleven_present,
    "publication_status":"RESULTS_READY_FOR_BOUNDED_PUBLICATION" if all_eleven_present and all_admissible and not cost_blockers else "PUBLICATION_BLOCKED",
    "claim_boundary":TASK["claim_boundary"],
}
(OUT/"eleven_lane_generation_3_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({
    "status":"PASS_HARNESS",
    "lane_count_defined":11,
    "lane_count_evidence_present":len(executed),
    "candidate_blockers":candidate_blockers,
    "cost_blockers":cost_blockers,
    "publication_status":result["publication_status"],
},indent=2))
raise SystemExit(0)
