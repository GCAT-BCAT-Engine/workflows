S6: Verification ledger.

---

## STAGE IDENTITY

**Stage:** S6 — Verification ledger
**Task:** SV-MATH-001-STAGED
**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Context mode:** Managed

---

## ADMITTED PRIOR STATE (carried forward without modification)

| Stage | SHA-256 | Admitted | Unresolved |
|-------|---------|----------|------------|
| S0 | `sha256:452623dc9b34fa013017eebc9f3a7b57f0a581b1998993caac6b78fa0dc8d1b2` | ✓ | deployed implementation binding remains unresolved |
| S1 | `sha256:e2919679a4b76009aac3293cda8b597f3e7dd4436b4ba06a24dfd07ccacdeb5a` | ✓ | deployed implementation binding remains unresolved |
| S2 | `sha256:5078a388f5c1016c81b81db36ad2d004fcc9f3791308613833d6275f5a860a76` | ✓ | deployed implementation binding remains unresolved |
| S3 | `sha256:43d4595c7b661088d400186d100f7768e99e87571474e415a61ad134ddd67d90` | ✓ | deployed implementation binding remains unresolved |
| S4 | `sha256:754c8e3a69879547722469141dff7dbbdc6cadfe74f91dbebb975c0ea22ad5c3` | ✓ | deployed implementation binding remains unresolved |
| S5 | `sha256:74376bf6fe2fb60c1e522629b9e2b8c6420ce1af30520a4a3a4946ecdced9565` | ✓ | deployed implementation binding remains unresolved |

---

## VERIFICATION LEDGER

### VL-SECTION-1: Stipulations (from S0–S1, carried forward)

| ID | Stipulation | Status |
|----|-------------|--------|
| STIP-01 | `T` is an abstract type representing candidate transitions. | Admitted |
| STIP-02 | `GBP`, `BD`, `OC` are predicates `T → Prop`. Their internal semantics are not specified here. | Admitted |
| STIP-03 | `ALLOW : T → Prop` is defined by: `ALLOW t ↔ GBP t ∧ BD t ∧ OC t`. This is a stipulative definition, not a derived claim. | Admitted |
| STIP-04 | The evaluator described in the task statement is modeled by STIP-03. No claim is made that any deployed system instantiates this model. | Admitted |
| STIP-05 | The claim boundary is the abstract model only. No deployed GCAT/BCAT implementation is asserted to conform. | Admitted |

---

### VL-SECTION-2: Generated Claims (from S2–S4)

| ID | Claim | Source Stage | Proof Character |
|----|-------|-------------|-----------------|
| CLAIM-NEC | For all `t : T`, if `ALLOW t` then `GBP t ∧ BD t ∧ OC t`. | S2, S4 | Definitional unfolding; single step; no case analysis, no induction. |
| CLAIM-SUF | For all `t : T`, if `GBP t ∧ BD t ∧ OC t` then `ALLOW t`. | S2, S4 | Definitional folding; single step; symmetric to CLAIM-NEC. |
| THEOREM-ALLOW-NAS | For all `t : T`, `ALLOW t ↔ GBP t ∧ BD t ∧ OC t`. | S2, S4 | Conjunction of CLAIM-NEC and CLAIM-SUF; reduces to `Iff.rfl` under the stipulative definition. |

---

### VL-SECTION-3: Verified Claims

| ID | Verification Basis | Verification Status | Notes |
|----|-------------------|--------------------|----|
| CLAIM-NEC | Informal proof complete (S4). Lean 4 candidate provided (S5). | **Informally verified.** Lean 4 kernel acceptance: **unverified** — candidate only, no compilation claimed. | Proof is trivial by definition; no logical gap identified in informal argument. |
| CLAIM-SUF | Informal proof complete (S4). Lean 4 candidate provided (S5). | **Informally verified.** Lean 4 kernel acceptance: **unverified** — candidate only, no compilation claimed. | Symmetric to CLAIM-NEC; same verification status. |
| THEOREM-ALLOW-NAS | Follows from CLAIM-NEC and CLAIM-SUF. Lean 4 candidate: `Iff.rfl` under definitional equality. | **Informally verified.** Lean 4 kernel acceptance: **unverified** — candidate only. | No logical gap identified. Proof is definitionally trivial. |

---

### VL-SECTION-4: Lean 4 Candidate — Corrected and Annotated

The S5 candidate contained syntactic irregularities. The following is a corrected candidate for independent verification. **No claim of compilation success or kernel acceptance is made.**

```lean4
-- CANDIDATE ONLY. Not claimed to compile. Not claimed to be kernel-accepted.
-- Offered for independent verification per STIP-05.

variable {T : Type*}
variable (G