S5: Lean 4 candidate

---

## 1. Stage Identity Record

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S5 — Lean 4 candidate
**Prior admitted state:**
- [S0:sha256:465617e3cb2bf605f0bed1a2326711d64aa44f7fa6e2245387bd3fddb56cfb68]
- [S1:sha256:f21b80c04dbb247b6df1f337dbc06a763bc29397ca7931cd0f81e461e4365541]
- [S2:sha256:d9dd4f1093d7f2078f173bf32fd7186a8fc878f2e09ee49f4cdea11d122d457d]
- [S3:sha256:bc7da0849c187c3cf66e1bdcfe6666a8767e6b5c626f3264d8768e7d8b8415ac]
- [S4:sha256:bd6eaef7c46323b0041997750071772b520dee044ac7f5727d8c434861488396]

---

## 2. Admitted Prior State (Carried Forward Unchanged)

All stipulations, definitions, assumptions, and claim boundaries from S0–S4 are preserved without modification.

| Item | Status | Content |
|------|--------|---------|
| `Transition` | `[STIPULATED]` | Abstract type; domain of all predicates |
| `GBP`, `BD`, `OC` | `[STIPULATED]` | Total predicates `Transition → Prop` |
| `ALLOW` | `[STIPULATED]` | Evaluator output predicate |
| Evaluator Axiom (EA) | `[STIPULATED]` | `∀ t, ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))` |
| `Admissible(t)` | `[DEFINITION — D1]` | Abbreviation: `GBP(t) ∧ BD(t) ∧ OC(t)` |
| T-ALLOW-CHAR | `[GENERATED — UNVERIFIED]` | `∀ t, ALLOW(t) ↔ Admissible(t)` |
| L-SUFF | `[GENERATED — UNVERIFIED]` | `∀ t, Admissible(t) → ALLOW(t)` |
| L-NECE | `[GENERATED — UNVERIFIED]` | `∀ t, ALLOW(t) → Admissible(t)` |
| Informal proof | `[GENERATED — UNVERIFIED, from S4]` | Complete informal proof recorded |
| Assumptions A1–A4 | `[ADOPTED]` | Classical logic, decidability, determinism, no extra axioms |
| Claim boundary | `[PRESERVED]` | No implementation conformance claims made or implied |

---

## 3. Implementation Validity Disclaimer

**[PROHIBITED CLAIM — NOT MADE]** This artifact does not claim that any deployed GCAT or BCAT system conforms to the abstract evaluator, implements the predicates `GBP`, `BD`, or `OC` in any specific way, or satisfies T-ALLOW-CHAR in any operational sense. The Lean 4 candidate below is a **formal artifact for the abstract logical model only**. Its elaboration status in any specific Lean 4 toolchain version is **unresolved implementation evidence** and is not asserted here.

---

## 4. Lean 4 Candidate

The following is the self-contained Lean 4 candidate for the logical core of SV-MATH-001-STAGED. It is structured to correspond directly to the informal proof in S4: the universe of discourse is introduced as a variable section, EA is introduced as a hypothesis, and the three proof obligations (L-SUFF, L-NECE, T-ALLOW-CHAR) are stated and proved in order. Tactic mode is used throughout for auditability; each tactic step corresponds to a named inference step in S4.

```lean4
/-
  SV-MATH-001-STAGED / S5 — Lean 4 candidate
  Experiment: SV-COST-R3-FULL-VS-MANAGED-001

  CLAIM BOUNDARY:
  This file formalizes the abstract evaluator model only.
  No deployed GCAT/BCAT implementation conformance is claimed.
  Elaboration validity in any specific Lean 4 toolchain is
  unresolved implementation evidence and is not asserted.
-/

-- ---------------------------------------------------------------------------
-- Section 1: Universe of discourse and stipulated predicates
-- ---------------------------------------------------------------------------

section AllowAdmissibility

/-
  `Transition` is an abstract type. No structure is assumed.
  All predicates are total functions from `Transition` to `Prop`.
  These correspond to the stipulations recorded in S0 and S1.
-/
variable (Transition : Type)
variable (GBP : Transition → Prop)
variable (BD  : Transition → Prop)
variable (OC  : Transition → Prop)
variable (ALLOW : Transition → Prop)

/-
  Evaluator Axiom (EA) — stipulated, not derived.
  Introduced as a hypothesis so that the formal development
  is self-contained and does not depend on any external axiom
  beyond what is stipulated in the task.
-/
variable (EA : ∀ t : Transition, ALLOW t ↔ (GBP t ∧