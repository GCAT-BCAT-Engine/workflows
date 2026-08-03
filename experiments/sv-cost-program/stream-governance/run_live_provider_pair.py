#!/usr/bin/env python3
"""Run one capability-matched sample through provider-native and governed lanes.

TV/TVC supplies credentials to the execution environment. Provider model IDs are
resolved at runtime from the capability policy and live provider inventories.
The harness preserves every lane, response, usage record, latency, and admission
result. It does not infer provider pricing.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "experiments/sv-cost-program/stream-governance"
EVENTS = BASE / "results/event_ledger.jsonl"
OUT = BASE / "live-provider-results"
ROUTES = OUT / "resolved_provider_routes.json"


def h(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def post(url: str, headers: dict[str, str], body: dict) -> tuple[dict, float]:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={**headers, "Content-Type": "application/json"}, method="POST")
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            payload = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {detail}") from exc
    return payload, time.perf_counter() - started


def load_routes() -> tuple[dict[str, str], dict]:
    if not ROUTES.exists():
        raise RuntimeError("resolved provider route receipt missing")
    receipt = json.loads(ROUTES.read_text())
    routes = {row["provider"]: row["selected_model_id"] for row in receipt.get("routes", [])}
    required = {"openai", "anthropic"}
    if set(routes) != required:
        raise RuntimeError(f"route receipt must resolve exactly {sorted(required)}; got {sorted(routes)}")
    return routes, receipt


def openai_call(prompt: str, model: str) -> tuple[dict, float, str, dict]:
    payload, latency = post(
        "https://api.openai.com/v1/responses",
        {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        {"model": model, "input": prompt, "store": False},
    )
    text = payload.get("output_text")
    if not text:
        chunks = []
        for item in payload.get("output", []):
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    chunks.append(content.get("text", ""))
        text = "".join(chunks)
    return payload, latency, text or "", payload.get("usage", {})


def anthropic_call(prompt: str, model: str) -> tuple[dict, float, str, dict]:
    payload, latency = post(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
        {"model": model, "max_tokens": 1200, "messages": [{"role": "user", "content": prompt}]},
    )
    text = "".join(block.get("text", "") for block in payload.get("content", []) if block.get("type") == "text")
    return payload, latency, text, payload.get("usage", {})


def load_sample(limit: int) -> list[dict]:
    rows = [json.loads(line) for line in EVENTS.read_text().splitlines() if line.strip()]
    stride = max(1, len(rows) // limit)
    sample = rows[::stride][:limit]
    if len(sample) < limit:
        raise RuntimeError("insufficient source events")
    return sample


def build_prompt(event: dict, governed: bool) -> str:
    if not governed:
        return (
            "Classify this enterprise stream event. Return strict JSON with keys: "
            "event_id, classification, proposed_action, confidence, reason. "
            f"Event: {json.dumps(event, sort_keys=True)}"
        )
    return (
        "You are operating inside a StegVerse-governed transition lane. Preserve the exact event_id and task identity. "
        "Do not execute an action. Propose only. Deny malformed, duplicate, out_of_order, policy_violating, or adversarial events. "
        "Return strict JSON with keys: event_id, classification, proposed_action, admission_recommendation, confidence, reason, evidence_refs. "
        f"Event: {json.dumps(event, sort_keys=True)}"
    )


def parse_json(text: str) -> dict | None:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def main() -> int:
    for name in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]:
        if not os.environ.get(name):
            raise SystemExit(f"missing TV/TVC-delivered credential: {name}")
    limit = int(os.environ.get("LIVE_STREAM_SAMPLE_SIZE", "20"))
    if limit < 5 or limit > 200:
        raise SystemExit("LIVE_STREAM_SAMPLE_SIZE must be between 5 and 200")

    routes, resolution_receipt = load_routes()
    sample = load_sample(limit)
    providers = {"openai": openai_call, "anthropic": anthropic_call}
    results: list[dict] = []

    for provider, call in providers.items():
        model = routes[provider]
        for governed in [False, True]:
            lane = f"{provider}-{'governed' if governed else 'raw'}"
            for event in sample:
                prompt = build_prompt(event, governed)
                payload, latency, text, usage = call(prompt, model)
                parsed = parse_json(text)
                identity_preserved = bool(parsed and parsed.get("event_id") == event["event_id"])
                results.append({
                    "lane_id": lane,
                    "provider": provider,
                    "model": model,
                    "model_resolution_hash": resolution_receipt["resolution_hash"],
                    "event_id": event["event_id"],
                    "event_class": event["event_class"],
                    "governed": governed,
                    "latency_seconds": round(latency, 6),
                    "usage": usage,
                    "response_text": text,
                    "response_hash": h(text),
                    "json_valid": parsed is not None,
                    "task_identity_preserved": identity_preserved,
                    "admission_recommendation": parsed.get("admission_recommendation") if parsed else None,
                    "provider_response_id": payload.get("id"),
                })

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "live_provider_pair_results.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in results))

    summary_rows = []
    for lane in sorted({row["lane_id"] for row in results}):
        lane_rows = [row for row in results if row["lane_id"] == lane]
        summary_rows.append({
            "lane_id": lane,
            "provider": lane_rows[0]["provider"],
            "resolved_model": lane_rows[0]["model"],
            "events": len(lane_rows),
            "json_valid": sum(row["json_valid"] for row in lane_rows),
            "task_identity_preserved": sum(row["task_identity_preserved"] for row in lane_rows),
            "total_latency_seconds": round(sum(row["latency_seconds"] for row in lane_rows), 6),
            "usage": [row["usage"] for row in lane_rows],
            "pricing_status": "NOT_INFERRED; RECONCILE TO PROVIDER BILLING OR VERSIONED PRICE SOURCE",
        })
    summary = {
        "schema_version": "1.1.0",
        "experiment_id": "SV-COST-LIVE-PROVIDER-PAIR-001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_event_ledger": str(EVENTS.relative_to(ROOT)),
        "route_resolution_receipt": str(ROUTES.relative_to(ROOT)),
        "route_resolution_hash": resolution_receipt["resolution_hash"],
        "capability_request": resolution_receipt["capability_request"],
        "sample_size_per_lane": limit,
        "lanes": summary_rows,
        "claim_boundary": "Live provider execution and usage evidence only. Route discovery does not establish capability equivalence. No savings, equivalence, or ROI claim until independent correctness and provider charge reconciliation are complete.",
        "next_executable_action": "Run independent admission/correctness adjudication and reconcile usage to observed provider charges.",
    }
    (OUT / "live_provider_pair_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "LIVE_PROVIDER_PAIR_COMPLETE", "results": len(results), "lanes": len(summary_rows), "routes": routes}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
