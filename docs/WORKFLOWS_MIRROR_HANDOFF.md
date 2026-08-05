# GCAT-BCAT-Engine/workflows Mirror Handoff

## Source of truth

This document is the single repository-wide current handoff for
`GCAT-BCAT-Engine/workflows`. Machine authority is declared in
`.handoff/current.json`; the current commit-bound transition is declared in
`.continuity/config.json`.

Scoped program lanes remain subordinate:

```text
SV_COST_MIRROR_HANDOFF.md
docs/TEN_ADVANCES_COST_ESTIMATION_MIRROR_HANDOFF.md
docs/GOVERNED_RESEARCH_ENGINE_HANDOFF.md
```

The execution inventory for the originating handoff-orchestration session is:

```text
data/session-consolidation/handoff-orchestration-session-20260804.json
```

Live default-branch state, Git history, workflow runs, retained artifacts,
receipts, custody records, validated change records, and verified adoption
registries override historical chat claims.

## Role

This repository owns reusable handoff authority, read-only semantic
reconciliation, continuity provenance, cross-repository adoption registries,
and session-consolidation coordination.

Workflow success is evidence. It is not execution, admissibility, custody,
repair, release, publication, deployment, or irreversible-transition authority.

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
.continuity/change-records/SV-CONT-20260804-PROVENANCE-008.json
.github/workflows/handoff-authority.yml
.github/workflows/handoff-authority-reusable.yml
.github/workflows/handoff-semantics.yml
.github/workflows/handoff-semantics-reusable.yml
.github/workflows/continuity-provenance.yml
.github/workflows/continuity-provenance-reusable.yml
tools/handoff_authority.py
tools/handoff_semantics.py
tools/continuity_provenance.py
tools/verify_handoff_semantic_adoption.py
tests/test_handoff_authority.py
tests/test_handoff_semantics.py
tests/test_continuity_provenance.py
tests/test_handoff_semantic_adoption.py
config/handoff-field-authority.format-a-v1.json
schemas/handoff-semantic-adoption-registry.schema.json
docs/HANDOFF_ORCHESTRATION_CONTRACT.md
docs/HANDOFF_SEMANTIC_RECONCILIATION_CONTRACT.md
docs/CONTINUITY_PROVENANCE_CONTRACT.md
docs/WORKFLOWS_MIRROR_HANDOFF.md
data/handoff-authority-adoption.json
data/continuity-provenance-adoption.json
data/handoff-semantic-adoption.json
data/session-consolidation/handoff-orchestration-session-20260804.json
```

## Current working path

```text
repository event
  -> governing handoff authority ALLOW
  -> Format A conformance
  -> repository-authoritative state comparison
  -> bounded read-only reconciliation
  -> commit-bound Git-diff and content-hash verification
  -> required cross-repository reference verification
  -> continuity provenance ALLOW
  -> reviewed adoption-registry verification
  -> standing and next-node selection
  -> bounded Master Records custody
```

Reusable workflows execute in the caller checkout and are pinned by consumers
to immutable host commits.

## Done state for this repo

The continuity foundation is complete when:

1. one governing handoff is machine verified;
2. authority, conformance, state delta, reconciliation, and provenance remain
   separate receipts;
3. intent and task fields are not mechanically reconciled;
4. bounded-loop exhaustion and oscillation fail closed;
5. repair remains disabled;
6. reusable execution occurs in caller context;
7. all five reviewed Format A repositories reach `COMPLETE_READ_ONLY`;
8. the central registry rejects incomplete, duplicate, tampered, non-ALLOW, or
   repair-enabled corpus state;
9. released evidence is hash-pinned; and
10. unresolved session goals have exact owners and durable locations.

Conditions 1–10 are installed. Hosted validation of transition `008` is the
current activation check.

## Completed in latest pass

Core host and source:

```text
portable source: StegVerse-002/micro-node-runtime@c0630fab9759d1a4e9cb62b3ba13ff818cf819f3
reusable host: ec8dc192617b4f145ccfe850d58a9cb803016d19
host authority run: 30962541372 — success
host semantic run: 30962541426 — success
host provenance run: 30962541361 — success
repair mode: READ_ONLY
governed repair: NOT_AUTHORIZED
```

Reviewed semantic corpus:

```text
StegVerse-002/capability-registry — COMPLETE_READ_ONLY
StegVerse-002/StegGuardian — COMPLETE_READ_ONLY
StegVerse-002/StegProfile — COMPLETE_READ_ONLY
StegVerse-002/core-lite — COMPLETE_READ_ONLY
StegVerse-002/admissibility-gateway — COMPLETE_READ_ONLY
conformance deltas: 0 across 5/5
state deltas: 0 across 5/5
reconciliation: FIXED_POINT_REACHED across 5/5
repair_enabled: false across 5/5
```

StegGuardian's initial DENY remains retained. The correction changed stale
descriptive state claims into exact repository paths; no semantic rule was
weakened.

Existing custody:

```text
handoff authority custody — COMPLETE
continuity provenance custody — COMPLETE
semantic pilot custody — COMPLETE
semantic custody run: 30963744926 — success
authority_effect: NONE
repair_authority: NOT_AUTHORIZED
```

Transition `008` adds:

```text
five-repository semantic registry
deterministic registry verifier and four negative/positive stdlib tests
nine hash-pinned required cross-repository references
complete session execution inventory with zero unassigned tasks
```

## Remaining work

```text
Accept the five-repository registry through a new bounded Master Records custody transition.
Install authority-plus-provenance verified-state admission at Runtime Orchestrator event intake and direct next-node selection.
Retain additional read-only measurements before any governed repair proposal.
Continue decision-envelope, plane-boundary, candidate-ingress, and portable-consumer work only through the exact canonical owners recorded in the session inventory.
Complete the pre-existing repository-agnostic sandbox builder under its existing owner.
```

Decision vocabulary, plane boundary, candidate ingress, consumer tests, and
publication are adjacent canonical workstreams. They are not completion claims
of semantic reconciliation.

## Destination installs

```text
reviewed handoff authority corpus — COMPLETE
reviewed continuity-provenance corpus — COMPLETE
reviewed read-only semantic corpus — COMPLETE
master-records/orchestration authority custody — COMPLETE
master-records/orchestration provenance custody — COMPLETE
master-records/orchestration semantic pilot custody — COMPLETE
master-records/orchestration expanded semantic custody — CLAIMED_FOR_INTEGRATION
StegVerse-002/micro-node-runtime dual-gate dispatch — CLAIMED_FOR_IMPLEMENTATION
GCAT-BCAT-Engine/Publisher and public wikis—no new release claim from this lane
```

## Next task

Validate transition `008`. Then accept the promoted five-repository registry
into bounded Master Records custody and install the dual-gate Runtime
Orchestrator admission boundary. The exact claim, collision, evidence, and
release conditions are in
`data/session-consolidation/handoff-orchestration-session-20260804.json`.
