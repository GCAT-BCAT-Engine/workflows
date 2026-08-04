# Handoff and Continuity Orchestration Contract

## Boundary

Continuity authority is the verified-state admission stage inside the existing
Runtime Orchestrator. It determines which repository handoff governs and
whether that handoff matches repository state. It does not select or execute a
task.

Continuity provenance then proves which actor or session changed that state,
which base commit it used, which paths changed, and which external references
were verified.

The Runtime Orchestrator may determine standing and select a next node only
after both gates return `ALLOW`.

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

Continuity provenance:

```yaml
jobs:
  continuity-provenance:
    uses: GCAT-BCAT-Engine/workflows/.github/workflows/continuity-provenance-reusable.yml@<immutable-commit>
    with:
      repository: owner/repository
      verifier_ref: <immutable-commit>
```

The called workflows verify the caller repository in the caller checkout
context. This avoids requiring the public workflows repository to retain
private cross-organization read credentials.

## Decisions

- `ALLOW`: required authority or provenance state is proven.
- `DENY`: a declared invariant is violated.
- `FAIL_CLOSED`: required evidence cannot be read or evaluated.

Only `ALLOW` admits standing evaluation, task selection, release, or
propagation.

## Custody

Per-repository workflow success is execution evidence. Master Records custody
is a separate downstream transition and retains source commit, manifest or
record hashes, workflow runs, boundary declarations, and custody decisions.
