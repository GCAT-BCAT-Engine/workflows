# Consequence Horizon Formalism — Proof Obligations

## Assumptions

- This document is a pre-code mathematical scaffold for `GCAT-BCAT-Engine/workflows`.
- The current insertion path is `math_solver/validation/`.
- The first test family is intentionally minimal: 2D disk geometry before 3D or n-dimensional generalization.
- The phrase “sphere” is treated as a normalized visualization. The mathematical object is a bounded radial transition region, normally star-shaped with respect to an operational center.
- In governed systems, the crossing predicate is admissibility. In natural/physical interpretation layers, use viability or actualizability instead of moral or institutional admissibility.

## Done Criteria

This proof-obligation set is complete when each obligation has:

1. a formal statement,
2. a plain-language interpretation,
3. a failure mode,
4. a corresponding test in `problem_spec_chf_001.yml`, `problem_spec_chf_002.yml`, or `problem_spec_chf_003.yml`.

---

## PO-001 — Radial Coverage

### Formal Statement

Let `Ω ⊂ R^n` be compact and star-shaped with respect to center `S ∈ Ω`.

Let the boundary be partitioned into measurable patches:

```text
∂Ω = ⋃ B_i
```

Define each radial cell:

```text
Cell_i(S, B_i) = { (1 - λ)S + λb : b ∈ B_i, λ ∈ [0,1] }
```

Then, assuming every ray from `S` intersects the represented boundary:

```text
Ω = ⋃ Cell_i
```

### Plain Meaning

Every tetrahedron, pyramid, cone, or irregular inward-pointing volume is a special case of the same primitive:

```text
boundary patch → radial cell → shared center
```

### Failure Mode

This obligation fails if `Ω` is not star-shaped relative to `S`; for example, a hole, disconnected pocket, or forbidden corridor causes a radial segment from boundary to center to leave `Ω`.

### Test Anchor

`problem_spec_chf_001.yml` validates the 2D version with a unit disk and four angular radial cells.

---

## PO-002 — Category Change

### Formal Statement

A proposed transition `p_t ∈ Ω_t` remains potential until a crossing event occurs:

```text
χ_t = Cross(p_t, H_t)
```

Actualization requires:

```text
Permit_t(p_t) = ALLOW
```

After crossing:

```text
Actualize(p_t) = S_{t+1}
```

Without `χ_t`, no new state-center may be created from `p_t`.

### Plain Meaning

No crossing, no actualized transition.

In computational terms:

```text
No commit, no mutation.
```

### Failure Mode

This obligation fails if a DENY or FAIL_CLOSED case creates a new center from the proposed transition.

### Test Anchor

`problem_spec_chf_001.yml` validates that only `p1` creates a crossing and new center.

---

## PO-003 — Conservative Uncertainty

### Formal Statement

Let a state-cloud produce multiple plausible centers:

```text
P_t = {S_t^1, S_t^2, ..., S_t^k}
```

Each center has its own transition region:

```text
Ω_t^1, Ω_t^2, ..., Ω_t^k
```

Define the conservative safe region:

```text
Ω_safe = ⋂ Ω_t^m
```

A transition is robustly ALLOW only if:

```text
p_t ∈ Ω_safe
```

and:

```text
∀m, Permit_t^m(p_t) = ALLOW
```

Otherwise, the result is not robustly ALLOW and normally becomes FAIL_CLOSED unless a known violation supports DENY.

### Plain Meaning

The system cannot select only the state estimate that makes a desired transition look safe.

### Failure Mode

This obligation fails if a transition is ALLOW under one plausible center while another unresolved plausible center blocks it.

### Test Anchor

`problem_spec_chf_002.yml` validates that `pB` and `pC` FAIL_CLOSED under multi-center uncertainty.

---

## PO-004 — Local-Global Coupling

### Formal Statement

Let entity `i` propose transition `p_i` and pass local permission:

```text
Permit_i(p_i) = ALLOW
```

If `p_i` deforms affected entity `j`:

```text
D_{i→j}(p_i): C_j → C'_j
```

with deformation magnitude:

```text
δ_{i→j} = Dist(C_j, C'_j)
```

then coupled permission requires:

```text
δ_{i→j} ≤ ε_j
```

and, when recoverability is modeled:

```text
Recoverability_j(C'_j) ≥ θ_j
```

### Plain Meaning

A transition is not admissible merely because it is coherent for the actor. It must remain bounded for affected clouds.

### Failure Mode

This obligation fails if local ALLOW automatically implies global ALLOW.

### Test Anchor

`problem_spec_chf_003.yml` validates that local ALLOW for A becomes coupled DENY when B’s deformation tolerance or recoverability threshold is violated.

---

## PO-005 — Threshold Record

### Formal Statement

Every actualized crossing requires both a historical shell and a propagated record:

```text
χ_t ⇒ ∃Σ_t
χ_t ⇒ ∃ρ_t
```

Record legibility is separate from record existence:

```text
L(ρ_t) ∈ [0,1]
```

### Plain Meaning

An actualized transition must preserve:

1. a structured shell of what was evaluated, and
2. a propagated trace of what occurred.

The trace may become less readable over time without making the event unreal.

### Failure Mode

This obligation fails if an actualized transition has no shell, no record, or assumes all records remain permanently legible.

### Test Anchor

`problem_spec_chf_001.yml` validates that `p1` requires shell and record creation.

---

## PO-006 — Observer Projection

### Formal Statement

Let:

```text
Ω = ⋃ Cell_i
```

be a radially tessellated transition region.

An observer `O` has distinguishability:

```text
Q_O = Q(resolution, probe_capacity, distance, noise, lag)
```

If:

```text
Q_O < q_min
```

then `Ω` appears as a smooth or sphericalized shell.

If:

```text
Q_O ≥ q_min
```

then the cell structure can be resolved.

### Plain Meaning

Distance sphericalizes consequence. Resolution re-cellularizes it.

### Failure Mode

This obligation fails if different valid projections are treated as contradictions rather than resolution-dependent observations.

### Test Anchor

This is not yet implemented in CHF-001 through CHF-003. It is reserved for CHF-004.

---

## Current Proof Status

| ID | Name | Current Status | First Test Anchor |
|---|---|---|---|
| PO-001 | Radial Coverage | Ready for 2D validation | CHF-001 |
| PO-002 | Category Change | Ready for 2D validation | CHF-001 |
| PO-003 | Conservative Uncertainty | Ready for 2D validation | CHF-002 |
| PO-004 | Local-Global Coupling | Ready for 2D validation | CHF-003 |
| PO-005 | Threshold Record | Ready for 2D validation | CHF-001 |
| PO-006 | Observer Projection | Defined, not yet tested | CHF-004 future |
