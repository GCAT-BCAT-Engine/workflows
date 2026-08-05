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

Live default-branch state, Git history, workflow runs, artifacts, issues,
receipts, declared scoped handoffs, verified change records, and validated
adoption registries override historical chat claims.

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
.continuity/change-records/SV-CONT-20260804-PROVENANCE-001.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-002.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-003.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-004.json
.continuity/cross-repository-references.json
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

Handoff authority is complete for the reviewed six-repository corpus and is
accepted for bounded Master Records custody.

Continuity provenance is complete for the host and reviewed corpus. Its
successor record `003` returned `ALLOW` for both authority and provenance.

The semantic host is complete when:

1. the host carries the Format A field-authority table;
2. conformance and repository-state deltas are separate receipts;
3. semantic evaluation runs only after authority `ALLOW`;
4. intent and task fields are never mechanically reconciled;
5. leading-dot display transforms are rejected;
6. bounded-loop exhaustion and oscillation fail closed;
7. the reusable workflow executes in the caller checkout;
8. repair remains disabled; and
9. host authority, semantic, and provenance workflows all return `ALLOW`.

Conditions 1–8 are installed. Condition 9 is the activation gate for successor
record `004`.

## Completed in latest pass

Handoff authority and custody:

```text
reviewed handoff corpus: 6/6 COMPLETE
hosted authority owner: COMPLETE
Master Records custody commit: 5cc259d414fb21fb94914ae244fdd033f3115b76
custody run: 30958850868 — success
custody decision: ACCEPTED_FOR_CUSTODY
authority effect: NONE
```

Continuity-provenance host and corpus:

```text
portable provenance implementation: a79134d666cd784a10d28fa62dd43e170fd62c77
reviewed provenance corpus: 6/6 HOSTED ALLOW
central provenance adoption registry: INSTALLED AND VALIDATED
successor record 003 authority run: 30961056934 — success
successor record 003 provenance run: 30961057019 — success
```

Portable semantic source:

```text
repository: StegVerse-002/micro-node-runtime
commit: c0630fab9759d1a4e9cb62b3ba13ff818cf819f3
semantic workflow run: 30961106607 — success
provenance workflow run: 30961106954 — success
portable semantic verifier blob: 8454e12d6cf659dd38b8a3fdffc072f5cc83086e
local and hosted stdlib semantic tests: 11 passed
```

Semantic host transition:

```text
successor record: SV-CONT-20260804-PROVENANCE-004
Format A parser: installed
multi-source field-authority table: installed
conformance worker: installed
state-delta worker: installed, read-only
fixed-point and loop guard: installed
reusable caller workflow: installed
repair mode: READ_ONLY
hosted validation: pending
```

## Remaining work

```text
observe successor record 004 authority, semantic, and provenance workflow success
pin StegVerse-002/capability-registry to the immutable semantic host commit
correct the known github/workflows display-path defect in capability-registry
retain the first read-only pilot receipts and measured delta result
extend the pilot to the remaining reviewed Format A repositories
accept released semantic evidence into Master Records custody
design governed repair proposals and an append-only repair ledger
make all applicable gates prerequisites for Runtime Orchestrator dispatch
begin canonical decision-contract migration
begin construction/governance plane enforcement
begin candidate-ingress hardening
complete the pre-existing repository-agnostic sandbox builder
```

Unrelated legacy workflow failures remain owned by their applicable repository
handoffs and are not reclassified as authority, semantic, or provenance
failures.

## Destination installs

```text
Handoff authority:
  reviewed corpus — COMPLETE
  GCAT-BCAT-Engine/workflows — COMPLETE HOST
  master-records/orchestration — COMPLETE BOUNDED CUSTODY

Continuity provenance:
  GCAT-BCAT-Engine/workflows — COMPLETE HOST
  reviewed corpus — 6/6 HOSTED ALLOW
  central adoption registry — COMPLETE
  master-records/orchestration — PENDING PROVENANCE CUSTODY

Handoff semantics:
  StegVerse-002/micro-node-runtime — PORTABLE SOURCE COMPLETE
  GCAT-BCAT-Engine/workflows — HOST INSTALLED; VALIDATION PENDING
  StegVerse-002/capability-registry — READ-ONLY PILOT PENDING
  remaining reviewed Format A repositories — PENDING AFTER PILOT
  master-records/orchestration — SEMANTIC CUSTODY PENDING
```

## Next task

After successor record `004` returns `ALLOW` for authority, semantics, and
provenance, pin the capability-registry pilot to that immutable host commit.
Correct only the canonical path defect, preserve all task intent, and retain
the read-only semantic receipts before any repair authority is proposed.
