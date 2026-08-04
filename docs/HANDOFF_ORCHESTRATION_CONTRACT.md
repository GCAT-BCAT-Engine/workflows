# Handoff Orchestration Contract

## Boundary

Continuity authority is the verified-state admission stage inside the existing
Runtime Orchestrator. It determines which repository handoff governs and
whether that handoff matches repository state. It does not select or execute a
task.

The Runtime Orchestrator may determine standing and select a next node only
after handoff authority returns `ALLOW`.

## Repository contract

Each governed repository carries:

```text
.handoff/current.json
one repository-wide current handoff
zero or more explicitly scoped handoffs
dated or SESSION_ARCHIVE_ historical handoffs
a hosted authority workflow
```

A repository must not infer source-of-truth authority from traversal order,
file modification time, file length, or prose in an undeclared document.

## Reusable workflow

Call:

```yaml
jobs:
  handoff-authority:
    uses: GCAT-BCAT-Engine/workflows/.github/workflows/handoff-authority-reusable.yml@main
    with:
      repository: owner/repository
```

Callers should replace `@main` with an immutable release tag or commit after the
first tagged contract release.

The called workflow checks out the caller repository, retrieves the public
stdlib verifier, verifies the declared repository identity, and uploads the
deterministic authority receipt.

## Decisions

- `ALLOW`: one repository-wide governing handoff is proven.
- `DENY`: a declared invariant is violated.
- `FAIL_CLOSED`: required authority evidence cannot be read or evaluated.

Only `ALLOW` admits standing evaluation, task selection, release, or
propagation.

## Scope

Goal-specific, private, research, cost, integration, and session handoffs may
remain active, but each must be declared as scoped. A scoped handoff cannot
supersede the repository-wide current handoff.

## Custody

Per-repository workflow success is execution evidence. Master Records custody
is a separate downstream transition and must retain the repository commit,
manifest hash, current handoff hash, authority receipt hash, workflow run, and
decision.
