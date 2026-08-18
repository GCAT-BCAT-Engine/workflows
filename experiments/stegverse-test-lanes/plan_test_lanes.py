#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping


class TestLanesError(ValueError):
    pass


MANIFEST_SCHEMA = "stegverse.test-lanes-manifest.v1"
PRIMARY_PROVIDER = "stegverse_local"
PRIMARY_CAPABILITY = "local.model.inference"
EXTERNAL_ROLE = "CONTROL_OR_FALLBACK_ONLY"

_PROHIBITED_FIELD_NAMES = {
    "api_key",
    "apikey",
    "authorization",
    "bearer_token",
    "credential",
    "credential_ref",
    "credential_value",
    "password",
    "secret",
    "secret_value",
    "token",
}
_PROHIBITED_VALUE_MARKERS = (
    "vault://",
    "authorization: bearer ",
    "bearer sk-",
    "github_pat_",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "DEEPSEEK_API_KEY",
    "MOONSHOT_API_KEY",
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _reject_credential_material(value: Any, path: str = "manifest") -> None:
    if isinstance(value, Mapping):
        for raw_key, child in value.items():
            key = str(raw_key).strip().lower().replace("-", "_")
            if key in _PROHIBITED_FIELD_NAMES:
                raise TestLanesError(f"credential-bearing field prohibited: {path}.{raw_key}")
            _reject_credential_material(child, f"{path}.{raw_key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_credential_material(child, f"{path}[{index}]")
    elif isinstance(value, str):
        lowered = value.lower()
        for marker in _PROHIBITED_VALUE_MARKERS:
            if marker.lower() in lowered:
                raise TestLanesError(f"credential-bearing value prohibited at {path}")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise TestLanesError(message)


def validate_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    _reject_credential_material(manifest)
    _require(manifest.get("schema_version") == MANIFEST_SCHEMA, "manifest schema mismatch")
    _require(manifest.get("primary_provider") == PRIMARY_PROVIDER, "StegVerse local must be primary")

    credential_policy = manifest.get("credential_policy")
    _require(isinstance(credential_policy, Mapping), "credential_policy required")
    _require(credential_policy.get("authority") == "TV/TVC", "credential authority must be TV/TVC")
    _require(credential_policy.get("manifest_contains_credentials") is False, "manifest must not contain credentials")
    _require(credential_policy.get("credential_export_allowed") is False, "credential export must be false")

    task = manifest.get("task")
    _require(isinstance(task, Mapping), "task required")
    _require(isinstance(task.get("task_id"), str) and task.get("task_id"), "task_id required")
    source_blob_sha = task.get("source_blob_sha")
    _require(isinstance(source_blob_sha, str) and len(source_blob_sha) == 40, "40-character task source blob SHA required")
    _require(all(ch in "0123456789abcdef" for ch in source_blob_sha), "task source blob SHA must be lowercase hex")

    lanes = manifest.get("lanes")
    _require(isinstance(lanes, list) and lanes, "at least one lane required")
    seen: set[str] = set()
    primary_lanes = 0
    normalized: list[dict[str, Any]] = []

    for index, raw in enumerate(lanes):
        _require(isinstance(raw, Mapping), f"lane {index} must be object")
        lane = dict(raw)
        lane_id = lane.get("lane_id")
        provider = lane.get("provider")
        role = lane.get("provider_role")
        capsule_id = lane.get("capsule_id")
        capability = lane.get("capability")
        mode = lane.get("mode")
        required = lane.get("required", False)
        governance_profile = lane.get("governance_profile")

        _require(isinstance(lane_id, str) and lane_id, f"lane {index}: lane_id required")
        _require(lane_id not in seen, f"duplicate lane_id: {lane_id}")
        seen.add(lane_id)
        _require(isinstance(provider, str) and provider, f"{lane_id}: provider required")
        _require(isinstance(capsule_id, str) and len(capsule_id) >= 3, f"{lane_id}: capsule_id required")
        _require(isinstance(capability, str) and capability, f"{lane_id}: capability required")
        _require(mode in {"REFERENCE", "RAW", "GOVERNED"}, f"{lane_id}: invalid mode")
        _require(isinstance(required, bool), f"{lane_id}: required must be boolean")

        if provider == PRIMARY_PROVIDER:
            primary_lanes += 1
            _require(role == "PRIMARY", f"{lane_id}: StegVerse local lane must be PRIMARY")
            _require(capability == PRIMARY_CAPABILITY, f"{lane_id}: StegVerse local capability mismatch")
            _require(required is True, f"{lane_id}: StegVerse primary/reference lane must be required")
            _require(mode in {"REFERENCE", "GOVERNED"}, f"{lane_id}: StegVerse primary cannot be RAW")
        else:
            _require(role == EXTERNAL_ROLE, f"{lane_id}: third-party lane must be control/fallback only")
            _require(mode in {"RAW", "GOVERNED"}, f"{lane_id}: external lane mode must be RAW or GOVERNED")

        if mode == "GOVERNED":
            _require(isinstance(governance_profile, str) and governance_profile, f"{lane_id}: governed lane requires governance_profile")
        if mode == "RAW":
            _require(governance_profile is None, f"{lane_id}: raw lane cannot claim governance_profile")

        normalized.append(deepcopy(lane))

    _require(primary_lanes == 1, "exactly one StegVerse-local primary/reference lane required")
    return {
        "schema": "stegverse.test-lanes-validation.v1",
        "state": "VALID",
        "test_id": manifest.get("test_id"),
        "manifest_hash": sha256_json(manifest),
        "lane_count": len(normalized),
        "primary_lane_count": primary_lanes,
        "credential_authority": "TV/TVC",
        "manifest_contains_credentials": False,
        "lanes": normalized,
    }


def _resolution_index(capsule_resolutions: Mapping[str, Any] | None) -> dict[str, Mapping[str, Any]]:
    if capsule_resolutions is None:
        return {}
    items = capsule_resolutions.get("resolutions")
    _require(isinstance(items, list), "capsule_resolutions.resolutions must be a list")
    result: dict[str, Mapping[str, Any]] = {}
    for raw in items:
        _require(isinstance(raw, Mapping), "capsule resolution must be object")
        capsule_id = raw.get("capsule_id")
        _require(isinstance(capsule_id, str) and capsule_id, "capsule resolution missing capsule_id")
        _require(capsule_id not in result, f"duplicate capsule resolution: {capsule_id}")
        _require(raw.get("credential_material_returned") is False, f"capsule resolution leaked credential material: {capsule_id}")
        result[capsule_id] = raw
    return result


def plan_manifest(
    manifest: Mapping[str, Any],
    *,
    capsule_resolutions: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    validated = validate_manifest(manifest)
    resolutions = _resolution_index(capsule_resolutions)
    planned: list[dict[str, Any]] = []
    blockers: list[str] = []

    task = manifest["task"]
    for lane in validated["lanes"]:
        provider = lane["provider"]
        required = lane.get("required", False)
        if provider == PRIMARY_PROVIDER:
            state = "READY_LOCAL_PRIMARY"
            resolution_state = "NOT_REQUIRED"
        else:
            resolution = resolutions.get(lane["capsule_id"])
            if resolution is None:
                state = "READY_FOR_TVC_CAPSULE_RESOLUTION"
                resolution_state = "NOT_SUPPLIED"
            else:
                _require(resolution.get("provider") == provider, f"{lane['lane_id']}: capsule/provider mismatch")
                _require(resolution.get("capability") == lane["capability"], f"{lane['lane_id']}: capsule/capability mismatch")
                resolution_state = str(resolution.get("state"))
                if resolution_state == "READY":
                    state = "READY_FOR_TVC_EXECUTION"
                elif resolution_state == "CREDENTIAL_BINDING_UNAVAILABLE" and not required:
                    state = "SKIPPED_OPTIONAL_CREDENTIAL_UNBOUND"
                elif resolution_state == "CREDENTIAL_BINDING_UNAVAILABLE":
                    state = "BLOCKED_REQUIRED_CREDENTIAL_UNBOUND"
                    blockers.append(f"REQUIRED_CREDENTIAL_BINDING_UNAVAILABLE:{lane['lane_id']}")
                else:
                    state = "BLOCKED_CAPSULE_RESOLUTION"
                    blockers.append(f"CAPSULE_RESOLUTION_INVALID:{lane['lane_id']}:{resolution_state}")

        request = {
            "schema": "stegverse.test-lane-execution-request.v1",
            "test_id": manifest["test_id"],
            "lane_id": lane["lane_id"],
            "state": state,
            "provider": provider,
            "provider_role": lane["provider_role"],
            "capsule_id": lane["capsule_id"],
            "capsule_resolution_state": resolution_state,
            "capability": lane["capability"],
            "mode": lane["mode"],
            "model": lane.get("model"),
            "parameters": deepcopy(lane.get("parameters") or {}),
            "governance_profile": lane.get("governance_profile"),
            "task_id": task["task_id"],
            "task_source": task["source"],
            "task_source_blob_sha": task["source_blob_sha"],
            "prompt_profile": task["prompt_profile"],
            "expected_output_hash": task.get("expected_output_hash"),
            "credential_authority": "TV/TVC",
            "credential_material_in_request": False,
            "credential_export_allowed": False,
            "execution_authority_granted_by_plan": False,
        }
        request["request_hash"] = sha256_json(request)
        planned.append(request)

    if blockers:
        overall = "BLOCKED"
    elif any(item["state"] == "READY_FOR_TVC_CAPSULE_RESOLUTION" for item in planned):
        overall = "CAPSULE_RESOLUTION_REQUIRED"
    else:
        overall = "READY"

    result = {
        "schema": "stegverse.test-lanes-plan.v1",
        "state": overall,
        "test_id": manifest["test_id"],
        "manifest_hash": validated["manifest_hash"],
        "primary_provider": PRIMARY_PROVIDER,
        "credential_authority": "TV/TVC",
        "credential_material_present": False,
        "lane_count": len(planned),
        "blockers": blockers,
        "lanes": planned,
    }
    result["plan_hash"] = sha256_json(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and plan a portable StegVerse Test Lanes manifest without provider credentials.")
    parser.add_argument("manifest")
    parser.add_argument("--capsule-resolutions")
    parser.add_argument("--output")
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    resolutions = None
    if args.capsule_resolutions:
        resolutions = json.loads(Path(args.capsule_resolutions).read_text(encoding="utf-8"))
    result = plan_manifest(manifest, capsule_resolutions=resolutions)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["state"] in {"READY", "CAPSULE_RESOLUTION_REQUIRED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
