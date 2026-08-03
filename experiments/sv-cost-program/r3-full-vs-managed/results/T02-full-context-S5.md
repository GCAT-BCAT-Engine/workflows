S5: Lean 4 candidate

---

## 1. Task Identity Preservation

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S5 — Lean 4 candidate
**Prior admitted state:** S4:sha256:f4310419504f48d1194f2449181aa6d085701b037f34f0a12b909f2f8ad66093

---

## 2. Admitted Prior State (Carried Forward Unchanged)

```
ADMITTED FROM S0–S4:
  ST-1  GBP, BD, OC are uninterpreted predicates on a candidate transition t.
  ST-2  E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)  [stipulated evaluator semantics]
  ST-3  The evaluator is abstract; no concrete implementation is referenced.
  ST-4  No deployed GCAT/BCAT system is referenced.

  DEF-1  T : arbitrary carrier type of candidate transitions
  DEF-2  GBP, BD, OC : T → Prop
  DEF-3  Outcome : type with inhabitants ALLOW, DENY
  DEF-4  E : T → Outcome, satisfying ST-2 as defining property
  DEF-5  Admissible(t) :≡ GBP(t) ∧ BD(t) ∧ OC(t)

  ASM-1  Classical propositional logic
  ASM-2  T is non-empty
  ASM-3  GBP, BD, OC are total on T
  ASM-4  E is total on T
  ASM-5  No further axioms in force

  THEOREM 1  ∀ t : T,  E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
  THEOREM 2  ∀ t : T,  Admissible(t)  ↔  E(t) = ALLOW
  THEOREM 3  ∀ t : T,  E(t) ≠ ALLOW  ↔  ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)

  LEMMA L1-SUFF  ∀ t : T,  GBP(t) ∧ BD(t) ∧ OC(t)  →  E(t) = ALLOW
  LEMMA L2-NEC   ∀ t : T,  E(t) = ALLOW  →  GBP(t) ∧ BD(t) ∧ OC(t)
  LEMMA L3-TRANS ∀ t : T,  Admissible(t)  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
  LEMMA L4-DM    ∀ t : T,  ¬(GBP(t) ∧ BD(t) ∧ OC(t))
                            ↔  ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)

  C-IN-1  [in-scope; established informally at S4]
  C-IN-2  [in-scope; this stage]
  C-IN-3  [in-scope; established informally at S4]
  C-OUT-1 through C-OUT-4  [permanently excluded]

VERIFIED CLAIMS FROM S0–S4: none mechanically verified
```

---

## 3. Governance Notes for This Stage

The artifact below is a **Lean 4 candidate**. The following governance constraints apply without exception:

| Constraint | Status |
|---|---|
| No claim that this candidate compiles or type-checks | Enforced |
| No claim that this candidate is implementation-valid | Enforced |
| No claim that any deployed GCAT/BCAT system conforms | Enforced |
| Stipulations, generated claims, and unresolved evidence are separated | Enforced |
| Task identity is preserved | Enforced |

The candidate is produced to encode the logical core established in S1–S4. It is offered for independent mechanical verification. A hash of this artifact proves artifact identity only, not semantic correctness.

---

## 4. Lean 4 Candidate

```lean
/-
  SV-MATH-001-STAGED — S5: Lean 4 Candidate
  Experiment: SV-COST-R3-FULL-VS-MANAGED-001

  GOVERNANCE:
  - This is a candidate artifact. No compilation validity is claimed.
  - No deployed GCAT/BCAT implementation is referenced or implied.
  - GBP, BD, OC are uninterpreted predicates (ST-1).
  - E is abstract, defined solely by its biconditional property (ST-2, DEF-4).
  - All claims below are generated claims pending independent mechanical verification.
-/

-- ============================================================
-- Section 1: Types and Signatures (DEF-1, DEF-2, DEF-3)
-- ============================================================

/-- Outcome type with at least two distinct inhabitants (DEF-3). -/
inductive Outcome : Type where
  | ALLOW : Outcome
  | DENY  : Outcome
  deriving DecidableEq

/--
  Abstract evaluator context (DEF-1, DEF-2, DEF-4).
  T