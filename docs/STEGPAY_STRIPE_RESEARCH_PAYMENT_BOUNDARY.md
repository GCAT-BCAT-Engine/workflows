# StegPay / Stripe Research Payment Boundary

## Purpose

Connect governed research budgets to verified payment evidence without allowing Stripe, StegPay, or payment completion to grant scientific, publication, or execution authority.

## Route

```text
approved research protocol
→ costed stage plan
→ user selects stage and hard amount
→ Stripe Checkout or PaymentIntent
→ Stripe webhook
→ StegPay verifies signature, amount, currency, status, and metadata
→ StegPay emits normalized payment evidence
→ research budget gate binds evidence to protocol_hash, budget_hash, research_id, and stage_id
→ governance evaluates stage authority
→ execution gate may ALLOW only the named stage and bounded amount
→ actual cost is reconciled
→ unused amount is released, credited, or refunded under policy
```

## Required Stripe metadata

```json
{
  "service": "governed_research",
  "research_id": "TIDC-001",
  "stage_id": "math_solver_analysis",
  "protocol_hash": "sha256:...",
  "budget_hash": "sha256:...",
  "authorization_id": "RPA-TIDC-001-004",
  "source": "stegverse_research_engine"
}
```

## Required boundaries

```text
payment completed != execution authority
payment verified != protocol approval
payment amount != permitted spend above the named stage ceiling
Stripe metadata != trusted until signature verification succeeds
StegPay evidence != entitlement
budget authorization != scientific validity
refund eligibility != conclusion validity
```

## Fail-closed conditions

- missing or invalid Stripe signature;
- stale webhook timestamp;
- unsupported event type or unpaid status;
- missing research_id, stage_id, protocol_hash, budget_hash, or authorization_id;
- metadata mismatch against the current approved protocol or budget;
- currency mismatch;
- amount below the required reservation or above the authorized stage ceiling;
- duplicate provider event without idempotent replay classification;
- event attempts to create execution authority or scientific entitlement;
- revoked, superseded, or expired protocol/budget hash;
- automatic-stop threshold already reached.

## Settlement model

StegPay verifies the external payment fact. The research engine maintains the stage reservation and actual-cost ledger. StegFinCo or another authorized financial effect layer controls refunds, credits, transfers, and settlement.

Each stage must preserve:

```text
quoted amount
paid amount
reserved amount
actual cost
failed-call cost
released amount
credited amount
refunded amount
remaining research balance
```

## Initial implementation target

1. Extend StegPay with a `governed_research_stage` Stripe event normalizer.
2. Add Checkout Session creation through an authorized server-side service; never expose Stripe secret keys in Site or browser code.
3. Verify webhook events in StegPay.
4. Emit `research-payment-authorization` records into the research engine.
5. Require a separate governance and stage-execution decision after payment verification.
6. Reconcile actual provider and compute costs after every stage.
7. Release or refund unused balances according to an explicit policy receipt.

No live payment processing is claimed until Stripe test-mode Checkout creation, signed webhook receipt, idempotent event handling, budget binding, stage gating, and refund/release paths are observed end to end.
