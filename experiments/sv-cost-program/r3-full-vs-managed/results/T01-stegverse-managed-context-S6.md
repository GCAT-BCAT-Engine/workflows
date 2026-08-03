S6: Verification ledger

---

## Stage S6 — Verification Ledger

This artifact is self-contained within the abstract model defined by stipulations A1–A4. No claim is made that any deployed GCAT/BCAT implementation conforms to this model. Deployed implementation binding remains unresolved. Stipulations, generated claims, verified claims, and unresolved implementation evidence are kept separate below.

---

### Section 1 — Admitted Stipulations (carried forward, unchanged)

| ID | Statement |
|----|-----------|
| A1 | `T` is an arbitrary type (the type of candidate transitions). |
| A2 | `GBP`, `BD`, `OC` are predicates `T → Prop`. |
| A3 | `Outcome` is an inductive type with exactly two constructors: `ALLOW` and `DENY`. |
| A4 | The evaluator `E : T → Outcome` is defined by: `E(t) = ALLOW` if and only if `GBP(t) ∧ BD(t) ∧ OC(t)`; otherwise `E(t) = DENY`. |

These stipulations are purely definitional. They carry no claim about any deployed system.

---

### Section 2 — Generated Claims (carried forward, unchanged)

| ID | Claim | Source stage |
|----|-------|-------------|
| S2-C1 | `∀ t : T, E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)` | S2 |
| S2-C2 | `∀ t : T, E(t) = DENY ↔ ¬(GBP(t) ∧ BD(t) ∧ OC(t))` | S2 |

---

### Section 3 — Verification Ledger

Each entry records the claim, the proof artifact that addresses it, the verification status within the abstract model, and any residual issues.

---

#### Entry VL-01 — Claim S2-C1

| Field | Content |
|-------|---------|
| **Claim ID** | S2-C1 |
| **Statement** | `∀ t : T, E(t) = ALLOW ↔ GBP(t) ∧ BD(t) ∧ OC(t)` |
| **Informal proof artifact** | S4 (sha256:87abe5167f755abc719153a804ee47a2abac77df6c801f51a2c77e03008f5d98) |
| **Lean 4 candidate artifact** | S5 (sha256:c1c801c1ed7db04e02e3137ee4a71e375056d156df67a64e14a4430cd014bcd4) |
| **Proof strategy** | Biconditional split. Direction 1 (→): assume `E(t) = ALLOW`; by A4 the only branch producing `ALLOW` requires `GBP(t) ∧ BD(t) ∧ OC(t)`, so the conjunction holds. Direction 2 (←): assume `GBP(t) ∧ BD(t) ∧ OC(t)`; by A4 the evaluator returns `ALLOW`. Both directions are immediate from A4 by case analysis on the definition of `E`. |
| **Informal proof status** | **Verified within abstract model.** The argument uses only A1–A4; no external facts are invoked. Each direction is independently auditable. |
| **Lean 4 candidate status** | **Candidate only — not machine-checked in this pipeline.** The S5 artifact presents the structural skeleton (`unfold E`, `constructor`, `intro h`, `exact h`). The tactic sequence is consistent with the informal proof. No Lean 4 kernel output is available; machine-check status is **unresolved**. |
| **Residual issues** | (i) Lean 4 kernel verification not performed in this pipeline. (ii) Deployed implementation binding unresolved. |

---

#### Entry VL-02 — Claim S2-C2

| Field | Content |
|-------|---------|
| **Claim ID** | S2-C2 |
| **Statement** | `∀ t : T, E(t) = DENY ↔ ¬(GBP(t) ∧ BD(t) ∧ OC(t))` |
| **Informal proof artifact** | S4 (sha256:87abe5167f755abc719153a804ee47a2abac77df6c801f51a2c77e03008f5d98) |
| **Lean 4 candidate artifact** | S5 (sha256:c1c801c1ed7db04e02e3137ee4a71e375056d156df67a64e14a4430cd014bcd4) |
| **Proof strategy** | S2-C2 is derivable from S2-C1 together with the exhaustiveness of `Outcome` (A3). Since `Outcome` has exactly two constructors and they are distinct, `E(t) ≠ ALLOW ↔ E(t) = DENY`. Composing with S2-C1 yields S2-C2. Alternatively: Direction 1 (→): assume `E(t) = DENY`; if `GBP(t) ∧ BD(t) ∧ OC(t)` held, A4 would force `E(t) = ALLOW`, contradicting `ALLOW ≠ DENY`; so the conjunction fails. Direction 2 (←): assume `¬(GBP