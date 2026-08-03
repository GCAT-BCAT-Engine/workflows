#!/usr/bin/env python3
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "results"
RESULTS = json.loads((OUT / "results.json").read_text())

BATCH_MULTIPLIER = 0.50
LOCAL_EXTERNAL_INFERENCE_COST = 0.0

rows = []
for result in RESULTS["results"]:
    provider = result["provider"]
    mode = result["context_mode"]
    is_compact = mode == "compact"
    observed = float(result["observed_api_cost_usd"])
    optimized = observed * BATCH_MULTIPLIER if is_compact else observed
    rows.append({
        "lane_id": result["lane_id"],
        "provider": provider,
        "workload_mode": mode,
        "execution_mode_observed": "synchronous",
        "batch_eligible": is_compact,
        "highest_admitted_stage": result["highest_admitted_stage"],
        "canonical_input_tokens": result["canonical_input_tokens"],
        "canonical_total_tokens": result["canonical_total_tokens"],
        "observed_synchronous_cost_usd": observed,
        "batch_normalized_remaining_work_cost_usd": optimized,
        "batch_multiplier": BATCH_MULTIPLIER if is_compact else 1.0,
        "cost_status": "BATCH_NORMALIZED_NOT_BATCH_RECEIPTED" if is_compact else "OBSERVED_SYNCHRONOUS",
    })

comparisons = []
for provider in ("openai", "anthropic"):
    full = next(r for r in rows if r["provider"] == provider and r["workload_mode"] == "full")
    compact = next(r for r in rows if r["provider"] == provider and r["workload_mode"] == "compact")
    baseline = full["observed_synchronous_cost_usd"]
    compact_sync = compact["observed_synchronous_cost_usd"]
    combined = compact["batch_normalized_remaining_work_cost_usd"]
    comparisons.append({
        "provider": provider,
        "same_highest_stage": full["highest_admitted_stage"] == compact["highest_admitted_stage"],
        "baseline_full_sync_cost_usd": baseline,
        "compact_sync_cost_usd": compact_sync,
        "combined_compact_batch_normalized_cost_usd": combined,
        "workload_reduction_percent": (1 - compact_sync / baseline) * 100 if baseline else 0,
        "combined_net_reduction_percent": (1 - combined / baseline) * 100 if baseline else 0,
        "governance_and_verification_external_cost_included": True,
        "batch_execution_receipt_present": False,
    })

stegverse_only = {
    "lane_id": "stegverse-only",
    "external_inference": "DENIED",
    "external_inference_cost_usd": LOCAL_EXTERNAL_INFERENCE_COST,
    "batch_applicable": False,
    "capability": [
        "resolve exact or governed-equivalent task identity",
        "retrieve admitted artifacts by hash",
        "reconstruct accepted state",
        "run deterministic validation and installed formal verification",
        "issue a fresh continuity receipt"
    ],
    "novel_unsolved_stage_behavior": "BLOCKED unless an installed local inference or theorem-discovery engine can perform the unresolved work",
    "economic_effect": "Artifact reuse can reduce external inference to zero for exact still-admissible repetitions. Batch pricing does not apply when no provider call occurs.",
    "unmeasured_local_costs": ["GitHub Actions runtime", "storage", "hashing", "retrieval", "deterministic verification"],
}

report = {
    "experiment_id": "SV-COMPACT-PROGRESS-002-ECONOMIC",
    "source_experiment": RESULTS["experiment_id"],
    "rows": rows,
    "comparisons": comparisons,
    "stegverse_only": stegverse_only,
    "claim_boundary": (
        "Observed synchronous costs are provider receipts from the four-lane rerun. "
        "Combined costs apply the documented 50% batch rate only to the remaining compact workload and are labeled batch-normalized until an actual Batch API receipt is retained."
    ),
}
(OUT / "economic-results.json").write_text(json.dumps(report, indent=2))

lines = [
    "# Four-Lane StegVerse Economic Capability Report",
    "",
    "| Lane | Stage | Canonical input | Observed sync cost | Combined compact + batch-normalized cost | Status |",
    "|---|---:|---:|---:|---:|---|",
]
for row in rows:
    lines.append(
        f"| {row['lane_id']} | {row['highest_admitted_stage']} | {row['canonical_input_tokens']:,} | "
        f"${row['observed_synchronous_cost_usd']:.6f} | ${row['batch_normalized_remaining_work_cost_usd']:.6f} | {row['cost_status']} |"
    )
lines += ["", "## Provider comparisons", ""]
for c in comparisons:
    lines.append(
        f"- {c['provider']}: same stage={c['same_highest_stage']}; workload-only reduction={c['workload_reduction_percent']:.2f}%; "
        f"combined compact + batch-normalized reduction={c['combined_net_reduction_percent']:.2f}%."
    )
lines += [
    "",
    "## StegVerse-only lane",
    "",
    "- External inference remains denied and external provider cost is $0.",
    "- Batch pricing does not apply because there is no provider request.",
    "- Exact still-admissible repetitions may be fulfilled through artifact retrieval, deterministic reconstruction, verification, and a fresh receipt.",
    "- Novel unresolved mathematical work remains BLOCKED unless an installed local solver can perform it.",
    "- Local GitHub Actions, storage, retrieval, hashing, and verification costs must be measured separately rather than reported as zero total cost.",
    "",
    "## Boundary",
    "",
    report["claim_boundary"],
]
(OUT / "economic-report.md").write_text("\n".join(lines) + "\n")
print(json.dumps({"comparisons": comparisons, "stegverse_only": stegverse_only}, indent=2))
