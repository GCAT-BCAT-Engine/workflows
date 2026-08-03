# Offline Semantic Adjudication

| Lane | Original stage | Offline stage | Available outputs | Next required stage |
|---|---:|---:|---:|---:|
| stegverse-openai-full | NONE | NONE | 1 | S0 |
| stegverse-openai-compact | NONE | NONE | 1 | S0 |
| stegverse-anthropic-full | NONE | NONE | 1 | S0 |
| stegverse-anthropic-compact | S6 | S6 | 7 | none |

## Boundary

This rescoring uses retained outputs only. It does not invent missing downstream stages or alter observed provider tokens, cost, or latency.
