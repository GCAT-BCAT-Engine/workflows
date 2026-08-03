S5: Lean 4 candidate.

---

## ADMITTED PRIOR STATE

All S0–S4 artifacts admitted as recorded in ARTIFACT_LEDGER. Unresolved item carried forward: **deployed implementation binding remains unresolved**. No claim is made that any deployed GCAT/BCAT system conforms to STIP-05 or to any theorem derived from it.

---

## S5 DELIVERABLE: LEAN 4 CANDIDATE

### Preamble

This artifact presents a self-contained Lean 4 candidate for the logical core of Theorem ALLOW-NAS. It is a **candidate only**. No claim of Lean 4 kernel acceptance, compilation success, or deployed implementation validity is made. The candidate is offered for independent verification.

---

### Lean 4 Candidate Source

```lean4
/-
  SV-MATH-001 — Stage S5: Lean 4 Candidate
  Theorem ALLOW-NAS: Necessary and Sufficient Characterization of ALLOW

  GOVERNANCE NOTICES:
  • This is a candidate artifact. No claim of kernel acceptance is made.
  • No claim is made that any deployed GCAT/BCAT implementation conforms
    to STIP-05 or to any theorem derived from it.
  • Predicates GBP, BD, OC, and type T are fully abstract (STIP-02–04).
  • ALLOW is defined by definitional equality to GBP ∧ BD ∧ OC (STIP-05).
  • The claim boundary is the abstract model only (STIP-05, STIP-06).
-/

-- ---------------------------------------------------------------
-- Abstract universe: type of candidate transitions
-- ---------------------------------------------------------------
variable (T : Type)

-- ---------------------------------------------------------------
-- STIP-02, STIP-03, STIP-04: abstract predicates
-- ---------------------------------------------------------------
variable (GBP : T → Prop)
variable (BD  : T → Prop)
variable (OC  : T → Prop)

-- ---------------------------------------------------------------
-- STIP-05: definitional introduction of ALLOW
-- ALLOW is defined as the conjunction of GBP, BD, and OC.
-- ---------------------------------------------------------------
def ALLOW (t : T) : Prop := GBP t ∧ BD t ∧ OC t

-- ---------------------------------------------------------------
-- LEMMA-NEC: Necessity direction
-- If ALLOW t, then GBP t ∧ BD t ∧ OC t.
-- ---------------------------------------------------------------
theorem lemma_nec (t : T) (h : ALLOW T GBP BD OC t) :
    GBP t ∧ BD t ∧ OC t :=
  h

-- ---------------------------------------------------------------
-- LEMMA-SUF: Sufficiency direction
-- If GBP t ∧ BD t ∧ OC t, then ALLOW t.
-- ---------------------------------------------------------------
theorem lemma_suf (t : T) (h : GBP t ∧ BD t ∧ OC t) :
    ALLOW T GBP BD OC t :=
  h

-- ---------------------------------------------------------------
-- THEOREM ALLOW-NAS: Necessary and Sufficient Characterization
-- ALLOW t ↔ GBP t ∧ BD t ∧ OC t, for all t : T.
-- Proof: Iff.rfl, since ALLOW unfolds to the conjunction by
-- definition (definitional equality; no information added or lost).
-- ---------------------------------------------------------------
theorem allow_nas (t : T) :
    ALLOW T GBP BD OC t ↔ GBP t ∧ BD t ∧ OC t :=
  Iff.rfl
```

---

### Annotation of Proof Steps

| Line | Role | Justification |
|---|---|---|
| `def ALLOW` | STIP-05 encoding | Definitional equality; `ALLOW t` *is* `GBP t ∧ BD t ∧ OC t` |
| `lemma_nec` | LEMMA-NEC | `h : ALLOW T GBP BD OC t` unfolds to the conjunction; term is `h` |
| `lemma_suf` | LEMMA-SUF | `h : GBP t ∧ BD t ∧ OC t` folds to `ALLOW`; term is `h` |
| `allow_nas` | Theorem ALLOW-NAS | `Iff.rfl` closes the goal because both sides are definitionally equal |

**Remark on `Iff.rfl`.** In Lean 4, `Iff.rfl` closes a goal of the form `P ↔ P`. Because `ALLOW T GBP BD OC t` reduces to `GBP t ∧ BD t ∧ OC t` by the unfolding of `def ALLOW`, the two sides of the biconditional are definitionally equal, and `Iff.rfl` is the appropriate closing term. No case analysis, induction, or auxiliary lemmas are required.

---

### Claim Boundary (carried from S1–S4)

| Claim | Status |
|---|---|
| `ALLOW t ↔ GBP t ∧ BD t ∧ OC t` holds for all abstract `t : T` under STIP-05 | **In scope — generated claim; Lean 4 candidate presented; kernel acceptance unverified** |
| `GBP`, `BD`, `OC` have any specific computational meaning | **Not claimed; abstract only** |
| Any deployed GCAT/BCAT system satisfies STIP-05 or Theorem ALLOW-NAS | **Not claimed; implementation