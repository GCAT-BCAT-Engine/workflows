# CHF Validation Matrix — v0.8b New Semantic Specs

This bundle performs Option B: add new semantic spec files and the corresponding validator support.

## Stable dispatcher rule

The GitHub Actions workflow is still not included and should remain unchanged.

## New specs

| Spec | Purpose |
|---|---|
| `problem_spec_chf_014.yml` | Probabilistic cloud admissibility gate |
| `problem_spec_chf_015.yml` | Branch splitting after unresolved uncertainty |
| `problem_spec_chf_016.yml` | Irreversible horizon analogy guardrail |

## Expected run

```text
Overall status: PASS
Specs evaluated: 16
```

## New result labels

```text
PROBABILISTIC_ALLOW
PROBABILISTIC_FAIL_CLOSED
BRANCH_SPLIT
BRANCH_FAIL_CLOSED
FORMAL_ANALOGY_ALLOWED
PHYSICS_CLAIM_BLOCKED
EMPIRICAL_CLAIM_FAIL_CLOSED
```
