# Anthropic candidate source evidence — 2026-08-17

Provider: Anthropic / Claude
UI model label observed in user-supplied screenshot: `Opus 5 High`
Task: `SV-RECON-001`
Provider API key transferred to StegVerse: `false`
Provider response ID: not exposed
Provider token counts: not exposed
Provider reported cost: not exposed
Provider latency: not exposed

## User-supplied provider response transcription

- E01 credit 25 — ALLOW → balance 125
- E02 debit 40 — ALLOW → balance 85
- E03 risk_add 2 — ALLOW → risk 3
- E04 debit 100 — DENY (85 − 100 = −15, below minimum 0); no state change
- E05 risk_add 3 — DENY (3 + 3 = 6, above maximum 5); no state change
- E06 debit 10 — ALLOW → balance 75

Final state

- Balance: 75
- Risk score: 3
- Standing: active

Provider note supplied by the user:

> Note that E05’s denial is what let E06 through unimpeded on the risk side — had the risk cap been higher, risk would sit at 6, but nothing in the stated rules gates debits on risk score, only on standing. If risk is meant to block debits above some threshold, that rule isn’t in the spec as given.

## Structured transcription note

The candidate schema requires `applied_count` and `denied_count`. The provider response did not separately state those totals, so the installed candidate deterministically derives them from the six explicit decisions: four ALLOW and two DENY. No provider usage, cost, latency, response ID, API model identifier, or API credential was inferred or fabricated.

Installed candidate: `../candidate-inputs/anthropic.json`
