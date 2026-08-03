S0: Task parsing and claim boundary.

---

## ARTIFACT: S0-PARSE-001

**Stage:** S0 — Task parsing and claim boundary
**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED

---

### 1. Task Decomposition

The task presents an **abstract evaluator** with the following stipulated structure:

- **Domain:** A set of candidate transitions (unspecified; treated as an abstract type `T`).
- **Predicates:** Three unary predicates on `T`:
  - `GBP : T → Prop` (Good Behavior Predicate)
  - `BD : T → Prop` (Boundary/Domain predicate)
  - `OC : T → Prop` (Other Condition predicate)
- **Evaluator output:** The evaluator returns `ALLOW` for a candidate transition `t` **exactly when** `GBP t ∧ BD t ∧ OC t`.

The task requests:
1. A **necessary-and-sufficient characterization** of ALLOW admissibility.
2. A **claim boundary** statement.
3. A **Lean 4 candidate** for the logical core (to be produced in a later stage).

---

### 2. Necessary-and-Sufficient Characterization (Stipulated)

**Definition (ALLOW admissibility):**
For a candidate transition `t : T`, the evaluator admits `t` (returns ALLOW) if and only if all three predicates hold simultaneously.

Formally:

```
ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)
```

This is a **biconditional by stipulation** — it is the defining rule of the abstract evaluator, not a derived theorem. Both directions follow directly:

- **(→) Necessity:** If `ALLOW(t)`, then `GBP(t)`, `BD(t)`, and `OC(t)` each hold. No single predicate is sufficient alone; all three are individually necessary.
- **(←) Sufficiency:** If `GBP(t)`, `BD(t)`, and `OC(t)` all hold, then `ALLOW(t)`. The conjunction is jointly sufficient.

---

### 3. Claim Boundary

The following distinctions are **admitted and binding** for all subsequent stages:

| Category | Content |
|---|---|
| **Stipulated (not proved)** | The biconditional `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)` is given as the definition of the abstract evaluator. It is not derived from any deeper axioms here. |
| **Generated claim (to be formalized)** | The logical core — that the biconditional holds as a Lean 4 proposition under these stipulations — is a candidate for formal statement in S1. |
| **Verified claim** | None yet. No Lean 4 artifact has been checked. |
| **Explicitly excluded** | No claim is made that any deployed GCAT/BCAT implementation satisfies these predicates. No claim is made about the semantic content of GBP, BD, or OC beyond their role as abstract propositions. |
| **Unresolved implementation evidence** | Whether any concrete system instantiates this evaluator correctly is outside scope and unresolved. |

---

### 4. Scope of Subsequent Stages

- **S1** will produce the Lean 4 candidate encoding the logical core.
- **S2** (if staged) will address proof structure.
- No stage will claim deployed implementation validity.

---

### 5. Artifact Identity

```
ARTIFACT_ID: S0-PARSE-001
STAGE: S0
HASH-NOTE: This hash covers artifact identity only, not semantic content.
SHA256-PLACEHOLDER: [to be assigned by ledger at artifact registration]
```

---

**ARTIFACT_LEDGER (updated):**
```
[S0-PARSE-001 | Stage: S0 | Status: ADMITTED | Verified: NO]
```

**SELECTED_RETRIEVAL:** [none]