S2: Theorem formulation.

---

## Artifact: S2 — Theorem Formulation

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S2

---

### 1. Admitted Prior State

**[S0:sha256:dec7e81f740a2aff62a2d95aa715ac5f8374499cc47b41391d4bc224280859dc]**
S0 established: task parsing, logical reading of the stipulation, and claim boundary.

**[S1:sha256:45051b9dd8b477371597de6f845a0ded497ecb6528d53c3a3033502261637344]**
S1 established: universe of discourse (`T` arbitrary non-empty type), primitive predicates (`GBP`, `BD`, `OC` as logically independent `T → Prop`), definitional equality `ALLOW(t) := GBP(t) ∧ BD(t) ∧ OC(t)`, Claim S1.C1 as the target, and logical framework assumptions (intuitionistic, no classical axioms required, `Prop`-valued).

---

### 2. Purpose of This Stage

S2 produces the **formal theorem statement** for Claim S1.C1, together with:

- A **proof sketch** establishing both directions,
- An explicit account of **why no classical axioms are needed**,
- The **named theorem** in a form suitable for direct transcription into Lean 4 in S3.

No Lean 4 syntax is produced here. S3 carries that responsibility.

---

### 3. Recapitulation of the Governing Definition

For reference, the governing definition admitted in S1 is:

> **Definition S1.5.** For all `t : T`,
> ```
> ALLOW(t)  :=  GBP(t) ∧ BD(t) ∧ OC(t)
> ```

This is a **definitional equality**. In the logical framework, `ALLOW(t)` and `GBP(t) ∧ BD(t) ∧ OC(t)` are **definitionally equal** (identical by unfolding). The biconditional is therefore not a substantive empirical or structural claim; it is a **logical consequence of the definition alone**.

---

### 4. Formal Theorem Statement

**Theorem S2.T1 (ALLOW Admissibility — Necessary and Sufficient Characterization).**

Let `T` be an arbitrary type. Let `GBP BD OC : T → Prop` be arbitrary predicates. Define `ALLOW : T → Prop` by

```
ALLOW(t)  :=  GBP(t) ∧ BD(t) ∧ OC(t)
```

Then:

```
∀ t : T,  ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))
```

**Named components:**

| Label | Statement |
|-------|-----------|
| **S2.T1-Suff** (Sufficiency) | `∀ t : T, GBP(t) ∧ BD(t) ∧ OC(t) → ALLOW(t)` |
| **S2.T1-Nec** (Necessity) | `∀ t : T, ALLOW(t) → GBP(t) ∧ BD(t) ∧ OC(t)` |
| **S2.T1** (Biconditional) | `∀ t : T, ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))` |

S2.T1 is the conjunction of S2.T1-Suff and S2.T1-Nec.

---

### 5. Proof Sketch

#### 5.1 Sufficiency (S2.T1-Suff)

**Goal:** `GBP(t) ∧ BD(t) ∧ OC(t) → ALLOW(t)`

**Proof:**
Let `t : T` be arbitrary. Assume `h : GBP(t) ∧ BD(t) ∧ OC(t)`.
By Definition S1.5, `ALLOW(t)` unfolds to `GBP(t) ∧ BD(t) ∧ OC(t)`.
The assumption `h` is therefore exactly a proof of `ALLOW(t)` after unfolding.
Hence `ALLOW(t)` holds. ∎

**Proof-theoretic note:** This direction uses only **conjunction introduction** (already present in `h`) and **definitional unfolding**. No elimination rules, no classical axioms.

---

#### 5.2 Necessity (S2.T1-Nec)

**Goal:** `ALLOW(t) → GBP(t) ∧ BD(t) ∧ OC(t)`

**Proof:**
Let `t : T` be arbitrary. Assume `h : ALLOW(t)`.
By Definition S1.5, `ALLOW(t)` unfolds to `GBP(t) ∧ BD(t) ∧ OC(t)`.
Therefore `h` is a proof of `GBP(t) ∧ BD(t) ∧ OC(t)` after unfolding.
Hence `GBP(t) ∧ BD(t) ∧ OC(t)` holds. 