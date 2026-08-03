# SV-COST-LINEAGE-002 Status

## Governing objective
Repeat the original SV-Cost test, compare the repeat to the first run, establish lineage, and only then test new routes.

## Retained historical anchors
- BL-001: 4,169 tokens; $0.061659; approximately 52.5 seconds.
- OP-002: 4,169 tokens; $0.0308295; reported 50% reduction.

## Existing repeat evidence discovered
The repository already contains `SV-COST-HISTORICAL-RERUN-002`, a best-available control-envelope reproduction of VAL-001 and BL-001.

BL-001-RERUN:
- 4,239 native tokens
- $0.061869 reconstructed observed provider cost
- 59.59 seconds
- stop reason `max_tokens`
- token delta from BL-001: +70 (+1.68%)
- cost delta from BL-001: +$0.000210 (+0.34%)

This is not a byte-identical replay because the exact historical prompt and request payload were not retained. The rerun also failed its output-class validator because the response saturated the 4,096-output-token ceiling before including the Lean candidate and claim boundary.

## Missing lineage work
1. Inventory and classify all historical fields as exact, reconstructed, inferred, or unknown.
2. Reconcile whether BL-001 historical validity depended on the same output obligations now used by the rerun validator.
3. Reproduce OP-002 under the same best-available control envelope.
4. Determine whether OP-002 was an actual provider batch execution, a batch-priced accounting route, or another optimization route from retained receipts.
5. Produce one original-versus-repeat lineage report covering BL-001 and OP-002 without introducing any new route.

## Gate
No compact-context, reconstruction, provider-substitution, or normalized-output benchmark may be labeled Cost Analysis 2 until the original BL-001/OP-002 lineage report is complete.
