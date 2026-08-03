# StegVerse Compact-Context Capability Benchmark

| Lane | Stage | Canonical input | Canonical total | Cost | Latency s |
|---|---:|---:|---:|---:|---:|
| stegverse-openai-full | S4 | 9,330 | 12,387 | $0.195070 | 93.88 |
| stegverse-openai-compact | S6 | 8,067 | 10,971 | $0.154830 | 65.91 |
| stegverse-anthropic-full | NONE | 222 | 937 | $0.014211 | 18.75 |
| stegverse-anthropic-compact | NONE | 222 | 765 | $0.011151 | 12.89 |

## Full versus compact

- openai: same stage=False; canonical input reduction=13.54%; cost reduction=20.63%
- anthropic: same stage=True; canonical input reduction=0.00%; cost reduction=21.53%

## Boundary

This tests governed context compression and selective retrieval. It does not establish independent theorem discovery by StegVerse.
