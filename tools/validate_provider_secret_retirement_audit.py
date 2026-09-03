#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"security/provider-secret-workflow-retirement-audit.v1.json"
SHA=re.compile(r"^[0-9a-f]{40}$")


def main()->int:
    doc=json.loads(AUDIT.read_text())
    failures=[]
    if doc.get("schema")!="stegverse.provider-secret-workflow-retirement-audit/v1":
        failures.append("schema")
    retired=doc.get("retired_workflows")
    if not isinstance(retired,list) or len(retired)!=17:
        failures.append("retired_workflow_count")
        retired=retired if isinstance(retired,list) else []
    seen=set()
    for entry in retired:
        path=entry.get("path")
        commit=entry.get("retirement_commit")
        if not isinstance(path,str) or path in seen:
            failures.append(f"duplicate_or_invalid_path:{path}")
            continue
        seen.add(path)
        workflow=ROOT/path
        if not workflow.is_file():
            failures.append(f"contained_workflow_missing:{path}")
        else:
            text=workflow.read_text(encoding="utf-8")
            if "workflow_dispatch" not in text:
                failures.append(f"contained_workflow_not_manual:{path}")
            if "exit 1" not in text:
                failures.append(f"contained_workflow_not_fail_closed:{path}")
            if "permissions:" not in text:
                failures.append(f"contained_workflow_permissions_missing:{path}")
            if "timeout-minutes: 5" not in text:
                failures.append(f"contained_workflow_timeout_unbounded:{path}")
        if not isinstance(commit,str) or not SHA.fullmatch(commit):
            failures.append(f"invalid_retirement_commit:{path}")
        if entry.get("current_state")!="CONTAINED_FAIL_CLOSED_PLACEHOLDER":
            failures.append(f"invalid_state:{path}")
        if entry.get("active_provider_execution_allowed") is not False:
            failures.append(f"provider_execution_not_disabled:{path}")
        if entry.get("provider_secret_consumption_allowed") is not False:
            failures.append(f"provider_secret_consumption_not_disabled:{path}")
        if entry.get("historical_evidence_preserved") is not True:
            failures.append(f"historical_evidence_not_preserved:{path}")
    for replacement in doc.get("canonical_replacements",[]):
        ref=replacement.get("ref")
        if not isinstance(ref,str) or not (ROOT/ref).exists():
            failures.append(f"replacement_missing:{ref}")
    criteria=doc.get("acceptance_criteria")
    if not isinstance(criteria,dict) or len(criteria)!=10 or any(v!="PASS" for v in criteria.values()):
        failures.append("acceptance_criteria")
    auth=doc.get("authority") or {}
    if auth.get("provider_capability_authority")!="StegVerse-Labs/TVC":
        failures.append("provider_authority")
    if auth.get("consumer_policy_authority") is not False:
        failures.append("consumer_policy_authority")
    if auth.get("github_token_production_authority") is not False:
        failures.append("github_token_authority")
    if auth.get("api_key_registration_required_for_eleven_lane_cost_analysis") is not False:
        failures.append("api_key_cost_analysis_boundary")
    if doc.get("authority_effect")!="NONE":
        failures.append("authority_effect")
    if failures:
        print("PROVIDER_SECRET_RETIREMENT_AUDIT=DENY")
        for item in failures: print(item)
        return 1
    print("PROVIDER_SECRET_RETIREMENT_AUDIT=PASS")
    print(f"retired_workflows={len(retired)}")
    print("active_direct_provider_secret_consumers=0")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
