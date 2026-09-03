#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"security/provider-secret-historical-source-audit.v1.json"
RETIRE=ROOT/"security/provider-secret-workflow-retirement-audit.v1.json"

def main()->int:
    src=json.loads(SOURCE.read_text())
    ret=json.loads(RETIRE.read_text())
    failures=[]
    if src.get("schema")!="stegverse.provider-secret-historical-source-audit/v1":
        failures.append("schema")
    entries=src.get("entries")
    if not isinstance(entries,list) or len(entries)!=17:
        failures.append("entry_count")
        entries=[] if not isinstance(entries,list) else entries
    retired={x["path"]:x["retirement_commit"] for x in ret.get("retired_workflows",[])}
    if len(retired)!=17:
        failures.append("retirement_audit_count")
    seen=set()
    for e in entries:
        path=e.get("path")
        if not isinstance(path,str) or path in seen:
            failures.append(f"duplicate_or_invalid_path:{path}")
            continue
        seen.add(path)
        if retired.get(path)!=e.get("retirement_commit"):
            failures.append(f"retirement_commit_mismatch:{path}")
        providers=e.get("providers")
        secrets=e.get("secret_names")
        if not isinstance(providers,list) or not isinstance(secrets,list):
            failures.append(f"provider_or_secret_shape:{path}")
        if e.get("historical_runtime_actor")!="UNRESOLVED_REQUIRES_ORG_AUDIT_LOG":
            failures.append(f"runtime_actor_boundary:{path}")
        if e.get("historical_token_provenance")!="UNRESOLVED_REQUIRES_ORG_AUDIT_LOG":
            failures.append(f"token_boundary:{path}")
        if e.get("repository_visibility_at_execution")!="UNRESOLVED_REQUIRES_ORG_AUDIT_LOG":
            failures.append(f"visibility_boundary:{path}")
        if e.get("result_artifact_hashes")!="UNRESOLVED_REQUIRES_RETAINED_RUN_ARTIFACTS":
            failures.append(f"artifact_boundary:{path}")
    s=src.get("summary") or {}
    expected={
      "workflows":len(entries),
      "workflows_with_provider_secret_names":sum(bool(x.get("secret_names")) for x in entries),
      "workflows_with_contents_write":sum(x.get("contents_write") is True for x in entries),
      "workflows_with_git_push":sum(x.get("git_push") is True for x in entries),
      "workflows_with_local_tvc_labels":sum(x.get("local_tvc_label") is True for x in entries),
      "workflows_with_local_cge_labels":sum(x.get("local_cge_label") is True for x in entries),
      "workflows_with_local_publication_labels":sum(x.get("local_publication_label") is True for x in entries),
      "workflows_with_explicit_provider_network_calls":sum(x.get("provider_network_call") is True for x in entries),
    }
    if s!=expected:
        failures.append("summary_mismatch")
    if src.get("authority_effect")!="NONE":
        failures.append("authority_effect")
    if failures:
        print("PROVIDER_SECRET_HISTORICAL_SOURCE_AUDIT=DENY")
        for x in failures: print(x)
        return 1
    print("PROVIDER_SECRET_HISTORICAL_SOURCE_AUDIT=PASS")
    for k,v in expected.items(): print(f"{k}={v}")
    print("runtime_actor_token_visibility=UNRESOLVED_REQUIRES_ORG_AUDIT_LOG")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
