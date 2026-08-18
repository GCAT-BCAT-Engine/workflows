# StegVerse Test Lanes Mirror Handoff

Updated: 2026-08-18T10:37:00-05:00

## Active goal

```text
goal_id: STEGVERSE-TEST-LANES-001
originating_session_goal: Allow any StegVerse user to reproduce or modify governed model test lanes using their own locally bound provider credentials without surrendering those credentials to the experiment.
repository: GCAT-BCAT-Engine/workflows
branch: main
canonical_provider_authority: StegVerse-Labs/TVC
canonical_provider_precedence: StegVerse-Labs/TVC/docs/PROVIDER_PRECEDENCE_MIRROR_HANDOFF.md
credential_authority: TV/TVC
consumer_credential_authority: NONE
NON-TV/TVC secret/token allowed: false
primary_provider: stegverse_local
third_party_role: CONTROL_OR_FALLBACK_ONLY
claim_state: CLAIMED_FOR_IMPLEMENTATION
```

This handoff is canonical for the portable Test Lanes experiment layer only. It does not create a provider credential store, provider runtime, heartbeat, route authority, or model authority.

## Design invariant

Experiments are portable; credentials are not.

A Test Lanes package may contain task data, prompts, lane definitions, governance modes, comparison rules, expected evidence contracts, and non-secret credential references. It may not contain provider API keys, bearer tokens, credential ciphertext intended for sharing, GitHub secrets, vault secret material, or a mechanism for retrieving raw credentials.

StegVerse-local inference is the primary/reference lane and requires no third-party credential. Third-party lanes are optional controls or explicit bounded fallbacks only.

## Intended execution split

```text
portable test manifest
-> credential-free Test Lanes planner
-> lane execution request
-> TVC route/credential authority
-> StegVerse-local primary execution OR admitted third-party control
-> sanitized evidence
-> Test Lanes comparison/replay
```

The experiment layer asks TVC to execute an admitted operation. It never asks TVC to return a credential.

## Initial implementation inventory

```text
manifest schema: experiments/stegverse-test-lanes/schema/test-lanes-manifest.schema.json
reference manifest: experiments/stegverse-test-lanes/manifests/sv-cost-nine-lane.v1.json
planner/validator: experiments/stegverse-test-lanes/plan_test_lanes.py
planner tests: experiments/stegverse-test-lanes/tests/test_plan_test_lanes.py
provider capsule contract: StegVerse-Labs/TVC/docs/PROVIDER_CAPSULE_MIRROR_HANDOFF.md
```

## Collision boundaries

1. Do not duplicate `StegVerse-002/micro-node-runtime` local model/runtime.
2. Do not duplicate `.github#60` heartbeat/worker activation.
3. Do not duplicate TVC provider credential ingress, provider-operation broker, lease ledger, or route authority.
4. Do not place provider credentials in manifests, workflows, logs, receipts, issues, PRs, or shared artifacts.
5. Do not make third-party providers required for Test Lanes operation.
6. Do not allow a successful third-party lane to promote provider authority.
7. Do not mutate Generation-2 evidence; the nine-lane manifest is a reusable reference definition, not a rewrite of prior evidence.

## Validation/release requirements

Release requires deterministic manifest validation, credential-field rejection, StegVerse-primary enforcement, lane-ID uniqueness, explicit raw/governed modes, fail-closed handling of unavailable provider bindings, deterministic execution-plan output, and a reference nine-lane manifest matching the canonical provider roles.

Hosted workflow success is not required to claim source installation but must be directly observed before claiming hosted validation.

## Machine/human boundaries

Provider credential enrollment remains TV/TVC-owned. A user may bind their own provider relationship locally through the TVC credential-entry surface. Test Lanes receives only non-secret logical references and sanitized evidence.

## Session consolidation

Transferred requirements:

- any StegVerse user can run the same experiment with their own provider relationships;
- users can modify/add/remove lanes without altering credential authority;
- StegVerse-local remains primary and can run with zero external API keys;
- third-party credentials remain user-local/non-portable;
- experiments/manifests are portable;
- exact provider telemetry can be compared without exposing credentials.

## Current accounting

```text
required source/control files: 5
implemented: 1/5 (handoff)
scaffolding/stubs: 0
missing: schema, reference manifest, planner, tests
validation: 0/3
integration: 1/3 (authority boundaries identified)
goal activation: 10%
```

## Next executable action

Install the manifest schema and credential-free deterministic planner, then bind the current nine-lane experiment as the first portable reference manifest. The planner must output execution requests only; TVC remains the sole route/credential authority.
