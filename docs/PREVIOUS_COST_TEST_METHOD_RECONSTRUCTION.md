# Previous Cost-Test Method Reconstruction

## Source authority

This reconstruction is based on the repository-native `SV-MATH-001` problem specification, the published cost-reduction paper, the historical `validation_run.yml`, and the RTG-001 cost-estimate receipt.

## Exact historical task

- Problem ID: `SV-MATH-001`
- Title: GCAT/BCAT Admissibility Complete Invariant Characterization
- Requested result: formal necessary-and-sufficient characterization for ALLOW admissibility.
- Required output: full formal proof structure, with definitions, theorem statements, proof reasoning, and formal/categorical rewriting content.
- Original specification additionally requested LaTeX plus Lean 4 verification, a $500 tier-1 ceiling, at most 50 iterations, at most 120 minutes, confidence >= 0.85, novelty >= 0.7, and three implications.

## Historical observed runs

| Run | Execution | Model | Max output | Observed tokens | Observed cost | Verdict |
|---|---|---|---:|---:|---:|---|
| VAL-001 | connectivity validation | Claude Sonnet 4.6 | not retained in summary | not retained | $0.015 | connectivity proven |
| BL-001 | direct, unoptimized, extended reasoning | Claude Sonnet 4.6 | 4096 | 4,169 | $0.061659 | baseline |
| OP-001 | cache-framed optimization | Claude Sonnet 4.6 | reduced output | 489 | $0.003 | rejected: output became meta-analysis |
| OP-002 | direct prompt with batch pricing | Claude Sonnet 4.6 | 4096 | 4,169 | $0.0308295 | validated: same required output class |
| COMB-001 | Haiku classification then Sonnet proof | Haiku 4.5 + Sonnet 4.6 | 512 + 4096 | 4,689 | $0.0333 | recommended production route |

Historical latency for BL-001 and OP-002 was approximately 52.5 seconds. The controlling rule was that a lower price was admissible only when task identity, output type, structural quality, and auditability were preserved.

## Five-lane rerun contract

The rerun preserves the same task, output criteria, maximum proof output of 4096 tokens, measured API usage, measured latency, raw response retention, and receipt hashing across:

1. OpenAI non-governed.
2. OpenAI StegVerse-governed.
3. Anthropic non-governed.
4. Anthropic StegVerse-governed.
5. StegVerse-only sandbox, with external inference denied.

The governed prompt may add declarations, evidence requirements, and claim boundaries, but may not alter the mathematical task or required proof output. Costs are calculated from observed API usage and declared current model rates. The StegVerse-only lane must report BLOCKED rather than inventing proof capability when no installed local inference engine can perform the task.

## Next-stage one-problem estimate

After calibration, the same five lanes estimate `TA-006`, quantum parallel repetition, because the recovered ten-problem forecast gave it the lowest Anthropic central estimate and a comparatively bounded theorem domain. This estimate is restricted to model inference/search effort, governance overhead, and verification/formalization effort; salaries, institutional overhead, procurement, and unspecified research-program costs are excluded.
