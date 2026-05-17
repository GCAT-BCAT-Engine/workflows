# Consequence Horizon Formalism Validation — v0.7a Edge Expansion

This package expands existing CHF problem specs without changing the stable GitHub Actions dispatcher or the deterministic validator.

## Stable dispatcher rule

The workflow remains a dispatcher only:

```text
checkout
setup Python
install dependencies
run validator
upload reports
```

New validation pressure is added through problem spec files under:

```text
math_solver/validation/
```

## Changed files in this bundle

```text
math_solver/validation/problem_spec_chf_001.yml
math_solver/validation/problem_spec_chf_002.yml
math_solver/validation/problem_spec_chf_006.yml
math_solver/validation/problem_spec_chf_011.yml
math_solver/validation/problem_spec_chf_013.yml
math_solver/validation/chf_validation_matrix.md
math_solver/validation/chf_readme.md
```

## Not changed

```text
.github/workflows/chf_validation_run.yml
math_solver/validation/chf_deterministic_validator.py
```

## Purpose

This expansion tests whether the current validator semantics are stable at boundary conditions.

The case IDs intentionally document the expected behavior because YAML comments are not surfaced in the workflow summary.
