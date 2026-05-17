# CHF Validation Matrix

## CHF-001

| Case | Expected |
|---|---|
| p1 | ALLOW |
| p2 | DENY |
| p3 | DENY |
| p4 | FAIL_CLOSED |
| p5 | DENY |

## CHF-002

| Case | Expected |
|---|---|
| pA | ALLOW |
| pB | FAIL_CLOSED |
| pC | FAIL_CLOSED |

## CHF-003

| Case | Expected |
|---|---|
| chf-003 | DENY |

## CHF-004

| Case | Expected |
|---|---|
| O_far_low_resolution | SMOOTH_SHELL |
| O_near_high_resolution | CELL_RESOLVED |
| O_noisy_intermediate | SMOOTH_SHELL |

## CHF-005

| Case | Expected |
|---|---|
| chi_allow_legible | RECORD_LEGIBLE |
| chi_allow_low_legibility | RECORD_EXISTS_LOW_LEGIBILITY |
| denied_attempt | NO_PROPAGATED_RECORD_REQUIRED |

## CHF-006

| Case | Expected |
|---|---|
| v1_allow | ALLOW |
| v2_deny | DENY |
| v3_fail_closed | FAIL_CLOSED |
| v4_outside_horizon | DENY |

## CHF-007

| Case | Expected |
|---|---|
| convex_region_valid | GEOMETRY_VALID |
| region_with_hole | GEOMETRY_FAIL_CLOSED |
| incomplete_boundary_partition | GEOMETRY_FAIL_CLOSED |
