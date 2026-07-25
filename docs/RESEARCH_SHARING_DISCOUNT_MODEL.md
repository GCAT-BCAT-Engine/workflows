# Governed Research Sharing and Discount Model

## Purpose

The Governed Research Engine may offer a lower price when a user affirmatively shares selected research artifacts with StegVerse for governed reuse. The discount compensates the user for permitting reuse that may reduce future evidence collection, duplicate computation, validation, and methodological development costs.

The checkbox must be optional, unselected by default, granular, revocable prospectively, and separate from payment authorization.

## User-facing control

Recommended primary control:

```text
[ ] Share selected research artifacts with StegVerse and receive the displayed research-sharing discount.
```

Selecting the control opens a scope panel. The user chooses whether to share:

```text
protocol
source ledger
normalized dataset
computed results
research prompts and model exchanges
identity or attribution
```

Identity sharing must be a separate unchecked control. Sharing research must not require sharing identity.

## Required price display

Before payment, the interface must display:

```text
Standard price
Research-sharing discount
Final authorized price
What is being shared
Allowed uses
Excluded data classes
Revocation posture
License posture
```

The discount must be computed before Stripe Checkout creation and bound to the consent hash, pricing-policy reference, protocol hash, budget hash, and payment authorization.

## Processing route

```text
user develops research protocol
→ base cost plan
→ optional granular sharing consent
→ eligibility and reuse-value calculation
→ discounted cost plan
→ user reviews exact scope and price
→ consent receipt and pricing-adjustment receipt
→ Stripe Checkout Session
→ StegPay verifies payment evidence
→ research budget gate separately authorizes execution
```

## Insight and cost-reduction opportunities

Shared research can reduce future costs through:

- source and citation reuse after provenance verification;
- duplicate-topic and duplicate-dataset detection;
- reuse of validated extraction and coding methods;
- comparison of findings across independent studies;
- improved priors for cost and runtime estimation;
- reuse of deterministic computation and test fixtures;
- discovery of contradictions, replications, and adjacent research questions;
- aggregate methodological benchmarking;
- identification of under-researched populations, periods, or variables.

A shared artifact is never accepted as true merely because it was paid for, submitted, or previously used. Every future use preserves provenance, consent scope, evidence posture, and validation status.

## Discount principles

```text
Discount is consideration for governed reuse permission.
Discount is not a purchase of ownership.
Discount does not eliminate attribution rights where selected.
Discount does not authorize public publication unless separately selected.
Discount does not permit use outside the recorded allowed-use scope.
Payment does not erase revocation or exclusion rules.
```

Discounts may be percentage-based, fixed, or issued as compute credit. The pricing policy should estimate actual ecosystem value rather than apply one universal percentage. Relevant factors include:

- expected reusable compute;
- source-acquisition cost avoided;
- uniqueness of the dataset;
- completeness and validation quality;
- breadth of allowed reuse;
- whether public redistribution is authorized;
- sensitivity and restriction burden;
- expected future demand.

## Consent and revocation

Consent must be versioned and hash-bound. A later change creates a new consent record rather than silently rewriting the earlier record.

Prospective revocation stops new uses after the effective revocation time. It does not falsify historical receipts or necessarily retract artifacts already incorporated into completed, independently reproducible outputs. The user-facing policy must explain these limits before consent.

Restricted third-party material, privileged information, direct identifiers, sensitive health or financial information, trade secrets, and data concerning minors must be excluded by default unless a separate lawful and governed intake process permits them.

## Cross-research use boundary

```text
shared artifact
→ consent and license validation
→ provenance and integrity validation
→ relevance matching
→ duplication and contamination review
→ admissibility decision for the new protocol
→ reuse with citation and lineage
```

A prior user's result may inform a new hypothesis, comparison, prior, or validation test. It cannot automatically become ground truth or replace independent evidence required by the new protocol.

## Required records

- `research-sharing-consent.json`
- `research-sharing-discount.json`
- consent receipt
- pricing-adjustment receipt
- Stripe payment evidence
- reuse-event receipts for every later research project
- revocation or scope-change receipts

## Governing boundary

```text
Sharing consent grants only the recorded reuse permission.
Pricing adjustment changes price only.
Stripe records payment.
StegPay verifies payment evidence.
Governance decides research admissibility and execution.
No checkbox transfers ownership, establishes truth, or grants publication authority beyond its explicit scope.
```
