S6: Verification ledger

---

## 1. Task Identity Preservation

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S6 — Verification ledger
**Prior admitted state:** S5:sha256:1ceea9232721c5cba07616a102c9778d5e6a6bac164e3a859ac1845fa6a1a876

---

## 2. Admitted Prior State (Carried Forward Unchanged)

```
ADMITTED FROM S0–S5:
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
  LEMMA L4-DM    ∀ t : T,  ¬(GBP(t) ∧ BD(t) ∧ OC(t))
                            ↔  ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)

  S5 Lean 4 candidate: produced, not mechanically verified
  C-IN-1  [established informally at S4]
  C-IN-2  [candidate produced at S5]
  C-IN-3  [established informally at S4]
  C-OUT-1 through C-OUT-4  [permanently excluded]

VERIFIED CLAIMS FROM S0–S5: none mechanically verified
```

---

## 3. Governance Notes for This Stage

The verification ledger records the verification status of every claim generated across S0–S5. It does not itself verify any claim. It separates:

- **Stipulations** — accepted without proof by task statement
- **Generated claims** — produced by this task's reasoning
- **Verified claims** — claims for which a completed verification exists
- **Unresolved implementation evidence** — items requiring external mechanical checking

No new mathematical content is introduced at this stage. The ledger is a faithful record of the epistemic state of the task at S6.

---

## 4. Stipulations Ledger

Stipulations are accepted as given. They are not subject to verification within this task. Their status is permanently ACCEPTED.

| Label | Content | Status |
|---|---|---|
| ST-1 | GBP, BD, OC are uninterpreted predicates on a candidate transition t | ACCEPTED (stipulated) |
| ST-2 | E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t) | ACCEPTED (stipulated) |
| ST-3 | The evaluator is abstract; no concrete implementation is referenced | ACCEPTED (stipulated) |
| ST-4 | No deployed GCAT/BCAT system is referenced | ACCEPTED (stipulated) |

---

## 5. Definitions Ledger

Definitions are introduced by this task. They are not claims requiring proof; they are naming conventions and structural choices. Status is INTRODUCED.

| Label | Content | Introduced At | Status |
|---|---|---|---|
| DEF-1 | T : arbitrary carrier type of candidate transitions | S1 | INTRODUCED |
| DEF-2 | GBP, BD, OC : T → Prop | S1 | INTRODUCED |
| DEF-3 | Outcome : type with inhabitants ALLOW, DENY | S