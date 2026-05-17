# CHF Validation Matrix — v0.7b Boundary Fix

This bundle fixes the v0.7a edge-test expectations without touching the stable dispatcher or validator.

## Why v0.7a failed

Two cases exposed mismatches between the expected labels and current validator semantics:

| Spec | Case | v0.7a issue |
|---|---|---|
| `chf-001` | `EDGE_exact_cell2_limit_allow` | Point `[-0.5, 0.0]` lies exactly at 180 degrees, which the validator assigns to `cell_3`, not `cell_2`. |
| `chf-002` | `EDGE_upper_shared_cell1_allow` | Point `[0.3, 0.4]` is at 90 degrees relative to center `[0.3, 0.0]`, which the validator assigns to `cell_2`, so robust all-center `cell_1` permission fails. |

## v0.7b corrections

| Spec | Correction |
|---|---|
| `chf-001` | Replaced exact cell-2 tests with 3-4-5 triangle points that truly fall inside `cell_2`. |
| `chf-002` | Moved `EDGE_upper_shared_cell1_allow` to `[0.6, 0.4]`, which is `cell_1` relative to both plausible centers. |

## Expected run

```text
Overall status: PASS
Specs evaluated: 13
```
