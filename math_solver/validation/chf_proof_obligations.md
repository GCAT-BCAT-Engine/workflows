# CHF Proof Obligations

## PO-001 — Radial Coverage

If a transition region is compact and star-shaped with respect to an operational center, and the represented boundary is partitioned into patches, coning each patch to the center should cover the transition region.

## PO-002 — Category Change

A transition point cannot become an actual next state unless a threshold crossing occurs.

## PO-003 — Conservative Uncertainty

Under multiple plausible centers, robust ALLOW requires the proposed transition to pass under every represented plausible center.

## PO-004 — Local-Global Coupling

Local ALLOW does not imply global ALLOW. Affected-cloud deformation and affected-entity recoverability must remain bounded.

## PO-005 — Threshold Record

Every actualized crossing produces a historical shell and propagated record. Record existence and record legibility are distinct.

## PO-006 — Observer Projection

The same radial tessellation may appear smooth or cell-resolved depending on observer distance, resolution, noise, lag, and probe capacity.

## PO-007 — 3D Radial Cell Assignment

The 3D model must assign transition vectors to radial cells using deterministic geometric criteria before applying cell-specific ALLOW, DENY, or FAIL_CLOSED rules.

## PO-008 — Star-Shaped Geometry Gate

The radial consequence cell model requires a star-shaped transition region with respect to the operational center. Non-star-shaped or incomplete geometry must fail closed before coverage is assumed.

## PO-009 — GCAT/BCAT Local Operator

GCAT/BCAT may serve as a local admissibility operator inside a radial consequence cell by evaluating the projected post-transition state.

## PO-010 — Commit Crossing Sufficiency

A commit crossing is only allowed when the projected state passes local admissibility and the historical shell and propagated record are ready.

## PO-011 — Recoverability and Purpose-Convergence

A transition can be denied when projected recoverability falls below threshold or when the transition inverts the purpose of the boundary it claims to support.

## PO-012 — Lag-Reachable Set Bound

A transition may only cross if the lag-reachable set remains inside the consequence horizon. Otherwise, the system must fail closed.

## PO-013 — Historical Shell Chain Continuity

A new transition sphere must remain linked to the historical shell, crossing event, propagated record, and new center that created it.

## PO-014 — Many-Body Relevance Threshold

Not every coupled deformation requires explicit governance. Deformations below relevance threshold may be NO_EFFECT unless protected status or unknown deformation requires review.
