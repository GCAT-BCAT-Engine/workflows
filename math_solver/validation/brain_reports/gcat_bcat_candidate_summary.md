# GCAT/BCAT Candidate Validation Summary

## Test Results

- Total: **6**
- Passed: **6**
- Failed: **0**

## Outcome Counts

- ALLOW: **1**
- DENY: **2**
- FAIL_CLOSED: **3**

## Cost Summary

- GCAT cost: **6.000000**
- BCAT cost: **7.000000**
- Total cost: **13.000000**
- Budget: **20.000000**
- Budget margin: **7.000000**

## Candidate Results

| ID | Outcome | Reason | Passed | Total Cost | Budget | Margin |
|---|---:|---|---:|---:|---:|---:|
| CT_GB_001 | ALLOW | gcat_bcat_admissible | ✅ | 2.000000 | 5.000000 | 3.000000 |
| CT_GB_002 | DENY | invariant_violation | ✅ | 3.000000 | 5.000000 | 2.000000 |
| CT_GB_003 | FAIL_CLOSED | state_missing_t | ✅ | 2.000000 | 5.000000 | 3.000000 |
| CT_GB_004 | DENY | budget_exceeded | ✅ | 6.000000 | 5.000000 | -1.000000 |
| CT_GB_005 | FAIL_CLOSED | cost_non_numeric_gcat | ✅ | 0.000000 | 0.000000 | 0.000000 |
| CT_GB_006 | FAIL_CLOSED | cost_negative_gcat | ✅ | 0.000000 | 0.000000 | 0.000000 |
