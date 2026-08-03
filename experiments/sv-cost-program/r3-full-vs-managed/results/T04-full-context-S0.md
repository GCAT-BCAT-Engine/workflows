# S0: Task parsing and claim boundary

---

## 1. Task Identity Record

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S0 — Task parsing and claim boundary
**Prior admitted state:** None

---

## 2. Parsed Problem Statement

The problem introduces an abstract evaluator (referred to as a GCAT/BCAT evaluator) that operates on candidate transitions. Three predicates are stipulated:

| Symbol | Role |
|--------|------|
| `GBP` | Predicate on a candidate transition |
| `BD` | Predicate on a candidate transition |
| `OC` | Predicate on a candidate transition |

The evaluator's output behavior is stipulated as:

> The evaluator returns **ALLOW** on a candidate transition `t` **if and only if** `GBP(t)` and `BD(t)` and `OC(t)` all hold.

---

## 3. Stipulations (Accepted Without Proof)

The following are **stipulations** — they are given as part of the problem definition and are not generated claims subject to verification in this task:

**S1.** There exists a type `T` of candidate transitions.
**S2.** `GBP`, `BD`, and `OC` are total predicates of type `T → Prop`.
**S3.** There exists a function `eval : T → Decision` where `Decision` has at least the value `ALLOW`.
**S4.** The evaluator's behavior is defined by: `eval(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`.

Stipulation S4 is the **definitional rule** — it is the object of formal characterization, not an empirical claim about any deployed system.

---

## 4. Claim Boundary

### 4.1 What this task DOES claim

**Claim C1 (Target — to be established in later stages):**
> For all candidate transitions `t`, the evaluator returns ALLOW on `t` if and only if `GBP(t)` holds and `BD(t)` holds and `OC(t)` holds.

Formally:
```
∀ t : T, eval(t) = ALLOW ↔ (GBP(t) ∧ BD(t) ∧ OC(t))
```

This is a **necessary-and-sufficient characterization** of ALLOW admissibility under the given stipulations.

**Claim C2 (Boundary of necessity — to be established):**
> If `eval(t) = ALLOW`, then `GBP(t)` holds, `BD(t)` holds, and `OC(t)` holds.

**Claim C3 (Boundary of sufficiency — to be established):**
> If `GBP(t)` holds and `BD(t)` holds and `OC(t)` holds, then `eval(t) = ALLOW`.

### 4.2 What this task DOES NOT claim

- **No claim** is made that any deployed GCAT or BCAT implementation conforms to stipulation S4 or to claims C1–C3.
- **No claim** is made about the semantic content of `GBP`, `BD`, or `OC` beyond their types as predicates.
- **No claim** is made that the Lean 4 candidate (to be produced in a later stage) has been compiled, type-checked by a running kernel, or verified by any external tool.
- **No claim** is made about the behavior of the evaluator on inputs where `eval(t) ≠ ALLOW`.

### 4.3 Claim status table

| Claim | Status at S0 |
|-------|-------------|
| C1 (biconditional characterization) | **Pending** — to be established in S1 |
| C2 (necessity direction) | **Pending** |
| C3 (sufficiency direction) | **Pending** |
| Lean 4 candidate type-checks | **Unresolved implementation evidence** — to be noted at artifact production stage |
| Deployed system conforms | **Not claimed** — outside task boundary |

---

## 5. Stage S0 Artifact

**Artifact type:** Task parse and claim boundary record
**Content:** Sections 1–4 above
**Artifact identity note:** This document constitutes the S0 artifact. A hash of this text would prove artifact identity only; it would not prove semantic correctness of any claim herein.

---

## 6. Admitted State After S0

| Item | Status |
|------|--------|
| Stipulations S1–S4 | Admitted |
| Claims C1–C3 | Identified, not yet established |
| Prior admitted state | None (as given) |
| Implementation evidence | None admitted |

---

**S0 complete. Ready to proceed to S1 upon instruction.**