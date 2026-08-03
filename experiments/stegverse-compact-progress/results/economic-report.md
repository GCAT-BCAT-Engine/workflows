# Four-Lane StegVerse Economic Capability Report

| Lane | Stage | Canonical input | Observed sync cost | Combined compact + batch-normalized cost | Status |
|---|---:|---:|---:|---:|---|
| stegverse-openai-full | S6 | 14,280 | $0.240140 | $0.240140 | OBSERVED_SYNCHRONOUS |
| stegverse-openai-compact | S3 | 4,475 | $0.141470 | $0.070735 | BATCH_NORMALIZED_NOT_BATCH_RECEIPTED |
| stegverse-anthropic-full | NONE | 222 | $0.013596 | $0.013596 | OBSERVED_SYNCHRONOUS |
| stegverse-anthropic-compact | NONE | 222 | $0.013266 | $0.006633 | BATCH_NORMALIZED_NOT_BATCH_RECEIPTED |

## Provider comparisons

- openai: same stage=False; workload-only reduction=41.09%; combined compact + batch-normalized reduction=70.54%.
- anthropic: same stage=True; workload-only reduction=2.43%; combined compact + batch-normalized reduction=51.21%.

## StegVerse-only lane

- External inference remains denied and external provider cost is $0.
- Batch pricing does not apply because there is no provider request.
- Exact still-admissible repetitions may be fulfilled through artifact retrieval, deterministic reconstruction, verification, and a fresh receipt.
- Novel unresolved mathematical work remains BLOCKED unless an installed local solver can perform it.
- Local GitHub Actions, storage, retrieval, hashing, and verification costs must be measured separately rather than reported as zero total cost.

## Boundary

Observed synchronous costs are provider receipts from the four-lane rerun. Combined costs apply the documented 50% batch rate only to the remaining compact workload and are labeled batch-normalized until an actual Batch API receipt is retained.
