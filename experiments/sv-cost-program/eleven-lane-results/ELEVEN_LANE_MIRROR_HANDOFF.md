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
