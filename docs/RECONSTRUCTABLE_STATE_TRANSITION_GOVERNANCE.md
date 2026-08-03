# Reconstructable State-Transition Governance

Status: **CANONICAL SESSION TRANSFER — DESIGN AND CLAIM BOUNDARY**

Program relationship: `SV-COST-MAJOR-GOAL-001`

This document preserves the governance and continuity formulation developed alongside the SV-COST relational testing program. It is a design contract and reasoning model. It does not, by itself, prove that a deployed implementation satisfies the model.

## 1. Governing proposition

Governance is not merely an approval mechanism attached to an action. Governance is the active constraint structure that determines which successor state may be committed from a sufficiently identified prior state.

The central question is not only:

> Was this action permitted?

It is:

> Given the actual prior state and the governance active at the transition boundary, what successor states were potential, which were admissible, which successor was committed, and why would any competing successor require a governance change, a correction to the reconstructed prior state, or evidence of implementation defect?

A compact expression is:

```text
T = F(S_prior, G_active, E_boundary)
```

where:

- `S_prior` is the reconstructed identity of the state immediately before the transition;
- `G_active` is the authentic governance actually active at the boundary;
- `E_boundary` is any evidence or observation that governance declares relevant to the transition;
- `T` is the governed successor-state determination.

Actor identity, approval, authorization, and human presence are attributes of `S_prior`, `G_active`, or `E_boundary` only when the governance makes them relevant. They are not free-standing sources of authority outside the transition relation.

## 2. Reconstruction singularity

For a prior state `S_i`, let:

```text
P(S_i)
```

be the set of reconstructable potential continuations.

Let:

```text
A(S_i, G_i, E_i) ⊆ P(S_i)
```

be the subset admitted by the governance and boundary evidence active at the transition.

The reconstruction singularity is the transition boundary at which multiple continuations may exist as potentials, while one continuation becomes historical reality through the commit relation.

For a fully instantiated governed boundary, deterministic transition validity requires:

```text
|A(S_i, G_i, E_i)| = 1
```

and the committed successor must equal that sole admitted element.

This uniqueness condition is evaluated after all governance-relevant boundary evidence is instantiated. A provider or external environment may produce uncertain observations. Governance need not predict the observation. It must deterministically map every admissible observation class to exactly one next governance state, including advancing, retrying, rejecting, blocking, or recording error.

Thus a deterministic governed path can contain stochastic observations when:

```text
for every admissible E_i: |A(S_i, G_i, E_i)| = 1
```

## 3. Governed path from A to B

A governed path is a sequence:

```text
S_0 → S_1 → ... → S_n
```

in which each successor becomes the exact prior state for the next transition.

Choosing a path from state A to desired state B requires enough prior-state identity and enough admissibility precision at each boundary that the desired successor is the sole state capable of advancing the path without changing governance.

A strong path-validity condition is:

1. reconstruct `S_i` with sufficient completeness;
2. reconstruct authentic `G_i`;
3. bind all governance-relevant `E_i`;
4. enumerate or characterize potential successor classes;
5. apply the admissibility matrix;
6. prove the committed successor is admitted;
7. prove no competing advancing successor is admitted under the same state, governance, and evidence;
8. bind `S_{i+1}` as the exact prior state for the next boundary.

Deviation outcomes may remain possible as observations or attempted writes, but governance must map them to non-advancing successors such as `RETRY`, `BLOCKED`, `REVIEW_REQUIRED`, `FAILED`, or `CORRUPT` rather than silently allowing them to become the intended continuing state.

## 4. State-transition validity

A transition is reconstructably valid only when all of the following are supported:

- prior-state completeness sufficient for the claimed transition;
- governance authenticity at the boundary;
- no omitted governing rule that would alter admissibility;
- faithful implementation of the active rules;
- authentic evidence binding;
- the observed commit belongs to the admitted successor set;
- the observed commit is the unique advancing successor for the fully instantiated boundary;
- the successor identity is preserved into the next transition.

The evaluator asks:

> Did the observed transition necessarily follow from the complete prior state under the governance actually active at the transition boundary?

A competing outcome must be explainable by at least one of:

- governance changed;
- the prior-state reconstruction was incomplete or incorrect;
- relevant evidence was omitted or misclassified;
- the implementation did not faithfully enforce governance;
- the observed write was unauthorized by the active transition relation.

## 5. Authorization as an attribute

When a user instructs a governed evaluation system to perform an authorized test, that instruction may supply authorization capacity because the active governance recognizes it.

When no human is in the loop, the active constraints may themselves be the authorizing party for the transition. The absence of a human does not imply the absence of authority if governance defines machine-enforced conditions as sufficient.

Conversely, a human approval does not make a transition admissible when the governance does not recognize that approval as sufficient.

Therefore:

- approval is evidence or state;
- execution is an attempted write;
- admissibility determines whether the write follows from governance;
- continuity preserves identity across boundaries;
- legitimacy depends on whether the claimed governance relation was authentic;
- reconstruction proves the relation later.

## 6. Reconstructibility and apparent corporate choice

Incomplete reconstruction can create an apparently broad option set. A company may appear able to continue, delay, reverse, substitute, conceal, reclassify, or proceed under a different interpretation.

Sufficient reconstruction may show that some apparent choices are not admissible continuations of the actual prior state. They may instead be:

- discontinuities;
- replacements of state identity;
- governance violations;
- actions requiring an explicit governance amendment;
- attempted writes that must resolve to a blocked or error state.

The consequence is:

```text
incomplete reconstruction → broad apparent discretion
sufficient reconstruction → reduced admissible set
complete boundary identity + active constraints → unique advancing successor
```

Reconstructibility does not externally take authority away from a company. It can reveal that some supposed alternatives were never continuity-preserving successors under the governance already in force.

Canonical formulation:

> Reconstructibility removes false discretion by exposing which apparent choices are not admissible continuations of the actual prior state.

This is an observed consequence of the same state-transition relationship, not a separate foundational principle.

## 7. Failure classes

The model must distinguish at least:

- `MULTIPLE_ADMISSIBLE_SUCCESSORS`: governance does not uniquely determine the next state;
- `NO_ADMISSIBLE_SUCCESSOR`: the transition cannot continue and must fail closed;
- `OBSERVED_OUTSIDE_ADMISSIBLE_SET`: the committed write violates governance;
- `PRIOR_STATE_MISMATCH`: the evaluator reconstructed the wrong state identity;
- `GOVERNANCE_DRIFT`: governance changed before or during the boundary;
- `EVIDENCE_OMISSION`: relevant evidence was not bound;
- `IMPLEMENTATION_DIVERGENCE`: enforcement did not match the declared governance;
- `CONTINUITY_BREAK`: the successor used for the next transition is not the exact committed successor;
- `NONDETERMINISTIC_ADVANCE`: the same fully instantiated boundary can produce different advancing states without governance change;
- `PURPOSE_INVERSION`: maintaining a local boundary prevents convergence to the intended governed state.

## 8. Relationship to SV-COST testing

The SV-COST workflows apply this model operationally:

- the prior relation state determines which experiment is admissible next;
- workflows have no free-standing authority to invent new experiment families;
- provider observations are uncertain, but governance deterministically maps evidence to `ADJUDICATED`, `RETRY`, `BLOCKED`, or `FAILED` states;
- route-price effects are not admitted as successful savings when completion and quality gates fail;
- generation, accounting transform, and reconstruction remain separate operation classes;
- a workflow's green status is not equivalent to an admissible economic conclusion;
- committed receipts bind the successor state for the next program transition.

The canonical program relation can be represented as:

```text
ProgramState_(i+1) = F(
  ProgramState_i,
  ActiveRelationContract_i,
  ObservedEvidence_i
)
```

The worker executes evidence-producing steps. The governance contract determines whether the evidence advances the program.

## 9. SPE evaluation obligations

A State Provenance Evaluator or equivalent verifier should be able to:

1. reconstruct the exact claimed prior state;
2. reconstruct the governance active at commit time;
3. establish authenticity and temporal applicability of rules;
4. bind evidence, policy, delegation, and constraint references;
5. characterize potential successor classes;
6. calculate the admitted successor set;
7. verify the observed transition is admitted;
8. verify uniqueness of the advancing successor for the instantiated boundary;
9. identify any alternative that required governance mutation, state correction, or implementation defect;
10. bind the committed successor into the next transition's prior-state identity;
11. produce a replayable receipt with explicit unknowns and claim boundaries.

## 10. Claim boundary

This document defines a formal relationship and implementation obligations. It does not establish that every StegVerse component, GCAT/BCAT engine, provider workflow, or deployed system currently satisfies those obligations.

Deployed correspondence requires separate evidence for:

- canonical state serialization;
- governance version and effective-time binding;
- evidence completeness;
- rule evaluation determinism;
- commit atomicity;
- successor identity continuity;
- independent reconstruction;
- runtime enforcement;
- failure-closed behavior.

## 11. Durable continuation

This formulation is merged into the canonical workstream at:

- `SV_COST_MIRROR_HANDOFF.md`;
- `experiments/sv-cost-program/session-goal-inventory.json` task `SV-COST-009-GOVERNANCE-FORMALISM`;
- issue `#12` for the active relational program.

Any later implementation must preserve the distinction between conceptual validity, contract validity, workflow execution, committed evidence, runtime enforcement, and deployed-system correspondence.
