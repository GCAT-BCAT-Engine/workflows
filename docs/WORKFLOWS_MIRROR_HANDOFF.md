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

The reviewed six-repository corpus is complete for handoff authority when:

1. each repository declares exactly one repository-wide current handoff;
2. scoped and archived handoffs cannot compete for authority;
3. each manifest hash matches the declared handoff;
4. each repository's hosted authority workflow returns `ALLOW`;
5. the reusable verifier is pinned to an immutable implementation commit; and
6. the central adoption registry records the commit and workflow evidence.

Those conditions are now satisfied for all six reviewed repositories. The
workflows repository also verifies its own authority state.

The older reusable sandbox-builder goal remains a separate unfinished
construction-plane goal and is not falsely marked complete by this work.

## Completed in latest pass

```text
portable stdlib authority verifier installed
repository-wide authority manifest installed
local release-blocking workflow installed
reusable caller-side workflow installed and pinned by consumers
format-A repository handoff established
scoped program handoffs explicitly declared
six-repository adoption registry completed
all seven hosted authority gates returned ALLOW
```

Validated corpus:

```text
StegVerse-002/micro-node-runtime — COMPLETE — run 30957032618
StegVerse-002/StegGuardian — COMPLETE — run 30957428849
StegVerse-002/StegProfile — COMPLETE — run 30957335435
StegVerse-002/core-lite — COMPLETE — run 30958116917
StegVerse-002/admissibility-gateway — COMPLETE — run 30958198224
StegVerse-002/capability-registry — COMPLETE — run 30958290028
GCAT-BCAT-Engine/workflows — HOST COMPLETE — run 30957952734
```

## Remaining work

The duplicate-current-handoff and ambiguous-authority problem is resolved for
the reviewed corpus. The next continuity-hardening work is distinct:

```text
add hash-pinned cross-repository reference objects
add session-change provenance contracts and receipts
transfer released authority evidence into Master Records custody
apply the reusable gate to additional ecosystem repositories
complete the pre-existing repository-agnostic sandbox builder
```

Separate existing workflow failures remain outside the authority result and are
recorded in `data/handoff-authority-adoption.json` without being misclassified
as handoff-authority failures.

No favorable general StegVerse savings claim is admitted by this handoff.
SV-COST issue `#13` remains the scoped owner of future ROI evidence.

## Destination installs

```text
StegVerse-002/micro-node-runtime — COMPLETE
StegVerse-002/StegGuardian — COMPLETE
StegVerse-002/StegProfile — COMPLETE
StegVerse-002/core-lite — COMPLETE
StegVerse-002/admissibility-gateway — COMPLETE
StegVerse-002/capability-registry — COMPLETE
GCAT-BCAT-Engine/workflows — COMPLETE HOST
master-records/orchestration — PENDING CUSTODY
```

## Next task

Transfer the adoption registry and authority evidence into Master Records,
then add the session-change and cross-repository-reference contracts before
starting the remaining decision-contract, plane-boundary, and ingress-hardening
correction workstreams.
