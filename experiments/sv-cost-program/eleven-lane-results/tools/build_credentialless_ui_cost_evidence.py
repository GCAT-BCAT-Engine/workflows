#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Mapping

ROOT=Path(__file__).resolve().parents[1]
RATE_CARDS=ROOT/"cost-evidence"/"provider-rate-cards.2026-09-02.json"
ALLOWED={"openai","anthropic","deepseek","zai"}
FORBIDDEN=("api_key","apikey","bearer","password","secret","authorization","private_key","access_token","refresh_token","cookie","session_token","client_secret")


def reject_protected(value: Any,path: str="$")->None:
    if isinstance(value,Mapping):
        for raw_key,child in value.items():
            key=str(raw_key).lower().replace("-","_")
            if any(key==x or key.endswith("_"+x) for x in FORBIDDEN):
                raise ValueError(f"protected field prohibited: {path}.{raw_key}")
            reject_protected(child,f"{path}.{raw_key}")
    elif isinstance(value,list):
        for i,child in enumerate(value):
            reject_protected(child,f"{path}[{i}]")


def number(obj: Mapping[str,Any],key: str)->float:
    value=obj.get(key)
    if not isinstance(value,(int,float)) or isinstance(value,bool) or not math.isfinite(float(value)):
        raise ValueError(f"{key} must be a finite number")
    return float(value)


def int_count(obj: Mapping[str,Any],key: str)->int:
    value=obj.get(key)
    if not isinstance(value,int) or isinstance(value,bool) or value<0:
        raise ValueError(f"{key} must be a nonnegative integer")
    return value


def exact_usage_cost(rate: Mapping[str,Any], before: Mapping[str,Any], after: Mapping[str,Any]) -> tuple[float,dict[str,int]]:
    bi=int_count(before,"input_tokens")
    bo=int_count(before,"output_tokens")
    bc=int_count(before,"cached_input_tokens") if "cached_input_tokens" in before else 0
    ai=int_count(after,"input_tokens")
    ao=int_count(after,"output_tokens")
    ac=int_count(after,"cached_input_tokens") if "cached_input_tokens" in after else 0
    di,do,dc=ai-bi,ao-bo,ac-bc
    if min(di,do,dc)<0:
        raise ValueError("exact token counters may not decrease")
    if dc>di:
        raise ValueError("cached token delta cannot exceed input token delta")
    cached_rate=rate.get("cached_input_usd_per_million")
    if dc and cached_rate is None:
        raise ValueError("selected rate card cannot price cached-input delta")
    uncached=di-dc
    cost=uncached*float(rate["input_usd_per_million"])/1_000_000
    cost+=do*float(rate["output_usd_per_million"])/1_000_000
    if dc:
        cost+=dc*float(cached_rate)/1_000_000
    return round(cost,12),{"input_tokens":di,"output_tokens":do,"cached_input_tokens":dc}


EXPECTED_STATE={"balance":75,"risk_score":3,"standing":"active"}
EXPECTED_SEQUENCE=[
    ("E01","ALLOW"),("E02","ALLOW"),("E03","ALLOW"),
    ("E04","DENY"),("E05","DENY"),("E06","ALLOW"),
]


def validate_candidate(candidate: Any) -> None:
    if not isinstance(candidate,Mapping):
        raise ValueError("candidate_output must be a JSON object")
    if candidate.get("task_id")!="SV-RECON-001":
        raise ValueError("candidate_output task_id mismatch")
    if candidate.get("final_state")!=EXPECTED_STATE:
        raise ValueError("candidate_output final_state mismatch")
    decisions=candidate.get("decisions")
    if not isinstance(decisions,list):
        raise ValueError("candidate_output decisions missing")
    sequence=[
        (item.get("event_id"),str(item.get("status") or "").upper())
        for item in decisions if isinstance(item,Mapping)
    ]
    if sequence!=EXPECTED_SEQUENCE:
        raise ValueError("candidate_output decision sequence mismatch")
    if candidate.get("applied_count")!=4 or candidate.get("denied_count")!=2:
        raise ValueError("candidate_output counts mismatch")
    if candidate.get("claim_boundary")!="DETERMINISTIC_RECONSTRUCTION_ONLY":
        raise ValueError("candidate_output claim boundary mismatch")


def build(obs: dict) -> dict:
    reject_protected(obs)
    if obs.get("schema")!="stegverse.credentialless-ui-cost-observation/v1":
        raise ValueError("unexpected observation schema")
    provider=str(obs.get("provider") or "")
    model=obs.get("model")
    if provider not in ALLOWED:
        raise ValueError("provider not admitted")
    if not isinstance(model,str) or not model:
        raise ValueError("exact model identity required")
    if obs.get("task_id")!="SV-RECON-001":
        raise ValueError("task_id must be SV-RECON-001")
    if obs.get("isolated_single_candidate_window") is not True:
        raise ValueError("observation window must isolate exactly one candidate")
    candidate_output=obs.get("candidate_output")
    validate_candidate(candidate_output)
    candidate_ref=obs.get("candidate_ref")
    if not isinstance(candidate_ref,str) or not candidate_ref:
        raise ValueError("candidate_ref is required")
    if obs.get("provider_api_key_transferred_to_stegverse") is not False or obs.get("non_tv_tvc_secret_or_token_used") is not False:
        raise ValueError("credential boundary mismatch")
    if obs.get("claim_boundary")!="CREDENTIALLESS_PROVIDER_UI_REQUEST_BOUND_OBSERVATION_ONLY":
        raise ValueError("claim boundary mismatch")
    before=obs.get("before")
    after=obs.get("after")
    if not isinstance(before,Mapping) or not isinstance(after,Mapping):
        raise ValueError("before and after observations are required")
    mode=obs.get("observation_mode")
    usage={}
    rate_ref=None

    if mode=="DIRECT_REQUEST_COST_USD":
        b=number(before,"request_cost_usd")
        a=number(after,"request_cost_usd")
        delta=a-b
        if delta<0: raise ValueError("request-cost counter may not decrease")
        cost=round(delta,12)
        basis="PROVIDER_REPORTED_REQUEST_COST_USD"
    elif mode=="USAGE_CREDIT_SPENT_USD":
        b=number(before,"usage_credit_spent_usd")
        a=number(after,"usage_credit_spent_usd")
        delta=a-b
        if delta<0: raise ValueError("usage-credit spend counter may not decrease")
        cost=round(delta,12)
        basis="PROVIDER_REPORTED_REQUEST_COST_USD"
    elif mode=="QUOTA_PERCENT":
        b=number(before,"quota_percent_used")
        a=number(after,"quota_percent_used")
        delta=a-b
        if delta<0: raise ValueError("quota-percent counter may not decrease")
        monthly=obs.get("subscription_monthly_equivalent_usd")
        if not isinstance(monthly,(int,float)) or isinstance(monthly,bool) or not math.isfinite(float(monthly)) or monthly<0:
            raise ValueError("subscription_monthly_equivalent_usd must be a finite nonnegative number")
        if not 0<=b<=100 or not 0<=a<=100:
            raise ValueError("quota percentages must be between 0 and 100")
        cost=round(float(monthly)*(delta/100.0),12)
        basis="PROVIDER_UI_SUBSCRIPTION_QUOTA_ALLOCATED_EFFECTIVE_COST"
    elif mode=="EXACT_TOKENS":
        rate_key=obs.get("rate_key")
        if not isinstance(rate_key,str) or not rate_key:
            raise ValueError("rate_key is required for EXACT_TOKENS")
        registry=json.loads(RATE_CARDS.read_text())
        rate=(registry.get("rates") or {}).get(rate_key)
        if not isinstance(rate,Mapping):
            raise ValueError("unknown or unverified rate key")
        if rate.get("provider")!=provider or rate.get("model")!=model:
            raise ValueError("rate-card provider/model mismatch")
        cost,usage=exact_usage_cost(rate,before,after)
        basis="EXACT_USAGE_PLUS_BOUND_VERSIONED_RATE_CARD"
        rate_ref={"registry":str(RATE_CARDS.relative_to(ROOT)),"rate_key":rate_key,"source":rate.get("source")}
    else:
        raise ValueError("unsupported observation_mode")

    return {
        "schema":"stegverse.request-bound-provider-cost-evidence/v1",
        "provider":provider,
        "model":model,
        "task_id":"SV-RECON-001",
        "basis":basis,
        "cost_usd":cost,
        "provider_usage":usage,
        "rate_card_ref":rate_ref,
        "candidate_ref":candidate_ref,
        "provider_api_key_transferred_to_stegverse":False,
        "non_tv_tvc_secret_or_token_used":False,
        "claim_boundary":"REQUEST_BOUND_EFFECTIVE_COST_ONLY",
        "observation_provenance":{
            "source_schema":"stegverse.credentialless-ui-cost-observation/v1",
            "observation_mode":mode,
            "isolated_single_candidate_window":True,
            "source_observation":obs.get("source_observation"),
            "before":dict(before),
            "after":dict(after),
            "subscription_monthly_equivalent_usd":obs.get("subscription_monthly_equivalent_usd"),
            "rate_key":obs.get("rate_key"),
            "candidate_output":candidate_output,
            "credentialless":True,
        }
    }


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("source",type=Path)
    ap.add_argument("--write",type=Path)
    ns=ap.parse_args()
    try:
        obs=json.loads(ns.source.read_text())
        result=build(obs)
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        raise SystemExit(str(exc))
    body=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if ns.write:
        ns.write.parent.mkdir(parents=True,exist_ok=True)
        ns.write.write_text(body)
    print(body,end="")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
