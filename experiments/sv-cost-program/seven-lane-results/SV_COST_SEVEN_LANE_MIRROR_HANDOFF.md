# SV-COST Seven-Lane Mirror Handoff

Status: **MACHINE_OWNED — DEEPSEEK V4 PRICE BOUND — EXECUTION BLOCKED ON AUTHORIZED CREDENTIAL**

## Active goal and source of truth

- Goal ID: `SV-GOVAI-DEEPSEEK-002`
- Originating session goal: extend the bounded reconstruction test with Lane 6 **DeepSeek** and Lane 7 **DeepSeek/StegVerse**, then use the matched pair in the Governed AI economics comparison.
- Repository / branch: `GCAT-BCAT-Engine/workflows@main`
- Canonical experiment: `experiments/sv-cost-program/seven-lane-results/`
- Canonical handoff: this file
- Parent product handoff: `experiments/sv-cost-program/governed-ai-premium/SV_GOVERNED_AI_PREMIUM_MIRROR_HANDOFF.md`
- Historical immutable evidence: `experiments/sv-cost-program/five-lane-results/results/five_lane_results.json`

Live Git state, workflow jobs/logs/artifacts, provider receipts, and committed results override chat claims.

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

## Authoritative files

```text
experiments/sv-cost-program/seven-lane-results/task.json
experiments/sv-cost-program/seven-lane-results/deepseek-price-card.json
experiments/sv-cost-program/seven-lane-results/run.py
experiments/sv-cost-program/seven-lane-results/run_deepseek_pair.py
experiments/sv-cost-program/seven-lane-results/validate_schema.py
.github/workflows/sv-cost-seven-lane-schema.yml
.github/workflows/sv-cost-deepseek-pair-continuation.yml
```

## Model and price correction

The earlier default `deepseek-chat` alias is not the canonical model for new execution. The official DeepSeek documentation states that `deepseek-chat` / `deepseek-reasoner` were deprecated after `2026-07-24T15:59:00Z` and current V4 execution uses `deepseek-v4-flash` or `deepseek-v4-pro`.

This experiment is now bound to:

```text
model: deepseek-v4-flash
base URL: https://api.deepseek.com
price card: deepseek-price-card.json
observed: 2026-08-07
cache-hit input: $0.0028 / 1M tokens
cache-miss input: $0.14 / 1M tokens
output: $0.28 / 1M tokens
cost rule: cache-miss unless provider usage proves cache-hit tokens separately
```

`task.json` schema `2.1.0` binds this versioned price evidence. Future pricing changes require a newer versioned card before a new cost claim.

## Machine-owned execution claim

```text
task_id: SV-GOVAI-DEEPSEEK-PAIR
claimant: github-actions:SV Cost DeepSeek Pair Continuation
role: implementation + validation
state: MACHINE_OWNED / BLOCKED
surfaces:
  - task.json
  - deepseek-price-card.json
  - run_deepseek_pair.py
  - results/deepseek_pair_results.json
  - .github/workflows/sv-cost-deepseek-pair-continuation.yml
claim_created: 2026-08-07T22:07:00Z
claim_expires: 2026-08-15T00:00:00Z
release_condition: both DeepSeek raw and DeepSeek/StegVerse reach the required normalized outcome with retained provider receipts and price-card binding
collision_boundary: do not rewrite the historical five-lane result or OpenAI/Anthropic evidence
```

Durable claim registry:

```text
experiments/sv-cost-program/governed-ai-premium/task-claims-2026-08-07.json
```

## Automation installed and activated

Workflow:

```text
.github/workflows/sv-cost-deepseek-pair-continuation.yml
```

Triggers:

```text
push on seven-lane files
daily schedule: 06:15 UTC
workflow_dispatch
```

Machine behavior:

1. validates Python and seven-lane schema;
2. validates the versioned DeepSeek price card;
3. executes only DeepSeek lanes 6 and 7 when `DEEPSEEK_API_KEY` is available;
4. emits `BLOCKED` when the authorized credential is absent;
5. emits `RETRY` for transient HTTP/network failure;
6. emits `FAILED` for non-equivalent/non-admissible output;
7. emits `COMPLETE` only when both lanes match the canonical required normalized output;
8. uploads an immutable workflow artifact on every run;
9. commits terminal provider evidence when state is `COMPLETE` or `FAILED`.

## First hosted machine observation

Workflow run:

```text
run: 31222916921
job: 93011124505
head: 71e4ca8bdf8d0b35d31fa82c85b9663c2c605d5f
workflow conclusion: success
machine state: BLOCKED
```

Every job step through schema validation, machine execution/blocker emission, result validation, and artifact upload passed. Terminal-result commit was correctly skipped because `BLOCKED` is not a terminal provider result.

Immutable artifact:

```text
artifact id: 9011025214
name: sv-cost-deepseek-pair-31222916921
digest: sha256:a59551c2364596afb34c5d2908cfb4c36ead66b97b8db40a5aa018da48ae4108
```

Artifact result:

```text
state: BLOCKED
raw.blocker: DEEPSEEK_API_KEY_MISSING
governed.blocker: DEEPSEEK_API_KEY_MISSING
price_card_hash: sha256:8f39bbbdaaaefacca468d488916e5aea1bb2db98ef14f73a746eaed96a9ee78b
```

This is the machine-observable release condition. No chat session needs to poll manually: the daily workflow will retry the capability gate and execute the pair when the authorized secret becomes present.

## Execution and admission contract

The comparison retains:

```text
task_id: SV-RECON-001
operation_class: governed_state_reconstruction
comparison_unit: successful equivalent admissible outcome
same initial state
same policy
same event order
same normalized required output
same DeepSeek model for raw and governed lanes
```

A DeepSeek pair is admitted only when:

```text
raw.state == COMPLETE
governed.state == COMPLETE
raw.actual_output_hash == raw.required_output_hash
governed.actual_output_hash == governed.required_output_hash
provider response hashes retained
usage/cost evidence bound to the versioned price card
```

The canonical full seven-lane publication remains more restrictive: all seven lanes and all required cost evidence must pass before a seven-lane publication claim is made.

## Exact remaining tasks

1. `MACHINE_OWNED` — `SV-GOVAI-DEEPSEEK-PAIR`: wait for the machine-observable condition `DEEPSEEK_API_KEY` present in the authorized GitHub Actions environment; the scheduled workflow then executes lanes 6 and 7 automatically.
2. `BLOCKED` — `SV-GOVAI-DEEPSEEK-INTEGRATE`: after `results/deepseek_pair_results.json` is `COMPLETE`, feed the pair into `experiments/sv-cost-program/governed-ai-premium/` without changing the comparison contract.
3. `BLOCKED` — canonical full seven-lane run: if a publication candidate needs all seven fresh lanes, execute `run.py` only with authorized OpenAI, Anthropic, and DeepSeek credentials and retain all raw receipts.
4. `BLOCKED` — propagation: no Publisher, Site, admissibility-wiki, or stegguardian-wiki mutation until the Governed AI publication gate is explicitly admitted and each destination handoff is re-read immediately before mutation.

## Claim boundary

This experiment measures one bounded deterministic reconstruction operation. It does not establish fresh-inference equivalence, universal provider quality, universal provider economics, company ROI, enterprise-wide savings, geopolitical superiority, or a general claim that one model is better than another.

The central DeepSeek comparison is only:

```text
DeepSeek raw
vs
DeepSeek + StegVerse execution governance
```

under the same deterministic contract.

## Completion state

```text
schema_definition: COMPLETE
schema_validation: PASS
lane_6_deepseek_raw: IMPLEMENTED_BLOCKED_ON_CREDENTIAL
lane_7_deepseek_stegverse: IMPLEMENTED_BLOCKED_ON_CREDENTIAL
v4_model_binding: COMPLETE
versioned_deepseek_price_source: COMPLETE
machine_continuation: ACTIVE
first_machine_observation: BLOCKED_WITH_ARTIFACT
provider_execution: PENDING_AUTHORIZED_CREDENTIAL
result_validation: PENDING_PROVIDER_EXECUTION
product_economics_integration: BLOCKED_ON_PAIR_COMPLETE
publication_propagation: NOT_ADMITTED
```

## Session consolidation

The DeepSeek lane requirement, model migration, price evidence, execution runner, machine-owned retry path, exact blocker, collision boundary, artifact evidence, and downstream integration condition are all durably transferred. This chat is not required to preserve or resume the DeepSeek pair task.
