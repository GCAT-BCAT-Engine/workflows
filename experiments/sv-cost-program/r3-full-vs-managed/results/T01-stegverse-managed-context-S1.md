S1: Definitions and assumptions

---

## Stage Identity

**Stage:** S1 — Definitions and assumptions
**Task:** SV-MATH-001-STAGED
**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Context mode:** managed
**Admitted prior stage:** S0 (sha256:345e03333781a3f599183ec53b1629d03fc9c26831800779aed2fd69c8735488)

---

## 1. Governance Reminders (Preserved from S0)

- All results in this task series concern the **abstract evaluator** defined by stipulation only.
- No claim is made or will be made that any deployed GCAT/BCAT system conforms to this abstract specification.
- Conformance of any deployed system is an independent empirical question, explicitly outside scope.
- Stipulations, generated claims, verified claims, and unresolved implementation evidence remain separated throughout.

---

## 2. Stipulations (This Stage)

The following are **definitional stipulations**. They are axiomatic inputs, not claims about any deployed system.

### 2.1 Universe of Discourse

Let **T** be an arbitrary nonempty type of *candidate transitions*. No further structure is assumed on T at this stage.

### 2.2 Predicate Stipulations

Three predicates are stipulated on T:

| Name | Type | Informal gloss |
|------|------|----------------|
| **GBP** | T → Prop | "Good Behavior Predicate" holds of a candidate transition |
| **BD** | T → Prop | "Boundary Disposition" holds of a candidate transition |
| **OC** | T → Prop | "Operational Condition" holds of a candidate transition |

These are treated as **opaque propositional predicates**. No internal structure, decidability, or computational content is assumed at this stage.

### 2.3 Evaluator Stipulation

An abstract evaluator **E** is stipulated as a function:

```
E : T → {ALLOW, DENY}
```

with the following **defining rule** (the sole axiom governing E):

> **Axiom E-DEF:**
> For all `t : T`,
> `E(t) = ALLOW` **if and only if** `GBP(t) ∧ BD(t) ∧ OC(t)`.

This axiom is the complete specification of E. No other behavior of E is stipulated.

### 2.4 Derived Consequence (Immediate, Not Yet a Verified Claim)

By contraposition of Axiom E-DEF, it follows immediately (within the abstract model) that:

> `E(t) = DENY` if and only if `¬(GBP(t) ∧ BD(t) ∧ OC(t))`,
> i.e., `¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)`.

This is recorded as a **generated consequence**, not yet a separately verified claim. It will be addressed in a later stage.

---

## 3. Assumptions Admitted at This Stage

| ID | Assumption | Status |
|----|-----------|--------|
| A1 | T is a nonempty type | Stipulated |
| A2 | GBP, BD, OC are predicates T → Prop | Stipulated |
| A3 | E is defined exactly by Axiom E-DEF | Stipulated |
| A4 | Classical logic (excluded middle) is available | Admitted for use in formal development; will be explicit in Lean artifact |
| A5 | No decidability of GBP, BD, OC is assumed | Stipulated absence |

**A4 note:** Classical logic is admitted because the necessary-and-sufficient characterization and its contrapositive are most naturally stated classically. If a constructive treatment is later required, this assumption will be revisited and flagged.

---

## 4. What Is Not Assumed

- No relationship among GBP, BD, OC is assumed (they may overlap, be independent, or be contradictory on some inputs).
- No cardinality of T is assumed beyond nonemptiness.
- No computational realizability of E is assumed.
- No deployed system is assumed to instantiate any of the above.

---

## 5. Lean 4 Candidate — Definitions Only

The following is a **Lean 4 candidate artifact** for the definitional layer. It is presented as a candidate for the logical core. **Implementation validity is not claimed.**

```lean4
-- SV-MATH-001-STAGED | Stage S1: Definitions and assumptions
-- Candidate artifact. Not claimed to be a verified Lean 4 build.
-- Classical logic admitted via import.

import Mathlib.Logic.Basic

-- Universe of candidate transitions (opaque type)
variable {T : Type*} [Nonempty T]

-- Predicate stipulations (opaque)
variable (GBP : T → Prop)
variable (BD  : T → Prop)
variable (OC  : T → Prop)

-- Evaluator outcome type
inductive Outcome : Type where
  | ALLOW : Outcome
  | DENY  : Outcome
deriving DecidableEq, Repr

-- Abstract evaluator, defined by Axiom E-DEF
-- (noncomputable: predicates are Props, not decidable by assumption)
noncomputable def E (GBP : T → Prop) (BD : T → Prop) (OC : T → Prop)
    (t : T) : Outcome :=
  if GBP t ∧ BD t ∧ OC t then Outcome.ALLOW else Outcome.DENY

-- Axiom E-DEF stated as a definitional lemma (to