# StegVerse Cost and Capability Analysis

Status: **DECISION READY — BOUNDED CLAIMS — GENERAL SAVINGS CLAIM NOT APPROVED**

Governing program: `SV-COST-MAJOR-GOAL-001`  
Canonical issue: `#12`  
Remaining favorable-ROI evidence: issue `#13`

This is the sole human-facing synthesis. Individual files are subordinate evidence and do not create independent conclusions.

## Decision

**DO_NOT_APPROVE_A_GENERAL_STEGVERSE_SAVINGS_CLAIM_FROM_CURRENT_EVIDENCE**

The testing program is decision-ready because it supports a bounded decision, not because it proves a favorable ROI.

## Evidence classes

1. **Observed execution:** native provider or repository execution with retained receipts, hashes, run identity, and artifacts.
2. **Pricing-derived value:** cost calculated from retained usage and a versioned price card; not an invoice.
3. **Accounting transform:** arithmetic applied without a distinct execution receipt.
4. **Reconstruction:** reuse of admitted repository state; not equivalent fresh inference.

## R1 — Historical control-envelope reproduction

| Measure | Historical BL-001 | Repeat | Difference |
|---|---:|---:|---:|
| Native tokens | 4,169 | 4,239 | +70 / +1.68% |
| Pricing-derived cost | $0.061659 | $0.061869 | +$0.000210 / +0.34% |
| Latency | ~52.5 s | 59.59 s | +7.09 s |

Verdict: `OBSERVED_AND_VALIDATED_WITH_RECONSTRUCTION_BOUNDARY`.

The exact historical prompt and request payload were not retained. OP-002 remains an accounting replay rather than an observed historical optimized-route execution.

Receipt: `experiments/sv-cost-program/results/historical-lineage-observation.json`

## R2 — Direct synchronous versus native provider batch

| Measure | Direct | Batch |
|---|---:|---:|
| Paired trials | 10 | 10 |
| Mean tokens | 4,239 | 4,239 |
| Mean pricing-derived cost | $0.061869 | $0.0309345 |
| Mean latency | 64.63 s | 181.95 s |
| Completion rate | 0% | 0% |
| Verifier pass rate | 0% | 10% |

Verdict: `ROUTE_EFFECT_NOT_ADMISSIBLE_DUE_TO_QUALITY_OR_COMPLETION_DIVERGENCE`.

The native batch route and batch identifier were observed, but successful quality-equivalent outputs were not established. The 50% route-price effect is not an admissible successful-output savings claim.

Receipt: `experiments/sv-cost-program/results/r2-adjudication.json`

## R3 — Full context versus StegVerse-managed context

Run: `30829852891`  
Generation: `r3-gen-20260803-fix1`  
Paired trials: 5

| Measure | Full context | Managed context |
|---|---:|---:|
| Mean input tokens | 19238.2 | 4938.4 |
| Mean output tokens | 7337.2 | 7707.0 |
| Mean pricing-derived cost | $0.167773 | $0.130420 |
| Mean latency | 122.55 s | 128.29 s |
| Full-path completion rate | 40% | 60% |
| Successful-output rate | 0% | 0% |

Paired managed-minus-full effects:

- Mean input-token delta: -14299.8
- Input-token 95% CI: [-28320.89480558595, -278.7051944140476]
- Mean pricing-derived cost delta: $-0.037352
- Cost 95% CI: [-0.13594626127664858, 0.06124146127664857]
- Mean latency delta: 5.74 seconds
- Latency 95% CI: [-48.887388905274385, 60.37189225287447]

Verdict: `CONTEXT_EFFECT_NOT_ADMISSIBLE_DUE_TO_QUALITY_OR_COMPLETION_DIVERGENCE`.

Managed context substantially reduced observed input tokens in this locked workload, but neither lane produced successful outputs under the full completion and verifier gate. The cost interval crosses zero, quality diverged, and pricing-derived cost is not invoice evidence. No headline context-savings claim is admitted.

Receipt: `experiments/sv-cost-program/results/r3-adjudication.json`

## R4 — Fresh generation versus governed reconstruction

Verdict: `EXTERNAL_PROVIDER_GENERATION_CAN_BE_AVOIDED_FOR_ALREADY_ADMITTED_WORK_NET_SAVINGS_UNPROVEN`.

Reconstruction of already admitted work can avoid a new external provider-generation charge. It is a different operation from fresh inference. The observed external-provider avoidance scenarios were $0.03881 versus the retained OpenAI generation and $0.02295 versus the retained Anthropic generation.

Net savings and fully burdened ROI remain unproven because StegVerse local compute, storage, verification, engineering, and maintenance costs are unmeasured.

Receipt: `experiments/sv-cost-program/results/r4-adjudication.json`

## R5 — Reliability

Status: `R5_ADJUDICATED_CROSS_RELATION_RELIABILITY`.

The program retains 15 paired trials across R2 and R3. These relations estimate different causal effects and are not pooled into one savings percentage. Failures, retries, confidence intervals, and quality gates remain part of the result.

Receipt: `experiments/sv-cost-program/results/r5-reliability-synthesis.json`

## CFO findings

- Historical control envelope reproduced: `true`
- Successful route savings established: `false`
- Successful managed-context savings established: `false`
- External provider charge avoidance for admitted reconstruction established: `true`
- Net reconstruction savings established: `false`

## Required before favorable ROI approval

1. Measure StegVerse compute, storage, verification, engineering, and maintenance cost.
2. Reconcile pricing-derived provider costs to invoices.
3. Execute a successful quality-equivalent held-out context-management test before any favorable context claim.
4. Calculate workload-weighted break-even and sensitivity ranges.

Durable owner: issue `#13`.

## Reproduction and audit paths

- Evidence index: `experiments/sv-cost-program/evidence-index.json`
- Program lineage: `experiments/sv-cost-program/lineage.json`
- Relational matrix: `experiments/sv-cost-program/relations.json`
- R3 immutable artifact: ID `8863128197`, digest `sha256:8591f70a40d1765d15fb45902d22643f5189d777126ca45d18e941d1b38e7912`
- Machine-readable CFO receipt: `experiments/sv-cost-program/results/cfo-decision.json`
- Session and continuation handoff: `SV_COST_MIRROR_HANDOFF.md`

## Claim boundary

The completed program supports a bounded financial decision. It does not support a favorable general StegVerse savings or ROI claim. No downstream publication may remove the distinctions among observed execution, pricing-derived values, accounting transforms, and reconstruction.
