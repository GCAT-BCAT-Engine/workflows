# ECAT/ICAT Replay Summary

- Receipts replayed: **14**
- Chain valid: **True**
- Mismatches found: **0**

| ID | Layer | Original Outcome | Replay Outcome | Original Reason | Replay Reason | Match? |
|---|---|---|---|---|---|---|
| ECAT_001 | ECAT | ALLOW | ALLOW | ecat_admissible | ecat_admissible | ✅ |
| ECAT_002 | ECAT | DENY | DENY | low_reputation | low_reputation | ✅ |
| ECAT_003 | ECAT | FAIL_CLOSED | FAIL_CLOSED | missing_reputation | missing_reputation | ✅ |
| ECAT_004 | ECAT | DENY | DENY | history_divergence_high | history_divergence_high | ✅ |
| ECAT_005 | ECAT | DENY | DENY | low_reputation | low_reputation | ✅ |
| ECAT_006 | ECAT | DENY | DENY | co_owner_rejection | co_owner_rejection | ✅ |
| ECAT_007 | ECAT | DENY | DENY | budget_exceeded | budget_exceeded | ✅ |
| ICAT_001 | ICAT | ALLOW | ALLOW | icat_admissible | icat_admissible | ✅ |
| ICAT_002 | ICAT | DENY | DENY | proof_invalid | proof_invalid | ✅ |
| ICAT_003 | ICAT | FAIL_CLOSED | FAIL_CLOSED | proof_unavailable | proof_unavailable | ✅ |
| ICAT_004 | ICAT | DENY | DENY | attestation_quorum_failed | attestation_quorum_failed | ✅ |
| ICAT_005 | ICAT | DENY | DENY | conservation_failed | conservation_failed | ✅ |
| ICAT_006 | ICAT | DENY | DENY | inverse_failed | inverse_failed | ✅ |
| ICAT_007 | ICAT | DENY | DENY | budget_exceeded | budget_exceeded | ✅ |
