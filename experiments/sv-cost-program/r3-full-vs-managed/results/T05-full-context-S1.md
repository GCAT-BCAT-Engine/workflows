S1: Definitions and assumptions.

---

## Artifact: S1 — Definitions and Assumptions

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S1

---

### Admitted Prior State

[S0:sha256:88c1f97e1f6599962b876deef766f4c1a9a454be1080a64de3380e78518083f3]

S0 established: task parsing, claim boundary table, and scope of the mathematical task. No characterization was generated at S0. All S0 content is admitted without modification.

---

### 1. Universe of Discourse

**Stipulation S1.1 (Transition type):**
Let `T` be an arbitrary non-empty type. Elements of `T` are called *candidate transitions*. No further structure is imposed on `T`. The choice of `T` is abstract and fixed for the remainder of this task.

---

### 2. Predicate Stipulations

The following three predicates are stipulated. They are not defined in terms of each other or in terms of any other structure. Their extensions over `T` are arbitrary.

**Stipulation S1.2 (GBP):**
`GBP : T → Prop`
For any `t : T`, `GBP(t)` is a proposition. Its truth value is not further constrained by this task.

**Stipulation S1.3 (BD):**
`BD : T → Prop`
For any `t : T`, `BD(t)` is a proposition. Its truth value is not further constrained by this task.

**Stipulation S1.4 (OC):**
`OC : T → Prop`
For any `t : T`, `OC(t)` is a proposition. Its truth value is not further constrained by this task.

---

### 3. Evaluator Output Stipulation

**Stipulation S1.5 (ALLOW semantics):**
The abstract evaluator is a function `Eval : T → {ALLOW, DENY}` (or equivalently, a predicate `ALLOW : T → Prop`) whose behavior is fully determined by the following biconditional, stipulated as the sole definitional source:

> For all `t : T`:
> `ALLOW(t)` holds **if and only if** `GBP(t) ∧ BD(t) ∧ OC(t)`.

This stipulation is **definitional**: it does not require proof and is not subject to derivation. It is the complete specification of the evaluator's semantics within this task.

---

### 4. Logical Status of Each Element

| Element | Type | Status |
|---|---|---|
| `T` | Abstract type | Stipulated; no structure assumed |
| `GBP`, `BD`, `OC` | Predicates `T → Prop` | Stipulated; extensions arbitrary |
| `ALLOW` | Predicate `T → Prop` | Stipulated via biconditional in S1.5 |
| The biconditional in S1.5 | Definitional axiom | Admitted stipulation; not a derived claim |
| Any claim derived from S1.5 | Proposition | Generated claim; subject to proof |
| Lean 4 encoding | Candidate artifact | Reserved for S3; not produced here |
| Deployed GCAT/BCAT conformance | — | Not claimed; out of scope |

---

### 5. Assumptions Explicitly Not Made

The following are **not** assumed and must not be introduced in later stages without explicit re-stipulation:

- **A1.** No ordering, metric, or topology is assumed on `T`.
- **A2.** No independence or dependence relation is assumed among `GBP`, `BD`, `OC`.
- **A3.** No default truth value is assumed for any predicate on any particular `t`.
- **A4.** The evaluator is not assumed to be computable, decidable, or total in any constructive sense beyond what classical propositional logic provides.
- **A5.** No deployed system is assumed to instantiate this abstract evaluator.

---

### 6. What S1 Does Not Produce

Consistent with stage discipline:

- The necessary-and-sufficient characterization is **not stated here**; it is reserved for S2.
- The claim boundary analysis for that characterization is **not produced here**; it is reserved for S2.
- The Lean 4 candidate is **not produced here**; it is reserved for S3.

S1 provides only the definitional substrate on which S2 will operate.

---

### 7. Stage Integrity Note

This artifact is self-contained for S1. It records all stipulations, the universe of discourse, the predicate declarations, the evaluator semantics, and the explicit non-assumptions. It introduces no derived claims and anticipates no content belonging to S2 or later.

---

*End of S1 artifact.*