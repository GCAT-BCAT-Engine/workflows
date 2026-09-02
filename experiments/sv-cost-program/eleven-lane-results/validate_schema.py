#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys

ROOT = pathlib.Path(__file__).parent
TASK = json.loads((ROOT / "task.json").read_text())
EXPECTED_IDS = [
    "openai-raw","openai-governed","anthropic-raw","anthropic-governed",
    "stegverse-only","deepseek-raw","deepseek-governed","kimi-raw",
    "kimi-governed","glm-5.3-flash-hosted","glm-5.3-flash-sovereign",
]
failures=[]
if TASK.get("schema_version") != "6.0.0":
    failures.append("SCHEMA_VERSION")
lanes=TASK.get("lane_schema",[])
if len(lanes) != 11:
    failures.append(f"EXPECTED_11_LANES_GOT_{len(lanes)}")
if [x.get("lane_id") for x in lanes] != EXPECTED_IDS:
    failures.append("LANE_ORDER_OR_ID_MISMATCH")
if TASK.get("candidate_source_contract",{}).get("provider_api_key_transferred_to_stegverse") is not False:
    failures.append("CREDENTIAL_TRANSFER_BOUNDARY")
if lanes and lanes[9].get("credential_mode") != "EXTERNAL_CANDIDATE_OR_TV_TVC_AUTHORIZED_PROVIDER_OPERATION":
    failures.append("GLM_HOSTED_CREDENTIAL_MODE")
if lanes and lanes[10].get("credential_mode") != "NO_VENDOR_API_CREDENTIAL":
    failures.append("GLM_SOVEREIGN_CREDENTIAL_MODE")

runner=(ROOT/"run.py").read_text()
for forbidden in (
    "OPENAI_API_KEY","ANTHROPIC_API_KEY","DEEPSEEK_API_KEY",
    "MOONSHOT_API_KEY","KIMI_API_KEY","ZAI_API_KEY",
    "api.openai.com","api.anthropic.com","api.deepseek.com",
):
    if forbidden in runner:
        failures.append("FORBIDDEN_PROVIDER_PATH:"+forbidden)

required=[
    "candidate-input.schema.json","sovereign-runtime-evidence.schema.json",
    "cost-evidence.schema.json","glm-integration-state.json",
    "requests/glm-hosted-candidate-request.json",
    "requests/glm-sovereign-execution-request.json",
]
for rel in required:
    if not (ROOT/rel).exists():
        failures.append("MISSING_FILE:"+rel)

if failures:
    print(json.dumps({"status":"FAIL","failures":failures},indent=2))
    sys.exit(2)
print(json.dumps({
    "status":"PASS",
    "experiment_id":TASK["experiment_id"],
    "lane_count":11,
    "new_lanes":EXPECTED_IDS[-2:],
    "historical_nine_lane_preserved":True,
    "provider_secret_required_by_harness":False
},indent=2))
