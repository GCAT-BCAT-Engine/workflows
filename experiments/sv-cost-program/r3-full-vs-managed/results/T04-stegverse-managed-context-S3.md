S3: Proof strategy and lemma decomposition.

---

## ARTIFACT: S3 — Proof Strategy and Lemma Decomposition

---

### Admitted Prior State (preserved)

- **S0** (sha256:b44121bb1cdd65ee8dd01278fe146d2e95fd3ace2868a16a4712f69ddd18dbdb): Stipulated rule — evaluator returns ALLOW exactly when GBP ∧ BD ∧ OC all hold. No deployed implementation binding claimed.
- **S1** (sha256:bfdeb98763fdf4539643c6b0a40851bd41833a816139f02f5b1915e9a9d4a873): Types and predicates stipulated. `T` is an abstract type; `GBP`, `BD`, `OC : T → Prop`. No correspondence to deployed fields claimed.
- **S2** (sha256:d47ff000acc7760ebea79f7d31c942b664c0552b8c502419a5c9481ee7e1481b): Theorem formulation. Target theorems:
  - `allow_iff (t : T) : eval t = ALLOW ↔ GBP t ∧ BD t ∧ OC t`
  - `deny_iff (t : T) : eval t = DENY ↔ ¬(GBP t ∧ BD t ∧ OC t)`

**Unresolved (carried forward):** Deployed implementation binding remains unresolved at all prior stages.

---

### 1. Proof Strategy Overview

The target theorems are biconditionals. The standard strategy for each is:

1. **Split** the `↔` into two implications: the forward direction (→) and the backward direction (←).
2. **Forward direction** (`eval t = ALLOW → GBP t ∧ BD t ∧ OC t`): unfold the definition of `eval`, use the stipulated rule to extract the conjunction.
3. **Backward direction** (`GBP t ∧ BD t ∧ OC t → eval t = ALLOW`): unfold the definition of `eval`, apply the stipulated rule to conclude ALLOW.
4. **`deny_iff`** is derived from `allow_iff` by the exhaustiveness of `{ALLOW, DENY}` and the law of excluded middle (or decidability).

The proof is purely propositional/definitional. No induction, no recursion, no arithmetic. The logical core reduces to:

- Unfolding a definition.
- Splitting and introducing conjunctions.
- Case analysis on the two-element result type.

---

### 2. Lemma Decomposition

The following lemmas are identified. Each is labeled, stated informally, and given a Lean 4 candidate signature. No lemma is claimed proven; all are candidates.

---

#### Lemma L1 — Evaluation Definition Unfolding

**Informal statement:** The evaluator `eval` on input `t` returns ALLOW if and only if the body of its definition holds, i.e., `GBP t ∧ BD t ∧ OC t`.

**Role:** This is the definitional bridge. It converts between the opaque `eval t = ALLOW` and the transparent propositional content. In Lean 4, if `eval` is defined by `if GBP t ∧ BD t ∧ OC t then ALLOW else DENY`, this lemma is discharged by `simp` or `rfl` after unfolding.

**Lean 4 candidate signature:**
```lean4
lemma eval_def (t : T) [Decidable (GBP t)] [Decidable (BD t)] [Decidable (OC t)] :
    eval t = if (GBP t ∧ BD t ∧ OC t) then Verdict.ALLOW else Verdict.DENY := by
  rfl  -- candidate; depends on definitional equality of eval
```

---

#### Lemma L2 — Forward Direction of `allow_iff`

**Informal statement:** If `eval t = ALLOW`, then `GBP t ∧ BD t ∧ OC t`.

**Role:** The necessary condition. Given the evaluation result, extract the propositional witnesses.

**Proof sketch:** Unfold `eval` via L1. The `if`-expression equals ALLOW only when the condition holds (by `if_pos`/`if_neg` and injectivity of constructors). Conclude the conjunction.

**Lean 4 candidate signature:**
```lean4
lemma allow_implies_conj (t : T)
    [Decidable (GBP t)] [Decidable (BD t)] [Decidable (OC t)]
    (h : eval t = Verdict.ALLOW) :
    GBP t ∧ BD t ∧ OC t := by
  rw [eval_def] at h
  split_ifs at h with hc
  · exact hc
  · exact absurd h (by decide)  -- ALLOW ≠ DENY; candidate tactic
```

---

#### Lemma L3 — Backward Direction of `allow_iff`

**Informal statement:** If `GBP t ∧ BD t ∧ OC t`, then `eval t = ALLOW`.

**Role:** The sufficient condition. Given the propositional witnesses, produce the evaluation result.

**Proof sketch:** Unfold `eval` via L1. Apply `if_pos` with the conjunction hypothesis. Conclude by `rfl`.

**Lean 4 candidate signature:**
```lean4
lemma conj_implies_allow (t : T)
    [Decidable (GBP t)] [Decidable