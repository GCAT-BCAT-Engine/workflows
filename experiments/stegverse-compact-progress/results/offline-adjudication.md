# Offline Semantic Adjudication

| Lane | Original stage | Offline stage | Available outputs | Next required stage |
|---|---:|---:|---:|---:|
| stegverse-openai-full | S6 | S6 | 7 | none |
| stegverse-openai-compact | S3 | S3 | 5 | S4 |
| stegverse-anthropic-full | NONE | NONE | 1 | S0 |
| stegverse-anthropic-compact | NONE | NONE | 1 | S0 |

## Boundary

This rescoring uses retained outputs only. It does not invent missing downstream stages or alter observed provider tokens, cost, or latency.
