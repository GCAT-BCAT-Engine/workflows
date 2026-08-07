# Governed AI Premium Mirror Handoff

Status: **ACTIVE — LOCAL GOVERNANCE ECONOMICS STACK PASS — WORKLOAD MIX PASS — DEEPSEEK AND REMOTE BURDEN PENDING**

## Source of truth

Canonical repository:

```text
GCAT-BCAT-Engine/workflows
```

Canonical workstream:

```text
experiments/sv-cost-program/governed-ai-premium/
```

This file is the current task, collision, evidence, and continuation handoff for the Governed AI product-economics comparison.

Historical provider evidence:

```text
experiments/sv-cost-program/five-lane-results/results/five_lane_results.json
```

DeepSeek extension source:

```text
experiments/sv-cost-program/seven-lane-results/
```

## Directional thesis

Provider unit-price ranking remains useful evidence, but it is not the durable long-run comparison if intelligence becomes abundant.

Primary long-run comparison:

```text
existing provider AI
vs
existing provider AI + StegGate
```

Preferred abundant-intelligence unit:

```text
absolute governance cost per governed admissible action by governance burden class
```

For mixed workloads, use:

```text
workload-weighted governance cost per governed admissible action
```

Percentage premium over inference remains secondary because the denominator can collapse while the governance workload stays unchanged.

## Installed implementation

```text
product-comparison-schema.json
execution_candidate.json
reduce.py
isolate_steggate.py
production-burden-profile.json
production_burden.py
product_tier_envelope.py
workload-mix-scenarios.json
workload_mix.py
.github/workflows/sv-governed-ai-premium.yml
```

The comparison schema is now `1.1.0` and explicitly separates provider inference cost, StegGate governance cost, provider-specific integration cost, and commercial margin.

## Hosted evidence

### Core isolation

Run `31219131269` completed `success` at commit `22b4235efdda04f2203bf81a0a2ddb431556ca40`.

Artifact:

```text
id: 9009669589
name: governed-ai-premium-evidence
digest: sha256:4cfd49475c42a160413f92fdcd9b616e4641946330441c0f78735eceb3267c71
```

### Production-burden curve

Run `31222023913` completed `success` at commit `3d5ea7c07e132893f5c9c2c5aaa5596b0f64920f`.

Artifact:

```text
id: 9010716206
name: governed-ai-premium-evidence
digest: sha256:7b174c0f3d7f1182f2891e9931f95d3d6a58e8b6285bc47367c55566ba43cd03
```

Observed local synthetic burden curve on the hosted Linux runner for that run:

| Tier | Mean latency | Modeled local cost / governed action |
|---|---:|---:|
| CORE | 0.036845 ms | $0.000000010353 |
| PROOF | 0.113322 ms | $0.000000022950 |
| LOOKUP | 0.420741 ms | $0.000000063939 |
| PERSIST | 1.123170 ms | $0.000000157596 |
| QUORUM | 1.116657 ms | $0.000000156728 |
| BOUNDARY | 1.233232 ms | $0.000000172271 |

All six tiers produced admissible results and all four fail-closed negative cases passed:

```text
revoked_delegation_denied: true
tampered_successor_denied: true
tampered_proof_denied: true
insufficient_quorum_denied: true
```

### Product-tier envelope

Run `31222078818`, commit `17e97fa20e0ce7d1ce697348da3b0ec47c57ad3f`, completed `success`.

Artifact:

```text
id: 9010737144
name: governed-ai-premium-evidence
digest: sha256:cd6c52f8d5b5a86eb3bb4cdb8aeddf35d1ed00a9297c23d5bfb6ced5b0658897
```

The envelope combines historical provider inference observations with measured local governance burden and hypothetical inference compression factors. It emits 20%, 40%, and 60% gross-margin arithmetic only as sensitivity cases, not recommended prices.

Example using the OpenAI historical raw cost and BOUNDARY burden tier:

| Inference compression | Hypothetical inference | Measured local governance | Governance share of floor | Mode |
|---:|---:|---:|---:|---|
| 1.0 | $0.006875000000 | $0.000000172271 | 0.002506% | TOKEN_PRICE_RELEVANT |
| 0.01 | $0.000068750000 | $0.000000172271 | 0.249950% | TOKEN_PRICE_RELEVANT |
| 0.0001 | $0.000000687500 | $0.000000172271 | 20.036837% | TOKEN_PRICE_COMPRESSED |

### Workload-mix sensitivity

Run `31222213580`, commit `c7ab2d3541b2529d677f49895e41f2027e7c9d4c`, completed `success`.

Every hosted step passed:

```text
historical pair reducer
isolated StegGate core meter
production-burden curve
Governed AI product-tier envelope
Governed AI workload-mix sensitivity
JSON validation
artifact upload
```

Artifact:

```text
id: 9010786489
name: governed-ai-premium-evidence
digest: sha256:b7e1a237539289e41a4cbb3bf6c8a4d014c7394a6f2d7c4f5f14b83512300d93
```

Observed workload-mix sensitivity from the run:

| Scenario | Expected local governance cost/action | Cost / 1M actions | Mean local latency/action | Receipt storage / 1M actions-month |
|---|---:|---:|---:|---:|
| LIGHT_ASSIST | $0.000000023842 | $0.023842 | 0.129918 ms | $0.006520 |
| ENTERPRISE_OPS | $0.000000117380 | $0.117380 | 0.823352 ms | $0.007600 |
| HIGH_CONSEQUENCE | $0.000000193594 | $0.193594 | 1.393519 ms | $0.007792 |
| BALANCED | $0.000000125621 | $0.125621 | 0.886060 ms | $0.007480 |

These scenarios are illustrative workload weights only; they are not usage, demand, revenue, or customer-mix forecasts.

The result supports a stronger product metric than one universal StegGate premium: a provider can potentially price or meter a Governed AI tier by the governance burden actually required by the action or by an observed workload mix.

## Historical provider-pair evidence

Completed five-lane evidence provides two matched prompt-path pairs:

| Pair | Raw cost | Governed cost | Observed pair delta | Delta % |
|---|---:|---:|---:|---:|
| OpenAI -> OpenAI/StegVerse | $0.006875 | $0.006880 | +$0.000005 | +0.072727% |
| Anthropic -> Anthropic/StegVerse | $0.010656 | $0.007116 | -$0.003540 | -33.220721% |

These deltas are not wholesale StegGate cost. They include provider-side token/output behavior. The negative Anthropic delta is direct evidence that raw-minus-governed provider cost cannot be relabeled as governance cost.

## Product interpretation under test

Candidate product label: **Governed AI**.

Potential provider economics form:

```text
provider inference
+ StegGate governance burden by class/workload mix
+ provider-specific integration/operations burden
+ provider margin
= governed service tier
```

No wholesale charge or retail price is admitted yet.

## Governance burden classes

```text
CORE      in-process admissibility + receipt/reconstruction
PROOF     CORE + cryptographic proof verification
LOOKUP    PROOF + policy/delegation artifact retrieval
PERSIST   LOOKUP + durable receipt persistence
QUORUM    PERSIST + 2-of-3 approval verification
BOUNDARY  QUORUM + serialized local service boundary
```

Different actions can require different governance burdens. This makes burden-class and workload-weighted economics more defensible than one fixed governance surcharge.

## Current metric contract

`product-comparison-schema.json` v1.1.0 now defines:

```text
primary: absolute governance cost per governed admissible action by burden class
workload: workload-weighted governance cost per governed admissible action
secondary: percentage premium, latency, storage, admissibility lift, margin headroom
```

Mode boundaries for sensitivity testing are ratio-based:

```text
TOKEN_PRICE_RELEVANT: inference >= 10x governance burden
TOKEN_PRICE_COMPRESSED: inference >= 1x and < 10x governance burden
INTELLIGENCE_ABUNDANT: inference < governance burden, or intelligence price is otherwise no longer the main differentiator
```

These thresholds are testing semantics, not market laws.

## Claim boundary

Do not claim:

- StegVerse improves underlying model intelligence;
- provider pair deltas equal StegGate cost;
- local synthetic measurements equal production cloud/service cost;
- one fixed governance premium applies to all actions;
- illustrative workload mixes predict customer usage;
- margin scenarios are recommended prices;
- market willingness to pay or enterprise ROI is established;
- DeepSeek economics are measured before canonical DeepSeek execution exists.

Admitted bounded finding:

> StegGate governance can be measured independently of provider inference, segmented into explicit control burdens, and aggregated into workload-weighted cost per governed admissible action. That metric remains coherent as inference pricing compresses.

## Exact next tasks

1. Complete canonical seven-lane execution for `DeepSeek` and `DeepSeek/StegVerse` with a versioned DeepSeek price source and retained provider receipts.
2. Feed the DeepSeek pair into the same Governed AI reducer without changing the comparison contract.
3. Replace local approximations one class at a time with measured remote burdens: policy service, delegation service, KMS/signature verification, durable remote persistence, and network boundary.
4. Separate provider-specific adapter overhead from provider-independent StegGate burden.
5. Replace illustrative workload weights with measured workload distributions only when real usage evidence exists; retain illustrative scenarios for sensitivity testing.
6. Only after remote burden evidence exists, test bounded wholesale price envelopes and provider margin scenarios as candidates rather than claims.
7. Before publication or cross-repo propagation, inspect newest destination `*_MIRROR_HANDOFF.md` in `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/Site`, `admissibility-wiki`, and `stegguardian-wiki`.

## Completion state

```text
comparison_mode_definition: COMPLETE
comparison_schema_v1_1: COMPLETE
abundant_intelligence_modes: COMPLETE
historical_pair_reducer: PASS
isolated_core_meter: PASS
production_burden_profile: COMPLETE
production_burden_runner: PASS
negative_fail_closed_cases: 4/4 PASS
product_tier_envelope: PASS
workload_mix_scenarios: 4/4 COMPLETE
workload_mix_reducer: PASS
hosted_artifact_evidence: PASS
provider_independent_local_burden_curve: ESTABLISHED_BOUNDED
workload_weighted_local_economics: ESTABLISHED_BOUNDED
remote_production_burden: PENDING
deepseek_pair: PENDING
provider_specific_adapter_overhead: PENDING
wholesale_price_claim: NOT_ADMITTED
retail_price_claim: NOT_ADMITTED
publication: NOT_ADMITTED
```

## Session consolidation

The abundant-intelligence metric shift, historical pair evidence, core isolation, production-burden curve, fail-closed negative tests, product-envelope sensitivity, workload-mix sensitivity, schema v1.1 metric promotion, workflow runs, artifact IDs/digests, claim boundaries, and exact next tasks are durably transferred here. Repository-native continuation owns the remaining work.
