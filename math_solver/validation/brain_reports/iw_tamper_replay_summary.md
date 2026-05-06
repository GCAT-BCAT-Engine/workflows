# Inference Window Replay Summary

- Receipts replayed: **19**
- Chain valid: **False**
- Mismatches found: **1**

| ID | Original Outcome | Replay Outcome | Original Reason | Replay Reason | Match? |
|---|---|---|---|---|---|
| IW_001 | DENY | ALLOW | tampered | iw_admissible | ❌ |
| IW_002 | DENY | DENY | budget_exceeded | budget_exceeded | ✅ |
| IW_003 | DENY | DENY | window_size_below_threshold | window_size_below_threshold | ✅ |
| IW_004 | FAIL_CLOSED | FAIL_CLOSED | missing_size | missing_size | ✅ |
| IW_005 | FAIL_CLOSED | FAIL_CLOSED | invalid_size | invalid_size | ✅ |
| IW_006 | ALLOW | ALLOW | iw_admissible | iw_admissible | ✅ |
| IW_007 | DENY | DENY | budget_exceeded | budget_exceeded | ✅ |
| IW_ADV_001 | ALLOW | ALLOW | iw_admissible | iw_admissible | ✅ |
| IW_ADV_002 | DENY | DENY | window_size_below_threshold | window_size_below_threshold | ✅ |
| IW_ADV_003 | DENY | DENY | budget_exceeded | budget_exceeded | ✅ |
| IW_ADV_004 | FAIL_CLOSED | FAIL_CLOSED | invalid_size | invalid_size | ✅ |
| IW_ADV_005 | FAIL_CLOSED | FAIL_CLOSED | invalid_size | invalid_size | ✅ |
| IW_ADV_006 | FAIL_CLOSED | FAIL_CLOSED | missing_size | missing_size | ✅ |
| IW_ADV_007 | ALLOW | ALLOW | iw_admissible | iw_admissible | ✅ |
| IW_ADV_008 | DENY | DENY | window_size_below_threshold | window_size_below_threshold | ✅ |
| IW_ADV_009 | DENY | DENY | budget_exceeded | budget_exceeded | ✅ |
| IW_ADV_010 | ALLOW | ALLOW | iw_admissible | iw_admissible | ✅ |
| IW_ADV_011 | DENY | DENY | budget_exceeded | budget_exceeded | ✅ |
| IW_ADV_012 | ALLOW | ALLOW | iw_admissible | iw_admissible | ✅ |
