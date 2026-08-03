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
  - `BD : T → Prop` (Boundary/Disposition predicate)
  - `OC : T → Prop` (Operational Condition predicate)
- **Evaluator output:** A binary decision `ALLOW : T → Prop`
- **Stipulated rule:** The evaluator returns `ALLOW` exactly when `GBP`, `BD`, and `OC` all hold.

The task requests:
1. A **necessary-and-sufficient characterization** of `ALLOW` admissibility.
2. A **claim boundary** statement.
3. A **Lean 4 candidate** for the logical core (to be produced in a later stage).

---

### 2. Necessary-and-Sufficient Characterization (Logical Core)

From the stipulation, the characterization is:

> **For any candidate transition `t : T`,**
> `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)`

This is a **definitional biconditional** — it is not derived from deeper axioms; it is the stipulated semantics of the evaluator. Both directions follow immediately:

- **(→) Necessity:** If `ALLOW(t)`, then `GBP(t)`, `BD(t)`, and `OC(t)` each hold. (No condition is redundant; all three are necessary.)
- **(←) Sufficiency:** If `GBP(t)`, `BD(t)`, and `OC(t)` all hold, then `ALLOW(t)`. (The conjunction is sufficient.)

---

### 3. Claim Boundary

The following distinctions are **admitted and enforced**:

| Category | Status |
|---|---|
| The biconditional `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)` as a **stipulated abstract claim** | **Admitted as stipulation** |
| The claim that this characterization is **logically necessary and sufficient** given the stipulation | **Claimable; to be formally verified in S2** |
| Any claim that a **deployed GCAT/BCAT implementation** satisfies this characterization | **Not claimed; outside scope** |
| Any claim that `GBP`, `BD`, `OC` correspond to specific real-world predicates | **Not claimed; abstract only** |
| The Lean 4 candidate as a **verified proof** | **Not yet claimed; candidate status only until checked** |

---

### 4. Unresolved Items (Carried Forward)

- `UNRESOLVED-001`: Lean 4 candidate not yet produced (scheduled for S1 or S2).
- `UNRESOLVED-002`: No mechanically checked proof exists yet; candidate will require verification.
- `UNRESOLVED-003`: The abstract type `T` is unconstrained; no inhabitant is assumed.

---

### 5. Artifact Ledger Update

```
ARTIFACT_LEDGER = [
  { id: "S0-PARSE-001",
    stage: "S0",
    type: "parse-and-boundary",
    status: "complete",
    claims_admitted: ["stipulated biconditional"],
    claims_deferred: ["Lean 4 candidate", "mechanically verified proof"],
    claims_excluded: ["deployed implementation validity"] }
]
```

---

**END OF S0 ARTIFACT**