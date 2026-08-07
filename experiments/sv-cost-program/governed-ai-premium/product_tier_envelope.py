#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)
FIVE = json.loads((ROOT.parent / "five-lane-results" / "results" / "five_lane_results.json").read_text())
BURDEN = json.loads((OUT / "production_burden_results.json").read_text())
ROWS = {row["lane_id"]: row for row in FIVE["rows"]}

PROVIDERS = [
    ("openai", "openai-raw"),
    ("anthropic", "anthropic-raw"),
]
COMPRESSION = [1.0, 0.1, 0.01, 0.001, 0.0001]
TARGET_MARGINS = [0.20, 0.40, 0.60]


def mode(inference_cost: float, governance_cost: float) -> str:
    if governance_cost <= 0:
        return "TOKEN_PRICE_RELEVANT"
    ratio = inference_cost / governance_cost
    if ratio >= 10:
        return "TOKEN_PRICE_RELEVANT"
    if ratio >= 1:
        return "TOKEN_PRICE_COMPRESSED"
    return "INTELLIGENCE_ABUNDANT"


cases = []
for provider, lane_id in PROVIDERS:
    observed_raw = float(ROWS[lane_id]["total_observed_and_modeled_cost_usd"])
    for tier in BURDEN["tiers"]:
        governance_cost = float(tier["modeled_local_cost_usd_per_governed_action"])
        for factor in COMPRESSION:
            inference_cost = observed_raw * factor
            floor = inference_cost + governance_cost
            margin_prices = {
                f"{int(margin * 100)}pct": floor / (1.0 - margin)
                for margin in TARGET_MARGINS
            }
            cases.append({
                "provider": provider,
                "source_raw_lane": lane_id,
                "burden_tier": tier["tier_id"],
                "inference_compression_factor": factor,
                "mode": mode(inference_cost, governance_cost),
                "hypothetical_inference_cost_usd": inference_cost,
                "measured_local_governance_cost_usd": governance_cost,
                "governance_share_of_floor_percent": 100 * governance_cost / floor if floor else None,
                "governed_product_floor_usd": floor,
                "illustrative_retail_price_by_gross_margin": margin_prices,
            })

result = {
    "schema_version": "1.0.0",
    "experiment_id": "SV-GOVERNED-AI-PRODUCT-TIER-ENVELOPE-001",
    "source_provider_experiment": FIVE["experiment_id"],
    "source_burden_experiment": BURDEN["experiment_id"],
    "providers_included": [provider for provider, _ in PROVIDERS],
    "deepseek_included": False,
    "target_margin_scenarios": TARGET_MARGINS,
    "cases": cases,
    "findings": {
        "comparison_unit": "provider inference plus measured local StegGate burden per governed admissible action",
        "mode_switch_is_ratio_based_not_market_claim": True,
        "absolute_governance_cost_remains_visible_as_inference_compresses": True,
        "retail_prices_are_illustrative_only": True,
    },
    "claim_boundary": "This combines historical provider inference observations with synthetic local StegGate burden measurements to test product-economics behavior under hypothetical inference compression. Margin prices are arithmetic scenarios, not recommended prices, wholesale quotes, market willingness-to-pay evidence, or production cost claims. DeepSeek is excluded until canonical seven-lane evidence exists."
}

(OUT / "product_tier_envelope_results.json").write_text(json.dumps(result, indent=2) + "\n")

lines = [
    "# Governed AI Product-Tier Envelope",
    "",
    "This analysis combines historical provider inference observations with the staged local StegGate burden curve. It is a sensitivity model, not a price recommendation.",
    "",
    "| Provider | Burden tier | Compression | Mode | Inference | Governance | Governance share | Floor |",
    "|---|---|---:|---|---:|---:|---:|---:|",
]
for case in cases:
    if case["inference_compression_factor"] in (1.0, 0.01, 0.0001):
        lines.append(
            f"| {case['provider']} | {case['burden_tier']} | {case['inference_compression_factor']:.4f} | {case['mode']} | "
            f"${case['hypothetical_inference_cost_usd']:.12f} | ${case['measured_local_governance_cost_usd']:.12f} | "
            f"{case['governance_share_of_floor_percent']:.4f}% | ${case['governed_product_floor_usd']:.12f} |"
        )

lines += [
    "",
    "## Interpretation",
    "",
    "As inference cost compresses, governance can move from a small add-on to the dominant share of the governed product floor without any increase in the governance workload itself. This is why percentage-over-inference is not a stable long-run primary metric.",
    "",
    "The stronger abundant-intelligence unit is absolute governance cost per governed admissible action, segmented by the burden required for that action.",
    "",
    "Illustrative 20%, 40%, and 60% gross-margin arithmetic is emitted in JSON only and is not a pricing recommendation.",
]
(OUT / "product_tier_envelope_report.md").write_text("\n".join(lines) + "\n")

assert BURDEN["all_tiers_admissible"] is True
assert BURDEN["all_negative_cases_fail_closed"] is True
print("GOVERNED_AI_PRODUCT_TIER_ENVELOPE_READY")
