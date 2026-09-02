#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEST = ROOT / "runtime-evidence" / "glm-sovereign.json"
RECEIPT = ROOT / "evidence" / "glm-sovereign-resident-intake.json"

EXPECTED_STATE = {"balance": 75, "risk_score": 3, "standing": "active"}
EXPECTED_SEQUENCE = [
    ("E01", "ALLOW"), ("E02", "ALLOW"), ("E03", "ALLOW"),
    ("E04", "DENY"), ("E05", "DENY"), ("E06", "ALLOW"),
]
FORBIDDEN_KEY_PARTS = (
    "api_key", "apikey", "bearer", "password", "secret",
    "authorization", "private_key", "mnemonic", "seed", "access_token",
)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def walk_forbidden_keys(value: Any, path: str = "$") -> list[str]:
    failures: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if any(part in lowered for part in FORBIDDEN_KEY_PARTS):
                failures.append(f"{path}.{key}")
            failures.extend(walk_forbidden_keys(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            failures.extend(walk_forbidden_keys(child, f"{path}[{index}]"))
    return failures


def unwrap(raw: Any) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("resident sovereign evidence must be a JSON object")
    if "consumer_evidence" in raw:
        raw = raw["consumer_evidence"]
    elif isinstance(raw.get("result"), dict) and isinstance(raw["result"].get("consumer_evidence"), dict):
        raw = raw["result"]["consumer_evidence"]
    if not isinstance(raw, dict):
        raise ValueError("consumer_evidence must be a JSON object")
    return raw


def validate(evidence: dict) -> None:
    forbidden = walk_forbidden_keys(evidence)
    if forbidden:
        raise ValueError("forbidden credential-like fields observed: " + ", ".join(forbidden))

    if evidence.get("model") != "GLM-5.3-Flash":
        raise ValueError("model must be GLM-5.3-Flash")
    if evidence.get("task_id") != "SV-RECON-001":
        raise ValueError("task_id must be SV-RECON-001")
    if evidence.get("vendor_api_credential_used") is not False:
        raise ValueError("vendor_api_credential_used must be false")
    if evidence.get("endpoint_class") != "SOVEREIGN_OPENAI_COMPATIBLE":
        raise ValueError("endpoint_class must be SOVEREIGN_OPENAI_COMPATIBLE")
    runtime_identity = evidence.get("runtime_identity")
    if not isinstance(runtime_identity, str) or not runtime_identity.strip():
        raise ValueError("runtime_identity is required")

    candidate = evidence.get("candidate_output")
    if not isinstance(candidate, dict):
        raise ValueError("candidate_output is required")
    if candidate.get("task_id") != "SV-RECON-001":
        raise ValueError("candidate_output task_id mismatch")
    if candidate.get("final_state") != EXPECTED_STATE:
        raise ValueError("candidate_output final_state mismatch")
    decisions = candidate.get("decisions")
    if not isinstance(decisions, list):
        raise ValueError("candidate_output decisions missing")
    sequence = [
        (item.get("event_id"), str(item.get("status") or "").upper())
        for item in decisions if isinstance(item, dict)
    ]
    if sequence != EXPECTED_SEQUENCE:
        raise ValueError("candidate_output decision sequence mismatch")
    if candidate.get("applied_count") != 4 or candidate.get("denied_count") != 2:
        raise ValueError("candidate_output counts mismatch")
    if candidate.get("claim_boundary") != "DETERMINISTIC_RECONSTRUCTION_ONLY":
        raise ValueError("candidate_output claim_boundary mismatch")

    metrics = evidence.get("metrics")
    if not isinstance(metrics, dict):
        raise ValueError("metrics are required")
    elapsed = metrics.get("elapsed_seconds")
    if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed < 0:
        raise ValueError("elapsed_seconds must be a nonnegative number")
    for key in (
        "energy_kwh",
        "hardware_amortization_usd",
        "energy_cost_usd",
        "storage_network_runtime_overhead_usd",
    ):
        value = metrics.get(key)
        if value is not None and (
            not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0
        ):
            raise ValueError(f"{key} must be null or a nonnegative number")


def install(source: pathlib.Path, dest: pathlib.Path, receipt_path: pathlib.Path) -> dict:
    source_raw = source.read_bytes()
    parsed = json.loads(source_raw)
    evidence = unwrap(parsed)
    validate(evidence)

    canonical = (json.dumps(evidence, indent=2, sort_keys=True) + "\n").encode()
    source_sha256 = sha256_bytes(source_raw)
    evidence_sha256 = sha256_bytes(canonical)

    if dest.exists():
        existing = dest.read_bytes()
        if existing != canonical:
            raise ValueError("destination already contains different sovereign evidence")
        state = "ALREADY_INSTALLED_IDENTICAL"
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(canonical)
        state = "INSTALLED"

    receipt = {
        "schema": "stegverse.glm53-sovereign-resident-evidence-intake/v1",
        "state": state,
        "source": str(source),
        "destination": str(dest),
        "source_sha256": source_sha256,
        "installed_evidence_sha256": evidence_sha256,
        "model": "GLM-5.3-Flash",
        "task_id": "SV-RECON-001",
        "runtime_identity": evidence["runtime_identity"],
        "vendor_api_credential_used": False,
        "network_fetch_performed": False,
        "provider_operation_performed": False,
        "hosted_inference_substitution_performed": False,
        "publication_authorized": False,
        "credential_authority": "TV/TVC",
        "authority_effect": "NONE_EVIDENCE_INTAKE_ONLY",
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Install exact credential-clean resident GLM-5.3-Flash sovereign evidence."
    )
    ap.add_argument("source", type=pathlib.Path)
    ap.add_argument("--dest", type=pathlib.Path, default=DEST)
    ap.add_argument("--receipt", type=pathlib.Path, default=RECEIPT)
    ns = ap.parse_args()
    try:
        receipt = install(ns.source, ns.dest, ns.receipt)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc))
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
