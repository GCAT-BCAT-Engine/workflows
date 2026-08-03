#!/usr/bin/env python3
import hashlib
import json
import os
import pathlib
import time
import urllib.request

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)
PROTOCOL = json.loads((ROOT / "protocol.json").read_text())
MODEL = os.getenv("ANTHROPIC_MODEL", PROTOCOL["known_historical_controls"]["model"])
INPUT_RATE = float(os.getenv("ANTHROPIC_INPUT_USD_PER_M", "3"))
OUTPUT_RATE = float(os.getenv("ANTHROPIC_OUTPUT_USD_PER_M", "15"))


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def post_message(prompt: str, max_tokens: int):
    body = {
        "model": MODEL,
        "max_tokens": max_tokens,
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
    latency = time.perf_counter() - started
    raw = json.loads(raw_bytes)
    text = "".join(part.get("text", "") for part in raw.get("content", []) if part.get("type") == "text")
    usage = raw.get("usage", {})
    input_tokens = int(usage.get("input_tokens", 0))
    output_tokens = int(usage.get("output_tokens", 0))
    cost = input_tokens / 1_000_000 * INPUT_RATE + output_tokens / 1_000_000 * OUTPUT_RATE
    return body, payload, raw, raw_bytes, text, input_tokens, output_tokens, cost, latency


def validate(test_id: str, text: str, raw: dict):
    low = text.lower()
    if test_id == "VAL-001-RERUN":
        checks = {
            "connected_marker": "status: connected" in low,
            "model_path_marker": "model_path: anthropic_sonnet_4_6" in low,
            "provider_message_id": bool(raw.get("id")),
            "model_identity": bool(raw.get("model")),
        }
    else:
        checks = {
            "direct_artifact": len(text.strip()) > 1000,
            "definitions": "definition" in low or "define" in low,
            "necessary_and_sufficient": ("necessary" in low and "sufficient" in low),
            "forward_direction": "forward" in low or "necessity" in low,
            "reverse_direction": "reverse" in low or "sufficiency" in low,
            "lean_candidate": "```lean" in low or "```lean4" in low,
            "claim_boundary": any(term in low for term in ["claim boundary", "deployed", "implementation"]),
            "not_meta_only": not ("here is a plan" in low and len(text.strip()) < 1500),
        }
    return {"checks": checks, "valid": all(checks.values())}


receipts = []
for test in PROTOCOL["tests"]:
    body, payload, raw, raw_bytes, text, input_tokens, output_tokens, cost, latency = post_message(
        test["prompt"], int(test["max_output_tokens"])
    )
    test_id = test["id"]
    validation = validate(test_id, text, raw)
    raw_path = OUT / f"{test_id}-raw.json"
    text_path = OUT / f"{test_id}.md"
    raw_path.write_bytes(raw_bytes)
    text_path.write_text(text)
    receipt = {
        "test_id": test_id,
        "method_status": PROTOCOL["status"],
        "model_requested": MODEL,
        "model_returned": raw.get("model"),
        "provider_message_id": raw.get("id"),
        "provider_stop_reason": raw.get("stop_reason"),
        "max_output_tokens": test["max_output_tokens"],
        "native_input_tokens": input_tokens,
        "native_output_tokens": output_tokens,
        "native_total_tokens": input_tokens + output_tokens,
        "observed_api_cost_usd": cost,
        "pricing_assumption": {
            "input_usd_per_million": INPUT_RATE,
            "output_usd_per_million": OUTPUT_RATE,
        },
        "latency_seconds": latency,
        "request_payload_sha256": sha256_bytes(payload),
        "prompt_sha256": sha256_bytes(test["prompt"].encode()),
        "raw_response_sha256": sha256_bytes(raw_bytes),
        "output_sha256": sha256_bytes(text.encode()),
        "validation": validation,
        "reconstruction_boundary": PROTOCOL["reconstruction_boundary"],
    }
    (OUT / f"{test_id}-receipt.json").write_text(json.dumps(receipt, indent=2))
    receipts.append(receipt)

historical = PROTOCOL["known_historical_controls"]
bl = next(r for r in receipts if r["test_id"] == "BL-001-RERUN")
comparison = {
    "experiment_id": PROTOCOL["experiment_id"],
    "method_status": PROTOCOL["status"],
    "historical": historical,
    "rerun_receipts": receipts,
    "bl_deltas": {
        "tokens_absolute": bl["native_total_tokens"] - historical["historical_bl_observed_tokens"],
        "tokens_percent": (bl["native_total_tokens"] / historical["historical_bl_observed_tokens"] - 1) * 100,
        "cost_usd_absolute": bl["observed_api_cost_usd"] - historical["historical_bl_cost_usd"],
        "cost_percent": (bl["observed_api_cost_usd"] / historical["historical_bl_cost_usd"] - 1) * 100,
        "latency_seconds_absolute_vs_approx": bl["latency_seconds"] - historical["historical_bl_latency_seconds_approx"],
    },
    "claim_boundary": "This is a best-available control-envelope reproduction. It is not a byte-identical replay because the exact historical prompts and payload were not retained."
}
(OUT / "comparison.json").write_text(json.dumps(comparison, indent=2))

lines = [
    "# Historical sv-cost VAL-001 / BL-001 Rerun",
    "",
    f"Method status: {PROTOCOL['status']}",
    "",
    "| Test | Valid | Native tokens | Observed cost | Latency s | Stop reason |",
    "|---|---:|---:|---:|---:|---|",
]
for receipt in receipts:
    lines.append(
        f"| {receipt['test_id']} | {str(receipt['validation']['valid']).upper()} | "
        f"{receipt['native_total_tokens']:,} | ${receipt['observed_api_cost_usd']:.6f} | "
        f"{receipt['latency_seconds']:.2f} | {receipt['provider_stop_reason']} |"
    )
lines += [
    "",
    "## BL-001 historical comparison",
    "",
    f"- Historical tokens: {historical['historical_bl_observed_tokens']:,}",
    f"- Rerun tokens: {bl['native_total_tokens']:,}",
    f"- Token delta: {comparison['bl_deltas']['tokens_absolute']:+,} ({comparison['bl_deltas']['tokens_percent']:+.2f}%)",
    f"- Historical cost: ${historical['historical_bl_cost_usd']:.6f}",
    f"- Rerun observed cost: ${bl['observed_api_cost_usd']:.6f}",
    f"- Cost delta: ${comparison['bl_deltas']['cost_usd_absolute']:+.6f} ({comparison['bl_deltas']['cost_percent']:+.2f}%)",
    f"- Historical latency: approximately {historical['historical_bl_latency_seconds_approx']:.1f}s",
    f"- Rerun latency: {bl['latency_seconds']:.2f}s",
    "",
    "## Reconstruction boundary",
    "",
    PROTOCOL["reconstruction_boundary"],
]
(OUT / "report.md").write_text("\n".join(lines) + "\n")
print(json.dumps(comparison, indent=2))
