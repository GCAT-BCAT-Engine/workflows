#!/usr/bin/env python3
"""Resolve provider model routes from capability policy and live provider inventories.

Credentials are supplied by TV/TVC to the execution environment. This resolver
never writes credential values. It emits a no-secret route-resolution receipt.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POLICY_PATH = ROOT / "experiments/sv-cost-program/cost-model/provider-capability-policy.json"
OUT_DIR = ROOT / "experiments/sv-cost-program/stream-governance/live-provider-results"
OUT_PATH = OUT_DIR / "resolved_provider_routes.json"


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def get_json(url: str, headers: dict[str, str]) -> dict:
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from model inventory endpoint: {detail}") from exc


def matches_any(value: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in patterns)


def rank_model(model_id: str, preferences: list[str]) -> tuple[int, str]:
    for index, pattern in enumerate(preferences):
        if re.search(pattern, model_id, flags=re.IGNORECASE):
            return index, model_id
    return len(preferences), model_id


def provider_headers(provider: str, adapter: dict) -> dict[str, str]:
    if provider == "openai":
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY was not delivered by TV/TVC")
        headers = {adapter["auth_header"]: f"{adapter.get('auth_scheme', '')} {key}".strip()}
    elif provider == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY was not delivered by TV/TVC")
        headers = {adapter["auth_header"]: key}
    else:
        raise RuntimeError(f"unsupported provider adapter: {provider}")
    headers.update(adapter.get("extra_headers", {}))
    return headers


def resolve_provider(provider: str, adapter: dict) -> dict:
    payload = get_json(adapter["list_models_url"], provider_headers(provider, adapter))
    rows = payload.get(adapter["response_list_field"], [])
    ids = sorted({str(row.get(adapter["model_id_field"], "")) for row in rows if row.get(adapter["model_id_field"])})
    selection = adapter["selection"]
    candidates = []
    excluded = []
    for model_id in ids:
        if selection.get("include_patterns") and not matches_any(model_id, selection["include_patterns"]):
            excluded.append({"model_id": model_id, "reason": "NO_INCLUDE_PATTERN_MATCH"})
            continue
        if selection.get("exclude_patterns") and matches_any(model_id, selection["exclude_patterns"]):
            excluded.append({"model_id": model_id, "reason": "EXCLUDE_PATTERN_MATCH"})
            continue
        candidates.append(model_id)
    if not candidates:
        raise RuntimeError(f"no eligible {provider} route matched capability policy")
    selected = sorted(candidates, key=lambda mid: rank_model(mid, selection.get("preference_patterns", [])))[0]
    return {
        "provider": provider,
        "selected_model_id": selected,
        "eligible_candidates": candidates,
        "excluded_candidates": excluded,
        "discovered_model_count": len(ids),
        "selection_basis": {
            "include_patterns": selection.get("include_patterns", []),
            "exclude_patterns": selection.get("exclude_patterns", []),
            "preference_patterns": selection.get("preference_patterns", []),
        },
    }


def main() -> int:
    policy_text = POLICY_PATH.read_text()
    policy = json.loads(policy_text)
    request = policy["request_contract"]
    routes = []
    for provider in request["required_providers"]:
        adapter = policy["provider_adapters"].get(provider)
        if not adapter:
            raise SystemExit(f"missing provider adapter in capability policy: {provider}")
        routes.append(resolve_provider(provider, adapter))

    receipt = {
        "schema_version": "1.0.0",
        "receipt_type": "TV_TVC_NO_SECRET_MODEL_ROUTE_RESOLUTION",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "capability_request": request,
        "policy_path": str(POLICY_PATH.relative_to(ROOT)),
        "policy_hash": sha256_text(policy_text),
        "routes": routes,
        "credentials_recorded": False,
        "authority_boundary": "Credentials were supplied by TV/TVC to the execution environment; this receipt contains no credential values and does not independently grant execution authority.",
    }
    canonical = json.dumps(receipt, sort_keys=True)
    receipt["resolution_hash"] = sha256_text(canonical)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "ROUTES_RESOLVED", "routes": {r['provider']: r['selected_model_id'] for r in routes}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
