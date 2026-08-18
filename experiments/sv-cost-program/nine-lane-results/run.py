#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent
RESULT = ROOT / "results" / "generation-2-output-boundary" / "nine_lane_generation_2_results.json"
KIMI_EVIDENCE = ROOT / "cost-evidence" / "kimi-k3-allegretto-subscription-allocation-2026-08-17.json"
RUNNER = ROOT / "run_candidate_outputs.py"

completed = subprocess.run([sys.executable, str(RUNNER)], cwd=ROOT.parent.parent.parent.parent)
if completed.returncode not in (0, 3):
    raise SystemExit(completed.returncode)

result = json.loads(RESULT.read_text())

if result.get("all_nine_present") and KIMI_EVIDENCE.exists():
    evidence = json.loads(KIMI_EVIDENCE.read_text())
    if evidence.get("provider") != "kimi" or evidence.get("task_id") != "SV-RECON-001":
        raise SystemExit("invalid Kimi cost evidence identity")
    if evidence.get("provider_api_key_transferred_to_stegverse") is not False:
        raise SystemExit("Kimi evidence violates credential-transfer boundary")
    if evidence.get("evidence_mode") != "SUBSCRIPTION_QUOTA_ALLOCATED_EFFECTIVE_COST":
        raise SystemExit("unsupported Kimi cost evidence mode")
    if evidence.get("marginal_api_charge_reported") is not False:
        raise SystemExit("Kimi subscription evidence must not be represented as marginal API charge")

    allocation = float(evidence["calculation"]["allocated_effective_cost_usd"])
    basis = "SUBSCRIPTION_QUOTA_ALLOCATED_EFFECTIVE_COST_NOT_MARGINAL_API_CHARGE"
    for row in result["rows"]:
        if row.get("provider") != "kimi":
            continue
        row["provider_cost_usd"] = allocation
        row["provider_cost_basis"] = basis
        row["provider_cost_evidence"] = str(KIMI_EVIDENCE.relative_to(ROOT))
        if row.get("lane_id") == "kimi-governed":
            incremental = row.get("governance_incremental_cost_usd")
            row["total_cost_usd"] = round(allocation + float(incremental or 0.0), 12)

    old = "MISSING_COST_EVIDENCE:kimi:reported_cost_or_versioned_official_rate_card_required"
    result["cost_blockers"] = [x for x in result.get("cost_blockers", []) if x != old]
    result["blockers"] = [x for x in result.get("blockers", []) if x != old]
    result["cost_basis_disclosure"] = {
        "kimi": basis,
        "evidence": str(KIMI_EVIDENCE.relative_to(ROOT)),
        "allocated_effective_cost_usd": allocation,
        "comparability_note": "Kimi value is an allocated share of a user-facing subscription quota, not a marginal API invoice charge. Other provider cost fields retain their own declared/reported basis."
    }

# A cost-analysis publication requires an admissible cost basis for every
# external raw candidate. Behavioral/governance proof may still pass when
# provider-facing applications do not expose per-request cost or token usage.
for provider in ("openai", "anthropic", "deepseek", "kimi"):
    raw = next((r for r in result.get("rows", []) if r.get("lane_id") == f"{provider}-raw"), None)
    if raw is None:
        continue
    if raw.get("provider_cost_usd") is None:
        blocker = f"MISSING_COST_EVIDENCE:{provider}:reported_cost_or_admissible_bound_cost_basis_required"
        if blocker not in result.setdefault("cost_blockers", []):
            result["cost_blockers"].append(blocker)
        if blocker not in result.setdefault("blockers", []):
            result["blockers"].append(blocker)

result["cost_evidence_complete"] = bool(result.get("all_nine_present")) and not result.get("cost_blockers")
all_admissible = bool(result.get("all_lanes_admissible"))
if result.get("all_nine_present") and result["cost_evidence_complete"] and all_admissible:
    result["publication_status"] = "RESULTS_READY_FOR_BOUNDED_PUBLICATION"
else:
    result["publication_status"] = "PUBLICATION_BLOCKED"

RESULT.write_text(json.dumps(result, indent=2) + "\n")
print(result["publication_status"])
raise SystemExit(0 if result.get("all_nine_present") else 3)
