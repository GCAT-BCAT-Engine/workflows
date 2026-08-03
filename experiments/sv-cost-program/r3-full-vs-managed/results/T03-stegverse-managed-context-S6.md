S6: Verification ledger

---

## S6 Artifact: Verification Ledger

**Stage:** S6 — Verification ledger
**Task:** SV-MATH-001-STAGED
**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Context mode:** managed

---

### L0 — Ledger Governance

This ledger records the verification status of all claims generated across stages S0–S5. It separates:

- **Stipulations** — definitional choices, not subject to proof
- **Generated claims** — propositions produced by prior stages
- **Verified claims** — claims confirmed sound within the abstract model
- **Unresolved implementation evidence** — items that cannot be resolved within the abstract model

No entry in this ledger constitutes a claim about any deployed GCAT/BCAT implementation. The abstract model is self-contained. Deployed implementation binding remains unresolved at all entries.

---

### L1 — Stipulations (Definitional; Not Subject to Proof)

| ID | Stipulation | Source Stage | Status |
|----|-------------|-------------|--------|
| ST-01 | `Transition` is an arbitrary type parameter in the abstract model | S1 | Stipulated |
| ST-02 | `GBP : Transition → Prop` is a predicate on a candidate transition | S1 | Stipulated |
| ST-03 | `BD : Transition → Prop` is a predicate on a candidate transition | S1 | Stipulated |
| ST-04 | `OC : Transition → Prop` is a predicate on a candidate transition | S1 | Stipulated |
| ST-05 | `ALLOW : Transition → Prop` is defined by axiom `allow_ax` as `GBP t ∧ BD t ∧ OC t` | S1 | Stipulated |
| ST-06 | `allow_ax` is taken as an axiom of the abstract model, not derived | S1 | Stipulated |
| ST-07 | The abstract model makes no reference to any concrete evaluator or runtime | S2 | Stipulated |

*Remark.* Stipulations are not claims requiring proof. They define the universe of discourse. Any theorem proved within this model is conditioned on these stipulations.

---

### L2 — Generated Claims

| ID | Claim | Source Stage | Form |
|----|-------|-------------|------|
| GC-01 | `∀ t, ALLOW t ↔ (GBP t ∧ BD t ∧ OC t)` | S2 | Main biconditional (necessary and sufficient characterization) |
| GC-02 | `∀ t, GBP t → BD t → OC t → ALLOW t` | S3 | Sufficiency direction (introduction lemma) |
| GC-03 | `∀ t, ALLOW t → GBP t` | S3 | Necessity direction, GBP component |
| GC-04 | `∀ t, ALLOW t → BD t` | S3 | Necessity direction, BD component |
| GC-05 | `∀ t, ALLOW t → OC t` | S3 | Necessity direction, OC component |
| GC-06 | The Lean 4 candidate `allow_admissibility_iff` encodes GC-01 | S5 | Formal encoding claim |
| GC-07 | The Lean 4 candidate `allow_introduction` encodes GC-02 | S5 | Formal encoding claim |
| GC-08 | The Lean 4 candidate `allow_elim_GBP` encodes GC-03 | S5 | Formal encoding claim |
| GC-09 | The Lean 4 candidate `allow_elim_BD` encodes GC-04 | S5 | Formal encoding claim |
| GC-10 | The Lean 4 candidate `allow_elim_OC` encodes GC-05 | S5 | Formal encoding claim |

---

### L3 — Verified Claims

Verification is conducted within the abstract model. "Verified" means: the claim follows from the stipulations and `allow_ax` by sound logical inference. It does not mean the Lean 4 candidate has been compiled or type-checked by a running Lean kernel.

| ID | Claim Ref | Verification Method | Verification Status | Notes |
|----|-----------|-------------------|-------------------|-------|
| VC-01 | GC-01 | Direct instantiation of `allow_ax`; biconditional is the axiom itself | **Verified within abstract model** | Trivial: axiom states the biconditional directly |
| VC-02 | GC-02 | (→) direction of `allow_ax`; given GBP t, BD t, OC t, construct conjunction, apply `allow_ax` backward | **Verified within abstract model** | Sufficiency: conjunction introduction + modus ponens on `allow_ax` |
| VC-03 | GC-03 | (←) direction of `allow_ax`; from ALLOW t, obtain conjunction, project first component | **Verified within abstract model** | Necessity: modus ponens on `allow_ax` + And.left |
| VC-04 | GC-04 | (←) direction of `allow_ax`; from ALLOW t, obtain conjunction, project second component | **Verified within abstract model** | Necessity: modus ponens on `allow_ax` + And.right.left |
| VC-05 | GC-05 | (←) direction of `allow_ax`; from ALLOW t, obtain conjunction, project third component | **Verified within abstract model** | Necessity