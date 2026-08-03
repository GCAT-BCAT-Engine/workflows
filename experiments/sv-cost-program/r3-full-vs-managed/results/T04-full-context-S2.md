S2: Theorem formulation.

---

## 1. Stage Identity Record

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S2 — Theorem formulation
**Prior admitted state:**
- [S0:sha256:80ebda8b5eb0b669896c574235ef8f6706086fea7940b29ccf7e1a0654be5b7c]
- [S1:sha256:538fbecfa3d47990f5fa63d8ca5131a001e5bd872357c41251bc7d1258f0cb96]

---

## 2. Admitted Prior State (Carried Forward Unchanged)

**Stipulations (admitted, not subject to proof within this task):**

- **S1.** There exists a type `T` of candidate transitions.
- **S2.** `GBP`, `BD`, and `OC` are total predicates of type `T → Prop`.
- **S3.** There exists a function `eval : T → Decision` where `Decision` has at least the value `ALLOW`.
- **S4.** The evaluator's behavior is defined by: `eval(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`.

**Definitions admitted at S1:** D1–D7 (candidate transition type, predicates GBP/BD/OC, Decision type, evaluator, ALLOW admissibility).

**Claims status entering S2:**

| Claim | Status entering S2 |
|-------|-------------------|
| C1 (biconditional characterization) | Pending |
| C2 (necessity direction) | Pending |
| C3 (sufficiency direction) | Pending |
| Lean 4 candidate type-checks | Unresolved implementation evidence |
| Deployed system conforms | Not claimed — outside task boundary |

---

## 3. Theorem Formulation

### 3.1 Principal Theorem (C1 — Necessary-and-Sufficient Characterization)

**Theorem T1 (ALLOW Admissibility Characterization).**

*Under stipulations S1–S4 and definitions D1–D7:*

> For every candidate transition `t : T`,
> `eval(t) = ALLOW` if and only if `GBP(t)` holds and `BD(t)` holds and `OC(t)` holds.

Formally:

```
∀ t : T,  eval(t) = ALLOW  ↔  (GBP(t) ∧ BD(t) ∧ OC(t))
```

**Proof sketch (from stipulation S4 directly):**
S4 asserts exactly this biconditional universally. T1 is therefore an immediate consequence of S4 — it requires no additional lemmas. The formal proof consists of introducing an arbitrary `t` and applying S4.

*Remark:* T1 is not a discovery; it is a restatement of S4 in theorem form, making the claim boundary explicit and preparing it for formal encoding. The value of the formulation lies in separating the stipulated axiom from the derived claim and in making the universal quantifier and biconditional structure explicit for the Lean 4 candidate.

---

### 3.2 Necessity Direction (C2)

**Theorem T2 (Necessity).**

*Under stipulations S1–S4 and definitions D1–D7:*

> For every candidate transition `t : T`,
> if `eval(t) = ALLOW`, then `GBP(t)` holds and `BD(t)` holds and `OC(t)` holds.

Formally:

```
∀ t : T,  eval(t) = ALLOW  →  (GBP(t) ∧ BD(t) ∧ OC(t))
```

**Proof sketch:**
Fix arbitrary `t`. Assume `eval(t) = ALLOW`. By S4, `eval(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`. Apply the forward direction (mp) of S4 to the assumption. Conclude `GBP(t) ∧ BD(t) ∧ OC(t)`. ∎

**Dependency:** S4 (forward direction only).

---

### 3.3 Sufficiency Direction (C3)

**Theorem T3 (Sufficiency).**

*Under stipulations S1–S4 and definitions D1–D7:*

> For every candidate transition `t : T`,
> if `GBP(t)` holds and `BD(t)` holds and `OC(t)` holds, then `eval(t) = ALLOW`.

Formally:

```
∀ t : T,  (GBP(t) ∧ BD(t) ∧ OC(t))  →  eval(t) = ALLOW
```

**Proof sketch:**
Fix arbitrary `t`. Assume `GBP(t) ∧ BD(t) ∧ OC(t)`. By S4, `eval(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`. Apply the backward direction (mpr) of S4 to the assumption. Conclude `eval(t) = ALLOW`. ∎

**Dependency:** S4 (backward direction only).

---

### 3.4 Relationship Among T1, T2, T3

T1 is logically equivalent to the conjunction of T2 and T3. Specifically