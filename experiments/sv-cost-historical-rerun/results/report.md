# Historical sv-cost VAL-001 / BL-001 Rerun

Method status: BEST_AVAILABLE_RECONSTRUCTION

| Test | Valid | Native tokens | Observed cost | Latency s | Stop reason |
|---|---:|---:|---:|---:|---|
| VAL-001-RERUN | FALSE | 121 | $0.001107 | 2.83 | end_turn |
| BL-001-RERUN | FALSE | 4,248 | $0.061896 | 61.13 | max_tokens |

## BL-001 historical comparison

- Historical tokens: 4,169
- Rerun tokens: 4,248
- Token delta: +79 (+1.89%)
- Historical cost: $0.061659
- Rerun observed cost: $0.061896
- Cost delta: $+0.000237 (+0.38%)
- Historical latency: approximately 52.5s
- Rerun latency: 61.13s

## Reconstruction boundary

The exact historical request payload and exact connectivity prompt were not retained in the repository evidence currently available. This rerun preserves the known provider, model, output ceiling, task identity, output class, usage capture, latency capture, raw response retention, and receipt hashing. Results must be labeled control-envelope reproduction, not byte-identical replay.
