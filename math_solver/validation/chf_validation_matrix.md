# CHF Validation Matrix — v0.8a Adversarial Existing-Spec Expansion

This bundle performs Option A: more adversarial cases inside existing supported schemas only.

## Stable files intentionally untouched

```text
.github/workflows/chf_validation_run.yml
math_solver/validation/chf_deterministic_validator.py
```

## Expanded specs

| Spec | New pressure |
|---|---|
| `chf-001` | precedence of horizon denial over cell uncertainty, radius boundary, cell boundary behavior |
| `chf-002` | conservative multi-center disagreement and robust all-center allow cases |
| `chf-004` | observer distinguishability exact threshold and high-lag smoothing |
| `chf-005` | record legibility exact threshold and missing legibility behavior |
| `chf-006` | 3D zero-vector and axis-tie assignment behavior |
| `chf-007` | geometry gate combinations beyond baseline |
| `chf-008` | GCAT invalid bounds and low-governance/high-autonomy cases |
| `chf-009` | missing propagated record and invalid-simplex commit cases |
| `chf-010` | exact recoverability threshold and combined failure cases |
| `chf-011` | default uncertainty buffer and high-drift failure |
| `chf-012` | extra links, missing prior shell, exact legibility threshold |
| `chf-013` | zero epsilon and protected above-threshold behavior |

## Expected run

```text
Overall status: PASS
Specs evaluated: 13
```

## Note

Case IDs are intentionally descriptive because YAML comments do not appear in the GitHub Actions summary.
