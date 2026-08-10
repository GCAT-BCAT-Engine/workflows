from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / "contracts" / "tvc-provider-capability-v1.json"


def stable_hash(value: Any) -> str:
    import hashlib
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def load_pin() -> dict[str, Any]:
    pin = json.loads(PIN_PATH.read_text(encoding="utf-8"))
    if pin.get("schema_version") != "stegverse.consumer-contract-pin.v1":
        raise RuntimeError("tvc_contract_pin_schema_mismatch")
    if pin.get("source_repository") != "StegVerse-Labs/TVC":
        raise RuntimeError("tvc_contract_source_repository_mismatch")
    if pin.get("route_authority") != "StegVerse-Labs/TVC":
        raise RuntimeError("tvc_contract_route_authority_mismatch")
    if pin.get("credential_authority") != "TC/TVC":
        raise RuntimeError("tvc_contract_credential_authority_mismatch")
    if pin.get("github_token_required") is not False:
        raise RuntimeError("tvc_contract_github_token_dependency")
    if pin.get("consumer_policy_authority") is not False or pin.get("fallback_to_local_policy_allowed") is not False:
        raise RuntimeError("consumer_policy_authority_not_disabled")
    return pin


def candidate_tvc_roots() -> list[Path]:
    roots: list[Path] = []
    override = os.environ.get("STEGVERSE_TVC_ROOT")
    if override:
        roots.append(Path(override).expanduser().resolve())
    roots.extend([
        (ROOT / "workloads" / "StegVerse-Labs" / "TVC").resolve(),
        (ROOT / "workloads" / "TVC").resolve(),
        (Path.home() / ".stegverse" / "workloads" / "StegVerse-Labs" / "TVC").resolve(),
        Path("/var/lib/stegverse/workloads/StegVerse-Labs/TVC"),
    ])
    return roots


def find_tvc_root() -> Path | None:
    pin = load_pin()
    required = (
        Path(pin["resolver_path"]),
        Path(pin["policy_path"]),
        Path(pin["request_schema_path"]),
        Path(pin["receipt_schema_path"]),
        Path(pin["source_task"]),
    )
    for root in candidate_tvc_roots():
        if all((root / relative).is_file() for relative in required):
            return root.resolve()
    return None


def load_tvc(root: Path):
    pin = load_pin()
    policy = json.loads((root / pin["policy_path"]).read_text(encoding="utf-8"))
    if stable_hash(policy) != pin["policy_stable_sha256"]:
        raise RuntimeError("tvc_provider_capability_policy_hash_mismatch")
    if policy.get("credential_authority") != "TC/TVC" or policy.get("authority") != "StegVerse-Labs/TVC":
        raise RuntimeError("tvc_provider_capability_policy_authority_mismatch")
    spec = importlib.util.spec_from_file_location("pinned_tvc_provider_capability_resolver", root / pin["resolver_path"])
    if not spec or not spec.loader:
        raise RuntimeError("tvc_provider_capability_resolver_unloadable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, policy


def resolve_via_tvc(request: Mapping[str, Any], *, tvc_root: Path | None = None) -> dict[str, Any]:
    root = tvc_root or find_tvc_root()
    if root is None:
        raise RuntimeError("canonical_tvc_provider_capability_contract_not_materialized")
    module, policy = load_tvc(root)
    receipt = module.resolve(request, policy=policy)
    if not module.verify_receipt(receipt):
        raise RuntimeError("canonical_tvc_provider_route_receipt_invalid")
    if receipt.get("route_authority") != "StegVerse-Labs/TVC":
        raise RuntimeError("canonical_tvc_route_authority_mismatch")
    if receipt.get("credential_authority") != "TC/TVC":
        raise RuntimeError("canonical_tvc_credential_authority_mismatch")
    if receipt.get("github_token_required") is not False or receipt.get("execution_authority") is not False:
        raise RuntimeError("canonical_tvc_authority_boundary_violation")
    return receipt


def build_provider_inventory(rows: list[Mapping[str, Any]], *, capability: str) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        inventory.append({
            "provider_id": str(row.get("provider_id") or row.get("provider") or f"provider-{index}"),
            "provider_class": str(row.get("provider_class") or ""),
            "model_class": row.get("model_class"),
            "capabilities": list(row.get("capabilities") or [capability]),
            "available": row.get("available") is not False,
            "priority": int(row.get("priority", index + 100)),
            "route_ref": row.get("route_ref"),
        })
    return inventory


__all__ = ["build_provider_inventory", "find_tvc_root", "load_pin", "load_tvc", "resolve_via_tvc", "stable_hash"]
