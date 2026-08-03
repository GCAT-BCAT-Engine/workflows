# StegVerse Compact-Context Capability Benchmark

| Lane | Stage | Canonical input | Canonical total | Cost | Latency s |
|---|---:|---:|---:|---:|---:|
| stegverse-openai-full | NONE | 222 | 625 | $0.018010 | 11.13 |
| stegverse-openai-compact | S1 | 1,787 | 2,453 | $0.070445 | 37.27 |
| stegverse-anthropic-full | S3 | 8,412 | 11,827 | $0.098529 | 77.90 |
| stegverse-anthropic-compact | NONE | 222 | 943 | $0.014301 | 16.73 |

## Full versus compact

- openai: same stage=False; canonical input reduction=-704.95%; cost reduction=-291.14%
- anthropic: same stage=False; canonical input reduction=97.36%; cost reduction=85.49%

## Boundary

This tests governed context compression and selective retrieval. It does not establish independent theorem discovery by StegVerse.
