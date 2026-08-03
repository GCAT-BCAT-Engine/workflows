S2: Theorem formulation.

---

## Artifact: S2 — Theorem Formulation

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S2

---

### Admitted Prior State

[S0:sha256:88c1f97e1f6599962b876deef766f4c1a9a454be1080a64de3380e78518083f3]
[S1:sha256:2538cec9627a6b36eb5cc3751eed63e21b4e1123634b5ef6d60f39edb19dca24]

S0 established: task parsing and claim boundary.
S1 established: universe of discourse (`T`), predicate stipulations (`GBP`, `BD`, `OC`), evaluator semantics (`ALLOW` defined by biconditional, Stipulation S1.5), and explicit non-assumptions A1–A5. All prior content is admitted without modification.

---

### 1. The Central Theorem (Generated Claim)

The following is a **generated claim**, derived from the stipulations of S1. It is not itself a stipulation. Its status as a theorem depends on the derivation given in Section 2 below.

---

**Theorem S2.T1 (Necessary and Sufficient Characterization of ALLOW Admissibility):**

> Let `T` be an arbitrary non-empty type. Let `GBP`, `BD`, `OC : T → Prop` be arbitrary predicates. Let `ALLOW : T → Prop` be defined by Stipulation S1.5. Then for all `t : T`:
>
> `ALLOW(t)` **if and only if** `GBP(t) ∧ BD(t) ∧ OC(t)`.
>
> That is:
>
> `∀ t : T, ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))`

---

### 2. Derivation

The derivation proceeds in two directions, as required by the biconditional.

**Stipulation S1.5 (recalled):**
`∀ t : T, ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))`

This biconditional is the **sole definitional source** for `ALLOW`. The theorem S2.T1 is therefore **immediate by definition**: the statement of S2.T1 is identical in logical content to Stipulation S1.5.

The derivation is thus:

- **(→) Necessity:** Assume `ALLOW(t)`. By S1.5 (forward direction), `GBP(t) ∧ BD(t) ∧ OC(t)` holds. Therefore, each of `GBP(t)`, `BD(t)`, `OC(t)` is necessary for `ALLOW(t)`.

- **(←) Sufficiency:** Assume `GBP(t) ∧ BD(t) ∧ OC(t)`. By S1.5 (reverse direction), `ALLOW(t)` holds. Therefore, the conjunction is sufficient for `ALLOW(t)`.

Both directions are established directly from S1.5. No additional lemmas, auxiliary hypotheses, or structural properties of `T` are required. The derivation is valid in classical and constructive propositional logic alike, since it uses only the biconditional introduction and elimination rules.

---

### 3. Claim Boundary Analysis

The following table records precisely what S2.T1 does and does not assert.

| Claim | Status |
|---|---|
| `∀ t : T, ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))` | **Generated claim — established** by derivation from S1.5 |
| `GBP`, `BD`, `OC` are independent predicates | **Not claimed** — S1 explicitly withholds this (A2) |
| Any particular `t` satisfies or fails any predicate | **Not claimed** — S1 explicitly withholds this (A3) |
| The evaluator is computable or decidable | **Not claimed** — S1 explicitly withholds this (A4) |
| Any deployed GCAT/BCAT system satisfies this characterization | **Not claimed** — out of scope (A5, S0 boundary) |
| The Lean 4 candidate (to be produced at S3) is verified | **Not claimed** — reserved for S3; implementation validity not asserted |
| S2.T1 is a non-trivial mathematical discovery | **Not claimed** — it is immediate from the definition; its value is formal precision, not novelty |

---

### 4. Corollaries (Generated Claims, Immediate)

The following corollaries follow directly from S2.T1 by standard propositional logic. They are stated for completeness and to support S3 encoding.

**Corollary S2.C1 (Necessity of each conjunct):**
`∀ t : T, ALLOW(t) → GBP(t)`
`∀ t : T, ALLOW(t) → BD(t)`
`∀ t : T, ALLOW(t) → OC(t)`

*Derivation:* From S2.T1 (→ direction) and conjunction elimination.

**Corollary S2.C2 (Sufficiency of the conjunction):**
`∀ t : T, GBP(t) → BD(t) → OC(t) → ALLOW(t