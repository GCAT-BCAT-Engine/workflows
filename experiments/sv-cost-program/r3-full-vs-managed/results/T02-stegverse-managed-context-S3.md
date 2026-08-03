S3: Proof strategy and lemma decomposition

---

## GOVERNANCE HEADER

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S3 — Proof strategy and lemma decomposition
**Context mode:** managed
**Admitted prior state:** S0, S1, S2 (see ARTIFACT_LEDGER above)
**Unresolved (carried forward):** Deployed implementation binding remains unresolved. Nothing in this artifact claims any deployed GCAT/BCAT system conforms to the formal model.

---

## SECTION 1 — Admitted prior state (preserved, not re-derived)

From S1 (stipulations, not empirical claims):

- **S1-D2:** `GBP : T → Prop`
- **S1-D3:** `BD : T → Prop`
- **S1-D4:** `OC : T → Prop`
- **S1-D5:** `E(t) = ALLOW ⟺ GBP(t) ∧ BD(t) ∧ OC(t)` (definitional)
- **S1-D6:** `ALLOW_admissible(t) ↔ E(t) = ALLOW` (definitional)

From S2 (generated claims, not verified against any implementation):

- **S2-C1:** The biconditional `allow_admissible_iff` is provable by definitional unfolding (`Iff.rfl` or `simp only [...]`).
- **S2-C2 (necessary direction):** `allow_admissible_necessary` — if `ALLOW_admissible(t)` then `GBP(t) ∧ BD(t) ∧ OC(t)`.
- **S2-C3 (sufficient direction):** `allow_admissible_sufficient` — if `GBP(t) ∧ BD(t) ∧ OC(t)` then `ALLOW_admissible(t)`.

---

## SECTION 2 — Proof strategy

### 2.1 Overall structure

Because S1-D5 and S1-D6 are **definitional equalities** (not axioms with independent content), the biconditional `allow_admissible_iff` collapses to a reflexivity proof. The proof strategy is therefore:

> **Strategy:** Unfold all definitions simultaneously. The goal reduces to `P ↔ P` for `P = GBP(t) ∧ BD(t) ∧ OC(t)`, which is closed by `Iff.rfl`.

The necessary and sufficient directions are then **corollaries** extracted from the biconditional by `Iff.mp` and `Iff.mpr` respectively. No non-trivial reasoning steps are required.

### 2.2 Proof shape (schematic)

```
allow_admissible_iff
  └─ unfold ALLOW_admissible, E, ALLOW
       └─ goal: GBP t ∧ BD t ∧ OC t ↔ GBP t ∧ BD t ∧ OC t
            └─ Iff.rfl

allow_admissible_necessary
  └─ intro h
       └─ exact (allow_admissible_iff t).mp h

allow_admissible_sufficient
  └─ intro h
       └─ exact (allow_admissible_iff t).mpr h
```

### 2.3 Dependency graph

```
S1-D5 (def: E)
S1-D6 (def: ALLOW_admissible)
        │
        ▼
  allow_admissible_iff   ←── Iff.rfl (after unfolding)
        │
   ┌────┴────┐
   ▼         ▼
necessary  sufficient
(Iff.mp)  (Iff.mpr)
```

No lemma depends on any other non-definitional fact. The graph is a shallow tree of depth 1.

---

## SECTION 3 — Lemma decomposition

### Lemma S3-L1 (Definitional unfolding — biconditional)

**Statement (informal):**
For all `t : T`, `ALLOW_admissible(t)` unfolds to `GBP(t) ∧ BD(t) ∧ OC(t)`, and the biconditional with itself is reflexive.

**Proof obligation:** Confirm that `ALLOW_admissible` and `E` are defined (not axiomatized) so that `unfold` or `simp only` with the definition lemmas reduces the goal to `P ↔ P`.

**Status:** Dischargeable by `Iff.rfl` after unfolding. No open subgoals.

**Boundary note:** This lemma characterizes the abstract model only. It does not characterize any deployed evaluator.

---

### Lemma S3-L2 (Necessary direction)

**Statement (informal):**
If `ALLOW_admissible(t)` holds, then `GBP(t) ∧ BD(t) ∧ OC(t)`.

**Derivation:** Immediate from S3-L1 via `Iff.mp`.

**Proof obligation:** None beyond S3-L1.

**Status:** Dischargeable as a one-line corollary.

---

### Lemma S3-L3 (Sufficient direction)

**Statement (informal):**
If `GBP(t) ∧ BD(t)