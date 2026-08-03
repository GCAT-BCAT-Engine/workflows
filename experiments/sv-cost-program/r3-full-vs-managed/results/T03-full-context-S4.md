S4: Complete informal proof.

## Artifact: S4 — Complete Informal Proof

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S4

---

### 1. Admitted Prior State

**[S0:sha256:dec7e81f740a2aff62a2d95aa715ac5f8374499cc47b41391d4bc224280859dc]**
S0 established: task parsing, logical reading of the stipulation, and claim boundary.

**[S1:sha256:45051b9dd8b477371597de6f845a0ded497ecb6528d53c3a3033502261637344]**
S1 established: universe of discourse (`T` arbitrary type), primitive predicates (`GBP`, `BD`, `OC : T → Prop`), definitional equality `ALLOW(t) := GBP(t) ∧ BD(t) ∧ OC(t)`, Claim S1.C1 as target, logical framework assumptions (intuitionistic, no classical axioms, `Prop`-valued).

**[S2:sha256:9378b75298b76732338fb08ea275c01cc12b5f07d09a0977c25255cc2c373bad]**
S2 established: formal theorem statement S2.T1 with named components S2.T1-Suff and S2.T1-Nec, proof sketches for both directions, confirmation that no classical axioms are required.

**[S3:sha256:d0d633ca8c62b06e9836042cbcd5d1e5a2327138bc9faebc98110598efbca1b9]**
S3 established: proof strategy (definitional unfolding, tactic selection rationale), lemma decomposition into S3.L1 (Sufficiency) and S3.L2 (Necessity), and a Lean 4 candidate for the logical core. No implementation validity was claimed.

---

### 2. Purpose of This Stage

S4 produces the **complete informal proof** of Theorem S2.T1. This means:

- Every inference step is stated explicitly in natural language,
- Each step is justified by reference to a named definition, assumption, or logical rule,
- The proof is **self-contained**: a reader with no prior exposure to this task can verify it by reading this artifact alone, consulting only the definitions admitted in S1,
- No step is deferred, abbreviated, or marked as obvious without justification,
- The proof is **constructive throughout**: no classical axioms are invoked.

---

### 3. Restatement of All Governing Definitions

For self-containment, the relevant definitions are restated here verbatim from S1.

**Definition S1.1 (Transition type).** `T` is an arbitrary non-empty type. Elements `t : T` are called candidate transitions.

**Definition S1.2 (GBP).** `GBP : T → Prop` is an arbitrary predicate on candidate transitions.

**Definition S1.3 (BD).** `BD : T → Prop` is an arbitrary predicate on candidate transitions.

**Definition S1.4 (OC).** `OC : T → Prop` is an arbitrary predicate on candidate transitions.

**Definition S1.5 (ALLOW).** For all `t : T`:
```
ALLOW(t)  :=  GBP(t) ∧ BD(t) ∧ OC(t)
```
This is a definitional equality. `ALLOW(t)` has no meaning independent of this definition within the scope of this task.

**Independence stipulation (S1).** No entailment relation among `GBP`, `BD`, and `OC` is assumed. They are logically independent.

---

### 4. The Theorem to Be Proved

**Theorem S2.T1 (ALLOW Admissibility — Necessary and Sufficient Characterization).**

Under the definitions above:

```
∀ t : T,  ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))
```

That is, for every candidate transition `t`, `ALLOW(t)` holds if and only if `GBP(t)`, `BD(t)`, and `OC(t)` all hold.

---

### 5. Preliminary Logical Rules Invoked

The proof uses only the following standard rules of intuitionistic propositional logic. Each is named for reference in the proof steps below.

| Rule Name | Statement |
|-----------|-----------|
| **Def-Unfold** | If `P := Q` by definition, then `P` and `Q` are interchangeable in any proof context. |
| **Iff-Intro** | To prove `P ↔ Q`, it suffices to prove `P → Q` and `Q → P` separately. |
| **Impl-Intro** | To prove `P → Q`, assume `P` and derive `Q`. |
| **Conj-Intro** | To prove `P ∧ Q`, provide a proof of `P` and a proof of `Q`. |
| **Conj-Elim-L** | From a proof of `P ∧ Q`, extract a proof of `P`. |
| **Conj-Elim-R** | From a proof of `P ∧ Q`, extract a proof of `Q`. |
| **Assumption** | If `P` is in the current hypothesis context, then `P` holds. |
| **Univ-Intro** | To prove `∀ x : T, P(x)`, let `t : T` be an arbitrary