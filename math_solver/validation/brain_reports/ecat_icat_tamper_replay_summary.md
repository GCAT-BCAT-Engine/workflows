# ECAT/ICAT Replay Summary

- Receipts replayed: **38**
- Chain valid: **False**
- Mismatches found: **1**

| ID | Layer | Original Outcome | Replay Outcome | Original Reason | Replay Reason | Match? |
|---|---|---|---|---|---|---|
| ECAT_001 | ECAT | DENY | ALLOW | tampered | ecat_admissible | ❌ |
| ECAT_002 | ECAT | DENY | DENY | low_reputation | low_reputation | ✅ |
| ECAT_003 | ECAT | FAIL_CLOSED | FAIL_CLOSED | missing_reputation | missing_reputation | ✅ |
| ECAT_004 | ECAT | DENY | DENY | history_divergence_high | history_divergence_high | ✅ |
| ECAT_005 | ECAT | DENY | DENY | low_reputation | low_reputation | ✅ |
| ECAT_006 | ECAT | DENY | DENY | co_owner_rejection | co_owner_rejection | ✅ |
| ECAT_007 | ECAT | DENY | DENY | budget_exceeded | budget_exceeded | ✅ |
| ECAT_ADV_001 | ECAT | ALLOW | ALLOW | ecat_admissible | ecat_admissible | ✅ |
| ECAT_ADV_002 | ECAT | DENY | DENY | low_reputation | low_reputation | ✅ |
| ECAT_ADV_003 | ECAT | ALLOW | ALLOW | ecat_admissible | ecat_admissible | ✅ |
| ECAT_ADV_004 | ECAT | DENY | DENY | insufficient_stake | insufficient_stake | ✅ |
| ECAT_ADV_005 | ECAT | ALLOW | ALLOW | ecat_admissible | ecat_admissible | ✅ |
| ECAT_ADV_006 | ECAT | DENY | DENY | history_divergence_high | history_divergence_high | ✅ |
| ECAT_ADV_007 | ECAT | DENY | DENY | low_reputation | low_reputation | ✅ |
| ECAT_ADV_008 | ECAT | FAIL_CLOSED | FAIL_CLOSED | missing_stake | missing_stake | ✅ |
| ECAT_ADV_009 | ECAT | FAIL_CLOSED | FAIL_CLOSED | missing_history | missing_history | ✅ |
| ECAT_ADV_010 | ECAT | DENY | DENY | insufficient_stake | insufficient_stake | ✅ |
| ECAT_ADV_011 | ECAT | DENY | DENY | insufficient_stake | insufficient_stake | ✅ |
| ECAT_ADV_012 | ECAT | DENY | DENY | co_owner_rejection | co_owner_rejection | ✅ |
| ICAT_001 | ICAT | ALLOW | ALLOW | icat_admissible | icat_admissible | ✅ |
| ICAT_002 | ICAT | DENY | DENY | proof_invalid | proof_invalid | ✅ |
| ICAT_003 | ICAT | FAIL_CLOSED | FAIL_CLOSED | proof_unavailable | proof_unavailable | ✅ |
| ICAT_004 | ICAT | DENY | DENY | attestation_quorum_failed | attestation_quorum_failed | ✅ |
| ICAT_005 | ICAT | DENY | DENY | conservation_failed | conservation_failed | ✅ |
| ICAT_006 | ICAT | DENY | DENY | inverse_failed | inverse_failed | ✅ |
| ICAT_007 | ICAT | DENY | DENY | budget_exceeded | budget_exceeded | ✅ |
| ICAT_ADV_001 | ICAT | ALLOW | ALLOW | icat_admissible | icat_admissible | ✅ |
| ICAT_ADV_002 | ICAT | DENY | DENY | proof_invalid | proof_invalid | ✅ |
| ICAT_ADV_003 | ICAT | FAIL_CLOSED | FAIL_CLOSED | proof_unavailable | proof_unavailable | ✅ |
| ICAT_ADV_004 | ICAT | DENY | DENY | attestation_quorum_failed | attestation_quorum_failed | ✅ |
| ICAT_ADV_005 | ICAT | FAIL_CLOSED | FAIL_CLOSED | attestation_unavailable | attestation_unavailable | ✅ |
| ICAT_ADV_006 | ICAT | DENY | DENY | conservation_failed | conservation_failed | ✅ |
| ICAT_ADV_007 | ICAT | DENY | DENY | inverse_failed | inverse_failed | ✅ |
| ICAT_ADV_008 | ICAT | DENY | DENY | budget_exceeded | budget_exceeded | ✅ |
| ICAT_ADV_009 | ICAT | FAIL_CLOSED | FAIL_CLOSED | inverse_unavailable | inverse_unavailable | ✅ |
| ICAT_ADV_010 | ICAT | FAIL_CLOSED | FAIL_CLOSED | conservation_unavailable | conservation_unavailable | ✅ |
| ICAT_ADV_011 | ICAT | DENY | DENY | attestation_quorum_failed | attestation_quorum_failed | ✅ |
| ICAT_ADV_012 | ICAT | DENY | DENY | attestation_quorum_failed | attestation_quorum_failed | ✅ |
