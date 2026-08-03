S4: Complete informal proof.

---

## ARTIFACT LEDGER (admitted prior state preserved)

| Stage | SHA-256 | Admitted | Unresolved |
|-------|---------|----------|------------|
| S0 | sha256:452623dc9b34fa013017eebc9f3a7b57f0a581b1998993caac6b78fa0dc8d1b2 | ✓ | Deployed implementation binding unresolved |
| S1 | sha256:e2919679a4b76009aac3293cda8b597f3e7dd4436b4ba06a24dfd07ccacdeb5a | ✓ | Deployed implementation binding unresolved |
| S2 | sha256:5078a388f5c1016c81b81db36ad2d004fcc9f3791308613833d6275f5a860a76 | ✓ | Deployed implementation binding unresolved |
| S3 | sha256:43d4595c7b661088d400186d100f7768e99e87571474e415a61ad134ddd67d90 | ✓ | Deployed implementation binding unresolved |

---

## STIPULATIONS (carried forward, unmodified)

**STIP-01.** `T` is an arbitrary type whose elements are called *candidate transitions*.  
**STIP-02.** `GBP`, `BD`, `OC` are uninterpreted predicates `T → Prop`.  
**STIP-03.** `ALLOW` is defined by: `ALLOW t ↔ GBP t ∧ BD t ∧ OC t` (definitional equality, not an axiom).  
**STIP-04.** All reasoning is purely within the abstract model; no operational semantics are assumed.  
**STIP-05.** The claim boundary is the abstract model only.  
**STIP-06.** No claim is made that any deployed GCAT/BCAT implementation conforms to STIP-05 or to any theorem derived from it.

---

## S4 DELIVERABLE: COMPLETE INFORMAL PROOF

### Theorem ALLOW-NAS (restated for self-containment)

> **Theorem ALLOW-NAS.** For every candidate transition `t : T`,  
> `ALLOW t ↔ GBP t ∧ BD t ∧ OC t`.

The proof establishes both directions in turn.

---

### Proof of LEMMA-NEC (Necessity direction)

**Claim.** If `ALLOW t` holds, then `GBP t ∧ BD t ∧ OC t` holds.

**Proof.**

1. Assume `ALLOW t` holds. Call this hypothesis `h`.
2. By STIP-03, `ALLOW` is *defined* as `GBP t ∧ BD t ∧ OC t`. The definition is a definitional equality (not a separate axiom), so `ALLOW t` and `GBP t ∧ BD t ∧ OC t` are the same proposition up to unfolding.
3. Unfolding the definition of `ALLOW` in `h` yields `GBP t ∧ BD t ∧ OC t` directly.
4. Therefore `GBP t ∧ BD t ∧ OC t` holds. ∎

**Remark on proof character.** This direction requires no case analysis, no induction, and no auxiliary lemmas. It is a single step of definitional unfolding. The hypothesis `h : ALLOW t` *is* (by definition) a proof of `GBP t ∧ BD t ∧ OC t`; no information is lost or added.

---

### Proof of LEMMA-SUF (Sufficiency direction)

**Claim.** If `GBP t ∧ BD t ∧ OC t` holds, then `ALLOW t` holds.

**Proof.**

1. Assume `GBP t ∧ BD t ∧ OC t` holds. Call this hypothesis `h`.
2. By STIP-03, `ALLOW t` is defined as `GBP t ∧ BD t ∧ OC t`.
3. Folding the definition of `ALLOW` into `h` yields `ALLOW t` directly.
4. Therefore `ALLOW t` holds. ∎

**Remark on proof character.** This direction is the exact converse of LEMMA-NEC and is equally trivial: it is a single step of definitional folding. The hypothesis `h : GBP t ∧ BD t ∧ OC t` *is* (by definition) a proof of `ALLOW t`.

---

### Assembly: Proof of ALLOW-NAS

**Proof.**

The biconditional `ALLOW t ↔ GBP t ∧ BD t ∧ OC t` is established by introducing both directions:

- The forward direction (→) is LEMMA-NEC, proved above.
- The backward direction (←) is LEMMA-SUF, proved above.

Applying `Iff.intro` to these two proofs yields a proof of the biconditional. Because both directions reduce to definitional unfolding/folding of STIP-03, the entire biconditional is in fact an instance of reflexivity of the definitional equality: `ALLOW t` and `GBP t ∧ BD t ∧ OC t` are the same proposition by definition, so `Iff.rfl` closes the goal directly. ∎

---

### Proof-structure diagram

```
ALLOW-NAS(t)