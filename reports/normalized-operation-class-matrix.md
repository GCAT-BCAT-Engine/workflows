# Normalized Operation-Class Cost Matrix

Status: **OBSERVED, OPERATION-CLASS SEPARATED**

> Reconstruction is compared only when reconstruction is the requested operation. Zero provider charge is not treated as zero total cost when local runtime cost is unmeasured.

| Lane | Model/runtime | Comparable | Fully burdened cost known | Eligible | Observed provider charge | Decision |
|---|---|---:|---:|---:|---:|---|
| openai | gpt-5.6 | true | true | true | $0.038810 | PASS TO COST COMPARISON |
| anthropic | claude-sonnet-4-6 | true | true | true | $0.022950 | PASS TO COST COMPARISON |
| stegverse-only | deterministic-contract-reconstructor-v1 | true | false | false | $0.000000 | LOCAL_RUNTIME_COST_UNMEASURED |

## Bounded selection

`anthropic` is the least observed-cost eligible provider lane at `$0.022950`.

## Governance result

The StegVerse-only lane is not selected merely because its external provider charge is zero. Its local runtime cost remains unmeasured.

Batch-normalized values remain counterfactual and are excluded because no actual native batch receipt is present. Provider token counts remain interface observations and do not determine selection.

## Provenance boundary

Source: `experiments/sv-cost-normalized/results/result.json` at Git blob `a500441a5a9f3a486b56f013016b1fa4ef8969c0`.

The canonical generator will recompute and replace the source SHA-256 field on its next successful run. This manually integrated report does not claim a newly computed source SHA-256.
