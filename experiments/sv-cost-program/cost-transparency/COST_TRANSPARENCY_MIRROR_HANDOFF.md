# AI Cost Transparency Research Mirror Handoff

Status: **RESEARCH OBJECTIVE IMPLEMENTED — PROVIDER DISCLOSURE PROTOCOL EXECUTION PENDING**

## Canonical authority

```text
repository: GCAT-BCAT-Engine/workflows
branch: main
parent_program: experiments/sv-cost-program/eleven-lane-results/ELEVEN_LANE_MIRROR_HANDOFF.md
research_objective_id: SV-COST-TRANSPARENCY-001
relationship: APPENDIX_RESEARCH_OBJECTIVE_TO_SV_COST_ANALYSIS
```

## Research question

How much effort is required for a reasonable evaluator to discover the literal, request-attributable economic cost of an AI inference, and how should that disclosure burden affect model/provider evaluation?

## Core premise

A public rate card is not treated as equivalent to actual request-attributable cost. Cost transparency requires that the literal economic consequence of a request be exposed directly or be exactly reconstructable from provider-exposed evidence.

Where an evaluator must perform additional research to discover material cost components, that research burden is itself an observable product attribute.

## Proposed evaluation attribute

`ACTUAL_COST_DISCLOSURE_BURDEN`

The attribute measures the work necessary to discover and reconstruct the literal attributable cost of one inference.

Initial ordinal scale:

```text
0 DIRECT
  Actual request cost is displayed with the request or receipt.

1 ONE_STEP_DERIVABLE
  Exact request usage is exposed and one public, version-bound pricing artifact is sufficient.

2 MULTI_SOURCE_DERIVABLE
  Exact cost requires combining multiple provider-controlled sources or non-obvious billing rules.

3 ACCOUNT_GATED
  Literal request cost or sufficient usage data exists only behind account/billing/admin surfaces.

4 SUPPORT_OR_EXTERNAL_RESEARCH_REQUIRED
  Provider surfaces are insufficient; evaluator must consult support, secondary documentation, or perform substantial external research.

5 NON_RECONSTRUCTABLE
  Literal request-attributable cost cannot be determined from available provider evidence.
```

Lower is more transparent.

## Evidence dimensions

For every provider/model observation, record:

```text
advertised_rate_present
advertised_rate_surface
actual_request_cost_directly_exposed
request_usage_directly_exposed
all_material_cost_components_disclosed
research_steps_required
provider_surfaces_consulted
external_sources_required
account_or_privilege_required
time_to_reconstruct_minutes
reconstructable_actual_cost
unresolved_cost_components
disclosure_burden_rating
```

## Claim discipline

Do not infer intent from opacity alone. Measure observable disclosure behavior, omitted material cost components, reconstruction burden, and whether a literal request-attributable cost can be established.

The study may characterize a pricing presentation as deceptive or misleading only where the evidence supports that the presented cost information materially differs from, omits, or obscures the literal economic consequence being represented.

## Relationship to current eleven-lane experiment

The current eleven-lane experiment remains unchanged.

This research objective appends a second paper/objective to the cost analysis and may consume its provider observations as inputs. It does not renumber lanes, alter frozen behavioral evidence, or convert missing cost evidence into estimated cost.

## Immediate implementation goals

1. Add a machine-readable transparency observation schema.
2. Add a provider research log format that preserves every discovery step and source.
3. Add a scoring function for `ACTUAL_COST_DISCLOSURE_BURDEN`.
4. Seed observations for OpenAI, Anthropic, DeepSeek, GLM Hosted, and supplemental Perplexity using only evidence already acquired.
5. Keep unknown values unknown; do not convert lack of evidence into an accusation of intent.
6. Produce a paper appendix once enough provider observations exist for comparative analysis.

## Downstream publication candidates

When research reaches release-ready state, verify propagation applicability to:
- StegVerse-Labs/Site
- GCAT-BCAT-Engine/Publisher
- StegVerse-Labs/admissibility-wiki
- StegVerse-Labs/stegguardian-wiki


## Implemented source — 2026-09-03

Issue: #58

Installed:
- `research-objective.md`
- `transparency-observation.schema.json`
- `research-log.schema.json`
- `score_disclosure_burden.py`
- `tests/test_score_disclosure_burden.py`
- `seed-observations.json`
- `task-state.json`

The scoring implementation fail-closes incomplete research: omission of cost on an initial UI surface does not automatically receive a final `5 NON_RECONSTRUCTABLE` rating. A final 5 requires completion of the research protocol.

Existing OpenAI, Anthropic, DeepSeek, Z.ai/GLM, and Perplexity observations are seeded only as prior evidence references with `NOT_SCORED_PROTOCOL_INCOMPLETE`. No provider has been assigned a final disclosure-burden score from the current UI observations alone.

### Remaining research execution

For each provider, execute the research protocol and preserve:
- discovery-step count;
- elapsed research time;
- every provider-controlled surface consulted;
- whether authentication/elevated billing access was necessary;
- every material cost component discovered;
- whether literal request-attributable cost became exactly reconstructable.

Only after that evidence is complete should final comparative ratings and the companion paper findings be produced.
