S3: Proof strategy and lemma decomposition.

---

## 1. Stage Identity Record

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S3 — Proof strategy and lemma decomposition
**Prior admitted state:**
- [S0:sha256:80ebda8b5eb0b669896c574235ef8f6706086fea7940b29ccf7e1a0654be5b7c]
- [S1:sha256:538fbecfa3d47990f5fa63d8ca5131a001e5bd872357c41251bc7d1258f0cb96]
- [S2:sha256:c957cef643aede95fde2bb13c6ffa22ca9f90318fc87d355bcc13f28dbc8e2de]

---

## 2. Admitted Prior State (Carried Forward Unchanged)

**Stipulations (admitted, not subject to proof within this task):**

- **S1.** There exists a type `T` of candidate transitions.
- **S2.** `GBP`, `BD`, and `OC` are total predicates of type `T → Prop`.
- **S3.** There exists a function `eval : T → Decision` where `Decision` has at least the value `ALLOW`.
- **S4.** The evaluator's behavior is defined by: `eval(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`.

**Definitions admitted at S1:** D1–D7.

**Theorems formulated at S2:**

| Label | Content | Status entering S3 |
|-------|---------|-------------------|
| T1 | `∀ t : T, eval(t) = ALLOW ↔ (GBP(t) ∧ BD(t) ∧ OC(t))` | Pending formal proof |
| T2 | `∀ t : T, eval(t) = ALLOW → (GBP(t) ∧ BD(t) ∧ OC(t))` | Pending formal proof |
| T3 | `∀ t : T, (GBP(t) ∧ BD(t) ∧ OC(t)) → eval(t) = ALLOW` | Pending formal proof |
| Lean 4 candidate type-checks | Unresolved implementation evidence |
| Deployed system conforms | Not claimed — outside task boundary |

---

## 3. Proof Strategy Selection

### 3.1 Strategic Observation

The logical core of this task is unusually direct. Stipulation S4 asserts the biconditional T1 universally and without qualification. There is therefore no gap between the axiom and the principal theorem: T1 is S4 restated with an explicit universal quantifier and explicit claim boundary.

The proof strategy must nonetheless be made explicit for two reasons:

1. **Lean 4 encoding discipline.** The Lean 4 candidate (to be produced at S4) requires a term-level or tactic-level proof. The strategy determines which proof terms or tactics are appropriate.
2. **Lemma decomposition discipline.** T2 and T3 are the two directed halves of T1. Decomposing them as named lemmas makes the biconditional structure auditable and allows each direction to be cited independently.

### 3.2 Chosen Strategy: Direct Application of S4

**Strategy name:** Axiom-direct.

**Description:** For each of T1, T2, T3, the proof proceeds by:

1. Introducing an arbitrary `t : T` via universal introduction.
2. Invoking S4 (the behavioral axiom for `eval`) to obtain the biconditional instance at `t`.
3. Applying the appropriate direction of the biconditional (both directions for T1; forward direction for T2; backward direction for T3).

No intermediate lemmas beyond T2 and T3 themselves are required. No case analysis, induction, or auxiliary constructions are needed.

**Justification for strategy choice:** The problem is logically atomic under the given stipulations. Any more complex strategy (e.g., proof by contradiction, induction on `T`) would introduce unnecessary structure and risk obscuring the claim boundary. The axiom-direct strategy is the minimal sound strategy.

### 3.3 Alternative Strategies Considered and Rejected

| Alternative | Reason for rejection |
|-------------|---------------------|
| Proof by contradiction | Unnecessary; the biconditional is directly available from S4. Would add proof length without logical gain. |
| Induction on `T` | `T` is an arbitrary type with no inductive structure assumed (D1). Induction is not available. |
| Proof via decision procedure | `Decision` has no assumed decidability structure. Not applicable. |
| Proof by constructing a model | The task is purely logical under stipulations; model construction is not required and would conflate the abstract claim with an implementation claim. |

---

## 4. Lemma Decomposition

### 4.1 Decomposition Rationale

T1 is a biconditional. In Lean 4, a biconditional `P ↔ Q` is introduced by `Iff.intro` applied to a proof of `P → Q` and a proof of `Q → P`. The natural decomposition is therefore into exactly two directed lemmas, corresponding to T2 and T3. T1 is then assembled from T2 and T3 via `Iff.intro`.

This decomposition is:
- **Complete:** T2 and T3 together are logically equivalent to T1.
- **Non-redundant:** Neither T2 nor T3 is derivable from the other alone