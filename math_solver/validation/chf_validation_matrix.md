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

## CHF-008

| Case | Expected |
|---|---|
| gcat_allow_balanced | ALLOW |
| gcat_deny_excess_autonomy | DENY |
| gcat_fail_closed_not_simplex | FAIL_CLOSED |

## CHF-009

| Case | Expected |
|---|---|
| commit_ready | ALLOW |
| commit_missing_shell | FAIL_CLOSED |
| commit_gcat_violation | DENY |

## CHF-010

| Case | Expected |
|---|---|
| recoverable_purpose_converges | ALLOW |
| recoverability_below_threshold | DENY |
| purpose_inversion | DENY |

## CHF-011

| Case | Expected |
|---|---|
| short_lag_inside_horizon | ALLOW |
| long_lag_exceeds_horizon | FAIL_CLOSED |
| uncertainty_buffer_exceeds_horizon | FAIL_CLOSED |

## CHF-012

| Case | Expected |
|---|---|
| complete_chain_legible | CHAIN_CONTINUOUS |
| missing_propagated_record_link | CHAIN_FAIL_CLOSED |
| low_legibility_chain | CHAIN_FAIL_CLOSED |

## CHF-013

| Case | Expected |
|---|---|
| below_threshold_unprotected | NO_EFFECT |
| above_threshold_unprotected | DENY |
| below_threshold_protected | FAIL_CLOSED |
| unknown_deformation_protected | FAIL_CLOSED |
