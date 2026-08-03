S0: Task parsing and claim boundary.

---

## Artifact: S0 — Task Parsing and Claim Boundary

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S0

---

### 1. Task Parsing

**Given (stipulated, not derived):**

- An abstract evaluator is defined. It is not identified with any deployed GCAT/BCAT system.
- Three predicates are stipulated over a candidate transition `t`:
  - `GBP(t)` — "Good Behavior Predicate"
  - `BD(t)` — "Boundary Disposition"
  - `OC(t)` — "Operational Condition"
- The evaluator's output behavior is stipulated as:

> The evaluator returns `ALLOW` on input `t` **exactly when** `GBP(t)` and `BD(t)` and `OC(t)` all hold.

This stipulation is the **sole definitional source** for the evaluator's semantics. No other behavior is stipulated.

---

### 2. Claim Boundary

The following distinctions are enforced throughout all subsequent stages:

| Category | Status |
|---|---|
| The stipulated conjunction rule | **Admitted stipulation** — not a derived claim |
| The necessary-and-sufficient characterization to be produced | **Generated claim** — derived from the stipulation by logical analysis |
| Lean 4 candidate for the logical core | **Candidate artifact** — not verified by a running proof checker at this stage |
| Conformance of any deployed GCAT/BCAT system to this model | **Not claimed** — explicitly out of scope |
| Implementation validity of any Lean 4 candidate | **Not claimed** |

---

### 3. Scope of the Mathematical Task

The task requires, in subsequent stages:

1. **(S1)** State the necessary-and-sufficient (iff) characterization of `ALLOW` admissibility formally.
2. **(S2)** Establish the claim boundary for that characterization (what it does and does not assert).
3. **(S3)** Produce a Lean 4 candidate encoding the logical core.

At **S0**, no characterization is generated and no Lean 4 code is produced. Those are reserved for their designated stages.

---

### 4. Admitted Prior State

**None.** This is the initial stage. No prior artifacts are admitted.

---

### 5. Stage Integrity Note

This artifact is self-contained for S0. It records what has been parsed, what has been stipulated, and what the claim boundaries are. It does not anticipate, derive, or assert any content belonging to S1 or later.

---

*End of S0 artifact.*