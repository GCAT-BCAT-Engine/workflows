#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
PROGRAM = ROOT.parent
SOURCE = PROGRAM / "five-lane-results" / "results" / "five_lane_results.json"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

SCHEMA = json.loads((ROOT / "product-comparison-schema.json").read_text())
DATA = json.loads(SOURCE.read_text())
ROWS = {row["lane_id"]: row for row in DATA["rows"]}

# These factors are sensitivity cases, not forecasts. 1.0 preserves the observed
# provider cost; smaller factors model progressively cheaper/abundant inference.
COMPRESSION_FACTORS = [1.0, 0.1, 0.01, 0.001, 0.0001]


def pair(raw_id: str, governed_id: str, label: str) -> dict[str, Any]:
    raw = ROWS[raw_id]
    gov = ROWS[governed_id]
    raw_cost = raw["total_observed_and_modeled_cost_usd"]
    gov_cost = gov["total_observed_and_modeled_cost_usd"]
    delta = gov_cost - raw_cost
    delta_pct = None if raw_cost == 0 else 100 * delta / raw_cost
    latency_delta = gov["latency_seconds"] - raw["latency_seconds"]
    hashes_match = raw["actual_output_hash"] == gov["actual_output_hash"] == DATA["required_output_hash"]

    sensitivity = []
    for factor in COMPRESSION_FACTORS:
        compressed_raw = raw_cost * factor
        # Hold the observed pair delta constant solely to expose denominator
        # behavior. This is not a claim that StegGate cost is fixed at delta.
        hypothetical_total = compressed_raw + delta
        premium_pct = None if compressed_raw == 0 else 100 * delta / compressed_raw
        sensitivity.append({
            "inference_compression_factor": factor,
            "hypothetical_raw_inference_cost_usd": compressed_raw,
            "held_constant_observed_pair_delta_usd": delta,
            "hypothetical_governed_total_usd": hypothetical_total,
            "premium_percent_if_delta_held_constant": premium_pct,
            "economically_invalid_if_total_negative": hypothetical_total < 0,
        })

    return {
        "product_label": label,
        "raw_lane": raw_id,
        "governed_lane": governed_id,
        "raw_cost_usd": raw_cost,
        "governed_cost_usd": gov_cost,
        "observed_pair_delta_usd": delta,
        "observed_pair_delta_percent": delta_pct,
        "incremental_latency_seconds": latency_delta,
        "raw_admissible": raw["admissible"],
        "governed_admissible": gov["admissible"],
        "normalized_outcome_equivalent": hashes_match,
        "pair_delta_interpretation": (
            "OBSERVED_PROVIDER_PAIR_DELTA_ONLY_NOT_ISOLATED_STEGGATE_COST"
        ),
        "compression_sensitivity": sensitivity,
    }


pairs = [
    pair("openai-raw", "openai-governed", "OpenAI + StegGate"),
    pair("anthropic-raw", "anthropic-governed", "Anthropic + StegGate"),
]

# The local deterministic lane is retained only as a reconstruction-cost reference.
# It must not be relabeled as the marginal wholesale StegGate cost for a provider.
local = ROWS["stegverse-only"]

result = {
    "schema_version": "1.0.0",
    "comparison_id": SCHEMA["comparison_id"],
    "source_experiment_id": DATA["experiment_id"],
    "source_task_id": DATA["task_id"],
    "source_required_output_hash": DATA["required_output_hash"],
    "analysis_type": "GOVERNED_AI_PREMIUM_AND_ABUNDANCE_SENSITIVITY",
    "provider_pairs": pairs,
    "stegverse_local_reference": {
        "lane_id": "stegverse-only",
        "cost_usd": local["total_observed_and_modeled_cost_usd"],
        "latency_seconds": local["latency_seconds"],
        "admissible": local["admissible"],
        "interpretation": "DETERMINISTIC_RECONSTRUCTION_REFERENCE_NOT_ISOLATED_PROVIDER_STEGGATE_PREMIUM",
    },
    "findings": {
        "unit_price_comparison_sufficient": False,
        "absolute_governance_cost_should_be_primary_under_compression": True,
        "percentage_premium_is_denominator_sensitive": True,
        "isolated_steggate_wholesale_cost_available": False,
        "deepseek_pair_available": False,
    },
    "claim_boundary": (
        "Sensitivity factors are hypothetical and are used only to test metric behavior as inference prices compress. "
        "Observed raw/governed pair deltas include provider token/output behavior and are not isolated StegGate wholesale cost. "
        "The StegVerse-only deterministic cost is a reference, not a provider integration premium. "
        "No market willingness-to-pay, target margin, enterprise ROI, or future provider price is established."
    ),
}

(OUT / "governed_ai_premium_results.json").write_text(json.dumps(result, indent=2) + "\n")

lines = [
    "# Governed AI Premium — Abundant-Intelligence Sensitivity",
    "",
    "This analysis uses the completed five-lane evidence only. DeepSeek remains pending.",
    "",
    "| Pair | Raw cost | Governed cost | Observed pair delta | Delta % | Latency delta | Equivalent/admissible |",
    "|---|---:|---:|---:|---:|---:|---|",
]
for item in pairs:
    lines.append(
        f"| {item['product_label']} | ${item['raw_cost_usd']:.12f} | ${item['governed_cost_usd']:.12f} | "
        f"${item['observed_pair_delta_usd']:.12f} | {item['observed_pair_delta_percent']:.6f}% | "
        f"{item['incremental_latency_seconds']:.6f}s | "
        f"{item['normalized_outcome_equivalent'] and item['raw_admissible'] and item['governed_admissible']} |"
    )

lines += [
    "",
    "## Interpretation",
    "",
    "The observed pair delta is not an isolated StegGate wholesale price. It includes any provider-side token/output changes caused by the governed prompt path.",
    "",
    "The compression sensitivity intentionally holds the observed pair delta constant while shrinking inference cost. This tests the metric, not the future market. If the denominator shrinks, percentage premium can explode even when absolute governance cost does not change.",
    "",
    "Therefore the preferred abundant-intelligence metric is absolute incremental governance cost per governed admissible outcome, once that cost is independently isolated.",
    "",
    "The next required experiment is isolation: provider inference must be held constant while StegGate compute, policy evaluation, receipt generation, storage, and reconstruction are metered separately.",
]
(OUT / "report.md").write_text("\n".join(lines) + "\n")

# Fail closed on the core invariants we can verify from historical evidence.
assert all(p["normalized_outcome_equivalent"] for p in pairs)
assert all(p["raw_admissible"] and p["governed_admissible"] for p in pairs)
assert result["findings"]["isolated_steggate_wholesale_cost_available"] is False
print("GOVERNED_AI_PREMIUM_SENSITIVITY_READY")
