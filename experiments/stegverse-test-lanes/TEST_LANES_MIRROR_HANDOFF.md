# StegVerse Test Lanes Mirror Handoff

Updated: 2026-08-18T10:37:00-05:00

## Active goal

```text
goal_id: STEGVERSE-TEST-LANES-001
originating_session_goal: Allow any StegVerse user to reproduce or modify governed model test lanes using their own locally bound provider credentials without surrendering those credentials to the experiment.
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
claim_state: SOURCE_IMPLEMENTED_VALIDATION_PENDING
```

This handoff is canonical for the portable Test Lanes experiment layer only. It does not create a credential store, provider runtime, heartbeat, lease ledger, route authority, or model authority.

## Design invariant

**Experiments are portable; credentials are not.**

A Test Lanes package contains task identity, prompts/profiles, lane definitions, governance modes, comparison rules, expected evidence contracts, and Provider Capsule IDs. It may not contain provider API keys, bearer tokens, vault refs, provider-secret labels, GitHub secrets, shared credential ciphertext, or a mechanism for retrieving raw credentials.

StegVerse-local inference is the mandatory primary/reference lane and requires no third-party credential. Third-party lanes are optional controls or explicitly required bounded controls only.

## Implemented source

```text
4b2ad7988191fc7cab5cd38e06146cc76e364135  initial scoped handoff
f097a9aab819471e3ea41c84d5b905968bd1c50c  schema/test-lanes-manifest.schema.json
a6521d4baafe48c44bd0f3b7bdb40313e0dede13  manifests/sv-cost-nine-lane.v1.json
d66dbc3b745dcf040b9669ba3c0f2c6fca8f478c  plan_test_lanes.py
165e0fabba4f90e7e4b260daf1f2b1fc972b1d66  tests/test_plan_test_lanes.py
165b0a379dd1d15e2b36eb598790f3ed1346c3b9  .github/workflows/stegverse-test-lanes-validation.yml
f16257a793569496a79068393cc4da047c82a6ff  task-state.json
```

## Portable manifest contract

The manifest requires:

- `primary_provider = stegverse_local`;
- exactly one required StegVerse-local primary/reference lane;
- lane IDs unique;
- every lane identifies only a Provider Capsule ID, capability, provider, mode and optional model/parameters;
- external provider role always `CONTROL_OR_FALLBACK_ONLY`;
- raw lanes cannot claim a governance profile;
- governed lanes require an explicit governance profile;
- `credential_policy.authority = TV/TVC`;
- manifest credentials/export both false;
- exact task source blob identity.

Credential-like fields and values such as `credential_ref`, `vault://`, provider API-key labels, bearer markers, and GitHub PAT markers fail closed.

## First reference experiment

`manifests/sv-cost-nine-lane.v1.json` is the reusable definition of the current nine-lane comparison:

```text
OpenAI raw
OpenAI governed
Anthropic raw
Anthropic governed
StegVerse local PRIMARY/reference
DeepSeek raw
DeepSeek governed
Kimi raw
Kimi governed
```

It binds the exact canonical `SV-RECON-001` task blob `1bd5a640bf067ffad87c427a5c12cb57c029b214` and required output hash `sha256:bb775b0ada3f33c16adb2f26919f465c5121f9b218d181344fe62908380575cf` while carrying zero provider credential material.

The Generation-2 nine-lane evidence remains immutable; this manifest is a portable reproduction definition, not a rewrite of prior results.

## Deterministic planner

`plan_test_lanes.py` validates the manifest and emits deterministic `stegverse.test-lane-execution-request.v1` packets plus request/manifest/plan hashes.

Without any local credential state:

```text
StegVerse primary -> READY_LOCAL_PRIMARY
external controls -> READY_FOR_TVC_CAPSULE_RESOLUTION
overall -> CAPSULE_RESOLUTION_REQUIRED
```

When supplied a non-secret TVC capsule-resolution bundle:

```text
BOUND external capsule -> READY_FOR_TVC_EXECUTION
UNBOUND optional external capsule -> SKIPPED_OPTIONAL_CREDENTIAL_UNBOUND
UNBOUND required external capsule -> BLOCKED_REQUIRED_CREDENTIAL_UNBOUND
```

An unavailable third-party credential therefore affects only its lane unless the experiment author explicitly declared that lane required. StegVerse-local remains independently executable.

The plan grants no execution authority and contains no credential material.

## TVC Provider Capsule integration

Canonical provider binding task:

`StegVerse-Labs/TVC/tasks/TVC-PROVIDER-CAPSULE-012.json`

TVC source:

```text
config/provider_capsule.schema.json
config/provider_capsules.example.json
tvc_provider_capsule.py
scripts/tvc_resolve_test_lane_capsules.py
```

TVC validates capsule provider/profile/ref/capability/model bindings locally. The Test Lanes bridge consumes the portable plan and returns a sanitized capsule resolution bundle with `credential_ref` removed. This repository receives readiness state only, never the underlying credential or local vault reference.

## Validation posture

Local validation requires only the Python standard library:

```text
python3 experiments/stegverse-test-lanes/tests/test_plan_test_lanes.py
python3 experiments/stegverse-test-lanes/plan_test_lanes.py experiments/stegverse-test-lanes/manifests/sv-cost-nine-lane.v1.json
```

The validation-only workflow uses `permissions: {}`, anonymous checkout, no package installation, no provider SDK, and no provider secrets. It proves the reference plan has 9 lanes, exactly one READY local primary and eight external capsule-resolution requests.

```text
manifest schema: INSTALLED
reference manifest: INSTALLED
planner: INSTALLED
planner tests: INSTALLED
stdlib-only validation workflow: INSTALLED
hosted workflow result directly observed: NO
live TVC capsule-resolution bundle consumed: NO
live lane execution: NO
```

No hosted or live PASS is inferred from source installation.

## Claims and collision partition

```text
Test Lanes source: IMPLEMENTED
Test Lanes validation: CLAIMED_FOR_VALIDATION
Provider Capsule authority: StegVerse-Labs/TVC
provider credential binding: TV/TVC local authority
StegVerse local runtime: COMPLETE_RELEASED elsewhere
StegVerse live activation: MACHINE_OWNED elsewhere
external provider execution: TVC provider-operation authority
Generation-2 evidence: COMPLETE/IMMUTABLE elsewhere
```

Collision boundaries:

1. Do not duplicate `StegVerse-002/micro-node-runtime` local model/runtime.
2. Do not duplicate `.github#60` heartbeat/worker activation.
3. Do not duplicate TVC credential ingress, provider broker, lease ledger, Provider Capsule authority, or route authority.
4. Do not place credentials or TVC vault refs in portable manifests/artifacts.
5. Do not make third-party providers mandatory for the framework itself.
6. Do not let third-party success promote provider authority.
7. Do not mutate Generation-2 evidence.

## Reusability

A user may copy/fork a manifest and add/remove lanes, models, parameters, governance profiles, comparison metrics, or entirely new provider capsule IDs. Their local TV/TVC installation decides whether those capsule IDs are actually bound and admissible.

A user with zero external provider credentials can still run the StegVerse primary lane. A user with one provider relationship can enable only that provider's lanes. A user with all admitted relationships can reproduce the full reference experiment.

## Session consolidation

Durably transferred requirements:

1. any StegVerse user can reproduce the experiment with their own provider relationships;
2. users can modify/add/remove lanes without altering credential authority;
3. StegVerse-local remains primary/reference and can run with zero external APIs;
4. third-party credentials remain user-local/non-portable;
5. experiment manifests are portable;
6. provider telemetry/evidence can be compared without exposing credentials;
7. unavailable optional provider bindings skip independently;
8. Test Lanes plans contain no execution authority;
9. Provider Capsule/TVC is the only external credential resolution path.

## Completion accounting

```text
required source/control surfaces: 7
implemented: 7/7
scaffolding/stubs: 0
missing required source files: 0
source implementation: 100%
validation mechanisms installed: 2/2
hosted validation observed: 0/1
live integration predicates: 0/2 (TVC resolution round-trip, live lane evidence)
session requirements transferred: 9/9
goal activation: 70% (portable source complete; live local capsule/execution evidence pending)
```

## Next executable action

Observe source validation. After a user binds any provider relationship locally through TV/TVC, generate the portable plan, resolve capsule IDs through `StegVerse-Labs/TVC/scripts/tvc_resolve_test_lane_capsules.py`, feed only the resulting non-secret resolution states back into `plan_test_lanes.py`, and execute READY lanes exclusively through their canonical owners. Persist sanitized evidence and comparisons without changing provider authority.
