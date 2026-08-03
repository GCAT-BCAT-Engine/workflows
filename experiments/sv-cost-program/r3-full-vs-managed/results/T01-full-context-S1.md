S1: Definitions and assumptions

---

## 1. Stage Identity Record

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S1 — Definitions and assumptions
**Prior admitted state:** [S0:sha256:465617e3cb2bf605f0bed1a2326711d64aa44f7fa6e2245387bd3fddb56cfb68]

---

## 2. Admitted Prior State (Carried Forward Unchanged)

The following are carried from S0 without modification. They remain stipulations, not generated claims.

| Symbol | Status | Meaning |
|--------|--------|---------|
| `GBP` | `[STIPULATED]` | A predicate on a candidate transition; holds or does not hold |
| `BD` | `[STIPULATED]` | A predicate on a candidate transition; holds or does not hold |
| `OC` | `[STIPULATED]` | A predicate on a candidate transition; holds or does not hold |
| `ALLOW` | `[STIPULATED]` | The evaluator's affirmative decision on a candidate transition |
| Evaluator rule | `[STIPULATED]` | `ALLOW` is returned **exactly when** `GBP ∧ BD ∧ OC` |

Claim boundary from S0 is **preserved in full**. No implementation conformance claims are made or implied at any point in this stage.

---

## 3. Formal Universe of Discourse

### 3.1 The type `Transition`

We introduce a type `Transition` as the domain over which all predicates are defined. This type is **abstract**: no structure is assumed beyond its existence as a type. No element of `Transition` is identified with any real-world object or any object in any deployed system.

> **[STIPULATED — domain]** There exists a non-empty type `Transition`. Variables `t`, `t₁`, `t₂`, … range over `Transition`.

### 3.2 The predicates

Each predicate is a total function from `Transition` to `Prop` (in the Lean 4 / dependent type theory sense, equivalently a total Boolean-valued function in classical logic).

| Predicate | Type | Status |
|-----------|------|--------|
| `GBP : Transition → Prop` | Total predicate | `[STIPULATED]` |
| `BD  : Transition → Prop` | Total predicate | `[STIPULATED]` |
| `OC  : Transition → Prop` | Total predicate | `[STIPULATED]` |

No relationship among `GBP`, `BD`, and `OC` is assumed. They may be independent, overlapping, or correlated; the formal development does not depend on any such relationship.

### 3.3 The evaluator output predicate

`ALLOW : Transition → Prop` is the predicate that holds of `t` exactly when the evaluator returns the affirmative decision for `t`.

> **[STIPULATED — evaluator rule]**
> For all `t : Transition`, `ALLOW t` holds if and only if `GBP t ∧ BD t ∧ OC t`.

This stipulation is the **sole definitional content** of `ALLOW` in this task. It is not derived; it is given.

---

## 4. Logical Assumptions Adopted

The following logical assumptions are adopted for this stage and all subsequent stages. They are standard and are stated explicitly for auditability.

| # | Assumption | Justification |
|---|-----------|---------------|
| A1 | Classical propositional logic (law of excluded middle applies) | Standard for biconditional reasoning; consistent with Lean 4 + `Classical` |
| A2 | Each predicate is decidable for each `t` (i.e., for any `t`, each of `GBP t`, `BD t`, `OC t` either holds or does not) | Follows from classical logic; no constructive restriction imposed |
| A3 | The evaluator is deterministic: for a given `t`, it returns at most one decision | Implicit in the stipulation; stated explicitly for completeness |
| A4 | No additional axioms about `Transition` or the predicates are introduced | Ensures the formal development is self-contained |

---

## 5. Definitions Introduced in This Stage

### 5.1 Admissibility predicate (definitional)

> **[DEFINITION — D1]** `[GENERATED — UNVERIFIED as a claim; definitional as a label]`
>
> For `t : Transition`, define:
> ```
> Admissible(t) :≡ GBP(t) ∧ BD(t) ∧ OC(t)
> ```
> This is a **definitional abbreviation** introduced for readability. It carries no logical content beyond the conjunction.

### 5.2 The target biconditional (stated, not yet proved)

> **[GENERATED — UNVERIFIED]** Target claim TC-1 (to be proved in S2):
>
> ```
> ∀ t : Transition,  ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))
> ```
>
> Equivalently, using D1:
> ```
> ∀ t : Transition,  ALLOW(t) ↔ Admissible(t)
> ```

This claim is **not yet verified**. It will be the subject of S2 (proof) and S3 (Lean 4 candidate).

### 5.3 Necessary condition (stated, not yet proved)

> **[GENERATED — UNVERIFIED]** Claim NC-1