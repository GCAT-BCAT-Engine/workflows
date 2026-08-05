# Handoff, Semantic, and Continuity Orchestration Contract

## Boundary

Continuity authority is the first verified-state admission stage inside the
Runtime Orchestrator. It proves which repository handoff governs, that its
declared hash matches, that scoped and archived handoffs cannot compete, and
that the declared document profile is structurally present.

Authority verification does not, by itself, prove that every factual claim
inside the handoff matches repository reality.

Semantic reconciliation is the second admission stage for Format A handoffs.
It parses the nine typed fields, applies a multi-source field-authority table,
checks conformance before state, and compares only repository-authoritative
claims with the checked-out repository tree. It is read-only.

Continuity provenance is the third admission stage. It proves which actor or
session changed state, which base commit it used, which paths changed, and
which external references were verified.

The Runtime Orchestrator may determine standing and select a next node only
after all applicable gates return `ALLOW`. A non-Format-A repository may
receive semantic `ALLOW` with processing disposition `DEFER`; that is an
explicit non-applicability result, not a claim of semantic verification.

## Repository authority contract

Each governed repository carries:

```text
.handoff/current.json
one repository-wide current handoff
zero or more explicitly scoped handoffs
dated or SESSION_ARCHIVE_ historical handoffs
a hosted authority workflow
```

A repository must not infer source-of-truth authority from traversal order,
modification time, document length, or prose in an undeclared document.

## Semantic reconciliation contract

Each Format A repository carries or receives a pinned copy of:

```text
config/handoff-field-authority.format-a-v1.json
a read-only semantic verifier
a hosted semantic workflow
```

The field authority sources are:

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

Only repository-tree fields are mechanically compared with repository state.
`Remaining work` and `Next task` are not stale merely because the work is not
complete, and no semantic worker may empty those queues.

Stored paths must be canonical repository-relative paths. Human display
transforms, including omission of a leading period from `.github`, are
non-conformant machine input.

Semantic reconciliation emits separate deterministic receipts:

```text
stegverse.handoff_conformance.receipt.v1
stegverse.handoff_state_delta.receipt.v1
stegverse.handoff_reconciliation.receipt.v1
stegverse.handoff_semantic_admission.receipt.v1
```

A reconciliation fixed point exists when one complete pass produces zero
conformance deltas and zero repository-authoritative state deltas. Remaining
intent does not prevent convergence. Maximum-pass exhaustion or repeated
nonconsecutive delta fingerprints fails closed.

Repair remains disabled:

```text
repair_mode: READ_ONLY
repair_enabled: false
```

A state delta may produce a proposal, but no automated handoff write is
authorized by this contract.

## Continuity provenance contract

Each enforced repository carries:

```text
.continuity/config.json
.continuity/change-records/<change-id>.json
.continuity/cross-repository-references.json
a hosted provenance workflow
```

The current change record binds the work to a base commit, actor, governing
handoff hash, complete changed-path inventory, per-path content hashes,
implemented claims, unresolved tasks, and deterministic record hash.

The validator compares every non-exempt declared path to the Git diff from the
declared base commit to `HEAD`. An undeclared changed path produces `DENY`.

Machine-generated exemptions must be explicit glob patterns in
`.continuity/config.json` and remain governed by their own machine lane.

## Cross-repository references

Every required external dependency identifies:

```text
reference id
owner/repository
source commit
repository-relative path
content hash
verification status
verification evidence
```

A required reference that is not `VERIFIED`, lacks a pinned commit or content
hash, or lacks verification evidence produces `DENY`.

Reference verification does not grant destination custody, execution
authority, admissibility, release, publication, or deployment.

## Reusable workflows

Handoff authority:

```yaml
jobs:
  handoff-authority:
    uses: GCAT-BCAT-Engine/workflows/.github/workflows/handoff-authority-reusable.yml@<immutable-commit>
    with:
      repository: owner/repository
      verifier_ref: <immutable-commit>
```

Handoff semantics:

```yaml
jobs:
  handoff-semantics:
    uses: GCAT-BCAT-Engine/workflows/.github/workflows/handoff-semantics-reusable.yml@<immutable-commit>
    with:
      repository: owner/repository
      verifier_ref: <immutable-commit>
```

Continuity provenance:

```yaml
jobs:
  continuity-provenance:
    uses: GCAT-BCAT-Engine/workflows/.github/workflows/continuity-provenance-reusable.yml@<immutable-commit>
    with:
      repository: owner/repository
      verifier_ref: <immutable-commit>
```

The called workflows verify caller repositories in the caller checkout
context. This avoids requiring the public workflows repository to retain
private cross-organization read credentials.

## Decision envelope

```text
terminal_decision:
  ALLOW | DENY | CONDITIONAL | FAIL_CLOSED

processing_disposition:
  NONE | REVIEW_REQUIRED | BLOCKED | DEFER
```

Only an applicable `ALLOW` result admits standing evaluation, task selection,
release, or propagation.

## Custody

Per-repository workflow success is execution evidence. Master Records custody
is a separate downstream transition and retains source commits, manifest or
record hashes, workflow runs, boundary declarations, and custody decisions.
Custody does not grant execution authority.
