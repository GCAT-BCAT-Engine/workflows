# Consequence Horizon Formalism Validation — v0.9

This version adds the CHF sandbox runner.

## Stable dispatcher preserved

This bundle does not include or modify:

```text
.github/workflows/chf_validation_run.yml
```

## Changed files

```text
math_solver/validation/chf_deterministic_validator.py
math_solver/validation/chf_sandbox_runner.py
math_solver/validation/chf_sandbox_config.yml
math_solver/validation/chf_sandbox_readme.md
math_solver/validation/chf_validation_matrix.md
math_solver/validation/chf_readme.md
```

## Validation layers

```text
Layer 1: explicit problem specs
Layer 2: generated sandbox subtests
Layer 3: aggregate report
```

## Expected GitHub result

```text
Overall status: PASS
Explicit status: PASS
Specs evaluated: 16
Sandbox status: PASS
```
