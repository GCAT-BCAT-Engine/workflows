# StegVerse Compact-Context Capability Benchmark

| Lane | Stage | Canonical input | Canonical total | Cost | Latency s |
|---|---:|---:|---:|---:|---:|
| stegverse-openai-full | S3 | 6,115 | 8,903 | $0.130425 | 64.44 |
| stegverse-openai-compact | NONE | 222 | 495 | $0.010750 | 5.69 |
| stegverse-anthropic-full | NONE | 222 | 949 | $0.014301 | 16.19 |
| stegverse-anthropic-compact | NONE | 222 | 866 | $0.012726 | 15.14 |

## Full versus compact

- openai: same stage=False; canonical input reduction=96.37%; cost reduction=91.76%
- anthropic: same stage=True; canonical input reduction=0.00%; cost reduction=11.01%

## Boundary

This tests governed context compression and selective retrieval. It does not establish independent theorem discovery by StegVerse.
