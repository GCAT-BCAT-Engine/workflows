# Five-Lane Reconstructable Governance Cost Results

Status: `RESEARCH_IN_PROGRESS_FAIL_CLOSED`

Comparison unit: `successful equivalent admissible outcome`

| Lane | Admissible | Attempts | Input | Output | Latency s | Provider cost | Local cost | Total cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| openai-raw | false | 2 | 569 | 905 | 15.413594 | $0.029995000 | $0.000000000000 | $0.029995000000 |
| openai-governed | false | 2 | 637 | 1174 | 17.170527 | $0.038405000 | $0.000000000000 | $0.038405000000 |
| anthropic-raw | false | 2 | 681 | 1192 | 15.045915 | $0.019923000 | $0.000000000000 | $0.019923000000 |
| anthropic-governed | false | 2 | 759 | 1198 | 15.173936 | $0.020247000 | $0.000000000000 | $0.020247000000 |
| stegverse-only | true | 1 | 0 | 0 | 0.000017 | $0.000000000 | $0.000000007030 | $0.000000007030 |

## Provider governance deltas

| Provider | Raw | Governed | Delta | Delta % |
|---|---:|---:|---:|---:|
| openai | $0.029995000 | $0.038405000 | $0.008410000 | 28.038006% |
| anthropic | $0.019923000 | $0.020247000 | $0.000324000 | 1.626261% |

## StegVerse-only matched reconstruction comparisons

| Provider lane | Provider cost | StegVerse-only cost | Ratio | Modeled reduction | Valid |
|---|---:|---:|---:|---:|---:|
| openai-raw | $0.029995000 | $0.000000007030 | 4266714.082504x | 99.999977% | false |
| openai-governed | $0.038405000 | $0.000000007030 | 5463015.647226x | 99.999982% | false |
| anthropic-raw | $0.019923000 | $0.000000007030 | 2833997.15505x | 99.999965% | false |
| anthropic-governed | $0.020247000 | $0.000000007030 | 2880085.348506x | 99.999965% | false |

## Derivation

Provider cost = input_tokens × input_rate + output_tokens × output_rate.

StegVerse-only local cost = measured runtime_seconds × declared Linux runner rate + output_bytes × declared storage rate.

Cost ranking occurs only after task identity, exact output, and claim-boundary validation pass.

Claim boundary: This task measures one bounded deterministic reconstruction operation. It does not establish universal provider economics, company ROI, or fresh-inference equivalence.
