# CHF Sandbox Runner

The CHF sandbox runner is the generated-case test bed for Consequence Horizon Formalism validation.

## Purpose

The direct problem specs validate known cases. The sandbox validates generated families of cases.

## Current suites

| Suite | Generated coverage |
|---|---|
| `chf-001` | 2D cell / horizon seeded sweeps and boundary probes |
| `chf-002` | multi-center robust permission seeded sweeps |
| `chf-004` | observer projection distinguishability grid |
| `chf-011` | lag-reachable radius seeded sweeps |
| `chf-014` | probabilistic recoverability / harm / unknown grid |
| `chf-015` | branch custody / receipts truth-table grid |
| `chf-016` | analogy-guardrail claim-scope truth-table grid |

## Done condition

The full validator should report both:

```text
Overall status: PASS
Sandbox status: PASS
```

The workflow file remains a stable dispatcher and does not need to change.
