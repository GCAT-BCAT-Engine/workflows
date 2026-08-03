# StegVerse Best-Case Cost Analysis

Status: **PRELIMINARY COMMERCIAL ESTIMATE — BEST-CASE PLANNING MODEL**

Program: `SV-COST-MAJOR-GOAL-001`

Canonical issue: `#13`

## Purpose

This analysis provides an immediate, defensible estimate for a prospective customer who asks what StegVerse may cost relative to current OpenAI or Anthropic spend.

It is designed for first-call qualification and pilot scoping. It is not a production quote, invoice reconciliation, or proven customer-specific ROI result.

## Primary variables

Let:

- `B` = current monthly OpenAI and Anthropic spend
- `g` = projected gross-savings rate
- `o` = StegVerse operating-cost rate as a share of current provider spend
- `f` = StegVerse commercial fee as a share of independently verified savings

Then:

```text
gross_savings = B × g
stegverse_operating_cost = B × o
stegverse_commercial_fee = gross_savings × f
customer_net_savings = gross_savings - stegverse_commercial_fee
customer_net_savings_after_estimated_operating_cost = gross_savings - stegverse_commercial_fee - stegverse_operating_cost
```

## Planning scenarios

| Scenario | Gross savings rate | SV operating-cost rate | SV fee share of verified savings | Intended use |
|---|---:|---:|---:|---|
| Conservative | 10% | 3% | 10% | Initial downside screen |
| Expected | 25% | 2% | 15% | Working commercial estimate |
| Best case | 50% | 1% | 20% | Upper planning case before customer-specific measurement |

The best-case model is intentionally bounded at 50% gross savings for an initial customer estimate, even though the deterministic synthetic pilot produced a higher modeled result. The synthetic pilot must not be treated as customer-specific production evidence.

## Best-case formula

For the best-case scenario:

```text
gross_savings = 0.50 × B
stegverse_operating_cost = 0.01 × B
stegverse_commercial_fee = 0.20 × gross_savings = 0.10 × B
customer_net_savings_before_operating_cost = 0.40 × B
customer_net_savings_after_estimated_operating_cost = 0.39 × B
```

Therefore, under this planning model:

- the customer retains approximately **39% of current provider spend** as estimated net monthly savings after the modeled StegVerse fee and narrow operating cost;
- StegVerse receives a commercial fee equal to approximately **10% of current provider spend** when the full 50% savings case is independently verified;
- narrow StegVerse operating cost is estimated at approximately **1% of current provider spend**.

## Monthly estimates

| Current provider spend | Gross savings at 50% | Estimated SV operating cost at 1% | SV fee at 20% of savings | Customer net savings after fee and operating cost |
|---:|---:|---:|---:|---:|
| $10,000 | $5,000 | $100 | $1,000 | $3,900 |
| $50,000 | $25,000 | $500 | $5,000 | $19,500 |
| $100,000 | $50,000 | $1,000 | $10,000 | $39,000 |
| $500,000 | $250,000 | $5,000 | $50,000 | $195,000 |
| $1,000,000 | $500,000 | $10,000 | $100,000 | $390,000 |

## Annualized estimates

| Current monthly provider spend | Annual provider spend | Annual gross savings | Annual SV operating cost | Annual SV fee | Annual customer net savings after fee and operating cost |
|---:|---:|---:|---:|---:|---:|
| $10,000 | $120,000 | $60,000 | $1,200 | $12,000 | $46,800 |
| $50,000 | $600,000 | $300,000 | $6,000 | $60,000 | $234,000 |
| $100,000 | $1,200,000 | $600,000 | $12,000 | $120,000 | $468,000 |
| $500,000 | $6,000,000 | $3,000,000 | $60,000 | $600,000 | $2,340,000 |
| $1,000,000 | $12,000,000 | $6,000,000 | $120,000 | $1,200,000 | $4,680,000 |

## Commercial structure

### Pilot pricing

| Pilot type | Scope | Preliminary price range |
|---|---|---:|
| Small pilot | Up to 100,000 governed events, one provider, one workflow, 30 days | $2,500–$5,000 |
| Standard enterprise pilot | Up to 1 million events, one provider, paired native/governed lanes, 30–60 days | $10,000–$25,000 |
| Dual-provider pilot | OpenAI and Anthropic, four primary lanes, same stream and business-outcome contract, 60–90 days | $25,000–$50,000 |

A pilot fee may be credited toward a production agreement when specified in the signed commercial terms.

### Production pricing concept

The expected production model is:

```text
base_platform_fee
+ governed_transition_usage
+ verification_and_receipt_usage
+ storage_and_custody
+ replay_and_recovery_usage
+ exceptional_human_review
```

The preferred early commercial structure is:

```text
commercial_fee = min(contracted_cap, 10% to 20% of independently verified savings)
```

This aligns StegVerse compensation with measured customer value rather than token volume alone.

## Synthetic calibration reference

The deterministic stream pilot used the following narrow synthetic unit assumptions:

- StegVerse admission: `$0.00005` per event
- receipt generation: `$0.00001` per event
- verification: `$0.00002` per event
- replay: `$0.00002` per replay event

The modeled narrow governance cost for a normal admitted transition was therefore:

```text
$0.00005 + $0.00001 + $0.00002 = $0.00008 per governed transition
```

At one million transitions, that narrow variable-cost model equals `$80` before fully burdened infrastructure, storage, maintenance, support, engineering, security, and human-review costs.

This calibration supports the expectation that StegVerse may be a low marginal-cost governance layer. It is not a production price.

## Required first-call inputs

A first estimate requires six customer-provided inputs:

1. current monthly OpenAI and Anthropic spend;
2. monthly request or event volume;
3. average retries per successful business outcome;
4. percentage of work requiring human review;
5. estimated cost of failed or incorrect execution;
6. frequency of regenerating prior results instead of replaying or reusing governed state.

## Immediate call script

> As a preliminary best-case estimate, we model StegVerse operating cost at approximately 1% of your current model spend, with commercial pricing tied to no more than 20% of independently verified savings. If your current OpenAI or Anthropic spend is $100,000 per month and the governed workload verifies 50% gross savings, the planning model is approximately $1,000 in narrow StegVerse operating cost, a $10,000 StegVerse fee, and about $39,000 in monthly net savings retained by your organization. The estimate must be confirmed against your actual event stream, failure burden, replay opportunity, provider charges, and StegVerse runtime meter.

## Claim boundaries

This document may support a preliminary best-case estimate only.

It does not establish:

- that any customer will save 50%;
- that StegVerse production operating cost will equal exactly 1% of provider spend;
- that synthetic unit assumptions are invoice evidence;
- that token reductions prove compute, energy, capability, or profit reduction;
- that all workloads are eligible for replay or reconstruction;
- that prevented failures have a specific monetary value without customer evidence.

Before a binding production quote, the customer-specific analysis must include observed provider charges, metered StegVerse runtime costs, workload identity, outcome equivalence, retries, failures, human-review burden, storage, support, and replay/reuse opportunities.

## Decision rule

Use the best-case model for first-call qualification only.

Proceed to a paid pilot when:

- the customer can provide spend and workload data;
- the same business outcome can be compared across native and governed lanes;
- all failures and retries remain in the ledger;
- StegVerse local costs can be metered;
- savings can be independently verified.

Do not issue a guaranteed savings commitment from this estimate.
