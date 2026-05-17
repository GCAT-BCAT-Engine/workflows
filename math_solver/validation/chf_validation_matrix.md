# CHF Validation Matrix — v0.7a Edge Expansion

This matrix expands existing supported specs only. The workflow dispatcher and validator do not need to change.

## Expanded specs

| Spec | Added pressure |
|---|---|
| `chf-001` | 2D angle boundaries, radius boundaries, origin behavior, near-horizon precision |
| `chf-002` | multi-center disagreement, exact horizon under plausible centers, center-boundary behavior |
| `chf-006` | 3D axis ties, exact horizon, just-outside horizon, small-vector cell behavior |
| `chf-011` | lag-reachable exact boundary, just-over boundary, zero-lag, high uncertainty |
| `chf-013` | exact relevance threshold, protected low deformation, unknown deformation |

## Expected run

```text
Overall status: PASS
Specs evaluated: 13
```

## Failure localization rule

Each added case has a descriptive ID so the GitHub Actions summary itself identifies where the formalism or validator behavior differs from expectation.
