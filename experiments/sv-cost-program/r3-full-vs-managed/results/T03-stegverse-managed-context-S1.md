S1: Definitions and assumptions

---

## Artifact Identity

**Stage:** S1 — Definitions and assumptions
**Depends on:** S0 `sha256:07aa63378ad0dbfdbd3ec73228d3e96b56d25f52091118ade6f601de65cbab6d`

---

## 1. Admitted Prior State (Preserved)

From S0:
- Task parsed. Three abstract predicates identified: **GBP**, **BD**, **OC**.
- Evaluator output: **ALLOW**.
- Claim boundary established: no deployed implementation binding; no semantic content claimed for predicates beyond their role as abstract propositions.
- Unresolved: deployed implementation binding remains unresolved.

---

## 2. Stipulations (This Stage)

The following are **stipulations** — definitional choices made for this task. They are not empirical claims and are not verified against any deployed system.

---

### 2.1 Universe of Discourse

**Stipulation S1.1:** There exists a non-empty type `Transition` representing candidate transitions submitted to the evaluator. No further structure is assumed on `Transition`.

---

### 2.2 Predicate Declarations

**Stipulation S1.2:** The following are abstract unary predicates on `Transition`:

| Identifier | Type | Role |
|---|---|---|
| `GBP` | `Transition → Prop` | First conjunct condition |
| `BD` | `Transition → Prop` | Second conjunct condition |
| `OC` | `Transition → Prop` | Third conjunct condition |

No internal structure, decidability, or mutual independence is assumed for these predicates at this stage. They are treated as arbitrary propositions parameterized by a transition.

---

### 2.3 Evaluator Output Declaration

**Stipulation S1.3:** The evaluator output `ALLOW` is modeled as a unary predicate on `Transition`:

```
ALLOW : Transition → Prop
```

`ALLOW t` holds when the evaluator returns the ALLOW decision for transition `t`.

---

### 2.4 Evaluator Semantics (The Core Stipulation)

**Stipulation S1.4 (Evaluator Rule):** The evaluator is stipulated to satisfy the following rule, taken as the defining behavioral specification:

> For all transitions `t`, `ALLOW t` holds **if and only if** `GBP t` holds **and** `BD t` holds **and** `OC t` holds.

Formally:

```
∀ t : Transition, ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)
```

This biconditional is the **sole** behavioral axiom governing the evaluator in this task. It is a stipulation, not a theorem at this stage.

---

### 2.5 Logical Framework Assumptions

**Stipulation S1.5:** The ambient logic is **classical propositional/predicate logic** embedded in a constructive type theory (Lean 4 / Prop). Classical reasoning (e.g., excluded middle) is available via `Classical` if needed, but the core biconditional does not require it.

**Stipulation S1.6:** No additional axioms (e.g., function extensionality, propositional extensionality) are assumed beyond what Lean 4's core provides, unless explicitly introduced in a later stage.

---

### 2.6 Scope of Definitions

**Stipulation S1.7:** The definitions in this stage are **purely abstract**. They do not reference:
- Any concrete GCAT or BCAT implementation.
- Any specific transition format, protocol, or system.
- Any runtime behavior of any deployed evaluator.

---

## 3. Generated Claims (This Stage)

The following claims are **generated** (asserted as consequences of the stipulations) but are **not yet verified** by proof in this stage. Verification is deferred to later stages.

| ID | Claim | Status |
|---|---|---|
| GC-S1-01 | Under S1.4, `ALLOW t` is necessary and sufficient for `GBP t ∧ BD t ∧ OC t` | Generated, unverified |
| GC-S1-02 | The biconditional in S1.4 is the minimal axiom needed to characterize ALLOW | Generated, unverified |

---

## 4. Verified Claims (This Stage)

None. No proofs are produced at S1. Definitions and stipulations are not subject to proof; they are admitted by construction.

---

## 5. Unresolved Items (Carried Forward)

| ID | Item |
|---|---|
| UR-001 | Deployed implementation binding remains unresolved (carried from S0) |
| UR-002 | Decidability of GBP, BD, OC is not assumed and remains unaddressed |
| UR-003 | Whether S1.4 is consistent with any concrete system is outside scope and unresolved |

---

## 6. Lean 4 Skeleton (Definitions Only — No Proofs)

The following is a **candidate skeleton** for the logical core. It encodes the stipulations above. It is **not claimed to compile without error** and is **not claimed to reflect any deployed implementation**.

```lean4
-- S1: Definitions and assumptions
-- Abstract GCAT/BCAT evaluator — logical core skeleton
-- No implementation validity claimed.

-- S1.1: Abstract transition type
variable (Transition : Type)

-- S1.2: Abstract predicates
variable (GBP : Transition → Prop)
variable (BD  : Transition → Prop)
variable (OC  : Transition → Prop)

-- S1.3 / S1.4: ALLOW predicate and evaluator rule (stipulated as axiom)
variable