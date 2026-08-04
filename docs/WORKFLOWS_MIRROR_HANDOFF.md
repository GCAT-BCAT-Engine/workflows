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
.continuity/change-records/SV-CONT-20260804-PROVENANCE-002.json
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

The continuity-provenance host lane is complete when:

1. its changes are bound to exact base commits;
2. actor and session instances are declared;
3. every non-exempt changed path is inventoried with a content hash;
4. governing handoff hashes match repository content;
5. required external references are pinned to source commits and content hashes
   with verification evidence;
6. Git diffs match the declared path inventories;
7. the hosted provenance workflow returns `ALLOW`; and
8. a successor transition is itself completed through a new verified change
   record rather than by mutating the first record.

Those host conditions are satisfied through provenance records `001` and `002`.
The older reusable sandbox-builder goal remains a separate unfinished
construction-plane goal and is not falsely marked complete by this work.

## Completed in latest pass

Handoff authority and custody:

```text
reviewed six-repository handoff corpus normalized
completed registry commit: dc0ab5077eafd3d57a6b9044c9e335424575a66f
completed registry run: 30958489248 — success
Master Records custody commit: 5cc259d414fb21fb94914ae244fdd033f3115b76
Master Records custody run: 30958850868 — success
custody decision: ACCEPTED_FOR_CUSTODY
authority effect: NONE
source-side custody record commit: aafa0fd002285da91a937c6dcf7a212351cc51be
source-side authority run: 30958998198 — success
```

Continuity provenance host:

```text
implementation commit: a79134d666cd784a10d28fa62dd43e170fd62c77
handoff authority run: 30959696225 — success
continuity provenance run: 30959696236 — success
change record 001 hash: fcf007e1154cf178fb58951da13b8046667c1649e7168b2b836c7b03ac06f383
changed paths in record 001: 12
required external references: 2, both VERIFIED
stdlib provenance tests: 8 passed in hosted workflow
```

The successor validation-closure transition is recorded separately in
`SV-CONT-20260804-PROVENANCE-002.json`, proving that completed validation did not
silently rewrite or invalidate record `001`.

## Remaining work

```text
pin downstream callers to immutable provenance implementation commit a79134d666cd784a10d28fa62dd43e170fd62c77
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
  reviewed six-repository corpus — COMPLETE
  GCAT-BCAT-Engine/workflows — COMPLETE HOST
  master-records/orchestration — COMPLETE BOUNDED CUSTODY

Continuity provenance:
  GCAT-BCAT-Engine/workflows — COMPLETE HOST
  reviewed six-repository corpus — PENDING ADOPTION
  master-records/orchestration — PENDING PROVENANCE CUSTODY
```

## Next task

Pin consumer workflows to provenance implementation commit `a79134d…`, adopt
the contract across the reviewed corpus, and then begin the decision-contract,
plane-boundary, and ingress-hardening workstreams under both verified gates.
