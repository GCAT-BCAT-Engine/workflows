S2: Theorem formulation

---

## ARTIFACT LEDGER (preserved)

| stage_id | output_sha256 | admitted | unresolved |
|----------|--------------|----------|------------|
| S0 | sha256:345e03333781a3f599183ec53b1629d03fc9c26831800779aed2fd69c8735488 | true | deployed implementation binding remains unresolved |
| S1 | sha256:6cdd29e798a6595ac32c58eeabe825cd17c34eb9e86075b0e0a439f1bd9ceda9 | true | deployed implementation binding remains unresolved |

---

## STIPULATIONS CARRIED FORWARD (from S1, unmodified)

| Label | Content | Status |
|-------|---------|--------|
| A1 | T is an arbitrary type (the type of candidate transitions) | Stipulated |
| A2 | GBP, BD, OC : T → Prop | Stipulated |
| A3 | E : T → {ALLOW, DENY} | Stipulated |
| A4 | E(t) = ALLOW iff GBP(t) ∧ BD(t) ∧ OC(t) | Stipulated (the evaluator definition) |
| A5 | No decidability of GBP, BD, OC is assumed | Stipulated absence |
| A6 | No relationship among GBP, BD, OC is assumed | Stipulated absence |

---

## S2 GENERATED CLAIMS

### Claim S2-C1 — Necessary and Sufficient Characterization (ALLOW)

**Informal statement:**

For any candidate transition `t : T`, the evaluator returns ALLOW if and only if all three predicates hold simultaneously:

> **E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)**

This is the *primary theorem*. It is a direct biconditional whose left-to-right direction (necessity) and right-to-left direction (sufficiency) are both required.

- **Necessity (→):** If E(t) = ALLOW, then GBP(t) holds, BD(t) holds, and OC(t) holds.
- **Sufficiency (←):** If GBP(t) holds and BD(t) holds and OC(t) holds, then E(t) = ALLOW.

Both directions follow immediately from A4 by the definition of the evaluator. The theorem is therefore *definitionally true* within the abstract model; its content is the explicit statement of that definition as a biconditional proposition available for downstream reasoning.

---

### Claim S2-C2 — Necessary and Sufficient Characterization (DENY)

**Informal statement:**

> **E(t) = DENY ↔ ¬GBP(t) ∨ ¬BD(t) ∨ ¬OC(t)**

This follows from S2-C1 and the fact that {ALLOW, DENY} is a two-element type (E(t) ≠ ALLOW ↔ E(t) = DENY), together with De Morgan's law applied to the negation of the conjunction.

---

### Claim S2-C3 — Conjunction Decomposition (ALLOW implies each predicate individually)

**Informal statement:**

> If E(t) = ALLOW then GBP(t).
> If E(t) = ALLOW then BD(t).
> If E(t) = ALLOW then OC(t).

These are the three projection lemmas derived from S2-C1 (necessity direction). They are stated separately because downstream stages may require them individually.

---

### Claim S2-C4 — Sufficiency of each predicate failing (each negation implies DENY)

**Informal statement:**

> ¬GBP(t) → E(t) = DENY
> ¬BD(t) → E(t) = DENY
> ¬OC(t) → E(t) = DENY

These follow from S2-C2 by disjunction introduction.

---

## CLAIM BOUNDARY

| Claim | Scope | Basis | Verified? |
|-------|-------|-------|-----------|
| S2-C1 | Abstract model only; no deployed system | A4 (stipulated definition) | Pending formal proof (Lean 4 candidate below) |
| S2-C2 | Abstract model only | S2-C1 + two-element outcome type + De Morgan | Pending |
| S2-C3 | Abstract model only | S2-C1 (necessity) | Pending |
| S2-C4 | Abstract model only | S2-C2 + ∨-intro | Pending |
| Deployed GCAT/BCAT conformance | **Out of scope** | Unresolved (carried from S0, S1) | **Not claimed** |

---

## LEAN 4 CANDIDATE — Logical Core

**Status: candidate only. Not claimed to compile or to be implementation-valid. Presented for review at a subsequent verification stage.**

```lean4
/-
  SV-MATH-001 Stage S2: Lean 4 candidate for the logical core.
  STATUS: CANDIDATE ONLY. Not verified. Not claimed to compile.
  Scope: abstract model. No deployed system binding.
-/

-- Outcome type: exactly two values.
inductive Outcome : Type where
  | ALLOW : Outcome
  | DENY  : Outcome
  deriving DecidableEq

-- Abstract evaluator specification (S2 logical core).
-- T is an arbitrary type of candidate transitions.
-- GBP, BD, OC are predicates on T.
-- E is