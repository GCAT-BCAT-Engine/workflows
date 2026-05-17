# Consequence Horizon Formalism Validation Summary

- Overall status: **PASS**
- Specs evaluated: **7**

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

