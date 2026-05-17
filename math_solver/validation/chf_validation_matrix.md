# CHF Validation Matrix — v0.16 Agent Boundary Batch

Adds explicit deterministic specs for `chf-041` through `chf-050`.

## Stable dispatcher

This bundle does not include:

```text
.github/workflows/chf_validation_run.yml
```

## New gates

| Spec | Purpose |
|---|---|
| `chf-041` | adversarial prompt / instruction boundary |
| `chf-042` | tool invocation standing |
| `chf-043` | secret / credential exposure |
| `chf-044` | data exfiltration / boundary crossing |
| `chf-045` | autonomous recursion limit |
| `chf-046` | model output reliance |
| `chf-047` | simulation-to-reality transfer |
| `chf-048` | governance capture / influence concentration |
| `chf-049` | dependency drift / supply chain |
| `chf-050` | emergency override / break-glass |

## Expected result

```text
Overall status: PASS
Explicit status: PASS
Specs evaluated: 50
Sandbox status: PASS
```
