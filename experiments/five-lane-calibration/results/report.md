# Five-Lane Observed Calibration and TA-006 Estimate

Status: VALID

## Observed SV-MATH-001 calibration

| Lane | Status | Input | Output | Latency s | Observed API cost |
|---|---|---:|---:|---:|---:|
| openai-raw | EXECUTED | 82 | 4096 | 100.99 | $0.123290 |
| openai-governed | EXECUTED | 129 | 4096 | 66.38 | $0.123525 |
| anthropic-raw | EXECUTED | 91 | 4096 | 63.63 | $0.061713 |
| anthropic-governed | EXECUTED | 142 | 4096 | 68.37 | $0.061866 |
| stegverse-only | BLOCKED_NO_LOCAL_INFERENCE | 0 | 0 | 0.00 | $0.000000 |

## TA-006 bounded estimates

| Lane | Low | Central | High | Success probability | Estimation-call cost |
|---|---:|---:|---:|---:|---:|
| openai-raw | $500.00 | $1,800.00 | $7,000.00 | 0.04 | $0.034735 |
| openai-governed | $900.00 | $2,800.00 | $8,500.00 | 0.03 | $0.034970 |
| anthropic-raw | $210.00 | $580.00 | $1,450.00 | 0.09 | $0.017100 |
| anthropic-governed | $0.00 | $0.00 | $0.00 | 0 | $0.023943 |
| stegverse-only | $0.00 | $0.00 | $0.00 | 0 | $0.000000 |
