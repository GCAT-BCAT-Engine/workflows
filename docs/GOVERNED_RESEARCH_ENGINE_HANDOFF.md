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
research_engine/schemas/triadic-deliberation.schema.json
research_engine/schemas/research-budget.schema.json
research_engine/schemas/math-solver-compute-request.schema.json
research_engine/schemas/research-result.schema.json
research_engine/costing/pricing_registry.example.json
research_engine/costing/cost_estimator.py
research_engine/costing/budget_gate.py
research_engine/examples/tidc-cost-plan.example.json
research_engine/examples/tidc-budget.example.json
research_engine/examples/tidc-math-solver-request.example.json
.github/workflows/governed-research-plan.yml
.github/workflows/governed-research-stage-gate.yml
```

The planning workflow is deliberately non-executing. It produces:

```text
cost-plan.json
cost-estimate.json
planning-receipt.json
```

It rejects `execution_authority=true` and grants no provider-call, spending, repository-mutation, conclusion, or publication authority.

The stage-gate workflow now evaluates:

```text
named stage exists
→ stage status is authorized
→ requested amount fits stage authorization
→ projected cumulative spend fits hard limit
→ projected spend fits automatic-stop threshold
→ hash-bound budget-gate receipt
```

An `ALLOW` decision is stage-specific and amount-specific. It cannot authorize another stage, provider, publication, conclusion, or repository mutation.

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

## TIDC-001 first-case posture

The first Math Solver request contract now asks for:

```text
point estimates
standard errors
confidence intervals
effect sizes
diagnostics
sensitivity tests
negative controls
missing-data analysis
reproducibility receipt
```

The example remains non-executable because the Math Solver stage is explicitly `not_authorized` and its authorization reference is pending. This is intentional evidence that the budget gate fails closed before compute.

## Required next build

1. Add OpenAI and Anthropic role-separated prompts and a triadic deliberation runner.
2. Record provider token usage and actual provider cost.
3. Add a dated pricing-registry loader that fails closed on example, unknown, or stale pricing.
4. Add stage reservation mutation receipts and cumulative-spend reconciliation.
5. Add the Math Solver adapter that validates request, budget-gate receipt, dataset hashes, and protocol hash before dispatch.
6. Implement deterministic pilot computations for TIDC-001.
7. Add independent result validation and conclusion-classification gates.
8. Add actual-cost reconciliation and unused-budget release receipts.
9. Connect StegScholar custody and Site progressive publication manifests.
10. Run the first complete artifact-only TIDC-001 research cycle before any paid live execution.

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
