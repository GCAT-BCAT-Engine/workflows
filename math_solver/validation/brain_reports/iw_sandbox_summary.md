# Inference Window Sandbox Summary

- Receipts emitted: **19**
- Chain valid: **True**
- Allowed: **6**
- Denied: **8**
- Fail Closed: **5**

| ID | Outcome | Reason | Total Cost | Budget | Pass? |
|---|---|---|---|---|---|
| IW_001 | ALLOW | iw_admissible | 0.0 | 1.0 | ✅ |
| IW_002 | DENY | budget_exceeded | 0.4 | 0.3 | ❌ |
| IW_003 | DENY | window_size_below_threshold |  |  | ❌ |
| IW_004 | FAIL_CLOSED | missing_size |  |  | ❌ |
| IW_005 | FAIL_CLOSED | invalid_size |  |  | ❌ |
| IW_006 | ALLOW | iw_admissible | 0.3999999999999999 | 1.0 | ✅ |
| IW_007 | DENY | budget_exceeded | 0.3999999999999999 | 0.2 | ❌ |
| IW_ADV_001 | ALLOW | iw_admissible | 0.5 | 1.0 | ✅ |
| IW_ADV_002 | DENY | window_size_below_threshold |  |  | ❌ |
| IW_ADV_003 | DENY | budget_exceeded | 1.0 | 0.5 | ❌ |
| IW_ADV_004 | FAIL_CLOSED | invalid_size |  |  | ❌ |
| IW_ADV_005 | FAIL_CLOSED | invalid_size |  |  | ❌ |
| IW_ADV_006 | FAIL_CLOSED | missing_size |  |  | ❌ |
| IW_ADV_007 | ALLOW | iw_admissible | -0.5 | 1.0 | ✅ |
| IW_ADV_008 | DENY | window_size_below_threshold |  |  | ❌ |
| IW_ADV_009 | DENY | budget_exceeded | 1.6 | 1.5 | ❌ |
| IW_ADV_010 | ALLOW | iw_admissible | 1.6 | 2.0 | ✅ |
| IW_ADV_011 | DENY | budget_exceeded | 0.4 | 0.3 | ❌ |
| IW_ADV_012 | ALLOW | iw_admissible | 0.4 | None | ✅ |
