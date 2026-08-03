S1: Definitions and assumptions

---

## Artifact Header

| Field | Value |
|---|---|
| Stage | S1 — Definitions and assumptions |
| Task | SV-MATH-001-STAGED |
| Experiment | SV-COST-R3-FULL-VS-MANAGED-001 |
| Depends on | S0 `sha256:452623dc9b34fa013017eebc9f3a7b57f0a581b1998993caac6b78fa0dc8d1b2` |
| Claims excluded | Deployed GCAT/BCAT implementation validity |

---

## 1. Admitted Prior State (Preserved)

```
ARTIFACT_LEDGER = [
  { stage_id: "S0",
    output_sha256: "sha256:452623dc9b34fa013017eebc9f3a7b57f0a581b1998993caac6b78fa0dc8d1b2",
    admitted: true,
    unresolved: "deployed implementation binding remains unresolved" }
]
```

Unresolved items carried forward from S0:

- `UNRESOLVED-001`: Lean 4 candidate not yet produced — **partially addressed this stage; proof obligation remains open**.
- `UNRESOLVED-002`: No mechanically checked proof exists yet.
- `UNRESOLVED-003`: Abstract type `T` is unconstrained; no inhabitant assumed.

---

## 2. Stipulated Definitions (This Stage)

All items in this section are **stipulations** — they fix vocabulary for the task. They are not empirical claims and do not assert anything about any deployed system.

---

### 2.1 Abstract Domain

**STIPULATION S1-D1 (Candidate transition type).**
Let `T` be an arbitrary type. Elements of `T` are called *candidate transitions*. No structure on `T` is assumed beyond what is stated here.

---

### 2.2 Predicate Stipulations

**STIPULATION S1-D2 (GBP).**
`GBP : T → Prop` is a predicate on candidate transitions. The name abbreviates *Good Baseline Predicate* for labeling purposes only; no semantic content beyond the type is stipulated.

**STIPULATION S1-D3 (BD).**
`BD : T → Prop` is a predicate on candidate transitions.

**STIPULATION S1-D4 (OC).**
`OC : T → Prop` is a predicate on candidate transitions.

---

### 2.3 Evaluator Stipulation

**STIPULATION S1-D5 (Abstract GCAT/BCAT evaluator — ALLOW rule).**
An abstract evaluator `E` is stipulated to satisfy the following rule, for every `t : T`:

```
E(t) = ALLOW   ⟺   GBP(t) ∧ BD(t) ∧ OC(t)
```

This is a **definitional stipulation** of the abstract evaluator. It is not a claim about any deployed system.

---

### 2.4 Admissibility Predicate

**STIPULATION S1-D6 (ALLOW-admissible).**
A candidate transition `t : T` is called *ALLOW-admissible* (written `Admissible t`) if and only if `E(t) = ALLOW`.

By S1-D5, this unfolds immediately to:

```
Admissible t   ⟺   GBP(t) ∧ BD(t) ∧ OC(t)
```

---

## 3. Necessary-and-Sufficient Characterization (Generated Claim)

**GENERATED CLAIM S1-C1 (N&S characterization of ALLOW admissibility).**

> *Under stipulations S1-D1 through S1-D6, for any `t : T`:*
>
> `Admissible t` **if and only if** `GBP t ∧ BD t ∧ OC t`.
>
> *Necessity:* If `Admissible t`, then by S1-D6 and S1-D5, `GBP t ∧ BD t ∧ OC t` holds.
>
> *Sufficiency:* If `GBP t ∧ BD t ∧ OC t`, then by S1-D5 and S1-D6, `Admissible t` holds.

**Status:** Generated claim. Follows directly from the stipulations by unfolding definitions. Not yet mechanically verified (see `UNRESOLVED-002`).

---

## 4. Claim Boundary (Restated and Sharpened)

| Claim | Status |
|---|---|
| S1-C1 holds under stipulations S1-D1–S1-D6 | **Generated; pending mechanical check** |
| Any deployed GCAT/BCAT system satisfies S1-C1 | **Not claimed; outside scope** |
| `T` has any particular inhabitant | **Not claimed** |
| The predicates GBP, BD, OC have any particular extension | **Not claimed** |
| The Lean 4 candidate below is verified by a proof checker | **Not claimed; UNRESOLVED-002 open** |

---

## 5. Lean 4 Candidate (Logical Core)

The following is a **candidate** for the logical core. It is syntactically structured for Lean 4. It is **not claimed to compile or to have been checked** by any proof assistant. It addresses `UNRESOLVED-001` partially; `UNRESOLVED-002` remains open.

```lean4
-- S1: Lean 4 candidate for ALLOW admissibility character