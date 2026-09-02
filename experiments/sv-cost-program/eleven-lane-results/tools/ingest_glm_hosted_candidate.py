#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEST = ROOT / "candidate-inputs" / "glm-hosted.json"

FORBIDDEN_KEY_PARTS = (
    "api_key","apikey","token","bearer","password","secret",
    "authorization","credential","private_key"
)

def walk_keys(value: Any, path: str = "$") -> list[str]:
    failures: list[str] = []
    if isinstance(value, dict):
        for k, v in value.items():
            lk = str(k).lower()
            if any(part in lk for part in FORBIDDEN_KEY_PARTS):
                failures.append(f"{path}.{k}")
            failures.extend(walk_keys(v, f"{path}.{k}"))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            failures.extend(walk_keys(v, f"{path}[{i}]"))
    return failures

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=pathlib.Path, help="JSON containing the exact GLM-5.3-Flash candidate output or a wrapper with candidate_output")
    ap.add_argument("--model", default="GLM-5.3-Flash")
    ap.add_argument("--response-id")
    ap.add_argument("--latency-seconds", type=float)
    ap.add_argument("--input-tokens", type=int)
    ap.add_argument("--output-tokens", type=int)
    ap.add_argument("--reported-cost-usd", type=float)
    ap.add_argument("--dest", type=pathlib.Path, default=DEST)
    ns = ap.parse_args()

    raw = json.loads(ns.source.read_text())
    forbidden = walk_keys(raw)
    if forbidden:
        raise SystemExit("forbidden credential-like fields observed: " + ", ".join(forbidden))

    candidate = raw.get("candidate_output") if isinstance(raw, dict) and "candidate_output" in raw else raw
    if not isinstance(candidate, dict):
        raise SystemExit("candidate output must be a JSON object")
    if candidate.get("task_id") != "SV-RECON-001":
        raise SystemExit("candidate task_id must be SV-RECON-001")

    usage: dict[str, Any] = {}
    if ns.input_tokens is not None:
        usage["input_tokens"] = ns.input_tokens
    if ns.output_tokens is not None:
        usage["output_tokens"] = ns.output_tokens
    if ns.reported_cost_usd is not None:
        usage["reported_cost_usd"] = ns.reported_cost_usd

    record = {
        "provider": "zai",
        "model": ns.model,
        "task_id": "SV-RECON-001",
        "provider_api_key_transferred_to_stegverse": False,
        "provider_response_id": ns.response_id,
        "provider_latency_seconds": ns.latency_seconds,
        "provider_usage": usage,
        "candidate_output": candidate,
    }

    if record["model"] != "GLM-5.3-Flash":
        raise SystemExit("model must be GLM-5.3-Flash")
    if ns.latency_seconds is not None and ns.latency_seconds < 0:
        raise SystemExit("latency must be nonnegative")
    for name in ("input_tokens","output_tokens"):
        if name in usage and usage[name] < 0:
            raise SystemExit(f"{name} must be nonnegative")
    if usage.get("reported_cost_usd", 0) < 0:
        raise SystemExit("reported cost must be nonnegative")

    ns.dest.parent.mkdir(parents=True, exist_ok=True)
    ns.dest.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({
        "status": "INSTALLED",
        "destination": str(ns.dest),
        "provider": "zai",
        "model": "GLM-5.3-Flash",
        "provider_api_key_transferred_to_stegverse": False,
        "usage_fields_preserved": sorted(usage),
    }, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
