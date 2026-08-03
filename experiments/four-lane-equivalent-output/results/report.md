# Four-Lane Equivalent-Output Benchmark

Status: VALID_MEASUREMENT_INCOMPLETE_OUTPUT

| Lane | Complete | Native in | Native out | Canonical in | Canonical out | API cost | Latency s |
|---|---:|---:|---:|---:|---:|---:|---:|
| openai-only | TRUE | 160 | 4809 | 155 | 3719 | $0.145070 | 65.98 |
| stegverse-openai | TRUE | 238 | 6264 | 234 | 4365 | $0.189110 | 95.08 |
| anthropic-only | FALSE | 176 | 8192 | 155 | 6450 | $0.123408 | 135.94 |
| stegverse-anthropic | FALSE | 269 | 8192 | 234 | 6104 | $0.123687 | 125.33 |

## Interpretation boundary

Costs are observed API charges under the recorded pricing assumptions. A lane enters the cost-per-equivalent-output comparison only when every required section and END_OF_ARTIFACT are present. Governed and ungoverned lanes use the same task; governed lanes add only the pinned StegVerse governance block.
