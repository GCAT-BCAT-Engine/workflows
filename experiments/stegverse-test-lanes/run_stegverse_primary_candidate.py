#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class PrimaryCandidateError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_json(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PrimaryCandidateError(message)


def load_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, Mapping), f"JSON object required: {path}")
    return value


def verify_loopback_endpoint(endpoint: str) -> str:
    parsed = urlparse(endpoint)
    require(parsed.scheme in {"http", "https"}, "primary endpoint must be http(s)")
    require(parsed.hostname in {"127.0.0.1", "localhost", "::1"}, "StegVerse primary endpoint must be loopback-local")
    require(parsed.username is None and parsed.password is None, "endpoint credentials prohibited")
    return endpoint.rstrip("/")


def verify_plan(plan: Mapping[str, Any]) -> None:
    require(plan.get("schema") == "stegverse.test-lanes-plan.v1", "plan schema mismatch")
    require(plan.get("state") == "READY", "primary execution requires resolved READY plan")
    require(plan.get("primary_provider") == "stegverse_local", "StegVerse local must remain primary")
    require(plan.get("credential_authority") == "TV/TVC", "credential authority must be TV/TVC")
    require(plan.get("credential_material_present") is False, "credential-bearing plan prohibited")
    recorded = plan.get("plan_hash")
    unsigned = dict(plan)
    unsigned.pop("plan_hash", None)
    require(recorded == sha256_json(unsigned), "plan hash mismatch")


def primary_group(plan: Mapping[str, Any]) -> Mapping[str, Any]:
    groups = plan.get("execution_groups")
    require(isinstance(groups, list), "execution_groups required")
    matches = [
        item for item in groups
        if isinstance(item, Mapping)
        and item.get("provider") == "stegverse_local"
        and item.get("provider_role") == "PRIMARY"
    ]
    require(len(matches) == 1, "exactly one StegVerse primary execution group required")
    group = matches[0]
    require(group.get("state") == "READY_LOCAL_PRIMARY", "StegVerse primary group is not ready")
    require(group.get("capability") == "local.model.inference", "StegVerse primary capability mismatch")
    require(group.get("credential_material_present") is False, "primary group contains credential material")
    require(group.get("execution_authority_granted_by_group") is False, "plan/group cannot grant execution authority")
    recorded = group.get("group_hash")
    unsigned = dict(group)
    unsigned.pop("group_hash", None)
    require(recorded == sha256_json(unsigned), "primary group hash mismatch")
    return group


def build_prompt(task: Mapping[str, Any], prompt_profile: str) -> str:
    require(prompt_profile == "stegverse.sv-recon-001.prompt.v1", "primary runner prompt profile not admitted")
    require(task.get("task_id") == "SV-RECON-001", "primary runner requires SV-RECON-001")
    payload = json.dumps(dict(task), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return (
        "Execute the following deterministic governed state-reconstruction task exactly. "
        "Process events in listed order and apply only the stated decision rules. "
        "Return only the required JSON object with no markdown, commentary, or additional keys.\n\n"
        + payload
    )


def http_json(url: str, *, payload: Mapping[str, Any] | None = None, timeout: int = 30) -> Mapping[str, Any]:
    request = Request(
        url,
        data=canonical_bytes(payload) if payload is not None else None,
        headers={"content-type": "application/json", "accept": "application/json"},
        method="POST" if payload is not None else "GET",
    )
    with urlopen(request, timeout=timeout) as response:
        value = json.loads(response.read().decode("utf-8"))
    require(isinstance(value, Mapping), "StegVerse primary returned non-object JSON")
    return value


def run_primary_candidate(
    *,
    plan: Mapping[str, Any],
    task_bytes: bytes,
    endpoint: str,
    timeout: int = 30,
) -> dict[str, Any]:
    verify_plan(plan)
    group = primary_group(plan)
    endpoint = verify_loopback_endpoint(endpoint)
    require(git_blob_sha(task_bytes) == group.get("task_source_blob_sha"), "task source blob mismatch")
    task = json.loads(task_bytes.decode("utf-8"))
    require(isinstance(task, Mapping), "task source must be object")
    require(task.get("task_id") == group.get("task_id"), "task ID mismatch")

    health = http_json(endpoint + "/health", timeout=min(timeout, 5))
    require(health.get("state") == "READY", "StegVerse primary health is not READY")
    require(health.get("private_endpoint_only") is True, "primary endpoint is not private-only")
    require(health.get("third_party_inference_required") is False, "primary endpoint requires third-party inference")
    require(health.get("authority_effect") == "NONE", "model health attempted authority effect")
    expected_model = group.get("model")
    require(isinstance(expected_model, str) and expected_model, "primary model identity required")
    require(health.get("model") == expected_model, "primary model identity mismatch")

    prompt_profile = str(group.get("prompt_profile") or "")
    prompt = build_prompt(task, prompt_profile)
    started_ns = time.monotonic_ns()
    response = http_json(
        endpoint + "/v1/chat/completions",
        payload={
            "model": expected_model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 256,
            "seed": 0,
        },
        timeout=timeout,
    )
    latency_ms = (time.monotonic_ns() - started_ns) / 1_000_000
    require(response.get("model") == expected_model, "primary response model mismatch")
    choices = response.get("choices")
    require(isinstance(choices, list) and len(choices) == 1, "primary response must contain one choice")
    message = choices[0].get("message") if isinstance(choices[0], Mapping) else None
    require(isinstance(message, Mapping) and isinstance(message.get("content"), str), "primary response content missing")
    usage = response.get("usage")
    require(isinstance(usage, Mapping), "primary usage missing")
    stegverse = response.get("stegverse")
    require(isinstance(stegverse, Mapping), "StegVerse proof metadata missing")
    require(stegverse.get("third_party_inference_required") is False, "response drifted to third-party inference")
    require(stegverse.get("authority_effect") == "NONE", "model response attempted authority effect")

    candidate = str(message["content"])
    return {
        "schema": "stegverse.test-lanes-primary-candidate.v1",
        "state": "PRIMARY_CANDIDATE_COMPLETE",
        "test_id": plan.get("test_id"),
        "plan_hash": plan.get("plan_hash"),
        "manifest_hash": plan.get("manifest_hash"),
        "execution_group_id": group.get("execution_group_id"),
        "group_hash": group.get("group_hash"),
        "lane_ids": list(group.get("lane_ids") or []),
        "provider": "stegverse_local",
        "provider_role": "PRIMARY",
        "model": expected_model,
        "model_hash": stegverse.get("model_hash"),
        "task_id": group.get("task_id"),
        "task_source_blob_sha": group.get("task_source_blob_sha"),
        "prompt_profile": prompt_profile,
        "prompt_sha256": sha256_text(prompt),
        "candidate_output": candidate,
        "candidate_output_sha256": sha256_text(candidate),
        "latency_ms": latency_ms,
        "provider_usage": dict(usage),
        "credential_requirement": "NONE",
        "credential_material_present": False,
        "third_party_inference_required": False,
        "execution_authority_granted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the StegVerse PRIMARY Test Lanes candidate against an already-live sovereign loopback endpoint.")
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--task-json", required=True, type=Path)
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    try:
        result = run_primary_candidate(
            plan=load_json(args.plan),
            task_bytes=args.task_json.read_bytes(),
            endpoint=args.endpoint,
            timeout=args.timeout,
        )
    except Exception as exc:
        print(json.dumps({"state": "FAIL_CLOSED", "reason": str(exc), "credential_material_present": False}, sort_keys=True))
        return 2
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "state": result["state"],
        "provider": result["provider"],
        "model": result["model"],
        "credential_requirement": "NONE",
        "third_party_inference_required": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
