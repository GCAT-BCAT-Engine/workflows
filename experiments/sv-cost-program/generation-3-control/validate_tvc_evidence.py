#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

EVIDENCE_SCHEMA = "stegverse.tvc.provider-measurement-evidence.v1"
PROVIDERS = {"openai", "anthropic", "deepseek", "kimi"}
REQUIRED_OUTPUT_HASH = "sha256:bb775b0ada3f33c16adb2f26919f465c5121f9b218d181344fe62908380575cf"
PROHIBITED_KEYS = {
    "authorization", "api_key", "apikey", "bearer", "bearer_token", "credential",
    "credentials", "password", "secret", "secret_value", "github_token", "gh_token",
}


class EvidenceError(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def reject_secret_fields(value: Any, path: str = "evidence") -> None:
    if isinstance(value, Mapping):
        for raw_key, child in value.items():
            key = str(raw_key).lower().replace("-", "_")
            if key in PROHIBITED_KEYS or any(marker in key for marker in ("api_key", "password", "secret_value", "bearer_token")):
                raise EvidenceError(f"secret-like field prohibited: {path}.{raw_key}")
            reject_secret_fields(child, f"{path}.{raw_key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_secret_fields(child, f"{path}[{index}]")


def validate_packet(packet: Mapping[str, Any], expected_provider: str | None = None) -> dict[str, Any]:
    reject_secret_fields(packet)
    if packet.get("schema") != EVIDENCE_SCHEMA:
        raise EvidenceError("unexpected evidence schema")
    provider = str(packet.get("provider") or "")
    if provider not in PROVIDERS:
        raise EvidenceError("provider not admitted")
    if expected_provider is not None and provider != expected_provider:
        raise EvidenceError("provider does not match expected slot")
    if packet.get("provider_api_key_transferred_to_consumer") is not False:
        raise EvidenceError("provider credential crossed consumer boundary")
    if packet.get("secret_material_returned") is not False:
        raise EvidenceError("secret material returned")
    for key in ("provider_response_id", "model", "candidate_output"):
        if not isinstance(packet.get(key), str) or not str(packet[key]).strip():
            raise EvidenceError(f"missing {key}")
    if not isinstance(packet.get("provider_usage"), Mapping) or not isinstance(packet.get("normalized_usage"), Mapping):
        raise EvidenceError("actual provider usage required")
    if packet.get("cost_status") != "REQUEST_BOUND_COST":
        raise EvidenceError("request-bound cost required")
    if packet.get("cost_basis") != "EXACT_PROVIDER_USAGE_X_OFFICIAL_MODEL_RATE_CARD":
        raise EvidenceError("inadmissible cost basis")
    if not isinstance(packet.get("calculated_request_cost_usd"), str):
        raise EvidenceError("calculated request cost required")
    rate = packet.get("rate_card")
    if not isinstance(rate, Mapping):
        raise EvidenceError("rate card required")
    if rate.get("provider") != provider or rate.get("model") != packet.get("model"):
        raise EvidenceError("rate card provider/model mismatch")
    source = rate.get("source")
    if not isinstance(source, str) or not source.startswith("https://"):
        raise EvidenceError("official HTTPS rate-card source required")
    if not isinstance(rate.get("observed_at"), str) or not rate.get("observed_at"):
        raise EvidenceError("rate-card observation time required")
    try:
        candidate = json.loads(str(packet["candidate_output"]))
    except json.JSONDecodeError as exc:
        raise EvidenceError("candidate output is not JSON") from exc
    if digest(candidate) != REQUIRED_OUTPUT_HASH:
        raise EvidenceError("candidate output does not match canonical SV-RECON-001 result")
    if candidate.get("task_id") != "SV-RECON-001":
        raise EvidenceError("candidate task identity mismatch")
    return {
        "provider": provider,
        "model": packet["model"],
        "provider_response_id": packet["provider_response_id"],
        "candidate_output_hash": digest(candidate),
        "calculated_request_cost_usd": packet["calculated_request_cost_usd"],
        "cost_status": packet["cost_status"],
        "secret_boundary": "PASS",
        "provider_authority_effect": "NONE_CONTROL_EVIDENCE_ONLY",
    }


def validate_bundle(directory: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for provider in sorted(PROVIDERS):
        path = directory / f"{provider}.json"
        if not path.is_file():
            raise EvidenceError(f"missing provider evidence: {provider}")
        packet = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(packet, dict):
            raise EvidenceError(f"provider evidence must be object: {provider}")
        results[provider] = validate_packet(packet, provider)
    return {
        "schema": "stegverse.sv-cost.generation-3-control-validation.v1",
        "state": "PASS_ALL_FOUR_TVC_CONTROL_ENVELOPES",
        "primary_provider": "stegverse_local",
        "third_party_role": "CONTROL_OR_FALLBACK_ONLY",
        "providers": results,
        "provider_credentials_received": False,
        "non_tv_tvc_secret_or_token_used": False,
        "publication_authority_granted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_dir", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = validate_bundle(args.evidence_dir)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
