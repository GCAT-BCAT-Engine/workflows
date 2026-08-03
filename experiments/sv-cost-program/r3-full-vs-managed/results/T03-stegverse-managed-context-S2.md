S2: Theorem formulation

---

## Admitted Prior State (preserved)

**ARTIFACT_LEDGER** (carried forward, unmodified):

| stage_id | output_sha256 | admitted | unresolved |
|----------|--------------|----------|------------|
| S0 | `sha256:07aa63378ad0dbfdbd3ec73228d3e96b56d25f52091118ade6f601de65cbab6d` | true | deployed implementation binding remains unresolved |
| S1 | `sha256:0f251aa6ee09b9845a753bedbd13b8f960ba2357e5ecaabeb19cc724e6bba25c` | true | deployed implementation binding remains unresolved |

**Carried stipulations from S1 (verbatim, not re-derived):**

- **S1.1** Three abstract predicates: `GBP`, `BD`, `OC`, each of type `Transition → Prop`.
- **S1.2** `ALLOW : Transition → Prop` is the evaluator output predicate.
- **S1.3** Governing semantic equation (stipulated, not yet formally proved):
  > For all transitions `t`, `ALLOW t` holds if and only if `GBP t` holds and `BD t` holds and `OC t` holds.

**Unresolved (carried):** Deployed implementation binding remains unresolved. No claim is made that any deployed GCAT/BCAT implementation conforms to these predicates or this characterization.

---

## S2 Artifact: Theorem Formulation

### S2.1 — Setting and Vocabulary

All terms below are **abstract**. `Transition` is an uninterpreted type. `GBP`, `BD`, `OC`, and `ALLOW` are uninterpreted predicates. No concrete system is referenced.

---

### S2.2 — Claim Boundary Statement

**What is being claimed:**
A necessary-and-sufficient logical characterization of `ALLOW` in terms of `GBP`, `BD`, and `OC`, under the abstract evaluator model stipulated in S1.

**What is NOT being claimed:**
- That any deployed GCAT/BCAT evaluator implements these predicates.
- That the Lean 4 candidate below has been verified by a Lean kernel.
- That the biconditional holds in any system beyond the abstract model defined here.

---

### S2.3 — Theorem Statement (Natural Language)

**Theorem (ALLOW Admissibility Characterization):**

Let `Transition` be a type. Let `GBP`, `BD`, `OC`, and `ALLOW` be predicates on `Transition`. Under the abstract evaluator model of S1, the following holds:

> For every transition `t : Transition`,
> `ALLOW t` is **necessary and sufficient** for the simultaneous holding of `GBP t`, `BD t`, and `OC t`.
>
> That is:
> `ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)`

**Necessity direction** (`→`):
If `ALLOW t` holds, then `GBP t` holds, `BD t` holds, and `OC t` holds.
*(ALLOW is not granted unless all three conditions are met.)*

**Sufficiency direction** (`←`):
If `GBP t` holds and `BD t` holds and `OC t` holds, then `ALLOW t` holds.
*(All three conditions jointly suffice for ALLOW.)*

---

### S2.4 — Formal Statement (Lean 4 Candidate)

**Status: CANDIDATE ONLY. Not kernel-verified. Not claimed to compile or be semantically complete.**

```lean4
-- S2 Lean 4 Candidate
-- Abstract GCAT/BCAT evaluator: ALLOW admissibility characterization
-- STATUS: Candidate formulation only. Not verified by Lean kernel.
-- GOVERNANCE: No deployed implementation conformance is claimed.

-- Uninterpreted type for transitions
variable (Transition : Type)

-- Abstract predicates (uninterpreted)
variable (GBP : Transition → Prop)
variable (BD  : Transition → Prop)
variable (OC  : Transition → Prop)
variable (ALLOW : Transition → Prop)

-- Governing axiom (from S1.3, stipulated)
-- This axiom encodes the evaluator's semantic equation.
-- It is stipulated, not derived from a concrete implementation.
axiom allow_characterization
    (t : Transition)
    : ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)

-- Theorem: Necessary and sufficient characterization (universal)
-- Follows directly from the governing axiom.
theorem allow_admissibility_iff
    (t : Transition)
    : ALLOW t ↔ (GBP t ∧ BD t ∧ OC t) :=
  allow_characterization Transition GBP BD OC ALLOW t

-- Necessity: ALLOW t → GBP t ∧ BD t ∧ OC t
theorem allow_necessity
    (t : Transition)
    (h : ALLOW t)
    : GBP t ∧ BD t ∧ OC t :=
  (allow_admissibility_iff Transition GBP BD OC ALLOW t).mp h

-- Sufficiency: GBP t ∧ BD t ∧ OC t → ALLOW t
theorem allow_sufficiency
    (t : Transition)
    (h : GBP t ∧ BD t ∧ OC t)
    : ALLOW t :=
  (allow_admissibility