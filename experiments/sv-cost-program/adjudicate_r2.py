#!/usr/bin/env python3
import hashlib
import json
import math
import pathlib
import statistics

ROOT = pathlib.Path(__file__).resolve().parent
R2 = ROOT / "r2-direct-vs-batch"
RESULT = R2 / "results" / "result.json"
GOV = R2 / "governance.json"
PROTOCOL = R2 / "protocol.json"
RELATIONS = ROOT / "relations.json"
OUT = ROOT / "results" / "r2-adjudication.json"
ANALYSIS = ROOT.parent.parent / "docs" / "SV_COST_MAJOR_ANALYSIS.md"


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def mean(values):
    return statistics.fmean(values) if values else None


def variance(values):
    return statistics.variance(values) if len(values) > 1 else 0.0


def rate(rows, key):
    return sum(bool(r[key]) for r in rows) / len(rows) if rows else 0.0


def verifier_rate(rows):
    return sum(bool(r.get("verifier", {}).get("pass")) for r in rows) / len(rows) if rows else 0.0


def ci95(values):
    if len(values) < 2:
        return [None, None]
    m = mean(values)
    se = statistics.stdev(values) / math.sqrt(len(values))
    margin = 2.262 * se if len(values) == 10 else 1.96 * se
    return [m - margin, m + margin]


result = load(RESULT)
gov = load(GOV)
protocol = load(PROTOCOL)
direct = result["direct_results"]
batch = result["batch_results"]

assert result["transition_status"] == "R2_OBSERVED_AND_VALIDATED"
assert len(direct) == len(batch) and len(direct) > 0
assert len({r["request_sha256"] for r in direct + batch}) == 1
assert all(r["provider"] == result["provider"] for r in direct + batch)
assert all(r["model_returned"] == result["model"] for r in direct + batch)
assert result.get("batch_id")

paired_cost_delta = [b["pricing_derived_cost_usd"] - d["pricing_derived_cost_usd"] for d, b in zip(direct, batch)]
paired_latency_delta = [b["latency_seconds"] - d["latency_seconds"] for d, b in zip(direct, batch)]

direct_completion = rate(direct, "complete")
batch_completion = rate(batch, "complete")
direct_verifier = verifier_rate(direct)
batch_verifier = verifier_rate(batch)
quality_equivalent = direct_completion == batch_completion and direct_verifier == batch_verifier
successful_quality_equivalent = quality_equivalent and direct_completion > 0 and direct_verifier > 0

if successful_quality_equivalent:
    verdict = "ROUTE_EFFECT_ADMISSIBLE_WITH_QUALITY_EQUIVALENCE"
elif quality_equivalent:
    verdict = "ROUTE_EFFECT_OBSERVED_BUT_BOTH_LANES_FAILED_QUALITY_GATE"
else:
    verdict = "ROUTE_EFFECT_NOT_ADMISSIBLE_DUE_TO_QUALITY_OR_COMPLETION_DIVERGENCE"

adjudication = {
    "program_id": "SV-COST-MAJOR-GOAL-001",
    "relation_id": "R2-DIRECT-VS-BATCH",
    "status": "R2_ADJUDICATED",
    "verdict": verdict,
    "governance_interpretation": "The prior state admitted R2 as the next relation. This adjudication reconstructs whether the observed transition satisfies the locked invariants and publication gate; worker identity is not treated as free-standing authority.",
    "evidence": {
        "result_sha256": sha(RESULT),
        "governance_sha256": sha(GOV),
        "protocol_sha256": sha(PROTOCOL),
        "batch_id": result["batch_id"],
        "paired_n": len(direct),
        "single_request_hash": next(iter({r["request_sha256"] for r in direct + batch})),
    },
    "direct": {
        "mean_tokens": mean([r["total_tokens"] for r in direct]),
        "mean_pricing_derived_cost_usd": mean([r["pricing_derived_cost_usd"] for r in direct]),
        "mean_latency_seconds": mean([r["latency_seconds"] for r in direct]),
        "completion_rate": direct_completion,
        "verifier_pass_rate": direct_verifier,
    },
    "batch": {
        "mean_tokens": mean([r["total_tokens"] for r in batch]),
        "mean_pricing_derived_cost_usd": mean([r["pricing_derived_cost_usd"] for r in batch]),
        "mean_latency_seconds": mean([r["latency_seconds"] for r in batch]),
        "completion_rate": batch_completion,
        "verifier_pass_rate": batch_verifier,
    },
    "paired_effect": {
        "mean_cost_delta_usd_batch_minus_direct": mean(paired_cost_delta),
        "cost_delta_variance": variance(paired_cost_delta),
        "cost_delta_ci95": ci95(paired_cost_delta),
        "mean_latency_delta_seconds_batch_minus_direct": mean(paired_latency_delta),
        "latency_delta_variance": variance(paired_latency_delta),
        "latency_delta_ci95": ci95(paired_latency_delta),
    },
    "publication_gate": {
        "quality_equivalent": quality_equivalent,
        "successful_quality_equivalent": successful_quality_equivalent,
        "headline_cost_savings_admissible": successful_quality_equivalent,
        "pricing_is_invoice_evidence": False,
        "claim_boundary": "The route and pricing effect is observed, but a CFO-grade savings claim requires successful equivalent outputs. Pricing-derived cost is not an invoice receipt.",
    },
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(adjudication, indent=2) + "\n")

relations = load(RELATIONS)
for relation in relations["relations"]:
    if relation["id"] == "R2-DIRECT-VS-BATCH":
        relation["status"] = verdict
        relation["adjudication_ref"] = str(OUT.relative_to(ROOT.parent.parent))
    if relation["id"] == "R3-FULL-VS-STEGVERSE-CONTEXT":
        relation["status"] = "NEXT_ADMISSIBLE_RELATION_DESIGN_REQUIRED"
relations["status"] = "R2_ADJUDICATED_R3_NEXT"
RELATIONS.write_text(json.dumps(relations, indent=2) + "\n")

section = f'''\n## R2 — Direct synchronous versus provider batch\n\n**Governed verdict:** `{verdict}`\n\n- Paired trials: {len(direct)}\n- Direct mean pricing-derived cost: ${adjudication['direct']['mean_pricing_derived_cost_usd']:.6f}\n- Batch mean pricing-derived cost: ${adjudication['batch']['mean_pricing_derived_cost_usd']:.6f}\n- Direct completion rate: {direct_completion:.0%}\n- Batch completion rate: {batch_completion:.0%}\n- Direct verifier pass rate: {direct_verifier:.0%}\n- Batch verifier pass rate: {batch_verifier:.0%}\n- Mean batch-minus-direct latency: {adjudication['paired_effect']['mean_latency_delta_seconds_batch_minus_direct']:.2f} seconds\n\nThe provider batch route and its native batch identifier were observed. The calculated route-price effect is retained as pricing-derived evidence. It is not presented as a CFO-grade successful-output savings claim unless both lanes produce equivalent successful outputs under the shared verifier.\n\nCanonical adjudication: `experiments/sv-cost-program/results/r2-adjudication.json`\n'''
text = ANALYSIS.read_text() if ANALYSIS.exists() else "# SV-COST Major Analysis\n"
marker = "\n## R2 — Direct synchronous versus provider batch\n"
if marker in text:
    text = text.split(marker)[0].rstrip() + "\n"
ANALYSIS.write_text(text.rstrip() + "\n" + section)
print(json.dumps(adjudication, indent=2))
