SECTION 1: ASSUMPTIONS AND CLAIM BOUNDARY

Artifact identifier: SV-MATH-001

1.1 Stipulated assumptions

Let \(P\) be the set of candidate transitions submitted to an ALLOW gate. For each \(p\in P\), stipulate:

- \(s_0(p)\): the pre-transition state.
- \(s_1(p)\): the proposed post-transition state.
- \(a(p)\): the proposed action.
- \(\partial(s)\): the geometric boundary signature assigned to state \(s\).
- \(\delta(p)\in\mathbb{R}_{\ge 0}\): the divergence measure of \(p\).
- \(\varepsilon\in\mathbb{R}_{\ge 0}\): the configured maximum divergence.
- \(\mathsf{OntValid}(p)\): the proposition that \(p\) is consistent with the governing ontology.
- \(\mathsf{Allow}(p)\): the proposition that the engine returns ALLOW for \(p\).

Define the three stated criteria:

\[
\begin{aligned}
G(p) &\;:\!\iff\; \partial(s_0(p))=\partial(s_1(p)),\\
D(p) &\;:\!\iff\; \delta(p)\le \varepsilon,\\
O(p) &\;:\!\iff\; \mathsf{OntValid}(p).
\end{aligned}
\]

The abstract GCAT/BCAT gate contract is the stipulated bridge:

\[
\tag{GCAT/BCAT-SPEC}
\forall p\in P,\quad
\mathsf{Allow}(p)\iff G(p)\land D(p)\land O(p).
\]

This bridge is an assumption about the abstract engine, not a verified fact about any deployed implementation.

1.2 Generated claims

This artifact proves:

1. Exact ALLOW admissibility is equivalent to the conjunction of geometric boundary preservation, bounded divergence, and ontological consistency under GCAT/BCAT-SPEC.
2. More generally, those criteria are jointly complete exactly when:
   - each criterion is necessary for ALLOW; and
   - their conjunction is sufficient for ALLOW.
3. The three predicates are not jointly complete merely because they are named as gate criteria. Without an implementation-to-specification bridge, both necessity and sufficiency can fail.
4. Joint completeness does not imply that the three criteria are logically independent or minimal.

1.3 Verified-claim boundary

The mathematical implications below are established by explicit derivation. A Lean 4 proof candidate is supplied, but no Lean compiler was executed in producing this artifact. Consequently, no claim of Lean compilation or kernel verification is made.

No deployed GCAT/BCAT source, build, configuration, ontology, divergence implementation, geometry implementation, execution trace, or attestation was supplied. Therefore this artifact does not verify that any deployed engine satisfies GCAT/BCAT-SPEC.

SECTION 2: DEFINITIONS

2.1 ALLOW admissibility

A proposal \(p\) is ALLOW-admissible exactly when:

\[
A(p) \;:\!\iff\; \mathsf{Allow}(p).
\]

2.2 Geometric boundary preservation

\[
G(p) \;:\!\iff\; \partial(s_0(p))=\partial(s_1(p)).
\]

The boundary signature may represent a geometric boundary, region identifier, topology-preserving invariant, permitted spatial envelope, or another engine-defined geometric invariant. Equality is equality in the abstract boundary-signature domain.

2.3 Bounded divergence

\[
D(p) \;:\!\iff\; \delta(p)\le\varepsilon.
\]

The measure \(\delta\), its units, normalization, treatment of undefined values, and threshold \(\varepsilon\) are parameters of the abstract model. They must be bound to deployed definitions before an implementation-level claim is warranted.

2.4 Ontological consistency

\[
O(p) \;:\!\iff\; \mathsf{OntValid}(p).
\]

Abstractly, this may mean that the transition is satisfiable with respect to an ontology \(K\), violates no integrity constraint, and produces no prohibited type, relation, or policy contradiction. The exact entailment regime is left unresolved until a specific ontology and reasoner semantics are supplied.

2.5 Joint criterion

\[
C(p) \;:\!\iff\; G(p)\land D(p)\land O(p).
\]

2.6 Necessity conditions

\[
\begin{aligned}
N_G &:\!\iff \forall p,\; A(p)\rightarrow G(p),\\
N_D &:\!\iff \forall p,\; A(p)\rightarrow D(p),\\
N_O &:\!\iff \forall p,\; A(p)\rightarrow O(p).
\end{aligned}
\]

2.7 Joint sufficiency

\[
S_C \;:\!\iff\; \forall p,\; C(p)\rightarrow A(p).
\]

2.8 Joint completeness

The three criteria are jointly complete for the ALLOW gate when:

\[
\mathsf{Complete}(G,D,O;A)
\;:\!\iff\;
\forall p,\; A(p)\leftrightarrow C(p).
\]

This is extensional completeness relative to ALLOW decisions. It does not assert that no criterion is redundant.

SECTION 3: THEOREM STATEMENT

Theorem SV-MATH-001 — ALLOW gate admissibility characterization.

For arbitrary predicates \(A,G,D,O:P\to\mathsf{Prop}\), let
\(C(p)=G(p)\land D(p)\land O(p)\). Then:

\[
\boxed{
\left(\forall p,\;A(p)\leftrightarrow C(p)\right)
\iff
\left(N_G\land N_D\land N_O\land S_C\right)
}
\]

Equivalently, geometric boundary preservation, bounded divergence, and ontological consistency are jointly complete for ALLOW admissibility if and only if:

1. every ALLOW decision preserves the geometric boundary;
2. every ALLOW decision respects the divergence bound;
3. every ALLOW decision is ontologically consistent; and
4. every proposal satisfying all three criteria receives ALLOW.

Corollary under GCAT/BCAT-SPEC:

\[
\boxed{
\forall p,\quad
\mathsf{Allow}(p)
\iff
\partial(s_0(p))=\partial(s_1(p))
\land
\delta(p)\le\varepsilon
\land
\mathsf{OntValid}(p)
}
\]

Thus the three criteria are necessary and jointly sufficient under the stipulated abstract gate contract.

Non-entailment statement:

Without GCAT/BCAT-SPEC or equivalent evidence establishing \(N_G\), \(N_D\), \(N_O\), and \(S_C\), the three criteria are not provably complete for an actual engine.

SECTION 4: MATHEMATICAL PROOF

Let:

\[
C(p)=G(p)\land D(p)\land O(p).
\]

We prove both directions of the characterization theorem.

4.1 Completeness implies individual necessity and joint sufficiency

Assume:

\[
H:\forall p,\quad A(p)\leftrightarrow C(p).
\]

To prove \(N_G\), take arbitrary \(p\) and assume \(A(p)\). By the forward direction of \(H\), \(C(p)\). Expanding \(C\) gives:

\[
G(p)\land D(p)\land O(p).
\]

Therefore \(G(p)\). Since \(p\) was arbitrary:

\[
N_G:\forall p,\quad A(p)\rightarrow G(p).
\]

The same conjunction yields \(D(p)\), so:

\[
N_D:\forall p,\quad A(p)\rightarrow D(p).
\]

It also yields \(O(p)\), so:

\[
N_O:\forall p,\quad A(p)\rightarrow O(p).
\]

To prove joint sufficiency, take arbitrary \(p\) and assume \(C(p)\). By the reverse direction of \(H\):

\[
C(p)\rightarrow A(p).
\]

Hence:

\[
S_C:\forall p,\quad C(p)\rightarrow A(p).
\]

Therefore:

\[
\mathsf{Complete}(G,D,O;A)
\rightarrow
N_G\land N_D\land N_O\land S_C.
\]

4.2 Individual necessity and joint sufficiency imply completeness

Assume \(N_G\), \(N_D\), \(N_O\), and \(S_C\). Fix arbitrary \(p\).

First suppose \(A(p)\). By the three necessity assumptions:

\[
A(p)\rightarrow G(p),\qquad
A(p)\rightarrow D(p),\qquad
A(p)\rightarrow O(p).
\]

Therefore:

\[
A(p)\rightarrow G(p)\land D(p)\land O(p),
\]

which is:

\[
A(p)\rightarrow C(p).
\]

Conversely, suppose \(C(p)\). By joint sufficiency \(S_C\):

\[
C(p)\rightarrow A(p).
\]

Combining the two implications:

\[
A(p)\leftrightarrow C(p).
\]

Since \(p\) was arbitrary:

\[
\forall p,\quad A(p)\leftrightarrow C(p).
\]

Therefore:

\[
N_G\land N_D\land N_O\land S_C
\rightarrow
\mathsf{Complete}(G,D,O;A).
\]

Together with Section 4.1, this proves the theorem.

4.3 Application to the stipulated abstract gate

GCAT/BCAT-SPEC states directly:

\[
\forall p,\quad
\mathsf{Allow}(p)\leftrightarrow G(p)\land D(p)\land O(p).
\]

Substituting the definitions of \(G,D,O\) gives:

\[
\mathsf{Allow}(p)
\iff
\partial(s_0(p))=\partial(s_1(p))
\land
\delta(p)\le\varepsilon
\land
\mathsf{OntValid}(p).
\]

The forward implication proves all three conditions necessary. The reverse implication proves their conjunction sufficient. Hence they are jointly complete relative to GCAT/BCAT-SPEC.

4.4 Why the bridge assumption is necessary

The criterion names alone impose no logical constraint on \(A\).

For failure of sufficiency, take a one-element proposal set \(P=\{\star\}\), define:

\[
G(\star)=D(\star)=O(\star)=\mathsf{True},
\qquad
A(\star)=\mathsf{False}.
\]

Then \(C(\star)\) is true but \(A(\star)\) is false. Thus:

\[
C(\star)\not\rightarrow A(\star).
\]

For failure of necessity, instead define:

\[
G(\star)=D(\star)=O(\star)=\mathsf{False},
\qquad
A(\star)=\mathsf{True}.
\]

Then \(A(\star)\) is true while every criterion is false. Thus none of the three necessity implications holds.

Consequently, geometric boundary preservation, bounded divergence, and ontological consistency are jointly complete only relative to a gate contract or verified implementation establishing the required equivalence. Completeness also does not establish minimality: one criterion could logically imply another in a particular model.

SECTION 5: LEAN 4 CANDIDATE

```lean
import Std

universe u v w

structure Proposal (State Action : Type u) where
  before : State
  after : State
  action : Action

structure GateSemantics
    (State Action : Type u) (Boundary : Type v) where
  boundarySignature : State → Boundary
  divergence : Proposal State Action → Nat
  ontologyValid : Proposal State Action → Prop

def GeometricBoundaryPreserved
    {State Action : Type u} {Boundary : Type v}
    (sem : GateSemantics State Action Boundary)
    (p : Proposal State Action) : Prop :=
  sem.boundarySignature p.before =
    sem.boundarySignature p.after

def BoundedDivergence
    {State Action : Type u} {Boundary : Type v}
    (sem : GateSemantics State Action Boundary)
    (epsilon : Nat)
    (p : Proposal State Action) : Prop :=
  sem.divergence p ≤ epsilon

def OntologicallyConsistent
    {State Action : Type u} {Boundary : Type v}
    (sem : GateSemantics State Action Boundary)
    (p : Proposal State Action) : Prop :=
  sem.ontologyValid p

structure Criteria (X : Type u) where
  geometricBoundary : X → Prop
  boundedDivergence : X → Prop
  ontologicalConsistency : X → Prop

def Joint
    {X : Type u}
    (c : Criteria X)
    (x : X) : Prop :=
  c.geometricBoundary x ∧
  c.boundedDivergence x ∧
  c.ontologicalConsistency x

theorem completeness_iff
    {X : Type u}
    (Allow : X → Prop)
    (c : Criteria X) :
    (∀ x, Allow x ↔ Joint c x) ↔
      ((∀ x, Allow x → c.geometricBoundary x) ∧
       (∀ x, Allow x → c.boundedDivergence x) ∧
       (∀ x, Allow x → c.ontologicalConsistency x) ∧
       (∀ x,
          c.geometricBoundary x →
          c.boundedDivergence x →
          c.ontologicalConsistency x →
          Allow x)) := by
  constructor
  · intro h
    constructor
    · intro x hx
      exact (h x).mp hx |>.1
    constructor
    · intro x hx
      exact (h x).mp hx |>.2.1
    constructor
    · intro x hx
      exact (h x).mp hx |>.2.2
    · intro x hg hd ho
      exact (h x).mpr ⟨hg, hd, ho⟩
  · rintro ⟨hGeo, hDiv, hOnt, hSuff⟩
    intro x
    constructor
    · intro hx
      exact ⟨hGeo x hx, hDiv x hx, hOnt x hx⟩
    · rintro ⟨hg, hd, ho⟩
      exact hSuff x hg hd ho

theorem allow_admissibility
    {X : Type u}
    (Allow : X → Prop)
    (c : Criteria X)
    (gateContract : ∀ x, Allow x ↔ Joint c x)
    (x : X) :
    Allow x ↔
      c.geometricBoundary x ∧
      c.boundedDivergence x ∧
      c.ontologicalConsistency x := by
  exact gateContract x

def allTrueCriteria : Criteria Unit where
  geometricBoundary := fun _ => True
  boundedDivergence := fun _ => True
  ontologicalConsistency := fun _ => True

def allFalseCriteria : Criteria Unit where
  geometricBoundary := fun _ => False
  boundedDivergence := fun _ => False
  ontologicalConsistency := fun _ => False

def denyAll : Unit → Prop := fun _ => False
def allowAll : Unit → Prop := fun _ => True

-- The criteria do not imply ALLOW without a gate contract.
example : Joint allTrueCriteria () ∧ ¬ denyAll () := by
  simp [Joint, allTrueCriteria, denyAll]

-- ALLOW does not imply the criteria without a gate contract.
example : allowAll () ∧ ¬ Joint allFalseCriteria () := by
  simp [Joint, allFalseCriteria, allowAll]
```

Candidate status: generated but not compiled in this execution. The code uses `Nat` for divergence to avoid imposing an unverified real-number library model. Replacing `Nat` with a deployed numeric domain requires preserving the intended order and threshold semantics.

SECTION 6: VERIFICATION LEDGER

| ID | Entry | Classification | Reconstruction procedure | Status |
|---|---|---|---|---|
| SV1 | GCAT/BCAT-SPEC: \(\mathsf{Allow}(p)\leftrightarrow G(p)\land D(p)\land O(p)\) | Stipulated assumption | Obtain the authoritative gate specification and compare its ALLOW rule with Section 2 | Unverified for any deployment |
| SV2 | Completeness characterization theorem | Generated mathematical claim | Expand `Joint`; prove both implications using conjunction introduction and elimination as in Section 4 | Paper-level derivation supplied |
| SV3 | Necessity of \(G,D,O\) under the gate contract | Derived claim | Apply the forward direction of SV1 and project each conjunct | Derived from SV1 |
| SV4 | Joint sufficiency under the gate contract | Derived claim | Introduce all three conjuncts and apply the reverse direction of SV1 | Derived from SV1 |
| SV5 | Criteria are not complete without a bridge | Generated countermodel claim | Evaluate the two one-element models in Section 4.4 | Explicit countermodels supplied |
| SV6 | Lean theorem `completeness_iff` | Generated formalization candidate | Save Section 5 as `SV_MATH_001.lean`; use a pinned Lean 4 toolchain; execute `lake env lean SV_MATH_001.lean` | Not compiled; kernel status unresolved |
| SV7 | Lean counterexamples | Generated formalization candidate | Compile the two `example` declarations and inspect for zero errors | Not compiled |
| DEP-GEO-1 | Meaning of deployed boundary signature | External dependency | Identify source functions, coordinate system, tolerances, canonicalization, topology rules, and failure handling used by GCAT/BCAT | Unresolved |
| DEP-DIV-1 | Meaning of deployed divergence | External dependency | Identify metric formula, numeric type, units, normalization, threshold source, comparison operator, overflow/NaN behavior, and defaults | Unresolved |
| DEP-ONT-1 | Meaning of ontology consistency | External dependency | Obtain ontology version/hash, constraint set, entailment regime, reasoner version, closed/open-world assumptions, and timeout/error policy | Unresolved |
| DEP-GATE-1 | Actual ALLOW control flow | External dependency | Review versioned source or executable semantics for all ALLOW branches, overrides, bypasses, caches, defaults, and additional predicates | Unresolved |
| DEP-BUILD-1 | Deployed artifact identity | External dependency | Record repository commit, dependency lockfile, compiler, build flags, binary/container digest, configuration digest, and signature | Unresolved |
| DEP-TRACE-1 | Runtime conformance | External dependency | Execute boundary, divergence, ontology, threshold-edge, malformed-input, and bypass-path test vectors; preserve signed inputs and outputs | Unresolved |
| DEP-MAP-1 | Abstract-to-concrete field mapping | External dependency | Map \(p,s_0,s_1,a,\partial,\delta,\varepsilon,\mathsf{OntValid}\) to exact deployed data fields and functions | Unresolved |
| DEP-LEAN-1 | Formal proof environment | External dependency | Pin Lean version and `Std` revision, compile Section 5, retain command, stdout/stderr, exit code, source digest, and toolchain digest | Unresolved |

Minimum evidence needed to bind this theorem to a deployed GCAT/BCAT engine:

1. An authoritative, versioned ALLOW specification.
2. Exact deployed source or equivalent executable semantics for every ALLOW path.
3. A complete abstract-to-concrete mapping for all predicates and parameters.
4. Versioned geometry, divergence, and ontology definitions.
5. Evidence that errors, missing values, timeouts, overrides, and defaults do not create unmodeled ALLOW paths.
6. Build and configuration identities sufficient to reconstruct the deployed executable.
7. Conformance traces covering positive, negative, boundary, and exceptional cases.
8. If machine-checked proof status is asserted, a reproducible Lean compilation record for the exact candidate source.

SECTION 7: FINAL CLAIM BOUNDARY

Bounded public claim:

SV-MATH-001 proves, at the abstract mathematical level, that geometric boundary preservation, bounded divergence, and ontological consistency are necessary and jointly sufficient for ALLOW exactly when the ALLOW predicate is extensionally equivalent to their conjunction. Under the stipulated GCAT/BCAT-SPEC contract, they are jointly complete.

This artifact does not establish that the criteria are independent, minimal, correctly implemented, or complete for any deployed GCAT/BCAT engine. Such a deployment-level claim remains contingent on the unresolved geometry, divergence, ontology, control-flow, build, mapping, trace, and formal-compilation evidence listed in Section 6. The Lean 4 text is a proof candidate and has not been claimed to compile.

END_OF_ARTIFACT