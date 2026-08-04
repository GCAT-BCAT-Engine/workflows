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
orchestration, handoff-authority enforcement, continuity-provenance validation,
and cross-repository adoption registries.

Workflow completion is evidence. It is not runtime authority, destination
custody, publication acceptance, deployment, or irreversible execution.

## Current installed files

```text
.handoff/current.json
.continuity/config.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-001.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-002.json
.continuity/change-records/SV-CONT-20260804-PROVENANCE-003.json
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
data/continuity-provenance-adoption.json
SV_COST_MIRROR_HANDOFF.md
docs/TEN_ADVANCES_COST_ESTIMATION_MIRROR_HANDOFF.md
docs/GOVERNED_RESEARCH_ENGINE_HANDOFF.md
```

## Current working path

```text
repository event
  -> governing handoff authority ALLOW
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

Continuity provenance is complete for the host and reviewed corpus when:

1. the host proves consecutive successor records without rewriting history;
2. all six repositories bind adoption to exact base commits and actor/session
   declarations;
3. governing handoff hashes and all non-exempt changed paths verify;
4. required validator references are commit- and content-hash-pinned;
5. authority and provenance workflows return `ALLOW` for every repository;
6. one central registry records exact commits, change-record hashes, and run
   identifiers; and
7. CI independently validates the registry and deterministic record hash.

Conditions 1–6 are installed and evidenced. Condition 7 is the activation gate
for successor record `003`.

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

Continuity-provenance host:

```text
portable implementation commit: a79134d666cd784a10d28fa62dd43e170fd62c77
implementation provenance run: 30959696236 — success
successor host commit: 893abee7b959169095af59a0051ac51cd716a68a
successor authority run: 30959846909 — success
successor provenance run: 30959846881 — success
```

Reviewed corpus provenance:

```text
StegVerse-002/micro-node-runtime
  commit: 317479afe0dd63920879677ecadebbdd0edf7c40
  authority run: 30960799498
  provenance run: 30960799786

StegVerse-002/StegGuardian
  commit: 90936c3a8725782cc395794f31f197ca0c4862af
  authority run: 30960467356
  provenance run: 30960467620

StegVerse-002/StegProfile
  commit: 02e53514c08ee4087919eb28d4bb54813d02e5d5
  authority/private-boundary run: 30960579063
  provenance run: 30960579422

StegVerse-002/core-lite
  commit: 18cdef35f07c0a694ac1d6383623a8e01fb00856
  authority run: 30960013770
  provenance run: 30960013822

StegVerse-002/admissibility-gateway
  commit: e6a2be8e4c95d3b4f81cacef992ccdfadddff273
  authority run: 30960176471
  provenance run: 30960176456

StegVerse-002/capability-registry
  commit: 86a5ef2e0880a1d0f0ab8a1e7310d847db26d0b1
  authority run: 30960309037
  provenance run: 30960309044
```

The machine-readable consolidation is
`data/continuity-provenance-adoption.json` with six unique complete repository
entries and deterministic registry hash
`63ffb2eb38e397fe3814c4de7331d7f4a601281cb1e6884842ff4930baeee5c0`.

## Remaining work

```text
observe successor record 003 authority and provenance workflow success
accept the validated provenance registry into Master Records custody
normalize Master Records repository-wide handoff authority
make dual-gate ALLOW a required Runtime Orchestrator dispatch prerequisite
begin canonical decision-contract migration
begin construction/governance plane enforcement
begin candidate-ingress hardening
complete the pre-existing repository-agnostic sandbox builder
```

Unrelated legacy workflow failures remain owned by their applicable repository
handoffs and are not reclassified as authority or provenance failures.

## Destination installs

```text
Handoff authority:
  reviewed corpus — COMPLETE
  GCAT-BCAT-Engine/workflows — COMPLETE HOST
  master-records/orchestration — COMPLETE BOUNDED CUSTODY

Continuity provenance:
  GCAT-BCAT-Engine/workflows — COMPLETE HOST
  reviewed corpus — 6/6 IMPLEMENTED AND HOSTED ALLOW
  central adoption registry — INSTALLED; SUCCESSOR VALIDATION PENDING
  master-records/orchestration — PENDING PROVENANCE CUSTODY
```

## Next task

After successor record `003` returns `ALLOW`, transfer the validated provenance
registry into Master Records custody. Then require both authority and provenance
`ALLOW` receipts before Runtime Orchestrator standing and task dispatch.
