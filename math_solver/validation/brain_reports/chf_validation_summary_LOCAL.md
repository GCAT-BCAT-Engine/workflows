# Consequence Horizon Formalism Validation Summary

- Overall status: **PASS**
- Specs evaluated: **13**

## Spec Results

### chf-001

- Status: **PASS**

- `p1`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `cell_rule_allows`
- `p2`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `cell_radius_limit_exceeded`
- `p3`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `forbidden_cell`
- `p4`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `uncertain_cell`
- `p5`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `outside_horizon`

### chf-002

- Status: **PASS**

- `pA`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `all_centers_pass`
- `pB`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `not_safe_across_all_plausible_centers`
- `pC`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `not_safe_across_all_plausible_centers`

### chf-003

- Status: **PASS**

- `chf-003`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `deformation_exceeds_tolerance`

### chf-004

- Status: **PASS**

- `O_far_low_resolution`: expected `SMOOTH_SHELL`, actual `SMOOTH_SHELL` — **PASS**
  - Reason: `observational_sphericalization`
- `O_near_high_resolution`: expected `CELL_RESOLVED`, actual `CELL_RESOLVED` — **PASS**
  - Reason: `cell_structure_resolved`
- `O_noisy_intermediate`: expected `SMOOTH_SHELL`, actual `SMOOTH_SHELL` — **PASS**
  - Reason: `observational_sphericalization`

### chf-005

- Status: **PASS**

- `chi_allow_legible`: expected `RECORD_LEGIBLE`, actual `RECORD_LEGIBLE` — **PASS**
  - Reason: `record_above_legibility_threshold`
- `chi_allow_low_legibility`: expected `RECORD_EXISTS_LOW_LEGIBILITY`, actual `RECORD_EXISTS_LOW_LEGIBILITY` — **PASS**
  - Reason: `record_exists_but_legibility_decayed`
- `denied_attempt`: expected `NO_PROPAGATED_RECORD_REQUIRED`, actual `NO_PROPAGATED_RECORD_REQUIRED` — **PASS**
  - Reason: `no_actualized_crossing`

### chf-006

- Status: **PASS**

- `v1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `stable_3d_radial_cell`
- `v2_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `authority_sensitive_3d_cell_denied`
- `v3_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `observer_impact_cell_unresolved`
- `v4_outside_horizon`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `outside_horizon`

### chf-007

- Status: **PASS**

- `convex_region_valid`: expected `GEOMETRY_VALID`, actual `GEOMETRY_VALID` — **PASS**
  - Reason: `radial_cell_coverage_valid`
- `region_with_hole`: expected `GEOMETRY_FAIL_CLOSED`, actual `GEOMETRY_FAIL_CLOSED` — **PASS**
  - Reason: `region_not_star_shaped`
- `incomplete_boundary_partition`: expected `GEOMETRY_FAIL_CLOSED`, actual `GEOMETRY_FAIL_CLOSED` — **PASS**
  - Reason: `boundary_partition_incomplete`

### chf-008

- Status: **PASS**

- `gcat_allow_balanced`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `gcat_invariant_satisfied`
- `gcat_deny_excess_autonomy`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `gcat_invariant_violated`
- `gcat_fail_closed_not_simplex`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `simplex_or_bounds_invalid`

### chf-009

- Status: **PASS**

- `commit_ready`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `commit_crossing_gcat_shell_record_ready`
- `commit_missing_shell`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `historical_shell_incomplete`
- `commit_gcat_violation`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `gcat_invariant_violated`

### chf-010

- Status: **PASS**

- `recoverable_purpose_converges`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `recoverability_and_purpose_converge`
- `recoverability_below_threshold`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `recoverability_below_threshold`
- `purpose_inversion`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `purpose_inversion_detected`

### chf-011

- Status: **PASS**

- `short_lag_inside_horizon`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `lag_reachable_set_inside_horizon`
- `long_lag_exceeds_horizon`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `lag_reachable_set_exceeds_horizon`
- `uncertainty_buffer_exceeds_horizon`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `lag_reachable_set_exceeds_horizon`

### chf-012

- Status: **PASS**

- `complete_chain_legible`: expected `CHAIN_CONTINUOUS`, actual `CHAIN_CONTINUOUS` — **PASS**
  - Reason: `historical_shell_chain_continuous`
- `missing_propagated_record_link`: expected `CHAIN_FAIL_CLOSED`, actual `CHAIN_FAIL_CLOSED` — **PASS**
  - Reason: `historical_chain_links_missing`
- `low_legibility_chain`: expected `CHAIN_FAIL_CLOSED`, actual `CHAIN_FAIL_CLOSED` — **PASS**
  - Reason: `historical_chain_legibility_below_threshold`

### chf-013

- Status: **PASS**

- `below_threshold_unprotected`: expected `NO_EFFECT`, actual `NO_EFFECT` — **PASS**
  - Reason: `below_relevance_threshold`
- `above_threshold_unprotected`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `deformation_exceeds_relevance_threshold`
- `below_threshold_protected`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `protected_cloud_requires_explicit_review`
- `unknown_deformation_protected`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `protected_affected_cloud_unknown_deformation`

