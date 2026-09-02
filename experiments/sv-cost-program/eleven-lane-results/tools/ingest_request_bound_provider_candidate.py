#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
RATE_CARDS=ROOT/"cost-evidence"/"provider-rate-cards.2026-09-02.json"

FORBIDDEN_EXACT={
    "api_key","apikey","bearer","password","secret","authorization",
    "credential","credentials","private_key","access_token","refresh_token",
    "id_token","session_token","client_secret",
}
SAFE_EVIDENCE_KEYS={
    "provider_api_key_transferred_to_stegverse",
    "non_tv_tvc_secret_or_token_used",
    "input_tokens","output_tokens","cached_input_tokens",
    "provider_usage",
}


def walk_forbidden(value: Any, path: str="$") -> list[str]:
    found=[]
    if isinstance(value,dict):
        for k,v in value.items():
            lk=str(k).lower()
            if lk not in SAFE_EVIDENCE_KEYS and (
                lk in FORBIDDEN_EXACT
                or lk.endswith("_api_key")
                or lk.endswith("_password")
                or lk.endswith("_secret")
                or lk.endswith("_private_key")
                or lk.endswith("_access_token")
                or lk.endswith("_refresh_token")
                or lk.endswith("_bearer")
            ):
                found.append(f"{path}.{k}")
            found.extend(walk_forbidden(v,f"{path}.{k}"))
    elif isinstance(value,list):
        for i,v in enumerate(value):
            found.extend(walk_forbidden(v,f"{path}[{i}]"))
    return found


def semantic_ok(candidate: dict) -> bool:
    expected_state={"balance":75,"risk_score":3,"standing":"active"}
    expected=[("E01","ALLOW"),("E02","ALLOW"),("E03","ALLOW"),("E04","DENY"),("E05","DENY"),("E06","ALLOW")]
    decisions=candidate.get("decisions") or []
    seq=[(x.get("event_id"),str(x.get("status") or "").upper()) for x in decisions if isinstance(x,dict)]
    return (
        candidate.get("task_id")=="SV-RECON-001"
        and candidate.get("final_state")==expected_state
        and seq==expected
        and candidate.get("applied_count")==4
        and candidate.get("denied_count")==2
        and candidate.get("claim_boundary")=="DETERMINISTIC_RECONSTRUCTION_ONLY"
    )


def compute_cost(rate: dict, usage: dict) -> float:
    inp=usage.get("input_tokens")
    out=usage.get("output_tokens")
    cached=usage.get("cached_input_tokens",0)
    if not all(isinstance(x,int) and x>=0 for x in (inp,out,cached)):
        raise ValueError("exact nonnegative input/output/cached token counts required")
    if cached>inp:
        raise ValueError("cached_input_tokens cannot exceed input_tokens")
    uncached=inp-cached
    cached_rate=rate.get("cached_input_usd_per_million")
    if cached and cached_rate is None:
        raise ValueError("rate card does not support cached-input allocation")
    total=uncached*float(rate["input_usd_per_million"])/1_000_000
    total+=out*float(rate["output_usd_per_million"])/1_000_000
    if cached:
        total+=cached*float(cached_rate)/1_000_000
    return round(total,12)


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("source",type=Path,help="credentialless JSON wrapper with provider/model/candidate_output/provider_usage")
    ap.add_argument("--rate-key")
    ap.add_argument("--reported-cost-usd",type=float)
    ap.add_argument("--subscription-monthly-equivalent-usd",type=float)
    ap.add_argument("--quota-percent",type=float)
    ap.add_argument("--candidate-dest",type=Path)
    ap.add_argument("--cost-dest",type=Path)
    ns=ap.parse_args()

    raw=json.loads(ns.source.read_text())
    forbidden=walk_forbidden(raw)
    if forbidden:
        raise SystemExit("forbidden credential-like fields: "+", ".join(forbidden))
    provider=raw.get("provider")
    model=raw.get("model")
    candidate=raw.get("candidate_output")
    usage=raw.get("provider_usage") or {}
    if provider not in {"openai","anthropic","deepseek","zai"}:
        raise SystemExit("unsupported provider")
    if not isinstance(model,str) or not model:
        raise SystemExit("exact model identity required")
    if not isinstance(candidate,dict) or not semantic_ok(candidate):
        raise SystemExit("candidate does not satisfy frozen SV-RECON-001 semantics")
    if raw.get("provider_api_key_transferred_to_stegverse") is not False:
        raise SystemExit("provider credential nonpossession must be explicit")

    basis=None
    cost=None
    rate_ref=None
    if ns.reported_cost_usd is not None:
        if ns.reported_cost_usd < 0:
            raise SystemExit("reported cost must be nonnegative")
        basis="PROVIDER_REPORTED_REQUEST_COST_USD"
        cost=round(ns.reported_cost_usd,12)
    elif ns.subscription_monthly_equivalent_usd is not None or ns.quota_percent is not None:
        if ns.subscription_monthly_equivalent_usd is None or ns.quota_percent is None:
            raise SystemExit("subscription allocation requires both monthly equivalent and quota percent")
        if ns.subscription_monthly_equivalent_usd < 0 or not (0 <= ns.quota_percent <= 100):
            raise SystemExit("invalid subscription allocation inputs")
        basis="PROVIDER_UI_SUBSCRIPTION_QUOTA_ALLOCATED_EFFECTIVE_COST"
        cost=round(ns.subscription_monthly_equivalent_usd*(ns.quota_percent/100.0),12)
    else:
        if not ns.rate_key:
            raise SystemExit("exact usage requires --rate-key; otherwise supply reported cost or quota allocation")
        cards=json.loads(RATE_CARDS.read_text())
        rate=cards.get("rates",{}).get(ns.rate_key)
        if not isinstance(rate,dict):
            raise SystemExit("unknown or unverified rate key")
        if rate.get("provider")!=provider or rate.get("model")!=model:
            raise SystemExit("rate card provider/model does not match exact run identity")
        cost=compute_cost(rate,usage)
        basis="EXACT_USAGE_PLUS_BOUND_VERSIONED_RATE_CARD"
        rate_ref={"registry":str(RATE_CARDS.relative_to(ROOT)),"rate_key":ns.rate_key,"source":rate.get("source")}

    record={
        "provider":provider,
        "model":model,
        "task_id":"SV-RECON-001",
        "provider_api_key_transferred_to_stegverse":False,
        "provider_response_id":raw.get("provider_response_id"),
        "provider_latency_seconds":raw.get("provider_latency_seconds"),
        "provider_usage":usage,
        "candidate_output":candidate,
    }
    cost_record={
        "schema":"stegverse.request-bound-provider-cost-evidence/v1",
        "provider":provider,
        "model":model,
        "task_id":"SV-RECON-001",
        "basis":basis,
        "cost_usd":cost,
        "provider_usage":usage,
        "rate_card_ref":rate_ref,
        "candidate_ref":None,
        "provider_api_key_transferred_to_stegverse":False,
        "non_tv_tvc_secret_or_token_used":False,
        "claim_boundary":"REQUEST_BOUND_EFFECTIVE_COST_ONLY",
    }

    candidate_dest=ns.candidate_dest or (ROOT/"candidate-inputs"/f"{provider}.json")
    cost_dest=ns.cost_dest or (ROOT/"cost-evidence"/f"{provider}.json")
    try:
        cost_record["candidate_ref"]=str(candidate_dest.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        cost_record["candidate_ref"]=str(candidate_dest)
    candidate_dest.parent.mkdir(parents=True,exist_ok=True)
    cost_dest.parent.mkdir(parents=True,exist_ok=True)
    candidate_dest.write_text(json.dumps(record,indent=2)+"\n")
    cost_dest.write_text(json.dumps(cost_record,indent=2)+"\n")
    print(json.dumps({"status":"INSTALLED","provider":provider,"model":model,"cost_usd":cost,"basis":basis,"candidate":str(candidate_dest),"cost_evidence":str(cost_dest)},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
