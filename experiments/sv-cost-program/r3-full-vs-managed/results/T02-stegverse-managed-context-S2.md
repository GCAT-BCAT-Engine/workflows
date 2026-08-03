S2: Theorem formulation

---

## ARTIFACT LEDGER (preserved)

| stage_id | output_sha256 | admitted | unresolved |
|----------|--------------|----------|------------|
| S0 | sha256:452623dc9b34fa013017eebc9f3a7b57f0a581b1998993caac6b78fa0dc8d1b2 | true | deployed implementation binding remains unresolved |
| S1 | sha256:8602a28a5856abca8df2a3a5a744757affd56840628e09a06dc1c03d0cf6d6bd | true | deployed implementation binding remains unresolved |

---

## STIPULATIONS CARRIED FORWARD (from S1, unmodified)

**S1-D2 (GBP).** `GBP : T → Prop`
**S1-D3 (BD).** `BD : T → Prop`
**S1-D4 (OC).** `OC : T → Prop`
**S1-D5 (ALLOW rule).** `E(t) = ALLOW ⟺ GBP(t) ∧ BD(t) ∧ OC(t)`
**S1-D6 (ALLOW-admissible).** A candidate transition `t : T` is *ALLOW-admissible* if and only if `E(t) = ALLOW`.

*These are stipulations. They fix vocabulary. They assert nothing about any deployed system.*

---

## S2 GENERATED CLAIMS

### S2-C1 — Necessary and Sufficient Characterization (informal statement)

**Claim S2-C1.**
For any candidate transition `t : T`, the following are equivalent:

1. `t` is ALLOW-admissible (i.e., `E(t) = ALLOW`)
2. `GBP(t) ∧ BD(t) ∧ OC(t)`

*Necessity:* If `E(t) = ALLOW`, then by S1-D5 (right-to-left reading of the biconditional), `GBP(t) ∧ BD(t) ∧ OC(t)` holds.
*Sufficiency:* If `GBP(t) ∧ BD(t) ∧ OC(t)`, then by S1-D5 (left-to-right reading), `E(t) = ALLOW`.

The biconditional in S1-D5 is the sole definitional source; no additional axioms are required. The proof is immediate by unfolding the definition.

---

### S2-C2 — Claim Boundary Statement

**What is claimed:**
S2-C1 is a purely logical consequence of the stipulations S1-D2 through S1-D6. It holds within the abstract model defined by those stipulations.

**What is NOT claimed:**
- That any deployed GCAT/BCAT implementation satisfies S1-D5.
- That `GBP`, `BD`, or `OC` as instantiated in any real system correspond to the abstract predicates here.
- That the Lean 4 candidate below has been verified by a Lean kernel or type-checker.
- That this theorem characterizes behavior of any software artifact outside this formal model.

**Unresolved (carried forward):** Deployed implementation binding remains unresolved.

---

### S2-C3 — Lean 4 Candidate for the Logical Core

*Status: candidate only. Not claimed to compile or to have been checked by a Lean kernel.*

```lean4
-- S2: Lean 4 candidate for ALLOW-admissibility characterization
-- STATUS: CANDIDATE ONLY — not verified by Lean kernel
-- CLAIM BOUNDARY: abstract model only; no deployed system binding

section AllowAdmissibility

-- Abstract type of candidate transitions (stipulation S1-D1, implicit)
variable (T : Type)

-- Predicates on candidate transitions (stipulations S1-D2, S1-D3, S1-D4)
variable (GBP : T → Prop)
variable (BD  : T → Prop)
variable (OC  : T → Prop)

-- Abstract evaluator outcome type
inductive Outcome : Type where
  | ALLOW : Outcome
  | other : Outcome

-- Abstract evaluator (stipulation S1-D5, encoded as a definition)
-- E(t) = ALLOW ⟺ GBP(t) ∧ BD(t) ∧ OC(t)
-- We encode this as a predicate rather than a function to stay purely logical.
def IsALLOW (t : T) : Prop :=
  GBP t ∧ BD t ∧ OC t

-- ALLOW-admissible (stipulation S1-D6)
def AllowAdmissible (t : T) : Prop :=
  IsALLOW GBP BD OC t

-- S2-C1: Necessary and sufficient characterization
-- The theorem is trivially true by definitional unfolding.
theorem allow_admissible_iff (t : T) :
    AllowAdmissible GBP BD OC t ↔ GBP t ∧ BD t ∧ OC t := by
  -- AllowAdmissible unfolds to IsALLOW, which unfolds to GBP t ∧ BD t ∧ OC t
  unfold AllowAdmissible IsALLOW
  exact Iff.rfl

-- Necessity direction (explicit)
theorem allow_admissible_necessary (t : T)
    (h : AllowAdmissible GBP BD OC t)