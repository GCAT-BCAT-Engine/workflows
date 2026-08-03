S2: Theorem formulation

---

## ARTIFACT LEDGER (preserved)

| stage_id | output_sha256 | admitted | unresolved |
|----------|--------------|----------|------------|
| S0 | sha256:452623dc9b34fa013017eebc9f3a7b57f0a581b1998993caac6b78fa0dc8d1b2 | true | deployed implementation binding remains unresolved |
| S1 | sha256:e2919679a4b76009aac3293cda8b597f3e7dd4436b4ba06a24dfd07ccacdeb5a | true | deployed implementation binding remains unresolved |

---

## STIPULATIONS CARRIED FORWARD (from S1, unmodified)

**STIP-01.** `T` is an abstract type of candidate transitions. No structure beyond type membership is assumed.

**STIP-02.** `GBP : T → Prop` — abstract predicate; internal semantics unspecified.

**STIP-03.** `BD : T → Prop` — abstract predicate; internal semantics unspecified.

**STIP-04.** `OC : T → Prop` — abstract predicate; internal semantics unspecified.

**STIP-05.** `ALLOW : T → Prop` is defined by:

```
ALLOW(t) ⟺ GBP(t) ∧ BD(t) ∧ OC(t)
```

This is a definitional biconditional, not an empirical claim about any deployed system.

**STIP-06.** No claim is made that any deployed GCAT/BCAT implementation conforms to STIP-05 or to any theorem derived from it.

---

## S2 DELIVERABLE: THEOREM FORMULATION

### Theorem ALLOW-NAS (Necessary and Sufficient Characterization)

**Informal statement:**

> For all `t : T`, `ALLOW(t)` holds if and only if `GBP(t)` holds and `BD(t)` holds and `OC(t)` holds.

**Formal statement:**

```
∀ t : T,  ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)
```

**Proof sketch (both directions, from STIP-05 by logical identity):**

- **(→) Necessity.** Assume `ALLOW(t)`. By STIP-05 (unfolding the definition), `GBP(t) ∧ BD(t) ∧ OC(t)` follows immediately. No additional premises are required.

- **(←) Sufficiency.** Assume `GBP(t) ∧ BD(t) ∧ OC(t)`. By STIP-05 (folding the definition), `ALLOW(t)` follows immediately. No additional premises are required.

Both directions are instances of definitional unfolding/folding; the biconditional is provable by `Iff.intro` applied to the two directions, each closed by the definition itself.

---

### Claim Boundary Table

| Claim | Status |
|-------|--------|
| `∀ t : T, ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)` holds under STIP-05 | **In scope — generated claim, proof pending (Lean 4 candidate below)** |
| `GBP`, `BD`, `OC` have specific computational or operational meaning | **Not claimed; abstract only** |
| Any deployed GCAT/BCAT system satisfies STIP-05 or Theorem ALLOW-NAS | **Not claimed; implementation binding unresolved** |
| The Lean 4 candidate below has been verified by a Lean kernel | **Not claimed; candidate status only** |

---

### Lean 4 Candidate (logical core only)

```lean4
-- S2 Lean 4 candidate for Theorem ALLOW-NAS
-- STATUS: CANDIDATE — not claimed kernel-verified
-- GOVERNANCE: Abstract model only. No deployed implementation binding claimed.

section ALLOW_NAS

variable {T : Type*}
variable (GBP BD OC : T → Prop)

-- STIP-05: definitional introduction of ALLOW
def ALLOW (t : T) : Prop := GBP t ∧ BD t ∧ OC t

-- Theorem ALLOW-NAS: necessary and sufficient characterization
theorem allow_nas (t : T) :
    ALLOW GBP BD OC t ↔ GBP t ∧ BD t ∧ OC t := by
  -- Both directions follow from unfolding/folding the definition.
  unfold ALLOW
  exact Iff.rfl

end ALLOW_NAS
```

**Annotation:**

- `unfold ALLOW` reduces the goal to `GBP t ∧ BD t ∧ OC t ↔ GBP t ∧ BD t ∧ OC t`.
- `Iff.rfl` closes the goal by reflexivity of the biconditional.
- No axioms beyond the definition are invoked.
- This is a candidate; kernel verification is not claimed.

---

## UNRESOLVED ITEMS (carried forward)

1. **Deployed implementation binding** — whether any deployed GCAT/BCAT evaluator conforms to STIP-05 remains unresolved and is not addressed by this stage.
2. **Lean 4 kernel verification** — the candidate above has not been submitted to a Lean kernel; verification status is pending.

---

## STAGE IDENTITY