# StegVerse Compact-Context Capability Benchmark

| Lane | Stage | Canonical input | Canonical total | Cost | Latency s |
|---|---:|---:|---:|---:|---:|
| stegverse-openai-full | NONE | 222 | 547 | $0.013870 | 8.50 |
| stegverse-openai-compact | NONE | 222 | 484 | $0.009100 | 5.43 |
| stegverse-anthropic-full | NONE | 222 | 922 | $0.014301 | 16.13 |
| stegverse-anthropic-compact | S6 | 8,784 | 13,778 | $0.125739 | 110.90 |

## Full versus compact

- openai: same stage=True; canonical input reduction=0.00%; cost reduction=34.39%
- anthropic: same stage=False; canonical input reduction=-3856.76%; cost reduction=-779.23%

## Boundary

This tests governed context compression and selective retrieval. It does not establish independent theorem discovery by StegVerse.
