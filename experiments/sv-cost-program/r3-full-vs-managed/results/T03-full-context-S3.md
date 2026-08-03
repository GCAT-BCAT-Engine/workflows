# S3: Proof strategy and lemma decomposition

## Artifact: S3 — Proof Strategy and Lemma Decomposition

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S3

---

### 1. Admitted Prior State

**[S0:sha256:dec7e81f740a2aff62a2d95aa715ac5f8374499cc47b41391d4bc224280859dc]**
S0 established: task parsing, logical reading of the stipulation, and claim boundary.

**[S1:sha256:45051b9dd8b477371597de6f845a0ded497ecb6528d53c3a3033502261637344]**
S1 established: universe of discourse (`T` arbitrary type), primitive predicates (`GBP`, `BD`, `OC : T → Prop`), definitional equality `ALLOW(t) := GBP(t) ∧ BD(t) ∧ OC(t)`, Claim S1.C1 as target, logical framework assumptions (intuitionistic, no classical axioms, `Prop`-valued).

**[S2:sha256:9378b75298b76732338fb08ea275c01cc12b5f07d09a0977c25255cc2c373bad]**
S2 established: formal theorem statement S2.T1 with named components S2.T1-Suff and S2.T1-Nec, proof sketches for both directions, and confirmation that no classical axioms are required. Both directions reduce to definitional unfolding of `ALLOW`.

---

### 2. Purpose of This Stage

S3 produces:

- A **proof strategy** for S2.T1, identifying the tactic structure to be used in Lean 4,
- A **lemma decomposition** naming each sub-goal explicitly,
- An account of **which Lean 4 mechanisms** handle each step,
- A **Lean 4 candidate** for the logical core.

The Lean 4 candidate is presented as a **candidate only**. No claim is made that it compiles without error in any specific Lean 4 toolchain version, nor that it constitutes a verified artifact. Implementation validity is not claimed.

---

### 3. Proof Strategy

#### 3.1 Central Observation

Because `ALLOW` is introduced by a **definitional equality** (`ALLOW(t) := GBP(t) ∧ BD(t) ∧ OC(t)`), the biconditional S2.T1 holds **by definitional reduction**. In Lean 4, this means:

- The `unfold` or `simp only` tactic (or `rfl`-adjacent reasoning at the `Iff` level) suffices to close both directions.
- No induction, case analysis, or classical reasoning is required.
- The proof is **structurally trivial** once the definition is in scope.

The non-trivial work of this stage is therefore **organizational**: making the decomposition explicit so that the Lean 4 candidate is readable, auditable, and correctly scoped.

#### 3.2 Tactic Selection Rationale

| Tactic | Role | Justification |
|--------|------|---------------|
| `intro t` | Universally quantify over `t : T` | Required to discharge `∀ t : T` |
| `constructor` | Split `↔` into `→` and `←` | Standard `Iff.intro` decomposition |
| `intro h` | Introduce hypothesis in each direction | Standard assumption introduction |
| `exact h` | Close goal after definitional unfolding | `ALLOW(t)` and `GBP(t) ∧ BD(t) ∧ OC(t)` are definitionally equal; `h` is a direct proof |
| `unfold ALLOW` | Make the definition explicit (optional) | Aids readability and auditability; not logically required if `exact h` suffices by definitional equality |

**Alternative:** The entire theorem may be closable by `tauto` or `simp [ALLOW]` in a single step. The decomposed form is preferred here for auditability.

---

### 4. Lemma Decomposition

The following named lemmas correspond exactly to the components identified in S2.

---

#### Lemma S3.L1 (Sufficiency)

**Statement:**
```
∀ (t : T), GBP t ∧ BD t ∧ OC t → ALLOW t
```

**Proof strategy:**
1. Introduce `t : T`.
2. Introduce `h : GBP t ∧ BD t ∧ OC t`.
3. Unfold `ALLOW`. The goal becomes `GBP t ∧ BD t ∧ OC t`.
4. Close with `exact h`.

**Lean 4 mechanism:** Definitional unfolding. `ALLOW t` reduces to `GBP t ∧ BD t ∧ OC t` by the `def` declaration. After `unfold ALLOW`, the goal is syntactically identical to `h`.

**Dependencies:** Definition S1.5 only.

**Classical axioms required:** None.

---

#### Lemma S3.L2 (Necessity)

**Statement:**
```
∀ (t : T), ALLOW t → GBP t ∧ BD t ∧ OC t
```

**Proof strategy:**
1. Introduce `t : T`.
2. Introduce `h : ALLOW t`.
3. Unfold `ALLOW` in `h`. The hypothesis becomes `h : GBP t ∧ BD t ∧