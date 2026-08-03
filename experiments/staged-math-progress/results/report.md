# Staged Mathematical Progress Benchmark

Status: MEASURED

| Lane | Highest admitted stage | Admitted stages | Canonical tokens | API cost | Latency s |
|---|---:|---:|---:|---:|---:|
| openai-only | S0 | 1 | 978 | $0.015760 | 8.16 |
| stegverse-openai | NONE | 0 | 523 | $0.008095 | 4.46 |
| anthropic-only | S0 | 1 | 2,066 | $0.026010 | 29.26 |
| stegverse-anthropic | NONE | 0 | 1,017 | $0.014601 | 17.81 |

## Boundary

This experiment measures progress through a stipulated formalization. It does not establish correctness for a deployed GCAT/BCAT implementation.

A stage is counted only after deterministic evidence-string validation. The benchmark measures serialized progress and observed provider cost; it does not expose or equate hidden provider reasoning.
