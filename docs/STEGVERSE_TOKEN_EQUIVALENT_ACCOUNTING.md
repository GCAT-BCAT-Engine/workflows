# StegVerse Token-Equivalent Accounting

## Purpose

Provide a comparable baseline for StegVerse-only, StegVerse/OpenAI, and StegVerse/Anthropic execution without treating a missing provider invoice as zero resource cost or double-counting provider-internal overhead.

## Canonical information-flow metric

Each lane records both provider-native billing tokens, when available, and a canonical cross-lane count using the pinned `cl100k_base` tokenizer.

Measured information-flow fields:

- canonical task-input tokens;
- canonical governance-context tokens;
- canonical repository-context tokens;
- canonical candidate-output tokens;
- canonical governance-ledger tokens;
- canonical receipt/reconstruction-output tokens;
- serialized input and output byte counts;
- SHA-256 hashes for every canonical payload.

## Cost views

1. **Native billed cost** — actual provider invoice derived from native token usage and the declared rate table.
2. **Token-equivalent counterfactual cost** — canonical input and output counts priced at the same OpenAI or Anthropic rate table.
3. **Observable external overhead** — workflow runtime, deterministic validation, hashing, artifact storage, repository writes, formal verification, retries, branches, and declared human review.
4. **Actual marginal infrastructure cost** — separately reported when directly observable.

Provider token pricing is treated as inclusive of provider-internal infrastructure and safety overhead unless a provider exposes a separable charge. Those internal costs must not be added again.

## StegVerse-only boundary

A provider-denied StegVerse-only run may produce a capability, governance, or reconstruction record without producing a theorem proof. It must report:

- actual normalized input/output information flow;
- actual deterministic runtime and external overhead;
- `solve_cost_usd: null` when no native reasoning engine performs the task;
- an explicit block reason;
- no fabricated proof or success claim.

## Comparability rule

The primary cross-lane baseline is:

> canonical information in/out + separately observable external governance overhead

Native provider token counts remain authoritative billing receipts. Canonical counts are the common comparison surface, not replacements for billed usage.
