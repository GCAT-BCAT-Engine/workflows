# Consequence Horizon Formalism Validation — v0.10

This version adds receipt sufficiency, branch merge reconciliation, and entropy/irreversibility budget validation.

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
math_solver/validation/problem_spec_chf_017.yml
math_solver/validation/problem_spec_chf_018.yml
math_solver/validation/problem_spec_chf_019.yml
math_solver/validation/chf_validation_matrix.md
math_solver/validation/chf_readme.md
```

## Expected GitHub result

```text
Overall status: PASS
Explicit status: PASS
Specs evaluated: 19
Sandbox status: PASS
```
