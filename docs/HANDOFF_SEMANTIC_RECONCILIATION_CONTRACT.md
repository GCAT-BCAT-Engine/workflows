# Handoff Semantic Reconciliation Contract

## Boundary

Handoff authority proves which handoff governs. Semantic reconciliation begins
only after that authority result is `ALLOW`.

This subsystem is read-only. It parses the governing Format A handoff, measures
document conformance, compares repository-authoritative claims with the checked-
out repository tree, and emits deterministic receipts. It does not modify a
handoff, select a task, grant authority, or execute a repair.

## Ordered evaluation

```text
handoff authority ALLOW
  -> Format A conformance
  -> repository-authoritative state comparison
  -> reconciliation fixed-point evaluation
  -> existing standing and task orchestration
```

Conformance always runs before state comparison. A malformed document is not a
safe input to a state worker.

## Field authority

The machine table is
`config/handoff-field-authority.format-a-v1.json`.

```text
Source of truth                 -> handoff manifest
Role                            -> governance policy
Current installed files         -> repository tree
Current working path            -> governance policy
Done state for this repo        -> governance policy
Completed in latest pass        -> repository tree and receipts
Remaining work                  -> durable task registry
Destination installs            -> destination evidence and governance plan
Next task                       -> durable task registry
```

Only repository-tree fields are mechanically state-checked. Intent and task
fields are never rewritten merely because the repository has not completed
them.

## Canonical paths

Stored paths must be actual repository-relative paths. Human display
transformations are not valid stored data. In particular:

```text
github/workflows/example.yml    INVALID when the repository path is .github/...
.github/workflows/example.yml   VALID
```

A leading-dot display transformation is a conformance failure. If the omitted-
dot path is evaluated as a state claim, the worker reports the canonical path
as a suggestion but performs no write.

## Receipts and decisions

### Conformance

`stegverse.handoff_conformance.receipt.v1`

```text
ALLOW        + NONE             document conforms
FAIL_CLOSED  + REVIEW_REQUIRED  document cannot be safely state-checked
```

### State delta

`stegverse.handoff_state_delta.receipt.v1`

```text
ALLOW        + NONE     checked repository-authoritative claims exist
DENY         + BLOCKED  one or more checked claims are false
FAIL_CLOSED  + BLOCKED  conformance or required evidence is unavailable
```

### Reconciliation

`stegverse.handoff_reconciliation.receipt.v1`

A fixed point exists when one full pass produces zero conformance deltas and
zero repository-authoritative state deltas. Remaining work and next-task intent
are not drift and do not prevent convergence.

The guard fails closed when the declared maximum pass count is reached or when
a nonconsecutive delta fingerprint repeats, indicating oscillation.

## Repair posture

```text
repair_mode: READ_ONLY
repair_enabled: false
```

State deltas may identify a field as `PROPOSAL_ONLY`, but no automated write is
authorized. A future repair transition must carry:

```text
expected prior handoff blob hash
typed field and authority source
prior claim and observed state
proposed replacement
terminal decision and processing disposition
session change record
append-only repair ledger event
resulting handoff blob and commit
```

Git history and the repair ledger preserve superseded claims. The current
handoff remains a clean projection of current state rather than accumulating an
unbounded inline archive.
