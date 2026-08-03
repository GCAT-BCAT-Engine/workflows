S4: Complete informal proof.

---

## S4 Artifact: Complete Informal Proof

**Task identity:** SV-MATH-001-STAGED / SV-COST-R3-FULL-VS-MANAGED-001
**Stage:** S4 — Complete informal proof
**Governance:** Stipulations, generated claims, and unresolved implementation evidence are kept separate. No deployed GCAT/BCAT implementation conformance is claimed.

---

### S4.1 — Recapitulation of Admitted State

From the artifact ledger, the following are admitted without re-derivation:

- **S1 (Stipulations):** The abstract evaluator model is fixed. `Transition` is an arbitrary type. `GBP`, `BD`, `OC`, and `ALLOW` are uninterpreted predicates on `Transition`. The sole governing axiom is:

  > **Axiom (allow_ax):** For every transition `t`, `ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)`.

  This axiom is a *stipulation* of the abstract model, not a claim about any deployed system.

- **S2 (Theorem formulation):** The target theorem is:

  > **Theorem (allow_admissibility_iff):** `∀ t : Transition, ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)`.

  With derived lemmas:
  - **L1 (allow_necessity):** `∀ t, ALLOW t → GBP t ∧ BD t ∧ OC t`
  - **L2 (allow_sufficiency):** `∀ t, GBP t ∧ BD t ∧ OC t → ALLOW t`

- **S3 (Proof sketch):** The proof strategy is identified as direct application of the biconditional axiom `allow_ax` in each direction.

- **Unresolved (all stages):** Deployed implementation binding remains unresolved throughout.

---

### S4.2 — Logical Preliminaries

**Setting.** All reasoning takes place in classical propositional logic (or equivalently, in the propositional fragment of first-order logic with one free variable `t`). No arithmetic, set theory, or additional inference rules beyond standard natural deduction for `∧`, `→`, and `↔` are required.

**Definitions in scope.**

| Symbol | Type | Role |
|---|---|---|
| `Transition` | Type | Abstract carrier; elements are candidate transitions |
| `GBP` | `Transition → Prop` | "Good Behavior Predicate" |
| `BD` | `Transition → Prop` | "Boundary" predicate |
| `OC` | `Transition → Prop` | "Operational Condition" predicate |
| `ALLOW` | `Transition → Prop` | Evaluator output predicate |
| `allow_ax` | Axiom | `∀ t, ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)` |

**Claim boundary (restated from S2).** The theorem and its proof are claims about the *abstract model* defined by `allow_ax`. They are not claims about any concrete GCAT/BCAT implementation, any deployed evaluator, or any runtime system. The abstract model is self-contained and the proof is complete within it.

---

### S4.3 — Main Theorem: Complete Informal Proof

**Theorem (allow_admissibility_iff).**
*For every transition `t`, `ALLOW t` holds if and only if `GBP t`, `BD t`, and `OC t` all hold simultaneously.*

Formally: `∀ t : Transition, ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)`.

**Proof.**

Let `t : Transition` be arbitrary. We must establish the biconditional `ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)`.

By `allow_ax`, instantiated at `t`, we have exactly:

> `ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)`

as an axiom of the abstract model. The biconditional is therefore immediate by axiom instantiation. Since `t` was arbitrary, universal generalization yields the theorem. ∎

*Remark.* The proof is trivial at the level of the main theorem because the axiom directly states the biconditional. The non-trivial content lies in the two directed lemmas, which we now prove in full.

---

### S4.4 — Lemma L1: Necessity (Complete Informal Proof)

**Lemma L1 (allow_necessity).**
*For every transition `t`, if `ALLOW t` holds, then `GBP t`, `BD t`, and `OC t` all hold.*

Formally: `∀ t : Transition, ALLOW t → (GBP t ∧ BD t ∧ OC t)`.

**Proof.**

Let `t : Transition` be arbitrary. Assume as hypothesis:

> `h : ALLOW t`

We must derive `GBP t ∧ BD t ∧ OC t`.

**Step 1.** Instantiate `allow_ax` at `t` to obtain:

> `allow_ax t : ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)`

**Step 2.** A biconditional `P ↔ Q` yields, by the elimination rule for `↔`, both `P → Q` (the forward direction, `mp`)