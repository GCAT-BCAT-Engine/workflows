S1: Definitions and assumptions.

---

## Artifact: S1 — Definitions and Assumptions

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S1

---

### 1. Admitted Prior State

**[S0:sha256:dec7e81f740a2aff62a2d95aa715ac5f8374499cc47b41391d4bc224280859dc]**
S0 established: task parsing, logical reading of the stipulation, and claim boundary. The biconditional `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)` was identified as the central logical claim. No implementation validity was claimed.

---

### 2. Universe of Discourse

**Definition S1.1 (Transition type).**
Let `T` be an arbitrary non-empty type. Elements `t : T` are called **candidate transitions**. No further structure is imposed on `T`. The abstract evaluator is defined over `T`.

*Stipulation boundary:* The choice of `T` is left abstract. No claim is made that `T` corresponds to any concrete transition type in a deployed system.

---

### 3. Primitive Predicates

**Definition S1.2 (GBP).**
`GBP : T → Prop` is a predicate on candidate transitions. Its intended reading within the abstract evaluator is "good behavior predicate." No semantic content beyond this label is stipulated or assumed.

**Definition S1.3 (BD).**
`BD : T → Prop` is a predicate on candidate transitions. Its intended reading is "boundary condition." No semantic content beyond this label is stipulated or assumed.

**Definition S1.4 (OC).**
`OC : T → Prop` is a predicate on candidate transitions. Its intended reading is "output condition." No semantic content beyond this label is stipulated or assumed.

*Independence stipulation:* `GBP`, `BD`, and `OC` are treated as **logically independent** predicates. No entailment relation among them is assumed. In particular:

- `GBP(t)` does not imply `BD(t)` or `OC(t)`, and vice versa, in general.
- Any specific transition `t` may satisfy any subset of the three predicates.

---

### 4. Defined Predicate: ALLOW

**Definition S1.5 (ALLOW — stipulated definition).**
`ALLOW : T → Prop` is defined by the following stipulation, given in the task and admitted as the governing rule of the abstract evaluator:

```
∀ t : T,  ALLOW(t)  :=  GBP(t) ∧ BD(t) ∧ OC(t)
```

This is a **definitional equality**, not a derived theorem. `ALLOW` has no independent meaning beyond this definition within the scope of this task.

*Consequence:* Because `ALLOW` is defined as the conjunction, the biconditional

```
∀ t : T,  ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))
```

holds **by definition** in the abstract model. The work of subsequent stages is to make this explicit, state it as a named claim, and render it in Lean 4.

---

### 5. Logical Framework Assumptions

**Assumption S1.A1 (Classical or constructive logic).**
The logical core is expressible in **intuitionistic propositional logic**. No classical axioms (excluded middle, choice) are required to establish the biconditional, because both directions follow directly from the definition of conjunction and the definitional equality of `ALLOW`. The Lean 4 candidate will not invoke `Classical` namespace axioms.

**Assumption S1.A2 (No additional axioms on T).**
No axioms beyond those of Lean 4's core type theory are assumed about `T`, `GBP`, `BD`, or `OC`. They are introduced as universally quantified variables.

**Assumption S1.A3 (Prop universe).**
All predicates take values in `Prop`. No `Bool`-valued or decision-procedure interpretation is assumed.

---

### 6. Claim Statement (to be established in S2)

**Claim S1.C1 (Necessary-and-sufficient characterization of ALLOW admissibility).**

> For all candidate transitions `t : T`, `ALLOW(t)` holds if and only if `GBP(t)`, `BD(t)`, and `OC(t)` all hold.

Formally:

```
∀ t : T,  ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))
```

- **Sufficiency direction:** `GBP(t) ∧ BD(t) ∧ OC(t) → ALLOW(t)`
- **Necessity direction:** `ALLOW(t) → GBP(t) ∧ BD(t) ∧ OC(t)`

Both directions follow from Definition S1.5 by unfolding. The proof structure will be made explicit in S2.

---

### 7. Claim Boundary (Preserved from S0, Extended)

| Category | Status |
|----------|--------|
| Claim S1.C1 as a logical claim about the abstract evaluator under Definition S1.5 | **In scope — to be established in S2** |
| Any claim that a deployed GCAT/BCAT implementation satisfies Definition S1.5 | **Out of scope — not claimed** |
| Any claim that `GBP`, `BD`, `OC` have semantic