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
- `UNRESOLVED-003`: Abstract type `T` is unconstrained; no inhabitant is assumed.

---

## 2. Stipulations (This Stage)

The following are **stipulations** — definitional choices made for this task. They are not empirical claims and do not assert anything about any deployed system.

### 2.1 Abstract Universe

**STIP-01.** There exists an abstract type `T` representing candidate transitions. No structure on `T` is assumed beyond its existence as a type.

### 2.2 Predicate Stipulations

**STIP-02.** `GBP : T → Prop` — "Good Baseline Predicate." A predicate on candidate transitions. Its internal semantics are left abstract.

**STIP-03.** `BD : T → Prop` — "Boundary Disposition." A predicate on candidate transitions. Its internal semantics are left abstract.

**STIP-04.** `OC : T → Prop` — "Operational Condition." A predicate on candidate transitions. Its internal semantics are left abstract.

### 2.3 Evaluator Stipulation

**STIP-05.** The abstract GCAT/BCAT evaluator is modeled as a function:

```
ALLOW : T → Prop
```

defined by the following **definitional equation** (the object of study):

```
ALLOW(t) ⟺ GBP(t) ∧ BD(t) ∧ OC(t)
```

This is a **stipulated definition**, not a derived theorem. It encodes the problem statement directly.

### 2.4 Scope Stipulations

**STIP-06.** All reasoning is purely propositional/logical over the abstract predicates. No computational or operational semantics are assumed.

**STIP-07.** "Necessary and sufficient characterization" means: a biconditional `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)` holds for all `t : T`, provable from STIP-05 alone by logical identity.

---

## 3. Claim Boundary (Restated and Refined)

| Claim | Status |
|---|---|
| `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)` holds for all abstract `t : T` under STIP-05 | **In scope — generated claim, proof pending** |
| The Lean 4 candidate below is logically correct | **Generated claim — not mechanically verified (UNRESOLVED-002)** |
| Any deployed GCAT/BCAT system satisfies this characterization | **Not claimed; outside scope** |
| `GBP`, `BD`, `OC` have any specific computational meaning | **Not claimed; abstract only** |

---

## 4. Generated Claim (This Stage)

**CLAIM-S1-01** *(Necessary and Sufficient Characterization — Abstract)*

> For all `t : T`, under the stipulated definition STIP-05:
>
> `ALLOW(t)` holds **if and only if** `GBP(t)` holds **and** `BD(t)` holds **and** `OC(t)` holds.

**Necessity direction:** If `ALLOW(t)`, then by STIP-05 (unfolding the definition), `GBP(t) ∧ BD(t) ∧ OC(t)`.

**Sufficiency direction:** If `GBP(t) ∧ BD(t) ∧ OC(t)`, then by STIP-05 (folding the definition), `ALLOW(t)`.

**Status:** Generated claim. Logical argument is by definitional unfolding/folding. Mechanical verification is pending (UNRESOLVED-002).

---

## 5. Lean 4 Candidate

The following is a **candidate** for the logical core. It is presented for review. **No claim is made that it compiles or that any proof obligation is discharged without mechanical checking.**

```lean4
-- SV-MATH-001-STAGED: Lean 4 Candidate (S1)
-- STATUS: Candidate only. Not mechanically verified.
-- CLAIM BOUNDARY: Abstract logical core only.
--   No deployed GCAT/BCAT implementation validity is claimed.

section GCATAbstract

-- STIP-01: