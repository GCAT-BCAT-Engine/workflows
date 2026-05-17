# Consequence Horizon Formalism Validation — v0.7b Boundary Fix

This package is a data/spec-only correction for the v0.7a edge expansion.

## Stable dispatcher rule preserved

This bundle does not include or modify:

```text
.github/workflows/chf_validation_run.yml
math_solver/validation/chf_deterministic_validator.py
```

## Changed files

```text
math_solver/validation/problem_spec_chf_001.yml
math_solver/validation/problem_spec_chf_002.yml
math_solver/validation/chf_validation_matrix.md
math_solver/validation/chf_readme.md
```

## Done condition

The existing workflow should run unchanged and report:

```text
Overall status: PASS
Specs evaluated: 13
```

## Meaning

The v0.7a failure was useful. It showed that the stable dispatcher and validator correctly surfaced edge-case expectation errors in the problem specs. v0.7b corrects those data points without changing the dispatcher or validator.
