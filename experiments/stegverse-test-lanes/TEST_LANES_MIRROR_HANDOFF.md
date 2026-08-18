# StegVerse Test Lanes Mirror Handoff

Updated: 2026-08-18T11:47:00-05:00

## Active goal

```text
goal_id: STEGVERSE-TEST-LANES-001
originating_session_goal: Allow any StegVerse user to reproduce, modify, add, or remove governed model test lanes using their own locally bound provider relationships without surrendering provider credentials to the experiment.
repository: GCAT-BCAT-Engine/workflows
branch: main
canonical_task_state: experiments/stegverse-test-lanes/task-state.json
canonical_provider_authority: StegVerse-Labs/TVC
canonical_provider_capsule: StegVerse-Labs/TVC/docs/PROVIDER_CAPSULE_MIRROR_HANDOFF.md
credential_authority: TV/TVC
consumer_credential_authority: NONE
NON-TV/TVC secret/token allowed: false
primary_provider: stegverse_local
third_party_role: CONTROL_OR_FALLBACK_ONLY
claim_state: SOURCE_IMPLEMENTED_VALIDATION_PENDING_LIVE_EXECUTION_PENDING
```

This handoff is canonical for the portable experiment/planning/evidence/comparison layer only. It creates no credential store, provider runtime, heartbeat, lease authority, provider broker, route authority, model authority or vault-readiness authority.

## Governing invariant

**Experiments are portable; credentials are not. Binding state is observed locally, not asserted by the portable experiment.**

StegVerse-local is the mandatory primary/reference lane and can execute with zero external API credentials. Third-party lanes are optional or explicitly required bounded `CONTROL_OR_FALLBACK_ONLY` controls/fallbacks.

Portable packages may contain task identity, prompt profile, lane/provider/capsule IDs, governance modes, model/parameter intent, evidence contracts and comparison rules. They may not contain API keys, bearer tokens, vault refs, provider-secret labels, shared credential ciphertext or raw-credential retrieval mechanisms.

## Portable source

```text
f097a9aab819471e3ea41c84d5b905968bd1c50c  manifest schema
a6521d4baafe48c44bd0f3b7bdb40313e0dede13  SV-COST nine-lane portable manifest
81d8bd35e2a13fb023693f2b6dea2829aeab4071  execution-group/shared-candidate planner
5bb043b6c435553947a2003ceb31a4c94825d648  planner tests
ca2dff6df1dd31f074238e5bfa1a4813f50e6687  generic lane-evidence schema
d34130b79929ae4379ecfd5b4de8f67af1d31b34  deterministic comparator
110de1013bc3b2649538b81fa6b495e60910c019  comparator tests
5e9c7c92ef50df1cb7497f1047ad4893e4e23cae  validation-only workflow
b28baefb69a2a5273e533a6576ec1823d6178778  latest task-state reconciliation
```

The reference experiment has nine logical lanes but five candidate executions:

```text
1 StegVerse primary/reference
1 OpenAI candidate    -> RAW + GOVERNED
1 Anthropic candidate -> RAW + GOVERNED
1 DeepSeek candidate  -> RAW + GOVERNED
1 Kimi candidate      -> RAW + GOVERNED
```

RAW/GOVERNED pairs therefore compare the exact same provider candidate.

## Live-vault-derived Provider Capsule resolution

The previous static/manual `BOUND` possibility is removed from the normal execution path.

Canonical source:

```text
StegVerse-Labs/stegfin-governance/stegwallet/vault_agent_service.py
  8229dc4f4f4384902850b8ccc5ffac4e5b9d6451  non-secret readiness operation
  6fdd8eb6b0c9987dad12f7767162ad0a0d687f33  readiness tests

StegVerse-Labs/TVC/scripts/tvc_materialize_provider_capsule_bindings.py
  8a198f5417096acdf1e4f7b4ca230a89eec8b79f  automatic materializer
  13a42833c58b47a1517ee564d536271fee63de48  materializer tests

StegVerse-Labs/TVC/scripts/tvc_resolve_test_lane_capsules.py
  4c05b2a4262b8175ef71bdd2db74888dd74c5baa  live-readiness resolution enforcement
  9202af28d214d48eb4946b4a121c1c433acb9043  live-readiness resolution tests
```

Normal resolution now performs:

```text
portable capsule template
-> live TV/TVC vault readiness
-> automatic runtime BOUND/UNBOUND materialization
-> sanitized capsule resolution
```

A static template that says `BOUND` cannot force READY. If the actual TV/TVC vault returns `UNAVAILABLE`, the external capsule resolves `CREDENTIAL_BINDING_UNAVAILABLE`. The sanitized bundle includes the originating plan hash and non-secret materialization commitments but no credential ref or value.

## Planning states

Without resolved external state:

```text
StegVerse primary -> READY_LOCAL_PRIMARY
external controls -> READY_FOR_TVC_CAPSULE_RESOLUTION
```

After live TVC resolution:

```text
vault-ready external -> READY_FOR_TVC_EXECUTION
vault-unavailable optional external -> SKIPPED_OPTIONAL_CREDENTIAL_UNBOUND
vault-unavailable required external -> BLOCKED_REQUIRED_CREDENTIAL_UNBOUND
```

Third-party absence therefore affects only its own lane unless the experiment author explicitly requires that control.

## Generic external execution

External READY groups are owned by TVC:

```text
StegVerse-Labs/TVC/scripts/tvc_issue_test_lane_lease.py
StegVerse-Labs/TVC/scripts/tvc_run_test_lane_external_candidate.py
```

The generic lease is separate from the specialized canonical `SV-RECON-001` measurement lease, <=300 seconds, single-use, non-exportable and external-provider-only. It binds provider/capability/model/capsule/test/manifest/plan/group/task/prompt/member-lane identities.

The runner accepts no provider credential, verifies exact plan/group/task identity and selected-model local capsule policy, then invokes the existing TVC vault broker. The broker performs the authoritative actual secret resolution at the provider-use boundary; if the key is unavailable, the provider operation cannot execute. No redundant pre-lease secret read is needed.

Relevant TVC evidence:

```text
69867d252d1a6594bc78982f8eb634a916d2b798  exact provider/capability lease binding
1657dd40834211228b808896ffe550c4f108a299  resolution-plan + selected-model capsule guard
78da241ed622a777a34a3ea1c8845b60b17c992f  focused guard tests
96aaf8e268fac0d7fef2c90a03294eed64ba6cd2  runner tests
821b2cf4c7220ba7af0e4b96e757d4ed587ca815  TVC validation hook
d77741f6ccad4392e78cd06a565a10f45b2b336f  Provider Capsule task reconciliation
903b8d10badc1c5f1766872e704a1a811abe33bd  Provider Capsule handoff reconciliation
```

## Sovereign primary execution

The StegVerse primary/reference execution remains owned by:

`StegVerse-002/micro-node-runtime -> StegVerse-Labs/.github#60/G18 -> TVC -> StegVerse-org/LLM-adapter -> Master Records`.

The local model/runtime source is already complete/released. Test Lanes cannot replace, duplicate or downgrade sovereign authority. Third-party success cannot establish canonical activation.

## Generic evidence/comparison

`schema/lane-evidence.schema.json` and `compare_test_lanes.py` bind sanitized evidence to the exact plan/task/provider/mode, require evidence for READY lanes and reject evidence for skipped lanes. Credentials and TVC vault refs are prohibited.

The framework is not cost-specific; cost measurement remains a specialized consumer of exact TVC telemetry.

## Validation and claim state

```text
portable source: IMPLEMENTED
live-vault capsule resolution source: IMPLEMENTED in TVC/shared vault
generic external execution source: IMPLEMENTED in TVC
validation workflows/tests: INSTALLED
hosted validation directly observed for latest heads: NO
live vault readiness READY: NOT_YET_OBSERVED
live sanitized capsule round-trip: NOT_YET_OBSERVED
live external candidate: NOT_YET_OBSERVED
live StegVerse primary Test-Lane evidence: NOT_YET_OBSERVED
```

Combined-status inspection exposes no status entries, so hosted PASS is not inferred.

Collision boundaries:

1. do not duplicate local model/runtime or heartbeat activation;
2. do not duplicate TVC vault, secret ingress, Provider Capsule, broker or lease authority;
3. do not place credentials/vault refs in portable artifacts;
4. do not make third-party availability a framework prerequisite;
5. do not promote external results to provider authority;
6. do not mutate Generation-2 evidence;
7. do not accept static capsule BOUND state as live evidence.

## Machine/human continuation

Only raw secret-value entry remains a human TV/TVC authority boundary. After entry the continuation is machine-executable:

```text
live vault readiness
-> automatic capsule materialization/resolution
-> re-plan READY / skip unavailable optional lanes
-> sovereign StegVerse primary execution
-> bounded external groups through TVC
-> sanitized evidence
-> deterministic comparison
```

Release requires direct source validation and live evidence for the above path, including actual broker-local provider-secret resolution at use time and no provider-authority promotion.

## Session consolidation

All session-specific design/source requirements are now durable, including:

- user-owned provider relationships;
- portable experiments/non-portable credentials;
- StegVerse-local mandatory primary/reference;
- optional third-party controls/fallbacks;
- shared RAW/GOVERNED candidates;
- bounded literal-prompt user tests;
- separate generic TVC lease;
- model/capsule/plan/task binding;
- generic sanitized evidence/comparison;
- live-vault-derived rather than user-asserted external binding state.

## Completion accounting

```text
required portable source/control surfaces: 8/8 implemented
scaffolding/stubs: 0
missing required source files: 0
validation mechanisms installed: 4/4
hosted validation observed: 0/1
live integration predicates: 0/4
session requirements transferred: 14/14
source implementation: 100%
goal activation: 82% (source complete; hosted/live evidence pending)
```

## Exact next action

1. Observe direct source validation when inspectable.
2. Complete authorized TV/TVC secret entry for desired external providers.
3. Resolve the portable plan through TVC; the resolver now performs live vault readiness/materialization automatically.
4. Re-plan to READY / skip unavailable optional lanes.
5. Execute StegVerse PRIMARY through the sovereign runtime.
6. Execute READY external groups through TVC; the existing broker resolves the actual provider secret at use time.
7. Persist sanitized lane evidence and deterministic comparison; release validation/integration claims only after direct inspection.
