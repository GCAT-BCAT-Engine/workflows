# Research Objective 2 — Literal AI Cost Transparency and Disclosure Burden

## Relationship to the primary SV-COST analysis

The primary SV-COST experiment asks whether equivalent governed and ungoverned model executions produce the required deterministic result and, where evidence permits, what those executions cost.

This second research objective asks a different question:

> How difficult is it for an ordinary evaluator to discover the literal economic cost attributable to one AI inference?

It is an appendix research objective. It consumes observations from the primary experiment but does not modify its lane count, frozen behavioral evidence, or cost claims.

## Motivation

A published pricing card describes a pricing rule. It does not, by itself, establish the literal economic consequence of a particular request.

For a request to be economically auditable, the evaluator must be able to identify either:

1. the actual request-attributable charge directly; or
2. all exact metered quantities and all material billing rules necessary to reconstruct that charge without hidden assumptions.

The amount of work required to reach that result is itself a measurable property of the provider surface.

## Primary attribute

`ACTUAL_COST_DISCLOSURE_BURDEN`

Ordinal scale, lower is more transparent:

| Rating | Name | Operational definition |
|---:|---|---|
| 0 | DIRECT | Actual request-attributable cost is exposed with the request, receipt, or immediately linked transaction record. |
| 1 | ONE_STEP_DERIVABLE | Exact request usage is exposed and one public, version-bound pricing artifact is sufficient to reconstruct literal cost. |
| 2 | MULTI_SOURCE_DERIVABLE | Literal cost is reconstructable, but requires multiple provider-controlled documents/surfaces or non-obvious billing rules. |
| 3 | ACCOUNT_GATED | Reconstruction is possible only through authenticated billing/admin/account surfaces unavailable at the ordinary request surface. |
| 4 | SUPPORT_OR_EXTERNAL_RESEARCH_REQUIRED | Reconstruction requires provider support, substantial external research, or evidence beyond ordinary provider-controlled self-service surfaces. |
| 5 | NON_RECONSTRUCTABLE | After the research protocol is completed, literal request-attributable cost still cannot be reconstructed from available evidence. |

A provider MUST NOT receive rating 5 merely because the initial consumer UI omits cost. Rating 5 requires completion of the defined discovery protocol.

## Research protocol

For each provider/model:

1. Record the exact model identity if exposed.
2. Execute or reuse one bounded `SV-RECON-001` observation.
3. Inspect the immediate request/result surface for direct cost or exact usage.
4. Inspect provider-controlled pricing documentation linked from the product surface.
5. Inspect provider-controlled account/billing/usage surfaces available to the evaluator.
6. Record every additional navigation/search/research action needed to find material billing rules.
7. Identify every cost component that can change the final attributable amount.
8. Attempt exact reconstruction.
9. Stop when either exact reconstruction succeeds or the protocol is exhausted.
10. Preserve URLs/document identities, timestamps, screenshots or hashes where available, and the number/time cost of discovery steps.

## Measurements

Required fields include:

- `advertised_rate_present`
- `advertised_rate_surface`
- `actual_request_cost_directly_exposed`
- `request_usage_directly_exposed`
- `all_material_cost_components_disclosed`
- `research_steps_required`
- `provider_surfaces_consulted`
- `external_sources_required`
- `account_or_privilege_required`
- `time_to_reconstruct_minutes`
- `reconstructable_actual_cost`
- `unresolved_cost_components`
- `protocol_complete`
- `disclosure_burden_rating`

## Secondary quantitative measures

The ordinal rating is the primary comparative attribute. The paper should also report:

- discovery-step count;
- elapsed research time;
- number of distinct provider surfaces consulted;
- number of material billing components discovered outside the initial pricing surface;
- whether authentication or elevated billing privileges were required;
- whether exact request usage was exposed;
- whether actual cost was independently reconstructable;
- the difference, if any, between prominently advertised unit pricing and the complete set of cost-determining rules.

## Hypotheses

H1: Providers differ materially in the research burden required to reconstruct literal request-attributable cost.

H2: Public availability of a rate card does not reliably predict low actual-cost disclosure burden.

H3: Providers that expose exact request usage and version-bound billing rules will produce lower disclosure-burden scores than providers exposing only generalized or subscription-level pricing.

H4: Consumer-facing model surfaces may be behaviorally observable while remaining economically non-reconstructable.

## Interpretation

The study measures disclosure and reconstructability, not provider intent.

Evidence of materially omitted or obscured cost components may support a finding that a pricing presentation is misleading or deceptive in effect. Claims about intent require separate evidence and are outside this protocol unless directly established.

## Publication relationship

The resulting paper should be presented as a companion/appendix to the primary SV-COST analysis:

**Primary:** comparative inference/governance/cost analysis.

**Research Objective 2:** literal-cost transparency and the burden imposed on a user or evaluator attempting to discover actual economic consequence.

The two studies should be cross-referenced but reported separately so an unavailable cost is not silently converted into a fabricated estimate.
