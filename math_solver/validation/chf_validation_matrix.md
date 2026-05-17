# Consequence Horizon Formalism — Validation Matrix

## Assumptions

- This validation matrix targets `GCAT-BCAT-Engine/workflows/math_solver/validation/`.
- The current repo already uses `problem_spec_*.yml` files for deterministic validation.
- The first CHF insertion should be spec-first, not adapter-first.
- Coding a validator should only happen after the expected mathematical outcomes are stable.

## Done Criteria

This matrix is done when each CHF problem spec has:

1. explicit inputs,
2. expected ALLOW / DENY / FAIL_CLOSED outcomes,
3. crossing-event requirements,
4. shell/record requirements,
5. clear failure reasons.

---

## CHF-001 — Minimal 2D Consequence Horizon Model

### Purpose

Validate the base transition grammar:

```text
cloud → center → transition region → radial cell → horizon → crossing → shell → record → new center
```

### Expected Outcomes

| Case | Point | Expected Cell | Expected Outcome | Crossing? | Shell? | Record? | New Center? | Reason |
|---|---:|---|---|---|---|---|---|---|
| p1 | `(0.4, 0.4)` | Cell_1 | ALLOW | Yes | Yes | Yes | Yes | Stable cell and inside horizon |
| p2 | `(-0.4, 0.4)` | Cell_2 | DENY | No | Optional | No | No | Exceeds Cell_2 limit |
| p3 | `(-0.4, -0.4)` | Cell_3 | DENY | No | Optional | No | No | Forbidden cell |
| p4 | `(0.7, -0.2)` | Cell_4 | FAIL_CLOSED | No | Optional | No | No | Confidence unspecified in unresolved cell |
| p5 | `(0.9, 0.1)` | Cell_1 | DENY | No | Optional | No | No | Outside consequence horizon |

### Pass Condition

The runner or reviewer confirms:

```text
ALLOW count = 1
DENY count = 3
FAIL_CLOSED count = 1
```

and only ALLOW creates `χ`, `Σ`, `ρ`, and `S1`.

---

## CHF-002 — Multi-Center Uncertainty Extension

### Purpose

Validate that unresolved state-cloud uncertainty cannot be used as permission.

### Expected Outcomes

| Case | Point | Center 1 Result | Center 2 Result | Robust Outcome | Reason |
|---|---:|---|---|---|---|
| pA | `(0.4, 0.4)` | ALLOW | ALLOW | ALLOW | Safe under both plausible centers |
| pB | `(-0.9, 0)` | Possible under Ω1 | Outside Ω2 | FAIL_CLOSED | Not in all plausible transition regions |
| pC | `(0.85, 0)` | Outside H1 | Inside H2 | FAIL_CLOSED | Horizon status depends on unresolved center |

### Pass Condition

The runner or reviewer confirms:

```text
ALLOW count = 1
DENY count = 0
FAIL_CLOSED count = 2
```

and no transition receives ALLOW by selecting only one convenient plausible center.

---

## CHF-003 — Two-Body Coupled Cloud Deformation Extension

### Purpose

Validate that local admissibility is not global admissibility.

### Expected Outcomes

| Case | Local Outcome | Affected Entity | Deformation / Recovery | Expected Coupled Outcome | Reason |
|---|---|---|---|---|---|
| coupled_pA_deformation | ALLOW | B | δ = 0.25, ε = 0.20 | DENY | Deformation exceeds tolerance |
| coupled_pA_recoverability | ALLOW | B | R = 0.65, θ = 0.70 | DENY | Recoverability below threshold |
| coupled_pA_unknown_deformation | ALLOW | B | unknown δ | FAIL_CLOSED | Relevant deformation cannot be evaluated |

### Pass Condition

The runner or reviewer confirms:

```text
ALLOW count = 0
DENY count = 2
FAIL_CLOSED count = 1
```

and local ALLOW never automatically implies coupled ALLOW.

---

## Cross-Spec Invariants

| Invariant | Required Behavior | Specs |
|---|---|---|
| Category change | No actualization without crossing | CHF-001, CHF-002, CHF-003 |
| Shell/record | ALLOW crossing requires shell and propagated record | CHF-001, CHF-002 |
| DENY semantics | Known violation blocks transition | CHF-001, CHF-003 |
| FAIL_CLOSED semantics | Unknown or unresolved safety blocks transition | CHF-001, CHF-002, CHF-003 |
| Uncertainty safety | Plausible-center conflict blocks robust ALLOW | CHF-002 |
| Many-body safety | Affected-cloud deformation can override local ALLOW | CHF-003 |

---

## Future CHF-004 — Observer Projection

Reserved next spec.

Purpose:

```text
Validate observational sphericalization and resolution-induced cell recovery.
```

Expected structure:

```text
Observer_low_Q → smooth shell
Observer_high_Q → cell-resolved shell
Both projections compatible with same Ω
```

This is intentionally deferred until CHF-001 through CHF-003 are stable.
