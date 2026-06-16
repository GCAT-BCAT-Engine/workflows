# RTG-001 Workflow Install Contract

Generated: `2026-06-16T01:53:55Z`

This package moves RTG from:

```text
handoff_contract_ready
```

to:

```text
handoff_installed_in_execution_repo
```

It still does not claim dispatch or solver execution.

Next valid states are:

```text
workflow_dispatch_attempted
artifact_returned
artifact_ingested
rtg_state_updated
```
