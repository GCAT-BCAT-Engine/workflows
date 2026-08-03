# Four-Lane StegVerse Economic Capability Report

| Lane | Stage | Canonical input | Observed sync cost | Combined compact + batch-normalized cost | Status |
|---|---:|---:|---:|---:|---|
| stegverse-openai-full | NONE | 222 | $0.013870 | $0.013870 | OBSERVED_SYNCHRONOUS |
| stegverse-openai-compact | NONE | 222 | $0.009100 | $0.004550 | BATCH_NORMALIZED_NOT_BATCH_RECEIPTED |
| stegverse-anthropic-full | NONE | 222 | $0.014301 | $0.014301 | OBSERVED_SYNCHRONOUS |
| stegverse-anthropic-compact | S6 | 8,784 | $0.125739 | $0.062870 | BATCH_NORMALIZED_NOT_BATCH_RECEIPTED |

## Provider comparisons

- openai: same stage=True; workload-only reduction=34.39%; combined compact + batch-normalized reduction=67.20%.
- anthropic: same stage=False; workload-only reduction=-779.23%; combined compact + batch-normalized reduction=-339.62%.

## StegVerse-only lane

- External inference remains denied and external provider cost is $0.
- Batch pricing does not apply because there is no provider request.
- Exact still-admissible repetitions may be fulfilled through artifact retrieval, deterministic reconstruction, verification, and a fresh receipt.
- Novel unresolved mathematical work remains BLOCKED unless an installed local solver can perform it.
- Local GitHub Actions, storage, retrieval, hashing, and verification costs must be measured separately rather than reported as zero total cost.

## Boundary

Observed synchronous costs are provider receipts from the four-lane rerun. Combined costs apply the documented 50% batch rate only to the remaining compact workload and are labeled batch-normalized until an actual Batch API receipt is retained.
