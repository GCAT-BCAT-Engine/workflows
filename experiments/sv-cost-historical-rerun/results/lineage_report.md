# SV-COST-LINEAGE-002 — Original versus Repeat

## Verdict

**Partially reproducible.**

The direct BL-001 control envelope reproduced closely. The optimized OP-002 arithmetic reproduces when the historical 50% route factor is applied to the rerun baseline, but no retained evidence currently proves that OP-002 was an independently observed provider-route execution.

## BL-001 lineage

| Field | Historical | Repeat | Delta |
|---|---:|---:|---:|
| Native total tokens | 4,169 | 4,239 | +70 (+1.68%) |
| Cost | $0.061659 | $0.061869 | +$0.000210 (+0.34%) |
| Latency | ~52.5 s | 59.59 s | +7.09 s |

The repeat used the reconstructed provider/model/control envelope and retained raw response, usage, hashes, and latency. It is not byte-identical because the exact historical request payload and prompt were not retained. The repeat reached the 4,096 output-token ceiling and its output-class validator did not find the Lean candidate or claim boundary before truncation.

## OP-002 lineage

| Field | Historical | Accounting replay from BL-001 repeat | Delta |
|---|---:|---:|---:|
| Workload tokens | 4,169 | 4,239 | +70 (+1.68%) |
| Cost after 50% factor | $0.0308295 | $0.0309345 | +$0.000105 (+0.34%) |
| Reported reduction | 50% | 50% | 0 percentage points |

The replay shows that the historical arithmetic is internally reproducible and inherits the same 0.34% cost variance as the repeated BL-001 baseline.

## Critical boundary

`OP-002-ACCOUNTING-REPLAY` is not an observed batch run and not an observed optimized provider-route run. No retained batch request receipt or distinct optimized-route execution receipt has been found. Until such evidence is found or a new route is actually executed under the same control envelope, OP-002 must be described as a route-accounting result rather than an independently observed execution result.

## Lineage decision

1. BL-001: **control-envelope reproducible**.
2. OP-002 arithmetic: **reproducible**.
3. OP-002 execution route: **not yet evidenced**.
4. Overall historical test: **partially reproducible**.
5. New-route testing remains gated until OP-002 is either reproduced as an observed route execution or permanently classified as accounting-only.
