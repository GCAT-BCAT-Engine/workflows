# Four-Lane StegVerse Economic Capability Report

| Lane | Stage | Canonical input | Observed sync cost | Combined compact + batch-normalized cost | Status |
|---|---:|---:|---:|---:|---|
| stegverse-openai-full | S3 | 6,115 | $0.130425 | $0.130425 | OBSERVED_SYNCHRONOUS |
| stegverse-openai-compact | NONE | 222 | $0.010750 | $0.005375 | BATCH_NORMALIZED_NOT_BATCH_RECEIPTED |
| stegverse-anthropic-full | NONE | 222 | $0.014301 | $0.014301 | OBSERVED_SYNCHRONOUS |
| stegverse-anthropic-compact | NONE | 222 | $0.012726 | $0.006363 | BATCH_NORMALIZED_NOT_BATCH_RECEIPTED |

## Provider comparisons

- openai: same stage=False; workload-only reduction=91.76%; combined compact + batch-normalized reduction=95.88%.
- anthropic: same stage=True; workload-only reduction=11.01%; combined compact + batch-normalized reduction=55.51%.

## StegVerse-only lane

- External inference remains denied and external provider cost is $0.
- Batch pricing does not apply because there is no provider request.
- Exact still-admissible repetitions may be fulfilled through artifact retrieval, deterministic reconstruction, verification, and a fresh receipt.
- Novel unresolved mathematical work remains BLOCKED unless an installed local solver can perform it.
- Local GitHub Actions, storage, retrieval, hashing, and verification costs must be measured separately rather than reported as zero total cost.

## Boundary

Observed synchronous costs are provider receipts from the four-lane rerun. Combined costs apply the documented 50% batch rate only to the remaining compact workload and are labeled batch-normalized until an actual Batch API receipt is retained.
