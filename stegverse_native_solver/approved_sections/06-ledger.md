SECTION 6: VERIFICATION LEDGER

| Item | Status | Evidence required |
|---|---|---|
| Artifact structure | REQUIRED | Seven ordered sections and completion marker |
| Source integrity | REQUIRED | SHA-256 for every approved component |
| Provider independence | REQUIRED | External provider calls equal zero during assembly and validation |
| Lean syntax/type check | REQUIRED | `lake env lean` exits zero against the extracted candidate |
| Theorem scope | SATISFIED BY SPECIFICATION | The result is limited to the canonical evaluator |
| Production conformance | UNVERIFIED | Separate extensional-conformance evidence from deployed GCAT/BCAT implementations |
| Independent inference | NOT CLAIMED | The capability is deterministic reconstruction from approved components |

A failed structure check, source mismatch, or Lean execution blocks equivalent-output status.
