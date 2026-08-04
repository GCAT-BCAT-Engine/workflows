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
receipts, declared scoped handoffs, and verified session change records override
historical chat claims.

## Role

`GCAT-BCAT-Engine/workflows` owns reusable construction, validation, hosted
orchestration, cross-repository verification, handoff authority enforcement,
and continuity-provenance verification workflows.

It does not grant runtime authority, destination custody, publication
acceptance, or deployment merely because a workflow completed.

## Current installed files

```text
.handoff/current.json
.continuity/config.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-001.json
.continuity/cross-repository-references.json
.github/workflows/handoff-authority.yml
.github/workflows/handoff-authority-reusable.yml
.github/workflows/continuity-provenance.yml
.github/workflows/continuity-provenance-reusable.yml
tools/handoff_authority.py
tools/continuity_provenance.py
tests/test_handoff_authority.py
tests/test_continuity_provenance.py
schemas/session-change-record.schema.json
schemas/cross-repository-reference-set.schema.json
docs/HANDOFF_ORCHESTRATION_CONTRACT.md
docs/CONTINUITY_PROVENANCE_CONTRACT.md
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
  -> .handoff/current.json
  -> governing handoff hash and profile verification
  -> handoff authority receipt
  -> .continuity/config.json
  -> commit-bound session change record
  -> complete changed-path and per-path hash verification
  -> required cross-repository reference verification
  -> continuity provenance receipt
  -> existing standing and task orchestration
  -> completed adoption registry
  -> Master Records bounded custody
```

The reusable workflows verify caller repositories in the caller checkout
context. This avoids requiring the public workflows repository to hold private
cross-organization read credentials.

## Done state for this repo

The handoff-authority lane is complete when each reviewed repository declares
one repository-wide governing handoff, all authority workflows return `ALLOW`,
the completed registry is retained, and Master Records accepts bounded custody.
Those conditions are satisfied.

The continuity-provenance lane is complete for this repository when:

1. its current change is bound to an exact base commit;
2. the actor and session instance are declared;
3. every non-exempt changed path is inventoried with a content hash;
4. the governing handoff hash matches repository content;
5. required external references are pinned to source commits and content
   hashes with verification evidence;
6. the Git diff matches the declared path inventory; and
7. the hosted provenance workflow returns `ALLOW`.

The older reusable sandbox-builder goal remains a separate unfinished
construction-plane goal and is not falsely marked complete by this work.

## Completed in latest pass

Handoff authority and custody:

```text
portable handoff authority verifier installed
six-repository reviewed corpus normalized
all seven hosted authority gates returned ALLOW
completed registry commit: dc0ab5077eafd3d57a6b9044c9e335424575a66f
completed registry run: 30958489248 — success
Master Records custody commit: 5cc259d414fb21fb94914ae244fdd033f3115b76
Master Records custody run: 30958850868 — success
custody decision: ACCEPTED_FOR_CUSTODY
authority effect: NONE
source-side custody record commit: aafa0fd002285da91a937c6dcf7a212351cc51be
source-side authority run: 30958998198 — success
```

Continuity provenance installation:

```text
commit-bound session change record schema installed
hash-pinned cross-repository reference schema installed
stdlib provenance validator installed
8 provenance tests prepared
local and reusable hosted provenance workflows installed
machine-owned SV-COST paths explicitly exempted, not silently ignored
portable handoff verifier reference pinned to commit and Git blob
Master Records custody reference pinned to commit and Git blob
```

## Remaining work

```text
observe hosted provenance workflow success for this installation
pin downstream callers to the immutable provenance implementation commit
adopt .continuity surfaces in the reviewed six-repository corpus
transfer released provenance receipts into Master Records custody
normalize Master Records repository-wide handoff authority
apply both reusable gates to additional ecosystem repositories
complete the pre-existing repository-agnostic sandbox builder
```

Separate existing workflow failures remain outside the handoff-authority and
continuity-provenance results and must remain owned by their applicable
repository handoffs.

No favorable general StegVerse savings claim is admitted by this handoff.
SV-COST issue `#13` remains the scoped owner of future ROI evidence.

## Destination installs

```text
Handoff authority:
  StegVerse-002/micro-node-runtime — COMPLETE
  StegVerse-002/StegGuardian — COMPLETE
  StegVerse-002/StegProfile — COMPLETE
  StegVerse-002/core-lite — COMPLETE
  StegVerse-002/admissibility-gateway — COMPLETE
  StegVerse-002/capability-registry — COMPLETE
  GCAT-BCAT-Engine/workflows — COMPLETE HOST
  master-records/orchestration — COMPLETE BOUNDED CUSTODY

Continuity provenance:
  GCAT-BCAT-Engine/workflows — IMPLEMENTED; HOSTED VALIDATION PENDING
  reviewed six-repository corpus — PENDING ADOPTION
  master-records/orchestration — PENDING PROVENANCE CUSTODY
```

## Next task

Validate this repository's commit-bound provenance record. After `ALLOW`, pin
consumer workflows to the resulting immutable commit, adopt the provenance
contract across the reviewed corpus, and then begin the decision-contract,
plane-boundary, and ingress-hardening workstreams under both verified gates.
