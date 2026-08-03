S1: Definitions and assumptions

---

## 1. Stage Identity Record

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S1 — Definitions and assumptions
**Prior admitted state:** [S0:sha256:80ebda8b5eb0b669896c574235ef8f6706086fea7940b29ccf7e1a0654be5b7c]

---

## 2. Admitted Prior State (Carried Forward Unchanged)

The following items were admitted at S0 and are preserved without modification:

**Stipulations (admitted, not subject to proof within this task):**

- **S1.** There exists a type `T` of candidate transitions.
- **S2.** `GBP`, `BD`, and `OC` are total predicates of type `T → Prop`.
- **S3.** There exists a function `eval : T → Decision` where `Decision` has at least the value `ALLOW`.
- **S4.** The evaluator's behavior is defined by: `eval(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`.

**Claims identified at S0 (status carried forward):**

| Claim | Status entering S1 |
|-------|-------------------|
| C1 (biconditional characterization) | Pending |
| C2 (necessity direction) | Pending |
| C3 (sufficiency direction) | Pending |
| Lean 4 candidate type-checks | Unresolved implementation evidence |
| Deployed system conforms | Not claimed — outside task boundary |

---

## 3. Definitions Introduced at S1

The following definitions are introduced to make the abstract structure precise. They are **definitional stipulations** for the purposes of this task — they do not generate new empirical claims.

---

### 3.1 Type of Candidate Transitions

**Definition D1 (Candidate transition type).**
Let `T` be an arbitrary but fixed type. Elements of `T` are called *candidate transitions*. No further structure is assumed on `T`.

*Remark:* `T` is left abstract. The characterization to be established holds for any instantiation of `T`.

---

### 3.2 Predicates

**Definition D2 (Predicate GBP).**
`GBP : T → Prop` is a total predicate. For any `t : T`, `GBP(t)` is a proposition. No assumption is made about which elements of `T` satisfy `GBP`.

**Definition D3 (Predicate BD).**
`BD : T → Prop` is a total predicate. For any `t : T`, `BD(t)` is a proposition. No assumption is made about which elements of `T` satisfy `BD`.

**Definition D4 (Predicate OC).**
`OC : T → Prop` is a total predicate. For any `t : T`, `OC(t)` is a proposition. No assumption is made about which elements of `T` satisfy `OC`.

*Remark:* The predicates `GBP`, `BD`, `OC` are treated as independent. No logical relationship among them is assumed or introduced here.

---

### 3.3 Decision Type

**Definition D5 (Decision type).**
Let `Decision` be a type with at least the distinguished constructor `ALLOW`. No other structure of `Decision` is assumed for the purposes of this task. In particular, no claim is made about what other values `Decision` may contain.

---

### 3.4 Evaluator Function

**Definition D6 (Evaluator).**
`eval : T → Decision` is a total function. Its behavior is governed exclusively by stipulation S4:

```
∀ t : T,  eval(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
```

*Remark:* S4 is the **sole behavioral axiom** for `eval` within this task. The behavior of `eval` on transitions where the conjunction fails is not characterized here and is not needed for claims C1–C3.

---

### 3.5 ALLOW Admissibility

**Definition D7 (ALLOW admissibility).**
A candidate transition `t : T` is called *ALLOW-admissible* if and only if `eval(t) = ALLOW`.

By S4, this is equivalent to: `GBP(t) ∧ BD(t) ∧ OC(t)`.

*Remark:* D7 does not assert the equivalence as a new claim — it records that S4 directly licenses the equivalence as a matter of definition. The formal establishment of C1–C3 from S4 is deferred to S2.

---

## 4. Assumption Inventory

All assumptions operative in this task are collected here for transparency.

| Label | Content | Source | Status |
|-------|---------|--------|--------|
| S1 | Type `T` exists | Problem stipulation | Admitted |
| S2 | `GBP`, `BD`, `OC` are total predicates `T → Prop` | Problem stipulation | Admitted |
| S3 | `eval : T → Decision`, `ALLOW ∈ Decision` | Problem stipulation | Admitted |
| S4 | `eval(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)` | Problem stipulation | Admitted |
| D1–D7 | Definitional elaborations of S1–S4 | This stage | Admitted as definitions |

**No additional assumptions are introduced.** In particular:

- No assumption is