S0: Task parsing and claim boundary.

---

## Artifact: S0 — Task Parsing and Claim Boundary

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S0

---

### 1. Task Parsing

The task presents an **abstract evaluator** with the following stipulated structure:

| Symbol | Role |
|--------|------|
| `GBP` | Predicate on a candidate transition |
| `BD` | Predicate on a candidate transition |
| `OC` | Predicate on a candidate transition |
| `ALLOW` | Output predicate on a candidate transition |

**Stipulated operational rule (given, not derived):**

> The evaluator returns `ALLOW` exactly when `GBP` and `BD` and `OC` all hold.

This is a **definitional stipulation** provided by the task. It is not a claim about any deployed system.

---

### 2. Logical Reading

Let `t` range over candidate transitions. The stipulation asserts:

```
ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))
```

This is a **biconditional** (necessary-and-sufficient characterization):

- **Sufficiency:** `GBP(t) ∧ BD(t) ∧ OC(t) → ALLOW(t)`
- **Necessity:** `ALLOW(t) → GBP(t) ∧ BD(t) ∧ OC(t)`

---

### 3. Claim Boundary

The following distinctions are **admitted and preserved** throughout all subsequent stages:

| Category | Status |
|----------|--------|
| The biconditional `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)` as a **logical claim about the abstract evaluator as stipulated** | **In scope — to be established** |
| Any claim that a deployed GCAT/BCAT implementation satisfies this characterization | **Out of scope — not claimed** |
| Any claim that `GBP`, `BD`, `OC`, or `ALLOW` have specific semantic content beyond the stipulation | **Out of scope — not claimed** |
| The Lean 4 artifact as a **candidate for the logical core** | **In scope — to be prepared in a later stage** |

---

### 4. Unresolved Items Carried Forward

- **S1** will state the formal claim precisely.
- **S2** will establish the claim (proof sketch or formal argument).
- **S3** will prepare the Lean 4 candidate.
- No implementation validity is claimed at any stage.

---

### 5. Admitted Prior State

**None.** This is the initial stage.

---

**Artifact hash (SHA-256 of artifact text, for identity tracking — not a semantic guarantee):**
`[hash to be computed by receiving system over the canonical text of this artifact]`

---

*End of S0 artifact.*