# SV-MATH-001
## Necessary and Sufficient Conditions for ALLOW Gate Admissibility in the GCAT/BCAT Engine

---

## SECTION 1: ASSUMPTIONS AND CLAIM BOUNDARY

### 1.1 Stipulated Assumptions (not derived; accepted as engine specification)

**A1 (Engine Topology).** The GCAT/BCAT engine operates on a state space `Ω` that is a compact, connected, orientable Riemannian manifold with boundary `∂Ω`, equipped with a fixed metric `g` and measure `μ` derived from `g`.

**A2 (Gate Ontology).** An ALLOW gate `G` is a morphism in the engine's gate category `𝒢`, formally a measurable map `G: Ω → Ω` that may alter state trajectories. Gates are composed sequentially; the identity gate `Id` is always admissible.

**A3 (Boundary Semantics).** The geometric boundary `∂Ω` encodes hard semantic constraints of the engine (e.g., safety envelopes, resource bounds). Admissibility requires that no gate transport probability mass outside `Ω`.

**A4 (Divergence Measure).** The engine tracks a Kullback-Leibler–type divergence `D(ρ || π)` between current state distribution `ρ` and a reference distribution `π` (the engine's stationary or target distribution). Bounded divergence is a stipulated operational requirement.

**A5 (Ontological Consistency).** The engine maintains a coherence predicate `OC: 𝒢 → {⊤, ⊥}` defined externally. For this artifact, `OC(G) = ⊤` is taken to mean: `G` does not introduce contradictions into the engine's knowledge graph under its inference rules. The precise definition of `OC` is an **unresolved dependency** (see Section 6).

**A6 (GCAT/BCAT Specification).** The GCAT and BCAT engine specifications are treated as black-box axioms here. No source code or formal specification document was available to the author at artifact generation time. This is a **critical unresolved dependency**.

### 1.2 Generated Claims (produced by this artifact; not yet externally verified)

- The three conditions (geometric boundary preservation, bounded divergence, ontological consistency) are jointly necessary and sufficient for ALLOW gate admissibility, under the abstract model defined in Section 2.
- The Lean 4 candidate in Section 5 correctly encodes this theorem structurally.

### 1.3 Verified Claims

- **None.** No external compilation, engine test, or peer review has been performed. The Lean 4 candidate has **not been compiled**. No GCAT/BCAT engine run has been executed against this artifact.

### 1.4 Bounded Public Claim

> Under the abstract model of Sections 1–2, and conditional on Assumptions A1–A6, Theorem 3.1 holds by mathematical proof. Binding this result to any deployed GCAT/BCAT engine requires the evidence enumerated in Section 6.

---

## SECTION 2: DEFINITIONS

Let the following definitions be fixed for the remainder of this artifact.

**Definition 2.1 (State Space).** `(Ω, g, μ)` is a compact, connected, orientable Riemannian manifold with boundary, `∂Ω ≠ ∅`, `μ` the Riemannian volume measure. Write `Int(Ω) = Ω \ ∂Ω`.

**Definition 2.2 (Gate).** A gate `G ∈ 𝒢` is a Borel-measurable map `G: Ω → Ω`. The gate category `𝒢` has objects `{Ω}` and morphisms all admissible gates, composed by function composition.

**Definition 2.3 (State Distribution).** A state distribution is a Borel probability measure `ρ ∈ 𝒫(Ω)` absolutely continuous with respect to `μ`, with density also written `ρ: Ω → ℝ≥0`.

**Definition 2.4 (Reference Distribution).** Fix `π ∈ 𝒫(Ω)` with density `π: Ω → ℝ>0`, `π` bounded away from zero: `∃ε > 0, π(x) ≥ ε` for `μ`-a.e. `x ∈ Ω`.

**Definition 2.5 (KL Divergence).** For `ρ, π ∈ 𝒫(Ω)` with `ρ ≪ π`,

```
D_KL(ρ || π) := ∫_Ω ρ(x) log(ρ(x)/π(x)) dμ(x) ∈ [0, +∞].
```

**Definition 2.6 (Pushforward).** For gate `G` and distribution `ρ`, the pushforward `G_*ρ ∈ 𝒫(Ω)` is defined by `(G_*ρ)(A) = ρ(G⁻¹(A))` for all Borel `A ⊆ Ω`.

**Definition 2.7 (Geometric Boundary Preservation — GBP).** Gate `G` satisfies GBP if and only if:

```
G(Ω) ⊆ Ω     [i.e., G maps Ω into itself]
```

Since `G: Ω → Ω` by definition, this is automatically satisfied for the codomain; the non-trivial content is:

```
GBP(G) :⟺ ∀x ∈ ∂Ω,  G(x) ∈ Ω    (boundary not mapped outside)
           ∧ ∀ρ ∈ 𝒫(Ω),  G_*ρ ∈ 𝒫(Ω)   (distributions preserved on Ω)
           ∧ G is continuous on ∂Ω.
```

*Remark:* Because `G: Ω → Ω` is the type, the first two conjuncts are definitionally satisfied. The operative force of GBP is that `G` does not concentrate mass on `∂Ω` in a way that escapes `Ω`-support. In the abstract model, GBP reduces to: `G_*ρ ∈ 𝒫(Ω)` for all `ρ ∈ 𝒫(Ω)`. We adopt this as the formal definition.

**GBP(G):** `∀ρ ∈ 𝒫(Ω), G_*ρ ∈ 𝒫(Ω)` and `G` is Borel measurable.

*Note: Under Definition 2.2, GBP is satisfied by all gates in 𝒢 by type. The theorem's force therefore comes from conditions BD and OC. GBP is retained as an explicit condition because deployed engines may relax the codomain to a larger ambient space; see Section 6, Evidence E3.*

**Definition 2.8 (Bounded Divergence — BD).** Fix a threshold `Δ > 0` (engine parameter). Gate `G` satisfies BD at `ρ` if:

```
D_KL(G_*ρ || π) ≤ Δ.
```

Gate `G` satisfies **BD uniformly** if:

```
BD(G) :⟺ sup_{ρ ∈ 𝒫(Ω): D_KL(ρ||π) < ∞} D_KL(G_*ρ || π) ≤ Δ.
```

**Definition 2.9 (Ontological Consistency — OC).** Gate `G` satisfies OC if:

```
OC(G) = ⊤
```

where `OC: 𝒢 → {⊤, ⊥}` is the engine's coherence predicate (Assumption A5). We require `OC` to satisfy:

- **(OC-Id)** `OC(Id) = ⊤`.
- **(OC-Comp)** If `OC(G₁) = ⊤` and `OC(G₂) = ⊤` then `OC(G₁ ∘ G₂) = ⊤`.
- **(OC-Refusal)** If `OC(G) = ⊥` then `G` is not executable by the engine.

**Definition 2.10 (ALLOW Admissibility).** Gate `G ∈ 𝒢` is **ALLOW-admissible** (written `Adm(G)`) if and only if the engine's gate controller permits `G` for execution in the current state. Formally (this definition encodes what we will prove):

```
Adm(G) :⟺ [engine permits G]
```

The theorem characterizes `Adm(G)` in terms of GBP, BD, OC.

**Definition 2.11 (Joint Admissibility Condition — JAC).** Define:

```
JAC(G) :⟺ GBP(G) ∧ BD(G) ∧ OC(G).
```

---

## SECTION 3: THEOREM STATEMENT

**Theorem 3.1 (Necessary and Sufficient Conditions for ALLOW Admissibility).**

*Under Assumptions A1–A6 and Definitions 2.1–2.11:*

```
∀G ∈ 𝒢,   Adm(G)  ⟺  JAC(G)
```

*That is, GBP, BD, and OC are jointly necessary and sufficient for ALLOW gate admissibility.*

**Corollary 3.2 (Completeness of the Condition Set).** The conditions GBP, BD, OC are jointly complete: no proper subset is sufficient, and no additional condition is necessary beyond JAC.

**Corollary 3.3 (Closure Under Composition).** If `Adm(G₁)` and `Adm(G₂)`, then under mild additional hypotheses (Lemma 4.6), `Adm(G₁ ∘ G₂)`.

---

## SECTION 4: MATHEMATICAL PROOF

### 4.1 Proof Strategy

We prove Theorem 3.1 by establishing:
- **(⇒) Necessity:** `Adm(G) ⟹ GBP(G) ∧ BD(G) ∧ OC(G)`.
- **(⇐) Sufficiency:** `GBP(G) ∧ BD(G) ∧ OC(G) ⟹ Adm(G)`.
- **Corollary 3.2:** Minimality of the condition set.
- **Corollary 3.3:** Closure under composition.

We then address joint completeness.

---

### 4.2 Proof of Necessity (⇒)

**Claim:** `Adm(G) ⟹ GBP(G)`.

*Proof.* Suppose `Adm(G)`. By Assumption A3, the engine only permits gates that do not transport probability mass outside `Ω`. Since `G: Ω → Ω` is the type constraint and the engine enforces this at the controller level, `G_*ρ ∈ 𝒫(Ω)` for all `ρ ∈ 𝒫(Ω)`. By Definition 2.7, `GBP(G)`. ∎

**Claim:** `Adm(G) ⟹ BD(G)`.

*Proof.* Suppose `Adm(G)`. We argue by contrapositive. Suppose `BD(G)` fails: there exists `ρ₀ ∈ 𝒫(Ω)` with `D_KL(ρ₀ || π) < ∞` and `D_KL(G_*ρ₀ || π) > Δ`.

By Assumption A4, the engine tracks divergence and enforces the bound `Δ`. If applying `G` to distribution `ρ₀` produces `G_*ρ₀` with `D_KL(G_*ρ₀ || π) > Δ`, the engine controller detects this and withholds ALLOW status. Therefore `G` is not permitted, contradicting `Adm(G)`. Hence `BD(G)`. ∎

**Claim:** `Adm(G) ⟹ OC(G)`.

*Proof.* Suppose `Adm(G)`. By (OC-Refusal) in Definition 2.9, if `OC(G) = ⊥` then `G` is not executable. Since `Adm(G)` implies `G` is permitted for execution, we must have `OC(G) = ⊤`. ∎

**Conclusion of (⇒):** `Adm(G) ⟹ GBP(G) ∧ BD(G) ∧ OC(G)`. ∎

---

### 4.3 Proof of Sufficiency (⇐)

**Claim:** `GBP(G) ∧ BD(G) ∧ OC(G) ⟹ Adm(G)`.

*Proof.*

We must show that any `G` satisfying all three conditions is permitted by the engine controller. We show each controller check passes.

**Step 1: Boundary Check.**

Assume `GBP(G)`. The engine's boundary validator checks `G_*ρ ∈ 𝒫(Ω)` for the current distribution `ρ`. By `GBP(G)`, this holds for all `ρ ∈ 𝒫(Ω)`, hence the boundary check passes.

**Step 2: Divergence Check.**

Assume `BD(G)`: `sup_ρ D_KL(G_*ρ || π) ≤ Δ`. The engine's divergence monitor computes (or bounds) `D_KL(G_*ρ_current || π)`. Since `BD(G)` holds uniformly, in particular for `ρ = ρ_current`, we have `D_KL(G_*ρ_current || π) ≤ Δ`. The divergence check passes.

**Step 3: Ontological Check.**

Assume `OC(G) = ⊤`. By (OC-Refusal) contrapositively, since `OC(G) = ⊤`, the engine does not block `G` on consistency grounds. The ontological check passes.

**Step 4: No Further Checks (Completeness Assertion).**

We assert (as part of the abstract engine model, justified by Assumption A2 and the completeness claim of Corollary 3.2) that GBP, BD, OC constitute the complete list of controller checks. Under this assertion, all checks pass, and the controller issues ALLOW status. Therefore `Adm(G)`. ∎

*Remark on Step 4:* The assertion that no further checks exist is **model-dependent**. It is justified within the abstract model by the minimality argument of Corollary 3.2 but requires empirical verification against the actual GCAT/BCAT engine (see Evidence E3, Section 6).

---

### 4.4 Proof of Corollary 3.2 (Joint Completeness — Minimality)

We show no proper subset of {GBP, BD, OC} is sufficient, and the set is complete (no condition is redundant from necessity).

**GBP is independently necessary.**

*Counterexample without GBP:* Let `Ω' ⊃ Ω` be a larger ambient space. Define `G'` mapping some `x ∈ Ω` to `y ∉ Ω`. Then `G'` satisfies `BD` (if the divergence is computed on `Ω` and `G'` pushes little mass outside) and `OC(G') = ⊤` (if the knowledge graph does not encode boundary constraints). Yet `G'` violates A3 and is not admissible. So `BD ∧ OC` without GBP is insufficient. ∎

**BD is independently necessary.**

*Counterexample without BD:* Let `G_e` be the entropy-concentrating map: `G_e` pushes all mass to a single point `x₀ ∈ Int(Ω)`. Then `GBP(G_e)` holds (all mass stays in `Ω`), and if `OC(G_e) = ⊤`, yet `D_KL(G_e * ρ || π) → +∞` as the concentration sharpens. This violates A4. So `GBP ∧ OC` without BD is insufficient. ∎

**OC is independently necessary.**

*Counterexample without OC:* Let `G_c` be a gate that satisfies `GBP` and `BD` but introduces a contradiction into the knowledge graph (e.g., simultaneously asserts `P` and `¬P`). By (OC-Refusal), `G_c` is blocked. So `GBP ∧ BD` without OC is insufficient. ∎

**No redundancy among conditions.** Each condition rules out a class of gates not ruled out by the conjunction of the other two. Hence no condition is redundant. The set {GBP, BD, OC} is minimal sufficient and jointly complete given the abstract engine model. ∎

---

### 4.5 Proof of Corollary 3.3 (Closure Under Composition)

**Lemma 4.4 (GBP Closed Under Composition).** If `GBP(G₁)` and `GBP(G₂)`, then `GBP(G₁ ∘ G₂)`.

*Proof.* `(G₁ ∘ G₂)_*ρ = G₁_*(G₂_*ρ)`. Since `GBP(G₂)`, `G₂_*ρ ∈ 𝒫(Ω)`. Since `GBP(G₁)`, `G₁_*(G₂_*ρ) ∈ 𝒫(Ω)`. ∎

**Lemma 4.5 (OC Closed Under Composition).** If `OC(G₁) = ⊤` and `OC(G₂) = ⊤`, then `OC(G₁ ∘ G₂) = ⊤`.

*Proof.* By (OC-Comp) in Definition 2.9. ∎

**Lemma 4.6 (BD Under Composition — with hypothesis).** Suppose `BD(G₁)` and `BD(G₂)` with threshold `Δ`. In general, `BD(G₁ ∘ G₂)` with the *same* threshold `Δ` need not hold. However, if additionally:

```
(H-comp)  D_KL(G₁_* ρ' || π) ≤ Δ  for all ρ' with D_KL(ρ' || π) ≤ Δ,
```

then `BD(G₁ ∘ G₂)` holds with threshold `Δ`.

*Proof.* Let `ρ` satisfy `D_KL(ρ || π) < ∞`. By `BD(G₂)`, `D_KL(G₂_*ρ || π) ≤ Δ`. Setting `ρ' = G₂_*ρ` and applying (H-comp), `D_KL(G₁_*(G₂_*ρ) || π) ≤ Δ`. Hence `BD(G₁ ∘ G₂)`. ∎

**Proof of Corollary 3.3.** Under (H-comp), Lemmas 4.4, 4.5, 4.6 give `JAC(G₁ ∘ G₂)`, hence `Adm(G₁ ∘ G₂)` by Theorem 3.1. ∎

---

### 4.6 On Joint Completeness of the Condition Set

The claim that GBP, BD, OC are *jointly* complete means:

1. **Soundness:** `JAC(G) ⟹ Adm(G)` — proved in Section 4.3.
2. **Completeness:** `Adm(G) ⟹ JAC(G)` — proved in Section 4.2.
3. **Minimality:** No proper subset of {GBP, BD, OC} is sufficient — proved in Section 4.4.

These three together establish that the characterization is exact within the abstract model. The caveat is that completeness (item 2) relies on the exhaustiveness assertion of Step 4 in Section 4.3, which is a modeling assumption, not a derived theorem. In a fully formal treatment, one would need to enumerate all engine controller checks axiomatically. This is an **unresolved dependency** (see Evidence E3).

---

## SECTION 5: LEAN 4 CANDIDATE

**IMPORTANT DISCLAIMER:** The following Lean 4 code has **not been compiled or type-checked**. It is a proof candidate — a structured encoding of the mathematical argument — intended for compilation verification. It may contain syntax errors, universe-level issues, or incomplete `sorry`-free proofs. Unproven lemmas are marked `sorry` explicitly.

```lean
/-!
# SV-MATH-001: ALLOW Gate Admissibility in GCAT/BCAT Engine
## Lean 4 Proof Candidate — NOT COMPILED

This file encodes Theorem 3.1 and supporting lemmas.
All `sorry` marks indicate genuine proof obligations.
-/

import Mathlib.MeasureTheory.Measure.MeasureSpace
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Topology.MetricSpace.Basic

open MeasureTheory ENNReal

/-! ## Universe and Type Setup -/

/-- Abstract state space; in the theorem, this is a compact Riemannian manifold.
    We abstract over the geometric structure here. -/
variable {Ω : Type*} [MeasurableSpace Ω] [TopologicalSpace Ω]

/-- Reference measure (Riemannian volume) -/
variable (μ : Measure Ω) [IsProbabilityMeasure μ]

/-- Reference distribution π, bounded below -/
variable (π : Measure Ω) [IsProbabilityMeasure π]

/-! ## Definition 2.6: KL Divergence (abstract) -/

/-- KL divergence of ρ from π, returning an extended nonneg real -/
noncomputable def klDiv (ρ π : Measure Ω) : ℝ≥0∞ :=
  ∫⁻ x, ENNReal.ofReal ((ρ.rnDeriv π x).toReal *
    Real.log ((ρ.rnDeriv π x).toReal)) ∂π

/-! ## Gate Definition -/

/-- A gate is a measurable map Ω → Ω -/
structure Gate (Ω : Type*) [MeasurableSpace Ω] where
  map     : Ω → Ω
  measurable : Measurable map

/-- Pushforward of a measure under a gate -/
noncomputable def Gate.pushforward (G : Gate Ω) (ρ : Measure Ω) : Measure Ω :=
  ρ.map G.map

/-! ## Definition 2.7: Geometric Boundary Preservation -/

/-- GBP: gate preserves probability measures on Ω.
    In the abstract setting (no ambient space), this is vacuous by type.
    We encode it as the pushforward being a probability measure. -/
def GBP (G : Gate Ω) : Prop :=
  ∀ (ρ : Measure Ω), IsProbabilityMeasure ρ →
    IsProbabilityMeasure (G.pushforward ρ)

/-! ## Definition 2.8: Bounded Divergence -/

/-- BD: gate does not increase KL divergence beyond Δ (uniformly) -/
def BD (G : Gate Ω) (π : Measure Ω) (Δ : ℝ≥0∞) : Prop :=
  ∀ (ρ : Measure Ω), IsProbabilityMeasure ρ → klDiv ρ π < ⊤ →
    klDiv (G.pushforward ρ) π ≤ Δ

/-! ## Definition 2.9: Ontological Consistency -/

/-- OC is given as an abstract predicate satisfying three axioms -/
class OntologicalConsistency (Gate : Type*) where
  oc         : Gate → Prop
  oc_id      : ∀ (id_gate : Gate), oc id_gate  -- simplified; needs identity gate
  oc_comp    : ∀ (G₁ G₂ : Gate), oc G₁ → oc G₂ → oc G₁  -- placeholder; comp not yet defined
  oc_refusal : ∀ (G : Gate), ¬oc G → ¬True  -- placeholder for "not executable"

/-- For our proof, OC is an opaque predicate with axioms -/
variable (OC : Gate Ω → Prop)
variable (OC_id   : OC ⟨id, measurable_id⟩)
variable (OC_comp : ∀ G₁ G₂ : Gate Ω, OC G₁ → OC G₂ →
                    OC ⟨G₁.map ∘ G₂.map, G₁.measurable.comp G₂.measurable⟩)
variable (OC_refusal : ∀ G : Gate Ω, ¬OC G → ¬True)
  -- OC_refusal encodes: ¬OC G → gate not executable; here ¬True is a placeholder

/-! ## Definition 2.11: JAC -/

def JAC (G : Gate Ω) (π : Measure Ω) (Δ : ℝ≥0∞) (OC : Gate Ω → Prop) : Prop :=
  GBP G ∧ BD G π Δ ∧ OC G

/-! ## Admissibility (axiomatized to match engine spec) -/

/-- Adm is the engine's admissibility predicate; axiomatized here -/
variable (Adm : Gate Ω → Prop)

/-- Engine Axiom 1: Admissibility implies GBP -/
variable (engine_GBP : ∀ G : Gate Ω, Adm G → GBP G)

/-- Engine Axiom 2: Admissibility implies BD -/
variable (engine_BD : ∀ G : Gate Ω, Adm G → BD G π Δ)

/-- Engine Axiom 3: Admissibility implies OC -/
variable (engine_OC : ∀ G : Gate Ω, Adm G → OC G)

/-- Engine Axiom 4: JAC is sufficient for Adm (completeness of controller checks) -/
variable (engine_sufficiency : ∀ G : Gate Ω, JAC G π Δ OC → Adm G)

variable (Δ : ℝ≥0∞)

/-! ## Theorem 3.1: Necessary and Sufficient Conditions -/

theorem allow_gate_admissibility_iff
    (G : Gate Ω)
    (engine_GBP     : ∀ G : Gate Ω, Adm G → GBP G)
    (engine_BD      : ∀ G : Gate Ω, Adm G → BD G π Δ)
    (engine_OC      : ∀ G : Gate Ω, Adm G → OC G)
    (engine_suff    : ∀ G : Gate Ω, JAC G π Δ OC → Adm G) :
    Adm G ↔ JAC G π Δ OC := by
  constructor
  · -- (⇒) Necessity
    intro h_adm
    refine ⟨?_, ?_, ?_⟩
    · exact engine_GBP G h_adm
    · exact engine_BD G h_adm
    · exact engine_OC G h_adm
  · -- (⇐) Sufficiency
    intro h_jac
    exact engine_suff G h_jac

/-! ## GBP closure under composition -/

lemma gbp_comp (G₁ G₂ : Gate Ω)
    (h₁ : GBP G₁) (h₂ : GBP G₂) :
    GBP ⟨G₁.map ∘ G₂.map, G₁.measurable.comp G₂.measurable⟩ := by
  intro ρ hρ
  simp only [GBP, Gate.pushforward, Gate.map] at *
  -- (G₁ ∘ G₂)_* ρ = G₁_* (G₂_* ρ)
  rw [Measure.map_map G₁.measurable G₂.measurable]
  apply h₁
  exact h₂ ρ hρ

/-! ## BD closure under composition (with hypothesis H-comp) -/

lemma bd_comp (G₁ G₂ : Gate Ω)
    (h₁ : BD G₁ π Δ) (h₂ : BD G₂ π Δ)
    (H_comp : ∀ ρ' : Measure Ω, IsProbabilityMeasure ρ' →
              klDiv ρ' π ≤ Δ → klDiv (G₁.pushforward ρ') π ≤ Δ) :
    BD ⟨G₁.map ∘ G₂.map, G₁.measurable.comp G₂.measurable⟩ π Δ := by
  intro ρ hρ hfin
  simp only [BD, Gate.pushforward, Gate.map] at *
  rw [Measure.map_map G₁.measurable G₂.measurable]
  apply H_comp
  · exact h₂ ρ hρ hfin |>.elim (fun h => sorry) -- needs: pushforward IsProbabilityMeasure
    -- TODO: show G₂.pushforward ρ is a probability measure
  · exact h₂ ρ hρ hfin

/-! ## Corollary 3.3: Composition closure -/

theorem adm_comp (G₁ G₂ : Gate Ω)
    (h₁ : Adm G₁) (h₂ : Adm G₂)
    (engine_GBP  : ∀ G : Gate Ω, Adm G → GBP G)
    (engine_BD   : ∀ G : Gate Ω, Adm G → BD G π Δ)
    (engine_OC   : ∀ G : Gate Ω, Adm G → OC G)
    (engine_suff : ∀ G : Gate Ω, JAC G π Δ OC → Adm G)
    (OC_comp     : ∀ G₁ G₂ : Gate Ω, OC G₁ → OC G₂