# Staged Mathematical Progress Benchmark

Status: MEASURED

| Lane | Highest admitted stage | Admitted stages | Canonical tokens | API cost | Latency s |
|---|---:|---:|---:|---:|---:|
| openai-only | S6 | 7 | 6,662 | $0.070790 | 30.62 |
| stegverse-openai | S6 | 7 | 10,533 | $0.118185 | 41.39 |
| anthropic-only | S6 | 7 | 17,309 | $0.133770 | 91.55 |
| stegverse-anthropic | S5 | 6 | 20,602 | $0.152289 | 97.90 |

## Boundary

This experiment measures progress through a stipulated formalization. It does not establish correctness for a deployed GCAT/BCAT implementation.

A stage is counted only after deterministic evidence-string validation. The benchmark measures serialized progress and observed provider cost; it does not expose or equate hidden provider reasoning.
