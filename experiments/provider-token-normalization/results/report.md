# Normalized StegVerse Provider Token Comparison

Status: VALID

| Lane | Native in | Native out | Canonical task in | Canonical governance in | Canonical proof out | Canonical governance out | API cost | Latency s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| stegverse-openai | 140 | 4096 | 77 | 58 | 15 | 1587 | $0.123580 | 62.15 |
| stegverse-anthropic | 155 | 4096 | 77 | 58 | 67 | 3202 | $0.061905 | 70.39 |

## Accounting boundary

Shared task content is counted once. Incremental StegVerse governance input is isolated from the task. Output is divided heuristically into proof content and governance/verification ledger content; raw responses and hashes are preserved for reconstruction. Native provider tokens remain billing receipts while cl100k_base counts provide the cross-lane comparison.
