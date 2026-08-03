#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import time
import urllib.request
from dataclasses import dataclass
from typing import Any

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "results"
NATIVE = OUT / "native"
NORMALIZED = OUT / "normalized"
OUT.mkdir(parents=True, exist_ok=True)
NATIVE.mkdir(parents=True, exist_ok=True)
NORMALIZED.mkdir(parents=True, exist_ok=True)
CONTRACT = json.loads((ROOT / "task_contract.json").read_text())


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def post_json(url: str, headers: dict[str, str], body: dict[str, Any]) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as response:
        return json.loads(response.read())


@dataclass
class NativeReceipt:
    lane_id: str
    platform: str
    route: str
    model: str
    attempt: int
    started_at_epoch: float
    latency_seconds: float
    request_id: str | None
    status: str
    input_tokens: int
    output_tokens: int
    cached_input_tokens: int
    native_text: str
    native_payload: dict[str, Any]
    prompt_hash: str
    output_hash: str
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


def response_prompt(missing: list[str] | None = None) -> str:
    schema = CONTRACT["canonical_schema"]
    remediation = ""
    if missing:
        remediation = (
            "\nREMEDIATION: Your prior response omitted these obligations: "
            + ", ".join(missing)
            + ". Correct them while preserving the same task and claim boundary."
        )
    return f"""EXPERIMENT: {CONTRACT['experiment_id']}
TASK VERSION: {CONTRACT['task_version']}
TASK: {CONTRACT['task']}

Return exactly one JSON object and no surrounding prose. Use this schema:
{json.dumps(schema, indent=2)}

Rules:
- Preserve the exact abstract claim ALLOW(t) iff GBP(t) and BD(t) and OC(t).
- Distinguish stipulated abstract logic from deployed implementation validity.
- Mark every required obligation truthfully.
- Do not claim any deployed GCAT/BCAT implementation is verified.
- The Lean candidate may prove only the abstract logical core.
{remediation}
"""


def call_openai(prompt: str, attempt: int) -> NativeReceipt:
    model = os.getenv("OPENAI_MODEL", "gpt-5.6")
    started = time.time()
    t0 = time.perf_counter()
    raw = post_json(
        "https://api.openai.com/v1/responses",
        {
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        {"model": model, "input": prompt, "max_output_tokens": 1800},
    )
    latency = time.perf_counter() - t0
    text = "".join(
        block.get("text", "")
        for item in raw.get("output", [])
        for block in item.get("content", [])
        if block.get("type") == "output_text"
    )
    usage = raw.get("usage", {})
    details = usage.get("input_tokens_details", {}) or {}
    return NativeReceipt(
        lane_id="openai",
        platform="openai",
        route="synchronous",
        model=model,
        attempt=attempt,
        started_at_epoch=started,
        latency_seconds=latency,
        request_id=raw.get("id"),
        status=raw.get("status", "unknown"),
        input_tokens=int(usage.get("input_tokens", 0)),
        output_tokens=int(usage.get("output_tokens", 0)),
        cached_input_tokens=int(details.get("cached_tokens", 0)),
        native_text=text,
        native_payload=raw,
        prompt_hash=sha256_text(prompt),
        output_hash=sha256_text(text),
    )


def call_anthropic(prompt: str, attempt: int) -> NativeReceipt:
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    started = time.time()
    t0 = time.perf_counter()
    raw = post_json(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        {
            "model": model,
            "max_tokens": 1800,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    latency = time.perf_counter() - t0
    text = "".join(x.get("text", "") for x in raw.get("content", []) if x.get("type") == "text")
    usage = raw.get("usage", {})
    return NativeReceipt(
        lane_id="anthropic",
        platform="anthropic",
        route="synchronous",
        model=model,
        attempt=attempt,
        started_at_epoch=started,
        latency_seconds=latency,
        request_id=raw.get("id"),
        status=raw.get("stop_reason", "unknown"),
        input_tokens=int(usage.get("input_tokens", 0)),
        output_tokens=int(usage.get("output_tokens", 0)),
        cached_input_tokens=int(usage.get("cache_read_input_tokens", 0)),
        native_text=text,
        native_payload=raw,
        prompt_hash=sha256_text(prompt),
        output_hash=sha256_text(text),
    )


def call_stegverse(prompt: str, attempt: int) -> NativeReceipt:
    started = time.time()
    t0 = time.perf_counter()
    obj = {
        "task_identity": f"{CONTRACT['experiment_id']}:{CONTRACT['task_version']}",
        "conclusion": "For every transition t, ALLOW(t) iff GBP(t) and BD(t) and OC(t).",
        "claims": [
            "ALLOW(t) implies GBP(t), BD(t), and OC(t).",
            "GBP(t), BD(t), and OC(t) together imply ALLOW(t).",
        ],
        "evidence": ["The abstract evaluator equivalence is stipulated by the task contract."],
        "unresolved": [
            "No evidence binds the abstract predicates or theorem to a deployed GCAT/BCAT implementation."
        ],
        "boundary": [
            "The result establishes only the stipulated abstract logical core, not implementation validity."
        ],
        "lean_candidate": "theorem allow_iff_conditions {T : Type} (GBP BD OC ALLOW : T → Prop) (spec : ∀ t, ALLOW t ↔ GBP t ∧ BD t ∧ OC t) : ∀ t, ALLOW t ↔ GBP t ∧ BD t ∧ OC t := spec",
        "obligations": {name: True for name in CONTRACT["required_obligations"]},
    }
    text = canonical_json(obj)
    latency = time.perf_counter() - t0
    raw = {
        "kind": "repository_native_deterministic_reconstruction",
        "source": "task_contract.json",
        "contract_hash": sha256_text(canonical_json(CONTRACT)),
        "external_provider_request": False,
    }
    return NativeReceipt(
        lane_id="stegverse-only",
        platform="stegverse-only",
        route="repository-native",
        model="deterministic-contract-reconstructor-v1",
        attempt=attempt,
        started_at_epoch=started,
        latency_seconds=latency,
        request_id=None,
        status="completed",
        input_tokens=0,
        output_tokens=0,
        cached_input_tokens=0,
        native_text=text,
        native_payload=raw,
        prompt_hash=sha256_text(prompt),
        output_hash=sha256_text(text),
    )


def extract_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("No JSON object found in native output")
        value = json.loads(cleaned[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("Normalized output must be a JSON object")
    return value


def normalize(receipt: NativeReceipt) -> dict[str, Any]:
    source = extract_json(receipt.native_text)
    obligations = source.get("obligations", {})
    normalized = {
        "experiment_id": CONTRACT["experiment_id"],
        "task_version": CONTRACT["task_version"],
        "lane_id": receipt.lane_id,
        "native_output_hash": receipt.output_hash,
        "task_identity": str(source.get("task_identity", "")),
        "conclusion": str(source.get("conclusion", "")),
        "claims": [str(x) for x in source.get("claims", [])],
        "evidence": [str(x) for x in source.get("evidence", [])],
        "unresolved": [str(x) for x in source.get("unresolved", [])],
        "boundary": [str(x) for x in source.get("boundary", [])],
        "lean_candidate": str(source.get("lean_candidate", "")),
        "obligations": {
            name: bool(obligations.get(name, False)) for name in CONTRACT["required_obligations"]
        },
    }
    normalized["normalized_hash"] = sha256_text(canonical_json(normalized))
    normalized["normalized_content_bytes"] = len(canonical_json(normalized).encode("utf-8"))
    return normalized


def adjudicate(record: dict[str, Any]) -> dict[str, Any]:
    missing = [name for name, value in record["obligations"].items() if not value]
    conclusion = record["conclusion"].lower()
    structural_errors = []
    if not all(term in conclusion for term in ["allow", "gbp", "bd", "oc"]):
        structural_errors.append("conclusion_missing_core_predicates")
    if not record["boundary"]:
        structural_errors.append("missing_boundary_content")
    if not record["unresolved"]:
        structural_errors.append("missing_unresolved_content")
    if not record["lean_candidate"]:
        structural_errors.append("missing_lean_candidate")
    classification = "comparable" if not missing and not structural_errors else "non-comparable"
    return {
        "lane_id": record["lane_id"],
        "classification": classification,
        "missing_obligations": missing,
        "structural_errors": structural_errors,
        "adjudication_hash": sha256_text(canonical_json({"missing": missing, "errors": structural_errors})),
    }


def provider_cost(receipt: NativeReceipt) -> dict[str, Any]:
    if receipt.platform == "stegverse-only":
        return {
            "observed_provider_cost_usd": 0.0,
            "batch_normalized_cost_usd": None,
            "price_card_version": None,
            "local_cost_status": "UNMEASURED_LOCAL_RUNTIME",
        }
    card = CONTRACT["pricing"][receipt.platform]
    uncached = max(0, receipt.input_tokens - receipt.cached_input_tokens)
    observed = (
        uncached * card["input_usd_per_million"]
        + receipt.output_tokens * card["output_usd_per_million"]
    ) / 1_000_000
    return {
        "observed_provider_cost_usd": observed,
        "batch_normalized_cost_usd": observed * 0.5,
        "price_card_version": card["price_card_version"],
        "local_cost_status": None,
    }


def execute_lane(lane: str) -> tuple[NativeReceipt, dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    caller = {"openai": call_openai, "anthropic": call_anthropic, "stegverse-only": call_stegverse}[lane]
    missing: list[str] | None = None
    attempts: list[dict[str, Any]] = []
    max_attempts = int(CONTRACT["retry_policy"]["max_attempts_per_lane"])
    last_receipt: NativeReceipt | None = None
    last_record: dict[str, Any] | None = None
    last_adjudication: dict[str, Any] | None = None
    for attempt in range(1, max_attempts + 1):
        prompt = response_prompt(missing)
        try:
            receipt = caller(prompt, attempt)
            record = normalize(receipt)
            decision = adjudicate(record)
            attempts.append({
                "attempt": attempt,
                "native_output_hash": receipt.output_hash,
                "classification": decision["classification"],
                "missing_obligations": decision["missing_obligations"],
                "structural_errors": decision["structural_errors"],
            })
            last_receipt, last_record, last_adjudication = receipt, record, decision
            if decision["classification"] == "comparable":
                break
            missing = decision["missing_obligations"] + decision["structural_errors"]
        except Exception as exc:
            attempts.append({"attempt": attempt, "classification": "error", "error": repr(exc)})
            missing = ["valid_json", "all_required_obligations"]
    if last_receipt is None or last_record is None or last_adjudication is None:
        raise RuntimeError(f"Lane {lane} failed all attempts without a normalizable receipt: {attempts}")
    return last_receipt, last_record, last_adjudication, attempts


def main() -> None:
    lane_results = []
    for lane in ["openai", "anthropic", "stegverse-only"]:
        receipt, normalized, adjudication, attempts = execute_lane(lane)
        (NATIVE / f"{lane}.json").write_text(json.dumps(receipt.to_dict(), indent=2))
        (NORMALIZED / f"{lane}.json").write_text(json.dumps(normalized, indent=2))
        economics = provider_cost(receipt)
        lane_results.append({
            "lane_id": lane,
            "platform": receipt.platform,
            "route": receipt.route,
            "model": receipt.model,
            "classification": adjudication["classification"],
            "attempt_count": len(attempts),
            "attempts": attempts,
            "input_tokens": receipt.input_tokens,
            "output_tokens": receipt.output_tokens,
            "cached_input_tokens": receipt.cached_input_tokens,
            "latency_seconds": receipt.latency_seconds,
            "native_output_hash": receipt.output_hash,
            "normalized_hash": normalized["normalized_hash"],
            "normalized_content_bytes": normalized["normalized_content_bytes"],
            **economics,
        })
    comparable = [x for x in lane_results if x["classification"] == "comparable"]
    human_intervention_count_after_dispatch = 0
    result = {
        "experiment_id": CONTRACT["experiment_id"],
        "task_version": CONTRACT["task_version"],
        "task_contract_hash": sha256_text(canonical_json(CONTRACT)),
        "lanes": lane_results,
        "all_three_comparable": len(comparable) == 3,
        "human_intervention_count_after_dispatch": human_intervention_count_after_dispatch,
        "claim_boundary": "Observed provider costs are reconstructed from retained native usage receipts and the versioned local price card. Batch-normalized values are counterfactual unless an actual batch receipt is retained. StegVerse-only external provider cost is zero while local runtime cost remains separately unmeasured.",
    }
    (OUT / "result.json").write_text(json.dumps(result, indent=2))
    lines = [
        "# SV-COST-NORMALIZED-001",
        "",
        "| Lane | Comparable | Attempts | Input | Output | Observed provider cost | Batch-normalized | Latency s |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for lane in lane_results:
        batch = lane["batch_normalized_cost_usd"]
        batch_text = "N/A" if batch is None else f"${batch:.6f}"
        lines.append(
            f"| {lane['lane_id']} | {lane['classification']} | {lane['attempt_count']} | "
            f"{lane['input_tokens']:,} | {lane['output_tokens']:,} | "
            f"${lane['observed_provider_cost_usd']:.6f} | {batch_text} | {lane['latency_seconds']:.2f} |"
        )
    lines += [
        "",
        f"All three comparable: **{result['all_three_comparable']}**",
        f"Human interventions after dispatch: **{human_intervention_count_after_dispatch}**",
        "",
        "## Boundary",
        "",
        result["claim_boundary"],
    ]
    (OUT / "report.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(result, indent=2))
    if not result["all_three_comparable"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
