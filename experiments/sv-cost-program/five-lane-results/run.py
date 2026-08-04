#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import time
import urllib.request
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
TASK_PATH = ROOT / "task.json"
OUT = ROOT / "results"
RAW = OUT / "raw"
OUT.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)

LANES = [
    ("openai-raw", "openai", False),
    ("openai-governed", "openai", True),
    ("anthropic-raw", "anthropic", False),
    ("anthropic-governed", "anthropic", True),
    ("stegverse-only", "stegverse", True),
]


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(value: Any) -> str:
    data = value if isinstance(value, bytes) else canonical(value).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def post(url: str, headers: dict[str, str], body: dict[str, Any]) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as response:
        return json.loads(response.read())


def openai_call(prompt: str) -> tuple[str, str, dict[str, Any], int, int, float]:
    model = os.getenv("OPENAI_FIVE_LANE_MODEL", "gpt-5.6")
    started = time.perf_counter()
    raw = post(
        "https://api.openai.com/v1/responses",
        {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"], "Content-Type": "application/json"},
        {"model": model, "input": prompt, "max_output_tokens": 1600},
    )
    text = raw.get("output_text") or "".join(
        part.get("text", "")
        for item in raw.get("output", [])
        for part in item.get("content", [])
        if part.get("type") == "output_text"
    )
    usage = raw.get("usage", {})
    return model, text, raw, int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0)), time.perf_counter() - started


def anthropic_call(prompt: str) -> tuple[str, str, dict[str, Any], int, int, float]:
    model = os.getenv("ANTHROPIC_FIVE_LANE_MODEL", "claude-sonnet-4-6")
    started = time.perf_counter()
    raw = post(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        {"model": model, "max_tokens": 1600, "messages": [{"role": "user", "content": prompt}]},
    )
    text = "".join(item.get("text", "") for item in raw.get("content", []) if item.get("type") == "text")
    usage = raw.get("usage", {})
    return model, text, raw, int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0)), time.perf_counter() - started


def extract_json(text: str) -> dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("JSON object not found")
    value = json.loads(text[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("response is not an object")
    return value


def provider_cost(provider: str, input_tokens: int, output_tokens: int, price_card: dict[str, Any]) -> float:
    if provider == "openai":
        i = price_card["openai_input_usd_per_million"]
        o = price_card["openai_output_usd_per_million"]
    else:
        i = price_card["anthropic_input_usd_per_million"]
        o = price_card["anthropic_output_usd_per_million"]
    return round((input_tokens * i + output_tokens * o) / 1_000_000, 9)


def build_prompt(task: dict[str, Any], governed: bool, correction: str | None = None) -> str:
    governance = ""
    if governed:
        governance = (
            "StegVerse governed execution controls: preserve task identity; apply every event in order; "
            "deny boundary violations before mutation; preserve the required claim boundary; emit no unsupported fields.\n\n"
        )
    correction_text = f"\nPrevious attempt failed validation: {correction}. Correct it without changing the task.\n" if correction else ""
    return (
        governance
        + "Reconstruct the final state and decisions from this exact task contract. Return only one JSON object exactly matching required_output keys and value types.\n"
        + canonical({k: task[k] for k in ["task_id", "initial_state", "policy", "events", "decision_rules"]})
        + correction_text
    )


def local_reconstruct(task: dict[str, Any]) -> dict[str, Any]:
    state = dict(task["initial_state"])
    decisions: list[dict[str, str]] = []
    for event in task["events"]:
        op = event["operation"]
        amount = event["amount"]
        if op == "credit":
            state["balance"] += amount
            decisions.append({"event_id": event["event_id"], "status": "ALLOW", "reason": "CREDIT_APPLIED"})
        elif op == "debit":
            if state["standing"] != task["policy"]["standing_required_for_debit"]:
                decisions.append({"event_id": event["event_id"], "status": "DENY", "reason": "STANDING_REQUIRED"})
            elif state["balance"] - amount < task["policy"]["minimum_balance"]:
                decisions.append({"event_id": event["event_id"], "status": "DENY", "reason": "MINIMUM_BALANCE_VIOLATION"})
            else:
                state["balance"] -= amount
                decisions.append({"event_id": event["event_id"], "status": "ALLOW", "reason": "DEBIT_WITHIN_BOUNDARY"})
        elif op == "risk_add":
            if state["risk_score"] + amount > task["policy"]["maximum_risk_score"]:
                decisions.append({"event_id": event["event_id"], "status": "DENY", "reason": "MAXIMUM_RISK_VIOLATION"})
            else:
                state["risk_score"] += amount
                decisions.append({"event_id": event["event_id"], "status": "ALLOW", "reason": "RISK_WITHIN_BOUNDARY"})
        else:
            raise ValueError(f"unsupported operation: {op}")
    return {
        "task_id": task["task_id"],
        "final_state": state,
        "decisions": decisions,
        "applied_count": sum(d["status"] == "ALLOW" for d in decisions),
        "denied_count": sum(d["status"] == "DENY" for d in decisions),
        "claim_boundary": "DETERMINISTIC_RECONSTRUCTION_ONLY",
    }


def compare(actual: dict[str, Any], expected: dict[str, Any]) -> tuple[bool, list[str]]:
    failures: list[str] = []
    for key in expected:
        if key not in actual:
            failures.append(f"MISSING_{key.upper()}")
        elif actual[key] != expected[key]:
            failures.append(f"MISMATCH_{key.upper()}")
    extra = sorted(set(actual) - set(expected))
    if extra:
        failures.append("UNSUPPORTED_FIELDS:" + ",".join(extra))
    return not failures, failures


def main() -> int:
    task = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    expected = task["required_output"]
    price_card = task["price_card"]
    rows: list[dict[str, Any]] = []

    for lane_id, provider, governed in LANES:
        attempts: list[dict[str, Any]] = []
        total_input = total_output = 0
        total_latency = 0.0
        total_provider_cost = 0.0
        model = "deterministic-state-reconstructor-v1"
        actual: dict[str, Any] = {}
        valid = False
        failures: list[str] = []
        local_compute_cost = 0.0
        local_storage_cost = 0.0

        if provider == "stegverse":
            started = time.perf_counter()
            actual = local_reconstruct(task)
            latency = time.perf_counter() - started
            valid, failures = compare(actual, expected)
            output_bytes = len(canonical(actual).encode("utf-8"))
            local_compute_cost = latency * (price_card["local_linux_runner_usd_per_minute"] / 60)
            local_storage_cost = (output_bytes / 1_000_000_000) * price_card["local_storage_usd_per_gb_month"]
            total_latency = latency
            attempts.append({
                "attempt": 1,
                "normalized_hash": sha256(actual),
                "valid": valid,
                "failures": failures,
                "latency_seconds": latency,
                "output_bytes": output_bytes,
            })
            (RAW / f"{lane_id}.json").write_text(json.dumps(actual, indent=2), encoding="utf-8")
        else:
            correction = None
            for attempt_no in range(1, 3):
                prompt = build_prompt(task, governed, correction)
                model, text, raw, input_tokens, output_tokens, latency = (
                    openai_call(prompt) if provider == "openai" else anthropic_call(prompt)
                )
                total_input += input_tokens
                total_output += output_tokens
                total_latency += latency
                call_cost = provider_cost(provider, input_tokens, output_tokens, price_card)
                total_provider_cost += call_cost
                (RAW / f"{lane_id}-attempt-{attempt_no}.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
                try:
                    actual = extract_json(text)
                    valid, failures = compare(actual, expected)
                except Exception as exc:
                    actual = {}
                    valid = False
                    failures = ["INVALID_JSON:" + str(exc)]
                attempts.append({
                    "attempt": attempt_no,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "latency_seconds": latency,
                    "provider_cost_usd": call_cost,
                    "response_hash": sha256(raw),
                    "normalized_hash": sha256(actual),
                    "valid": valid,
                    "failures": failures,
                })
                if valid:
                    break
                correction = ";".join(failures)

        local_total = local_compute_cost + local_storage_cost
        total_cost = total_provider_cost + local_total
        rows.append({
            "lane_id": lane_id,
            "provider": provider,
            "model": model,
            "governed": governed,
            "operation_class": task["operation_class"],
            "status": "SUCCESSFUL_EQUIVALENT_ADMISSIBLE_OUTCOME" if valid else "FAILED_ADMISSIBILITY_OR_EQUIVALENCE",
            "attempt_count": len(attempts),
            "attempts": attempts,
            "input_tokens": total_input,
            "output_tokens": total_output,
            "latency_seconds": total_latency,
            "provider_cost_usd": round(total_provider_cost, 9),
            "local_compute_cost_usd": round(local_compute_cost, 12),
            "local_storage_cost_usd": round(local_storage_cost, 12),
            "total_observed_and_modeled_cost_usd": round(total_cost, 12),
            "cost_per_successful_equivalent_admissible_outcome_usd": round(total_cost, 12) if valid else None,
            "task_identity_preserved": actual.get("task_id") == task["task_id"],
            "required_output_hash": sha256(expected),
            "actual_output_hash": sha256(actual),
            "admissible": valid,
            "gate_failures": failures,
            "cost_evidence_status": price_card["status"] if provider != "stegverse" else "MEASURED_RUNTIME_WITH_VERSIONED_DECLARED_INFRASTRUCTURE_RATES",
        })

    admissible = [row for row in rows if row["admissible"]]
    selected = min(admissible, key=lambda row: row["cost_per_successful_equivalent_admissible_outcome_usd"]) if admissible else None
    by_id = {row["lane_id"]: row for row in rows}
    provider_pairs = []
    for provider in ["openai", "anthropic"]:
        raw = by_id[f"{provider}-raw"]
        governed = by_id[f"{provider}-governed"]
        provider_pairs.append({
            "provider": provider,
            "raw_cost_usd": raw["total_observed_and_modeled_cost_usd"],
            "governed_cost_usd": governed["total_observed_and_modeled_cost_usd"],
            "governance_delta_usd": round(governed["total_observed_and_modeled_cost_usd"] - raw["total_observed_and_modeled_cost_usd"], 12),
            "governance_delta_percent": round(((governed["total_observed_and_modeled_cost_usd"] / raw["total_observed_and_modeled_cost_usd"]) - 1) * 100, 6) if raw["total_observed_and_modeled_cost_usd"] else None,
            "raw_admissible": raw["admissible"],
            "governed_admissible": governed["admissible"],
        })

    local = by_id["stegverse-only"]
    replacement_comparisons = []
    for lane_id in ["openai-raw", "openai-governed", "anthropic-raw", "anthropic-governed"]:
        lane = by_id[lane_id]
        ratio = lane["total_observed_and_modeled_cost_usd"] / local["total_observed_and_modeled_cost_usd"] if local["total_observed_and_modeled_cost_usd"] else None
        reduction = (1 - local["total_observed_and_modeled_cost_usd"] / lane["total_observed_and_modeled_cost_usd"]) * 100 if lane["total_observed_and_modeled_cost_usd"] else None
        replacement_comparisons.append({
            "provider_lane": lane_id,
            "provider_lane_cost_usd": lane["total_observed_and_modeled_cost_usd"],
            "stegverse_only_cost_usd": local["total_observed_and_modeled_cost_usd"],
            "provider_to_stegverse_cost_ratio": round(ratio, 6) if ratio is not None else None,
            "matched_operation_modeled_reduction_percent": round(reduction, 6) if reduction is not None else None,
            "valid_only_if_both_admissible": lane["admissible"] and local["admissible"],
        })

    all_five_complete = len(rows) == 5 and all(row["admissible"] for row in rows)
    result = {
        "schema_version": "1.0.0",
        "experiment_id": task["experiment_id"],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "task_id": task["task_id"],
        "operation_class": task["operation_class"],
        "comparison_unit": task["comparison_unit"],
        "task_contract_hash": sha256(task),
        "required_output_hash": sha256(expected),
        "price_card": price_card,
        "rows": rows,
        "provider_pairs": provider_pairs,
        "replacement_comparisons": replacement_comparisons,
        "all_five_successful_equivalent_admissible": all_five_complete,
        "selected_lowest_cost_admissible_lane": selected,
        "total_test_cost_usd": round(sum(row["total_observed_and_modeled_cost_usd"] for row in rows), 12),
        "claim_boundary": task["claim_boundary"],
        "publication_status": "RESULTS_READY_FOR_BOUNDED_PUBLICATION" if all_five_complete else "RESEARCH_IN_PROGRESS_FAIL_CLOSED",
    }
    (OUT / "five_lane_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    report = [
        "# Five-Lane Reconstructable Governance Cost Results",
        "",
        f"Status: `{result['publication_status']}`",
        "",
        f"Comparison unit: `{task['comparison_unit']}`",
        "",
        "| Lane | Admissible | Attempts | Input | Output | Latency s | Provider cost | Local cost | Total cost |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        local_cost = row["local_compute_cost_usd"] + row["local_storage_cost_usd"]
        report.append(
            f"| {row['lane_id']} | {str(row['admissible']).lower()} | {row['attempt_count']} | {row['input_tokens']} | {row['output_tokens']} | {row['latency_seconds']:.6f} | ${row['provider_cost_usd']:.9f} | ${local_cost:.12f} | ${row['total_observed_and_modeled_cost_usd']:.12f} |"
        )
    report += ["", "## Provider governance deltas", "", "| Provider | Raw | Governed | Delta | Delta % |", "|---|---:|---:|---:|---:|"]
    for pair in provider_pairs:
        report.append(f"| {pair['provider']} | ${pair['raw_cost_usd']:.9f} | ${pair['governed_cost_usd']:.9f} | ${pair['governance_delta_usd']:.9f} | {pair['governance_delta_percent']}% |")
    report += ["", "## StegVerse-only matched reconstruction comparisons", "", "| Provider lane | Provider cost | StegVerse-only cost | Ratio | Modeled reduction | Valid |", "|---|---:|---:|---:|---:|---:|"]
    for item in replacement_comparisons:
        report.append(f"| {item['provider_lane']} | ${item['provider_lane_cost_usd']:.9f} | ${item['stegverse_only_cost_usd']:.12f} | {item['provider_to_stegverse_cost_ratio']}x | {item['matched_operation_modeled_reduction_percent']}% | {str(item['valid_only_if_both_admissible']).lower()} |")
    report += [
        "",
        "## Derivation",
        "",
        "Provider cost = input_tokens × input_rate + output_tokens × output_rate.",
        "",
        "StegVerse-only local cost = measured runtime_seconds × declared Linux runner rate + output_bytes × declared storage rate.",
        "",
        "Cost ranking occurs only after task identity, exact output, and claim-boundary validation pass.",
        "",
        f"Claim boundary: {task['claim_boundary']}",
    ]
    (OUT / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"all_five_complete": all_five_complete, "selected": selected["lane_id"] if selected else None}))
    return 0 if all_five_complete else 2


if __name__ == "__main__":
    raise SystemExit(main())
