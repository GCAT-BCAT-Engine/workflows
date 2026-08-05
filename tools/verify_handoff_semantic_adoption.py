#!/usr/bin/env python3
"""Fail-closed verification for the reviewed semantic-adoption registry."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "stegverse.handoff.semantic_adoption_registry.v1"
RECEIPT = "stegverse.handoff.semantic_adoption_registry_verification.v1"
REQUIRED = {
    "StegVerse-002/capability-registry",
    "StegVerse-002/StegGuardian",
    "StegVerse-002/StegProfile",
    "StegVerse-002/core-lite",
    "StegVerse-002/admissibility-gateway",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def canonical_hash(payload: dict[str, Any], field: str) -> str:
    clean = dict(payload)
    clean.pop(field, None)
    return hashlib.sha256(
        json.dumps(clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("registry_object_required")
    return value


def verify(payload: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    if payload.get("schema") != SCHEMA:
        failures.append("registry_schema_invalid")
    if payload.get("repair_mode") != "READ_ONLY":
        failures.append("repair_mode_not_read_only")
    if payload.get("governed_repair_state") != "NOT_AUTHORIZED":
        failures.append("governed_repair_not_blocked")
    if payload.get("registry_hash") != canonical_hash(payload, "registry_hash"):
        failures.append("registry_hash_mismatch")

    for source in ("host", "portable_source"):
        value = payload.get(source)
        if not isinstance(value, dict) or value.get("decision") != "ALLOW":
            failures.append(f"{source}_not_allow")
        elif not HEX40.fullmatch(str(value.get("commit", ""))):
            failures.append(f"{source}_commit_invalid")

    repositories = payload.get("repositories")
    if not isinstance(repositories, list):
        failures.append("repositories_invalid")
        repositories = []
    seen: set[str] = set()
    for index, item in enumerate(repositories):
        if not isinstance(item, dict):
            failures.append(f"repository_{index}_invalid")
            continue
        repository = item.get("repository")
        if repository in seen:
            failures.append("duplicate_repository")
        if isinstance(repository, str):
            seen.add(repository)
        if item.get("state") != "COMPLETE_READ_ONLY":
            failures.append(f"{repository}_state_incomplete")
        if item.get("terminal_decision") != "ALLOW":
            failures.append(f"{repository}_decision_not_allow")
        if item.get("conformance_delta_count") != 0:
            failures.append(f"{repository}_conformance_delta")
        if item.get("state_delta_count") != 0:
            failures.append(f"{repository}_state_delta")
        if item.get("reconciliation_status") != "FIXED_POINT_REACHED":
            failures.append(f"{repository}_not_fixed_point")
        if item.get("repair_enabled") is not False:
            failures.append(f"{repository}_repair_enabled")
        for field in ("evidence_commit", "release_commit"):
            if not HEX40.fullmatch(str(item.get(field, ""))):
                failures.append(f"{repository}_{field}_invalid")
        for field in ("semantic_receipt", "conformance_receipt", "state_delta_receipt", "reconciliation_receipt"):
            if not HEX64.fullmatch(str(item.get(field, ""))):
                failures.append(f"{repository}_{field}_invalid")
        if not DIGEST.fullmatch(str(item.get("artifact_digest", ""))):
            failures.append(f"{repository}_artifact_digest_invalid")
        for field in ("semantic_run", "provenance_run", "artifact_id"):
            if not isinstance(item.get(field), int) or item.get(field) <= 0:
                failures.append(f"{repository}_{field}_invalid")

    if seen != REQUIRED:
        failures.append("reviewed_repository_set_mismatch")
    completion = payload.get("completion")
    if not isinstance(completion, dict):
        failures.append("completion_invalid")
    else:
        if completion.get("required_repositories") != len(REQUIRED):
            failures.append("completion_required_count_invalid")
        if completion.get("complete_read_only") != len(REQUIRED):
            failures.append("completion_complete_count_invalid")
        if completion.get("pending") != 0 or completion.get("failed") != 0:
            failures.append("completion_not_terminal")

    decision = "ALLOW" if not failures else "DENY"
    receipt = {
        "receipt_type": RECEIPT,
        "registry_hash": payload.get("registry_hash"),
        "required_repository_count": len(REQUIRED),
        "observed_repository_count": len(seen),
        "terminal_decision": decision,
        "repair_enabled": False,
        "authority_effect": "NONE",
        "failures": sorted(set(failures)),
    }
    receipt["receipt_hash"] = canonical_hash(receipt, "receipt_hash")
    return receipt


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("data/handoff-semantic-adoption.json"))
    parser.add_argument("--output", type=Path, default=Path("data/handoff-semantic-adoption.verification-receipt.json"))
    args = parser.parse_args(argv)
    try:
        payload = load(args.registry)
        receipt = verify(payload)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        receipt = {
            "receipt_type": RECEIPT,
            "terminal_decision": "FAIL_CLOSED",
            "repair_enabled": False,
            "authority_effect": "NONE",
            "failures": [f"{type(exc).__name__}:{exc}"],
        }
        receipt["receipt_hash"] = canonical_hash(receipt, "receipt_hash")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("HANDOFF_SEMANTIC_ADOPTION=" + receipt["terminal_decision"])
    return 0 if receipt["terminal_decision"] == "ALLOW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
