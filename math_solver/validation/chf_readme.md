# Consequence Horizon Formalism Validation — v0.8a

This is Option A: add adversarial validation pressure to existing supported problem-spec schemas only.

## Done condition

The existing workflow dispatcher and validator remain unchanged, and the run should report:

```text
Overall status: PASS
Specs evaluated: 13
```

## Changed files

This bundle replaces only supported problem specs and docs under:

```text
math_solver/validation/
```

## Not changed

This bundle does not include or modify:

```text
.github/workflows/chf_validation_run.yml
math_solver/validation/chf_deterministic_validator.py
```

## Next step after v0.8a

Option B should add new semantic coverage with new spec files, likely requiring validator support. Candidate new specs:

```text
problem_spec_chf_014.yml  # probabilistic cloud admissibility
problem_spec_chf_015.yml  # branch splitting after unresolved uncertainty
problem_spec_chf_016.yml  # irreversible horizon / black-hole-like threshold analogy guardrail
```
