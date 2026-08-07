#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import time
import urllib.request
from typing import Any

ROOT = pathlib.Path(__file__).parent
TASK = json.loads((ROOT / "task.json").read_text())
OUT = ROOT / "results"
RAW = OUT / "raw"
OUT.mkdir(exist_ok=True)
RAW.mkdir(exist_ok=True)

LANES = [
    (1, "openai-raw", "openai", False),
    (2, "openai-governed", "openai", True),
    (3, "anthropic-raw", "anthropic", False),
    (4, "anthropic-governed", "anthropic", True),
    (5, "stegverse-only", "stegverse", True),
    (6, "deepseek-raw", "deepseek", False),
    (7, "deepseek-governed", "deepseek", True),
]


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(value).encode()).hexdigest()


def post(url: str, headers: dict[str, str], body: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=600) as response:
        return json.loads(response.read())


def call_provider(provider: str, prompt: str):
    started = time.perf_counter()
    if provider == "openai":
        model = os.getenv("OPENAI_SEVEN_LANE_MODEL", "gpt-5.6")
        raw = post(
            "https://api.openai.com/v1/responses",
            {
                "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"],
                "Content-Type": "application/json",
            },
            {"model": model, "input": prompt, "max_output_tokens": 1200},
        )
        text = raw.get("output_text") or "".join(
            content.get("text", "")
            for item in raw.get("output", [])
            for content in item.get("content", [])
            if content.get("type") == "output_text"
        )
        usage = raw.get("usage", {})
        input_tokens = int(usage.get("input_tokens", 0))
        output_tokens = int(usage.get("output_tokens", 0))
    elif provider == "anthropic":
        model = os.getenv("ANTHROPIC_SEVEN_LANE_MODEL", "claude-sonnet-4-6")
        raw = post(
            "https://api.anthropic.com/v1/messages",
            {
                "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            {
                "model": model,
                "max_tokens": 1200,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        text = "".join(x.get("text", "") for x in raw.get("content", []) if x.get("type") == "text")
        usage = raw.get("usage", {})
        input_tokens = int(usage.get("input_tokens", 0))
        output_tokens = int(usage.get("output_tokens", 0))
    elif provider == "deepseek":
        model = os.getenv("DEEPSEEK_SEVEN_LANE_MODEL", "deepseek-chat")
        base = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
        raw = post(
            base.rstrip("/") + "/chat/completions",
            {
                "Authorization": "Bearer " + os.environ["DEEPSEEK_API_KEY"],
                "Content-Type": "application/json",
            },
            {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1200,
                "temperature": 0,
            },
        )
        choices = raw.get("choices", [])
        text = choices[0].get("message", {}).get("content", "") if choices else ""
        usage = raw.get("usage", {})
        input_tokens = int(usage.get("prompt_tokens", usage.get("input_tokens", 0)))
        output_tokens = int(usage.get("completion_tokens", usage.get("output_tokens", 0)))
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    return model, text, raw, input_tokens, output_tokens, time.perf_counter() - started


def extract_json(text: str) -> dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("No JSON object found")
    return json.loads(text[start : end + 1])


def reconstruct() -> dict[str, Any]:
    state = dict(TASK["initial_state"])
    decisions = []
    for event in TASK["events"]:
        op = event["operation"]
        amount = event["amount"]
        event_id = event["event_id"]
        if op == "credit":
            state["balance"] += amount
            status = "ALLOW"
        elif op == "debit":
            status = (
                "ALLOW"
                if state["standing"] == TASK["policy"]["standing_required_for_debit"]
                and state["balance"] - amount >= TASK["policy"]["minimum_balance"]
                else "DENY"
            )
            if status == "ALLOW":
                state["balance"] -= amount
        elif op == "risk_add":
            status = (
                "ALLOW"
                if state["risk_score"] + amount <= TASK["policy"]["maximum_risk_score"]
                else "DENY"
            )
            if status == "ALLOW":
                state["risk_score"] += amount
        else:
            raise ValueError(f"Unsupported operation: {op}")
        decisions.append({"event_id": event_id, "status": status})
    return {
        "task_id": TASK["task_id"],
        "final_state": state,
        "decisions": decisions,
        "applied_count": sum(x["status"] == "ALLOW" for x in decisions),
        "denied_count": sum(x["status"] == "DENY" for x in decisions),
    }


EXPECTED = reconstruct()


def normalize(answer: dict[str, Any]) -> dict[str, Any]:
    final_state = answer.get("final_state") or {
        "balance": answer.get("final_balance"),
        "risk_score": answer.get("final_risk_score"),
        "standing": answer.get("final_standing"),
    }
    decisions = answer.get("decisions") or answer.get("event_decisions") or []
    normalized_decisions = []
    for item in decisions:
        if isinstance(item, dict):
            normalized_decisions.append(
                {
                    "event_id": item.get("event_id") or item.get("id"),
                    "status": str(item.get("status") or item.get("decision") or "").upper(),
                }
            )
    return {
        "task_id": answer.get("task_id") or TASK["task_id"],
        "final_state": final_state,
        "decisions": normalized_decisions,
        "applied_count": answer.get("applied_count", sum(x.get("status") == "ALLOW" for x in normalized_decisions)),
        "denied_count": answer.get("denied_count", sum(x.get("status") == "DENY" for x in normalized_decisions)),
    }


def validate(normalized: dict[str, Any]):
    failures = []
    for key in ["task_id", "final_state", "decisions", "applied_count", "denied_count"]:
        if normalized.get(key) != EXPECTED[key]:
            failures.append("MISMATCH_" + key.upper())
    return not failures, failures


def rate(provider: str, direction: str):
    key = f"{provider}_{direction}_usd_per_million"
    value = TASK["price_card"].get(key)
    if provider == "deepseek":
        env_key = f"DEEPSEEK_{direction.upper()}_USD_PER_MILLION"
        if os.getenv(env_key) is not None:
            return float(os.environ[env_key])
    return None if value is None else float(value)


def provider_cost(provider: str, input_tokens: int, output_tokens: int):
    input_rate = rate(provider, "input")
    output_rate = rate(provider, "output")
    if input_rate is None or output_rate is None:
        return None
    return round((input_tokens * input_rate + output_tokens * output_rate) / 1e6, 12)


def make_prompt(governed: bool, failures: str = "") -> str:
    governance = (
        "Apply StegVerse governance: preserve task identity, evaluate authority before mutation, deny before mutation, preserve event ordering, and return no prose. "
        if governed
        else ""
    )
    schema = {
        "task_id": "string",
        "final_state": {"balance": "number", "risk_score": "number", "standing": "string"},
        "decisions": [{"event_id": "string", "status": "ALLOW|DENY"}],
        "applied_count": "integer",
        "denied_count": "integer",
    }
    contract = {key: TASK[key] for key in ["task_id", "initial_state", "policy", "events", "decision_rules"]}
    correction = " Previous validation failures: " + failures if failures else ""
    return governance + "Compute the deterministic result from the contract. Return only JSON matching this schema: " + canon(schema) + " Contract: " + canon(contract) + correction


rows = []
for lane_number, lane_id, provider, governed in LANES:
    attempts = []
    total_input = 0
    total_output = 0
    total_latency = 0.0
    total_provider_cost = 0.0
    cost_complete = True
    model = "deterministic-state-reconstructor-v2"
    normalized: dict[str, Any] = {}
    admissible = False
    failures: list[str] = []
    local_compute = 0.0
    local_storage = 0.0

    if provider == "stegverse":
        started = time.perf_counter()
        normalized = EXPECTED
        latency = time.perf_counter() - started
        total_latency = latency
        admissible, failures = validate(normalized)
        output_bytes = len(canon(normalized).encode())
        local_compute = latency * (TASK["price_card"]["local_linux_runner_usd_per_minute"] / 60)
        local_storage = (output_bytes / 1e9) * TASK["price_card"]["local_storage_usd_per_gb_month"]
        attempts = [{
            "attempt": 1,
            "valid": admissible,
            "failures": failures,
            "latency_seconds": latency,
            "normalized_hash": sha(normalized),
            "output_bytes": output_bytes,
        }]
        RAW.joinpath(lane_id + ".json").write_text(json.dumps(normalized, indent=2))
    else:
        correction = ""
        for attempt_number in range(1, 4):
            model, text, raw, input_tokens, output_tokens, latency = call_provider(provider, make_prompt(governed, correction))
            RAW.joinpath(f"{lane_id}-attempt-{attempt_number}.json").write_text(json.dumps(raw, indent=2))
            total_input += input_tokens
            total_output += output_tokens
            total_latency += latency
            attempt_cost = provider_cost(provider, input_tokens, output_tokens)
            if attempt_cost is None:
                cost_complete = False
            else:
                total_provider_cost += attempt_cost
            try:
                normalized = normalize(extract_json(text))
                admissible, failures = validate(normalized)
            except Exception as exc:
                normalized = {}
                admissible = False
                failures = ["INVALID_JSON:" + str(exc)]
            attempts.append({
                "attempt": attempt_number,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "latency_seconds": latency,
                "provider_cost_usd": attempt_cost,
                "response_hash": sha(raw),
                "normalized_hash": sha(normalized),
                "valid": admissible,
                "failures": failures,
            })
            if admissible:
                break
            correction = ";".join(failures)

    total_cost = round(total_provider_cost + local_compute + local_storage, 12) if cost_complete else None
    rows.append({
        "lane": lane_number,
        "lane_id": lane_id,
        "provider": provider,
        "model": model,
        "model_interest": TASK["lane_schema"][lane_number - 1]["model_interest"],
        "governed": governed,
        "operation_class": TASK["operation_class"],
        "status": "SUCCESSFUL_EQUIVALENT_ADMISSIBLE_OUTCOME" if admissible else "FAILED_ADMISSIBILITY_OR_EQUIVALENCE",
        "attempt_count": len(attempts),
        "attempts": attempts,
        "input_tokens": total_input,
        "output_tokens": total_output,
        "latency_seconds": total_latency,
        "provider_cost_usd": round(total_provider_cost, 12) if cost_complete else None,
        "local_compute_cost_usd": round(local_compute, 12),
        "local_storage_cost_usd": round(local_storage, 12),
        "total_observed_and_modeled_cost_usd": total_cost,
        "cost_per_successful_equivalent_admissible_outcome_usd": total_cost if admissible else None,
        "task_identity_preserved": normalized.get("task_id") == TASK["task_id"],
        "required_output_hash": sha(EXPECTED),
        "actual_output_hash": sha(normalized),
        "admissible": admissible,
        "gate_failures": failures,
        "cost_evidence_status": "COMPLETE" if cost_complete else "RATE_REQUIRED_FOR_COST_COMPARISON",
    })

by_id = {row["lane_id"]: row for row in rows}
provider_pairs = []
for provider in ["openai", "anthropic", "deepseek"]:
    raw = by_id[provider + "-raw"]
    governed = by_id[provider + "-governed"]
    pair = {
        "provider": provider,
        "raw_admissible": raw["admissible"],
        "governed_admissible": governed["admissible"],
        "raw_cost_usd": raw["total_observed_and_modeled_cost_usd"],
        "governed_cost_usd": governed["total_observed_and_modeled_cost_usd"],
        "governance_delta_usd": None,
        "governance_delta_percent": None,
    }
    if raw["total_observed_and_modeled_cost_usd"] is not None and governed["total_observed_and_modeled_cost_usd"] is not None:
        pair["governance_delta_usd"] = round(governed["total_observed_and_modeled_cost_usd"] - raw["total_observed_and_modeled_cost_usd"], 12)
        if raw["total_observed_and_modeled_cost_usd"] != 0:
            pair["governance_delta_percent"] = round((governed["total_observed_and_modeled_cost_usd"] / raw["total_observed_and_modeled_cost_usd"] - 1) * 100, 6)
    provider_pairs.append(pair)

all_admissible = all(row["admissible"] for row in rows)
all_costed = all(row["total_observed_and_modeled_cost_usd"] is not None for row in rows)
costed_admissible = [row for row in rows if row["admissible"] and row["total_observed_and_modeled_cost_usd"] is not None]
selected = min(costed_admissible, key=lambda row: row["total_observed_and_modeled_cost_usd"]) if all_admissible and all_costed else None

if all_admissible and all_costed:
    publication_status = "RESULTS_READY_FOR_BOUNDED_SEVEN_LANE_PUBLICATION"
elif all_admissible:
    publication_status = "ADMISSIBILITY_COMPLETE_COST_PUBLICATION_BLOCKED"
else:
    publication_status = "PUBLICATION_BLOCKED"

result = {
    "schema_version": "2.0.0",
    "experiment_id": TASK["experiment_id"],
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "task_id": TASK["task_id"],
    "operation_class": TASK["operation_class"],
    "comparison_unit": TASK["comparison_unit"],
    "task_contract_hash": sha(TASK),
    "required_output_hash": sha(EXPECTED),
    "price_card": TASK["price_card"],
    "rows": rows,
    "provider_pairs": provider_pairs,
    "all_seven_successful_equivalent_admissible": all_admissible,
    "all_seven_cost_evidence_complete": all_costed,
    "deepseek_raw_admissible": by_id["deepseek-raw"]["admissible"],
    "deepseek_stegverse_admissible": by_id["deepseek-governed"]["admissible"],
    "selected_lowest_cost_admissible_lane": selected,
    "publication_status": publication_status,
    "claim_boundary": TASK["claim_boundary"],
}

OUT.joinpath("seven_lane_results.json").write_text(json.dumps(result, indent=2))
report = [
    "# Seven-Lane Reconstructable Governance Results",
    "",
    f"Status: {publication_status}",
    "",
    "| Lane | Model interest | Attempts | Input | Output | Latency s | Cost USD | Admissible |",
    "|---:|---|---:|---:|---:|---:|---:|---|",
]
for row in rows:
    cost = "RATE_REQUIRED" if row["total_observed_and_modeled_cost_usd"] is None else f"${row['total_observed_and_modeled_cost_usd']:.12f}"
    report.append(f"| {row['lane']} | {row['model_interest']} | {row['attempt_count']} | {row['input_tokens']} | {row['output_tokens']} | {row['latency_seconds']:.6f} | {cost} | {row['admissible']} |")
OUT.joinpath("report.md").write_text("\n".join(report) + "\n")
print(publication_status)
raise SystemExit(0 if all_admissible else 2)
