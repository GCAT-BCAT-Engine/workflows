# SV-COST Nine-Lane Mirror Handoff

Status: **ALL FOUR EXTERNAL CANDIDATES PRESENT — 9/9 BEHAVIORAL LANES SOURCE-READY — KIMI COST EVIDENCE BOUND — HOSTED PROOF PENDING**

## Canonical authority

```text
repository: GCAT-BCAT-Engine/workflows
branch: main
experiment_id: SV-COST-NINE-LANE-RESULTS-001
generation: GENERATION_2_CREDENTIALLESS_OUTPUT_BOUNDARY
credential_authority: TV/TVC
non-TV/TVC protected secret/token authority: FORBIDDEN
canonical task state: experiments/sv-cost-program/nine-lane-results/task-state.json
hosted proof observer: experiments/sv-cost-program/nine-lane-results/hosted-proof-observer-task.json
machine runner: .github/workflows/sv-cost-nine-lane-candidate-proof.yml
```

## Candidate state

```text
OpenAI: supplied / locally validated
Anthropic Opus 5 High: supplied / locally validated
DeepSeek UI model unspecified: supplied / locally validated
Kimi K3: supplied / locally validated
external candidates: 4/4
behavioral lanes available: 9/9
provider API keys transferred to StegVerse: false
```

Canonical candidate commits:

```text
OpenAI: 13c0941704f0e3e037dcdd6e1ae70910345f056f
Anthropic: ef7feb4a9a5322e79f40ff0802736209c3da28b3
DeepSeek: 1c0e30513d844cb63be9e1e5bab189697df3566e
Kimi: b76fc0489e356773e98ff4006daa7fe7a61e7de4
```

## Kimi cost evidence

The user-facing Kimi account does not expose exact API token billing for the candidate. It does expose subscription-plan price and per-request quota consumption.

```text
model: Kimi K3
plan: Allegretto
annual subscription price: $374.99
quota reset: monthly
candidate usage record: k3 Token Usage Query (1), 2026-08-17 19:57 local
candidate quota consumption: 0.02%
separate token-usage follow-up: k3 Token Usage Query (2), 2026-08-17 20:04 local, 0.02%
monthly-equivalent subscription: $374.99 / 12 = $31.249166666667
candidate allocation: $31.249166666667 * 0.0002 = $0.006249833333
```

Canonical evidence:

```text
cost-evidence/kimi-k3-allegretto-subscription-allocation-2026-08-17.json
commit: 926490c407eb199e401ab991b4fdd8b8c860bb56
basis: SUBSCRIPTION_QUOTA_ALLOCATED_EFFECTIVE_COST_NOT_MARGINAL_API_CHARGE
```

This value is an allocated share of a subscription quota, not a Kimi marginal API invoice charge. Kimi's UI-generated approximate token counts are retained as non-billing estimates only and are not used as exact cost inputs.

## Cost-method policy

`task.json` schema version 5.0.0 now permits Kimi cost evidence in this order:

1. candidate-reported marginal cost;
2. a versioned official rate card;
3. provider-UI subscription-quota allocation when explicitly labeled non-marginal.

Policy commit: `7360ce6f66aee89c42087b033ac3507f4c8b4655`.

The canonical `run.py` entrypoint binds the Kimi allocation after the behavioral/governance runner executes, without creating a second runner or credential authority. Entrypoint commit: `972b0b68c5c7652023b1cc3e59b624663f60c2e9`.

## Hosted proof

Source state is ready for a complete 9/9 run. Hosted success is **not yet claimed**.

```text
observer: hosted-proof-observer-task.json
observer commit: 0f9ee19a3e0b1ec54362d8dc8e33ea828a608a4b
required rows: 9
required all_nine_present: true
required all_lanes_admissible: true
required candidate blockers: []
required cost_evidence_complete: true
required cost blockers: []
required Kimi basis: SUBSCRIPTION_QUOTA_ALLOCATED_EFFECTIVE_COST_NOT_MARGINAL_API_CHARGE
required bounded publication status: RESULTS_READY_FOR_BOUNDED_PUBLICATION
```

The observer must directly inspect the newest workflow run, job, logs, artifact and result before hosted validation is promoted to PASS.

## Adjacent goal convergence

Sovereign local model/runtime remains merged into:

`StegVerse-002/micro-node-runtime/docs/SOVEREIGN_LOCAL_MODEL_RUNTIME_MIRROR_HANDOFF.md`

StegFin trade readiness remains merged into:

`StegVerse-Labs/stegfin-governance/docs/STEGFIN_MIRROR_HANDOFF.md`

No cost-analysis task gains runtime credential authority, wallet signing authority, or broadcast authority.

## Next executable work

1. Existing GitHub workflow executes the current 9/9 source state.
2. `hosted-proof-observer-task.json` inspects run/job/log/artifact/result evidence.
3. On PASS, integrate the bounded result into `experiments/sv-cost-program/governed-ai-premium/`, preserving the mixed cost-basis disclosure.
4. Re-read Publisher/Site/wiki handoffs before any public propagation.

## Completion accounting

```text
source/control implementation: COMPLETE
external candidates: 4/4
behavioral lanes source-ready: 9/9
Kimi cost evidence: COMPLETE_BOUNDED_SUBSCRIPTION_ALLOCATION
hosted workflow proof: PENDING_DIRECT_OBSERVATION
publication: SOURCE_READY_NOT_YET_HOSTED_VALIDATED
session unique untransferred requirements: 0
archive safe: true
```
