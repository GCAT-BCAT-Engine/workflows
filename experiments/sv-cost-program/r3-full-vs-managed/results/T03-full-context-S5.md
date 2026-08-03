S5: Lean 4 candidate.

## Artifact: S5 — Lean 4 Candidate

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S5

---

### 1. Admitted Prior State

**[S0:sha256:dec7e81f740a2aff62a2d95aa715ac5f8374499cc47b41391d4bc224280859dc]**
S0 established: task parsing, logical reading of the stipulation, and claim boundary.

**[S1:sha256:45051b9dd8b477371597de6f845a0ded497ecb6528d53c3a3033502261637344]**
S1 established: universe of discourse (`T` arbitrary type), primitive predicates (`GBP`, `BD`, `OC : T → Prop`), definitional equality `ALLOW(t) := GBP(t) ∧ BD(t) ∧ OC(t)`, Claim S1.C1 as target, logical framework assumptions (intuitionistic, no classical axioms, `Prop`-valued).

**[S2:sha256:9378b75298b76732338fb08ea275c01cc12b5f07d09a0977c25255cc2c373bad]**
S2 established: formal theorem statement S2.T1 with named components S2.T1-Suff and S2.T1-Nec, proof sketches for both directions, confirmation that no classical axioms are required.

**[S3:sha256:d0d633ca8c62b06e9836042cbcd5d1e5a2327138bc9faebc98110598efbca1b9]**
S3 established: proof strategy (definitional unfolding, tactic selection rationale), lemma decomposition into S3.L1 (Sufficiency) and S3.L2 (Necessity).

**[S4:sha256:1bf27aacbe7040f35041065c7021ec848fbcd83569f17343a0d74af10f740b95]**
S4 established: complete informal proof of Theorem S2.T1, with every inference step stated explicitly, justified by named rules, and confirmed constructive throughout. No classical axioms invoked.

---

### 2. Purpose of This Stage

S5 produces the **Lean 4 candidate** for the logical core of Theorem S2.T1. This artifact:

- Transcribes the informal proof of S4 into Lean 4 syntax,
- Decomposes the proof into named lemmas corresponding to S3.L1 and S3.L2,
- Presents the main theorem S2.T1 as a named `theorem`,
- Includes inline annotations explaining each tactic step,
- Is presented as a **candidate only**.

**Implementation validity is not claimed.** This artifact has not been run against any Lean 4 toolchain. No claim is made that it compiles without error in any specific version of Lean 4 or Mathlib. It is offered as a faithful transcription of the informal proof for audit and subsequent verification.

---

### 3. Stipulations Governing This Artifact

| Stipulation | Status |
|-------------|--------|
| The Lean 4 candidate faithfully represents the logical structure of S2.T1 and S4 | **Claimed** |
| The Lean 4 candidate compiles without error in any specific toolchain | **Not claimed** |
| Any deployed GCAT/BCAT implementation conforms to this characterization | **Not claimed** |
| `GBP`, `BD`, `OC` have semantic content beyond their role as arbitrary `T → Prop` predicates | **Not claimed** |
| Classical axioms are invoked anywhere in this candidate | **Not claimed; the candidate is designed to avoid them** |

---

### 4. Lean 4 Candidate

```lean
/-
  Artifact: S5 — Lean 4 Candidate
  Experiment: SV-COST-R3-FULL-VS-MANAGED-001
  Task: SV-MATH-001-STAGED

  CANDIDATE ONLY. Implementation validity is not claimed.
  This file has not been verified against any Lean 4 toolchain.
  It is a faithful transcription of the informal proof in S4.

  Claim boundary:
  - In scope:  the logical structure of Theorem S2.T1 as an abstract claim.
  - Out of scope: any deployed GCAT/BCAT implementation.
  - Out of scope: semantic content of GBP, BD, OC beyond their type signatures.
-/

-- ============================================================
-- Section 1: Universe of Discourse and Primitive Predicates
-- (Corresponds to S1: Definitions and Assumptions)
-- ============================================================

-- T is an arbitrary type of candidate transitions.
-- No structure is imposed on T beyond its existence as a type.
-- GBP, BD, OC are arbitrary Prop-valued predicates on T.
-- They are introduced as variables so that all subsequent
-- definitions and theorems are universally quantified over them.

variable {T : Type*}
variable (GBP BD OC : T → Prop)

-- ============================================================
-- Section 2: Definition of ALLOW
-- (Corresponds to Definition S1.5)
-- ============================================================

-- ALLOW is defined as the conjunction of GBP, BD, and OC.
-- This is a definitional equality, not a derived theorem.
-- ALLOW(t) and GBP(t) ∧ BD(t) ∧ OC(t) are interchangeable
-- by unfolding throughout all subsequent proofs.

def ALLOW (t : T) : Prop