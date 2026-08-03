# SV-COST-NORMALIZED-001

| Lane | Comparable | Attempts | Input | Output | Observed provider cost | Batch-normalized | Latency s |
|---|---:|---:|---:|---:|---:|---:|---:|
| openai | comparable | 1 | 310 | 1,242 | $0.038810 | $0.019405 | 22.38 |
| anthropic | comparable | 1 | 375 | 1,455 | $0.022950 | $0.011475 | 24.73 |
| stegverse-only | comparable | 1 | 0 | 0 | $0.000000 | N/A | 0.00 |

All three comparable: **True**
Human interventions after dispatch: **0**

## Boundary

Observed provider costs are reconstructed from retained native usage receipts and the versioned local price card. Batch-normalized values are counterfactual unless an actual batch receipt is retained. StegVerse-only external provider cost is zero while local runtime cost remains separately unmeasured.
