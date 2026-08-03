S3: Proof strategy and lemma decomposition

---

## 1. Task Identity Preservation

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S3 — Proof strategy and lemma decomposition
**Prior admitted state:** S2:sha256:f911fa0dc49be87da8f61e6d2639fdfd6a99677d691de8e22c9105ac4276f9ed

---

## 2. Admitted Prior State (Carried Forward Unchanged)

```
ADMITTED FROM S0–S2:
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

  THEOREM 1  ∀ t : T,  E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
             [generated claim; proof by unfolding DEF-4/ST-2]
  THEOREM 2  ∀ t : T,  Admissible(t)  ↔  E(t) = ALLOW
             [generated claim; follows from THM1 and DEF-5]
  THEOREM 3  ∀ t : T,  E(t) ≠ ALLOW  ↔  ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)
             [generated claim; follows from THM1 and De Morgan under ASM-1]

  C-IN-1, C-IN-2, C-IN-3   [in-scope, not yet established]
  C-OUT-1 through C-OUT-4   [permanently excluded]

VERIFIED CLAIMS FROM S0–S2: none
```

---

## 3. Proof Strategy Overview

### 3.1 Structural observation

All three theorems from S2 reduce to a single logical core: the biconditional stipulated in ST-2 / DEF-4. The proof architecture is therefore **definitional unfolding followed by propositional manipulation**. No induction, no case analysis over `T`, and no axioms beyond ASM-1 through ASM-5 are required.

The strategy is organized in three layers:

```
Layer 0 (Atomic):   Biconditional introduction and elimination rules
Layer 1 (Core):     THM1 — direct unfolding of DEF-4
Layer 2 (Derived):  THM2 — biconditional transitivity from THM1 + DEF-5
                    THM3 — negation + De Morgan from THM1
```

Each layer depends only on the layer below it. This dependency structure is acyclic and shallow.

---

### 3.2 Proof method selection

| Theorem | Method | Justification |
|---|---|---|
| THM1 | Definitional unfolding | DEF-4 *is* the biconditional; both directions are immediate |
| THM2 | Biconditional transitivity | DEF-5 defines Admissible as the RHS of THM1 |
| THM3 | Contrapositive + De Morgan | Negation of THM1 LHS and RHS; De Morgan valid under ASM-1 |

No proof by contradiction is required. No appeal to excluded middle beyond what De Morgan requires under classical logic (ASM-1).

---

## 4. Lemma Decomposition

The following lemmas are introduced to make the proof structure explicit and to isolate each logical step. Each lemma is a **generated claim** at this stage; none are yet verified.

---

### LEMMA 1 (Biconditional Right-to-Left — Sufficiency Direction)

**Label:** L1-SUFF

**Statement:**
```
∀ t : T,  GBP(t) ∧ BD(t) ∧ OC(t)  →  E(t) = ALLOW
```

**Proof strategy:**
Fix arbitrary `t : T`. Assume `h : GBP(t) ∧ BD(t) ∧ OC(t)`. Apply the right-to-left direction of DEF-4 (which records ST-2) to `h`. Conclude `E(t) = ALLOW`.

**Logical rule used:** Biconditional elimination (modus ponens on `↔`, right-to-left direction).

**Dependencies:** DEF-4, ST-2.

**Status:** Generated claim. Proof is a single rule application.

---

### LEMMA 