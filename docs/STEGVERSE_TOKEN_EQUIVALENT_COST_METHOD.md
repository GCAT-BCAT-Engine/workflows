# StegVerse Token-Equivalent Cost Method

## Purpose

The StegVerse-only lane is compared to StegVerse/OpenAI and StegVerse/Anthropic first by information flow, then by execution overhead. It must not be represented as zero-cost merely because no provider invoice exists.

## Comparable baseline

Every lane reports two token views:

1. **Provider-native tokens** — the usage values returned by OpenAI or Anthropic when a provider is used.
2. **Canonical token-equivalent units** — all lane inputs and outputs serialized to canonical UTF-8 text and tokenized with one pinned reference tokenizer and version.

The canonical token-equivalent view is the cross-lane comparison surface. Provider-native token counts remain the billing receipt surface.

## Upstream and downstream units

For each lane, record:

- `task_input_equivalent_tokens`: problem statement and required output contract.
- `governance_input_equivalent_tokens`: declarations, policies, admissibility constraints, routing instructions, and verification requirements introduced by StegVerse.
- `context_input_equivalent_tokens`: retrieved repository evidence and prior state supplied to execution.
- `candidate_output_equivalent_tokens`: proof, estimate, or answer candidate.
- `governance_output_equivalent_tokens`: decision ledger, claim boundary, uncertainty declarations, and escalation decision.
- `evidence_output_equivalent_tokens`: receipts, hashes, verification records, and reconstruction metadata expressed in canonical serialized form.

Total normalized input is the sum of the three input classes. Total normalized output is the sum of the three output classes.

## Overhead separation

Token-equivalent usage is the baseline. The following are reported separately rather than silently folded into token counts:

- deterministic validator CPU time;
- workflow runner time;
- repository reads and writes;
- artifact bytes stored;
- hash operations;
- formal-verification runtime;
- retry and branch counts;
- human review time, when present;
- actual infrastructure charge or allocated marginal cost.

## Counterfactual provider pricing

The StegVerse-only lane reports two counterfactual token prices:

- `openai_equivalent_token_cost_usd`: canonical input/output equivalents priced at the declared OpenAI input/output rates;
- `anthropic_equivalent_token_cost_usd`: canonical input/output equivalents priced at the declared Anthropic input/output rates.

These values are comparison baselines, not invoices and not actual StegVerse spend.

## Total comparable cost views

Each lane exposes:

1. `token_baseline_cost_usd` — provider-native billed cost for provider lanes, or counterfactual canonical-token cost for StegVerse-only.
2. `governance_overhead_cost_usd` — measurable compute, storage, verification, and review overhead not already included in provider billing.
3. `total_comparable_cost_usd` — baseline plus separately measured overhead.
4. `actual_cash_cost_usd` — actual marginal invoice when observable.

OpenAI and Anthropic token prices may already internalize model training, serving infrastructure, orchestration, safety systems, and provider operational overhead. Those internal components are not independently observable and must not be double-counted. StegVerse overhead is added only for work performed outside the provider response path.

## Interpretation rule

The primary comparison is:

`normalized information in/out + external governance overhead`

not:

`provider invoice versus zero-dollar local execution`.

A StegVerse-only run that cannot generate the required candidate still records its consumed input equivalents, decision/receipt output equivalents, and execution overhead, but its solve result remains `BLOCKED` and its solve cost remains null.

## Required receipt fields

- tokenizer name and pinned version;
- canonical serialization version;
- input/output class token counts;
- provider-native usage when applicable;
- declared rate table and timestamp;
- actual cash cost;
- counterfactual equivalent costs;
- measured overhead components;
- receipt hashes for every canonical input and output artifact.
