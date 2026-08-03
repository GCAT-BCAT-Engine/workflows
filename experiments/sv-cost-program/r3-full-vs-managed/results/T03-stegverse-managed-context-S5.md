S5: Lean 4 candidate.

---

**Stage:** S5 — Lean 4 candidate
**Depends on:** S4 `sha256:3a850ab0f9e72ce1bf5725c6560a9493de9d55ad381cf6cf50c3c10257f23979`
**Governance note:** This artifact is a candidate Lean 4 encoding of the abstract logical core established in S1–S4. It is not claimed to compile without error in any specific Lean 4 toolchain version, and it is not claimed to bind to any deployed GCAT/BCAT implementation. Deployed implementation binding remains unresolved.

---

## S5 Artifact: Lean 4 Candidate

```lean4
/-
  SV-MATH-001 — ALLOW Admissibility Characterization
  Stage S5: Lean 4 candidate

  GOVERNANCE:
  - This file encodes the abstract model stipulated in S1–S4.
  - No claim is made that this file compiles in any specific Lean 4
    toolchain version without modification.
  - No claim is made that any deployed GCAT/BCAT implementation
    conforms to this abstract model.
  - Deployed implementation binding remains unresolved.

  CLAIM BOUNDARY:
  - All theorems below are claims about the abstract model defined
    by `allow_ax` alone.
  - They are not claims about any concrete evaluator, runtime system,
    or deployed artifact.
-/

-- ---------------------------------------------------------------
-- Section 1: Abstract types and predicates
-- ---------------------------------------------------------------

/-- Abstract type of candidate transitions. -/
variable (Transition : Type)

/-- GBP: "Good Boundary Predicate" — first conjunct condition. -/
variable (GBP : Transition → Prop)

/-- BD: "Boundary" predicate — second conjunct condition. -/
variable (BD  : Transition → Prop)

/-- OC: "Output Condition" predicate — third conjunct condition. -/
variable (OC  : Transition → Prop)

/-- ALLOW: evaluator decision predicate. -/
variable (ALLOW : Transition → Prop)

-- ---------------------------------------------------------------
-- Section 2: Axiom — the abstract evaluator specification
--
-- Stipulation (from S1, S2):
--   For all t : Transition,
--     ALLOW t ↔ GBP t ∧ BD t ∧ OC t
--
-- This axiom is the sole non-logical assumption of the model.
-- ---------------------------------------------------------------

/-- Abstract evaluator axiom: ALLOW holds iff all three predicates hold. -/
axiom allow_ax
    (Transition : Type)
    (GBP BD OC ALLOW : Transition → Prop)
    (t : Transition) :
    ALLOW t ↔ GBP t ∧ BD t ∧ OC t

-- ---------------------------------------------------------------
-- Section 3: Main theorem — necessary and sufficient
--            characterization (universal form)
-- ---------------------------------------------------------------

/--
  Theorem (ALLOW Admissibility Characterization):
  For every transition t, ALLOW t holds if and only if
  GBP t, BD t, and OC t all hold simultaneously.

  Proof: Immediate by instantiation of `allow_ax`.
-/
theorem allow_admissibility_iff
    (Transition : Type)
    (GBP BD OC ALLOW : Transition → Prop)
    (t : Transition) :
    ALLOW t ↔ GBP t ∧ BD t ∧ OC t :=
  allow_ax Transition GBP BD OC t

-- ---------------------------------------------------------------
-- Section 4: Directed lemmas
-- ---------------------------------------------------------------

/--
  Lemma (Sufficiency / Introduction):
  If GBP t, BD t, and OC t all hold, then ALLOW t holds.

  Proof: Apply the forward direction of `allow_admissibility_iff`.
-/
theorem allow_introduction
    (Transition : Type)
    (GBP BD OC ALLOW : Transition → Prop)
    (t : Transition)
    (hGBP : GBP t)
    (hBD  : BD  t)
    (hOC  : OC  t) :
    ALLOW t :=
  (allow_admissibility_iff Transition GBP BD OC t).mpr ⟨hGBP, hBD, hOC⟩

/--
  Lemma (Necessity / Elimination — GBP):
  If ALLOW t holds, then GBP t holds.

  Proof: Apply the backward direction of `allow_admissibility_iff`
  and project the first conjunct.
-/
theorem allow_elim_GBP
    (Transition : Type)
    (GBP BD OC ALLOW : Transition → Prop)
    (t : Transition)
    (h : ALLOW t) :
    GBP t :=
  ((allow_admissibility_iff Transition GBP BD OC t).mp h).1

/--
  Lemma (Necessity / Elimination — BD):
  If ALLOW t holds, then BD t holds.
-/
theorem allow_elim_BD
    (Transition : Type)
    (GBP BD OC ALLOW : Transition → Prop)
    (t : Transition)
    (h : ALLOW t) :
    BD t :=
  ((allow_admissibility_iff Transition GBP BD OC t).mp h).2.1

/--
  Lemma (Necessity / Elimination — OC):
  If ALLOW t