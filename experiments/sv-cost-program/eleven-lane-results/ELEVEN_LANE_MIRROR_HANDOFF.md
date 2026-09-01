# SV-COST Eleven-Lane Mirror Handoff

Status: ACTIVE — SOURCE TRANSITION FROM FROZEN NINE-LANE BASELINE

## Canonical authority

```text
repository: GCAT-BCAT-Engine/workflows
branch: feat/sv-cost-eleven-lane
experiment_id: SV-COST-ELEVEN-LANE-RESULTS-001
generation: GENERATION_3_CREDENTIALLESS_PLUS_SOVEREIGN_MODEL_BOUNDARY
predecessor: experiments/sv-cost-program/nine-lane-results/SV_COST_NINE_LANE_MIRROR_HANDOFF.md
credential_authority: TV/TVC
non-TV/TVC protected secret/token authority: FORBIDDEN
```

The nine-lane Generation-2 result is historical and must remain unchanged. This directory is the successor surface.

## Goal

Extend the comparison from 9 lanes to 11 lanes by adding exactly:

10. GLM-5.3-Flash Hosted
11. GLM-5.3-Flash Sovereign

The hosted and sovereign GLM lanes are intentionally distinct because their credential, custody, network, privacy, and cost bases differ.

## Credential boundary

No provider API key is required to execute the comparison harness itself.

Existing external-provider lanes continue to consume committed external candidate outputs. StegVerse does not possess or consume provider API keys for those lanes.

GLM hosted may operate in either of two states:

```text
PRE_VAULT: external candidate output only; no StegVerse-held Z.ai credential
POST_VAULT: TV/TVC-authorized hosted API execution; no direct repository/userland secret possession
```

GLM sovereign requires no vendor API credential. It requires an eligible sovereign inference runtime and StegVerse node/runtime identity/authority.

## Eleven lanes

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

## Cost basis classes

External hosted candidate lanes may publish bounded cost only from admissible provider evidence already defined by Generation 2.

GLM hosted cost basis:
- provider-reported request cost; or
- provider-reported exact input/output tokens plus a bound versioned official rate card; or
- provider-observed subscription/quota allocation when explicitly labeled non-marginal.

GLM sovereign cost basis:
- measured runtime duration;
- measured or bounded energy consumption;
- hardware amortization;
- storage/network/runtime overhead;
- successful equivalent outcome denominator.

Do not represent the sovereign lane using hosted token prices.

## Current execution state

```text
lanes 1-9: inherited source/evidence from frozen Generation 2
lane 10 hosted: SOURCE_DEFINED; live hosted execution blocked until external candidate evidence or TV/TVC Vault authorization
lane 11 sovereign: SOURCE_DEFINED; live execution blocked until eligible sovereign runtime is available
provider API key transfer to StegVerse: false
```

## Remaining files/modules to install

Destination: `GCAT-BCAT-Engine/workflows`

- eleven-lane runner derived from Generation-2 runner without mutating frozen nine-lane artifacts
- eleven-lane schema validator
- GLM hosted candidate schema/input record
- GLM sovereign runtime evidence schema/input record
- GLM hosted cost evidence record
- GLM sovereign compute-cost evidence record
- local validation receipt
- hosted observer task/workflow update for 11-lane cardinality
- publication integration after evidence gates pass

Downstream publication/propagation, once release-ready, must re-read current handoffs in:
- StegVerse-Labs/Site
- GCAT-BCAT-Engine/Publisher
- StegVerse-Labs/admissibility-wiki
- StegVerse-Labs/stegguardian-wiki

## Claim boundary

Source definition of the two new lanes does not claim live Z.ai API execution, sovereign model execution, provider credential availability, cost completion, hosted proof PASS, or publication readiness.
