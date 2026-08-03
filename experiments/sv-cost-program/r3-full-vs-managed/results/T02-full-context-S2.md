S2: Theorem formulation

---

## 1. Task Identity Preservation

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S2 — Theorem formulation
**Prior admitted state:** S1:sha256:babafd42c0d3472120d68d79e42a2f530070d9f5199161ce59f2dca757711ac7

---

## 2. Admitted Prior State (Carried Forward Unchanged)

```
ADMITTED FROM S0–S1:
  ST-1  GBP, BD, OC are uninterpreted predicates on a candidate transition t.
  ST-2  E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)  [stipulated evaluator semantics]
  ST-3  The evaluator is abstract; no concrete implementation is referenced.
  ST-4  No deployed GCAT/BCAT system is referenced.

  DEF-1  T : arbitrary carrier type of candidate transitions
  DEF-2  GBP, BD, OC : T → Prop
  DEF-3  Outcome : type with inhabitants ALLOW, DENY
  DEF-4  E : T → Outcome, satisfying ST-2 as defining property
  DEF-5  Admissible(t) :≡ GBP(t) ∧ BD(t) ∧ OC(t)

  ASM-1  Classical propositional logic
  ASM-2  T is non-empty
  ASM-3  GBP, BD, OC are total on T
  ASM-4  E is total on T
  ASM-5  No further axioms in force

  C-IN-1, C-IN-2, C-IN-3   [in-scope, not yet established]
  C-OUT-1 through C-OUT-4   [permanently excluded]

VERIFIED CLAIMS FROM S0–S1: none
```

---

## 3. Theorem Statements

The following theorems are formulated at this stage. They are **generated claims**, not yet verified. Verification status is recorded explicitly in Section 6.

---

### THEOREM 1 (Necessary and Sufficient Characterization of ALLOW-Admissibility)

**Informal statement:**
A candidate transition `t` receives outcome `ALLOW` from the abstract evaluator `E` if and only if all three predicates `GBP`, `BD`, and `OC` hold of `t`.

**Formal statement:**
```
∀ t : T,  E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
```

**Proof sketch (from stipulation):**
This is immediate from DEF-4, which records ST-2 as the defining property of `E`. Both directions are:

- **(Sufficiency — THM1-S):** Assume `GBP(t) ∧ BD(t) ∧ OC(t)`. By DEF-4 (right-to-left direction of the biconditional), `E(t) = ALLOW`.
- **(Necessity — THM1-N):** Assume `E(t) = ALLOW`. By DEF-4 (left-to-right direction of the biconditional), `GBP(t) ∧ BD(t) ∧ OC(t)`.

**Status:** Generated claim. Proof is by direct unfolding of the stipulated definition. No non-trivial logical step is required beyond the biconditional introduction and elimination rules of classical propositional logic under ASM-1.

---

### THEOREM 2 (Admissibility Predicate Coincidence)

**Informal statement:**
The admissibility predicate `Admissible` as defined in DEF-5 coincides exactly with the evaluator returning `ALLOW`.

**Formal statement:**
```
∀ t : T,  Admissible(t)  ↔  E(t) = ALLOW
```

**Proof sketch:**
By DEF-5, `Admissible(t) :≡ GBP(t) ∧ BD(t) ∧ OC(t)`. By THEOREM 1, `E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`. The result follows by transitivity of the biconditional.

**Status:** Generated claim. Follows from THEOREM 1 and DEF-5 by biconditional transitivity.

---

### THEOREM 3 (Failure Mode Decomposition)

**Informal statement:**
The evaluator does not return `ALLOW` if and only if at least one of `GBP`, `BD`, `OC` fails to hold.

**Formal statement:**
```
∀ t : T,  E(t) ≠ ALLOW  ↔  ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)
```

**Proof sketch:**
By THEOREM 1, `E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`. Negating both sides:
```
¬(E(t) = ALLOW)  ↔  ¬(GBP(t) ∧ BD(t) ∧ OC(t))
```
By De Morgan's law (valid under ASM-1):
```
¬(GBP(