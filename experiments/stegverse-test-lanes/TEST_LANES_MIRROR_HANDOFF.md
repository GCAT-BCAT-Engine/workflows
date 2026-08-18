# StegVerse Test Lanes Mirror Handoff

Updated: 2026-08-18T11:15:00-05:00

## Active goal

```text
goal_id: STEGVERSE-TEST-LANES-001
originating_session_goal: Allow any StegVerse user to reproduce, modify, add, or remove governed model test lanes using their own locally bound provider relationships without surrendering provider credentials to the experiment.
repository: GCAT-BCAT-Engine/workflows
branch: main
canonical_task_state: experiments/stegverse-test-lanes/task-state.json
canonical_provider_authority: StegVerse-Labs/TVC
canonical_provider_capsule: StegVerse-Labs/TVC/docs/PROVIDER_CAPSULE_MIRROR_HANDOFF.md
canonical_provider_precedence: StegVerse-Labs/TVC/docs/PROVIDER_PRECEDENCE_MIRROR_HANDOFF.md
credential_authority: TV/TVC
consumer_credential_authority: NONE
NON-TV/TVC secret/token allowed: false
primary_provider: stegverse_local
third_party_role: CONTROL_OR_FALLBACK_ONLY
claim_state: SOURCE_IMPLEMENTED_VALIDATION_PENDING_LIVE_EXECUTION_PENDING
```

This handoff is canonical for the portable experiment/planning/evidence/comparison layer only. It does not create a credential store, provider runtime, heartbeat, lease authority, provider broker, route authority, or model authority.

## Design invariant

**Experiments are portable; credentials are not.**

Portable packages may contain task identity, prompt profile, lane/provider/capsule IDs, governance modes, model/parameter intent, expected evidence contracts and comparison rules. They may not contain API keys, bearer tokens, vault refs, provider-secret labels, shared credential ciphertext, or mechanisms for retrieving raw credentials.

StegVerse-local inference is the mandatory primary/reference lane and can execute with zero third-party credentials. Third-party lanes are optional or explicitly required bounded controls/fallbacks only.

## Implemented portable source

```text
f097a9aab819471e3ea41c84d5b905968bd1c50c  schema/test-lanes-manifest.schema.json
a6521d4baafe48c44bd0f3b7bdb40313e0dede13  manifests/sv-cost-nine-lane.v1.json
d66dbc3b745dcf040b9669ba3c0f2c6fca8f478c  initial plan_test_lanes.py
81d8bd35e2a13fb023693f2b6dea2829aeab4071  execution-group/shared-candidate planner upgrade
165e0fabba4f90e7e4b260daf1f2b1fc972b1d66  initial planner tests
5bb043b6c435553947a2003ceb31a4c94825d648  execution-group planner tests
ca2dff6df1dd31f074238e5bfa1a4813f50e6687  schema/lane-evidence.schema.json
d34130b79929ae4379ecfd5b4de8f67af1d31b34  compare_test_lanes.py
110de1013bc3b2649538b81fa6b495e60910c019  deterministic comparator tests
5e9c7c92ef50df1cb7497f1047ad4893e4e23cae  validation-only workflow reconciliation
af18f164414cb3ffb6e2e3be2589ab6057597e7a  task-state reconciliation
```

## First portable reference experiment

`manifests/sv-cost-nine-lane.v1.json` reproduces the current nine logical lanes while containing zero credential material:

```text
OpenAI RAW
OpenAI GOVERNED
Anthropic RAW
Anthropic GOVERNED
StegVerse local PRIMARY/reference
DeepSeek RAW
DeepSeek GOVERNED
Kimi RAW
Kimi GOVERNED
```

It binds the exact canonical `SV-RECON-001` task blob `1bd5a640bf067ffad87c427a5c12cb57c029b214` and expected output hash `sha256:bb775b0ada3f33c16adb2f26919f465c5121f9b218d181344fe62908380575cf` without mutating Generation-2 evidence.

Nine logical lanes compile into five execution groups:

```text
1 StegVerse primary/reference execution
1 OpenAI candidate    -> RAW + GOVERNED
1 Anthropic candidate -> RAW + GOVERNED
1 DeepSeek candidate  -> RAW + GOVERNED
1 Kimi candidate      -> RAW + GOVERNED
```

Thus RAW/GOVERNED pairs consume the exact same external candidate instead of making duplicate provider calls. This preserves the original comparison invariant and avoids provider variance/cost duplication.

## Deterministic planning and capsule resolution

`plan_test_lanes.py` emits credential-free lane requests plus execution groups, manifest hash and plan hash.

Without local capsule state:

```text
StegVerse primary -> READY_LOCAL_PRIMARY
external controls -> READY_FOR_TVC_CAPSULE_RESOLUTION
overall -> CAPSULE_RESOLUTION_REQUIRED
```

After TVC supplies non-secret capsule resolutions:

```text
BOUND external capsule -> READY_FOR_TVC_EXECUTION
UNBOUND optional capsule -> SKIPPED_OPTIONAL_CREDENTIAL_UNBOUND
UNBOUND required capsule -> BLOCKED_REQUIRED_CREDENTIAL_UNBOUND
```

A missing optional third-party provider therefore affects only its own lanes. The plan itself grants no execution authority.

Canonical TVC resolution bridge:

`StegVerse-Labs/TVC/scripts/tvc_resolve_test_lane_capsules.py`

The exported bundle strips local credential refs and returns only sanitized provider/capsule/capability/model/readiness metadata plus the originating plan hash.

## Generic external Test-Lane execution

External READY execution groups are owned by TVC, not this repository:

```text
StegVerse-Labs/TVC/scripts/tvc_issue_test_lane_lease.py
StegVerse-Labs/TVC/scripts/tvc_run_test_lane_external_candidate.py
```

The generic Test-Lane lease is separate from the specialized canonical `SV-RECON-001` measurement lease. It is <=300 seconds, single-use, external-provider-only, non-exportable and binds provider/capability/model/capsule/test/manifest/plan/group/task/prompt/member-lane identities.

The runner accepts no provider credential. It supports exact canonical reproduction and user-authored literal-prompt JSON tasks. Before provider access it requires:

1. exact plan hash validity;
2. exact execution-group/member request binding;
3. sanitized resolution `test_id` and `plan_hash` match;
4. exact task Git blob match;
5. provider-profile model admission;
6. fresh re-resolution of the actually selected model against the user's local Provider Capsule;
7. local capsule state READY and role `CONTROL_OR_FALLBACK_ONLY`.

A portable manifest may leave `model: null`, allowing a user-local selection, but the selected model cannot exceed local Provider Capsule policy.

TVC implementation evidence for the final execution guard:

```text
1657dd40834211228b808896ffe550c4f108a299  exact local capsule model + resolution-plan guard
78da241ed622a777a34a3ea1c8845b60b17c992f  focused guard tests
96aaf8e268fac0d7fef2c90a03294eed64ba6cd2  full runner test reconciliation
14e3a9afff3111ac6f81ede8f50bd69571283d04  TVC CI hook
9ac171419faa0a4d615ff6cc6e123bb61b89bef2  Provider Capsule task reconciliation
a956505e9794f3329e3b5f91b704aeb8d676a27d  Provider Capsule mirror handoff reconciliation
```

## Sovereign primary execution

The StegVerse primary/reference execution is **not** implemented in the portable consumer or external runner. It remains owned by the already-developed sovereign path:

`StegVerse-002/micro-node-runtime -> StegVerse-Labs/.github#60/G18 -> TVC -> StegVerse-org/LLM-adapter -> Master Records`.

The local model/runtime source is already complete/released; live governed activation remains machine-owned. Test Lanes cannot replace, duplicate, or downgrade that authority.

## Generic evidence and comparison

`schema/lane-evidence.schema.json` defines sanitized portable lane evidence. `compare_test_lanes.py` deterministically binds evidence back to the exact plan/task/provider/mode and requires evidence for READY lanes while forbidding evidence for lanes that were skipped.

This generic layer is intentionally not cost-specific. A user may compare outputs, usage, latency, governance outcomes and other admitted metrics, while the existing Generation-3 cost control remains a specialized consumer of exact TVC provider telemetry.

Credential material, provider vault refs and provider authority cannot appear in accepted evidence.

## Validation posture

```text
manifest schema: INSTALLED
reference manifest: INSTALLED
planner/execution groups: INSTALLED
planner tests: INSTALLED
generic lane evidence schema: INSTALLED
generic deterministic comparator: INSTALLED
comparator tests: INSTALLED
validation-only workflow: INSTALLED
workflow provider secrets: NONE
hosted workflow result directly observed: NO
live TVC capsule resolution consumed: NO
live external candidate evidence: NO
live StegVerse primary Test-Lane evidence: NO
```

No hosted or live PASS is inferred from source installation.

## Claims and collision partition

```text
portable Test Lanes source: IMPLEMENTED
portable validation: CLAIMED_FOR_VALIDATION
Provider Capsule / external runner: StegVerse-Labs/TVC
provider credential binding: TV/TVC local authority
StegVerse local source runtime: COMPLETE_RELEASED elsewhere
StegVerse live activation: MACHINE_OWNED elsewhere
Generation-2 evidence: COMPLETE / IMMUTABLE elsewhere
```

Collision boundaries:

1. Do not duplicate the local model/runtime.
2. Do not duplicate heartbeat/worker activation.
3. Do not duplicate TVC credential ingress, Provider Capsule, provider broker or lease authority.
4. Do not place credentials/vault refs in portable manifests or evidence.
5. Do not make third-party availability a framework prerequisite.
6. Do not promote third-party success to provider authority.
7. Do not mutate Generation-2 evidence.
8. Do not loosen the specialized canonical provider-measurement lease for arbitrary user experiments.

## User extensibility

A StegVerse user can fork/copy a manifest, change tasks, add/remove lanes, choose models locally where permitted, change parameters/governance profiles and bind only the provider relationships they personally possess. The portable experiment remains shareable while the credential relationship never leaves that user's TV/TVC runtime.

`stegverse.literal-prompt.v1` provides an admitted generic task form without turning Test Lanes into arbitrary code execution.

## Machine/human continuation and release condition

Human secret-value entry is already assigned to the TV/TVC credential-binding task; it grants no route or execution authority. After binding, machine continuation is:

```text
portable manifest
-> credential-free plan
-> TVC local capsule resolution
-> re-plan READY / skip optional unbound lanes
-> StegVerse primary execution through sovereign runtime
-> external READY execution groups through TVC generic runner
-> sanitized lane evidence
-> deterministic comparison
```

Release requires direct source validation plus live evidence that this sequence preserves StegVerse PRIMARY, TV/TVC-only credential custody, exact plan/capsule/model binding, sanitized evidence, independent optional-lane skipping and no third-party authority promotion.

## Session consolidation

Durably transferred requirements:

1. any StegVerse user can reproduce the experiment with their own provider relationships;
2. users can modify/add/remove lanes without altering credential authority;
3. StegVerse-local remains primary/reference and runs without external APIs;
4. provider credentials remain user-local/non-portable;
5. experiment manifests/plans are portable and credential-free;
6. optional missing provider bindings skip independently;
7. RAW/GOVERNED lane pairs share one candidate;
8. arbitrary user literal-prompt tests are supported through a bounded non-code task profile;
9. external operations use a separate bounded TVC lease;
10. selected models are checked against provider policy and the user's actual local capsule;
11. sanitized evidence is bound to the exact plan/task/provider/mode;
12. generic deterministic comparison is installed;
13. no third-party result can replace sovereign provider authority.

All unique source/design requirements are durable. Remaining work is validation/live authority execution, not chat-only project state.

## Completion accounting

```text
required portable source/control surfaces: 8/8 implemented
scaffolding/stubs: 0
missing required source files: 0
validation mechanisms installed: 4/4
hosted validation observed: 0/1
live integration predicates: 0/3 (capsule round-trip, external candidate evidence, sovereign primary evidence)
session requirements transferred: 13/13
source implementation: 100%
goal activation: 78% (source complete; hosted/live execution evidence pending)
```

## Exact next action

1. Observe direct source-validation results when available.
2. Complete authorized TV/TVC credential binding for whichever external providers the user chooses to enable.
3. Generate a portable plan, resolve capsules through TVC, and re-plan to READY.
4. Execute the mandatory primary/reference group through the sovereign StegVerse runtime.
5. Execute READY external groups through the TVC generic runner with the same local capsule registry used for admission.
6. Persist only sanitized lane evidence and run the deterministic comparator; release validation/integration claims only after direct evidence inspection.
