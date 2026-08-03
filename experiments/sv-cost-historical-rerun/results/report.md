# Historical sv-cost VAL-001 / BL-001 Rerun

Method status: BEST_AVAILABLE_CONTROL_ENVELOPE_REPRODUCTION

| Test | Transport | Output class | Complete | Native tokens | Observed cost | Latency s | Stop reason |
|---|---:|---:|---:|---:|---:|---:|---|
| VAL-001-RERUN | TRUE | N/A | TRUE | 33 | $0.000207 | 1.30 | end_turn |
| BL-001-RERUN | TRUE | FALSE | FALSE | 4,239 | $0.061869 | 61.87 | max_tokens |

## BL-001 historical comparison

- Historical tokens: 4,169
- Rerun tokens: 4,239
- Token delta: +70 (+1.68%)
- Historical cost: $0.061659
- Rerun observed cost: $0.061869
- Cost delta: $+0.000210 (+0.34%)
- Historical latency: approximately 52.5s
- Rerun latency: 61.87s

## Interpretation

Transport success, historical output-class validity, and full completion are separate measurements. A max-token stop does not erase a valid cost-envelope observation, but it cannot be represented as a complete artifact.

## Reconstruction boundary

The exact historical request payload and exact connectivity prompt were not retained. This run reproduces the known provider, model, 4096-token ceiling, direct-unoptimized task class, usage capture, latency capture, raw response retention, and receipt hashing. It is a control-envelope reproduction, not a byte-identical replay.
