SECTION 1: ASSUMPTIONS AND CLAIM BOUNDARY

**Artifact identifier:** SV-MATH-001.

Let a GCAT/BCAT engine process a request \(r\) in state \(s\), producing the candidate state \(T(s,r)\). This artifact treats ALLOW as a Boolean gate whose intended meaning is semantic admissibility.

The proof is relative to the following explicit contract assumptions:

1. **Gate exactness:** the ALLOW bit is true exactly when the candidate transition is semantically admissible.
2. **Necessity:** every semantically admissible transition:
   - preserves the designated geometric boundary,
   - has divergence bounded by the request-specific budget, and
   - is ontologically consistent.
3. **Sufficiency:** every transition satisfying all three conditions is semantically admissible.

No unconditional claim is made that geometry, divergence, and ontology are intrinsically complete for every possible GCAT/BCAT implementation. Their joint completeness follows exactly when the engine specification validates the sufficiency assumption. Without that assumption, the three conditions can be necessary but incomplete; without necessity, they can admit semantically invalid transitions.

The following model uses exact pointwise preservation of the designated boundary. An implementation using geometric equivalence, tolerance, isotopy, or an authorized boundary transformation may replace equality with the corresponding formally specified equivalence relation without changing the logical proof structure.

SECTION 2: DEFINITIONS

Let:

- \(S\) be the set of engine states;
- \(R\) be the set of requests;
- \(P\) be the geometric point domain;
- \(T:S\times R\to S\) be the candidate-transition function;
- \(\partial(s)\subseteq P\) be the designated boundary of state \(s\);
- \(\Delta:S\times S\to\mathbb N\) be the divergence measure;
- \(\beta:R\to\mathbb N\) be the request-specific divergence budget;
- \(\mathsf{Ont}:S\to\{\mathsf{true},\mathsf{false}\}\) express state-level ontological validity;
- \(\mathsf{Req}:R\to\{\mathsf{true},\mathsf{false}\}\) express request-level ontological compatibility;
- \(\mathsf{Adm}:R\times S\to\{\mathsf{true},\mathsf{false}\}\) be semantic admissibility;
- \(\mathsf{ALLOW}:R\times S\to\{\mathsf{true},\mathsf{false}\}\) be the implemented gate.

For \(r\in R\) and \(s\in S\), define:

\[
\mathsf{GBP}(r,s)
\;:\Longleftrightarrow\;
\forall p\in P,\;
p\in\partial(T(s,r))
\iff
p\in\partial(s).
\]

Thus \(\mathsf{GBP}\) is geometric boundary preservation.

Define bounded divergence by

\[
\mathsf{BD}(r,s)
\;:\Longleftrightarrow\;
\Delta(s,T(s,r))\leq\beta(r).
\]

Because \(\beta(r)\in\mathbb N\), this gives an explicit finite bound rather than merely asserting that divergence is finite.

Define ontological consistency by

\[
\mathsf{OC}(r,s)
\;:\Longleftrightarrow\;
\mathsf{Req}(r)
\land
\bigl(\mathsf{Ont}(s)\Rightarrow\mathsf{Ont}(T(s,r))\bigr).
\]

Define the conjunction of the three candidate criteria:

\[
\mathsf{C}(r,s)
\;:\Longleftrightarrow\;
\mathsf{GBP}(r,s)\land
\mathsf{BD}(r,s)\land
\mathsf{OC}(r,s).
\]

The engine contract consists of:

\[
\tag{E}
\mathsf{ALLOW}(r,s)=\mathsf{true}
\iff
\mathsf{Adm}(r,s),
\]

\[
\tag{N}
\mathsf{Adm}(r,s)\Rightarrow\mathsf{C}(r,s),
\]

and

\[
\tag{S}
\mathsf{C}(r,s)\Rightarrow\mathsf{Adm}(r,s).
\]

Condition (N) is the collective necessity obligation. Condition (S) is the joint-completeness, or sufficiency, obligation.

SECTION 3: THEOREM STATEMENT

**Theorem SV-MATH-001 — ALLOW admissibility characterization.**

For every request \(r\in R\) and state \(s\in S\), if the engine satisfies contracts (E), (N), and (S), then

\[
\mathsf{ALLOW}(r,s)=\mathsf{true}
\iff
\mathsf{GBP}(r,s)\land
\mathsf{BD}(r,s)\land
\mathsf{OC}(r,s).
\]

Equivalently,

\[
\mathsf{ALLOW}(r,s)=\mathsf{true}
\iff
\begin{cases}
\forall p\in P,\;
p\in\partial(T(s,r))\iff p\in\partial(s),\\[2mm]
\Delta(s,T(s,r))\leq\beta(r),\\[2mm]
\mathsf{Req}(r)\land
\bigl(\mathsf{Ont}(s)\Rightarrow\mathsf{Ont}(T(s,r))\bigr).
\end{cases}
\]

Moreover:

1. Under (N), the three conditions are necessary.
2. Under (S), their conjunction is sufficient.
3. Under both (N) and (S), they are jointly complete for semantic admissibility.
4. Conditions (E) and (N) alone do not establish joint completeness.
5. Conditions (E) and (S) alone do not establish necessity.

SECTION 4: MATHEMATICAL PROOF

Fix arbitrary \(r\in R\) and \(s\in S\).

First suppose

\[
\mathsf{ALLOW}(r,s)=\mathsf{true}.
\]

By gate exactness (E),

\[
\mathsf{Adm}(r,s).
\]

Applying necessity (N) gives

\[
\mathsf{C}(r,s).
\]

Expanding the definition of \(\mathsf{C}\),

\[
\mathsf{GBP}(r,s)\land
\mathsf{BD}(r,s)\land
\mathsf{OC}(r,s).
\]

Therefore,

\[
\mathsf{ALLOW}(r,s)=\mathsf{true}
\Rightarrow
\mathsf{GBP}(r,s)\land
\mathsf{BD}(r,s)\land
\mathsf{OC}(r,s).
\]

This proves necessity of all three conditions for an ALLOW decision.

Conversely, suppose

\[
\mathsf{GBP}(r,s)\land
\mathsf{BD}(r,s)\land
\mathsf{OC}(r,s).
\]

By definition, this is \(\mathsf{C}(r,s)\). Applying sufficiency (S) yields

\[
\mathsf{Adm}(r,s).
\]

By gate exactness (E),

\[
\mathsf{ALLOW}(r,s)=\mathsf{true}.
\]

Hence,

\[
\mathsf{GBP}(r,s)\land
\mathsf{BD}(r,s)\land
\mathsf{OC}(r,s)
\Rightarrow
\mathsf{ALLOW}(r,s)=\mathsf{true}.
\]

Combining the two implications proves

\[
\mathsf{ALLOW}(r,s)=\mathsf{true}
\iff
\mathsf{GBP}(r,s)\land
\mathsf{BD}(r,s)\land
\mathsf{OC}(r,s).
\]

Since \(r\) and \(s\) were arbitrary, the equivalence holds for every request and state.

To determine whether the three conditions are jointly complete independently of (S), treat admissibility and the three criteria as propositions \(A,G,D,O\). Pure logic does not prove

\[
A\iff(G\land D\land O)
\]

for arbitrary propositions. For example, let

\[
A=\mathsf{false},
\qquad
G=D=O=\mathsf{true}.
\]

Then all three criteria hold, but admissibility does not. Thus the criteria are not sufficient in this model.

Likewise, let

\[
A=\mathsf{true},
\qquad
G=\mathsf{false},
\qquad
D=O=\mathsf{true}.
\]

Then admissibility holds while geometric boundary preservation fails. Thus necessity is also not a consequence of propositional logic alone.

Accordingly, geometric boundary preservation, bounded divergence, and ontological consistency are jointly complete precisely relative to a GCAT/BCAT semantic specification proving both

\[
\mathsf{Adm}\Rightarrow\mathsf{C}
\quad\text{and}\quad
\mathsf{C}\Rightarrow\mathsf{Adm}.
\]

The second implication is the substantive completeness obligation; it cannot be inferred merely from the names or individual definitions of the three predicates. ∎

SECTION 5: LEAN 4 CANDIDATE

```lean
/-
SV-MATH-001
Lean 4 candidate using only core logical and arithmetic notions.
-/

universe uS uR uP

structure Engine
    (State : Type uS)
    (Request : Type uR)
    (Point : Type uP) where
  step       : State → Request → State
  boundary   : State → Point → Prop
  divergence : State → State → Nat
  budget     : Request → Nat
  ontOK      : State → Prop
  reqOK      : Request → Prop
  admissible : Request → State → Prop
  allow      : Request → State → Bool

namespace SVMATH001

variable
  {State : Type uS}
  {Request : Type uR}
  {Point : Type uP}

def GeometricBoundaryPreservation
    (e : Engine State Request Point)
    (r : Request)
    (s : State) : Prop :=
  ∀ p : Point,
    e.boundary (e.step s r) p ↔ e.boundary s p

def BoundedDivergence
    (e : Engine State Request Point)
    (r : Request)
    (s : State) : Prop :=
  e.divergence s (e.step s r) ≤ e.budget r

def OntologicalConsistency
    (e : Engine State Request Point)
    (r : Request)
    (s : State) : Prop :=
  e.reqOK r ∧ (e.ontOK s → e.ontOK (e.step s r))

def Conditions
    (e : Engine State Request Point)
    (r : Request)
    (s : State) : Prop :=
  GeometricBoundaryPreservation e r s ∧
  BoundedDivergence e r s ∧
  OntologicalConsistency e r s

structure AllowContract
    (e : Engine State Request Point) : Prop where
  gate_exact :
    ∀ r s, e.allow r s = true ↔ e.admissible r s

  necessary :
    ∀ r s, e.admissible r s → Conditions e r s

  sufficient :
    ∀ r s, Conditions e r s → e.admissible r s

theorem admissible_iff_conditions
    (e : Engine State Request Point)
    (contract : AllowContract e)
    (r : Request)
    (s : State) :
    e.admissible r s ↔ Conditions e r s := by
  constructor
  · intro hAdm
    exact contract.necessary r s hAdm
  · intro hConditions
    exact contract.sufficient r s hConditions

theorem allow_iff_conditions
    (e : Engine State Request Point)
    (contract : AllowContract e)
    (r : Request)
    (s : State) :
    e.allow r s = true ↔ Conditions e r s := by
  constructor
  · intro hAllow
    have hAdm : e.admissible r s :=
      (contract.gate_exact r s).mp hAllow
    exact contract.necessary r s hAdm
  · intro hConditions
    have hAdm : e.admissible r s :=
      contract.sufficient r s hConditions
    exact (contract.gate_exact r s).mpr hAdm

theorem allow_implies_geometric_preservation
    (e : Engine State Request Point)
    (contract : AllowContract e)
    (r : Request)
    (s : State)
    (hAllow : e.allow r s = true) :
    GeometricBoundaryPreservation e r s := by
  have hAll : Conditions e r s :=
    (allow_iff_conditions e contract r s).mp hAllow
  exact hAll.1

theorem allow_implies_bounded_divergence
    (e : Engine State Request Point)
    (contract : AllowContract e)
    (r : Request)
    (s : State)
    (hAllow : e.allow r s = true) :
    BoundedDivergence e r s := by
  have hAll : Conditions e r s :=
    (allow_iff_conditions e contract r s).mp hAllow
  exact hAll.2.1

theorem allow_implies_ontological_consistency
    (e : Engine State Request Point)
    (contract : AllowContract e)
    (r : Request)
    (s : State)
    (hAllow : e.allow r s = true) :
    OntologicalConsistency e r s := by
  have hAll : Conditions e r s :=
    (allow_iff_conditions e contract r s).mp hAllow
  exact hAll.2.2

theorem conditions_imply_allow
    (e : Engine State Request Point)
    (contract : AllowContract e)
    (r : Request)
    (s : State)
    (hGeom : GeometricBoundaryPreservation e r s)
    (hDiv : BoundedDivergence e r s)
    (hOnt : OntologicalConsistency e r s) :
    e.allow r s = true := by
  apply (allow_iff_conditions e contract r s).mpr
  exact ⟨hGeom, hDiv, hOnt⟩

/-
The criteria are not logically sufficient without a sufficiency
contract: all three can be true while admissibility is false.
-/
theorem no_unconditional_sufficiency :
    ¬ (False ↔ (True ∧ True ∧ True)) := by
  simp

/-
The criteria are not logically necessary without a necessity
contract: admissibility can be true while one criterion is false.
-/
theorem no_unconditional_necessity :
    ¬ (True ↔ (False ∧ True ∧ True)) := by
  simp

end SVMATH001
```

SECTION 6: VERIFICATION LEDGER

| Obligation | Formal source | Status |
|---|---|---|
| ALLOW corresponds exactly to semantic admissibility | Contract (E), `AllowContract.gate_exact` | Required assumption |
| Geometric boundary preservation is necessary | Contract (N), first component of `Conditions` | Proved from necessity contract |
| Bounded divergence is necessary | Contract (N), second component of `Conditions` | Proved from necessity contract |
| Ontological consistency is necessary | Contract (N), third component of `Conditions` | Proved from necessity contract |
| The conjunction is sufficient | Contract (S), `AllowContract.sufficient` | Required completeness assumption |
| ALLOW implies all three criteria | (E) followed by (N) | Proved |
| All three criteria imply ALLOW | (S) followed by (E) | Proved |
| Semantic admissibility is equivalent to the conjunction | (N) and (S) | Proved |
| ALLOW is equivalent to the conjunction | (E), (N), and (S) | Proved |
| Completeness follows from the definitions alone | Countermodel with \(A=\mathsf{false}\), \(G=D=O=\mathsf{true}\) | Refuted |
| Necessity follows from the definitions alone | Countermodel with \(A=\mathsf{true}\), \(G=\mathsf{false}\) | Refuted |
| Divergence has an explicit finite bound | Natural-number budget \(\beta(r)\) | Established by definition |
| Lean proof kernel execution | Candidate supplied but not executed in this artifact | Pending toolchain verification |

SECTION 7: FINAL CLAIM BOUNDARY

SV-MATH-001 establishes the following conditional characterization:

\[
\boxed{
\mathsf{ALLOW}(r,s)=\mathsf{true}
\iff
\mathsf{GBP}(r,s)\land
\mathsf{BD}(r,s)\land
\mathsf{OC}(r,s)
}
\]

provided that the GCAT/BCAT engine validates gate exactness, necessity, and sufficiency.

Geometric boundary preservation, bounded divergence, and ontological consistency are therefore jointly complete **if and only if** semantic admissibility is proved equivalent to their conjunction. They are not jointly complete merely by being individually desirable safety properties. Any additional admissibility requirement—such as authorization, provenance, temporal constraints, confidentiality, resource limits, or policy compliance—must either be incorporated into one of the three predicates or added as another conjunct before sufficiency can validly be asserted.

END_OF_ARTIFACT