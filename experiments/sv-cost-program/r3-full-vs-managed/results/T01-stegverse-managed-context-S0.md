S0: Task parsing and claim boundary.

---

## ARTIFACT: S0-PARSE-001

**Stage:** S0 — Task parsing and claim boundary
**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED

---

### 1. Task Parsing

**Subject domain:** Abstract evaluator with identifier GCAT/BCAT evaluator.

**Primitive predicates (stipulated, not derived):**
- `GBP` : a predicate on a candidate transition
- `BD` : a predicate on a candidate transition
- `OC` : a predicate on a candidate transition

**Evaluator output rule (stipulated):**
> The evaluator returns `ALLOW` exactly when `GBP` and `BD` and `OC` all hold.

This is a definitional stipulation. It is not a claim about any deployed system. It is the axiomatic input to the task.

**Requested outputs (across all stages):**
1. Necessary-and-sufficient characterization of `ALLOW` admissibility
2. Statement of the claim boundary
3. A Lean 4 candidate for the logical core

**Current stage output:** Items 2 and the structural setup for item 1 (formal parsing only). Item 3 is deferred to a later stage.

---

### 2. Claim Boundary (Established at S0)

The following distinctions are fixed and carried forward into all subsequent stages.

| Category | Content |
|---|---|
| **Stipulation** | The evaluator returns `ALLOW` iff `GBP ∧ BD ∧ OC`. This is given, not proved. |
| **Generated claim (pending)** | The necessary-and-sufficient characterization to be stated formally in S1. |
| **Verified claim** | None yet. No proof has been constructed or checked. |
| **Unresolved implementation evidence** | No claim is made or will be made that any deployed GCAT/BCAT system conforms to this abstract specification. |

**Boundary statement (normative, carried forward):**

> All formal results produced in this task series are results about the *abstract* evaluator defined by the stipulation above. They are not results about any deployed implementation. Conformance of any deployed system to this abstract specification is an independent empirical question and is explicitly outside the scope of this task.

---

### 3. Structural Setup for Necessary-and-Sufficient Characterization

The task asks to characterize `ALLOW` admissibility. Given the stipulation, the characterization has the following logical shape:

```
For any candidate transition t:
  ALLOW(t)  ⟺  GBP(t) ∧ BD(t) ∧ OC(t)
```

**Necessary direction:** If `ALLOW(t)`, then `GBP(t) ∧ BD(t) ∧ OC(t)`.
**Sufficient direction:** If `GBP(t) ∧ BD(t) ∧ OC(t)`, then `ALLOW(t)`.

Both directions follow directly from the stipulation. The formal proof structure and Lean 4 candidate are deferred to S1 and S2 respectively.

---

### 4. Artifact Ledger Update

```
ARTIFACT_LEDGER = [
  {
    id: "S0-PARSE-001",
    stage: "S0",
    type: "parse-and-boundary",
    status: "complete",
    content: "Task parsed; claim boundary established; no proofs constructed",
    hash_note: "Hash proves artifact identity, not semantic content"
  }
]
```

---

**End of S0 artifact. No stages skipped. No implementation validity claimed.**