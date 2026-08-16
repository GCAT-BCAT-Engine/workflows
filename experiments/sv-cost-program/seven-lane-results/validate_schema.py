#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
TASK = json.loads((ROOT / "task.json").read_text())

EXPECTED = [
    (1, "openai-raw", "OpenAI", False, "EXTERNAL"),
    (2, "openai-governed", "OpenAI/StegVerse", True, "EXTERNAL"),
    (3, "anthropic-raw", "Anthropic", False, "EXTERNAL"),
    (4, "anthropic-governed", "Anthropic/StegVerse", True, "EXTERNAL"),
    (5, "stegverse-only", "StegVerse deterministic reconstruction", True, "NONE"),
    (6, "deepseek-raw", "DeepSeek", False, "EXTERNAL"),
    (7, "deepseek-governed", "DeepSeek/StegVerse", True, "EXTERNAL"),
]

failures: list[str] = []
lanes = TASK.get("lane_schema", [])
if TASK.get("schema_version") != "3.0.0":
    failures.append("EXPECTED_SCHEMA_3_0_0")
if TASK.get("generation") != "GENERATION_2_CREDENTIALLESS_OUTPUT_BOUNDARY":
    failures.append("GENERATION_DRIFT")
if TASK.get("credential_invariant") != "NO_PROVIDER_API_KEY_POSSESSED_OR_CONSUMED_BY_STEGVERSE_TEST_WORKLOAD":
    failures.append("CREDENTIAL_INVARIANT_DRIFT")
if len(lanes) != 7:
    failures.append(f"EXPECTED_7_LANES_GOT_{len(lanes)}")

for index, expected in enumerate(EXPECTED):
    if index >= len(lanes):
        failures.append(f"MISSING_LANE_{expected[0]}")
        continue
    lane = lanes[index]
    actual = (
        lane.get("lane"),
        lane.get("lane_id"),
        lane.get("model_interest"),
        lane.get("stegverse_governed"),
        lane.get("credential_mode"),
    )
    if actual != expected:
        failures.append(f"LANE_{expected[0]}_MISMATCH:{actual!r}")

if TASK.get("task_id") != "SV-RECON-001":
    failures.append("TASK_ID_DRIFT")
if TASK.get("operation_class") != "governed_state_reconstruction":
    failures.append("OPERATION_CLASS_DRIFT")
if TASK.get("comparison_unit") != "successful equivalent admissible outcome":
    failures.append("COMPARISON_UNIT_DRIFT")

candidate = TASK.get("candidate_source_contract", {})
if candidate.get("provider_api_key_transferred_to_stegverse") is not False:
    failures.append("CANDIDATE_CONTRACT_MUST_FORBID_KEY_TRANSFER")
if candidate.get("same_candidate_used_for_raw_and_governed_pair") is not True:
    failures.append("RAW_GOVERNED_MUST_SHARE_CANDIDATE")

prod = TASK.get("production_artifact_reference", {})
if prod.get("stegcore_repository") != "StegVerse-Labs/StegCore":
    failures.append("PRODUCTION_STEGCORE_REFERENCE_MISSING")
if prod.get("sdk_repository") != "StegVerse-org/StegVerse-SDK":
    failures.append("PRODUCTION_SDK_REFERENCE_MISSING")
if prod.get("provider_account_required_by_portable_unit") is not False:
    failures.append("PORTABLE_UNIT_PROVIDER_ACCOUNT_BOUNDARY_DRIFT")
if prod.get("non_tv_tvc_secret_required") is not False:
    failures.append("PORTABLE_UNIT_SECRET_BOUNDARY_DRIFT")

required = TASK.get("required_output", {})
if required.get("final_state") != {"balance": 75, "risk_score": 3, "standing": "active"}:
    failures.append("REQUIRED_FINAL_STATE_DRIFT")
if required.get("applied_count") != 4 or required.get("denied_count") != 2:
    failures.append("REQUIRED_DECISION_COUNT_DRIFT")

proof = TASK.get("proof_requirements", {})
for key in (
    "governance_receipt",
    "replay_receipt",
    "reconstruction_receipt",
    "candidate_hash_bound",
    "provider_credential_nonpossession_asserted",
    "raw_and_governed_candidate_hash_must_match",
):
    if proof.get(key) is not True:
        failures.append("PROOF_REQUIREMENT_MISSING:" + key)

canonical_runner = (ROOT / "run.py").read_text()
candidate_runner = (ROOT / "run_candidate_outputs.py").read_text()
combined = canonical_runner + "\n" + candidate_runner
for forbidden in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY", "api.openai.com/v1/responses", "api.anthropic.com/v1/messages", "api.deepseek.com"):
    if forbidden in combined:
        failures.append("DIRECT_PROVIDER_CREDENTIAL_OR_CALL_MARKER_FORBIDDEN:" + forbidden)
for required_marker in (
    "provider_api_key_transferred_to_stegverse",
    "governance-receipt.v1",
    "replay-receipt.v1",
    "reconstruction-receipt.v1",
    "GENERATION_2_CREDENTIALLESS_OUTPUT_BOUNDARY",
):
    if required_marker not in combined:
        failures.append("RUNNER_MARKER_MISSING:" + required_marker)

if failures:
    print(json.dumps({"status": "FAIL", "failures": failures}, indent=2))
    sys.exit(2)

print(json.dumps({
    "status": "PASS",
    "experiment_id": TASK["experiment_id"],
    "generation": TASK["generation"],
    "lane_count": 7,
    "credential_invariant": TASK["credential_invariant"],
    "production_repositories": [prod["stegcore_repository"], prod["sdk_repository"]],
    "historical_five_lane_result_preserved": TASK["preserves_historical_result"],
}, indent=2))
