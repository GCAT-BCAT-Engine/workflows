# GCAT-BCAT-Engine/workflows Mirror Handoff

## Source of truth

This document is the single repository-wide current handoff for
`GCAT-BCAT-Engine/workflows`. Machine authority is declared in
`.handoff/current.json`, and the current commit-bound transition is declared in
`.continuity/config.json`.

Goal-specific handoffs remain active only as scoped lanes:

```text
SV_COST_MIRROR_HANDOFF.md
docs/TEN_ADVANCES_COST_ESTIMATION_MIRROR_HANDOFF.md
docs/GOVERNED_RESEARCH_ENGINE_HANDOFF.md
```

Live default-branch state, Git history, workflow runs, artifacts, receipts,
verified change records, and validated adoption registries override historical
chat claims.

## Role

`GCAT-BCAT-Engine/workflows` owns reusable construction, validation, hosted
orchestration, handoff-authority enforcement, read-only handoff-semantic
reconciliation, continuity-provenance validation, and cross-repository
adoption registries.

Workflow completion is evidence. It is not runtime authority, destination
custody, publication acceptance, deployment, repair authority, or irreversible
execution.

## Current installed files

```text
.handoff/current.json
.continuity/config.json
.continuity/cross-repository-references.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-001.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-002.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-003.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-004.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-005.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-006.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-007.json
.github/workflows/handoff-authority.yml
.github/workflows/handoff-authority-reusable.yml
.github/workflows/handoff-semantics.yml
.github/workflows/handoff-semantics-reusable.yml
.github/workflows/continuity-provenance.yml
.github/workflows/continuity-provenance-reusable.yml
tools/handoff_authority.py
tools/handoff_semantics.py
tools/continuity_provenance.py
tests/test_handoff_authority.py
tests/test_handoff_semantics.py
tests/test_continuity_provenance.py
config/handoff-field-authority.format-a-v1.json
schemas/handoff-field-authority.schema.json
schemas/handoff-conformance-receipt.schema.json
schemas/handoff-state-delta-receipt.schema.json
schemas/handoff-reconciliation-receipt.schema.json
schemas/session-change-record.schema.json
schemas/cross-repository-reference-set.schema.json
docs/HANDOFF_ORCHESTRATION_CONTRACT.md
docs/HANDOFF_SEMANTIC_RECONCILIATION_CONTRACT.md
docs/CONTINUITY_PROVENANCE_CONTRACT.md
docs/WORKFLOWS_MIRROR_HANDOFF.md
data/handoff-authority-adoption.json
data/continuity-provenance-adoption.json
data/handoff-semantic-adoption.json
SV_COST_MIRROR_HANDOFF.md
docs/TEN_ADVANCES_COST_ESTIMATION_MIRROR_HANDOFF.md
docs/GOVERNED_RESEARCH_ENGINE_HANDOFF.md
```

## Current working path

```text
repository event
  -> governing handoff authority ALLOW
  -> Format A conformance
  -> repository-authoritative state comparison
  -> bounded reconciliation receipt
  -> commit-bound session change record
  -> complete Git-diff and per-path hash verification
  -> required cross-repository reference verification
  -> continuity provenance ALLOW
  -> standing and next-node selection
  -> validated adoption registry
  -> Master Records bounded custody
```

Reusable workflows verify caller repositories in the caller checkout context
and are pinned by consumers to immutable implementation commits.

## Done state for this repo

Handoff authority, the reusable semantic host, and continuity provenance are
installed and validated when:

1. exactly one governing handoff is verified;
2. Format A conformance and repository-state deltas are separate receipts;
3. intent and task fields are never mechanically reconciled;
4. bounded-loop exhaustion and oscillation fail closed;
5. repair remains disabled;
6. reusable execution occurs in the caller checkout;
7. host authority, semantic, and provenance workflows return `ALLOW`; and
8. at least one repository pilot reaches a retained zero-delta fixed point.

All eight conditions are satisfied.

## Completed in latest pass

Portable semantic source:

```text
repository: StegVerse-002/micro-node-runtime
commit: c0630fab9759d1a4e9cb62b3ba13ff818cf819f3
semantic run: 30961106607 — success
provenance run: 30961106954 — success
```

Reusable semantic host:

```text
commit: ec8dc192617b4f145ccfe850d58a9cb803016d19
authority run: 30962541372 — success
semantic run: 30962541426 — success
provenance run: 30962541361 — success
repair mode: READ_ONLY
```

The two prior host failures remain retained in records `004` and `005` as
integration evidence. Record `006` removed the private-source dependency without
weakening semantic rules.

Capability-registry pilot:

```text
repository: StegVerse-002/capability-registry
commit: 44dbee72e856adeb4f3572fb92be2145b0bdf4b6
authority run: 30963084750 — success
semantic run: 30963084736 — success
provenance run: 30963084782 — success
conformance deltas: 0
state deltas: 0
reconciliation: FIXED_POINT_REACHED
repair_enabled: false
artifact digest: sha256:fe89cc16d624169e311bde9e65f44ab5329453fcd36fc1c2338d6162d8821f40
semantic receipt: 816a14db19ffecf1a3bb2eb920d3aaa75838f85862082d0c4353cccf6ee2879e
```

The pilot also exposed and corrected a stale scoped-handoff pointer before
semantic evaluation. Canonical `.github` paths and the capability task queue
were preserved.

```text
data/handoff-semantic-adoption.json — INSTALLED
.continuity/cross-repository-references.json — PILOT EVIDENCE PINNED
```

## Remaining work

```text
Propagate the read-only semantic gate to StegGuardian, StegProfile, core-lite, and admissibility-gateway.
Retain additional zero-delta or typed-delta measurements.
Transfer released semantic evidence into Master Records custody.
Design governed repair proposals and an append-only repair ledger only after additional measurements.
Make applicable authority, semantic, and provenance gates prerequisites for Runtime Orchestrator dispatch.
Continue canonical decision-contract, plane-boundary, and candidate-ingress workstreams separately.
Complete the pre-existing repository-agnostic sandbox builder.
```

No favorable general StegVerse savings claim is admitted by this handoff.

## Destination installs

```text
Handoff authority:
  reviewed corpus — COMPLETE
  GCAT-BCAT-Engine/workflows — COMPLETE HOST
  master-records/orchestration — COMPLETE BOUNDED CUSTODY

Continuity provenance:
  GCAT-BCAT-Engine/workflows — COMPLETE HOST
  reviewed corpus — COMPLETE HOSTED ADOPTION
  master-records/orchestration — PENDING PROVENANCE CUSTODY

Handoff semantics:
  StegVerse-002/micro-node-runtime — PORTABLE SOURCE COMPLETE
  GCAT-BCAT-Engine/workflows — REUSABLE HOST COMPLETE
  StegVerse-002/capability-registry — READ-ONLY FIXED-POINT PILOT COMPLETE
  StegVerse-002/StegGuardian — PENDING READ-ONLY
  StegVerse-002/StegProfile — PENDING READ-ONLY
  StegVerse-002/core-lite — PENDING READ-ONLY
  StegVerse-002/admissibility-gateway — PENDING READ-ONLY
  master-records/orchestration — SEMANTIC CUSTODY PENDING
```

## Next task

Accept the released capability-registry semantic evidence into bounded Master
Records custody, then extend the pinned read-only gate to the remaining Format A
repositories. Do not enable repair until the additional measurements and repair
proposal contract are retained.
