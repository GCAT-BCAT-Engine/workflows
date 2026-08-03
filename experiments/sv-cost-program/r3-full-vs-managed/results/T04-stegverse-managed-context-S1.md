S1: Definitions and assumptions.

---

## Artifact Type
Definitions and assumptions for the abstract GCAT/BCAT evaluator model.

---

## 1. Admitted Prior State (Preserved)

From S0 (sha256:b44121bb1cdd65ee8dd01278fe146d2e95fd3ace2868a16a4712f69ddd18dbdb):

- **Stipulated rule:** The evaluator returns ALLOW exactly when GBP ∧ BD ∧ OC all hold.
- **Claim boundary declared:** No claim is made that any deployed GCAT or BCAT implementation conforms to this characterization.
- **Unresolved:** Deployed implementation binding remains unresolved.

---

## 2. Primitive Sorts and Domains

**Definition S1.1 — Candidate Transition.**
Let `T` be an abstract type representing a *candidate transition*. The internal structure of `T` is unspecified at this stage; it is treated as an opaque parameter.

**Definition S1.2 — Evaluator.**
An *evaluator* `E` is a function of type `T → {ALLOW, DENY}`. The evaluator under analysis is the abstract GCAT/BCAT evaluator; no claim is made about any deployed instance.

---

## 3. Predicate Stipulations

The following three predicates are stipulated. Each is a total function from candidate transitions to `Prop` (in the logical model) or `Bool` (in a computational model). At this stage they are treated as uninterpreted — their internal definitions are not assumed.

**Stipulation S1.A — GBP.**
`GBP : T → Prop`
*Good-standing / Base-Pass predicate.* Holds of a candidate transition `t` when the base-pass condition is satisfied. Content is stipulated, not derived.

**Stipulation S1.B — BD.**
`BD : T → Prop`
*Boundary / Domain predicate.* Holds of a candidate transition `t` when the domain-boundary condition is satisfied. Content is stipulated, not derived.

**Stipulation S1.C — OC.**
`OC : T → Prop`
*Operational-Constraint predicate.* Holds of a candidate transition `t` when the operational-constraint condition is satisfied. Content is stipulated, not derived.

> **Governance note:** GBP, BD, and OC are names assigned for this task. No claim is made that these names or their interpretations correspond to any specific field in a deployed GCAT/BCAT system.

---

## 4. Evaluator Output Stipulation

**Stipulation S1.D — ALLOW/DENY codomain.**
The evaluator output set is `{ALLOW, DENY}`, treated as a two-element type. In the Lean model this will be represented as `Bool` or an inductive type; the choice is deferred to S2.

**Stipulation S1.E — Evaluator rule (restated from S0 for self-containment).**
For all candidate transitions `t : T`:

```
E(t) = ALLOW   iff   GBP(t) ∧ BD(t) ∧ OC(t)
```

This is the *sole* stipulated rule governing `E`. No additional conditions are assumed.

---

## 5. Logical Framework Assumptions

**Assumption S1.F — Classical propositional logic.**
The characterization is developed in classical propositional logic. In particular, the law of excluded middle is assumed for each predicate: for any `t`, each of `GBP(t)`, `BD(t)`, `OC(t)` is either true or false.

**Assumption S1.G — Totality.**
`E` is total: it returns exactly one of `{ALLOW, DENY}` for every `t : T`. There are no undefined, error, or partial outputs in the abstract model.

**Assumption S1.H — Independence of predicates.**
No logical dependency among GBP, BD, OC is assumed. All eight truth-value combinations are considered possible in principle. Dependencies, if any, belong to a deployed implementation and are outside the claim boundary.

**Assumption S1.I — No side effects.**
The evaluator is modeled as a pure function. State, sequencing, and side effects are outside scope.

---

## 6. Derived Immediate Consequence (Stipulation-Entailed, Not Yet a Verified Claim)

From Stipulations S1.D and S1.E, by contrapositive:

```
E(t) = DENY   iff   ¬(GBP(t) ∧ BD(t) ∧ OC(t))
               iff   ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)
```

This is a logical consequence of the stipulation, not an independent claim. It is recorded here for completeness and will be used in S2.

---

## 7. Claim Boundary (Preserved and Extended)

| Category | Content |
|---|---|
| **Stipulations** | S1.A–S1.E: predicate and evaluator rule definitions |
| **Assumptions** | S1.F–S1.I: logical framework, totality, independence, purity |
| **Generated claims** | None yet; characterization theorem deferred to S2 |
| **Verified claims** | None yet |
| **Unresolved implementation evidence** | Deployed implementation binding remains unresolved; no conformance claimed |

---

## 8. Lean 4 Skeleton (Definitions Only — No Proofs Claimed)

The following is a candidate Lean 4 fragment encoding the definitions above. It is a **logical skeleton only**. No claim is made that it compiles, that proofs are complete, or that