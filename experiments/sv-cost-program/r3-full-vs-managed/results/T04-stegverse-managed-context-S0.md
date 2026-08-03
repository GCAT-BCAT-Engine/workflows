S0: Task parsing and claim boundary.

---

## ARTIFACT: S0-PARSE-001

**Artifact type:** Task parse and claim boundary declaration
**Stage:** S0
**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED

---

### 1. Task Parsing

**Subject domain:** Abstract evaluator semantics.

**Named entities (stipulated, not empirically sourced):**

| Identifier | Role |
|---|---|
| `GCAT/BCAT evaluator` | Abstract evaluator; behavior is fully stipulated by the problem statement |
| `GBP` | Predicate on a candidate transition (stipulated) |
| `BD` | Predicate on a candidate transition (stipulated) |
| `OC` | Predicate on a candidate transition (stipulated) |
| `ALLOW` | Output verdict of the evaluator (stipulated) |
| `candidate transition` | The object over which GBP, BD, OC, and ALLOW are defined |

**Stipulated operational rule (verbatim extraction):**

> "The evaluator returns ALLOW exactly when GBP and BD and OC all hold."

This is the **sole definitional input**. No other behavioral rules are in scope for this task.

---

### 2. Logical Content to Be Characterized

The task requests a **necessary-and-sufficient characterization** of ALLOW admissibility.

From the stipulation, the intended logical content is:

```
ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)
```

where `t` ranges over candidate transitions.

This is a **biconditional** (iff) claim. Both directions are in scope:

- **Sufficiency:** `GBP(t) ∧ BD(t) ∧ OC(t) → ALLOW(t)`
- **Necessity:** `ALLOW(t) → GBP(t) ∧ BD(t) ∧ OC(t)`

---

### 3. Claim Boundary Declaration

The following boundaries are **explicitly admitted** and govern all subsequent stages:

**WITHIN SCOPE (this task):**
- The abstract logical equivalence `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)` as a stipulated definition.
- Formal statement and proof of the biconditional in a propositional/predicate logic setting.
- A Lean 4 candidate encoding the logical core (to be produced in a later stage).

**OUT OF SCOPE / EXPLICITLY DISCLAIMED:**
- No claim is made that any deployed GCAT or BCAT implementation conforms to this characterization.
- No claim is made about the semantic content of GBP, BD, or OC beyond their role as abstract predicates.
- No claim is made about completeness or correctness of any real evaluator system.
- The Lean 4 artifact (when produced) is a **candidate**; implementation validity is not claimed.
- Hash values, if produced, prove artifact identity only, not semantic correctness.

---

### 4. Separation of Stipulations vs. Generated Claims

| Category | Content |
|---|---|
| **Stipulation (given)** | `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)` — sourced directly from problem statement |
| **Generated claim (pending)** | Formal proof of the biconditional — to be produced in S1 |
| **Verified claim** | None yet |
| **Unresolved implementation evidence** | None in scope; deployment conformance explicitly disclaimed |

---

### 5. Updated Artifact Ledger

```
ARTIFACT_LEDGER = [
  {
    id: "S0-PARSE-001",
    stage: "S0",
    type: "Task parse and claim boundary",
    status: "COMPLETE",
    content_summary: "Parsed stipulated rule; declared claim boundary; separated stipulations from generated/verified claims.",
    implementation_validity_claimed: false
  }
]
```

---

**Stage S0 complete. Awaiting instruction to proceed to S1 (formal characterization and proof).**