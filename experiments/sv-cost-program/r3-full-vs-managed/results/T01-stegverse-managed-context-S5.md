S5: Lean 4 candidate.

---

## Stage S5 — Lean 4 Candidate

This artifact is self-contained within the abstract model defined by stipulations A1–A4 (admitted in S1–S4). No claim is made that any deployed GCAT/BCAT implementation conforms to this model. Deployed implementation binding remains unresolved. The Lean 4 text below is a **candidate**; compilation and semantic correctness in any specific Lean 4 toolchain version are **not claimed**.

---

### Stipulations (preserved, not re-derived)

| ID | Content |
|----|---------|
| A1 | `T` is an arbitrary type (candidate transitions). |
| A2 | `GBP`, `BD`, `OC` are predicates `T → Prop`. |
| A3 | `Outcome` is an inductive type with constructors `ALLOW` and `DENY`. |
| A4 | `E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)` — the evaluator definition. |
| A5 | No decidability of `GBP`, `BD`, `OC` is assumed. |

---

### Lean 4 Candidate Text

```lean4
/-
  S5: Lean 4 candidate for SV-MATH-001-STAGED.
  Abstract GCAT/BCAT evaluator — ALLOW admissibility characterization.

  GOVERNANCE NOTICE:
  - This is a candidate artifact. Compilation validity is not claimed.
  - No deployed GCAT/BCAT implementation is claimed to conform.
  - Stipulations, generated claims, and proof steps are kept separate.
  - Deployed implementation binding remains unresolved.
-/

-- ============================================================
-- SECTION 1: Stipulated types and predicates (A1–A3)
-- ============================================================

/-- A1: T is an arbitrary type representing candidate transitions. -/
variable {T : Type*}

/-- A2: GBP, BD, OC are predicates on candidate transitions. -/
variable (GBP : T → Prop)
variable (BD  : T → Prop)
variable (OC  : T → Prop)

/-- A3: Outcome type with exactly two constructors. -/
inductive Outcome : Type where
  | ALLOW : Outcome
  | DENY  : Outcome

-- ============================================================
-- SECTION 2: Evaluator definition (A4)
-- ============================================================

/--
  A4: The abstract evaluator E.
  E(t) = ALLOW if and only if GBP(t) ∧ BD(t) ∧ OC(t).
  This definition encodes the stipulation directly; it is not
  derived from any deployed implementation.
-/
noncomputable def E (t : T) : Outcome :=
  if GBP t ∧ BD t ∧ OC t then Outcome.ALLOW else Outcome.DENY

-- ============================================================
-- SECTION 3: Primary theorem — Claim S2-C1 (ALLOW characterization)
-- ============================================================

/--
  Theorem ALLOW_iff (Claim S2-C1):
  For any candidate transition t,
    E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t).

  Both directions follow immediately from the definition of E (A4).
  The proof makes each direction explicit to mirror the informal
  proof structure established in S4.

  CLAIM BOUNDARY: Valid within the abstract model (A1–A4).
  No deployed implementation conformance is claimed.
-/
theorem ALLOW_iff (t : T) :
    E GBP BD OC t = Outcome.ALLOW ↔ GBP t ∧ BD t ∧ OC t := by
  unfold E
  -- After unfolding, the goal is:
  --   (if GBP t ∧ BD t ∧ OC t then ALLOW else DENY) = ALLOW
  --   ↔ GBP t ∧ BD t ∧ OC t
  constructor
  · -- Direction 1 (necessity): E(t) = ALLOW → GBP(t) ∧ BD(t) ∧ OC(t)
    intro h
    -- h : (if GBP t ∧ BD t ∧ OC t then ALLOW else DENY) = ALLOW
    -- Split on whether the condition holds.
    by_cases hc : GBP t ∧ BD t ∧ OC t
    · exact hc
    · -- If condition is false, the if-expression reduces to DENY,
      --   but h asserts it equals ALLOW — contradiction.
      simp [hc] at h
  · -- Direction 2 (sufficiency): GBP(t) ∧ BD(t) ∧ OC(t) → E(t) = ALLOW
    intro hc
    -- hc : GBP t ∧ BD t ∧ OC t
    -- The condition is true, so the if-expression reduces to ALLOW.
    simp [hc]

-- ============================================================
-- SECTION 4: Secondary theorem — Claim S2-C2 (DENY characterization)
-- ============================================================

/--
  Theorem DENY_iff (Claim S2-C2):
  For any candidate transition t,
    E(t) = DENY  ↔  ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC