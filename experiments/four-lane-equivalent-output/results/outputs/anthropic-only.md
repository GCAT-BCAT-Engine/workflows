# SV-MATH-001: ALLOW Gate Admissibility in the GCAT/BCAT Engine

---

## SECTION 1: ASSUMPTIONS AND CLAIM BOUNDARY

**Document Identifier:** SV-MATH-001
**Version:** 1.0
**Status:** Mathematical Artifact — Formal Draft

### 1.1 Foundational Assumptions

**A1 (Set-Theoretic Foundation).** We work within ZFC extended with a Grothendieck universe U. All constructions are assumed to be U-small unless stated otherwise.

**A2 (GCAT/BCAT Engine Model).** The GCAT/BCAT engine is modeled as a concrete operational structure (defined in Section 2). The term "engine" refers specifically to this mathematical model, not to any particular software implementation. Properties of implementations are not derived here.

**A3 (Gate Abstraction).** An ALLOW gate is an abstract computational gate in the engine's control-flow graph. Its behavior is fully characterized by the triple (φ, D, Ω) defined in Section 2. No empirical or physical interpretation is assumed.

**A4 (Metric Structure).** All topological spaces considered are assumed to be Hausdorff and second-countable. Geometric boundary is taken in the sense of topological manifold-with-boundary theory.

**A5 (Divergence Boundedness).** Divergence is measured via a fixed reference measure μ (Borel, σ-finite) on the state space. Bounded divergence is Dₖₗ-boundedness unless otherwise specified.

**A6 (Ontological Consistency Model).** "Ontological consistency" is given a precise logical meaning in Definition 2.7 as a local consistency predicate on the type-theoretic interpretation of gate output. This is the *only* meaning used in proofs.

### 1.2 Claim Boundary

**This artifact establishes:**
- Precise definitions of the three proposed admissibility conditions.
- A theorem characterizing ALLOW gate admissibility as equivalent to the conjunction of three conditions.
- A proof of necessity and sufficiency of those conditions jointly.
- A Lean 4 proof candidate formalizing the core logical structure.

**This artifact does NOT establish:**
- Any claim about runtime behavior of systems outside the defined model.
- Any claim about physical or biological systems.
- Completeness in any proof-theoretic sense beyond what is explicitly stated.
- That the Lean 4 candidate compiles without modification; it is a proof *candidate* requiring toolchain verification.

**Open Questions Acknowledged:**
- Whether the chosen divergence measure (Dₖₗ) is the uniquely correct one for all applications of the model.
- Whether the ontological consistency predicate fully captures informal intended meanings of "consistency" in all contexts where GCAT/BCAT might be deployed.

---

## SECTION 2: DEFINITIONS

### 2.1 State Space

**Definition 2.1 (State Space).** The *state space* is a tuple S = (X, τ, μ, ∂X) where:
- X is a topological manifold-with-boundary of dimension n ≥ 1,
- τ is the manifold topology on X,
- μ is a Borel probability measure on (X, τ),
- ∂X ⊆ X is the topological boundary of X (as a manifold-with-boundary),
- int(X) = X \ ∂X is the interior.

We denote by M(X) the set of all Borel probability measures on X, equipped with the weak-* topology.

### 2.2 GCAT/BCAT Engine

**Definition 2.2 (GCAT/BCAT Engine).** A *GCAT/BCAT engine* E is a tuple:

$$\mathcal{E} = (S, \mathcal{G}, \mathcal{T}, \mathcal{C}, \mathcal{F})$$

where:
- S = (X, τ, μ, ∂X) is a state space (Definition 2.1),
- G is a finite directed acyclic graph (DAG) called the *control-flow graph*,
- T : V(G) → {ALLOW, DENY, TRANSFORM, BRANCH} is a gate-type labeling,
- C : V(G) → Pred(S) assigns a *context predicate* to each gate vertex, where Pred(S) is the set of measurable predicates on X,
- F : E(G) → (M(X) → M(X)) assigns to each directed edge a *state-transformer function*.

### 2.3 ALLOW Gate

**Definition 2.3 (ALLOW Gate).** An *ALLOW gate* in engine E is a vertex v ∈ V(G) with T(v) = ALLOW. Its *gate characterization triple* is (φ_v, D_v, Ω_v) where:
- φ_v : X → X is the *flow map* of the gate, assumed to be a Borel-measurable function,
- D_v : M(X) → [0, ∞] is the *gate divergence functional*, defined by D_v(ν) = Dₖₗ(φ_v∗ν ‖ μ) where φ_v∗ν denotes the pushforward measure,
- Ω_v ⊆ X is the *gate domain*, a Borel-measurable subset of X with μ(Ω_v) > 0.

### 2.4 Geometric Boundary Preservation (GBP)

**Definition 2.4 (Geometric Boundary Preservation).** An ALLOW gate v with flow map φ_v satisfies *Geometric Boundary Preservation* (GBP) if and only if:

$$\phi_v(\partial X) \subseteq \partial X \quad \text{and} \quad \phi_v(\operatorname{int}(X)) \subseteq \operatorname{int}(X)$$

That is, φ_v maps boundary points to boundary points and interior points to interior points.

Equivalently, GBP holds iff φ_v is a *stratum-preserving* map with respect to the stratification {int(X), ∂X}.

**Remark 2.4.1.** GBP is strictly about the topological-geometric structure of X. It does not require φ_v to be a homeomorphism, only measurability and stratum-preservation.

### 2.5 Bounded Divergence (BD)

**Definition 2.5 (Bounded Divergence).** An ALLOW gate v satisfies *Bounded Divergence* (BD) with constant K ∈ [0,∞) if and only if:

$$D_v(\mu) = D_{\mathrm{KL}}(\phi_{v*}\mu \| \mu) \leq K < \infty$$

We say BD holds (without specifying K) if there exists some finite K ≥ 0 such that the above holds.

**Remark 2.5.1.** BD ensures that the gate's action does not make the output distribution arbitrarily singular with respect to the reference measure. When K = 0, φ_v∗μ = μ almost everywhere (μ-invariance).

**Definition 2.5.2 (Uniform Bounded Divergence).** An engine E satisfies *Uniform Bounded Divergence* (UBD) if there exists K < ∞ such that every ALLOW gate in E satisfies BD with the same constant K.

### 2.6 Ontological Consistency (OC)

**Definition 2.6 (Type-Theoretic Output Interpretation).** Fix a dependent type theory T (e.g., Martin-Löf type theory). Each gate v has an associated *output type* τ_out(v) ∈ Type(T) derived from the gate's semantic annotation. A *gate output* is a term t : τ_out(v).

**Definition 2.7 (Ontological Consistency).** An ALLOW gate v satisfies *Ontological Consistency* (OC) if and only if the following two conditions hold:

**(OC-1) Type Safety:** For every input state x ∈ Ω_v, the output φ_v(x) yields a well-typed term under the type interpretation, i.e., φ_v(x) ∈ Ω_{T(v)} where Ω_{T(v)} is the semantic domain of τ_out(v).

**(OC-2) Categorical Coherence:** The diagram of gate semantics commutes in the interpretation category C(E): for every morphism f : v → v' in the engine's semantic category, the naturality square for φ_v and φ_{v'} commutes up to the contextual equivalence relation ≃_E.

**Remark 2.7.1.** OC is a *syntactic-semantic bridge condition*. It ensures that what the gate computes is consistent with what the type system expects. The categorical coherence condition (OC-2) generalizes across composed gate sequences.

**Remark 2.7.2.** OC is defined relative to the engine's specific type annotation and semantic category C(E). A gate may satisfy OC in one engine but not when transplanted to another engine with different annotations.

### 2.7 ALLOW Gate Admissibility

**Definition 2.8 (ALLOW Gate Admissibility).** An ALLOW gate v in engine E is *admissible* if it satisfies the following *Admissibility Conditions*:

**(AC-1)** The gate satisfies GBP (Definition 2.4).
**(AC-2)** The gate satisfies BD (Definition 2.5).
**(AC-3)** The gate satisfies OC (Definition 2.7).

We write Adm(v) to mean that gate v is admissible, i.e., Adm(v) ⟺ GBP(v) ∧ BD(v) ∧ OC(v).

**Definition 2.9 (Engine Admissibility).** Engine E is *admissible* if every ALLOW gate v ∈ V(G) with T(v) = ALLOW satisfies Adm(v).

### 2.8 Projection Maps

**Definition 2.10.** For a gate v, define projection maps:

$$\pi_{\mathrm{geo}}(v) = \phi_v \upharpoonright \partial X \quad \text{(boundary restriction)}$$
$$\pi_{\mathrm{div}}(v) = D_v(\mu) \quad \text{(divergence value at reference measure)}$$
$$\pi_{\mathrm{ont}}(v) = (\tau_{\mathrm{out}}(v), [\phi_v]_{\simeq_E}) \quad \text{(type-semantic pair)}$$

These projections are used in the proof to analyze each condition independently.

---

## SECTION 3: THEOREM STATEMENT

### 3.1 Main Theorem

**Theorem 3.1 (Necessary and Sufficient Conditions for ALLOW Gate Admissibility).**

*Let E = (S, G, T, C, F) be a GCAT/BCAT engine (Definition 2.2) and let v ∈ V(G) be an ALLOW gate (Definition 2.3). Then:*

$$\mathrm{Adm}(v) \iff \mathrm{GBP}(v) \land \mathrm{BD}(v) \land \mathrm{OC}(v)$$

*That is, the three conditions — Geometric Boundary Preservation, Bounded Divergence, and Ontological Consistency — are jointly necessary and sufficient for ALLOW gate admissibility.*

### 3.2 Joint Completeness Claim

**Corollary 3.2 (Joint Completeness).** The condition set {GBP, BD, OC} is *jointly complete* for admissibility in the sense that:

1. **(Sufficiency)** GBP(v) ∧ BD(v) ∧ OC(v) → Adm(v).
2. **(Necessity)** Adm(v) → GBP(v) ∧ BD(v) ∧ OC(v).
3. **(Independence)** Each condition is logically independent of the conjunction of the other two: for each condition C_i ∈ {GBP, BD, OC}, there exists a gate satisfying the other two conditions but not C_i.

### 3.3 Structural Lemmas Required

The following lemmas are required for the proof:

**Lemma 3.3 (GBP Measurability Compatibility).** If φ_v satisfies GBP, then φ_v∗μ is absolutely continuous with respect to μ restricted to int(X) ∪ ∂X, respectively.

**Lemma 3.4 (BD Implies Absolute Continuity).** If BD(v) holds (with finite K), then φ_v∗μ ≪ μ (absolute continuity of pushforward with respect to reference measure).

**Lemma 3.5 (OC Closure Under Composition).** If v, v' are consecutive ALLOW gates both satisfying OC, then their composition v' ∘ v satisfies OC.

**Lemma 3.6 (Independence Witnesses).** For each i ∈ {1, 2, 3}, there exists an explicit gate construction satisfying conditions {C_j : j ≠ i} but not C_i.

---

## SECTION 4: MATHEMATICAL PROOF

### 4.1 Proof Strategy

Theorem 3.1 is established by proving:
- (→) Necessity: Adm(v) implies each of GBP(v), BD(v), OC(v) separately.
- (←) Sufficiency: GBP(v) ∧ BD(v) ∧ OC(v) implies Adm(v).
- Corollary 3.2(3): Independence of each condition.

Since Adm(v) is defined as GBP(v) ∧ BD(v) ∧ OC(v) (Definition 2.8), the biconditional is definitionally true. The substantive content of the theorem lies in:
(a) Establishing that the definition is *well-posed* (i.e., the three conditions are mutually consistent and the definition is non-vacuous),
(b) Proving the independence of the three conditions (Corollary 3.2(3)), which is the non-trivial part,
(c) Establishing the structural lemmas, which reveal the mathematical content underlying each condition.

**Note on Definitional Biconditional.** We acknowledge explicitly: because Adm(v) is defined as the conjunction, the biconditional Adm(v) ⟺ GBP(v) ∧ BD(v) ∧ OC(v) is by definition. The theorem's non-trivial content is therefore: (i) the conditions are independently satisfiable, (ii) each condition captures a distinct geometric/analytic/logical constraint, and (iii) the set is complete in the sense that no further conditions are derivable from the engine structure that are not implied by the three.

### 4.2 Proof of Structural Lemmas

---

**Proof of Lemma 3.3 (GBP Measurability Compatibility).**

*Claim:* If φ_v satisfies GBP, then φ_v∗μ restricted to int(X) equals φ_v∗(μ|_{int(X)}) and similarly for ∂X.

*Proof.* Let A ⊆ int(X) be Borel measurable. Then:

$$(\phi_{v*}\mu)(A) = \mu(\phi_v^{-1}(A))$$

Since φ_v(int(X)) ⊆ int(X) by GBP, we have φ_v⁻¹(A) ⊆ int(X) for any A ⊆ int(X). Therefore:

$$\mu(\phi_v^{-1}(A)) = \mu(\phi_v^{-1}(A) \cap \operatorname{int}(X)) = \mu|_{\operatorname{int}(X)}(\phi_v^{-1}(A))$$

Similarly, for A ⊆ ∂X: since φ_v(∂X) ⊆ ∂X, we have φ_v⁻¹(A) ⊆ ∂X for A ⊆ ∂X, so:

$$(\phi_{v*}\mu)(A) = \mu(\phi_v^{-1}(A) \cap \partial X) = \mu|_{\partial X}(\phi_v^{-1}(A))$$

This establishes that the pushforward respects the stratum decomposition. □

---

**Proof of Lemma 3.4 (BD Implies Absolute Continuity).**

*Claim:* If D_v(μ) = Dₖₗ(φ_v∗μ ‖ μ) < ∞, then φ_v∗μ ≪ μ.

*Proof.* Recall that for measures ν, μ on a measurable space:

$$D_{\mathrm{KL}}(\nu \| \mu) = \int \log\frac{d\nu}{d\mu} d\nu$$

when ν ≪ μ (with the Radon-Nikodym derivative existing), and Dₖₗ(ν ‖ μ) = +∞ when ν is not absolutely continuous with respect to μ (by the standard convention in information theory).

Therefore: if Dₖₗ(φ_v∗μ ‖ μ) = D_v(μ) ≤ K < ∞, then by contrapositive, φ_v∗μ ≪ μ. □

---

**Proof of Lemma 3.5 (OC Closure Under Composition).**

*Claim:* If v and v' are consecutive ALLOW gates both satisfying OC, then their composition (as a composite gate v'∘v) satisfies OC.

*Proof.*

**Part 1 (Type Safety under Composition).**

Suppose v satisfies OC-1: for all x ∈ Ω_v, φ_v(x) ∈ Ω_{T(v)}.
Suppose v' satisfies OC-1: for all x' ∈ Ω_{v'}, φ_{v'}(x') ∈ Ω_{T(v')}.

For the composite gate w = v' ∘ v, the flow map is φ_w = φ_{v'} ∘ φ_v and the domain is Ω_w = Ω_v ∩ φ_v⁻¹(Ω_{v'}).

For x ∈ Ω_w: φ_v(x) ∈ Ω_{T(v)} (by OC-1 of v). Since v' follows v in the DAG and v satisfies OC, the output type T(v) is the input type of v'. By the type annotation consistency of E (part of the engine's well-formedness), Ω_{T(v)} ⊆ Ω_{v'}. Therefore φ_v(x) ∈ Ω_{v'}, and then φ_{v'}(φ_v(x)) ∈ Ω_{T(v')} by OC-1 of v'.

Hence φ_w(x) = φ_{v'}(φ_v(x)) ∈ Ω_{T(v')} = Ω_{T(w)}, establishing OC-1 for w.

**Part 2 (Categorical Coherence under Composition).**

Let f: v → v' be a morphism in C(E). By OC-2 of v, the naturality square for φ_v commutes up to ≃_E. By OC-2 of v', the naturality square for φ_{v'} commutes up to ≃_E. Composing these squares horizontally in C(E), the composite square for φ_w = φ_{v'} ∘ φ_v commutes up to ≃_E (since ≃_E is a congruence relation closed under horizontal composition of natural transformations).

Therefore w satisfies OC-2. □

---

**Proof of Lemma 3.6 (Independence Witnesses).**

We construct explicit gate configurations.

**Witness W1 (BD ∧ OC but ¬GBP):**

Let X = [0,1] (the closed unit interval, with ∂X = {0,1} and int(X) = (0,1)).
Let μ = Lebesgue measure on [0,1].
Define φ_v : [0,1] → [0,1] by φ_v(x) = 1/2 (constant map).

- *¬GBP:* φ_v(0) = 1/2 ∈ int(X), so boundary point 0 maps to interior. GBP fails. ✓
- *BD:* φ_v∗μ = δ_{1/2} (Dirac mass at 1/2). Then Dₖₗ(δ_{1/2} ‖ μ) = +∞ since δ_{1/2} ⋪ μ.

*Correction:* We need to refine W1. The constant map to an interior point fails BD. Instead:

Let φ_v(x) = min(x + ε, 1) for small ε > 0, which is Lebesgue measure-preserving on most of int(X) but maps points near 1 to the boundary incorrectly (still ¬GBP near boundaries).

More carefully: Let φ_v : [0,1] → [0,1] by φ_v(x) = sin(πx/2). Then:
- φ_v(0) = 0 ∈ ∂X ✓ but φ_v(1) = 1 ∈ ∂X ✓.
- Actually this preserves boundary. We need ¬GBP.

Let φ_v(x) = x²/2 + 1/4. Then φ_v(0) = 1/4 ∈ int(X) so ¬GBP for the boundary point 0.
φ_v∗μ is absolutely continuous w.r.t. μ (since φ_v is differentiable with φ'_v(x) = x > 0 a.e.), so Dₖₗ(φ_v∗μ ‖ μ) < ∞ by standard arguments (the Radon-Nikodym derivative is the inverse of the Jacobian).

Explicitly: φ_v maps [0,1] → [1/4, 3/4] ⊂ int(X), so φ_v∗μ = (1/φ'_v ∘ φ_v⁻¹) · μ|_{[1/4,3/4]} which is absolutely continuous, and:

$$D_{\mathrm{KL}}(\phi_{v*}\mu \| \mu) = \int_{1/4}^{3/4} \log\left(\frac{d\phi_{v*}\mu}{d\mu}\right) d\phi_{v*}\mu < \infty$$

since the Radon-Nikodym derivative is bounded and bounded away from zero on [1/4, 3/4].

OC: Define the type annotation for this gate as τ_out(v) = [1/4, 3/4] (a subtype of X). Then OC-1 holds since φ_v maps all of [0,1] into [1/4, 3/4]. OC-2 holds trivially (the coherence diagram commutes since there are no downstream gates interfering with this type).

**Conclusion:** W1 = φ_v(x) = x²/2 + 1/4 satisfies BD, OC, but not GBP. ✓

---

**Witness W2 (GBP ∧ OC but ¬BD):**

Let X = [0,1], μ = Lebesgue measure.
Define φ_v : [0,1] → [0,1] by:

$$\phi_v(x) = \begin{cases} 0 & x = 0 \\ 1 & x = 1 \\ \sin^2(1/(x(1-x))) \cdot (1 - \mathbf{1}_{\{0,1\}}(x)) & x \in (0,1) \end{cases}$$

Actually, we need φ_v∗μ to not be absolutely continuous with respect to μ, but we also need GBP. A cleaner construction:

Let f_n : [0,1] → [0,1] be a sequence of measure-preserving boundary-preserving maps that concentrate mass. Instead, construct:

Let φ_v(x) = Cantor function (Devil's staircase) composed with a boundary map.

More directly: Let X = [0,1]², so ∂X is the topological boundary of the square. Define φ_v on X such that GBP holds (it maps the square's boundary to itself and interior to interior). But make the pushforward φ_v∗μ singular with respect to μ by concentrating mass onto a set of lower dimension intersected with int(X).

Precise construction: Let X = [0,1] with ∂X = {0,1}. Let C ⊂ (0,1) be the Cantor set (a closed nowhere dense subset of (0,1) with Lebesgue measure 0). Define:

$$\phi_v(x) = \begin{cases} 0 & x = 0 \\ 1 & x = 1 \\ F_C(x) \cdot \frac{1}{2} + \frac{1}{4} & x \in (0,1) \end{cases}$$

where F_C is the Cantor function (which maps (0,1) to [0,1] and is constant on the complement of C). Then φ_v maps (0,1) → (1/4, 3/4) ⊂ int(X), so GBP holds. The pushforward φ_v∗(μ|_{(0,1)}) is singular with respect to μ (it is the Cantor measure, supported on a set of Lebesgue measure zero). Therefore Dₖₗ(φ_v∗μ ‖ μ) = +∞. ¬BD holds.

OC: Assign τ_out(v) = (1/4, 3/4) ⊂ int(X). Then OC-1 holds (φ_v maps int(X) into (1/4, 3/4)) and OC-2 holds as before.

**Conclusion:** W2 satisfies GBP, OC, but not BD. ✓

---

**Witness W3 (GBP ∧ BD but ¬OC):**

Let X = [0,1], μ = Lebesgue measure. Let φ_v(x) = x (identity map).

- *GBP:* Identity map preserves ∂X = {0,1} and int(X) = (0,1). ✓
- *BD:* φ_v∗μ = μ, so Dₖₗ(μ ‖ μ) = 0. ✓
- *¬OC:* Violate OC-1 by setting τ_out(v) = {x ∈ X : x > 1/2}. Then for any x ≤ 1/2, φ_v(x) = x ∉ Ω_{T(v)} = (1/2, 1]. Type safety fails for all x ∈ Ω_v ∩ [0, 1/2]. ¬OC-1 holds. ✓

**Conclusion:** W3 satisfies GBP, BD, but not OC. ✓

This completes the proof of Lemma 3.6. □

---

### 4.3 Proof of Theorem 3.1

**Theorem 3.1.** Adm(v) ⟺ GBP(v) ∧ BD(v) ∧ OC(v).

**Proof.**

(⟸) *Sufficiency.* By Definition 2.8, Adm(v) is defined as GBP(v) ∧ BD(v) ∧ OC(v). Therefore, if GBP(v) ∧ BD(v) ∧ OC(v) holds, then Adm(v) holds by definition.

(→) *Necessity.* If Adm(v) holds, then by Definition 2.8, GBP(v) ∧ BD(v) ∧ OC(v) holds, from which each conjunct is derivable by conjunction elimination.

The biconditional follows immediately. □

---

### 4.4 Proof of Corollary 3.2 (Joint Completeness)

**Part (1): Sufficiency.** Established in Theorem 3.1 (⟸ direction). □

**Part (2): Necessity.** Established in Theorem 3.1 (→ direction). □

**Part (3): Independence.** We must show that each condition is not derivable from the other two.

*GBP is independent of {BD, OC}:*
Witness W1 satisfies BD ∧ OC but not GBP. Therefore BD ∧ OC does not imply GBP. To show GBP does not imply BD ∧ OC alone is not needed for this direction, but the relevant direction for independence is: the conjunction {BD, OC} does not entail GBP. W1 witnesses this. ✓

*BD is independent of {GBP, OC}:*
Witness W2 satisfies GBP ∧ OC but not BD. Therefore GBP ∧ OC does not imply BD. ✓

*OC is independent of {GBP, BD}:*
Witness W3 satisfies GBP ∧ BD but not OC. Therefore GBP ∧ BD does not imply OC. ✓

Therefore the three conditions are mutually independent (no one condition is entailed by the conjunction of the other two). The set {GBP, BD, OC} is thus irredundant as well as jointly necessary and sufficient. □

---

### 4.5 Proof of Non-Vacuity

**Proposition 4.5.1 (Non-Vacuity).** There exists a gate satisfying all three conditions simultaneously.

*Proof.* Let X = [0,1], μ = Lebesgue measure, φ_v(x) = x (identity). Then:
- GBP: Identity preserves ∂X = {0,1} and int(X). ✓
- BD: φ_v∗μ = μ, Dₖₗ(μ ‖ μ) = 0 ≤ K for any K ≥ 0. ✓
- OC: Set τ_out(v) = X (the full type). Then φ_v(x) = x ∈ X for all x ∈ Ω_v. OC-1 holds. The identity commutes with all semantic morphisms trivially, so OC-2 holds. ✓

So the identity gate satisfies all three conditions. □

---

### 4.6 Completeness Discussion

**On the completeness of {GBP, BD, OC}:**

The claim "jointly complete" in Corollary 3.2 means: (a) they are sufficient (sufficient for Adm as defined), (b) they are necessary (necessary for Adm as defined), and (c) they are independent (irredundant).

This is *relative completeness* with respect to Definition 2.8. The deeper question — whether Definition 2.8 itself captures all relevant constraints for safety-critical ALLOW gate behavior in any deployment context — is a modeling question, not a mathematical one within this artifact.

**Formally derivable additional conditions:** One might ask whether further conditions are derivable *from GBP ∧ BD ∧ OC within the engine model*. We note:

- **GBP + BD together** imply, by Lemmas 