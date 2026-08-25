# StegVerse Test Lanes Mirror Handoff

Updated: 2026-08-25T18:30:00-05:00

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
claim_state: SOURCE_IMPLEMENTED_DIRECT_EXECUTION_PATH_INSTALLED_REQUIRED_LIVE_EXECUTION_PENDING
archive_state: PROHIBITED_UNTIL_REQUIRED_RUNTIME_OUTCOME_IS_TERMINAL
```

This handoff is canonical for portable Test Lanes planning, sovereign-primary candidate adaptation, candidate-to-lane evidence construction and deterministic comparison. It creates no credential store, provider broker, route authority, model authority or heartbeat authority.

## Governing invariant

**Experiments are portable; credentials are not. Binding state is observed, not asserted. StegVerse-local is PRIMARY.**

The named canonical run contains nine logical lanes and five actual candidate executions:

```text
StegVerse PRIMARY/reference             1 candidate -> 1 lane
OpenAI CONTROL_OR_FALLBACK_ONLY         1 candidate -> RAW + GOVERNED
Anthropic CONTROL_OR_FALLBACK_ONLY      1 candidate -> RAW + GOVERNED
DeepSeek CONTROL_OR_FALLBACK_ONLY       1 candidate -> RAW + GOVERNED
Kimi CONTROL_OR_FALLBACK_ONLY           1 candidate -> RAW + GOVERNED
```

RAW/GOVERNED pairs reuse the exact same provider candidate. Canonical 9/9 means all nine logical lanes execute; partial portable runs may still skip optional external controls but may not be called the canonical 9/9 result.

## Portable source — IMPLEMENTED

```text
manifest/schema/planner: IMPLEMENTED
run_stegverse_primary_candidate.py: IMPLEMENTED
build_lane_evidence.py: IMPLEMENTED
compare_test_lanes.py: IMPLEMENTED
portable tests/workflow: INSTALLED
```

The PRIMARY adapter verifies `stegverse-reference-lm-v1`, loopback-only health, private endpoint status, credential requirement NONE, no third-party inference and authority effect NONE. It emits a sanitized PRIMARY candidate.

The evidence builder consumes one PRIMARY plus four external candidates and produces exactly nine sanitized lane records. The comparator requires a fully READY plan and returns PASS only when every READY lane has valid evidence.

## Canonical direct execution — HEARTBEAT INDEPENDENT

The experiment itself does **not** require heartbeat, G18, WorkerCoordinator or product activation.

Canonical direct runner:

```text
StegVerse-Labs/.github:scripts/run_test_lanes_direct.py
StegVerse-Labs/.github:docs/STEGVERSE_TEST_LANES_DIRECT_RUN_MIRROR_HANDOFF.md
```

Direct pipeline:

```text
StegVerse-controlled runtime
-> current TVC + Test Lanes + micro-node + stegfIn-governance source trees
-> reject hosted runtime and secret-bearing environment
-> use an existing StegVerse loopback endpoint OR start bounded canonical micro-node tools/run_sovereign_model.py
-> verify stegverse-reference-lm-v1 READY/private/no-third-party
-> use existing TVC vault-agent/broker services OR start the existing services from already-provisioned protected provider files
-> live Provider Capsule readiness/materialization
-> exact READY nine-lane plan
-> one StegVerse PRIMARY candidate
-> four TVC external candidates
-> exactly nine sanitized lane records
-> deterministic comparator PASS
-> direct-run receipt
```

Heartbeat/G18/WorkerCoordinator may remain available as optional automation infrastructure but must not block this direct path.

## Canonical external models

Owned/enforced by `StegVerse-Labs/TVC:config/test_lanes_model_selection.sv-cost-nine-lane.v1.json`:

```text
OpenAI    gpt-5.6-sol
Anthropic claude-opus-5
DeepSeek  deepseek-v4-pro
Kimi      kimi-k3
```

TVC independently revalidates each model against its provider operation profile/Provider Capsule before provider access.

## TVC credential/runtime boundary

External execution remains exclusively TVC-owned:

```text
StegVerse-Labs/TVC/scripts/tvc_materialize_provider_capsule_bindings.py
StegVerse-Labs/TVC/scripts/tvc_resolve_test_lane_capsules.py
StegVerse-Labs/TVC/scripts/tvc_issue_test_lane_lease.py
StegVerse-Labs/TVC/scripts/tvc_run_test_lane_external_candidate.py
```

The direct runner never receives a key. It rejects provider/GitHub secret environment variables. If protected TVC provider files are already provisioned it can bootstrap the existing local vault agent/broker with run-local Unix sockets. If those files are missing, execution must stop at the existing hidden-TTY credential registration boundary; no chat/GitHub secret workaround is allowed.

## Optional heartbeat autolaunch

`StegVerse-Labs/.github:STEGVERSE-TEST-LANES-AUTOLAUNCH-001` remains installed as **OPTIONAL_AUTOMATION_ONLY**. Its heartbeat-specific matrix is not the canonical direct-run release condition.

## Request-bound cost integrity repair

The canonical manifest declares `request_bound_cost`, but the previous planner dropped the comparison contract and the evidence builder emitted `cost: null`. Consequently, the comparator could return PASS without cost evidence. This branch repairs the protocol boundary:

- manifest validation requires the canonical comparison contract and its request-bound-cost metric;
- the immutable plan preserves that contract;
- evidence construction requires a typed non-negative request-bound cost for every executed lane;
- comparison fails closed when any declared cost is missing, malformed or unbound;
- tests cover both complete cost evidence and missing-cost rejection.

This does not invent prices. External candidates must provide exact provider usage bound to official model-matched rate cards. The StegVerse PRIMARY must provide measured local resource cost bound to an observed unit-cost profile. Until those producer integrations exist and a live run supplies them, the canonical cost analysis must not report PASS.

## Current live state

```text
direct runner: INSTALLED
bounded StegVerse test-primary bootstrap: INSTALLED
TVC vault-service bootstrap from provisioned files: INSTALLED
canonical model selection: INSTALLED
hosted exact-head validation directly observed: NO
live four-provider TVC readiness: NOT DIRECTLY OBSERVED
live StegVerse PRIMARY candidate: NOT OBSERVED
live four external candidates: NOT OBSERVED
typed request-bound cost gate: IMPLEMENTED_PENDING_PR_VALIDATION
live nine-lane evidence bundle: NOT OBSERVED
live deterministic comparison PASS: NOT OBSERVED
```

## Exact continuation

1. Execute `StegVerse-Labs/.github:scripts/run_test_lanes_direct.py` on the existing StegVerse-controlled runtime.
2. If the direct receipt reports `TVC_PROVIDER_CREDENTIAL_REGISTRATION_REQUIRED`, execute only the already-installed hidden-TTY TV/TVC registrar on that authorized Linux runtime; never paste keys into chat/GitHub/env.
3. Retry the direct runner. It must derive live capsule readiness, produce a fully READY nine-lane plan, execute five candidates, build nine records and require comparator PASS.
4. If a provider call fails, remediate that exact TVC provider/profile/runtime boundary and rerun; do not wait for heartbeat/G18.
5. Preserve and propagate terminal evidence only after direct runtime PASS exists.

## Completion accounting

```text
required portable source/control surfaces: IMPLEMENTED
scaffolding/stubs: 0
missing required source files: 0
direct execution source: IMPLEMENTED
hosted validation directly observed for latest heads: NO
live required runtime result: NOT_YET_OBSERVED
archive eligible: false
```

Source, plan, model selection, READY, handoff, assignment, heartbeat state or workflow success never satisfy the required runtime outcome.
