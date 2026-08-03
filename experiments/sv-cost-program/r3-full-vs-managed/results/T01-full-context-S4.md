S4: Complete informal proof

---

## 1. Stage Identity Record

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S4 — Complete informal proof
**Prior admitted state:**
- [S0:sha256:465617e3cb2bf605f0bed1a2326711d64aa44f7fa6e2245387bd3fddb56cfb68]
- [S1:sha256:f21b80c04dbb247b6df1f337dbc06a763bc29397ca7931cd0f81e461e4365541]
- [S2:sha256:d9dd4f1093d7f2078f173bf32fd7186a8fc878f2e09ee49f4cdea11d122d457d]
- [S3:sha256:bc7da0849c187c3cf66e1bdcfe6666a8767e6b5c626f3264d8768e7d8b8415ac]

---

## 2. Admitted Prior State (Carried Forward Unchanged)

All stipulations, definitions, assumptions, and claim boundaries from S0–S3 are preserved without modification.

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
| L-SUFF | `[GENERATED — UNVERIFIED, from S3]` | Sufficiency lemma, proof strategy recorded |
| L-NECE | `[GENERATED — UNVERIFIED, from S3]` | Necessity lemma, proof strategy recorded |
| Assumptions A1–A4 | `[ADOPTED]` | Classical logic, decidability, determinism, no extra axioms |
| Claim boundary | `[PRESERVED]` | No implementation conformance claims made or implied |

---

## 3. Preliminary Remarks on Proof Structure

The informal proof proceeds in three parts, corresponding to the three proof obligations identified in S3:

- **Part I:** Proof of L-SUFF (sufficiency direction).
- **Part II:** Proof of L-NECE (necessity direction).
- **Part III:** Assembly of T-ALLOW-CHAR from L-SUFF and L-NECE via biconditional introduction.

Each part is written at the level of detail appropriate for direct transcription into a Lean 4 term-mode or tactic-mode proof in S5. Every inference step is named and justified by reference to the admitted axiom or a prior step. No step appeals to any fact not in the admitted prior state.

The proofs are **complete** in the sense that no step is deferred, elided, or marked as obvious without explicit justification. The proofs are **sound** relative to the admitted axioms: every conclusion follows from EA and standard propositional rules alone.

---

## 4. Part I — Proof of L-SUFF (Sufficiency)

**Statement.**
`∀ t : Transition, GBP(t) ∧ BD(t) ∧ OC(t) → ALLOW(t)`

**Proof.**

Let `t : Transition` be arbitrary. We must show: if `GBP(t) ∧ BD(t) ∧ OC(t)`, then `ALLOW(t)`.

**Step 1.** Assume `h : GBP(t) ∧ BD(t) ∧ OC(t)`.

This is the hypothesis of the implication. It asserts that all three predicates hold simultaneously of `t`. No further decomposition of `h` into its conjuncts is needed for this step; the conjunction is passed whole to Step 3.

**Step 2.** Instantiate EA at `t`.

From the Evaluator Axiom EA — `∀ t, ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))` — by universal instantiation at the fixed `t`, we obtain:

```
ea_t : ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))
```

This is a biconditional. It has two components:
- Forward component: `ea_t.mp  : ALLOW(t) → (GBP(t) ∧ BD(t) ∧ OC(t))`
- Reverse component: `ea_t.mpr