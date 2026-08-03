# S0: Task parsing and claim boundary

---

## 1. Task Identity Preservation

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S0 — Task parsing and claim boundary
**Prior admitted state:** None

---

## 2. Stipulations (Given, Not Generated)

The following are stipulated by the task statement and are accepted without proof or derivation:

| Label | Stipulation |
|---|---|
| **ST-1** | `GBP`, `BD`, and `OC` are uninterpreted predicates on a candidate transition `t`. |
| **ST-2** | An abstract evaluator `E` returns `ALLOW` on input `t` exactly when `GBP(t) ∧ BD(t) ∧ OC(t)` holds. |
| **ST-3** | The evaluator is abstract (no concrete implementation is referenced or assumed). |
| **ST-4** | The task concerns a GCAT/BCAT evaluator in name only; no deployed system is referenced. |

---

## 3. Claim Boundary

The following distinctions are enforced for all subsequent stages:

### 3.1 Claims that are IN SCOPE for this task

- **C-IN-1:** A purely logical, necessary-and-sufficient characterization of `ALLOW` in terms of `GBP`, `BD`, `OC`, derived from ST-2 alone.
- **C-IN-2:** A Lean 4 candidate encoding the logical core of that characterization.
- **C-IN-3:** Structural properties of the conjunction (e.g., monotonicity, failure modes) derivable from propositional logic.

### 3.2 Claims that are OUT OF SCOPE and will NOT be made

- **C-OUT-1:** That any deployed GCAT or BCAT implementation satisfies or instantiates this characterization.
- **C-OUT-2:** That `GBP`, `BD`, or `OC` have any specific semantic content beyond their stipulated role as predicates.
- **C-OUT-3:** That the Lean 4 candidate compiles, type-checks, or is implementation-valid without independent verification.
- **C-OUT-4:** That this characterization governs any real transition system, financial system, or operational system.

---

## 4. Parsed Problem Statement (Canonical Form)

**Domain:** Abstract transition `t` drawn from an unspecified type `T`.

**Predicates:**
```
GBP : T → Prop
BD  : T → Prop
OC  : T → Prop
```

**Evaluator semantics (stipulated):**
```
E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
```

**Target:** Establish the biconditional above as a necessary-and-sufficient characterization, i.e., show:
- **(Sufficiency)** `GBP(t) ∧ BD(t) ∧ OC(t) → E(t) = ALLOW`
- **(Necessity)** `E(t) = ALLOW → GBP(t) ∧ BD(t) ∧ OC(t)`

Note: Because ST-2 stipulates the biconditional directly, both directions are immediate from the stipulation. The mathematical work in later stages is to make this explicit, state it formally, and encode it in Lean 4.

---

## 5. Stage Deliverable Confirmation

| Item | Status |
|---|---|
| Task identity preserved | ✓ |
| Stipulations separated from generated claims | ✓ |
| Claim boundary stated | ✓ |
| No implementation validity claimed | ✓ |
| No stages skipped | ✓ |
| Prior admitted state recorded | ✓ (none) |

---

## 6. Admitted State After S0

```
ADMITTED:
  ST-1, ST-2, ST-3, ST-4  [stipulations, accepted]
  C-IN-1, C-IN-2, C-IN-3  [in-scope claims, not yet established]
  C-OUT-1 through C-OUT-4  [out-of-scope, permanently excluded]

UNRESOLVED:
  Formal proof of biconditional  [deferred to S1]
  Lean 4 candidate               [deferred to S2]
  Structural properties          [deferred to S1]

VERIFIED CLAIMS: none yet
```

---

*S0 artifact complete. Awaiting instruction to proceed to S1.*