# Cross-Model Governance Cost Matrix

Status: **BOUNDED OBSERVED CALIBRATION ADJUDICATED**

> Cost is compared only after task identity, execution, output, and receipt gates pass.

| Lane | Provider | Executed | Task preserved | Output present | Admissible | Observed cost | Decision |
|---|---|---:|---:|---:|---:|---:|---|
| openai-raw | openai | True | False | True | False | $0.123290 | TASK_IDENTITY_NOT_PRESERVED |
| openai-governed | openai | True | True | True | True | $0.123525 | PASS TO COST COMPARISON |
| anthropic-raw | anthropic | True | True | True | True | $0.061713 | PASS TO COST COMPARISON |
| anthropic-governed | anthropic | True | True | True | True | $0.061866 | PASS TO COST COMPARISON |
| stegverse-only | stegverse | False | True | False | False | $0.000000 | NOT_EXECUTED, REQUIRED_OUTPUT_NOT_PRESENT |

## Provider-pair findings

- **openai**: GOVERNED_LANE_ONLY_ADMISSIBLE; governed-minus-raw observed provider charge `$0.000235` (0.191%).
- **anthropic**: BOTH_ADMISSIBLE_RAW_LOWER_COST; governed-minus-raw observed provider charge `$0.000153` (0.248%).

## Bounded selection

`anthropic-raw` is the lowest observed-cost lane among the structurally admissible calibration lanes at `$0.061713`.

This is not a general model ranking. Full proof correctness and complete StegVerse local cost remain outside this bounded receipt.
