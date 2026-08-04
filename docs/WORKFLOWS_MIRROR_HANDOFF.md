# GCAT-BCAT-Engine/workflows Mirror Handoff

## Source of truth

This document is the single repository-wide current handoff for
`GCAT-BCAT-Engine/workflows`. Machine authority is declared in
`.handoff/current.json`.

Goal-specific handoffs remain active only as scoped lanes:

```text
SV_COST_MIRROR_HANDOFF.md
docs/TEN_ADVANCES_COST_ESTIMATION_MIRROR_HANDOFF.md
docs/GOVERNED_RESEARCH_ENGINE_HANDOFF.md
```

Live default-branch state, Git history, workflow runs, artifacts, issues,
receipts, and declared scoped handoffs override historical chat claims.

## Role

`GCAT-BCAT-Engine/workflows` owns reusable construction, validation, hosted
orchestration, and cross-repository verification workflows.

It does not grant runtime authority, destination custody, publication
acceptance, or deployment merely because a workflow completed.

## Current installed files

```text
.handoff/current.json
.github/workflows/handoff-authority.yml
.github/workflows/handoff-authority-reusable.yml
tools/handoff_authority.py
tests/test_handoff_authority.py
docs/HANDOFF_ORCHESTRATION_CONTRACT.md
docs/WORKFLOWS_MIRROR_HANDOFF.md
data/handoff-authority-adoption.json
SV_COST_MIRROR_HANDOFF.md
docs/TEN_ADVANCES_COST_ESTIMATION_MIRROR_HANDOFF.md
docs/GOVERNED_RESEARCH_ENGINE_HANDOFF.md
```

Existing provider, sandbox, validation, research, cost, and session-
consolidation workflows remain installed and retain their scoped ownership.

## Current working path

```text
repository event
  -> caller repository checkout
  -> .handoff/current.json
  -> governing handoff hash and profile verification
  -> duplicate/scoped/archive checks
  -> deterministic authority receipt
  -> existing standing and task orchestration
```

The reusable workflow verifies the caller repository in the caller context.
This avoids requiring the public workflows repository to hold private
cross-organization read credentials.

## Done state for this repo

The handoff-authority lane is complete when:

1. this repository verifies its own governing handoff;
2. the reusable workflow can be called by another repository;
3. duplicate current handoffs return `DENY`;
4. missing authority manifests return `FAIL_CLOSED`;
5. authority receipts are deterministic;
6. adopted repositories record their commit and hosted workflow evidence; and
7. orchestration consumes only an `ALLOW` authority result.

The older reusable sandbox-builder goal remains a separate unfinished
construction-plane goal and is not falsely marked complete by this work.

## Completed in latest pass

```text
portable stdlib authority verifier installed
repository-wide authority manifest installed
local release-blocking workflow installed
reusable caller-side workflow installed
format-A repository handoff established
scoped program handoffs explicitly declared
adoption registry installed
```

First adoption wave:

```text
StegVerse-002/micro-node-runtime — COMPLETE
StegVerse-002/StegGuardian — COMPLETE
StegVerse-002/StegProfile — COMPLETE
```

## Remaining work

```text
Adopt the reusable gate in:
  StegVerse-002/core-lite
  StegVerse-002/admissibility-gateway
  StegVerse-002/capability-registry

Then:
  add signed or hash-pinned cross-repository references
  add session-change provenance contracts
  transfer released receipts into Master Records
  complete the pre-existing repository-agnostic sandbox builder
```

No favorable general StegVerse savings claim is admitted by this handoff.
SV-COST issue `#13` remains the scoped owner of future ROI evidence.

## Destination installs

```text
StegVerse-002/micro-node-runtime — COMPLETE
StegVerse-002/StegGuardian — COMPLETE
StegVerse-002/StegProfile — COMPLETE
StegVerse-002/core-lite — PENDING
StegVerse-002/admissibility-gateway — PENDING
StegVerse-002/capability-registry — PENDING
master-records/orchestration — PENDING CUSTODY
```

## Next task

Install `.handoff/current.json` and a caller of
`.github/workflows/handoff-authority-reusable.yml` in core-lite,
admissibility-gateway, and capability-registry. Do not start centralized
correction orchestration in a repository whose authority result is not
`ALLOW`.
