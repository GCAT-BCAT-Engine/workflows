# Governed Research Engine Handoff

## Goal

Build a reusable pay-to-research route that converts a witnessed topic into a user-approved research protocol, estimates cost before execution, conducts bounded evidence collection and computation, calculates uncertainty, and emits reproducible conclusions and publication artifacts.

## Operating route

```text
user witness statement
→ constructive research LLM
→ adversarial research LLM
→ reconciled protocol candidate
→ user approval
→ costed execution plan
→ user budget authorization
→ governed evidence collection
→ dataset construction
→ Math Solver analysis
→ error and uncertainty calculation
→ independent validation
→ conclusion classification
→ Site / StegScholar publication
→ recurring evidence refresh
```

## Repository roles

```text
StegVerse-Labs/StegScholar
  topic records, protocols, source ledgers, datasets, conclusions, publication continuity

GCAT-BCAT-Engine/workflows
  provider orchestration, planning, pricing registry, budget gates, sandbox execution, receipts

GCAT-BCAT-Engine/workflows/math_solver
  mathematical formalization, statistical computation, diagnostics, error calculation, reproducibility

StegVerse-Labs/Site
  public progressive projection; not proof authority
```

## Implemented foundation

```text
research_engine/schemas/research-run.schema.json
research_engine/costing/pricing_registry.example.json
research_engine/costing/cost_estimator.py
research_engine/examples/tidc-cost-plan.example.json
.github/workflows/governed-research-plan.yml
```

The planning workflow is deliberately non-executing. It produces:

```text
cost-plan.json
cost-estimate.json
planning-receipt.json
```

It rejects `execution_authority=true` and grants no provider-call, spending, repository-mutation, conclusion, or publication authority.

## Cost model

For stage `i`:

```text
expected_i = fixed_i + units_i × unit_cost_i × (1 + retry_rate_i)
sigma_i = expected_i × uncertainty_fraction_i
```

For the full research plan:

```text
expected_total = Σ expected_i
sigma_total = sqrt(Σ sigma_i²)
high_confidence_cost = expected_total + z × sigma_total
```

The plan is within budget only if the high-confidence cost does not exceed the user's hard limit.

## Required next build

1. Add a triadic-deliberation request and response schema.
2. Add OpenAI and Anthropic role-separated prompts: formulation versus adversarial review.
3. Record provider token usage and actual provider cost.
4. Add a dated pricing-registry loader that fails closed on example, unknown, or stale pricing.
5. Add budget reservation, stage authorization, cumulative spend, and automatic-stop records.
6. Add a Math Solver compute-request schema and adapter.
7. Add result schemas for estimates, standard errors, confidence intervals, diagnostics, sensitivity tests, negative controls, and conclusion classes.
8. Add an execution workflow separate from the planning workflow.
9. Add actual-cost reconciliation and unused-budget release receipts.
10. Connect TIDC-001 as the first end-to-end research case.

## Required authority boundaries

```text
witness statement != established fact
LLM agreement != validation
research protocol != execution authority
cost estimate != invoice
budget approval != scientific validity
provider output != evidence
Math Solver output != accepted conclusion
statistical significance != causal or practical importance
Site publication != proof authority
```

## Commercial rule

```text
Pay for an inspectable research process, not an answer.
```

The user must retain all completed artifacts at every paid stage and may halt before authorizing later stages.
