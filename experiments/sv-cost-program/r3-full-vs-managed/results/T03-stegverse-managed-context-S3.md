S3: Proof strategy and lemma decomposition

---

## S3 Artifact: Proof Strategy and Lemma Decomposition

**Depends on:**
- S1 `sha256:0f251aa6ee09b9845a753bedbd13b8f960ba2357e5ecaabeb19cc724e6bba25c`
- S2 `sha256:4108822c11a254244e18b4d806a4c39fc4b52f080bb78a865e36e2ef50d7aa02`

---

### S3.1 — Proof-Theoretic Orientation

The central theorem `allow_admissibility_iff` has the form:

```
∀ t : Transition, ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)
```

An iff proof decomposes canonically into two directed implications:

| Direction | Name | Reading |
|---|---|---|
| (→) | **Necessity** | `ALLOW t → GBP t ∧ BD t ∧ OC t` |
| (←) | **Sufficiency** | `GBP t ∧ BD t ∧ OC t → ALLOW t` |

Both directions are derivable directly from the axiomatic stipulation introduced in S1 (Stipulation S1.3), which asserts the biconditional as a definitional axiom over the abstract model. No induction, case analysis, or computational unfolding is required. The proof is purely propositional.

---

### S3.2 — Lemma Inventory

**Lemma L1 — Necessity (Forward Direction):**

> If `ALLOW t` holds, then `GBP t` holds, `BD t` holds, and `OC t` holds.

```
lemma allow_necessity :
    ∀ t : Transition, ALLOW t → GBP t ∧ BD t ∧ OC t
```

*Proof strategy:* Apply the forward direction (`mp`) of the axiomatic biconditional `allow_ax` to the hypothesis `h : ALLOW t`. The result is the conjunction `GBP t ∧ BD t ∧ OC t` directly.

---

**Lemma L2 — Sufficiency (Backward Direction):**

> If `GBP t` holds, `BD t` holds, and `OC t` holds, then `ALLOW t` holds.

```
lemma allow_sufficiency :
    ∀ t : Transition, GBP t ∧ BD t ∧ OC t → ALLOW t
```

*Proof strategy:* Apply the backward direction (`mpr`) of the axiomatic biconditional `allow_ax` to the hypothesis `h : GBP t ∧ BD t ∧ OC t`. The result is `ALLOW t` directly.

---

**Lemma L3 — Conjunct Extraction (Auxiliary, used in downstream stages):**

> From `GBP t ∧ BD t ∧ OC t`, each conjunct is individually extractable.

```
lemma extract_GBP : GBP t ∧ BD t ∧ OC t → GBP t
lemma extract_BD  : GBP t ∧ BD t ∧ OC t → BD t
lemma extract_OC  : GBP t ∧ BD t ∧ OC t → OC t
```

*Proof strategy:* Standard `And.left` / `And.right` projections. These are trivial but are isolated to keep the main theorem proof readable and to support any future stage that requires individual predicate witnesses.

---

### S3.3 — Assembly Strategy for `allow_admissibility_iff`

The main theorem is assembled from L1 and L2 via `Iff.intro`:

```
theorem allow_admissibility_iff (t : Transition) :
    ALLOW t ↔ GBP t ∧ BD t ∧ OC t :=
  Iff.intro
    (allow_necessity t)
    (allow_sufficiency t)
```

No additional lemmas are required for the logical core. L3 is auxiliary and supports downstream use only.

---

### S3.4 — Axiomatic Dependency Map

```
allow_ax : ∀ t, ALLOW t ↔ GBP t ∧ BD t ∧ OC t   [stipulated, S1]
         │
         ├──(mp)──→  allow_necessity   (L1)
         │
         └──(mpr)─→  allow_sufficiency (L2)
                          │
                          └──(Iff.intro)──→  allow_admissibility_iff
```

All proof steps are single-step applications of the axiom. No auxiliary hypotheses, no induction, no decidability assumptions.

---

### S3.5 — Lean 4 Candidate (Logical Core)

```lean4
-- S3 Lean 4 Candidate: Proof strategy instantiation
-- CLAIM BOUNDARY: Abstract model only. No deployed GCAT/BCAT implementation validity claimed.

section AllowAdmissibility

variable (Transition : Type)
variable (GBP BD OC : Transition → Prop)
variable (ALLOW     : Transition → Prop)

-- Axiomatic stipulation (from S1)
variable (allow_ax : ∀ t : Transition, ALLOW t ↔ (GBP t ∧ BD t ∧ OC t))

-- L1: Necessity
lemma allow_necessity
    (t : Transition)