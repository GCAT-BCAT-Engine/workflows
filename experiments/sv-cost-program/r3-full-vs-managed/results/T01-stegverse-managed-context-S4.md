S4: Complete informal proof.

---

## Stage S4 — Complete Informal Proof

### Governance Notice

This artifact is self-contained within the abstract model defined by stipulations A1–A4. No claim is made that any deployed GCAT/BCAT implementation conforms to this model. Deployed implementation binding remains unresolved. Stipulations, generated claims, and proof steps are kept separate below.

---

### Recalled Stipulations (from S1/S2)

| Label | Content |
|-------|---------|
| A1 | `t` ranges over candidate transitions in an abstract domain `T`. |
| A2 | `GBP`, `BD`, `OC` are uninterpreted predicates on `T`. |
| A3 | `E : T → {ALLOW, DENY}` is the abstract evaluator. |
| A4 | `E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)` — the evaluator definition (stipulated). |

---

### Theorem to Prove (S2-C1, restated)

**Theorem (ALLOW Admissibility — Necessary and Sufficient Characterization).**
For all `t : T`,

```
E(t) = ALLOW   ↔   GBP(t) ∧ BD(t) ∧ OC(t).
```

---

### Proof

The proof proceeds by establishing each direction of the biconditional separately. Both directions are immediate consequences of A4, but we make the reasoning fully explicit so that each step is independently auditable and so that the Lean 4 candidate in S5 can mirror the structure exactly.

---

#### Direction 1 — Sufficiency (right-to-left): `GBP(t) ∧ BD(t) ∧ OC(t) → E(t) = ALLOW`

**Lemma S3-L1 (recalled):** If `GBP(t)` holds, and `BD(t)` holds, and `OC(t)` holds, then `E(t) = ALLOW`.

**Proof of Direction 1.**

Let `t : T` be arbitrary. Assume:

- (H1) `GBP(t)`
- (H2) `BD(t)`
- (H3) `OC(t)`

From H1, H2, H3, by conjunction introduction:

- (H4) `GBP(t) ∧ BD(t) ∧ OC(t)`

A4 states: `E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`.

Apply the right-to-left direction of A4 to H4:

- (H5) `E(t) = ALLOW`

**Conclusion:** `E(t) = ALLOW`. ∎

---

#### Direction 2 — Necessity (left-to-right): `E(t) = ALLOW → GBP(t) ∧ BD(t) ∧ OC(t)`

**Lemma S3-L2 (recalled):** If `E(t) = ALLOW`, then `GBP(t)` holds, `BD(t)` holds, and `OC(t)` holds.

**Proof of Direction 2.**

Let `t : T` be arbitrary. Assume:

- (H1) `E(t) = ALLOW`

A4 states: `E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)`.

Apply the left-to-right direction of A4 to H1:

- (H2) `GBP(t) ∧ BD(t) ∧ OC(t)`

By conjunction elimination from H2:

- (H3) `GBP(t)`
- (H4) `BD(t)`
- (H5) `OC(t)`

**Conclusion:** `GBP(t) ∧ BD(t) ∧ OC(t)`. ∎

---

#### Combination — Biconditional

From Direction 1 and Direction 2, by biconditional introduction:

```
E(t) = ALLOW   ↔   GBP(t) ∧ BD(t) ∧ OC(t).
```

Since `t` was arbitrary, this holds for all `t : T`. ∎

---

### Claim Boundary

| Claim | Status |
|-------|--------|
| S2-C1: The biconditional holds in the abstract model | **Proved** — both directions established above, each by direct application of A4. |
| The proof is valid within the abstract model defined by A1–A4 | **Asserted** — the model is purely stipulative; no external facts are used. |
| Any deployed GCAT/BCAT system satisfies A4 | **Not claimed** — deployed implementation binding remains unresolved. |

---

### Proof-Structure Summary

```
Theorem S2-C1
├── Direction 1 (Sufficiency, S3-L1)
│   ├── Assume: GBP(t), BD(t), OC(t)
│   ├── Conjunction introduction → GBP(t) ∧ BD(t) ∧ OC(t)
│   └── A4 (←) → E(t) = ALLOW                          ✓
└── Direction 2 (Necessity, S3-L2)
    ├── Assume: E(t) = ALLOW
    ├── A4 (→) → GBP(t