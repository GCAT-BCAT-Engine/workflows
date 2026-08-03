S3: Proof strategy and lemma decomposition.

---

## Artifact: S3 — Proof Strategy and Lemma Decomposition

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S3

---

### Admitted Prior State

[S0:sha256:88c1f97e1f6599962b876deef766f4c1a9a454be1080a64de3380e78518083f3]
[S1:sha256:2538cec9627a6b36eb5cc3751eed63e21b4e1123634b5ef6d60f39edb19dca24]
[S2:sha256:234757af8fc343df9d94434a9115f15586a28c18b1efd3c97c1fb88cabd31969]

S0 established: task parsing and claim boundary.
S1 established: universe of discourse (`T`), predicate stipulations (`GBP`, `BD`, `OC`), evaluator semantics (`ALLOW` defined by biconditional, Stipulation S1.5), and explicit non-assumptions A1–A5.
S2 established: Theorem S2.T1 (`∀ t : T, ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))`), its derivation, claim boundary analysis, and Corollaries S2.C1 and S2.C2.
All prior content is admitted without modification.

---

### 1. Purpose of S3

S3 has two responsibilities:

1. **Proof strategy:** Identify the proof-theoretic structure required to establish S2.T1 and its corollaries in a formal proof assistant (Lean 4), and justify why that structure is sufficient.
2. **Lemma decomposition:** Decompose the logical core into named lemmas at a granularity suitable for Lean 4 encoding, with each lemma's statement, proof obligation, and dependency recorded explicitly.
3. **Lean 4 candidate:** Produce the candidate encoding. Implementation validity is **not claimed**.

---

### 2. Proof-Theoretic Observations

**Observation S3.O1 (Definitional collapse):**
S2.T1 is logically identical to Stipulation S1.5. The theorem does not require a non-trivial proof search. In a formal system, the proof reduces to unfolding the definition of `ALLOW` and applying `Iff.intro` with the two directions supplied by the definition itself.

**Observation S3.O2 (Constructive validity):**
The proof uses only:
- Biconditional introduction (`Iff.intro`)
- Biconditional elimination (`Iff.mp`, `Iff.mpr`)
- Conjunction introduction (`And.intro`)
- Conjunction elimination (`And.left`, `And.right`, pattern matching)

No classical axioms (excluded middle, choice) are required. The proof is valid in constructive type theory, which is the foundation of Lean 4's kernel.

**Observation S3.O3 (Proof term structure):**
The proof term for S2.T1 is:
```
Iff.intro
  (fun h => h)          -- forward: ALLOW(t) → GBP(t) ∧ BD(t) ∧ OC(t)
  (fun h => h)          -- backward: GBP(t) ∧ BD(t) ∧ OC(t) → ALLOW(t)
```
when `ALLOW` is defined as `def ALLOW (t : T) : Prop := GBP t ∧ BD t ∧ OC t`, because the two sides are definitionally equal. The proof is `Iff.rfl` or `Iff.intro id id` depending on the encoding choice.

**Observation S3.O4 (Encoding choice and its effect):**
There are two encoding strategies:

| Strategy | Description | Proof obligation for S2.T1 |
|---|---|---|
| **Def-encoding** | `ALLOW` is defined as `GBP t ∧ BD t ∧ OC t` | S2.T1 is `Iff.rfl` (definitional) |
| **Axiom-encoding** | `ALLOW` is an opaque predicate; S1.5 is an axiom | S2.T1 requires applying the axiom |

The Lean 4 candidate will use **Def-encoding** as the primary form, with the axiom-encoding variant noted. Def-encoding is preferred because it avoids introducing axioms and keeps the proof kernel-checkable without additional trust.

---

### 3. Lemma Decomposition

The following lemmas are identified. Each is a **generated claim**. None is asserted to be verified by a running proof checker at this stage.

---

**Lemma S3.L1 (Forward direction — Necessity):**

*Statement:*
`∀ (T : Type) (GBP BD OC : T → Prop) (t : T), ALLOW GBP BD OC t → GBP t ∧ BD t ∧ OC t`

*Proof obligation:*
Assume `h : ALLOW GBP BD OC t`. Unfold the definition of `ALLOW`. The hypothesis `h` is already of type `GBP t ∧ BD t ∧ OC t`. Return `h`.

*Dependencies:* Definition of `ALLOW` (Def-encoding).

*Proof term candidate:* `fun h => h` (identity, after unfolding).

---

**Lemma