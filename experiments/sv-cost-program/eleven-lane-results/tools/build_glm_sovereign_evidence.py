#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEST = ROOT / "runtime-evidence" / "glm-sovereign.json"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate", type=pathlib.Path, help="Exact JSON output returned by sovereign GLM-5.3-Flash")
    ap.add_argument("--runtime-identity", required=True)
    ap.add_argument("--elapsed-seconds", required=True, type=float)
    ap.add_argument("--energy-kwh", type=float)
    ap.add_argument("--hardware-amortization-usd", type=float)
    ap.add_argument("--energy-cost-usd", type=float)
    ap.add_argument("--storage-network-runtime-overhead-usd", type=float)
    ap.add_argument("--dest", type=pathlib.Path, default=DEST)
    ns = ap.parse_args()

    if ns.elapsed_seconds < 0:
        raise SystemExit("elapsed seconds must be nonnegative")
    candidate = json.loads(ns.candidate.read_text())
    if not isinstance(candidate, dict) or candidate.get("task_id") != "SV-RECON-001":
        raise SystemExit("candidate must be the SV-RECON-001 JSON object")

    metrics = {"elapsed_seconds": ns.elapsed_seconds}
    for key, value in {
        "energy_kwh": ns.energy_kwh,
        "hardware_amortization_usd": ns.hardware_amortization_usd,
        "energy_cost_usd": ns.energy_cost_usd,
        "storage_network_runtime_overhead_usd": ns.storage_network_runtime_overhead_usd,
    }.items():
        if value is not None:
            if value < 0:
                raise SystemExit(f"{key} must be nonnegative")
            metrics[key] = value

    evidence = {
        "model": "GLM-5.3-Flash",
        "task_id": "SV-RECON-001",
        "vendor_api_credential_used": False,
        "runtime_identity": ns.runtime_identity,
        "endpoint_class": "SOVEREIGN_OPENAI_COMPATIBLE",
        "candidate_output": candidate,
        "metrics": metrics,
    }

    ns.dest.parent.mkdir(parents=True, exist_ok=True)
    ns.dest.write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps({
        "status": "INSTALLED",
        "destination": str(ns.dest),
        "runtime_identity": ns.runtime_identity,
        "vendor_api_credential_used": False,
        "measured_fields": sorted(metrics),
    }, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
