# StegVerse Compact-Context Capability Benchmark

| Lane | Stage | Canonical input | Canonical total | Cost | Latency s |
|---|---:|---:|---:|---:|---:|
| stegverse-openai-full | NONE | 222 | 562 | $0.023260 | 15.98 |
| stegverse-openai-compact | S1 | 1,823 | 2,585 | $0.063935 | 33.86 |
| stegverse-anthropic-full | NONE | 222 | 950 | $0.014301 | 19.53 |
| stegverse-anthropic-compact | S3 | 5,117 | 8,748 | $0.085770 | 84.82 |

## Full versus compact

- openai: same stage=False; canonical input reduction=-721.17%; cost reduction=-174.87%
- anthropic: same stage=False; canonical input reduction=-2204.95%; cost reduction=-499.75%

## Boundary

This tests governed context compression and selective retrieval. It does not establish independent theorem discovery by StegVerse.
