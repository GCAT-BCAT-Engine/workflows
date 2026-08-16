# SV-COST Seven-Lane Mirror Handoff

Status: **GENERATION_2 CREDENTIALLESS OUTPUT-BOUNDARY IMPLEMENTED — HOSTED VALIDATION PASS — EXTERNAL CANDIDATES PENDING**

## Source of truth

```text
repository: GCAT-BCAT-Engine/workflows
branch: main
experiment: experiments/sv-cost-program/seven-lane-results/
experiment_id: SV-COST-SEVEN-LANE-RESULTS-001
generation: GENERATION_2_CREDENTIALLESS_OUTPUT_BOUNDARY
credential_invariant: NO_PROVIDER_API_KEY_POSSESSED_OR_CONSUMED_BY_STEGVERSE_TEST_WORKLOAD
historical_generation_1: experiments/sv-cost-program/five-lane-results/results/five_lane_results.json
```

Live Git state, workflow logs/artifacts, candidate receipts, and committed results override chat claims.

## Governing architecture

Generation 2 no longer executes OpenAI, Anthropic, or DeepSeek by consuming provider API keys inside the StegVerse experiment.

```text
user / existing application / TV-TVC provider relationship
  -> provider generation
  -> external candidate output
  -> StegVerse seven-lane ingestion boundary
  -> raw observation + governed observation
  -> governance receipt
  -> replay receipt
  -> reconstruction receipt
```

The same provider candidate is used for each raw/governed pair. Therefore the changed variable is StegVerse governance, not credential plumbing or a second provider generation.

`raw` means provider candidate observed without StegVerse admission, not direct possession of provider credentials.

## Production-artifact reference

```text
StegVerse-Labs/StegCore
  docs/STEGVERSE_MICRO_ECOSYSTEM_MIRROR_HANDOFF.md
  runtime identity: stegverse:steggate:canonical:three-layer:v1

StegVerse-org/StegVerse-SDK
  docs/SDK_PORTABLE_PACKAGE_CONSOLE_MIRROR_HANDOFF.md
  docs/SDK_OUTPUT_BOUNDARY_PROOF_MIRROR_HANDOFF.md

portable deployment classes:
  S  = Sovereign isolated deployment
  NS = Node Sovereign profile; install/profile does not itself grant membership

provider account required by portable unit: FALSE
non-TV/TVC secret required: FALSE
```

## Seven lanes

| Lane | Lane ID | Candidate / operation | StegVerse governance | Provider credential inside StegVerse workload |
|---:|---|---|---|---|
| 1 | `openai-raw` | external OpenAI candidate | No | No |
| 2 | `openai-governed` | same OpenAI candidate | Yes | No |
| 3 | `anthropic-raw` | external Anthropic candidate | No | No |
| 4 | `anthropic-governed` | same Anthropic candidate | Yes | No |
| 5 | `stegverse-only` | deterministic reconstruction | Yes | None |
| 6 | `deepseek-raw` | external DeepSeek candidate | No | No |
| 7 | `deepseek-governed` | same DeepSeek candidate | Yes | No |

## Canonical files

```text
experiments/sv-cost-program/seven-lane-results/task.json
experiments/sv-cost-program/seven-lane-results/candidate-input.schema.json
experiments/sv-cost-program/seven-lane-results/run.py
experiments/sv-cost-program/seven-lane-results/run_candidate_outputs.py
experiments/sv-cost-program/seven-lane-results/run_deepseek_pair.py
experiments/sv-cost-program/seven-lane-results/validate_schema.py
experiments/sv-cost-program/seven-lane-results/deepseek-price-card.json
.github/workflows/sv-cost-seven-lane-schema.yml
.github/workflows/sv-cost-deepseek-pair-continuation.yml
```

`run.py` is the canonical Generation-2 entrypoint. `run_deepseek_pair.py` is retained only as a compatibility entrypoint and delegates to the same credentialless candidate runner. The prior direct-key DeepSeek implementation is retired from the canonical execution path.

## Candidate contract

Generation 2 consumes:

```text
candidate-inputs/openai.json
candidate-inputs/anthropic.json
candidate-inputs/deepseek.json
```

Each candidate must bind:

```text
provider
model
task_id
candidate_output
provider_api_key_transferred_to_stegverse: false
```

Optional retained economic evidence includes provider token usage, reported provider cost, latency, response ID, and response hash.

Missing candidates fail closed as `PUBLICATION_BLOCKED`; they do not cause the experiment to seek a provider secret.

## Proof surface

For every governed external candidate, the runner emits:

```text
receipts/<provider>-governance.json
receipts/<provider>-replay.json
receipts/<provider>-reconstruction.json
```

The governed row binds candidate hash, decision, required and normalized output hashes, credential non-possession, governance incremental compute/storage cost, replay match, and reconstruction match.

## Economic isolation

Generation 1 remains immutable historical evidence and used provider credentials directly in the provider execution workflow.

Generation 2 intentionally separates:

```text
provider generation cost
+ StegVerse governance incremental cost
+ receipt storage cost
+ replay/reconstruction cost
```

The raw/governed pair shares the exact same provider candidate, so no second provider generation is needed merely to add governance.

Provider price values remain declared-rate evidence unless independently invoice reconciled.

## Hosted validation evidence

### Schema validation

```text
workflow: .github/workflows/sv-cost-seven-lane-schema.yml
run: 31918107807
job: 95093309152
head: f5c3a1f32c865155daa1baabf08bbc10de0eb285
conclusion: SUCCESS
```

Syntax validation and the Generation-2 credentialless contract validation passed.

### Candidate proof continuation

Historical filename retained for compatibility:

```text
.github/workflows/sv-cost-deepseek-pair-continuation.yml
```

Current workflow name: `SV Cost Seven-Lane Credentialless Candidate Proof`.

```text
run: 31918122419
job: 95093347248
head: f309f56e225c8eac1f57ef9171fd01d365b66092
conclusion: SUCCESS
artifact: 9255521460
artifact name: sv-cost-seven-lane-generation-2-31918122419
artifact digest: sha256:5aebc4bb45dd04baf0fd0cdc37679a3654ec9041f0900307e113169aa9f53e56
```

Passed stages:

1. credentialless seven-lane contract validation;
2. external-candidate processing / bounded blocker generation;
3. generated proof-surface validation;
4. immutable Generation-2 evidence upload;
5. release-condition summary.

The hosted run had no provider candidates, so it correctly produced the bounded external-candidate blocker rather than seeking provider credentials.

## Completion state

```text
generation_1_five_lane_evidence: COMPLETE_IMMUTABLE
seven_lane_schema_3_0_0: COMPLETE
credentialless_candidate_contract: COMPLETE
canonical_direct_key_path_removed: COMPLETE
same_candidate_raw_governed_invariant: COMPLETE
production_stegcore_reference: COMPLETE
production_sdk_reference: COMPLETE
S_NS_reference_boundary: COMPLETE
governance_receipt_generation: COMPLETE_IMPLEMENTATION
replay_receipt_generation: COMPLETE_IMPLEMENTATION
reconstruction_receipt_generation: COMPLETE_IMPLEMENTATION
credential_nonpossession_receipt: COMPLETE_IMPLEMENTATION
cost_isolation: COMPLETE_IMPLEMENTATION
hosted_schema_validation: PASS
hosted_candidate_proof: PASS_BLOCKED_AS_DESIGNED_WITHOUT_EXTERNAL_CANDIDATES
openai_generation_2_candidate: PENDING_EXTERNAL_CANDIDATE
anthropic_generation_2_candidate: PENDING_EXTERNAL_CANDIDATE
deepseek_generation_2_candidate: PENDING_EXTERNAL_CANDIDATE
full_generation_2_result: BLOCKED_ON_THREE_EXTERNAL_CANDIDATES
seven_lane_publication: NOT_ADMITTED
```

## Next executable tasks

1. Supply production-equivalent OpenAI, Anthropic, and DeepSeek candidate artifacts through the candidate schema without transferring provider API keys to StegVerse.
2. Execute one full Generation-2 seven-lane run and retain immutable candidate + governance/replay/reconstruction evidence.
3. Compare Generation-2 OpenAI/Anthropic measurements to immutable Generation-1 direct-key historical results as a separate architecture-overhead observation.
4. Feed the admitted Generation-2 result into `experiments/sv-cost-program/governed-ai-premium/` only after all seven lanes and proof requirements pass.
5. Continue SDK successor goal `SDK-OUTPUT-BOUNDARY-CANONICAL-004`: bind arbitrary provider output into the canonical sovereign transaction lifecycle so a canonical `manifest_receipt_id` can demonstrate Master Records replay/reconstruction while preserving provider credential non-possession.
6. Run the same path from exact immutable S and NS portable package artifacts once the parent package-artifact binding workstream releases them.
7. Before publication/release propagation, re-read destination handoffs for `GCAT-BCAT-Engine/Publisher`, `StegVerse-Labs/Site`, `admissibility-wiki`, and `stegguardian-wiki`.

## Claim boundary

This experiment measures one bounded deterministic reconstruction operation and the incremental cost/evidence behavior of credentialless StegVerse output-boundary governance. It does not establish fresh-inference equivalence, universal provider quality, universal provider economics, company ROI, universal savings, or Node Sovereign membership.

## Current claim

```yaml
active_goal: SV-COST-SEVEN-LANE-GEN2-003
state: IMPLEMENTED_VALIDATED_BLOCKED_ON_EXTERNAL_CANDIDATES
credential_authority_inside_stegverse_workload: NONE
protected_credential_authority: TV/TVC_OR_USER_EXISTING_PROVIDER_RELATIONSHIP
historical_five_lane_result_mutable: false
publication_admitted: false
sdk_successor_goal: SDK-OUTPUT-BOUNDARY-CANONICAL-004
```
