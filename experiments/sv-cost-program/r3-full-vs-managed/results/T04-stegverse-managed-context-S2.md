S2: Theorem formulation.

---

## ARTIFACT: S2 — Theorem Formulation

**Task identity:** SV-MATH-001-STAGED / SV-COST-R3-FULL-VS-MANAGED-001
**Stage:** S2
**Depends on admitted:** S0 (`b44121bb1cdd65ee8dd01278fe146d2e95fd3ace2868a16a4712f69ddd18dbdb`), S1 (`bfdeb98763fdf4539643c6b0a40851bd41833a816139f02f5b1915e9a9d4a873`)

---

### 1. Preserved Admitted State

From S0/S1 (admitted, unresolved implementation binding):

- **Type:** `T` — the type of candidate transitions (abstract, uninterpreted).
- **Evaluator:** `E : T → {ALLOW, DENY}` — abstract; no deployed instance claimed.
- **Stipulated rule:** `E(t) = ALLOW ⟺ GBP(t) ∧ BD(t) ∧ OC(t)`.
- **Predicates (stipulated names, no deployed binding claimed):**
  - `GBP : T → Prop`
  - `BD : T → Prop`
  - `OC : T → Prop`

---

### 2. Theorem Statement (Natural Language)

**Theorem (ALLOW Admissibility — Necessary and Sufficient Characterization).**

Let `T` be an arbitrary type of candidate transitions. Let `GBP`, `BD`, `OC : T → Prop` be predicates on `T`. Let `E : T → {ALLOW, DENY}` be an evaluator satisfying the stipulated rule.

For any candidate transition `t : T`:

> `E(t) = ALLOW` **if and only if** `GBP(t) ∧ BD(t) ∧ OC(t)`.

Equivalently, decomposed into its two directions:

- **(Sufficiency / →-direction):** If `GBP(t)` and `BD(t)` and `OC(t)` all hold, then `E(t) = ALLOW`.
- **(Necessity / ←-direction):** If `E(t) = ALLOW`, then `GBP(t)` holds, `BD(t)` holds, and `OC(t)` holds.

**Corollary (DENY characterization):**

> `E(t) = DENY` **if and only if** `¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)`.

---

### 3. Claim Boundary

| Item | Status |
|---|---|
| The biconditional above is a **logical consequence of the stipulated rule** | ✓ Claimed |
| The predicates GBP, BD, OC are **abstract/uninterpreted** for this task | ✓ Stipulated |
| Any deployed GCAT/BCAT system conforms to this rule | ✗ Not claimed |
| The Lean 4 candidate below is a **verified proof** | ✗ Not claimed — candidate only |
| The names GBP, BD, OC correspond to specific deployed fields | ✗ Not claimed |

---

### 4. Lean 4 Candidate (Logical Core)

```lean4
-- S2 Lean 4 Candidate: ALLOW Admissibility Characterization
-- STATUS: Candidate only. Not claimed to be verified or implementation-valid.
-- Governance: No deployed GCAT/BCAT binding claimed.

section AllowAdmissibility

/-- Abstract type of candidate transitions. -/
variable {T : Type}

/-- Abstract predicates on candidate transitions (stipulated names). -/
variable (GBP BD OC : T → Prop)

/-- Abstract outcome type. -/
inductive Outcome : Type where
  | ALLOW : Outcome
  | DENY  : Outcome
deriving DecidableEq

/-- The evaluator satisfies the stipulated rule by definition. -/
def evaluator (t : T) : Outcome :=
  if GBP t ∧ BD t ∧ OC t then Outcome.ALLOW else Outcome.DENY

/-- Theorem: ALLOW admissibility — necessary and sufficient characterization.
    This is a logical consequence of the stipulated rule encoded in `evaluator`. -/
theorem allow_iff (t : T) [Decidable (GBP t)] [Decidable (BD t)] [Decidable (OC t)] :
    evaluator GBP BD OC t = Outcome.ALLOW ↔ GBP t ∧ BD t ∧ OC t := by
  simp [evaluator]
  split_ifs with h
  · exact ⟨fun _ => h, fun _ => rfl⟩
  · exact ⟨fun hc => absurd hc (by simp [Outcome.ALLOW.injEq]),
           fun hc => absurd hc h⟩

/-- Corollary: DENY characterization. -/
theorem deny_iff (t : T) [Decidable (GBP t)] [Decidable (BD t)] [Decidable (OC t)] :
    evaluator GBP BD OC t = Outcome.DENY ↔ ¬(GBP t ∧ BD t ∧ OC t) := by
  simp [evaluator]
  split_ifs with h
  · exact ⟨fun hc => by simp [Outcome.DENY] at h