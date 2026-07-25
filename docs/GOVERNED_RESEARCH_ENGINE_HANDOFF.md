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
→ Stripe payment for named stage
→ StegPay verified payment evidence
→ separate governance and execution gate
→ governed evidence collection
→ dataset construction
→ Math Solver analysis
→ error and uncertainty calculation
→ independent validation
→ conclusion classification
→ Site / StegScholar publication
→ actual-cost reconciliation
→ unused-balance release, credit, or refund
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

StegVerse-Labs/StegPay
  Stripe signature verification, payment-event normalization, idempotent payment evidence

StegFinCo or authorized financial effect layer
  refunds, credits, settlement, and treasury effects

StegVerse-Labs/Site
  public progressive projection; not proof authority and never a holder of Stripe secret keys
```

## Implemented foundation

```text
research_engine/schemas/research-run.schema.json
research_engine/schemas/triadic-deliberation.schema.json
research_engine/schemas/research-budget.schema.json
research_engine/schemas/math-solver-compute-request.schema.json
research_engine/schemas/research-result.schema.json
research_engine/schemas/research-payment-authorization.schema.json
research_engine/costing/pricing_registry.example.json
research_engine/costing/cost_estimator.py
research_engine/costing/budget_gate.py
research_engine/examples/tidc-cost-plan.example.json
research_engine/examples/tidc-budget.example.json
research_engine/examples/tidc-math-solver-request.example.json
.github/workflows/governed-research-plan.yml
.github/workflows/governed-research-stage-gate.yml
docs/STEGPAY_STRIPE_RESEARCH_PAYMENT_BOUNDARY.md
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

## Payment boundary

```text
Stripe confirms payment status.
StegPay verifies signature, status, amount, currency, metadata, and event identity.
The research engine binds verified payment evidence to research_id, stage_id, protocol_hash, and budget_hash.
Governance separately decides whether the named stage may execute.
StegFinCo or another authorized financial effect layer controls refund, credit, and settlement effects.
```

Required governed-research Stripe metadata:

```text
service = governed_research
research_id
stage_id
protocol_hash
budget_hash
authorization_id
source = stegverse_research_engine
```

Payment verification creates evidence only. It never creates execution authority, scientific validity, publication authority, guaranteed results, or permission to exceed the named stage ceiling.

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
4. Implement authorized server-side Stripe Checkout Session creation for one named research stage.
5. Extend StegPay normalization and webhook tests for `governed_research` metadata, amount/currency checks, and idempotent replay.
6. Add payment-to-budget binding and a separate governance decision after payment verification.
7. Add stage reservation mutation receipts and cumulative-spend reconciliation.
8. Add the Math Solver adapter that validates request, payment evidence, budget-gate receipt, dataset hashes, and protocol hash before dispatch.
9. Implement deterministic pilot computations for TIDC-001.
10. Add independent result validation and conclusion-classification gates.
11. Add actual-cost reconciliation and unused-budget release, credit, or refund receipts.
12. Connect StegScholar custody and Site progressive publication manifests.
13. Run the first complete Stripe test-mode, artifact-only TIDC-001 cycle before any live paid execution.

## Required authority boundaries

```text
witness statement != established fact
LLM agreement != validation
research protocol != execution authority
cost estimate != invoice
Stripe payment != stage authority
StegPay verification != entitlement
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
