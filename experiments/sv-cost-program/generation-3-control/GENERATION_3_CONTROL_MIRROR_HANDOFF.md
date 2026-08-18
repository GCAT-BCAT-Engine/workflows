# SV-COST Generation-3 Control Mirror Handoff

Updated: 2026-08-18T07:58:00-05:00

## Active goal

```text
goal_id: SV-COST-GENERATION-3-CONTROL-001
originating_session_goal: Use StegVerse as the primary provider; use third-party APIs only as bounded comparison/fallback controls; compare estimated economics with provider-returned API telemetry without transferring provider credentials outside TV/TVC.
repository: GCAT-BCAT-Engine/workflows
branch: main
canonical_generation_2_handoff: experiments/sv-cost-program/nine-lane-results/SV_COST_NINE_LANE_MIRROR_HANDOFF.md
canonical_provider_authority: StegVerse-Labs/TVC
canonical_precedence_handoff: StegVerse-Labs/TVC/docs/PROVIDER_PRECEDENCE_MIRROR_HANDOFF.md
credential_authority: TV/TVC
NON-TV/TVC secret/token allowed: false
consumer credential authority: NONE
claim_state: CONSUMER_INTEGRATION_DEFINED_LIVE_EVIDENCE_PENDING
```

## Provider role model

StegVerse sovereign/local inference is the canonical primary/reference provider path. OpenAI, Anthropic, DeepSeek, and Kimi/Moonshot are Generation-3 controls and optional bounded fallbacks only. Their success or failure cannot promote them to canonical production inference authority.

```text
StegVerse local: PRIMARY / REFERENCE
OpenAI API: CONTROL_OR_FALLBACK_ONLY
Anthropic API: CONTROL_OR_FALLBACK_ONLY
DeepSeek API: CONTROL_OR_FALLBACK_ONLY
Kimi/Moonshot API: CONTROL_OR_FALLBACK_ONLY
```

The Generation-2 nine-lane consumer-app experiment remains immutable evidence and is not replaced by API execution.

## Canonical TVC execution path

```text
TVC-PROVIDER-PRECEDENCE-010
-> TVC-PROVIDER-MEASUREMENT-INGRESS-006
-> TVC-PROVIDER-MEASUREMENT-LIVE-RUN-009
-> short-lived single-use provider lease
-> TV/TVC non-exportable inherited-FD vault binding
-> provider API control request
-> exact provider response/model/output/actual usage
-> official exact-model rate-card binding
-> REQUEST_BOUND_COST sanitized evidence
-> this consumer repository
```

No API key, bearer token, credential value, GitHub token, or vault secret is accepted by this repository.

## Credential availability observation

Non-secret state transferred from the originating session:

```text
all four API keys created: true
OpenAI key: created; currently preserved as transitional GitHub Secret; live TVC binding not observed
Anthropic key: created; currently preserved as transitional GitHub Secret; live TVC binding not observed
DeepSeek key: created; private/idle; live TVC binding not observed
Kimi/Moonshot key: created; private/idle; live TVC binding not observed
raw key values observed by this repository/session records: false
```

This observation is availability metadata only; it grants no credential authority. Production/control use requires TV/TVC inherited-FD vault binding.

## Canonical task identity

Generation 3 reuses the exact Generation-2 deterministic task rather than creating a new workload:

```text
source: experiments/sv-cost-program/nine-lane-results/task.json
task_id: SV-RECON-001
Git blob SHA: 1bd5a640bf067ffad87c427a5c12cb57c029b214
required output hash: sha256:bb775b0ada3f33c16adb2f26919f465c5121f9b218d181344fe62908380575cf
```

Any live runner must fail closed on task-blob mismatch.

## Accepted Generation-3 evidence

For each third-party control, this repository may consume only a sanitized TVC envelope containing:

- provider identity;
- exact provider-returned model ID;
- provider response ID when available;
- exact retained output;
- provider-returned actual usage object;
- normalized token categories derived only from actual usage;
- execution-time official rate-card identity/source;
- exact model-matched rate fields;
- deterministic request-bound cost or direct request-bound provider charge where available;
- assertions `provider_api_key_transferred_to_consumer=false` and `secret_material_returned=false`.

Token estimates may be retained as separate controls but may not substitute for actual provider usage.

## Comparison outputs

Generation 3 will compare, without conflation:

1. Generation-2 consumer-surface economics/observability;
2. StegVerse sovereign/local measured execution and local cost basis;
3. provider API exact usage;
4. official rate-card request-bound cost;
5. optional direct provider balance/charge delta when defensibly isolated;
6. difference between prior estimate/allocation and provider-verified API telemetry.

The comparison does not make third-party APIs primary providers.

## Claims and ownership

```text
Generation-2 nine-lane source/behavior: COMPLETE_RELEASED
Generation-2 hosted proof observation: MACHINE_OWNED by nine-lane hosted observer
Generation-3 provider execution: TV/TVC OWNED
Generation-3 credential binding: TV/TVC OWNED
Generation-3 evidence consumer integration: GCAT-BCAT-Engine/workflows
StegVerse local model/runtime: COMPLETE_RELEASED elsewhere
StegVerse live sovereign activation: MACHINE_OWNED elsewhere
```

No duplicate provider execution, credential store, local model runtime, heartbeat, or route authority is authorized here.

## Validation and release conditions

Current validation state:

```text
Generation-3 consumer handoff: INSTALLED
consumer task state: PENDING_INSTALLATION
live TVC key binding: NOT OBSERVED
live API calls: NOT EXECUTED
exact provider usage receipts: NOT EMITTED
REQUEST_BOUND_COST receipts: NOT EMITTED
cross-generation comparison: NOT YET EXECUTABLE
```

Release requires 4/4 sanitized provider control envelopes accepted by schema/validator, exact canonical task identity, no secret material, exact provider usage, provider/model-matched rate cards, and retained distinction between Generation 2, StegVerse primary execution, and Generation 3 controls.

## Integration/propagation boundary

No Site, Publisher, admissibility-wiki, or stegguardian-wiki propagation is authorized from source readiness alone. Public propagation may occur only after the applicable cost publication gate and sovereign activation/release criteria are met and the destination handoffs are re-read.

## Session consolidation

MERGED INTO:

- `StegVerse-Labs/TVC/docs/PROVIDER_PRECEDENCE_MIRROR_HANDOFF.md`
- `StegVerse-Labs/TVC/tasks/TVC-PROVIDER-MEASUREMENT-INGRESS-006.json`
- `StegVerse-Labs/TVC/tasks/TVC-PROVIDER-MEASUREMENT-LIVE-RUN-009`
- `experiments/sv-cost-program/nine-lane-results/SV_COST_NINE_LANE_MIRROR_HANDOFF.md`

Unique session requirements transferred here: StegVerse-primary provider role, third-party fallback/control-only role, four-key non-secret availability state, Generation-2/Generation-3 separation, exact API telemetry control objective, and TV/TVC-only credential authority.

## Completion accounting

```text
required control/integration files: 2
implemented: 1/2
scaffolding/stubs: 0
missing: task-state.json
validation: 0/2 live evidence gates
integration: 1/3 (handoff installed; task state + live evidence pending)
session requirements transferred: 6/6
```

## Next executable action

Install the consumer task state/validator contract, then wait for TVC-owned `TVC-PROVIDER-MEASUREMENT-LIVE-RUN-009` sanitized evidence. Do not execute provider APIs or handle provider credentials in this repository.
