S6: Verification ledger.

## Artifact: S6 — Verification Ledger

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S6

---

### 1. Admitted Prior State

**[S0:sha256:dec7e81f740a2aff62a2d95aa715ac5f8374499cc47b41391d4bc224280859dc]**
S0 established: task parsing, logical reading of the stipulation, claim boundary. Biconditional `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)` identified as central logical claim. No implementation validity claimed.

**[S1:sha256:45051b9dd8b477371597de6f845a0ded497ecb6528d53c3a3033502261637344]**
S1 established: universe of discourse (`T` arbitrary type), primitive predicates (`GBP`, `BD`, `OC : T → Prop`), definitional equality `ALLOW(t) := GBP(t) ∧ BD(t) ∧ OC(t)`, Claim S1.C1 as target, logical framework assumptions (intuitionistic, no classical axioms, `Prop`-valued).

**[S2:sha256:9378b75298b76732338fb08ea275c01cc12b5f07d09a0977c25255cc2c373bad]**
S2 established: formal theorem statement S2.T1 with named components S2.T1-Suff and S2.T1-Nec, proof sketches for both directions, confirmation that no classical axioms are required.

**[S3:sha256:d0d633ca8c62b06e9836042cbcd5d1e5a2327138bc9faebc98110598efbca1b9]**
S3 established: proof strategy (definitional unfolding, tactic selection rationale), lemma decomposition into S3.L1 (Sufficiency) and S3.L2 (Necessity), Lean 4 candidate structure.

**[S4:sha256:1bf27aacbe7040f35041065c7021ec848fbcd83569f17343a0d74af10f740b95]**
S4 established: complete informal proof of Theorem S2.T1, every inference step stated explicitly, justified by named rules, confirmed constructive throughout. No classical axioms invoked.

**[S5:sha256:ffd8a6d6e0ad9116d5c78d79e917b08d56623440cfe7a77b03a0d644af3b60c4]**
S5 established: Lean 4 candidate for the logical core, presented as candidate only. Implementation validity not claimed. Candidate transcribes S4 informal proof into Lean 4 syntax with inline annotations. Artifact ends mid-definition of `ALLOW` due to stage boundary.

---

### 2. Purpose of This Stage

S6 produces the **verification ledger**: a structured record of every claim generated across S0–S5, its current verification status, the evidence basis for that status, and any unresolved items. The ledger is the authoritative record of what has and has not been established by this task sequence.

The ledger does **not** advance any new claims. It consolidates and audits prior state.

---

### 3. Ledger Structure

Each entry records:

| Field | Meaning |
|-------|---------|
| **ID** | Unique identifier for the claim or item |
| **Stage** | Stage in which the item was introduced |
| **Type** | Stipulation / Generated Claim / Verified Claim / Unresolved Implementation Evidence |
| **Statement** | Precise statement of the item |
| **Status** | Admitted / Established / Candidate / Unresolved / Out of Scope |
| **Evidence Basis** | What supports the current status |
| **Notes** | Caveats, dependencies, or forward references |

---

### 4. Ledger Entries

---

#### Entry L-001

| Field | Content |
|-------|---------|
| **ID** | L-001 |
| **Stage** | S0 |
| **Type** | Stipulation |
| **Statement** | The abstract evaluator returns `ALLOW` exactly when `GBP` and `BD` and `OC` all hold. Formally: `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)`. |
| **Status** | **Admitted** |
| **Evidence Basis** | Given by task statement. Admitted as governing stipulation in S0. Not derived; not subject to proof. |
| **Notes** | This stipulation is the sole source of the definition of `ALLOW`. All subsequent claims depend on it. It does not describe any deployed system. |

---

#### Entry L-002

| Field | Content |
|-------|---------|
| **ID** | L-002 |
| **Stage** | S1 |
| **Type** | Stipulation |
| **Statement** | `T` is an arbitrary non-empty type. `GBP`, `BD`, `OC : T → Prop` are logically independent predicates. No entailment among them is assumed. |
| **Status** | **Admitted** |
| **Evidence Basis** | Introduced in S1 as framework assumptions S1.A1–S1.A3 and independence stipulation. |
| **Notes** | The independence stipulation means no direction of the biconditional can be collapsed or simplified by assumed entailments. The proof must hold for all possible assignments of `