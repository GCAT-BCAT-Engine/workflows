# Suggested Repository Landing Insert

## Consequence Horizon Formalism Validation

This repository contains a deterministic validation lane for the StegVerse Consequence Horizon Formalism.

CHF asks whether a consequence-bearing transition has standing to bind reality at commit.

The current lane validates:

```text
chf-001 through chf-040
explicit problem specs
generated sandbox suites
artifact-backed reporting
stable workflow dispatcher
```

Latest confirmed validation:

```text
Consequence Horizon Formalism Validation #16
Status: PASS
Specs evaluated: 40
Commit: 2455f61
```

### Architecture

```text
.github/workflows/chf_validation_run.yml
  stable dispatcher

math_solver/validation/chf_deterministic_validator.py
  explicit spec evaluator

math_solver/validation/chf_sandbox_runner.py
  generated-case sandbox evaluator

math_solver/validation/problem_spec_chf_###.yml
  deterministic formal gates
```

### Current claim

```text
A transition should not bind merely because an agent can execute it.
It should bind only when the system proves that authority, policy, records,
time, recovery, participants, downstream effects, and replay evidence remain coherent at commit.
```
