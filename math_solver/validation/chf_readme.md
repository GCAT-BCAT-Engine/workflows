# Consequence Horizon Formalism Validation — v0.8b

This is Option B: new semantic specs plus validator support.

## Stable dispatcher preserved

This bundle does not include or modify:

```text
.github/workflows/chf_validation_run.yml
```

The workflow remains a stable dispatcher.

## Changed files

```text
math_solver/validation/chf_deterministic_validator.py
math_solver/validation/problem_spec_chf_014.yml
math_solver/validation/problem_spec_chf_015.yml
math_solver/validation/problem_spec_chf_016.yml
math_solver/validation/chf_validation_matrix.md
math_solver/validation/chf_readme.md
```

## New semantic coverage

### CHF-014 — Probabilistic Cloud Admissibility

Adds probability thresholds for recoverability, harm, and unknown mass.

### CHF-015 — Branch Splitting

Allows unresolved uncertainty to split into preserved branches only when custody and receipts are ready.

### CHF-016 — Irreversible Horizon Analogy Guardrail

Allows bounded formal analogy while blocking unsupported physical-equivalence claims.

## Done condition

The existing workflow should run unchanged and report:

```text
Overall status: PASS
Specs evaluated: 16
```
