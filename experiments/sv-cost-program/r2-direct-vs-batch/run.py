#!/usr/bin/env python3
import concurrent.futures
import hashlib
import json
import math
import os
import pathlib
import statistics
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)
PROTOCOL = json.loads((ROOT / "protocol.json").read_text())
GOVERNANCE = json.loads((ROOT / "governance.json").read_text())
API_KEY = os.environ["ANTHROPIC_API_KEY"]
BASE = "https://api.anthropic.com"
HEADERS = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}


def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def sha256(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


def request_json(method, path, body=None, timeout=900):
    data = canonical_bytes(body) if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=HEADERS)
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read()
            return response.status, raw, time.perf_counter() - started
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        raise RuntimeError(f"HTTP {exc.code} {path}: {raw.decode(errors='replace')}") from exc


def text_from_message(message):
    return "".join(
        part.get("text", "")
        for part in message.get("content", [])
        if part.get("type") == "text"
    )


def verify(text):
    low = text.lower()
    checks = {
        "direct_artifact": len(text.strip()) > 1000,
        "definitions": "definition" in low or "define" in low,
        "necessary_and_sufficient": "necessary" in low and "sufficient" in low,
        "forward_direction": "forward" in low or "necessity" in low,
        "reverse_direction": "reverse" in low or "sufficiency" in low,
        "implementation_claim_boundary": any(x in low for x in ("deployed", "implementation", "abstract proof")),
        "not_meta_only": not ("here is a plan" in low and len(text.strip()) < 1500),
    }
    return {"checks": checks, "pass": all(checks.values())}


def params():
    return {
        "model": PROTOCOL["model"],
        "max_tokens": PROTOCOL["max_output_tokens"],
        "temperature": PROTOCOL["temperature"],
        "messages": [{"role": "user", "content": PROTOCOL["prompt"]}],
    }


def cost(usage, lane):
    rates = PROTOCOL["lanes"][lane]["pricing_usd_per_million"]
    return usage.get("input_tokens", 0) / 1_000_000 * rates["input"] + usage.get("output_tokens", 0) / 1_000_000 * rates["output"]


def normalize(trial_id, lane, message, latency, request_hash, route_id):
    text = text_from_message(message)
    usage = message.get("usage") or {}
    result = {
        "trial_id": trial_id,
        "lane": lane,
        "provider": "anthropic",
        "model_requested": PROTOCOL["model"],
        "model_returned": message.get("model"),
        "route_id": route_id,
        "provider_message_id": message.get("id"),
        "stop_reason": message.get("stop_reason"),
        "input_tokens": int(usage.get("input_tokens", 0)),
        "output_tokens": int(usage.get("output_tokens", 0)),
        "total_tokens": int(usage.get("input_tokens", 0)) + int(usage.get("output_tokens", 0)),
        "pricing_derived_cost_usd": cost(usage, lane),
        "latency_seconds": latency,
        "complete": message.get("stop_reason") != "max_tokens",
        "verifier": verify(text),
        "request_sha256": request_hash,
        "response_sha256": sha256(canonical_bytes(message)),
        "output_sha256": sha256(text.encode()),
    }
    (OUT / f"{lane}-{trial_id}.json").write_text(json.dumps({"result": result, "raw": message}, indent=2))
    return result


def direct_trial(index):
    trial_id = f"T{index:02d}"
    body = params()
    status, raw, latency = request_json("POST", "/v1/messages", body)
    if status < 200 or status >= 300:
        raise RuntimeError(f"direct {trial_id} status {status}")
    message = json.loads(raw)
    return normalize(trial_id, "direct", message, latency, sha256(canonical_bytes(body)), "messages")


def run_direct():
    count = PROTOCOL["trial_count_per_lane"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        return list(pool.map(direct_trial, range(1, count + 1)))


def run_batch():
    count = PROTOCOL["trial_count_per_lane"]
    request_params = params()
    requests = [{"custom_id": f"T{i:02d}", "params": request_params} for i in range(1, count + 1)]
    body = {"requests": requests}
    status, raw, submit_latency = request_json("POST", "/v1/messages/batches", body)
    if status < 200 or status >= 300:
        raise RuntimeError(f"batch submit status {status}")
    batch = json.loads(raw)
    batch_id = batch["id"]
    submitted_at = time.time()
    while True:
        _, poll_raw, _ = request_json("GET", f"/v1/messages/batches/{batch_id}", timeout=120)
        batch = json.loads(poll_raw)
        if batch.get("processing_status") == "ended":
            break
        if time.time() - submitted_at > 18000:
            raise TimeoutError(f"batch {batch_id} did not end within five hours")
        time.sleep(30)
    _, results_raw, _ = request_json("GET", f"/v1/messages/batches/{batch_id}/results", timeout=900)
    (OUT / "batch-results.jsonl").write_bytes(results_raw)
    elapsed = time.time() - submitted_at + submit_latency
    records = []
    for line in results_raw.splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        trial_id = item["custom_id"]
        result = item.get("result", {})
        if result.get("type") != "succeeded":
            records.append({"trial_id": trial_id, "lane": "batch", "batch_id": batch_id, "result_type": result.get("type"), "error": result})
            continue
        message = result["message"]
        records.append(normalize(trial_id, "batch", message, elapsed, sha256(canonical_bytes(request_params)), batch_id))
    (OUT / "batch-metadata.json").write_text(json.dumps(batch, indent=2))
    return records, batch_id


def mean(xs):
    return statistics.mean(xs) if xs else None


def sample_sd(xs):
    return statistics.stdev(xs) if len(xs) > 1 else None


def ci95(xs):
    if len(xs) < 2:
        return None
    m = statistics.mean(xs)
    margin = 1.96 * statistics.stdev(xs) / math.sqrt(len(xs))
    return [m - margin, m + margin]


def summarize(direct, batch, batch_id):
    dmap = {r["trial_id"]: r for r in direct if "pricing_derived_cost_usd" in r}
    bmap = {r["trial_id"]: r for r in batch if "pricing_derived_cost_usd" in r}
    pairs = []
    for trial_id in sorted(set(dmap) & set(bmap)):
        d, b = dmap[trial_id], bmap[trial_id]
        pairs.append({
            "trial_id": trial_id,
            "direct_cost_usd": d["pricing_derived_cost_usd"],
            "batch_cost_usd": b["pricing_derived_cost_usd"],
            "cost_delta_usd": b["pricing_derived_cost_usd"] - d["pricing_derived_cost_usd"],
            "cost_reduction_percent": (1 - b["pricing_derived_cost_usd"] / d["pricing_derived_cost_usd"]) * 100 if d["pricing_derived_cost_usd"] else None,
            "token_delta": b["total_tokens"] - d["total_tokens"],
            "direct_verifier_pass": d["verifier"]["pass"],
            "batch_verifier_pass": b["verifier"]["pass"],
            "direct_complete": d["complete"],
            "batch_complete": b["complete"],
        })
    deltas = [p["cost_delta_usd"] for p in pairs]
    reductions = [p["cost_reduction_percent"] for p in pairs if p["cost_reduction_percent"] is not None]
    invariant_hash = sha256(canonical_bytes(params()))
    all_request_hashes = {r.get("request_sha256") for r in direct + batch if r.get("request_sha256")}
    admitted = (
        len(pairs) > 0
        and len(all_request_hashes) == 1
        and all(r.get("provider_message_id") for r in direct if "pricing_derived_cost_usd" in r)
        and bool(batch_id)
    )
    return {
        "experiment_id": PROTOCOL["experiment_id"],
        "relation_id": PROTOCOL["relation_id"],
        "governance_id": GOVERNANCE["governance_id"],
        "transition_status": "R2_OBSERVED_AND_VALIDATED" if admitted else "R2_EVIDENCE_INCOMPLETE",
        "provider": PROTOCOL["provider"],
        "model": PROTOCOL["model"],
        "trial_count_requested_per_lane": PROTOCOL["trial_count_per_lane"],
        "direct_results": direct,
        "batch_results": batch,
        "batch_id": batch_id,
        "request_contract_sha256": invariant_hash,
        "all_observed_request_hashes": sorted(all_request_hashes),
        "paired_trials": pairs,
        "statistics": {
            "paired_n": len(pairs),
            "mean_cost_delta_usd": mean(deltas),
            "sample_sd_cost_delta_usd": sample_sd(deltas),
            "paired_cost_delta_95pct_ci_usd": ci95(deltas),
            "mean_cost_reduction_percent": mean(reductions),
            "direct_verifier_pass_rate": mean([1 if r["verifier"]["pass"] else 0 for r in dmap.values()]),
            "batch_verifier_pass_rate": mean([1 if r["verifier"]["pass"] else 0 for r in bmap.values()]),
            "direct_completion_rate": mean([1 if r["complete"] else 0 for r in dmap.values()]),
            "batch_completion_rate": mean([1 if r["complete"] else 0 for r in bmap.values()]),
        },
        "claim_boundary": PROTOCOL["claim_boundary"],
    }


def main():
    prior = pathlib.Path("experiments/sv-cost-program/results/historical-lineage-observation.json")
    if not prior.exists():
        raise SystemExit("required prior-state receipt is missing")
    prior_state = json.loads(prior.read_text())
    if prior_state.get("status") != "OBSERVED_AND_VALIDATED":
        raise SystemExit("prior-state governance does not admit R2 execution")
    direct = run_direct()
    batch, batch_id = run_batch()
    summary = summarize(direct, batch, batch_id)
    summary["workflow"] = {
        "run_id": os.getenv("GITHUB_RUN_ID"),
        "run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "commit_sha": os.getenv("GITHUB_SHA"),
    }
    (OUT / "result.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({"transition_status": summary["transition_status"], "paired_n": summary["statistics"]["paired_n"], "batch_id": batch_id}, indent=2))
    if summary["transition_status"] != "R2_OBSERVED_AND_VALIDATED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
