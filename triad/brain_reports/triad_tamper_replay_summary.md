# Triad Replay Summary

- Receipts replayed: **10**
- Chain valid: **False**
- Mismatches found: **1**

| ID | Original Outcome | Replay Outcome | Original Reason | Replay Reason | Match? |
|---|---|---|---|---|---|
| TRIAD_001 | DENY | ALLOW | tampered | triad_admissible | ❌ |
| TRIAD_002 | DENY | DENY | gcat_invariant_violation | gcat_invariant_violation | ✅ |
| TRIAD_003 | DENY | DENY | low_reputation | low_reputation | ✅ |
| TRIAD_004 | FAIL_CLOSED | FAIL_CLOSED | proof_unavailable | proof_unavailable | ✅ |
| TRIAD_005 | DENY | DENY | probability_below_threshold | probability_below_threshold | ✅ |
| TRIAD_006 | DENY | DENY | insufficient_stake | insufficient_stake | ✅ |
| TRIAD_007 | FAIL_CLOSED | FAIL_CLOSED | gcat_missing_c | gcat_missing_c | ✅ |
| TRIAD_008 | FAIL_CLOSED | FAIL_CLOSED | proof_unavailable | proof_unavailable | ✅ |
| TRIAD_009 | FAIL_CLOSED | FAIL_CLOSED | probability_unavailable | probability_unavailable | ✅ |
| TRIAD_010 | DENY | DENY | insufficient_stake | insufficient_stake | ✅ |
