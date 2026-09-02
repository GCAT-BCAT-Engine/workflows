# SV-COST Eleven-Lane Mirror Handoff

Status: **SOURCE COMPLETE ON MAIN — CREDENTIALLESS HARNESS READY — GLM EVIDENCE ACQUISITION NEXT**

## Canonical authority

```text
repository: GCAT-BCAT-Engine/workflows
branch: main
experiment_id: SV-COST-ELEVEN-LANE-RESULTS-001
generation: GENERATION_3_CREDENTIALLESS_PLUS_SOVEREIGN_MODEL_BOUNDARY
predecessor: experiments/sv-cost-program/nine-lane-results/SV_COST_NINE_LANE_MIRROR_HANDOFF.md
credential_authority: TV/TVC
non-TV/TVC protected secret/token authority: FORBIDDEN
initial_merge: a66b8dbc6a2d319ecef66834f7babf7b5a586100
acquisition_tooling_merge: bd0868c38d28e23b4bd37699acf360a2294d7a10
pull_requests: 19, 21
```

The Generation-2 nine-lane result remains frozen. Generation 3 is the successor and does not rewrite historical evidence.

## Goal

Execute an 11-lane comparison whose final two lanes are:

```text
10 GLM-5.3-Flash Hosted
11 GLM-5.3-Flash Sovereign
```

Hosted and sovereign GLM remain distinct because credential authority, custody, network exposure, privacy, and cost basis differ.

## Credential boundary

The harness requires no provider API key.

Existing OpenAI, Anthropic, DeepSeek, and Kimi lanes consume the already-committed external candidate outputs from Generation 2.

GLM Hosted:
- before Vault: external candidate output only;
- after Vault: TV/TVC-authorized runtime credential lease;
- provider credential in repository/userland: forbidden.

GLM Sovereign:
- vendor API credential: not required;
- eligible sovereign runtime identity: required;
- execution evidence: required before any live claim.

## Lane schema

```text
1  OpenAI raw
2  OpenAI governed
3  Anthropic raw
4  Anthropic governed
5  StegVerse deterministic reconstruction
6  DeepSeek raw
7  DeepSeek governed
8  Kimi raw
9  Kimi governed
10 GLM-5.3-Flash Hosted
11 GLM-5.3-Flash Sovereign
```

## Installed source/control surface

```text
README.md
task.json
task-state.json
glm-integration-state.json
candidate-input.schema.json
sovereign-runtime-evidence.schema.json
cost-evidence.schema.json
cost-evidence-request.json
run.py
validate_schema.py
hosted-proof-observer-task.json
model-sources/glm-5.3-flash.v1.json
tools/ingest_glm_hosted_candidate.py
tools/build_glm_sovereign_evidence.py
tests/test_glm_acquisition_tools.py
requests/glm-evaluation-prompt.md
requests/glm-hosted-candidate-request.json
requests/glm-sovereign-execution-request.json
.github/workflows/sv-cost-eleven-lane-candidate-proof.yml
```

The runner:
- inherits lanes 1-9 from frozen Generation-2 candidate evidence;
- emits all 11 lane rows;
- fail-closes lane 10 when `candidate-inputs/glm-hosted.json` is absent;
- fail-closes lane 11 when `runtime-evidence/glm-sovereign.json` is absent;
- never substitutes hosted token pricing for sovereign compute economics;
- preserves missing cost evidence as blockers rather than estimating it.

## Cost basis classes

GLM Hosted accepted bases:
- provider-reported request cost;
- exact provider-reported input/output usage plus a bound versioned rate card;
- provider-observed subscription/quota allocation explicitly labeled non-marginal.

GLM Sovereign accepted basis:
- measured runtime duration;
- measured or bounded energy consumption;
- hardware amortization;
- storage/network/runtime overhead;
- successful equivalent outcome denominator.

## Current execution state

```text
lanes 1-9: inherited evidence available
lane 10: ACQUISITION_ISSUE_OPEN / GCAT-BCAT-Engine/workflows#20
lane 11: MACHINE_OWNED_RUNTIME_EVALUATION_REQUEST_OPEN / StegVerse-002/micro-node-runtime#69
credentialless harness: SOURCE READY ON MAIN
hosted workflow: INSTALLED
hosted workflow run observation: NOT YET DIRECTLY OBSERVED
publication: BLOCKED
```

Direct workflow-run enumeration returned no run objects for the merge commit or sampled predecessor commits. Do not infer either workflow failure or workflow success from that connector result. The repository-native observer remains the hosted-proof owner.

## Fastest next execution

1. Credentialless harness execution request is committed at `run-requests/2026-09-02T0756-0500-credentialless-eleven-lane.md`; direct workflow-run enumeration remains unavailable through the connected observer surface.
2. Acquire GLM Hosted output using `requests/glm-evaluation-prompt.md` through an existing external relationship; store only output metadata, never a provider credential.
3. Execute the same exact prompt on an eligible sovereign GLM runtime and capture `runtime-evidence/glm-sovereign.json`.
4. Re-run the harness and compare behavioral equivalence, governance evidence, and cost basis.
5. Complete remaining OpenAI/Anthropic/DeepSeek bounded cost evidence before publication.

## Remaining files/modules to install

Destination: `GCAT-BCAT-Engine/workflows`

```text
candidate-inputs/glm-hosted.json                  OWNER workflows#20 / BLOCKED_ON_REAL_GLM_HOSTED_OUTPUT
runtime-evidence/glm-sovereign.json              OWNER micro-node-runtime#69 / BLOCKED_ON_ELIGIBLE_SOVEREIGN_RUNTIME
cost-evidence/glm-hosted.json                    BLOCKED_ON_PROVIDER_COST/USAGE EVIDENCE
results/generation-3-eleven-lane/...             GENERATED_BY_RUNNER
local validation receipt                         PENDING_EXECUTION
hosted proof observation                         MACHINE_OWNED_PENDING_OBSERVATION
publication integration                          BLOCKED_ON_EVIDENCE GATES
```

## Downstream release propagation

When the eleven-lane result becomes release-ready, re-read current handoffs before applying publication changes to:

- `StegVerse-Labs/Site`
- `GCAT-BCAT-Engine/Publisher`
- `StegVerse-Labs/admissibility-wiki`
- `StegVerse-Labs/stegguardian-wiki`

## Claim boundary

Source/control implementation is complete and merged. This does not claim live Z.ai execution, sovereign GLM execution, provider credential availability, complete cost evidence, hosted proof PASS, or publication readiness.


## Candidate-acquisition tooling — 2026-09-02

Merged acquisition tooling: `bd0868c38d28e23b4bd37699acf360a2294d7a10` / PR #21.

Installed helpers:

```text
tools/ingest_glm_hosted_candidate.py
tools/build_glm_sovereign_evidence.py
tests/test_glm_acquisition_tools.py
model-sources/glm-5.3-flash.v1.json
```

The hosted ingestion tool rejects credential-like fields and writes only the candidate/output and explicitly supplied provider-observed usage metadata. The sovereign builder writes only exact candidate output, runtime identity, elapsed time, and supplied measured/bounded infrastructure metrics. Neither tool calls a provider or launches a model.

Official source identity is bound to `zai-org/GLM-5.3-Flash` with MIT license and supported local serving profiles including OpenAI-compatible vLLM/SGLang endpoints. Source compatibility does not prove runtime eligibility or execution.

Current acquisition owners:

```text
GLM Hosted candidate: GCAT-BCAT-Engine/workflows#20
GLM Sovereign runtime evaluation: StegVerse-002/micro-node-runtime#69
```


## GLM-5.3-Flash Hosted evidence acquired and validated — 2026-09-02

Hosted lane 10 is no longer blocked on candidate acquisition.

Evidence:
- exact candidate: `candidate-inputs/glm-hosted.json`
- acquisition boundary: `evidence/glm-hosted-acquisition-2026-09-02.json`
- source merge: `36d3802505780c423b56a41918003e7b8612d848`
- eleven-lane validation run: `33687039059` / run number `19` — SUCCESS
- acquisition-tool tests: PASS
- eleven-lane harness: `PASS_HARNESS`
- lanes with behavioral evidence: `10 / 11`

The exact hosted output reconstructs:
```text
final balance: 75
final risk_score: 3
standing: active
applied: 4
denied: 2
event status sequence: ALLOW, ALLOW, ALLOW, DENY, DENY, ALLOW
```

The provider's free-form reason prose is preserved in the raw candidate. Harness semantic comparison normalizes reason wording to the deterministic event reason only when event identity and ALLOW/DENY status match, because the frozen evaluation prompt did not require exact reason strings.

Credential boundary:
- provider API key transferred to StegVerse: false
- provider usage observed: false
- provider cost observed: false
- hosted source acquisition: user-observed provider hosted UI
- repository independently verified provider runtime identity: false
- no provider runtime credential is stored or inferred

Current harness result:
```text
lane_count_defined: 11
lane_count_evidence_present: 10
candidate blocker:
  MISSING_SOVEREIGN_RUNTIME_EVIDENCE:runtime-evidence/glm-sovereign.json

cost blockers:
  openai-raw
  anthropic-raw
  deepseek-raw
  glm-5.3-flash-hosted
  glm-5.3-flash-sovereign

publication: BLOCKED
```

Lane 10 acquisition issue `#20` is satisfied at the candidate/semantic-validation boundary. Lane 11 remains machine-owned by `StegVerse-002/micro-node-runtime#69`.

This does not claim independent provider-side request telemetry, provider billing evidence, sovereign GLM execution, all-eleven completion, or publication readiness.


## Request-bound provider cost intake — 2026-09-02

Issue: #24

Installed source:
```text
cost-evidence/provider-rate-cards.2026-09-02.json
schemas/request-bound-provider-cost-evidence.schema.json
requests/request-bound-provider-evidence-pack.json
tools/ingest_request_bound_provider_candidate.py
tests/test_request_bound_cost_intake.py
```

The intake allows Generation-3 provider candidates to supersede the frozen Generation-2 candidate only for the new run; Generation 2 remains immutable. A replacement provider run must preserve the exact SV-RECON-001 semantic result and credential nonpossession.

Accepted request-cost bases remain fail-closed:
```text
PROVIDER_REPORTED_REQUEST_COST_USD
EXACT_USAGE_PLUS_BOUND_VERSIONED_RATE_CARD
PROVIDER_UI_SUBSCRIPTION_QUOTA_ALLOCATED_EFFECTIVE_COST
```

Current bound rate-card identities:
```text
OpenAI   gpt-5.6-sol
Anthropic claude-opus-5
DeepSeek deepseek-v4-flash / deepseek-v4-pro with explicit peak/off-peak cache-miss rate key
```

No Z.ai official request rate card is bound in this registry. GLM Hosted therefore remains cost-blocked unless the provider exposes request cost, an admissible quota allocation, or exact usage plus a later verified official Z.ai rate card.

Important: a rate card does not create request cost evidence. Existing OpenAI/Anthropic aggregate/plan observations remain insufficient. Existing DeepSeek candidate has unspecified UI model identity and cannot be priced against a current API rate card. The new intake exists so authentic request-bound observations can close those blockers without estimation.

Generation-3 `run.py` now consumes a request-bound provider override from `candidate-inputs/<provider>.json` when present and applies `cost-evidence/<provider>.json`; otherwise it preserves the Generation-2 candidate.
