# S2: Theorem formulation

---

## 1. Stage Identity Record

**Experiment:** SV-COST-R3-FULL-VS-MANAGED-001
**Task:** SV-MATH-001-STAGED
**Stage:** S2 — Theorem formulation
**Prior admitted state:**
- [S0:sha256:465617e3cb2bf605f0bed1a2326711d64aa44f7fa6e2245387bd3fddb56cfb68]
- [S1:sha256:f21b80c04dbb247b6df1f337dbc06a763bc29397ca7931cd0f81e461e4365541]

---

## 2. Admitted Prior State (Carried Forward Unchanged)

All stipulations, definitions, and claim boundaries from S0 and S1 are preserved without modification.

| Item | Status | Content |
|------|--------|---------|
| `Transition` | `[STIPULATED]` | Abstract type; domain of all predicates |
| `GBP`, `BD`, `OC` | `[STIPULATED]` | Total predicates `Transition → Prop` |
| `ALLOW` | `[STIPULATED]` | Evaluator output predicate; defined by the evaluator rule |
| Evaluator rule | `[STIPULATED]` | `ALLOW(t)` holds iff `GBP(t) ∧ BD(t) ∧ OC(t)`, for all `t` |
| `Admissible(t)` | `[DEFINITION — D1]` | Abbreviation for `GBP(t) ∧ BD(t) ∧ OC(t)` |
| TC-1 | `[GENERATED — UNVERIFIED, carried from S1]` | `∀ t, ALLOW(t) ↔ Admissible(t)` |
| Assumptions A1–A4 | `[ADOPTED]` | Classical logic, decidability, determinism, no extra axioms |
| Claim boundary | `[PRESERVED]` | No implementation conformance claims made or implied |

---

## 3. Theorem Formulation

### 3.1 Primary theorem — necessary and sufficient characterization

> **[GENERATED — UNVERIFIED]** **Theorem T-ALLOW-CHAR** *(ALLOW Admissibility Characterization)*
>
> Let `Transition` be an abstract type. Let `GBP`, `BD`, `OC`, `ALLOW : Transition → Prop` be total predicates satisfying the evaluator rule:
>
> > **(Evaluator Axiom, EA)** `∀ t : Transition, ALLOW(t) ↔ (GBP(t) ∧ BD(t) ∧ OC(t))`
>
> Then, for any `t : Transition`:
>
> ```
> ALLOW(t)  ↔  GBP(t) ∧ BD(t) ∧ OC(t)
> ```
>
> That is, `ALLOW(t)` holds **if and only if** all three of `GBP(t)`, `BD(t)`, and `OC(t)` hold.

**Remark on logical status.** The Evaluator Axiom EA is the stipulated rule from S0/S1. T-ALLOW-CHAR is the universal instantiation and explicit biconditional restatement of EA. Its proof is immediate by the definition of universal quantification and the biconditional: EA directly supplies both directions for every `t`. The theorem is stated separately from EA to make the necessary-and-sufficient structure explicit and to provide a named target for the Lean 4 candidate in S3.

---

### 3.2 Decomposition into necessary and sufficient conditions

The biconditional T-ALLOW-CHAR decomposes into two directed implications, each of which is a separately statable claim.

---

#### 3.2.1 Sufficient condition

> **[GENERATED — UNVERIFIED]** **Theorem T-ALLOW-SUFF** *(Sufficiency)*
>
> For all `t : Transition`:
>
> ```
> GBP(t) ∧ BD(t) ∧ OC(t)  →  ALLOW(t)
> ```
>
> *Reading:* If all three predicates hold of `t`, then the evaluator returns `ALLOW` for `t`.

**Proof sketch (informal).** Assume `GBP(t) ∧ BD(t) ∧ OC(t)`. By the forward direction of EA, `ALLOW(t)` follows immediately. ∎

---

#### 3.2.2 Necessary condition

> **[GENERATED — UNVERIFIED]** **Theorem T-ALLOW-NECE** *(Necessity)*
>
> For all `t : Transition`:
>
> ```
> ALLOW(t)  →  GBP(t) ∧ BD(t) ∧ OC(t)
> ```
>
> *Reading:* If the evaluator returns `ALLOW` for `t`, then all three predicates must hold of `t`.

**Proof sketch (informal).** Assume `ALLOW(t)`. By the reverse direction of EA, `GBP(t) ∧ BD(t) ∧ OC(t)` follows immediately. ∎

---

#### 3.2.3 Conjunction of T-ALLOW-SUFF and T-ALLOW-NECE yields T-ALLOW-CHAR

> **[GENERATED — UNVERIFIED]** **Corollary C-EQUIV**
>
> T-ALLOW