# StegVerse Test Lanes Mirror Handoff

Updated: 2026-08-18T15:00:00-05:00

## Active goal and authority

```text
goal_id: STEGVERSE-TEST-LANES-001
repository: GCAT-BCAT-Engine/workflows
branch: main
canonical_task_state: experiments/stegverse-test-lanes/task-state.json
credential_authority: TV/TVC
consumer_credential_authority: NONE
primary_provider: stegverse_local
third_party_role: CONTROL_OR_FALLBACK_ONLY
NON-TV/TVC secret/token allowed: false
claim_state: SOURCE_IMPLEMENTED_AUTOLAUNCH_INTEGRATED_REQUIRED_LIVE_EXECUTION_PENDING
archive_state: PROHIBITED_UNTIL_REQUIRED_RUNTIME_OUTCOME_IS_TERMINAL
```

This handoff is canonical for portable Test Lanes planning, sovereign-primary candidate adaptation, candidate-to-lane evidence construction and deterministic comparison. It creates no credential store, provider broker, route authority, model authority or heartbeat authority.

## Governing invariants

**Experiments are portable; credentials are not. Binding state is observed, not asserted. StegVerse-local is PRIMARY.**

Portable experiments carry task/model intent, capsule IDs and evidence contracts; they never carry API keys, bearer tokens or TVC vault refs. External providers remain `CONTROL_OR_FALLBACK_ONLY`. Portable/noncanonical runs may skip optional unavailable controls; the specifically named canonical full-nine-lane autolaunch is stricter and requires all nine logical lanes before it may call itself a 9/9 run.

## Canonical reference experiment

`manifests/sv-cost-nine-lane.v1.json` binds `SV-RECON-001` Git blob `1bd5a640bf067ffad87c427a5c12cb57c029b214`.

```text
9 logical lanes
5 candidate executions

1 StegVerse PRIMARY/reference
1 OpenAI candidate    -> RAW + GOVERNED
1 Anthropic candidate -> RAW + GOVERNED
1 DeepSeek candidate  -> RAW + GOVERNED
1 Kimi candidate      -> RAW + GOVERNED
```

RAW/GOVERNED pairs use the exact same provider candidate.

## Implemented portable planning/evidence source

```text
f097a9aab819471e3ea41c84d5b905968bd1c50c  manifest schema
a6521d4baafe48c44bd0f3b7bdb40313e0dede13  nine-lane manifest
81d8bd35e2a13fb023693f2b6dea2829aeab4071  planner/execution-group sharing
5bb043b6c435553947a2003ceb31a4c94825d648  planner tests
ca2dff6df1dd31f074238e5bfa1a4813f50e6687  generic lane-evidence schema
d34130b79929ae4379ecfd5b4de8f67af1d31b34  deterministic comparator
110de1013bc3b2649538b81fa6b495e60910c019  comparator tests
```

## Sovereign PRIMARY Test-Lane adapter — IMPLEMENTED

```text
462b829abb1f09516dadef4e41a41c494aa62a4f  run_stegverse_primary_candidate.py
 d57d43c29f7657b77d3a5a8c061c3e90d6e6d1d5  stdlib primary-runner tests
```

The adapter consumes an **already-live** StegVerse loopback endpoint. It cannot launch or authorize the model. It verifies exact plan/group/task hashes, `stegverse-reference-lm-v1`, loopback-only health, `private_endpoint_only=true`, `credential_requirement=NONE`, `third_party_inference_required=false` and `authority_effect=NONE`. It emits a sanitized PRIMARY candidate with measured latency and usage.

The sovereign runtime itself remains owned by:

`StegVerse-002/micro-node-runtime -> StegVerse-Labs/.github#60/G18 -> TVC -> StegVerse-org/LLM-adapter -> Master Records`.

## External controls — TVC-owned

Canonical external execution remains:

```text
StegVerse-Labs/TVC/scripts/tvc_materialize_provider_capsule_bindings.py
StegVerse-Labs/TVC/scripts/tvc_resolve_test_lane_capsules.py
StegVerse-Labs/TVC/scripts/tvc_issue_test_lane_lease.py
StegVerse-Labs/TVC/scripts/tvc_run_test_lane_external_candidate.py
```

Live vault readiness derives BOUND/UNBOUND. Static `BOUND` is not live evidence. The external runner accepts no API key; the existing TVC vault broker resolves the actual provider secret at the provider-use boundary.

## Candidate -> nine lane evidence — IMPLEMENTED

```text
83fad5f1fa0e560ea42090bbfcb2ca4fdab4f2b2  build_lane_evidence.py
aa94e8d443a4768f4bf0ce1b28a43c5617454a29  nine-evidence/comparator tests
a1739fe5940a1597e2114a6c63da46f040b74fef  stdlib validation workflow hook
```

The builder accepts one StegVerse PRIMARY candidate plus four TVC external candidates and produces exactly nine `stegverse.test-lane-evidence.v1` records. RAW/GOVERNED evidence for each external provider retains the same candidate output/hash; GOVERNED adds deterministic `stegverse.default-governed.v1` output-boundary evidence. The existing comparator must then return `PASS` with `lane_evidence_count=9`.

## Canonical 9/9 heartbeat autolaunch — INSTALLED, LIVE EXECUTION PENDING

Owner: `StegVerse-Labs/.github` task `STEGVERSE-TEST-LANES-AUTOLAUNCH-001`.

Canonical surfaces:

```text
StegVerse-Labs/.github/docs/STEGVERSE_TEST_LANES_AUTOLAUNCH_MIRROR_HANDOFF.md
StegVerse-Labs/.github/handoffs/STEGVERSE-TEST-LANES-AUTOLAUNCH-001.json
StegVerse-Labs/.github/control/test-lanes-autolaunch-matrix.v1.json
StegVerse-Labs/.github/control/worker-registry.d/test-lanes-autolaunch.json
StegVerse-Labs/.github/control/process-worker-adapters.d/test-lanes-autolaunch.json
StegVerse-Labs/.github/workers/test_lanes_autolaunch_entrypoint.py
StegVerse-Labs/.github/workers/test_lanes_autolaunch_worker.py
```

The carrier only wakes/references. v12 emits a non-authorizing assignment trigger for a `HANDOFF_READY` task; WorkerCoordinator independently validates authority, chooses the exact worker, creates the fresh claim/fence and invokes it. The autolaunch matrix requires HB30+/WorkerCoordinator proof, same-execution sovereign activation, primary health/model proof, TVC route, TV/TVC-only credential authority, all four live external capsule groups, explicit non-secret external model selection, exact manifest/task/plan identities, nine ready logical lanes, five ready execution groups, runtime-safe source validation, a writable evidence sink and no conflicting execution claim.

For this named canonical full 9/9 run, all four external groups must be READY. This does **not** change the general Test Lanes rule that third-party providers are optional controls/fallbacks and never sovereign prerequisites.

## External model identity boundary

Historical Gen-2 candidate records are not uniformly usable API identifiers: OpenAI records `gpt-5.6-sol`, while other historical records include UI labels or unspecified UI identity. Therefore autolaunch does not guess or translate those labels. Exact model selection is a non-secret local runtime input (`stegverse.test-lanes-model-selection/v1`) and is independently checked by TVC provider/capsule policy before provider access.

## Validation state

```text
portable source/tests: INSTALLED
sovereign PRIMARY adapter/tests: INSTALLED
candidate->nine-evidence builder/tests: INSTALLED
stdlib validation workflow: INSTALLED
hosted validation directly observed for latest heads: NO
live HB30+/WorkerCoordinator: NOT_YET_OBSERVED
live sovereign PRIMARY Test-Lane candidate: NOT_YET_OBSERVED
live four-provider TVC candidate set: NOT_YET_OBSERVED
live nine-lane evidence bundle: NOT_YET_OBSERVED
live deterministic comparison PASS: NOT_YET_OBSERVED
```

No source, task, handoff, assignment or workflow state is treated as runtime completion.

## Collision boundaries

1. Do not duplicate the local model/runtime, G18 heartbeat/WorkerCoordinator activation, TVC vault, provider broker or lease authority.
2. Do not put credentials/vault refs into portable Test Lanes.
3. Do not promote third-party providers to PRIMARY.
4. Do not label a partial run as the canonical 9/9 run.
5. Do not treat static capsule state, a plan, a handoff, a machine assignment or workflow success as live execution evidence.
6. Do not mutate immutable Generation-2 evidence.

## Exact continuation

1. G18 must produce/validate the separated HB30+ carrier and WorkerCoordinator observation.
2. The autolaunch registry fragment must be projected by WorkerCoordinator; a later carrier emits its non-authorizing assignment trigger and WorkerCoordinator binds the fresh claim/fence.
3. Desired external credentials must become live through TV/TVC; no key enters Test Lanes or the autolaunch worker.
4. Exact external API model IDs must be available through the non-secret local model-selection contract and admitted by TVC.
5. The matrix worker remains BLOCKED until every canonical 9/9 predicate passes.
6. The worker then runs one StegVerse PRIMARY candidate plus four TVC candidates, builds nine lane evidence records and requires comparator PASS.
7. Preserve the terminal receipt and propagate to Master Records/required publication surfaces only after direct runtime evidence exists.

## Completion accounting

```text
required Test Lanes source/control surfaces: 11/11 implemented
scaffolding/stubs: 0
missing source files: 0
validation mechanisms installed: 6/6
hosted validation directly observed: 0/1
live integration predicates: 0/5
source implementation: 100%
goal activation: 68%
archive readiness: 0% while required runtime/test outcome remains nonterminal
```
