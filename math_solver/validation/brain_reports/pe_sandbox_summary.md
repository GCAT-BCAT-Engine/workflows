# PE Sandbox Summary

- Receipts emitted: **20**
- Chain valid: **True**
- Allowed: **7**
- Denied: **7**
- Fail Closed: **6**

| ID | Outcome | Reason | Total Cost | Budget | Pass? |
|---|---|---|---|---|---|
| PE_001 | ALLOW | pe_admissible | 0.0 | 1.0 | ✅ |
| PE_002 | DENY | probability_below_threshold |  |  | ❌ |
| PE_003 | FAIL_CLOSED | probability_unavailable |  |  | ❌ |
| PE_004 | FAIL_CLOSED | probability_invalid |  |  | ❌ |
| PE_005 | ALLOW | pe_admissible | 0.19999999999999996 | 0.2 | ✅ |
| PE_006 | DENY | budget_exceeded | 1.9999999999999996 | 1.0 | ❌ |
| PE_007 | FAIL_CLOSED | probability_invalid |  |  | ❌ |
| PE_008 | ALLOW | pe_admissible | 2.5 | None | ✅ |
| PE_ADV_001 | ALLOW | pe_admissible | 0.19999999999999996 | 1.0 | ✅ |
| PE_ADV_002 | DENY | probability_below_threshold |  |  | ❌ |
| PE_ADV_003 | DENY | budget_exceeded | 2.0 | 1.0 | ❌ |
| PE_ADV_004 | FAIL_CLOSED | probability_unavailable |  |  | ❌ |
| PE_ADV_005 | FAIL_CLOSED | probability_invalid |  |  | ❌ |
| PE_ADV_006 | DENY | budget_exceeded | 2.500000000000002 | 2.0 | ❌ |
| PE_ADV_007 | ALLOW | pe_admissible | 2.500000000000002 | 5.0 | ✅ |
| PE_ADV_008 | ALLOW | pe_admissible | 9.999999999999998 | None | ✅ |
| PE_ADV_009 | ALLOW | pe_admissible | -0.0 | 1.0 | ✅ |
| PE_ADV_010 | DENY | budget_exceeded | 0.09999999999999998 | 0.05 | ❌ |
| PE_ADV_011 | DENY | budget_exceeded | 10.0 | 5.0 | ❌ |
| PE_ADV_012 | FAIL_CLOSED | probability_invalid |  |  | ❌ |
