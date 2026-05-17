# CHF Validation Matrix — v0.9 Full Sandbox Preflight

This bundle adds generated-case sandbox validation while preserving the stable workflow dispatcher.

## Direct specs

The repo should continue evaluating:

```text
problem_spec_chf_001.yml through problem_spec_chf_016.yml
```

Expected direct result:

```text
Explicit status: PASS
Specs evaluated: 16
```

## Sandbox suites

| Suite | Expected |
|---|---|
| `chf-001` generated 2D cell/horizon | PASS |
| `chf-002` generated multi-center uncertainty | PASS |
| `chf-004` generated observer projection grid | PASS |
| `chf-011` generated lag reachability | PASS |
| `chf-014` generated probabilistic cloud grid | PASS |
| `chf-015` generated branch-splitting grid | PASS |
| `chf-016` generated analogy guardrail grid | PASS |

Expected aggregate result:

```text
Overall status: PASS
Sandbox status: PASS
```
