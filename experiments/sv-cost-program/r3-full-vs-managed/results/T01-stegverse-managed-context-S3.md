S3: Proof strategy and lemma decomposition

---

## 1. Recap of What Must Be Proved

From S2, the two primary claims are:

**S2-C1 (ALLOW characterization):**
> For all `t : T`, `E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`

**S2-C2 (DENY characterization):**
> For all `t : T`, `E(t) = DENY ↔ ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)`

Both are consequences of the single stipulated definition A4. The proof strategy must make the derivation structure explicit and identify every lemma needed to close the proof in Lean 4 without assuming classical decidability.

---

## 2. Proof Strategy Overview

### 2.1 Foundational Observation

A4 stipulates the evaluator *by definition*:

```
E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
```

This is not an empirical claim about a deployed system. It is a *definitional axiom* within the abstract model. Both S2-C1 and S2-C2 are therefore *analytic* consequences of A4 plus the two-valued structure of the codomain `{ALLOW, DENY}`.

The proof strategy is:

1. Encode A4 as a definitional axiom or hypothesis in Lean 4.
2. Prove S2-C1 by unfolding A4 (both directions are immediate).
3. Prove S2-C2 by combining A4 with the exhaustiveness of `{ALLOW, DENY}` (i.e., `ALLOW ≠ DENY` and every value is one or the other).
4. Decompose each biconditional into its two directed lemmas for auditability.

### 2.2 Why Classical Logic Is Not Required for S2-C1

S2-C1 is a biconditional whose right-to-left direction (`GBP(t) ∧ BD(t) ∧ OC(t) → E(t) = ALLOW`) and left-to-right direction (`E(t) = ALLOW → GBP(t) ∧ BD(t) ∧ OC(t)`) both follow directly from A4 by `Iff.mp` and `Iff.mpr`. No case analysis on the truth values of GBP, BD, OC is needed. No decidability assumption is invoked.

### 2.3 Why S2-C2 Requires One Additional Structural Lemma

S2-C2 involves `¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)`, which is the De Morgan dual of `¬(GBP(t) ∧ BD(t) ∧ OC(t))`. The equivalence of these two forms requires De Morgan's law, which in constructive logic requires classical reasoning (specifically `Classical.em` or `Classical.byContradiction`). This is the *only* classically non-constructive step in the entire proof.

Additionally, S2-C2 requires the structural lemma that `E(t) ≠ ALLOW → E(t) = DENY`, which follows from the exhaustiveness of the two-element type.

---

## 3. Lemma Decomposition

Each lemma is labeled, given its logical content, its dependency, and its proof method.

---

### Lemma S3-L1 — ALLOW Sufficiency
**Statement:** `GBP(t) ∧ BD(t) ∧ OC(t) → E(t) = ALLOW`
**Dependency:** A4 (right-to-left direction of the biconditional)
**Proof method:** `Iff.mpr` applied to A4
**Classical logic required:** No
**Notes:** This is the *sufficiency* direction of S2-C1.

---

### Lemma S3-L2 — ALLOW Necessity
**Statement:** `E(t) = ALLOW → GBP(t) ∧ BD(t) ∧ OC(t)`
**Dependency:** A4 (left-to-right direction of the biconditional)
**Proof method:** `Iff.mp` applied to A4
**Classical logic required:** No
**Notes:** This is the *necessity* direction of S2-C1.

---

### Lemma S3-L3 — Codomain Exhaustiveness
**Statement:** `∀ t : T, E(t) = ALLOW ∨ E(t) = DENY`
**Dependency:** The definition of the inductive type `Verdict` (or equivalent two-element type)
**Proof method:** `cases` on `E(t)`; each branch is closed by `Or.inl rfl` or `Or.inr rfl`
**Classical logic required:** No
**Notes:** This is a purely structural lemma about the codomain. It does not depend on GBP, BD, or OC.

---

### Lemma S3-L4 — ALLOW/DENY Distinctness
**Statement:** `ALLOW ≠ DENY`
**Dependency:** Inductive type definition; `decide` or `simp` closes it
**Proof method:** `decide` (if the type is a simple inductive with two constructors)
**Classical logic required:** No
**Notes:** Required to derive `E(t) = DENY` from `E(t) ≠ ALLOW`.

---

### Lemma S3