#!/usr/bin/env python3
import hashlib
import json
import math
import os
import pathlib
import statistics
import time
import urllib.request

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)
PROTOCOL = json.loads((ROOT / "protocol.json").read_text())
GOVERNANCE = json.loads((ROOT / "governance.json").read_text())
STAGES = json.loads((ROOT.parents[1] / "staged-math-progress" / "stage_contract.json").read_text())["stages"]
MODEL = os.getenv("ANTHROPIC_MODEL", PROTOCOL["model"])
MAX_OUT = int(PROTOCOL["max_output_tokens_per_stage"])
TEMPERATURE = PROTOCOL["temperature"]
INPUT_RATE = float(PROTOCOL["pricing"]["input_usd_per_million"])
OUTPUT_RATE = float(PROTOCOL["pricing"]["output_usd_per_million"])


def sha_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode())


def post_message(prompt: str) -> dict:
    body = {
        "model": MODEL,
        "max_tokens": MAX_OUT,
        "temperature": TEMPERATURE,
        "messages": [{"role": "user", "content": prompt}],
    }
    payload = json.dumps(body, separators=(",", ":")).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        method="POST",
        headers={
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=900) as response:
        raw_bytes = response.read()
        status = response.status
    latency = time.perf_counter() - started
    raw = json.loads(raw_bytes)
    text = "".join(x.get("text", "") for x in raw.get("content", []) if x.get("type") == "text")
    usage = raw.get("usage", {})
    inp = int(usage.get("input_tokens", 0))
    out = int(usage.get("output_tokens", 0))
    return {
        "body": body,
        "payload": payload,
        "raw": raw,
        "raw_bytes": raw_bytes,
        "text": text,
        "http_status": status,
        "input_tokens": inp,
        "output_tokens": out,
        "cost": inp / 1_000_000 * INPUT_RATE + out / 1_000_000 * OUTPUT_RATE,
        "latency": latency,
    }


def validate(stage_id: str, text: str) -> dict:
    low = text.lower()
    requirements = {
        "S0": [["task identity", "sv-math-001"], ["abstract", "stipulated"], ["deployed", "implementation"], ["unresolved", "out of scope"]],
        "S1": [["gbp"], ["bd"], ["oc"], ["allow"]],
        "S2": [["necessary", "necessity"], ["sufficient", "sufficiency"], ["if and only if", "iff", "↔"]],
        "S3": [["forward", "necessity"], ["reverse", "sufficiency"]],
        "S4": [["proof"], ["forward", "necessity"], ["reverse", "sufficiency"], ["implementation", "deployed", "claim boundary"]],
        "S5": [["```lean", "```lean4"], ["theorem"], ["allow"], ["gbp"], ["bd"], ["oc"]],
        "S6": [["verified", "verification"], ["unresolved"], ["evidence"], ["implementation", "deployed"]],
    }
    missing = [" OR ".join(group) for group in requirements[stage_id] if not any(term in low for term in group)]
    forbidden = any(term in low for term in ("deployed engine satisfies", "production engine satisfies", "verified deployed implementation"))
    return {"pass": not missing and not forbidden, "missing": missing, "forbidden_claim": forbidden}


def excerpt(stage_id: str, text: str) -> str:
    terms = {
        "S0": ["task identity", "claim boundary", "deployed", "unresolved"],
        "S1": ["gbp", "bd", "oc", "allow"],
        "S2": ["theorem", "necessary", "sufficient", "iff"],
        "S3": ["forward", "reverse", "necessity", "sufficiency"],
        "S4": ["proof", "therefore", "hence", "boundary"],
        "S5": ["```lean", "theorem", "def ", "unfold"],
        "S6": ["verified", "unresolved", "evidence", "implementation"],
    }[stage_id]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    selected = [line for line in lines if any(term in line.lower() for term in terms)][:10]
    return "\n".join(selected or lines[:5])[:2200]


def managed_context(stage_id: str, records: list[dict], ledger: list[dict]) -> str:
    needed = {
        "S0": [], "S1": ["S0"], "S2": ["S1"], "S3": ["S1", "S2"],
        "S4": ["S2", "S3"], "S5": ["S1", "S2", "S4"], "S6": ["S4", "S5"],
    }[stage_id]
    compact_ledger = json.dumps(ledger, separators=(",", ":"), ensure_ascii=False)
    selected = "\n\n".join(
        f"[{r['stage_id']}:{r['output_sha256']}]\n{r['excerpt']}"
        for r in records if r["stage_id"] in needed
    )
    return f"ARTIFACT_LEDGER={compact_ledger}\nSELECTED_RETRIEVAL:\n{selected or '[none]'}"


def full_context(records: list[dict]) -> str:
    if not records:
        return "[none]"
    return "\n\n".join(f"[{r['stage_id']}:{r['output_sha256']}]\n{r['output']}" for r in records)


def prompt_for(stage: dict, mode: str, records: list[dict], ledger: list[dict]) -> tuple[str, str]:
    context = full_context(records) if mode == "full" else managed_context(stage["id"], records, ledger)
    prompt = f"""EXPERIMENT: {PROTOCOL['experiment_id']}
TASK: {PROTOCOL['task']['id']}
PROBLEM: {PROTOCOL['task']['problem']}
CURRENT STAGE: {stage['id']} — {stage['name']}
CONTEXT MODE: {mode}
GOVERNANCE: {PROTOCOL['task']['governance']}

Produce only the self-contained artifact required for this stage. Preserve admitted prior state. Do not skip ahead. A hash proves artifact identity, not semantic content. Do not claim deployed implementation validity.

ADMITTED PRIOR STATE:
{context}

Head the response exactly: {stage['id']}: {stage['name']}.
"""
    return prompt, context


def run_lane(trial_id: str, lane: dict) -> dict:
    records, ledger = [], []
    total_in = total_out = 0
    total_cost = total_latency = 0.0
    for stage in STAGES:
        prompt, context = prompt_for(stage, lane["context_mode"], records, ledger)
        response = post_message(prompt)
        validation = validate(stage["id"], response["text"])
        record = {
            "trial_id": trial_id,
            "lane_id": lane["id"],
            "context_mode": lane["context_mode"],
            "stage_id": stage["id"],
            "provider": PROTOCOL["provider"],
            "model_requested": MODEL,
            "model_returned": response["raw"].get("model"),
            "route": PROTOCOL["route"],
            "provider_message_id": response["raw"].get("id"),
            "http_status": response["http_status"],
            "stop_reason": response["raw"].get("stop_reason"),
            "input_tokens": response["input_tokens"],
            "output_tokens": response["output_tokens"],
            "pricing_derived_cost_usd": response["cost"],
            "latency_seconds": response["latency"],
            "complete": response["raw"].get("stop_reason") != "max_tokens",
            "verifier": validation,
            "prompt_sha256": sha_bytes(response["payload"]),
            "context_sha256": sha_text(context),
            "response_sha256": sha_bytes(response["raw_bytes"]),
            "output_sha256": sha_text(response["text"]),
            "excerpt": excerpt(stage["id"], response["text"]),
            "output": response["text"],
        }
        records.append(record)
        ledger.append({
            "stage_id": stage["id"],
            "output_sha256": record["output_sha256"],
            "admitted": validation["pass"],
            "unresolved": "deployed implementation binding remains unresolved",
        })
        total_in += response["input_tokens"]
        total_out += response["output_tokens"]
        total_cost += response["cost"]
        total_latency += response["latency"]
        (OUT / f"{trial_id}-{lane['id']}-{stage['id']}-raw.json").write_bytes(response["raw_bytes"])
        (OUT / f"{trial_id}-{lane['id']}-{stage['id']}.md").write_text(response["text"])
        if not validation["pass"]:
            break
    return {
        "trial_id": trial_id,
        "lane_id": lane["id"],
        "context_mode": lane["context_mode"],
        "attempted_stages": len(records),
        "admitted_stages": sum(1 for r in records if r["verifier"]["pass"]),
        "terminal_stage": records[-1]["stage_id"] if records else "NONE",
        "all_attempted_complete": all(r["complete"] for r in records),
        "all_attempted_verified": all(r["verifier"]["pass"] for r in records),
        "input_tokens": total_in,
        "output_tokens": total_out,
        "total_tokens": total_in + total_out,
        "pricing_derived_cost_usd": total_cost,
        "latency_seconds": total_latency,
        "ledger_sha256": sha_text(json.dumps(ledger, sort_keys=True)),
        "stages": records,
    }


def mean(values):
    return statistics.mean(values) if values else 0.0


def variance(values):
    return statistics.variance(values) if len(values) > 1 else 0.0


def ci95(values):
    if not values:
        return [0.0, 0.0]
    m = mean(values)
    if len(values) < 2:
        return [m, m]
    half = 2.776 * statistics.stdev(values) / math.sqrt(len(values))
    return [m - half, m + half]


all_results = []
trial_ids = PROTOCOL["pairing"]["trial_ids"]
lanes = PROTOCOL["lanes"]
for index, trial_id in enumerate(trial_ids):
    ordered = lanes if index % 2 == 0 else list(reversed(lanes))
    for lane in ordered:
        all_results.append(run_lane(trial_id, lane))

full = sorted((r for r in all_results if r["context_mode"] == "full"), key=lambda r: r["trial_id"])
managed = sorted((r for r in all_results if r["context_mode"] == "managed"), key=lambda r: r["trial_id"])
pairs = []
for left, right in zip(full, managed):
    pairs.append({
        "trial_id": left["trial_id"],
        "input_token_delta_managed_minus_full": right["input_tokens"] - left["input_tokens"],
        "cost_delta_managed_minus_full": right["pricing_derived_cost_usd"] - left["pricing_derived_cost_usd"],
        "latency_delta_managed_minus_full": right["latency_seconds"] - left["latency_seconds"],
        "same_terminal_stage": right["terminal_stage"] == left["terminal_stage"],
        "same_admitted_stage_count": right["admitted_stages"] == left["admitted_stages"],
        "completion_equal": right["all_attempted_complete"] == left["all_attempted_complete"],
        "managed_not_lower_verifier": right["admitted_stages"] >= left["admitted_stages"],
    })
quality_equivalent = all(
    p["same_terminal_stage"] and p["same_admitted_stage_count"] and p["completion_equal"] and p["managed_not_lower_verifier"]
    for p in pairs
)
input_deltas = [p["input_token_delta_managed_minus_full"] for p in pairs]
cost_deltas = [p["cost_delta_managed_minus_full"] for p in pairs]
latency_deltas = [p["latency_delta_managed_minus_full"] for p in pairs]
status = "R3_OBSERVED_AND_VALIDATED" if quality_equivalent else "R3_QUALITY_DIVERGENCE"
result = {
    "experiment_id": PROTOCOL["experiment_id"],
    "relation_id": PROTOCOL["relation_id"],
    "governance_id": GOVERNANCE["governance_id"],
    "transition_status": status,
    "provider": PROTOCOL["provider"],
    "model": MODEL,
    "paired_n": len(pairs),
    "results": all_results,
    "pairs": pairs,
    "statistics": {
        "full_mean_input_tokens": mean([r["input_tokens"] for r in full]),
        "managed_mean_input_tokens": mean([r["input_tokens"] for r in managed]),
        "mean_input_token_delta_managed_minus_full": mean(input_deltas),
        "input_token_delta_variance": variance(input_deltas),
        "input_token_delta_ci95": ci95(input_deltas),
        "full_mean_cost_usd": mean([r["pricing_derived_cost_usd"] for r in full]),
        "managed_mean_cost_usd": mean([r["pricing_derived_cost_usd"] for r in managed]),
        "mean_cost_delta_managed_minus_full": mean(cost_deltas),
        "cost_delta_variance": variance(cost_deltas),
        "cost_delta_ci95": ci95(cost_deltas),
        "mean_latency_delta_managed_minus_full": mean(latency_deltas),
        "latency_delta_ci95": ci95(latency_deltas),
        "full_complete_rate": mean([1.0 if r["all_attempted_complete"] else 0.0 for r in full]),
        "managed_complete_rate": mean([1.0 if r["all_attempted_complete"] else 0.0 for r in managed]),
        "full_all_verified_rate": mean([1.0 if r["all_attempted_verified"] else 0.0 for r in full]),
        "managed_all_verified_rate": mean([1.0 if r["all_attempted_verified"] else 0.0 for r in managed]),
    },
    "publication_gate": {
        "quality_equivalent": quality_equivalent,
        "headline_context_savings_admissible": quality_equivalent and mean(cost_deltas) < 0,
        "pricing_is_invoice_evidence": False,
        "claim_boundary": PROTOCOL["success_criteria"]["claim_boundary"],
    },
}
(OUT / "result.json").write_text(json.dumps(result, indent=2))
print(json.dumps({"transition_status": status, "statistics": result["statistics"], "publication_gate": result["publication_gate"]}, indent=2))
