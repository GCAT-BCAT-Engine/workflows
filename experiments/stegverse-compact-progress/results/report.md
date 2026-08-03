# StegVerse Compact-Context Capability Benchmark

| Lane | Stage | Canonical input | Canonical total | Cost | Latency s |
|---|---:|---:|---:|---:|---:|
| stegverse-openai-full | S6 | 14,280 | 18,388 | $0.240140 | 97.48 |
| stegverse-openai-compact | S3 | 4,475 | 6,412 | $0.141470 | 67.91 |
| stegverse-anthropic-full | NONE | 222 | 908 | $0.013596 | 19.51 |
| stegverse-anthropic-compact | NONE | 222 | 854 | $0.013266 | 19.36 |

## Full versus compact

- openai: same stage=False; canonical input reduction=68.66%; cost reduction=41.09%
- anthropic: same stage=True; canonical input reduction=0.00%; cost reduction=2.43%

## Boundary

This tests governed context compression and selective retrieval. It does not establish independent theorem discovery by StegVerse.
