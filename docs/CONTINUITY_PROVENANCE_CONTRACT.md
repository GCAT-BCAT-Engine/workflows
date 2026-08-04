# Continuity Provenance and Cross-Repository Reference Contract

## Purpose

Handoff authority proves which repository state governs. Continuity provenance
proves which actor or session changed that state, which base commit it used,
which paths changed, and which claims or unresolved tasks were transferred.

Cross-repository reference sets replace prose-only dependencies with pinned
source commits and content hashes.

## Repository surfaces

```text
.continuity/config.json
.continuity/change-records/<change-id>.json
.continuity/cross-repository-references.json
```

## Session change invariant

Every enforced change identifies:

```text
repository
base commit
actor class and instance
governing handoff path and content hash
complete changed-path inventory
per-path content hashes
implemented claims
unresolved tasks
deterministic record hash
```

The change-record file itself is excluded from its changed-path inventory to
avoid a self-hash cycle. The verifier compares all other declared paths against
the Git diff from `base_commit` to `HEAD`.

An undeclared changed path produces `DENY`.

## Cross-repository reference invariant

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

The reference object does not grant destination custody, execution authority,
admissibility, release, publication, or deployment.

## Decisions

```text
ALLOW       provenance and required references verified
DENY        declared state is contradictory or incomplete
FAIL_CLOSED required continuity evidence cannot be read or evaluated
```

Only `ALLOW` may proceed into standing and task selection.

## Hosted use

The reusable workflow checks out the caller repository with full Git history,
retrieves the validator from an immutable workflows commit, verifies the Git
change set, and retains a deterministic receipt artifact.
