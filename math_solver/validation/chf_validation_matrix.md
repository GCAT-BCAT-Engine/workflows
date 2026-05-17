# CHF Validation Matrix — v0.10 Receipt, Reconciliation, Entropy

This bundle adds semantic specs 017-019 and generated sandbox suites for each.

## New specs

| Spec | Purpose |
|---|---|
| `chf-017` | Receipt sufficiency and custody gate |
| `chf-018` | Branch merge and reconciliation gate |
| `chf-019` | Entropy and irreversibility budget gate |

## Stable dispatcher

This bundle does not include:

```text
.github/workflows/chf_validation_run.yml
```

## Expected direct result

```text
Explicit status: PASS
Specs evaluated: 19
```

## Expected sandbox result

```text
Sandbox status: PASS
Subtests failed: 0
```
