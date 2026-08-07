#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
TASK = json.loads((ROOT / "task.json").read_text())

EXPECTED = [
    (1, "openai-raw", "OpenAI", False),
    (2, "openai-governed", "OpenAI/StegVerse", True),
    (3, "anthropic-raw", "Anthropic", False),
    (4, "anthropic-governed", "Anthropic/StegVerse", True),
    (5, "stegverse-only", "StegVerse deterministic reconstruction", True),
    (6, "deepseek-raw", "DeepSeek", False),
    (7, "deepseek-governed", "DeepSeek/StegVerse", True),
]

failures: list[str] = []
lanes = TASK.get("lane_schema", [])
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
    )
    if actual != expected:
        failures.append(f"LANE_{expected[0]}_MISMATCH:{actual!r}")

if TASK.get("task_id") != "SV-RECON-001":
    failures.append("TASK_ID_DRIFT")
if TASK.get("operation_class") != "governed_state_reconstruction":
    failures.append("OPERATION_CLASS_DRIFT")
if TASK.get("comparison_unit") != "successful equivalent admissible outcome":
    failures.append("COMPARISON_UNIT_DRIFT")

required = TASK.get("required_output", {})
if required.get("final_state") != {"balance": 75, "risk_score": 3, "standing": "active"}:
    failures.append("REQUIRED_FINAL_STATE_DRIFT")
if required.get("applied_count") != 4 or required.get("denied_count") != 2:
    failures.append("REQUIRED_DECISION_COUNT_DRIFT")

price_card = TASK.get("price_card", {})
if "deepseek_input_usd_per_million" not in price_card or "deepseek_output_usd_per_million" not in price_card:
    failures.append("DEEPSEEK_RATE_FIELDS_MISSING")

runner = (ROOT / "run.py").read_text()
for marker in [
    '"deepseek-raw"',
    '"deepseek-governed"',
    'DEEPSEEK_API_KEY',
    'DEEPSEEK_SEVEN_LANE_MODEL',
    '/chat/completions',
    'all_seven_successful_equivalent_admissible',
]:
    if marker not in runner:
        failures.append("RUNNER_MARKER_MISSING:" + marker)

if failures:
    print(json.dumps({"status": "FAIL", "failures": failures}, indent=2))
    sys.exit(2)

print(json.dumps({
    "status": "PASS",
    "experiment_id": TASK["experiment_id"],
    "lane_count": 7,
    "lane_6": "DeepSeek",
    "lane_7": "DeepSeek/StegVerse",
    "historical_five_lane_result_preserved": TASK["preserves_historical_result"],
}, indent=2))
