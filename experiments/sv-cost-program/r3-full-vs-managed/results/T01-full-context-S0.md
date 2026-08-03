# S0: Task parsing and claim boundary

---

## 1. Task Identity Record

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S0 — Task parsing and claim boundary
**Prior admitted state:** None

---

## 2. Stipulated Definitions (Given, Not Generated)

The following are stipulations accepted as task input. They are not claims under verification.

| Symbol | Status | Meaning |
|--------|--------|---------|
| `GBP` | Stipulated predicate | Holds or does not hold of a candidate transition |
| `BD` | Stipulated predicate | Holds or does not hold of a candidate transition |
| `OC` | Stipulated predicate | Holds or does not hold of a candidate transition |
| `ALLOW` | Stipulated output | The evaluator's affirmative decision on a candidate transition |
| Evaluator rule | Stipulated | `ALLOW` is returned **exactly when** `GBP ∧ BD ∧ OC` |

The phrase "exactly when" is parsed as **material biconditional**: the evaluator returns `ALLOW` if and only if all three predicates hold.

---

## 3. Claim Boundary — What This Task Does and Does Not Assert

### 3.1 Claims that WILL be generated in subsequent stages

> **Target claim (to be formally stated in S1):**
> For any candidate transition `t`, the evaluator returns `ALLOW(t)` if and only if `GBP(t) ∧ BD(t) ∧ OC(t)`.

This is a **purely logical/mathematical claim** about the abstract evaluator as stipulated.

### 3.2 Claims that are EXPLICITLY OUT OF SCOPE and will NOT be made

- That any deployed GCAT or BCAT system implements this rule.
- That any deployed GCAT or BCAT system conforms to the abstract evaluator.
- That the predicates `GBP`, `BD`, `OC` correspond to any specific real-world checks in any implementation.
- That a Lean 4 proof artifact, once produced, validates any deployed system.
- That artifact hashes prove semantic correctness of any implementation.

### 3.3 Separation of artifact types

| Artifact type | Will be labeled |
|---------------|----------------|
| Stipulations (task input) | `[STIPULATED]` |
| Generated logical claims | `[GENERATED — UNVERIFIED]` until formally proved |
| Formally proved claims | `[VERIFIED — within formal system]` |
| Implementation conformance claims | `[PROHIBITED in this task]` |

---

## 4. Parsing Resolution

The task phrase **"ALLOW admissibility"** is parsed as: the condition under which the evaluator is permitted to (i.e., does) return `ALLOW`. This is fully determined by the stipulated rule and requires no additional interpretation.

The task phrase **"necessary-and-sufficient characterization"** is parsed as: a biconditional statement of the form `ALLOW(t) ↔ P(t)` where `P(t)` is the simplest predicate expression equivalent to the evaluator rule. Given the stipulation, `P(t) ≡ GBP(t) ∧ BD(t) ∧ OC(t)`.

---

## 5. Stage S0 Output Summary

- Task identity: **preserved**.
- Stipulations: **recorded, not generated**.
- Claim boundary: **established**.
- No logical claims generated yet (deferred to S1).
- No implementation validity claimed.
- No stages skipped.

**S0 is complete. Ready to proceed to S1 upon instruction.**

---

*Artifact identity: SV-MATH-001-STAGED / S0 / no prior state / boundary-only*