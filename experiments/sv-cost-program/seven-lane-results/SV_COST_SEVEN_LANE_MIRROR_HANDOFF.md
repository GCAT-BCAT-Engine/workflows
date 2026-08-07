# SV-COST Seven-Lane Mirror Handoff

Status: **ACTIVE — SCHEMA INSTALLED — EXECUTION PENDING**

## Source of truth

This file is the current task and verification handoff for the seven-lane extension of the bounded reconstructable-governance experiment.

Canonical repository:

```text
GCAT-BCAT-Engine/workflows
```

Canonical experiment:

```text
experiments/sv-cost-program/seven-lane-results/
```

Historical five-lane evidence remains immutable at:

```text
experiments/sv-cost-program/five-lane-results/results/five_lane_results.json
```

## Goal

Extend the existing five-lane testing schema with two new lanes while preserving the exact task contract and admissibility comparison unit:

- Lane 6: **DeepSeek raw**
- Lane 7: **DeepSeek/StegVerse governed**

The models of interest for the new work are therefore **DeepSeek** and **DeepSeek/StegVerse**.

## Seven lanes

| Lane | Lane ID | Model interest | StegVerse governance |
|---:|---|---|---|
| 1 | `openai-raw` | OpenAI | No |
| 2 | `openai-governed` | OpenAI/StegVerse | Yes |
| 3 | `anthropic-raw` | Anthropic | No |
| 4 | `anthropic-governed` | Anthropic/StegVerse | Yes |
| 5 | `stegverse-only` | StegVerse deterministic reconstruction | Yes |
| 6 | `deepseek-raw` | DeepSeek | No |
| 7 | `deepseek-governed` | DeepSeek/StegVerse | Yes |

## Installed files

```text
experiments/sv-cost-program/seven-lane-results/task.json
experiments/sv-cost-program/seven-lane-results/run.py
experiments/sv-cost-program/seven-lane-results/SV_COST_SEVEN_LANE_MIRROR_HANDOFF.md
```

## Execution contract

The test reuses task `SV-RECON-001`, operation class `governed_state_reconstruction`, and comparison unit `successful equivalent admissible outcome`.

The DeepSeek runner uses the OpenAI-compatible DeepSeek chat-completions interface and defaults to:

```text
DEEPSEEK_API_BASE=https://api.deepseek.com
DEEPSEEK_SEVEN_LANE_MODEL=deepseek-chat
```

Required provider credential for lanes 6 and 7:

```text
DEEPSEEK_API_KEY
```

DeepSeek pricing is deliberately not fabricated or frozen in the schema. At execution, a versioned provider rate source must populate:

```text
DEEPSEEK_INPUT_USD_PER_MILLION
DEEPSEEK_OUTPUT_USD_PER_MILLION
```

If the model succeeds but rates are absent, admissibility evidence may complete while cost publication remains fail-closed with `ADMISSIBILITY_COMPLETE_COST_PUBLICATION_BLOCKED`.

## Admission boundary

A seven-lane publication is admitted only when the generated canonical result states:

```text
all_seven_successful_equivalent_admissible = true
all_seven_cost_evidence_complete = true
publication_status = RESULTS_READY_FOR_BOUNDED_SEVEN_LANE_PUBLICATION
```

No historical five-lane value may be rewritten to make the seven-lane run pass.

## Claim boundary

This experiment measures one bounded deterministic reconstruction operation. It does not establish fresh-inference equivalence, universal provider quality, universal provider economics, company ROI, enterprise-wide savings, geopolitical superiority, or a general claim that one model is better than another.

The central new comparison is narrower:

```text
DeepSeek raw
vs
DeepSeek + StegVerse execution governance
```

under the same deterministic contract, identity, state, policy, events, validation, retry ceiling, and normalized admissible outcome used by the existing schema.

## Exact next tasks

1. Install an authorized execution route with the required provider secrets.
2. Resolve and record a versioned DeepSeek price source before any cost claim.
3. Execute all seven lanes or an explicitly labeled DeepSeek-only preflight followed by the canonical seven-lane run.
4. Retain raw provider responses, usage, latency, failures, normalized hashes, and generated result/report artifacts.
5. Validate that lanes 6 and 7 produce the same required normalized outcome hash as the established task contract.
6. Only after canonical execution passes, update the root `SV_COST_MIRROR_HANDOFF.md` and inspect destination `*_MIRROR_HANDOFF.md` files before any Publisher, Site, admissibility-wiki, or stegguardian-wiki propagation.

## Collision boundary

Do not modify or supersede the historical five-lane result artifact. The seven-lane experiment is a new result lineage. Do not broaden its bounded claims into favorable ROI or universal model-quality claims. Issue `#13` remains the only canonical continuation for a future favorable general ROI revision.

## Completion state

```text
schema_definition: COMPLETE
lane_6_deepseek_raw: INSTALLED_NOT_EXECUTED
lane_7_deepseek_stegverse: INSTALLED_NOT_EXECUTED
runner: COMPLETE
provider_credential_route: PENDING
versioned_deepseek_price_source: PENDING
canonical_execution: PENDING
result_validation: PENDING
publication_propagation: NOT_ADMITTED
```

## Session consolidation

The new lane definitions, execution contract, claim boundary, collision boundary, installed files, remaining prerequisites, and exact next tasks are durably transferred here. Repository state owns continuation.
