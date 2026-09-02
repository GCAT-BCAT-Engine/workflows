#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

ROOT=Path(__file__).resolve().parents[1]
ALLOWED={"openai","anthropic","deepseek"}
FORBIDDEN={
    "authorization","api_key","apikey","bearer","bearer_token","password",
    "secret","secret_value","credential","credentials","private_key",
    "access_token","refresh_token","client_secret",
}


def reject_protected(value: Any, path: str="$") -> None:
    if isinstance(value,Mapping):
        for raw_key,child in value.items():
            key=str(raw_key).lower().replace("-","_")
            if key in FORBIDDEN or key.endswith(("_api_key","_password","_secret","_private_key","_access_token","_refresh_token")):
                raise ValueError(f"protected field prohibited: {path}.{raw_key}")
            reject_protected(child,f"{path}.{raw_key}")
    elif isinstance(value,list):
        for index,child in enumerate(value):
            reject_protected(child,f"{path}[{index}]")


def semantic_ok(candidate: Mapping[str,Any]) -> bool:
    expected_state={"balance":75,"risk_score":3,"standing":"active"}
    expected=[("E01","ALLOW"),("E02","ALLOW"),("E03","ALLOW"),("E04","DENY"),("E05","DENY"),("E06","ALLOW")]
    decisions=candidate.get("decisions") or []
    seq=[(x.get("event_id"),str(x.get("status") or "").upper()) for x in decisions if isinstance(x,Mapping)]
    return (
        candidate.get("task_id")=="SV-RECON-001"
        and candidate.get("final_state")==expected_state
        and seq==expected
        and candidate.get("applied_count")==4
        and candidate.get("denied_count")==2
        and candidate.get("claim_boundary")=="DETERMINISTIC_RECONSTRUCTION_ONLY"
    )


def standardized_usage(provider: str, normalized: Mapping[str,Any]) -> dict[str,int]:
    if provider=="openai":
        keys=("input_tokens","output_tokens","cached_input_tokens")
        result={k:int(normalized.get(k,0)) for k in keys}
    elif provider=="anthropic":
        result={
            "input_tokens":int(normalized.get("input_tokens",0)),
            "output_tokens":int(normalized.get("output_tokens",0)),
        }
    elif provider=="deepseek":
        result={
            "input_tokens":int(normalized.get("prompt_tokens",0)),
            "output_tokens":int(normalized.get("completion_tokens",0)),
            "cached_input_tokens":int(normalized.get("prompt_cache_hit_tokens",0)),
        }
    else:
        raise ValueError("provider not admitted")
    if any(v<0 for v in result.values()):
        raise ValueError("normalized usage must be nonnegative")
    return result


def install(source: Path, *, candidate_dest: Path|None=None, cost_dest: Path|None=None) -> dict[str,Any]:
    raw=json.loads(source.read_text())
    if not isinstance(raw,dict):
        raise ValueError("TVC evidence must be an object")
    reject_protected(raw)
    if raw.get("schema")!="stegverse.tvc.provider-measurement-evidence.v1":
        raise ValueError("unexpected TVC evidence schema")
    provider=str(raw.get("provider") or "")
    if provider not in ALLOWED:
        raise ValueError("provider not admitted for eleven-lane TVC bridge")
    model=raw.get("model")
    response_id=raw.get("provider_response_id")
    if not isinstance(model,str) or not model or not isinstance(response_id,str) or not response_id:
        raise ValueError("exact provider model/response identity required")
    if raw.get("provider_api_key_transferred_to_consumer") is not False or raw.get("secret_material_returned") is not False:
        raise ValueError("TVC secret boundary mismatch")
    if raw.get("cost_status")!="REQUEST_BOUND_COST":
        raise ValueError("TVC REQUEST_BOUND_COST required")
    if raw.get("cost_basis")!="EXACT_PROVIDER_USAGE_X_OFFICIAL_MODEL_RATE_CARD":
        raise ValueError("TVC exact official-rate cost basis required")
    rate=raw.get("rate_card")
    if not isinstance(rate,Mapping) or rate.get("provider")!=provider or rate.get("model")!=model:
        raise ValueError("TVC rate-card identity mismatch")
    source_url=rate.get("source")
    observed_at=rate.get("observed_at")
    if not isinstance(source_url,str) or not source_url.startswith("https://") or not isinstance(observed_at,str) or not observed_at:
        raise ValueError("TVC official rate-card provenance required")
    try:
        cost=float(raw.get("calculated_request_cost_usd"))
    except (TypeError,ValueError) as exc:
        raise ValueError("TVC calculated request cost required") from exc
    if cost<0:
        raise ValueError("TVC calculated request cost must be nonnegative")
    candidate_raw=raw.get("candidate_output")
    if not isinstance(candidate_raw,str):
        raise ValueError("TVC candidate_output must be exact JSON text")
    candidate=json.loads(candidate_raw)
    if not isinstance(candidate,dict) or not semantic_ok(candidate):
        raise ValueError("TVC candidate does not satisfy frozen SV-RECON-001 semantics")
    normalized=raw.get("normalized_usage")
    if not isinstance(normalized,Mapping):
        raise ValueError("TVC normalized actual usage required")
    usage=standardized_usage(provider,normalized)

    candidate_dest=candidate_dest or ROOT/"candidate-inputs"/f"{provider}.json"
    cost_dest=cost_dest or ROOT/"cost-evidence"/f"{provider}.json"
    candidate_ref=str(candidate_dest.resolve().relative_to(ROOT.resolve())) if candidate_dest.resolve().is_relative_to(ROOT.resolve()) else str(candidate_dest)
    candidate_usage={
        "input_tokens":usage.get("input_tokens",0),
        "output_tokens":usage.get("output_tokens",0),
    }
    candidate_record={
        "provider":provider,
        "model":model,
        "task_id":"SV-RECON-001",
        "provider_api_key_transferred_to_stegverse":False,
        "provider_response_id":response_id,
        "provider_latency_seconds":None,
        "provider_usage":candidate_usage,
        "candidate_output":candidate,
    }
    cost_record={
        "schema":"stegverse.request-bound-provider-cost-evidence/v1",
        "provider":provider,
        "model":model,
        "task_id":"SV-RECON-001",
        "basis":"EXACT_USAGE_PLUS_BOUND_VERSIONED_RATE_CARD",
        "cost_usd":round(cost,12),
        "provider_usage":usage,
        "rate_card_ref":{
            "authority":"StegVerse-Labs/TVC",
            "source":source_url,
            "observed_at":observed_at,
            "tvc_cost_basis":"EXACT_PROVIDER_USAGE_X_OFFICIAL_MODEL_RATE_CARD",
        },
        "candidate_ref":candidate_ref,
        "provider_api_key_transferred_to_stegverse":False,
        "non_tv_tvc_secret_or_token_used":False,
        "claim_boundary":"REQUEST_BOUND_EFFECTIVE_COST_ONLY",
    }
    candidate_dest.parent.mkdir(parents=True,exist_ok=True)
    cost_dest.parent.mkdir(parents=True,exist_ok=True)
    candidate_dest.write_text(json.dumps(candidate_record,indent=2)+"\n")
    cost_dest.write_text(json.dumps(cost_record,indent=2)+"\n")
    return {
        "state":"INSTALLED",
        "provider":provider,
        "model":model,
        "cost_usd":round(cost,12),
        "candidate":str(candidate_dest),
        "cost_evidence":str(cost_dest),
        "credential_authority":"TV/TVC",
        "provider_operation_performed":False,
        "network_fetch_performed":False,
        "authority_effect":"NONE_EVIDENCE_FORMAT_INTEGRATION_ONLY",
    }


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("source",type=Path)
    ap.add_argument("--candidate-dest",type=Path)
    ap.add_argument("--cost-dest",type=Path)
    ns=ap.parse_args()
    try:
        result=install(ns.source,candidate_dest=ns.candidate_dest,cost_dest=ns.cost_dest)
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        raise SystemExit(str(exc))
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
