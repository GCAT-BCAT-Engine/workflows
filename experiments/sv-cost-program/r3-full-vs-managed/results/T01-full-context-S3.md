# S3: Proof strategy and lemma decomposition

---

## 1. Stage Identity Record

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S3 — Proof strategy and lemma decomposition
**Prior admitted state:**
- [S0:sha256:465617e3cb2bf605f0bed1a2326711d64aa44f7fa6e2245387bd3fddb56cfb68]
- [S1:sha256:f21b80c04dbb247b6df1f337dbc06a763bc29397ca7931cd0f81e461e4365541]
- [S2:sha256:d9dd4f1093d7f2078f173bf32fd7186a8fc878f2e09ee49f4cdea11d122d457d]

---

## 2. Admitted Prior State (Carried Forward Unchanged)

All stipulations, definitions, assumptions, and claim boundaries from S0, S1, and S2 are preserved without modification. The following table records the items directly relevant to this stage.

| Item | Status | Content |
|------|--------|---------|
| `Transition` | `[STIPULATED]` | Abstract type; domain of all predicates |
| `GBP`, `BD`, `OC` | `[STIPULATED]` | Total predicates `Transition → Prop` |
| `ALLOW` | `[STIPULATED]` | Evaluator output predicate |
| Evaluator Axiom (EA) | `[STIPULATED]` | `∀ t, ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))` |
| `Admissible(t)` | `[DEFINITION — D1]` | Abbreviation: `GBP(t) ∧ BD(t) ∧ OC(t)` |
| T-ALLOW-CHAR | `[GENERATED — UNVERIFIED]` | `∀ t, ALLOW(t) ↔ Admissible(t)` |
| T-ALLOW-SUFF | `[GENERATED — UNVERIFIED]` | `∀ t, Admissible(t) → ALLOW(t)` |
| T-ALLOW-NECE | `[GENERATED — UNVERIFIED]` | `∀ t, ALLOW(t) → Admissible(t)` |
| C-EQUIV | `[GENERATED — UNVERIFIED]` | T-ALLOW-SUFF ∧ T-ALLOW-NECE ↔ T-ALLOW-CHAR |
| Assumptions A1–A4 | `[ADOPTED]` | Classical logic, decidability, determinism, no extra axioms |
| Claim boundary | `[PRESERVED]` | No implementation conformance claims made or implied |

---

## 3. Proof Strategy Overview

### 3.1 Strategic observation

The logical core of this task is structurally minimal. The Evaluator Axiom EA is itself a universally quantified biconditional. T-ALLOW-CHAR is the restatement of EA with the biconditional made explicit as a named theorem. Consequently:

- **No lemmas are logically required** to prove T-ALLOW-CHAR from EA. The proof is a single application of EA at an arbitrary `t`.
- However, **decomposition into lemmas is methodologically warranted** for three reasons:
  1. It makes the necessary and sufficient directions independently auditable.
  2. It provides named targets for the Lean 4 candidate, enabling `exact` or `apply` tactics to be used at each step without opaque automation.
  3. It separates the structural observation (biconditional decomposition) from the directional proofs, which is good practice for formal verification artifacts.

### 3.2 Chosen strategy: biconditional introduction via directed lemmas

The proof of T-ALLOW-CHAR proceeds by:

1. Proving **L-SUFF**: the forward direction `Admissible(t) → ALLOW(t)` for arbitrary `t`.
2. Proving **L-NECE**: the reverse direction `ALLOW(t) → Admissible(t)` for arbitrary `t`.
3. Combining L-SUFF and L-NECE via the biconditional introduction rule (`Iff.intro`) to obtain T-ALLOW-CHAR.

This strategy is **complete**: the two directed lemmas jointly exhaust the biconditional, and their combination is the theorem.

This strategy is **sound**: each directed lemma is proved directly from EA, which is the sole axiom governing `ALLOW`. No additional hypotheses are introduced.

---

## 4. Lemma Decomposition

### 4.1 Lemma L-SUFF — Sufficiency direction

> **[GENERATED — UNVERIFIED]** **Lemma L-SUFF**
>
> ```
> ∀ t : Transition,  GBP(t) ∧ BD(t) ∧ OC(t)  →  ALLOW(t)
> ```

**Proof strategy for L-SUFF:**

- Fix arbitrary `t : Transition`.
- Assume hypothesis `h : GBP(t) ∧ BD(t) ∧ OC(t)`.
- Instantiate EA at `t` to obtain `ea_t : ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))`.
- Extract the forward direction: `ea_t.mpr : (GBP(t) ∧