# SV-COST Eleven-Lane Mirror Handoff

Status: **HOSTED GLM VALIDATED — SOVEREIGN RUNTIME EVIDENCE PENDING — CREDENTIALLESS COST EVIDENCE ACQUISITION ACTIVE**

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
- credentialless external/provider-UI candidate evidence is sufficient for this experiment;
- TV/TVC-authorized hosted provider operation is an optional execution path, not a prerequisite for cost acquisition;
- provider credential in repository/userland: forbidden;
- API-key registration is not required by the eleven-lane cost-analysis path.

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
tools/ingest_glm_sovereign_resident_evidence.py
tests/test_glm_acquisition_tools.py
tests/test_glm_sovereign_resident_intake.py
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
lanes 1-9: inherited behavioral evidence available
lane 10 hosted GLM: EVIDENCE_PRESENT_HARNESS_VALIDATED
lane 11 sovereign GLM: RESIDENT_BRIDGE_MERGED_INTAKE_READY_AUTHENTIC_EXECUTION_PENDING
behavioral evidence present: 10 / 11
credentialless harness: MERGED_VALIDATED
hosted workflow observation: SUCCESS OBSERVED
credentialless provider-cost intake/capture: MERGED_VALIDATED
publication: BLOCKED_ON_LANE_11_AND_COST_EVIDENCE
```

Observed validation includes successful eleven-lane candidate-proof runs through the hosted GLM, resident-intake, request-bound-cost, and credentialless UI-capture changes. Source/workflow success remains evidence only and does not substitute for authentic sovereign execution or provider cost observations.

## Fastest next execution

1. Resident WorkerCoordinator executes the already-installed private GLM-5.3-Flash lane-11 task and emits authentic sovereign evidence with available runtime/infrastructure measurements.
2. Install that exact resident evidence through `tools/ingest_glm_sovereign_resident_evidence.py` and re-run the eleven-lane harness.
3. For OpenAI, Anthropic, DeepSeek, and hosted GLM cost blockers, use credentialless isolated before/after provider observations from `requests/credentialless-ui-cost-capture-pack.json`, including the exact candidate output from the isolated window.
4. Build request-bound cost evidence with `tools/build_credentialless_ui_cost_evidence.py`; do not provision an API key merely to satisfy this experiment.
5. Publish only after all eleven behavioral lanes and required bounded cost evidence pass.

## Remaining evidence to install

Destination: `GCAT-BCAT-Engine/workflows`

```text
runtime-evidence/glm-sovereign.json              OWNER micro-node-runtime#69 / AUTHENTIC_RESIDENT_EXECUTION_PENDING
cost-evidence/openai.json                        CREDENTIALLESS_REQUEST_BOUND_OBSERVATION_PENDING
cost-evidence/anthropic.json                     CREDENTIALLESS_REQUEST_BOUND_OBSERVATION_PENDING
cost-evidence/deepseek.json                      CREDENTIALLESS_REQUEST_BOUND_OBSERVATION_PENDING
cost-evidence/glm-hosted.json                    CREDENTIALLESS_REQUEST_BOUND_OBSERVATION_PENDING
sovereign infrastructure cost fields             AUTHENTIC_RUNTIME_MEASUREMENT_PENDING
publication integration                          BLOCKED_ON_EVIDENCE GATES
```

`candidate-inputs/glm-hosted.json` is already installed and validated. Current validation/hosted proof observations are already available; they are not remaining installation work.

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


## Resident sovereign evidence intake — 2026-09-02

Issue: #26

The source-side handoff from the merged sovereign WorkerCoordinator lane to this Generation-3 experiment is now explicitly bounded.

Resident producer:
`StegVerse-Labs/.github:SHWP-GLM53-SOVEREIGN-LANE-001`

Resident bridge merge:
`StegVerse-Labs/.github@be021c2b842ea347f2223a0949ed7562cdd854b1`

Consumer intake:
`tools/ingest_glm_sovereign_resident_evidence.py`

The intake accepts either:
- the exact consumer evidence object emitted by the resident worker; or
- the micro-node producer receipt containing `consumer_evidence`.

It then verifies:
```text
model = GLM-5.3-Flash
task_id = SV-RECON-001
endpoint_class = SOVEREIGN_OPENAI_COMPATIBLE
vendor_api_credential_used = false
final state = balance 75 / risk 3 / active
decision sequence = ALLOW, ALLOW, ALLOW, DENY, DENY, ALLOW
applied_count = 4
denied_count = 2
claim_boundary = DETERMINISTIC_RECONSTRUCTION_ONLY
elapsed_seconds >= 0
all supplied infrastructure metrics >= 0
```

It fails closed on credential-like material and on semantic mismatch. The destination is first-write-wins for differing evidence and idempotent for exact re-ingestion.

The intake performs no network fetch, provider operation, hosted inference substitution, credential acquisition, runtime activation, publication decision, or release action.

Current boundary remains:
```text
resident bridge source: MERGED_VALIDATED
resident lane-11 execution: NOT YET OBSERVED
runtime-evidence/glm-sovereign.json: NOT YET INSTALLED
behavioral evidence: 10 / 11
```

This closes the source-side format/installation seam only. It does not satisfy lane 11 without authentic resident evidence.


### Resident intake merge and validation evidence

```text
intake issue: #26 CLOSED
intake PR: #27
intake merge: fdc731eedc8823d00e510ffd6f5b283f9f3a209d
intake validated head: 22e98f2538151c4693dbd7393d92f8022e9676ef
handoff authority: 33695260783 SUCCESS
handoff semantics: 33695260777 SUCCESS
continuity provenance: 33695260773 SUCCESS
eleven-lane candidate proof: 33695260791 SUCCESS

validation-binding issue: #28 CLOSED
validation-binding PR: #29
validation-binding merge: 8196f8670114b2ec81ee7b0f49a816765b49838c
validation-binding head: 855916385a128a577a1592aa5e0e3534228e417d
resident intake acquisition tests: 6/6 PASS
candidate proof: 33695457195 SUCCESS
continuity provenance: 33695457306 SUCCESS
handoff semantics: 33695457297 SUCCESS
```

The repository-side lane-11 intake path is now source-complete and exercised by the existing candidate-proof validation lane. Authentic resident GLM execution remains the only behavioral lane-11 evidence prerequisite.


## Request-bound cost consumption closure — 2026-09-02

Issue: #31

The Generation-3 intake already produced `cost-evidence/<provider>.json`, but the eleven-lane harness did not consume those files. That left a software-side gap between accepted request-bound cost evidence and the experiment's `cost_blockers`.

The harness now:
- loads `cost-evidence/openai.json`, `anthropic.json`, and `deepseek.json` when a Generation-3 provider candidate is installed;
- verifies provider/model/task identity, explicit credential nonpossession, claim boundary, nonnegative cost, and candidate binding;
- applies the same request-bound provider cost to the raw and governed rows derived from that one provider execution;
- loads `cost-evidence/glm-hosted.json` for the hosted Z.ai row with the same identity/boundary checks;
- preserves inherited Generation-2 behavior when no Generation-3 cost packet exists;
- fails closed on mismatched or malformed cost evidence.

This does not create provider cost evidence. It ensures authentic evidence, once installed, actually closes the corresponding harness blocker.


### Sanitized TVC measurement bridge

The same issue also installs `tools/ingest_tvc_request_bound_measurement.py`.

That bridge accepts only already-sanitized `stegverse.tvc.provider-measurement-evidence.v1` with `REQUEST_BOUND_COST` and the TVC exact-usage/official-rate-card basis. It supports the currently blocked OpenAI, Anthropic, and DeepSeek cost lanes. It parses and revalidates the exact frozen candidate, maps only actual normalized usage into the Generation-3 candidate/cost schemas, preserves TV/TVC as source authority through rate-card provenance, and rejects protected fields or non-request-bound evidence.

The bridge performs no provider operation, network fetch, credential handling, runtime execution, or publication action.


### Cost-consumption merge evidence

```text
issue: #31 CLOSED
PR: #32
merge: ba1c8476e00c4e2746f98edee520d554ba0ff897
validated head: 2ded4de6423e6e25e708e932c2ea6196e62ff130
handoff authority: 33696882189 SUCCESS
handoff semantics: 33696882160 SUCCESS
continuity provenance: 33696882171 SUCCESS
eleven-lane candidate proof: 33696882131 SUCCESS
GLM acquisition tests: 6/6 PASS
request-bound cost intake/consumption tests: 11/11 PASS
```

Request-bound cost packets are now active harness inputs rather than inert artifacts. Sanitized TVC measurement evidence can be converted into the exact Generation-3 candidate/cost inputs for OpenAI, Anthropic, and DeepSeek. Actual cost evidence remains absent and is not inferred from this merge.


## Credentialless before/after provider UI cost capture — 2026-09-02

Issue: #34

The remaining hosted-provider cost blockers now have a machine-validated credentialless observation path.

Installed source:
```text
schemas/credentialless-ui-cost-observation.schema.json
tools/build_credentialless_ui_cost_evidence.py
tests/test_credentialless_ui_cost_builder.py
requests/credentialless-ui-cost-capture-pack.json
```

Supported isolated observation modes:
```text
DIRECT_REQUEST_COST_USD
USAGE_CREDIT_SPENT_USD
QUOTA_PERCENT
EXACT_TOKENS
```

The capture contract requires one exact SV-RECON-001 candidate between a before/after observation pair and rejects non-isolated windows, negative/decreasing counters, credential-like material, unverified rate keys, and model/rate-card mismatch.

The builder emits the existing `stegverse.request-bound-provider-cost-evidence/v1` shape already consumed by the eleven-lane harness.

This preserves the Generation-3 credentialless evidence boundary. It performs no login, API request, provider operation, browser automation, credential handling, runtime execution, or publication action.

No current cost blocker is closed merely by installing this source. Provider-facing before/after evidence must still be authentically observed.


### Credentialless UI capture merge evidence

```text
issue: #34 CLOSED
PR: #35
merge: d6e2a353ff60623fb6d67c17adef91b2307d569f
validated head: d19e4c6dcea09b6a1e1ca71e432a4945d8ea99b9
handoff authority: 33699425571 SUCCESS
handoff semantics: 33699425643 SUCCESS
continuity provenance: 33699425573 SUCCESS
eleven-lane candidate proof: 33699425570 SUCCESS
credentialless UI cost capture validation step: SUCCESS
```

The hosted-provider cost path is now explicitly credentialless. API-key registration is not a prerequisite for this experiment's cost acquisition.


## Credentialless UI observation candidate binding — 2026-09-02

Issue: #37

The credentialless before/after observation object now carries the exact provider candidate output from the isolated window. The builder semantically verifies:
- `task_id=SV-RECON-001`;
- final state balance 75 / risk 3 / active;
- ordered decisions ALLOW, ALLOW, ALLOW, DENY, DENY, ALLOW;
- applied_count 4;
- denied_count 2;
- `claim_boundary=DETERMINISTIC_RECONSTRUCTION_ONLY`.

Free-form reason prose remains provider-authentic and is not required to match deterministic wording.

This prevents an otherwise valid cost delta from being bound to a different provider request or task while preserving the credentialless path.


### Credentialless UI candidate-binding merge evidence

```text
issue: #37 CLOSED
PR: #38
merge: 444bba037fa0f770a1317be93e64818b15f7dde8
validated head: 4a2e3935ce7c8c76d402d7851598837fa25fe6dc
handoff authority: 33699713869 SUCCESS
handoff semantics: 33699713871 SUCCESS
continuity provenance: 33699713879 SUCCESS
eleven-lane candidate proof: 33699713884 SUCCESS
```

Credentialless cost observations are now bound to the exact provider candidate output as well as the isolated before/after provider UI window.


## Reconstructable credentialless UI cost provenance — 2026-09-02

Issue: #42

The emitted request-bound cost packet now preserves the exact `before` and `after` provider observation objects used for the calculation, plus the applicable subscription monthly-equivalent amount and/or bound rate key. It already preserved the exact provider candidate output and observation mode.

This makes the derived dollar cost reconstructable from the emitted evidence packet itself rather than depending on an unstored transient input file.

No cost value is inferred beyond the already-validated observation mode.


### Reconstructable UI cost provenance merge evidence

```text
issue: #42 CLOSED
PR: #43
merge: 95b940bdee5440fe3124d49d6bd4ae3d60219adb
validated head: be6258059a95b1cec0afb6c6be96a8f0c3706328
handoff authority: 33704619397 SUCCESS
handoff semantics: 33704619401 SUCCESS
continuity provenance: 33704619417 SUCCESS
eleven-lane candidate proof: 33704619393 SUCCESS
```


## OpenAI 5.6 Sol UI candidate observation — 2026-09-03

Issue: #48

User-supplied iOS evidence now records:
- ChatGPT General settings UI displaying model `5.6 Sol`;
- a fresh ChatGPT composer surface;
- an exact `SV-RECON-001` JSON result with final state `balance=75`, `risk_score=3`, `standing=active`;
- decision sequence `ALLOW, ALLOW, ALLOW, DENY, DENY, ALLOW`;
- applied/denied counts `4/2`;
- `DETERMINISTIC_RECONSTRUCTION_ONLY` claim boundary.

Evidence file:
`evidence/openai-ui-candidate-observation-2026-09-03.json`

The two submitted screenshots are bound by SHA-256:
- `4504ae82e253551e5989124d758c4fbe6c3504e7097aea753ee23b2c0940a16d`
- `88d9463216a5ac652571f731995f3797340c3985983f2691a0aed7910cb21028`

This evidence is sufficient for model/candidate observation only. Neither screenshot exposes an admissible before/after usage, dollar-cost, token, credit-spend, or quota counter. Therefore OpenAI request-bound cost remains:

```text
INSUFFICIENT_NO_BEFORE_AFTER_USAGE_SURFACE
```

No cost is inferred from ChatGPT Plus access, model selection, or the candidate result itself.


## Anthropic Opus 5 UI candidate observation — 2026-09-03

Issue: #50

User-supplied Claude iOS evidence now records:
- model selector displaying `Opus 5 High`;
- UI warning that Opus consumes usage limits faster than other models;
- an exact `SV-RECON-001` JSON result with final state `balance=75`, `risk_score=3`, `standing=active`;
- decision sequence `ALLOW, ALLOW, ALLOW, DENY, DENY, ALLOW`;
- applied/denied counts `4/2`;
- `DETERMINISTIC_RECONSTRUCTION_ONLY` claim boundary.

Evidence file:
`evidence/anthropic-ui-candidate-observation-2026-09-03.json`

Submitted screenshot SHA-256:
`852f4685fe2d09a7421a5c1f0d68f8556445c3ebd6770e85fa6899062de5d7af`

This is sufficient for model/candidate observation only. The UI warning is qualitative and exposes no numeric before/after usage, token, credit-spend, quota, or dollar-cost counter. Therefore Anthropic request-bound cost remains:

```text
INSUFFICIENT_NO_NUMERIC_BEFORE_AFTER_USAGE_SURFACE
```

No dollar cost or quota allocation is inferred from the qualitative warning.


## DeepSeek iOS candidate observation — 2026-09-03

Issue: #52

User-supplied DeepSeek iOS evidence now records:
- app Settings surface with version `2.4.4(3)`;
- an exact `SV-RECON-001` JSON result with final state `balance=75`, `risk_score=3`, `standing=active`;
- decision sequence `ALLOW, ALLOW, ALLOW, DENY, DENY, ALLOW`;
- applied/denied counts `4/2`;
- `DETERMINISTIC_RECONSTRUCTION_ONLY` claim boundary.

Evidence file:
`evidence/deepseek-ui-candidate-observation-2026-09-03.json`

Submitted screenshot SHA-256:
`e8ca58c92f3782cdd7261b096987f01564f96dbebdfd971e59e2c5bcfa70f96c`

The supplied Settings screen does not expose exact model identity, so no V4 Flash/Pro model claim is made from this evidence. Exact model identity remains:

```text
UNOBSERVED_IN_SUPPLIED_UI
```

The same screen exposes no numeric before/after usage, token, credit-spend, quota, or dollar-cost counter. Therefore DeepSeek request-bound cost remains:

```text
INSUFFICIENT_NO_NUMERIC_BEFORE_AFTER_USAGE_SURFACE
```

No model or cost value is inferred from the app version or candidate semantics.


## GLM-5.3-Flash Hosted UI candidate observation — 2026-09-03

Issue: #54

User-supplied Z.ai hosted UI evidence now records:
- model header displaying `GLM-5.3-Flash`;
- the `SV-RECON-001` prompt in the hosted chat surface;
- an exact returned JSON result with final state `balance=75`, `risk_score=3`, `standing=active`;
- decision sequence `ALLOW, ALLOW, ALLOW, DENY, DENY, ALLOW`;
- applied/denied counts `4/2`;
- `DETERMINISTIC_RECONSTRUCTION_ONLY` claim boundary.

Evidence file:
`evidence/glm-hosted-ui-candidate-observation-2026-09-03.json`

Submitted screenshot SHA-256:
`fd7639d4a7b0f8ea93ebc1ba49b6a1abd48dbbbe760fd27b27d516cb7241dba2`

The returned candidate is semantically identical to the deterministic baseline and the already-installed hosted GLM candidate. Free-form reason prose differs only in wording and remains semantically valid.

The submitted hosted UI surface exposes no admissible numeric before/after request-cost, token, credit-spend, quota, or usage counter. Therefore hosted GLM request-bound cost remains:

```text
INSUFFICIENT_NO_NUMERIC_BEFORE_AFTER_USAGE_SURFACE
```

No provider billing, usage, runtime identity, credential, sovereign execution, or request-bound dollar cost is inferred from the model header or successful candidate output.


## Perplexity supplemental candidate observation — 2026-09-03

Issue: #56

User-supplied Perplexity text output records an exact `SV-RECON-001` result with:
- final state `balance=75`, `risk_score=3`, `standing=active`;
- decision sequence `ALLOW, ALLOW, ALLOW, DENY, DENY, ALLOW`;
- applied/denied counts `4/2`;
- `DETERMINISTIC_RECONSTRUCTION_ONLY` claim boundary.

Evidence file:
`evidence/perplexity-ui-candidate-observation-2026-09-03.json`

Semantic comparison: `PASS`.

No Perplexity model/version identity was exposed in the supplied result, so model identity remains:

```text
UNOBSERVED_IN_SUPPLIED_RESULT
```

No screenshot, request telemetry, token usage, quota, credit-spend, or request-bound dollar cost was supplied. This record is supplemental exploratory evidence only and does not expand, renumber, or alter the canonical eleven-lane experiment.


## Companion research objective — literal cost transparency

A second research objective now appends to this cost analysis without modifying the canonical eleven-lane experiment:

`experiments/sv-cost-program/cost-transparency/COST_TRANSPARENCY_MIRROR_HANDOFF.md`

Primary comparative attribute:

`ACTUAL_COST_DISCLOSURE_BURDEN`

It measures the amount of research required to discover or exactly reconstruct the literal request-attributable economic cost of an inference. A public rate card alone is not treated as evidence of actual request cost.

Current UI observations for OpenAI, Anthropic, DeepSeek, hosted GLM, and supplemental Perplexity are seed evidence only. Final disclosure-burden ratings require completion of the separate provider research protocol.
