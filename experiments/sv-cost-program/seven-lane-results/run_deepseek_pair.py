#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import time
import urllib.error
import urllib.request
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
TASK = json.loads((ROOT / "task.json").read_text())
PRICE = json.loads((ROOT / "deepseek-price-card.json").read_text())
OUT = ROOT / "results"
RAW = OUT / "raw-deepseek-pair"
OUT.mkdir(exist_ok=True)
RAW.mkdir(exist_ok=True)


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(value).encode()).hexdigest()


def expected() -> dict[str, Any]:
    state = dict(TASK["initial_state"])
    decisions: list[dict[str, str]] = []
    for event in TASK["events"]:
        op, amount, event_id = event["operation"], event["amount"], event["event_id"]
        if op == "credit":
            state["balance"] += amount
            status = "ALLOW"
        elif op == "debit":
            status = "ALLOW" if (
                state["standing"] == TASK["policy"]["standing_required_for_debit"]
                and state["balance"] - amount >= TASK["policy"]["minimum_balance"]
            ) else "DENY"
            if status == "ALLOW":
                state["balance"] -= amount
        elif op == "risk_add":
            status = "ALLOW" if state["risk_score"] + amount <= TASK["policy"]["maximum_risk_score"] else "DENY"
            if status == "ALLOW":
                state["risk_score"] += amount
        else:
            raise ValueError(op)
        decisions.append({"event_id": event_id, "status": status})
    return {
        "task_id": TASK["task_id"],
        "final_state": state,
        "decisions": decisions,
        "applied_count": sum(x["status"] == "ALLOW" for x in decisions),
        "denied_count": sum(x["status"] == "DENY" for x in decisions),
    }


EXPECTED = expected()


def prompt(governed: bool) -> str:
    prefix = ""
    if governed:
        prefix = (
            "Apply StegVerse governance: preserve task identity; evaluate authority before mutation; "
            "deny before mutation; preserve event ordering; return no prose. "
        )
    contract = {k: TASK[k] for k in ["task_id", "initial_state", "policy", "events", "decision_rules"]}
    schema = {
        "task_id": "string",
        "final_state": {"balance": "number", "risk_score": "number", "standing": "string"},
        "decisions": [{"event_id": "string", "status": "ALLOW|DENY"}],
        "applied_count": "integer",
        "denied_count": "integer",
    }
    return prefix + "Compute the deterministic result. Return only JSON matching " + canon(schema) + " Contract: " + canon(contract)


def extract(text: str) -> dict[str, Any]:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("NO_JSON_OBJECT")
    obj = json.loads(text[start:end + 1])
    decisions = obj.get("decisions") or obj.get("event_decisions") or []
    normalized_decisions = [
        {
            "event_id": x.get("event_id") or x.get("id"),
            "status": str(x.get("status") or x.get("decision") or "").upper(),
        }
        for x in decisions if isinstance(x, dict)
    ]
    final_state = obj.get("final_state") or {
        "balance": obj.get("final_balance"),
        "risk_score": obj.get("final_risk_score"),
        "standing": obj.get("final_standing"),
    }
    return {
        "task_id": obj.get("task_id") or TASK["task_id"],
        "final_state": final_state,
        "decisions": normalized_decisions,
        "applied_count": obj.get("applied_count", sum(x["status"] == "ALLOW" for x in normalized_decisions)),
        "denied_count": obj.get("denied_count", sum(x["status"] == "DENY" for x in normalized_decisions)),
    }


def validate(value: dict[str, Any]) -> tuple[bool, list[str]]:
    failures = [f"MISMATCH_{k.upper()}" for k in EXPECTED if value.get(k) != EXPECTED[k]]
    return not failures, failures


def cost(usage: dict[str, Any]) -> tuple[float, dict[str, int]]:
    prompt_tokens = int(usage.get("prompt_tokens", 0))
    output_tokens = int(usage.get("completion_tokens", 0))
    details = usage.get("prompt_tokens_details") or {}
    cached = int(details.get("cached_tokens", 0) or 0)
    miss = max(0, prompt_tokens - cached)
    amount = (
        cached * PRICE["input_cache_hit_usd_per_million"]
        + miss * PRICE["input_cache_miss_usd_per_million"]
        + output_tokens * PRICE["output_usd_per_million"]
    ) / 1_000_000
    return round(amount, 12), {
        "input_tokens": prompt_tokens,
        "cached_input_tokens": cached,
        "cache_miss_input_tokens": miss,
        "output_tokens": output_tokens,
    }


def call(governed: bool) -> dict[str, Any]:
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        return {"state": "BLOCKED", "blocker": "DEEPSEEK_API_KEY_MISSING"}
    model = os.getenv("DEEPSEEK_SEVEN_LANE_MODEL", TASK["provider_execution"]["deepseek_model"])
    base = os.getenv("DEEPSEEK_API_BASE", TASK["provider_execution"]["deepseek_base_url"])
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt(governed)}],
        "max_tokens": 1200,
        "temperature": 0,
    }
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            raw = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode(errors="replace")[:2000]
        return {"state": "RETRY", "http_status": exc.code, "error": payload}
    except Exception as exc:
        return {"state": "RETRY", "error": type(exc).__name__ + ":" + str(exc)}
    latency = time.perf_counter() - started
    text = (raw.get("choices") or [{}])[0].get("message", {}).get("content", "")
    try:
        normalized = extract(text)
        admissible, failures = validate(normalized)
    except Exception as exc:
        normalized, admissible, failures = {}, False, [type(exc).__name__ + ":" + str(exc)]
    amount, tokens = cost(raw.get("usage", {}))
    lane = "deepseek-governed" if governed else "deepseek-raw"
    RAW.joinpath(lane + ".json").write_text(json.dumps(raw, indent=2) + "\n")
    return {
        "state": "COMPLETE" if admissible else "FAILED",
        "lane_id": lane,
        "model": model,
        "governed": governed,
        "latency_seconds": latency,
        "provider_cost_usd": amount,
        "token_usage": tokens,
        "admissible": admissible,
        "failures": failures,
        "required_output_hash": sha(EXPECTED),
        "actual_output_hash": sha(normalized),
        "provider_response_hash": sha(raw),
    }


raw = call(False)
governed = call(True)
if raw.get("state") == "BLOCKED" or governed.get("state") == "BLOCKED":
    overall = "BLOCKED"
elif raw.get("state") == "RETRY" or governed.get("state") == "RETRY":
    overall = "RETRY"
elif raw.get("state") == governed.get("state") == "COMPLETE":
    overall = "COMPLETE"
else:
    overall = "FAILED"

result = {
    "schema_version": "1.0.0",
    "task_id": "SV-COST-DEEPSEEK-PAIR-001",
    "originating_goal": "Add DeepSeek and DeepSeek/StegVerse as lanes 6 and 7 and evaluate Governed AI economics under abundant intelligence.",
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "state": overall,
    "price_card_hash": sha(PRICE),
    "price_card": PRICE,
    "raw": raw,
    "governed": governed,
    "release_condition": "COMPLETE requires both DeepSeek raw and DeepSeek/StegVerse to reach the required normalized output under the same task contract with retained provider receipts.",
    "next_task": "Feed the pair into governed-ai-premium workload/product reducers if COMPLETE; otherwise preserve BLOCKED/RETRY/FAILED evidence without widening claims.",
}
(OUT / "deepseek_pair_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(overall)
raise SystemExit(0 if overall in {"COMPLETE", "BLOCKED", "RETRY"} else 2)
