# StegVerse Cost and Capability Analysis

Status: **IN PROGRESS — NOT YET PUBLICATION READY**

Governing program: `SV-COST-MAJOR-GOAL-001` / issue #12

This is the only human-facing synthesis document for the SV-Cost program. Individual receipts and reports are evidence inputs. They are not separate conclusions and should not require operator reconciliation.

## Major question

Under controlled, lineage-preserving tests, what measurable cost, latency, reliability, and capability changes can be attributed to execution route selection or StegVerse intervention?

## Current conclusions

### 1. Historical baseline reproduction

The best-available BL-001 repeat reproduced the original cost envelope closely:

| Measure | Historical BL-001 | Repeat | Difference |
|---|---:|---:|---:|
| Native tokens | 4,169 | 4,239 | +70 / +1.68% |
| Cost | $0.061659 | $0.061869 | +$0.000210 / +0.34% |
| Latency | ~52.5 s | 59.59 s | +7.09 s |

This is a control-envelope reproduction, not a byte-identical replay. The exact original prompt and request payload were not retained, and the repeat reached the output-token ceiling.

### 2. Historical OP-002 status

The reported OP-002 value of $0.0308295 is exactly 50% of the historical BL-001 cost. Applying the same arithmetic factor to the repeated BL-001 cost gives $0.0309345, also +0.34% from the historical OP-002 value.

This demonstrates reproducible arithmetic. It does **not** yet demonstrate an observed batch or optimized route execution because no retained provider route receipt has been found.

### 3. Three-platform normalized run

The OpenAI, Anthropic, and repository-native StegVerse outputs satisfied the selected obligations. This remains useful reconstruction evidence, but it is not a like-for-like inference-cost comparison: OpenAI and Anthropic generated new answers, while the StegVerse-only lane reconstructed an answer from admitted repository state.

It is therefore excluded from headline platform-cost comparison tables and will be reported later as governed reuse economics.

## Relational test program

| Relation | Independent variable | Current state |
|---|---|---|
| Historical BL-001 vs faithful repeat | execution time / reconstructed historical payload | Partially executed |
| Direct vs actual batch route | provider execution route | Blocked: no observed batch receipt |
| Full context vs StegVerse-managed context | context representation | Designed, not executed |
| Generation vs governed reconstruction | operation class | Executed; separate analysis class |
| Repeated paired trials | trial instance | Pending executable paired relation |

The full machine-readable contracts are maintained at:

- `experiments/sv-cost-program/evidence-index.json`
- `experiments/sv-cost-program/relations.json`

## Publication gate

This document becomes publication-ready only when:

1. the historical lineage record is complete and every unknown is explicit;
2. at least one genuinely paired route or StegVerse-context relation has been executed;
3. the same verifier and completion criteria are used across each pair;
4. repeated trials report variance, failures, and retry cost;
5. observed costs are distinguished from accounting transforms and counterfactual estimates;
6. every headline statement links to canonical receipts.

## Operator boundary

The operator is not required to interpret individual result files. New evidence must update the canonical index, relational matrix, and this document. No standalone narrative result document may redefine the program or create a new goal.

## R2 — Direct synchronous versus provider batch

**Governed verdict:** `ROUTE_EFFECT_NOT_ADMISSIBLE_DUE_TO_QUALITY_OR_COMPLETION_DIVERGENCE`

- Paired trials: 10
- Direct mean pricing-derived cost: $0.061869
- Batch mean pricing-derived cost: $0.030934
- Direct completion rate: 0%
- Batch completion rate: 0%
- Direct verifier pass rate: 0%
- Batch verifier pass rate: 10%
- Mean batch-minus-direct latency: 117.33 seconds

The provider batch route and its native batch identifier were observed. The calculated route-price effect is retained as pricing-derived evidence. It is not presented as a CFO-grade successful-output savings claim unless both lanes produce equivalent successful outputs under the shared verifier.

Canonical adjudication: `experiments/sv-cost-program/results/r2-adjudication.json`
