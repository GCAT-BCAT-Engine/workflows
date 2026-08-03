S1: Definitions and assumptions

---

## 1. Task Identity Preservation

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S1 — Definitions and assumptions
**Prior admitted state:** S0:sha256:c4df42b3317fffb79961171953710091fe8399f18aeabf1dfae257de731e3859

---

## 2. Admitted Prior State (Carried Forward Unchanged)

```
ADMITTED FROM S0:
  ST-1  GBP, BD, OC are uninterpreted predicates on a candidate transition t.
  ST-2  E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)  [stipulated evaluator semantics]
  ST-3  The evaluator is abstract; no concrete implementation is referenced.
  ST-4  No deployed GCAT/BCAT system is referenced.

  C-IN-1, C-IN-2, C-IN-3   [in-scope, not yet established]
  C-OUT-1 through C-OUT-4   [permanently excluded]

VERIFIED CLAIMS FROM S0: none
```

---

## 3. Definitions Introduced at S1

All definitions below are stipulative or derived solely from ST-1 and ST-2. No semantic content is added to GBP, BD, or OC beyond their role as propositions.

### 3.1 Carrier type

**DEF-1 (Transition type).**
Let `T` be an arbitrary, unspecified type. Elements of `T` are called *candidate transitions* and are denoted `t`.

*Governance note:* `T` is left abstract. No structure (order, metric, algebraic) is assumed on `T`.

---

### 3.2 Predicate signatures

**DEF-2 (Predicate signatures).**
```
GBP : T → Prop
BD  : T → Prop
OC  : T → Prop
```
Each predicate maps a candidate transition to a proposition in classical propositional logic. No relationship among GBP, BD, OC is assumed; they may be independent, correlated, or logically related — the characterization holds regardless.

---

### 3.3 Outcome type

**DEF-3 (Outcome type).**
Let `Outcome` be a type with at least two distinct inhabitants:
```
ALLOW  : Outcome
DENY   : Outcome
```
No other inhabitants are assumed or required for this task. The characterization concerns only the `ALLOW` case.

*Governance note:* Whether `Outcome` is a two-element type or a richer type is immaterial; the biconditional characterizes exactly the `ALLOW` case.

---

### 3.4 Evaluator

**DEF-4 (Abstract evaluator).**
`E : T → Outcome` is a function satisfying ST-2, i.e.:
```
∀ t : T,  E(t) = ALLOW  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
```
This is the *defining property* of `E` for this task. No algorithm, implementation, or computational procedure is assumed for `E`.

---

### 3.5 Admissibility predicate

**DEF-5 (ALLOW-admissible).**
A candidate transition `t` is called *ALLOW-admissible* (written `Admissible(t)`) if and only if:
```
Admissible(t)  :≡  GBP(t) ∧ BD(t) ∧ OC(t)
```
By DEF-4 (i.e., ST-2), `Admissible(t) ↔ E(t) = ALLOW`. This equivalence is the object of the characterization.

---

## 4. Assumptions in Force at S1

The following assumptions are explicitly recorded. Each is either a direct carry-forward from S0 or a clarification of scope.

| Label | Assumption | Source |
|---|---|---|
| **ASM-1** | Classical propositional logic governs all connectives. | Methodological default |
| **ASM-2** | `T` is non-empty (there exists at least one candidate transition). | Required for universal statements to be non-vacuous |
| **ASM-3** | `GBP`, `BD`, `OC` are total functions on `T` (defined for every `t`). | ST-1 |
| **ASM-4** | `E` is total on `T`. | DEF-4 |
| **ASM-5** | No axioms beyond ST-1, ST-2, DEF-1 through DEF-5, and ASM-1 through ASM-4 are in force. | Minimality |

*Governance note:* ASM-1 (classical logic) is the default for propositional characterization tasks. If constructive logic were required, the biconditional would still hold but the proof term structure would differ. That distinction is noted but does not affect the characterization at this stage.

---

## 5. Logical Primitives and Notation

For precision in S2 and the Lean 4 candidate, the following notation is fixed:

| Symbol | Meaning |
|---|---|
| `∧` | Conjunction (logical AND) |
| `↔` | Biconditional (if and only if) |
| `→` | Implication |
| `∀ t : T` | Universal quantification over transitions |
| `¬` | Negation |
| `∨` | Disjunction (used in