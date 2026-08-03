S4: Complete informal proof

---

## 1. Task Identity Preservation

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S4 — Complete informal proof
**Prior admitted state:** S3:sha256:30d4e0041b38790470798b73bb02288804619b2325144210f796c3a795120e9e

---

## 2. Admitted Prior State (Carried Forward Unchanged)

```
ADMITTED FROM S0–S3:
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
  THEOREM 2  ∀ t : T,  Admissible(t)  ↔  E(t) = ALLOW
  THEOREM 3  ∀ t : T,  E(t) ≠ ALLOW  ↔  ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)

  LEMMA L1-SUFF  ∀ t : T,  GBP(t) ∧ BD(t) ∧ OC(t)  →  E(t) = ALLOW
  LEMMA L2-NEC   ∀ t : T,  E(t) = ALLOW  →  GBP(t) ∧ BD(t) ∧ OC(t)
  LEMMA L3-TRANS ∀ t : T,  Admissible(t)  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
                            [by DEF-5, definitional]
  LEMMA L4-DM    ∀ t : T,  ¬(GBP(t) ∧ BD(t) ∧ OC(t))
                            ↔  ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)
                            [De Morgan under ASM-1]

  C-IN-1, C-IN-2, C-IN-3   [in-scope, not yet established]
  C-OUT-1 through C-OUT-4   [permanently excluded]

VERIFIED CLAIMS FROM S0–S3: none
```

---

## 3. Proof Governance Notes

All proofs below are **informal mathematical proofs**. They are complete in the sense that every logical step is named and every dependency is cited. No step is deferred. The proofs are not claimed to be mechanically verified; that is the province of the Lean 4 candidate (S5, not this stage).

Proof structure follows the layer decomposition established in S3:

```
Layer 0:  Logical rules (biconditional elim/intro, De Morgan, transitivity)
Layer 1:  L1-SUFF, L2-NEC  →  THEOREM 1
Layer 2:  THEOREM 1 + DEF-5  →  THEOREM 2
          THEOREM 1 + L4-DM  →  THEOREM 3
```

---

## 4. Proof of Lemma L1-SUFF (Sufficiency)

**Statement:**
```
∀ t : T,  GBP(t) ∧ BD(t) ∧ OC(t)  →  E(t) = ALLOW
```

**Proof.**

Let `t : T` be arbitrary (universally fixed; no properties of `t` are assumed beyond membership in `T`).

Assume:
```
h : GBP(t) ∧ BD(t) ∧ OC(t)
```

By DEF-4, the evaluator `E` satisfies the biconditional:
```
E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
```

Apply the right-to-left direction of this biconditional (biconditional elimination, `↔`-elim-right`) to hypothesis `h`:
```
h : GBP(t) ∧ BD(t) ∧ OC(t)
DEF-4 (←) : GBP(t) 