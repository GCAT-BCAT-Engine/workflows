S3: Proof strategy and lemma decomposition

---

## ARTIFACT IDENTITY

**Stage:** S3
**Depends on admitted artifacts:** S0, S1, S2 (see ARTIFACT_LEDGER)
**Unresolved (carried forward):** Deployed implementation binding remains unresolved. No claim is made that any deployed GCAT/BCAT system conforms to STIP-05 or any theorem derived from it.

---

## ADMITTED PRIOR STATE (preserved)

- **STIP-02/03/04:** `GBP`, `BD`, `OC` are abstract predicates `T → Prop`.
- **STIP-05:** `ALLOW` is defined by `ALLOW(t) ⟺ GBP(t) ∧ BD(t) ∧ OC(t)` for all `t : T`.
- **STIP-06:** No deployed implementation binding is claimed.
- **STIP-07:** The necessary-and-sufficient characterization is the biconditional `ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)`, provable from STIP-05 alone by logical identity.
- **Theorem ALLOW-NAS** (S2, generated claim, proof pending): `∀ t : T, ALLOW(t) ↔ GBP(t) ∧ BD(t) ∧ OC(t)`
- **S2 Lean 4 candidate:** `exact Iff.rfl` proposed as the proof term.

---

## S3 DELIVERABLE: PROOF STRATEGY AND LEMMA DECOMPOSITION

---

### 1. Proof-Theoretic Setting

The proof context is purely propositional and definitional. `ALLOW` is introduced by a `def` (or `abbrev`) in Lean 4 that makes `ALLOW t` *definitionally equal* to `GBP t ∧ BD t ∧ OC t`. No axioms beyond the definition are required. The proof obligation reduces to a question of definitional equality in Lean 4's type theory.

---

### 2. Decomposition of the Biconditional

Theorem ALLOW-NAS decomposes into exactly two directed lemmas:

---

#### LEMMA-NEC (Necessity)

**Statement:** `∀ t : T, ALLOW(t) → GBP(t) ∧ BD(t) ∧ OC(t)`

**Informal argument:**
Assume `h : ALLOW(t)`. By STIP-05, `ALLOW(t)` is defined as `GBP(t) ∧ BD(t) ∧ OC(t)`. Unfolding the definition, `h` already has type `GBP(t) ∧ BD(t) ∧ OC(t)`. The conclusion is immediate.

**Proof strategy:** Definitional unfolding. In Lean 4, if `ALLOW` is a `def`, `exact h` or `assumption` suffices after unfolding, or `Iff.mp (by rfl) h` makes the step explicit.

**Lean 4 candidate for LEMMA-NEC:**
```lean4
lemma allow_necessity (t : T) (h : ALLOW t) : GBP t ∧ BD t ∧ OC t :=
  h  -- definitional equality; ALLOW t unfolds to GBP t ∧ BD t ∧ OC t
```

---

#### LEMMA-SUF (Sufficiency)

**Statement:** `∀ t : T, GBP(t) ∧ BD(t) ∧ OC(t) → ALLOW(t)`

**Informal argument:**
Assume `h : GBP(t) ∧ BD(t) ∧ OC(t)`. By STIP-05, `ALLOW(t)` is defined as exactly this conjunction. Folding the definition, `h` witnesses `ALLOW(t)`.

**Proof strategy:** Definitional folding. In Lean 4, `exact h` suffices by the same definitional equality.

**Lean 4 candidate for LEMMA-SUF:**
```lean4
lemma allow_sufficiency (t : T) (h : GBP t ∧ BD t ∧ OC t) : ALLOW t :=
  h  -- definitional equality; GBP t ∧ BD t ∧ OC t folds to ALLOW t
```

---

### 3. Assembly Strategy for Theorem ALLOW-NAS

With LEMMA-NEC and LEMMA-SUF established, Theorem ALLOW-NAS follows by `Iff.intro`:

```
ALLOW-NAS(t) = Iff.intro (allow_necessity t) (allow_sufficiency t)
```

Because both lemmas reduce to definitional equality, the entire biconditional collapses to `Iff.rfl` — the S2 candidate — which is the most compact expression of the same fact. The lemma decomposition makes the logical structure explicit and auditable even though the proof term is trivial.

---

### 4. Dependency Graph

```
STIP-05 (definition of ALLOW)
    │
    ├──► LEMMA-NEC  (necessity direction)  ─┐
    │                                        ├──► Theorem ALLOW-NAS
    └──► LEMMA-SUF  (sufficiency direction) ─┘
```

No additional lemmas are required. No induction, case analysis, or auxiliary hypotheses are needed. The proof is closed at the definitional level.

---

### 5. Proof