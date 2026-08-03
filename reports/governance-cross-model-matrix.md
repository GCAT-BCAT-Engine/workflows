# Cross-Model Governance Cost Matrix

Status: **BOUNDED OBSERVED CALIBRATION — ALL LANES PRESENTED**

> Every lane and every observed cost remains in the evidence record. Admission controls selection only; it does not erase failed, blocked, or non-admissible test data.

## Complete lane evidence

| Lane | Provider | Status | Task preserved | Output | Admissible for selection | Observed cost | Evidence use |
|---|---|---|---:|---|---:|---:|---|
| openai-raw | openai | EXECUTED | False | formal_proof_candidate | False | $0.123290 | TEST EVIDENCE ONLY: TASK_IDENTITY_NOT_PRESERVED |
| openai-governed | openai | EXECUTED | True | formal_proof_candidate | True | $0.123525 | SELECTION + TEST EVIDENCE |
| anthropic-raw | anthropic | EXECUTED | True | formal_proof_candidate | True | $0.061713 | SELECTION + TEST EVIDENCE |
| anthropic-governed | anthropic | EXECUTED | True | formal_proof_candidate | True | $0.061866 | SELECTION + TEST EVIDENCE |
| stegverse-only | stegverse | BLOCKED_NO_LOCAL_INFERENCE | True | no_generated_proof | False | $0.000000 | TEST EVIDENCE ONLY: NOT_EXECUTED, REQUIRED_OUTPUT_NOT_PRESENT |

## Full testing economics

- Total observed cost across all 5 lanes: `$0.370394`.
- Total observed cost across executed lanes: `$0.370394`.
- Failed and blocked lanes remain economically relevant because they reveal failure, retry, and capability boundaries.

## Provider-pair findings

| Provider | Raw cost | Governed cost | Total paired test cost | Raw admitted | Governed admitted | Governance delta |
|---|---:|---:|---:|---:|---:|---:|
| openai | $0.123290 | $0.123525 | $0.246815 | False | True | $0.000235 (0.191%) |
| anthropic | $0.061713 | $0.061866 | $0.123579 | True | True | $0.000153 (0.248%) |

## Bounded selection

`anthropic-raw` is the lowest observed-cost lane among structurally admissible calibration lanes at `$0.061713`.

This selection does not remove or discount any other lane's testing data. It is not a general model ranking. Full correctness and fully burdened StegVerse cost remain outside this bounded receipt.
