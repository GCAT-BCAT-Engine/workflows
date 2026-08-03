# Four-Lane StegVerse Economic Capability Report

| Lane | Stage | Canonical input | Observed sync cost | Combined compact + batch-normalized cost | Status |
|---|---:|---:|---:|---:|---|
| stegverse-openai-full | NONE | 222 | $0.023260 | $0.023260 | OBSERVED_SYNCHRONOUS |
| stegverse-openai-compact | S1 | 1,823 | $0.063935 | $0.031967 | BATCH_NORMALIZED_NOT_BATCH_RECEIPTED |
| stegverse-anthropic-full | NONE | 222 | $0.014301 | $0.014301 | OBSERVED_SYNCHRONOUS |
| stegverse-anthropic-compact | S3 | 5,117 | $0.085770 | $0.042885 | BATCH_NORMALIZED_NOT_BATCH_RECEIPTED |

## Provider comparisons

- openai: same stage=False; workload-only reduction=-174.87%; combined compact + batch-normalized reduction=-37.44%.
- anthropic: same stage=False; workload-only reduction=-499.75%; combined compact + batch-normalized reduction=-199.87%.

## StegVerse-only lane

- External inference remains denied and external provider cost is $0.
- Batch pricing does not apply because there is no provider request.
- Exact still-admissible repetitions may be fulfilled through artifact retrieval, deterministic reconstruction, verification, and a fresh receipt.
- Novel unresolved mathematical work remains BLOCKED unless an installed local solver can perform it.
- Local GitHub Actions, storage, retrieval, hashing, and verification costs must be measured separately rather than reported as zero total cost.

## Boundary

Observed synchronous costs are provider receipts from the four-lane rerun. Combined costs apply the documented 50% batch rate only to the remaining compact workload and are labeled batch-normalized until an actual Batch API receipt is retained.
