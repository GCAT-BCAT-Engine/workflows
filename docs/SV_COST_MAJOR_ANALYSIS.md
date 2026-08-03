# StegVerse Cost and Capability Analysis

Status: **DECISION READY — BOUNDED CLAIMS — GENERAL SAVINGS CLAIM NOT APPROVED**

Governing program: `SV-COST-MAJOR-GOAL-001` / issue #12

This is the only human-facing synthesis document for the SV-Cost program. Individual receipts and reports are subordinate evidence. They do not create separate conclusions and should not require operator reconciliation.

## Major question

Under controlled, lineage-preserving tests, what measurable cost, latency, reliability, and capability changes can be attributed to execution-route selection, StegVerse-managed context, or governed reconstruction?

## Decision posture

The evidence currently supports three bounded conclusions:

1. The historical BL-001 cost envelope is reproducible within a narrow difference, subject to loss of the exact original prompt and payload.
2. A native Anthropic batch route and its route-price effect were observed, but the comparison did not produce successful quality-equivalent outputs, so no CFO-grade route-savings claim is admitted.
3. Repository reconstruction can avoid a new external provider call for already admitted work, but it is a different operation from fresh inference and local StegVerse cost is not yet measured.

The active R3 relation is testing whether StegVerse-managed context changes provider tokens, pricing-derived cost, latency, or successful-output quality while holding the provider, model, route, task, stage order, and verifier constant. No R3 conclusion is admitted until generation-bound evidence and adjudication are committed.

## Canonical control surfaces

- Evidence index: `experiments/sv-cost-program/evidence-index.json`
- Program lineage: `experiments/sv-cost-program/lineage.json`
- Relational matrix: `experiments/sv-cost-program/relations.json`
- Canonical results: `experiments/sv-cost-program/results/`

## R1 — Historical baseline reproduction

The best-available BL-001 repeat reproduced the historical control envelope closely:

| Measure | Historical BL-001 | Repeat | Difference |
|---|---:|---:|---:|
| Native tokens | 4,169 | 4,239 | +70 / +1.68% |
| Pricing-derived cost | $0.061659 | $0.061869 | +$0.000210 / +0.34% |
| Latency | ~52.5 s | 59.59 s | +7.09 s |

**Verdict:** `OBSERVED_AND_VALIDATED_WITH_RECONSTRUCTION_BOUNDARY`

This is a control-envelope reproduction, not a byte-identical replay. The exact original prompt and request payload were not retained, and the repeated BL-001 response reached the output-token ceiling.

### Historical OP-002 boundary

The historical OP-002 value of $0.0308295 is exactly 50% of the historical BL-001 cost. Applying the same factor to the repeated BL-001 cost gives $0.0309345, also +0.34% from the historical value.

That reproduces the accounting transformation. It does **not** prove a historical optimized-route execution because no distinct OP-002 provider route receipt was retained.

Canonical observation: `experiments/sv-cost-program/results/historical-lineage-observation.json`

## R2 — Direct synchronous versus provider batch

**Governed verdict:** `ROUTE_EFFECT_NOT_ADMISSIBLE_DUE_TO_QUALITY_OR_COMPLETION_DIVERGENCE`

| Measure | Direct | Batch |
|---|---:|---:|
| Paired trials | 10 | 10 |
| Mean tokens | 4,239 | 4,239 |
| Mean pricing-derived cost | $0.061869 | $0.0309345 |
| Mean latency | 64.63 s | 181.95 s |
| Completion rate | 0% | 0% |
| Verifier pass rate | 0% | 10% |

Observed paired effects:

- Mean batch-minus-direct pricing-derived cost: **-$0.0309345**
- Mean batch-minus-direct latency: **+117.33 seconds**
- Native provider batch identifier retained: `msgbatch_01HL3iB57s9Z7TNtHYj3LtxG`

The provider batch route was genuinely observed. However, neither lane established successful completion, and verifier outcomes diverged. The route-price effect is retained as evidence but is not admissible as a successful-output savings claim. Pricing-derived cost is not invoice evidence.

Canonical adjudication: `experiments/sv-cost-program/results/r2-adjudication.json`

## R3 — Full context versus StegVerse-managed context

**Current state:** `REPAIRED_GENERATION_DISPATCHED`

Active generation: `r3-gen-20260803-fix1`

The paired test holds constant:

- provider and model;
- synchronous route;
- task identity and seven-stage S0–S6 order;
- output obligations and verifier;
- trial identities and pricing basis.

The changed variable is the context representation:

- full lane: all prior generated stage content;
- managed lane: artifact ledger plus stage-selective retrieval.

The first generation failed because the runner used a non-Python lowercase Boolean literal after provider execution. That implementation defect was isolated from the economic claim, the defective controller was retired, and a repaired generation was dispatched with source SHA, run ID, attempt, and generation binding.

No token, cost, latency, quality, or savings result is claimed until both of these exist:

- `experiments/sv-cost-program/r3-full-vs-managed/results/result.json`
- `experiments/sv-cost-program/results/r3-adjudication.json`

A headline context-savings claim requires both lanes to complete and verify the full S0–S6 path in every accepted pair.

## R4 — Fresh generation versus governed reconstruction

The normalized evidence contains three operation lanes:

| Lane | Operation | Input tokens | Output tokens | Pricing-derived / observed provider cost | Local cost status |
|---|---|---:|---:|---:|---|
| OpenAI | Fresh generation | 310 | 1,242 | $0.038810 | N/A |
| Anthropic | Fresh generation | 375 | 1,455 | $0.022950 | N/A |
| StegVerse-only | Deterministic repository reconstruction | 0 external | 0 external | $0 external provider cost | Unmeasured local runtime |

All three lanes satisfied the selected structural obligations, but the operation classes differ. The StegVerse-only lane reconstructed already encoded work; it did not perform equivalent fresh provider inference.

The admissible economic statement is therefore limited to:

> Governed reconstruction can avoid a new external provider-generation charge for already admitted work.

The evidence does not yet establish net savings because StegVerse compute, storage, verification, maintenance, and engineering costs remain unmeasured. R4 must remain outside like-for-like provider comparison tables.

Source evidence: `experiments/sv-cost-normalized/results/result.json`

## R5 — Repetition, variance, and reliability

R2 includes ten paired trials and reports route effects, completion rates, verifier rates, latency variance, and confidence intervals. R3 is designed as five paired trials and will extend the reliability record only after its terminal evidence is committed.

Averages alone are not sufficient. The final synthesis must preserve:

- trial count and pairing;
- completion and verifier failure rates;
- retries and bounded-repair events;
- variance and 95% confidence intervals;
- provider execution receipts and source identity.

## CFO-readiness gate

| Requirement | Current state |
|---|---|
| Immutable lineage and canonical evidence paths | Established |
| Historical reproducibility boundary | Established |
| Observed native route execution | Established in R2 |
| Successful quality-equivalent route savings | Not established |
| Successful quality-equivalent managed-context effect | R3 pending |
| Repeated paired trials and failure reporting | R2 established; R3 pending |
| Provider invoice reconciliation | Missing |
| StegVerse local compute/storage/verification cost | Missing |
| Fully burdened cost and break-even analysis | Blocked by local-cost gap |
| One decision-facing synthesis | This document, still in progress |

## Claim boundaries

The final document must keep four classes separate:

1. **Observed execution:** native provider or repository execution with retained receipts and hashes.
2. **Pricing-derived value:** cost calculated from retained usage and a versioned price card; not an invoice.
3. **Accounting transform:** arithmetic applied without a distinct execution receipt.
4. **Reconstruction savings:** avoided fresh-provider work for already admitted artifacts; not inference equivalence.

No favorable or unfavorable result may be promoted beyond its evidence class.

## Remaining governed transitions

1. Observe and adjudicate repaired R3 evidence.
2. Canonically adjudicate R4 as a different-operation reuse result.
3. Consolidate R2 and R3 reliability evidence under R5.
4. Add local-cost and invoice evidence or explicitly preserve those gaps.
5. Produce the final CFO decision section with workload scenarios, break-even sensitivity, risks, and reproduction instructions.

## Operator boundary

The operator is not required to inspect individual result files. New evidence must update the canonical evidence index, lineage manifest, relational matrix, and this document. No standalone report may redefine the program or introduce a new major goal.

## R3 — Full versus StegVerse-managed context

- Verdict: `CONTEXT_EFFECT_NOT_ADMISSIBLE_DUE_TO_QUALITY_OR_COMPLETION_DIVERGENCE`
- Paired trials: 5
- Full successful-output rate: 0%
- Managed successful-output rate: 0%
- Mean input-token delta, managed minus full: -14299.80
- Mean pricing-derived cost delta, managed minus full: $-0.037352
- Mean latency delta, managed minus full: 5.74 seconds
- Headline savings admissible: false

The finding is bounded by successful full-path quality equivalence and by the distinction between pricing-derived cost and invoice evidence.
## Final program synthesis

**Program state:** `RELATIONAL_PROGRAM_EXECUTED_DECISION_READY_BOUNDED_CLAIMS`

**CFO decision:** Do not approve a general StegVerse savings or ROI claim from the current evidence.

- R1 reproduced the historical control envelope with an explicit reconstruction boundary.
- R2 observed a native batch route and pricing effect, but successful quality-equivalent outputs were not established.
- R3 verdict: `CONTEXT_EFFECT_NOT_ADMISSIBLE_DUE_TO_QUALITY_OR_COMPLETION_DIVERGENCE`.
- R3 headline managed-context savings admissible: `false`.
- R4 establishes only that reconstruction of already admitted work can avoid a new external provider-generation charge; net savings remain unproven because local costs are unmeasured.
- R5 retains 15 paired trials across two distinct causal relations and does not pool them into one savings percentage.

### Required before ROI approval

1. Meter StegVerse compute, storage, verification, engineering, and maintenance cost.
2. Reconcile pricing-derived provider charges to invoices.
3. Repeat any favorable R3 effect on a held-out workload.
4. Produce workload-weighted break-even and sensitivity ranges.

The completed testing program supports a bounded financial decision. It does not support a favorable general savings claim unless the remaining cost and validation gates are satisfied.

Machine-readable decision receipt: `experiments/sv-cost-program/results/cfo-decision.json`
