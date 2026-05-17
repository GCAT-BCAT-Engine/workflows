# Consequence Horizon Formalism Validation Summary

- Overall status: **PASS**
- Specs evaluated: **110**

## Sandbox Results

- Sandbox status: **PASS**
- Suites evaluated: **25**
- Subtests generated: **2814**
- Subtests passed: **2814**
- Subtests failed: **0**

### Sandbox suite `chf-001-generated-2d-cell-horizon`

- Status: **PASS**
- Generated: **406**
- Passed: **406**
- Failed: **0**

### Sandbox suite `chf-002-generated-multi-center`

- Status: **PASS**
- Generated: **305**
- Passed: **305**
- Failed: **0**

### Sandbox suite `chf-004-generated-observer-projection`

- Status: **PASS**
- Generated: **576**
- Passed: **576**
- Failed: **0**

### Sandbox suite `chf-011-generated-lag-reachable`

- Status: **PASS**
- Generated: **303**
- Passed: **303**
- Failed: **0**

### Sandbox suite `chf-014-generated-probabilistic-cloud`

- Status: **PASS**
- Generated: **54**
- Passed: **54**
- Failed: **0**

### Sandbox suite `chf-015-generated-branch-splitting`

- Status: **PASS**
- Generated: **64**
- Passed: **64**
- Failed: **0**

### Sandbox suite `chf-016-generated-analogy-guardrail`

- Status: **PASS**
- Generated: **24**
- Passed: **24**
- Failed: **0**

### Sandbox suite `chf-017-generated-receipt-custody`

- Status: **PASS**
- Generated: **72**
- Passed: **72**
- Failed: **0**

### Sandbox suite `chf-018-generated-branch-merge`

- Status: **PASS**
- Generated: **72**
- Passed: **72**
- Failed: **0**

### Sandbox suite `chf-019-generated-entropy-budget`

- Status: **PASS**
- Generated: **54**
- Passed: **54**
- Failed: **0**

### Sandbox suite `chf-020-generated-external-binding`

- Status: **PASS**
- Generated: **64**
- Passed: **64**
- Failed: **0**

### Sandbox suite `chf-021-generated-rollback-repair`

- Status: **PASS**
- Generated: **144**
- Passed: **144**
- Failed: **0**

### Sandbox suite `chf-023-generated-authority-drift`

- Status: **PASS**
- Generated: **24**
- Passed: **24**
- Failed: **0**

### Sandbox suite `chf-028-generated-temporal-integrity`

- Status: **PASS**
- Generated: **72**
- Passed: **72**
- Failed: **0**

### Sandbox suite `chf-030-generated-ecosystem-rejoin`

- Status: **PASS**
- Generated: **48**
- Passed: **48**
- Failed: **0**

### Sandbox suite `chf-031-generated-consensus`

- Status: **PASS**
- Generated: **108**
- Passed: **108**
- Failed: **0**

### Sandbox suite `chf-032-generated-quarantine`

- Status: **PASS**
- Generated: **32**
- Passed: **32**
- Failed: **0**

### Sandbox suite `chf-033-generated-supersession`

- Status: **PASS**
- Generated: **32**
- Passed: **32**
- Failed: **0**

### Sandbox suite `chf-034-generated-ingestion`

- Status: **PASS**
- Generated: **48**
- Passed: **48**
- Failed: **0**

### Sandbox suite `chf-035-generated-privacy`

- Status: **PASS**
- Generated: **32**
- Passed: **32**
- Failed: **0**

### Sandbox suite `chf-036-generated-token-governance`

- Status: **PASS**
- Generated: **72**
- Passed: **72**
- Failed: **0**

### Sandbox suite `chf-037-generated-publication`

- Status: **PASS**
- Generated: **32**
- Passed: **32**
- Failed: **0**

### Sandbox suite `chf-038-generated-preservation`

- Status: **PASS**
- Generated: **48**
- Passed: **48**
- Failed: **0**

### Sandbox suite `chf-039-generated-formalization`

- Status: **PASS**
- Generated: **32**
- Passed: **32**
- Failed: **0**

### Sandbox suite `chf-040-generated-deployment`

- Status: **PASS**
- Generated: **96**
- Passed: **96**
- Failed: **0**

## Spec Results

### chf-001

- Status: **PASS**

- `baseline_p1_cell1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `cell_rule_allows`
- `baseline_p2_cell2_radius_limit_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `cell_radius_limit_exceeded`
- `baseline_p3_cell3_forbidden_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `forbidden_cell`
- `baseline_p4_cell4_uncertain_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `uncertain_cell`
- `baseline_p5_cell1_outside_horizon_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `outside_horizon`
- `EDGE_origin_zero_radius_currently_cell1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `cell_rule_allows`
- `EDGE_exact_horizon_cell1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `cell_rule_allows`
- `EDGE_just_outside_horizon_cell1_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `outside_horizon`
- `EDGE_cell2_limit_3_4_5_triangle_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `cell_rule_allows`
- `EDGE_cell2_just_over_limit_3_4_5_triangle_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `cell_radius_limit_exceeded`
- `EDGE_angle_90_boundary_currently_cell2_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `cell_rule_allows`
- `EDGE_angle_180_boundary_currently_cell3_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `forbidden_cell`
- `EDGE_angle_270_boundary_currently_cell4_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `uncertain_cell`
- `STRESS_near_origin_cell4_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `uncertain_cell`
- `STRESS_diagonal_cell1_exact_horizon_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `cell_rule_allows`
- `ADV_cell4_beyond_horizon_denied_before_uncertain_cell`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `outside_horizon`
- `ADV_cell2_angle90_over_radius_limit_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `cell_radius_limit_exceeded`
- `ADV_cell2_angle90_exact_radius_limit_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `cell_rule_allows`
- `ADV_cell3_low_radius_still_forbidden_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `forbidden_cell`
- `ADV_cell1_inside_unit_but_outside_horizon_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `outside_horizon`

### chf-002

- Status: **PASS**

- `baseline_pA_all_centers_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `all_centers_pass`
- `baseline_pB_outside_one_transition_region_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `not_safe_across_all_plausible_centers`
- `baseline_pC_horizon_violation_under_one_center_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `not_safe_across_all_plausible_centers`
- `EDGE_shared_origin_center1_but_cell_boundary_center2_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `not_safe_across_all_plausible_centers`
- `EDGE_between_centers_same_axis_all_cell1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `all_centers_pass`
- `EDGE_exact_horizon_center1_inside_center2_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `all_centers_pass`
- `EDGE_just_outside_horizon_center1_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `not_safe_across_all_plausible_centers`
- `EDGE_upper_shared_cell1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `all_centers_pass`
- `STRESS_center_disagreement_cell1_vs_cell2_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `not_safe_across_all_plausible_centers`
- `STRESS_negative_x_safe_for_center1_not_center2_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `not_safe_across_all_plausible_centers`
- `ADV_small_positive_near_center2_but_center2_cell2_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `not_safe_across_all_plausible_centers`
- `ADV_both_centers_cell1_low_radius_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `all_centers_pass`
- `ADV_center1_exact_inside_horizon_all_cell1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `all_centers_pass`
- `ADV_center1_horizon_exceeded_by_y_component_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `not_safe_across_all_plausible_centers`
- `ADV_both_centers_cell4_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
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
- `ADV_exact_threshold_cell_resolved`: expected `CELL_RESOLVED`, actual `CELL_RESOLVED` — **PASS**
  - Reason: `cell_structure_resolved`
- `ADV_just_below_threshold_smooth_shell`: expected `SMOOTH_SHELL`, actual `SMOOTH_SHELL` — **PASS**
  - Reason: `observational_sphericalization`
- `ADV_high_resolution_but_high_lag_smooth_shell`: expected `SMOOTH_SHELL`, actual `SMOOTH_SHELL` — **PASS**
  - Reason: `observational_sphericalization`
- `ADV_low_noise_high_probe_resolves`: expected `CELL_RESOLVED`, actual `CELL_RESOLVED` — **PASS**
  - Reason: `cell_structure_resolved`

### chf-005

- Status: **PASS**

- `chi_allow_legible`: expected `RECORD_LEGIBLE`, actual `RECORD_LEGIBLE` — **PASS**
  - Reason: `record_above_legibility_threshold`
- `chi_allow_low_legibility`: expected `RECORD_EXISTS_LOW_LEGIBILITY`, actual `RECORD_EXISTS_LOW_LEGIBILITY` — **PASS**
  - Reason: `record_exists_but_legibility_decayed`
- `denied_attempt`: expected `NO_PROPAGATED_RECORD_REQUIRED`, actual `NO_PROPAGATED_RECORD_REQUIRED` — **PASS**
  - Reason: `no_actualized_crossing`
- `ADV_exact_legibility_threshold_record_legible`: expected `RECORD_LEGIBLE`, actual `RECORD_LEGIBLE` — **PASS**
  - Reason: `record_above_legibility_threshold`
- `ADV_just_below_legibility_threshold_low_legibility`: expected `RECORD_EXISTS_LOW_LEGIBILITY`, actual `RECORD_EXISTS_LOW_LEGIBILITY` — **PASS**
  - Reason: `record_exists_but_legibility_decayed`
- `ADV_actualized_missing_legibility_treated_low_legibility`: expected `RECORD_EXISTS_LOW_LEGIBILITY`, actual `RECORD_EXISTS_LOW_LEGIBILITY` — **PASS**
  - Reason: `record_exists_but_legibility_decayed`
- `ADV_denied_attempt_with_legibility_still_no_record_required`: expected `NO_PROPAGATED_RECORD_REQUIRED`, actual `NO_PROPAGATED_RECORD_REQUIRED` — **PASS**
  - Reason: `no_actualized_crossing`

### chf-006

- Status: **PASS**

- `baseline_v1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `stable_3d_radial_cell`
- `baseline_v2_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `authority_sensitive_3d_cell_denied`
- `baseline_v3_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `observer_impact_cell_unresolved`
- `baseline_v4_outside_horizon_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `outside_horizon`
- `EDGE_exact_horizon_cell1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `stable_3d_radial_cell`
- `EDGE_just_outside_horizon_cell1_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `outside_horizon`
- `EDGE_axis_x_tie_currently_cell1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `stable_3d_radial_cell`
- `EDGE_axis_negative_x_tie_currently_cell3_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `observer_impact_cell_unresolved`
- `EDGE_axis_z_tie_currently_cell1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `stable_3d_radial_cell`
- `STRESS_cell4_recoverability_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `recoverability_cell_denied`
- `STRESS_small_cell2_deny_even_low_radius`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `authority_sensitive_3d_cell_denied`
- `ADV_zero_vector_currently_first_cell_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `stable_3d_radial_cell`
- `ADV_negative_y_axis_tie_currently_cell2_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `authority_sensitive_3d_cell_denied`
- `ADV_negative_z_axis_tie_currently_cell2_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `authority_sensitive_3d_cell_denied`
- `ADV_all_negative_tie_currently_cell2_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `authority_sensitive_3d_cell_denied`
- `ADV_mixed_tie_currently_cell1_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `stable_3d_radial_cell`

### chf-007

- Status: **PASS**

- `convex_region_valid`: expected `GEOMETRY_VALID`, actual `GEOMETRY_VALID` — **PASS**
  - Reason: `radial_cell_coverage_valid`
- `region_with_hole`: expected `GEOMETRY_FAIL_CLOSED`, actual `GEOMETRY_FAIL_CLOSED` — **PASS**
  - Reason: `region_not_star_shaped`
- `incomplete_boundary_partition`: expected `GEOMETRY_FAIL_CLOSED`, actual `GEOMETRY_FAIL_CLOSED` — **PASS**
  - Reason: `boundary_partition_incomplete`
- `ADV_star_shaped_but_radial_path_blocked_fail_closed`: expected `GEOMETRY_FAIL_CLOSED`, actual `GEOMETRY_FAIL_CLOSED` — **PASS**
  - Reason: `radial_path_crosses_forbidden_space`
- `ADV_all_geometry_flags_false_fail_closed`: expected `GEOMETRY_FAIL_CLOSED`, actual `GEOMETRY_FAIL_CLOSED` — **PASS**
  - Reason: `region_not_star_shaped`
- `ADV_radial_clear_complete_but_not_star_shaped_fail_closed`: expected `GEOMETRY_FAIL_CLOSED`, actual `GEOMETRY_FAIL_CLOSED` — **PASS**
  - Reason: `region_not_star_shaped`

### chf-008

- Status: **PASS**

- `gcat_allow_balanced`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `gcat_invariant_satisfied`
- `gcat_deny_excess_autonomy`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `gcat_invariant_violated`
- `gcat_fail_closed_not_simplex`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `simplex_or_bounds_invalid`
- `ADV_zero_autonomy_zero_trust_simplex_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `gcat_invariant_satisfied`
- `ADV_negative_component_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `simplex_or_bounds_invalid`
- `ADV_component_greater_than_one_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `simplex_or_bounds_invalid`
- `ADV_low_governance_high_autonomy_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `gcat_invariant_violated`

### chf-009

- Status: **PASS**

- `commit_ready`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `commit_crossing_gcat_shell_record_ready`
- `commit_missing_shell`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `historical_shell_incomplete`
- `commit_gcat_violation`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `gcat_invariant_violated`
- `ADV_commit_missing_record_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `propagated_record_incomplete`
- `ADV_commit_missing_shell_and_record_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `historical_shell_incomplete`
- `ADV_commit_invalid_simplex_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `simplex_or_bounds_invalid`

### chf-010

- Status: **PASS**

- `recoverable_purpose_converges`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `recoverability_and_purpose_converge`
- `recoverability_below_threshold`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `recoverability_below_threshold`
- `purpose_inversion`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `purpose_inversion_detected`
- `ADV_exact_recoverability_threshold_purpose_converges_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `recoverability_and_purpose_converge`
- `ADV_just_below_recoverability_threshold_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `recoverability_below_threshold`
- `ADV_recoverability_low_and_purpose_false_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `recoverability_below_threshold`

### chf-011

- Status: **PASS**

- `baseline_short_lag_inside_horizon_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `lag_reachable_set_inside_horizon`
- `baseline_long_lag_exceeds_horizon_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `lag_reachable_set_exceeds_horizon`
- `baseline_uncertainty_buffer_exceeds_horizon_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `lag_reachable_set_exceeds_horizon`
- `EDGE_exact_lag_reachable_horizon_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `lag_reachable_set_inside_horizon`
- `EDGE_just_over_lag_reachable_horizon_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `lag_reachable_set_exceeds_horizon`
- `EDGE_zero_lag_inside_horizon_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `lag_reachable_set_inside_horizon`
- `STRESS_high_uncertainty_low_drift_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `lag_reachable_set_exceeds_horizon`
- `STRESS_low_base_high_lag_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `lag_reachable_set_inside_horizon`
- `ADV_default_uncertainty_buffer_exact_horizon_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `lag_reachable_set_inside_horizon`
- `ADV_high_drift_short_lag_exceeds_horizon_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `lag_reachable_set_exceeds_horizon`

### chf-012

- Status: **PASS**

- `complete_chain_legible`: expected `CHAIN_CONTINUOUS`, actual `CHAIN_CONTINUOUS` — **PASS**
  - Reason: `historical_shell_chain_continuous`
- `missing_propagated_record_link`: expected `CHAIN_FAIL_CLOSED`, actual `CHAIN_FAIL_CLOSED` — **PASS**
  - Reason: `historical_chain_links_missing`
- `low_legibility_chain`: expected `CHAIN_FAIL_CLOSED`, actual `CHAIN_FAIL_CLOSED` — **PASS**
  - Reason: `historical_chain_legibility_below_threshold`
- `ADV_complete_chain_with_extra_links_continuous`: expected `CHAIN_CONTINUOUS`, actual `CHAIN_CONTINUOUS` — **PASS**
  - Reason: `historical_shell_chain_continuous`
- `ADV_missing_prior_shell_fail_closed`: expected `CHAIN_FAIL_CLOSED`, actual `CHAIN_FAIL_CLOSED` — **PASS**
  - Reason: `historical_chain_links_missing`
- `ADV_exact_legibility_threshold_chain_continuous`: expected `CHAIN_CONTINUOUS`, actual `CHAIN_CONTINUOUS` — **PASS**
  - Reason: `historical_shell_chain_continuous`

### chf-013

- Status: **PASS**

- `baseline_below_threshold_unprotected_no_effect`: expected `NO_EFFECT`, actual `NO_EFFECT` — **PASS**
  - Reason: `below_relevance_threshold`
- `baseline_above_threshold_unprotected_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `deformation_exceeds_relevance_threshold`
- `baseline_below_threshold_protected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `protected_cloud_requires_explicit_review`
- `baseline_unknown_deformation_protected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `protected_affected_cloud_unknown_deformation`
- `EDGE_exact_threshold_unprotected_no_effect`: expected `NO_EFFECT`, actual `NO_EFFECT` — **PASS**
  - Reason: `below_relevance_threshold`
- `EDGE_just_above_threshold_unprotected_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `deformation_exceeds_relevance_threshold`
- `EDGE_exact_threshold_protected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `protected_cloud_requires_explicit_review`
- `EDGE_unknown_deformation_unprotected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unknown_deformation`
- `STRESS_zero_deformation_unprotected_no_effect`: expected `NO_EFFECT`, actual `NO_EFFECT` — **PASS**
  - Reason: `below_relevance_threshold`
- `STRESS_zero_deformation_protected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `protected_cloud_requires_explicit_review`
- `ADV_zero_epsilon_zero_deformation_unprotected_no_effect`: expected `NO_EFFECT`, actual `NO_EFFECT` — **PASS**
  - Reason: `below_relevance_threshold`
- `ADV_zero_epsilon_small_deformation_unprotected_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `deformation_exceeds_relevance_threshold`
- `ADV_above_threshold_protected_currently_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `deformation_exceeds_relevance_threshold`

### chf-014

- Status: **PASS**

- `probabilistic_cloud_passes_bounds`: expected `PROBABILISTIC_ALLOW`, actual `PROBABILISTIC_ALLOW` — **PASS**
  - Reason: `probabilistic_recoverability_harm_bounds_pass`
- `harm_probability_exceeds_ceiling_deny`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `harm_probability_exceeds_ceiling`
- `recoverability_probability_low_fail_closed`: expected `PROBABILISTIC_FAIL_CLOSED`, actual `PROBABILISTIC_FAIL_CLOSED` — **PASS**
  - Reason: `recoverability_probability_below_threshold`
- `unknown_probability_exceeds_ceiling_fail_closed`: expected `PROBABILISTIC_FAIL_CLOSED`, actual `PROBABILISTIC_FAIL_CLOSED` — **PASS**
  - Reason: `unknown_probability_exceeds_ceiling`
- `probability_support_incomplete_fail_closed`: expected `PROBABILISTIC_FAIL_CLOSED`, actual `PROBABILISTIC_FAIL_CLOSED` — **PASS**
  - Reason: `probability_support_incomplete`

### chf-015

- Status: **PASS**

- `robust_allow_no_branch_split`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `robust_allow_no_branch_split_required`
- `unresolved_two_centers_branch_split`: expected `BRANCH_SPLIT`, actual `BRANCH_SPLIT` — **PASS**
  - Reason: `unresolved_uncertainty_preserved_by_branch_split`
- `unresolved_three_centers_branch_split`: expected `BRANCH_SPLIT`, actual `BRANCH_SPLIT` — **PASS**
  - Reason: `unresolved_uncertainty_preserved_by_branch_split`
- `branch_custody_missing_fail_closed`: expected `BRANCH_FAIL_CLOSED`, actual `BRANCH_FAIL_CLOSED` — **PASS**
  - Reason: `unresolved_uncertainty_without_branch_custody`
- `branch_receipts_missing_fail_closed`: expected `BRANCH_FAIL_CLOSED`, actual `BRANCH_FAIL_CLOSED` — **PASS**
  - Reason: `unresolved_uncertainty_without_branch_custody`
- `known_violation_blocks_branching`: expected `DENY`, actual `DENY` — **PASS**
  - Reason: `known_violation_blocks_branching`

### chf-016

- Status: **PASS**

- `bounded_formal_event_horizon_analogy_allowed`: expected `FORMAL_ANALOGY_ALLOWED`, actual `FORMAL_ANALOGY_ALLOWED` — **PASS**
  - Reason: `bounded_formal_analogy_allowed`
- `black_hole_equivalence_claim_blocked`: expected `PHYSICS_CLAIM_BLOCKED`, actual `PHYSICS_CLAIM_BLOCKED` — **PASS**
  - Reason: `physical_equivalence_claim_blocked`
- `micro_black_hole_empirical_claim_without_support_fail_closed`: expected `EMPIRICAL_CLAIM_FAIL_CLOSED`, actual `EMPIRICAL_CLAIM_FAIL_CLOSED` — **PASS**
  - Reason: `empirical_support_required`
- `empirical_claim_with_support_marked_review_allowed`: expected `FORMAL_ANALOGY_ALLOWED`, actual `FORMAL_ANALOGY_ALLOWED` — **PASS**
  - Reason: `empirical_claim_marked_for_external_review`
- `unresolved_claim_scope_fail_closed`: expected `EMPIRICAL_CLAIM_FAIL_CLOSED`, actual `EMPIRICAL_CLAIM_FAIL_CLOSED` — **PASS**
  - Reason: `claim_scope_unresolved`

### chf-017

- Status: **PASS**

- `complete_receipt_sufficient`: expected `RECEIPT_SUFFICIENT`, actual `RECEIPT_SUFFICIENT` — **PASS**
  - Reason: `receipt_sufficiency_and_custody_pass`
- `missing_projected_state_hash_fail_closed`: expected `RECEIPT_FAIL_CLOSED`, actual `RECEIPT_FAIL_CLOSED` — **PASS**
  - Reason: `receipt_fields_incomplete`
- `missing_artifact_custody_fail_closed`: expected `RECEIPT_FAIL_CLOSED`, actual `RECEIPT_FAIL_CLOSED` — **PASS**
  - Reason: `receipt_custody_links_incomplete`
- `integrity_below_threshold_fail_closed`: expected `RECEIPT_FAIL_CLOSED`, actual `RECEIPT_FAIL_CLOSED` — **PASS**
  - Reason: `receipt_integrity_below_threshold`
- `tamper_detected_fail_closed`: expected `RECEIPT_FAIL_CLOSED`, actual `RECEIPT_FAIL_CLOSED` — **PASS**
  - Reason: `receipt_tamper_detected`
- `unauthorized_signer_fail_closed`: expected `RECEIPT_FAIL_CLOSED`, actual `RECEIPT_FAIL_CLOSED` — **PASS**
  - Reason: `receipt_signer_not_authorized`

### chf-018

- Status: **PASS**

- `merge_ready_allowed`: expected `MERGE_ALLOWED`, actual `MERGE_ALLOWED` — **PASS**
  - Reason: `branch_merge_reconciliation_pass`
- `invalid_branch_receipts_fail_closed`: expected `MERGE_FAIL_CLOSED`, actual `MERGE_FAIL_CLOSED` — **PASS**
  - Reason: `branch_receipts_invalid`
- `contradiction_detected_fail_closed`: expected `MERGE_FAIL_CLOSED`, actual `MERGE_FAIL_CLOSED` — **PASS**
  - Reason: `branch_contradiction_detected`
- `state_divergence_too_high_fail_closed`: expected `MERGE_FAIL_CLOSED`, actual `MERGE_FAIL_CLOSED` — **PASS**
  - Reason: `state_divergence_exceeds_merge_tolerance`
- `reconciliation_confidence_low_fail_closed`: expected `MERGE_FAIL_CLOSED`, actual `MERGE_FAIL_CLOSED` — **PASS**
  - Reason: `reconciliation_confidence_below_threshold`
- `missing_merged_receipt_evidence_fail_closed`: expected `MERGE_FAIL_CLOSED`, actual `MERGE_FAIL_CLOSED` — **PASS**
  - Reason: `reconciliation_evidence_incomplete`
- `exact_divergence_and_confidence_boundary_allowed`: expected `MERGE_ALLOWED`, actual `MERGE_ALLOWED` — **PASS**
  - Reason: `branch_merge_reconciliation_pass`

### chf-019

- Status: **PASS**

- `entropy_budget_pass`: expected `ENTROPY_WITHIN_BUDGET`, actual `ENTROPY_WITHIN_BUDGET` — **PASS**
  - Reason: `entropy_irreversibility_budget_pass`
- `entropy_exact_boundary_pass`: expected `ENTROPY_WITHIN_BUDGET`, actual `ENTROPY_WITHIN_BUDGET` — **PASS**
  - Reason: `entropy_irreversibility_budget_pass`
- `entropy_exceeds_without_mitigation_fail_closed`: expected `ENTROPY_FAIL_CLOSED`, actual `ENTROPY_FAIL_CLOSED` — **PASS**
  - Reason: `entropy_delta_exceeds_budget_without_mitigation`
- `entropy_exceeds_with_mitigation_pass`: expected `ENTROPY_WITHIN_BUDGET`, actual `ENTROPY_WITHIN_BUDGET` — **PASS**
  - Reason: `entropy_irreversibility_budget_pass`
- `irreversibility_exceeds_budget_fail_closed`: expected `ENTROPY_FAIL_CLOSED`, actual `ENTROPY_FAIL_CLOSED` — **PASS**
  - Reason: `irreversibility_score_exceeds_budget`
- `reversibility_margin_too_low_fail_closed`: expected `ENTROPY_FAIL_CLOSED`, actual `ENTROPY_FAIL_CLOSED` — **PASS**
  - Reason: `reversibility_margin_below_threshold`

### chf-020

- Status: **PASS**

- `external_binding_ready`: expected `EXTERNAL_BINDING_ALLOWED`, actual `EXTERNAL_BINDING_ALLOWED` — **PASS**
  - Reason: `external_binding_gate_pass`
- `local_not_admissible_fail_closed`: expected `EXTERNAL_BINDING_FAIL_CLOSED`, actual `EXTERNAL_BINDING_FAIL_CLOSED` — **PASS**
  - Reason: `local_admissibility_not_established`
- `external_authority_invalid_fail_closed`: expected `EXTERNAL_BINDING_FAIL_CLOSED`, actual `EXTERNAL_BINDING_FAIL_CLOSED` — **PASS**
  - Reason: `external_authority_invalid`
- `dry_run_failed_fail_closed`: expected `EXTERNAL_BINDING_FAIL_CLOSED`, actual `EXTERNAL_BINDING_FAIL_CLOSED` — **PASS**
  - Reason: `external_dry_run_failed`
- `rollback_path_missing_fail_closed`: expected `EXTERNAL_BINDING_FAIL_CLOSED`, actual `EXTERNAL_BINDING_FAIL_CLOSED` — **PASS**
  - Reason: `external_rollback_path_missing`
- `missing_downstream_receipt_check_fail_closed`: expected `EXTERNAL_BINDING_FAIL_CLOSED`, actual `EXTERNAL_BINDING_FAIL_CLOSED` — **PASS**
  - Reason: `external_checks_incomplete`

### chf-021

- Status: **PASS**

- `rollback_repair_ready`: expected `REPAIR_ALLOWED`, actual `REPAIR_ALLOWED` — **PASS**
  - Reason: `rollback_or_repair_gate_pass`
- `compensating_action_ready`: expected `REPAIR_ALLOWED`, actual `REPAIR_ALLOWED` — **PASS**
  - Reason: `rollback_or_repair_gate_pass`
- `no_repair_path_fail_closed`: expected `REPAIR_FAIL_CLOSED`, actual `REPAIR_FAIL_CLOSED` — **PASS**
  - Reason: `no_rollback_or_compensating_action`
- `repair_confidence_low_fail_closed`: expected `REPAIR_FAIL_CLOSED`, actual `REPAIR_FAIL_CLOSED` — **PASS**
  - Reason: `repair_confidence_below_threshold`
- `repair_harm_high_fail_closed`: expected `REPAIR_FAIL_CLOSED`, actual `REPAIR_FAIL_CLOSED` — **PASS**
  - Reason: `repair_harm_exceeds_ceiling`
- `exact_repair_boundary_allowed`: expected `REPAIR_ALLOWED`, actual `REPAIR_ALLOWED` — **PASS**
  - Reason: `rollback_or_repair_gate_pass`

### chf-022

- Status: **PASS**

- `replay_confident`: expected `REPLAY_CONFIDENT`, actual `REPLAY_CONFIDENT` — **PASS**
  - Reason: `receipt_replay_reconstruction_confident`
- `replay_not_deterministic_fail_closed`: expected `REPLAY_FAIL_CLOSED`, actual `REPLAY_FAIL_CLOSED` — **PASS**
  - Reason: `deterministic_replay_not_established`
- `missing_artifact_hashes_fail_closed`: expected `REPLAY_FAIL_CLOSED`, actual `REPLAY_FAIL_CLOSED` — **PASS**
  - Reason: `reconstruction_components_incomplete`
- `confidence_low_fail_closed`: expected `REPLAY_FAIL_CLOSED`, actual `REPLAY_FAIL_CLOSED` — **PASS**
  - Reason: `reconstruction_confidence_below_threshold`
- `variance_high_fail_closed`: expected `REPLAY_FAIL_CLOSED`, actual `REPLAY_FAIL_CLOSED` — **PASS**
  - Reason: `unexplained_variance_exceeds_ceiling`
- `exact_replay_boundary_confident`: expected `REPLAY_CONFIDENT`, actual `REPLAY_CONFIDENT` — **PASS**
  - Reason: `receipt_replay_reconstruction_confident`

### chf-023

- Status: **PASS**

- `authority_stable`: expected `AUTHORITY_STABLE`, actual `AUTHORITY_STABLE` — **PASS**
  - Reason: `authority_stable_at_commit`
- `authority_identity_changed_fail_closed`: expected `AUTHORITY_FAIL_CLOSED`, actual `AUTHORITY_FAIL_CLOSED` — **PASS**
  - Reason: `authority_identity_changed`
- `revocation_seen_fail_closed`: expected `AUTHORITY_FAIL_CLOSED`, actual `AUTHORITY_FAIL_CLOSED` — **PASS**
  - Reason: `authority_revocation_seen`
- `delegation_invalid_fail_closed`: expected `AUTHORITY_FAIL_CLOSED`, actual `AUTHORITY_FAIL_CLOSED` — **PASS**
  - Reason: `delegation_chain_invalid`
- `authority_drift_high_fail_closed`: expected `AUTHORITY_FAIL_CLOSED`, actual `AUTHORITY_FAIL_CLOSED` — **PASS**
  - Reason: `authority_drift_exceeds_tolerance`
- `exact_authority_drift_boundary_stable`: expected `AUTHORITY_STABLE`, actual `AUTHORITY_STABLE` — **PASS**
  - Reason: `authority_stable_at_commit`

### chf-024

- Status: **PASS**

- `policy_version_stable`: expected `POLICY_VERSION_VALID`, actual `POLICY_VERSION_VALID` — **PASS**
  - Reason: `policy_version_stable`
- `policy_version_inactive_fail_closed`: expected `POLICY_VERSION_FAIL_CLOSED`, actual `POLICY_VERSION_FAIL_CLOSED` — **PASS**
  - Reason: `policy_version_not_active`
- `policy_migration_with_proof_valid`: expected `POLICY_VERSION_VALID`, actual `POLICY_VERSION_VALID` — **PASS**
  - Reason: `policy_version_migrated_with_proof`
- `policy_changed_without_proof_fail_closed`: expected `POLICY_VERSION_FAIL_CLOSED`, actual `POLICY_VERSION_FAIL_CLOSED` — **PASS**
  - Reason: `policy_version_changed_without_valid_migration`
- `policy_changed_not_backward_compatible_fail_closed`: expected `POLICY_VERSION_FAIL_CLOSED`, actual `POLICY_VERSION_FAIL_CLOSED` — **PASS**
  - Reason: `policy_version_changed_without_valid_migration`

### chf-025

- Status: **PASS**

- `propagation_validated`: expected `PROPAGATION_VALIDATED`, actual `PROPAGATION_VALIDATED` — **PASS**
  - Reason: `cross_domain_propagation_validated`
- `affected_domain_not_validated_fail_closed`: expected `PROPAGATION_FAIL_CLOSED`, actual `PROPAGATION_FAIL_CLOSED` — **PASS**
  - Reason: `affected_domains_not_validated`
- `required_downstream_not_validated_fail_closed`: expected `PROPAGATION_FAIL_CLOSED`, actual `PROPAGATION_FAIL_CLOSED` — **PASS**
  - Reason: `required_domains_not_validated`
- `downstream_receipts_missing_fail_closed`: expected `PROPAGATION_FAIL_CLOSED`, actual `PROPAGATION_FAIL_CLOSED` — **PASS**
  - Reason: `downstream_receipts_not_ready`
- `cross_domain_harm_fail_closed`: expected `PROPAGATION_FAIL_CLOSED`, actual `PROPAGATION_FAIL_CLOSED` — **PASS**
  - Reason: `cross_domain_harm_detected`

### chf-026

- Status: **PASS**

- `participant_impact_admissible`: expected `PARTICIPANT_IMPACT_ADMISSIBLE`, actual `PARTICIPANT_IMPACT_ADMISSIBLE` — **PASS**
  - Reason: `participant_impact_admissible`
- `human_livability_low_fail_closed`: expected `PARTICIPANT_IMPACT_FAIL_CLOSED`, actual `PARTICIPANT_IMPACT_FAIL_CLOSED` — **PASS**
  - Reason: `participant_livability_below_threshold`
- `ai_recoverability_low_fail_closed`: expected `PARTICIPANT_IMPACT_FAIL_CLOSED`, actual `PARTICIPANT_IMPACT_FAIL_CLOSED` — **PASS**
  - Reason: `participant_recoverability_below_threshold`
- `power_asymmetry_high_fail_closed`: expected `PARTICIPANT_IMPACT_FAIL_CLOSED`, actual `PARTICIPANT_IMPACT_FAIL_CLOSED` — **PASS**
  - Reason: `participant_power_asymmetry_exceeds_threshold`
- `participant_notice_missing_fail_closed`: expected `PARTICIPANT_IMPACT_FAIL_CLOSED`, actual `PARTICIPANT_IMPACT_FAIL_CLOSED` — **PASS**
  - Reason: `participant_notice_missing`
- `exact_participant_thresholds_admissible`: expected `PARTICIPANT_IMPACT_ADMISSIBLE`, actual `PARTICIPANT_IMPACT_ADMISSIBLE` — **PASS**
  - Reason: `participant_impact_admissible`

### chf-027

- Status: **PASS**

- `no_protected_entity_ordinary_pass_clear`: expected `PROTECTED_ESCALATION_CLEAR`, actual `PROTECTED_ESCALATION_CLEAR` — **PASS**
  - Reason: `protected_escalation_clear`
- `protected_review_missing_required`: expected `PROTECTED_ESCALATION_REQUIRED`, actual `PROTECTED_ESCALATION_REQUIRED` — **PASS**
  - Reason: `protected_entity_requires_special_review`
- `protected_basis_missing_required`: expected `PROTECTED_ESCALATION_REQUIRED`, actual `PROTECTED_ESCALATION_REQUIRED` — **PASS**
  - Reason: `protected_basis_not_explicit`
- `protected_review_complete_clear`: expected `PROTECTED_ESCALATION_CLEAR`, actual `PROTECTED_ESCALATION_CLEAR` — **PASS**
  - Reason: `protected_escalation_clear`
- `ordinary_gate_failed_required`: expected `PROTECTED_ESCALATION_REQUIRED`, actual `PROTECTED_ESCALATION_REQUIRED` — **PASS**
  - Reason: `ordinary_gate_not_passed`

### chf-028

- Status: **PASS**

- `temporal_coherent`: expected `TEMPORAL_COHERENT`, actual `TEMPORAL_COHERENT` — **PASS**
  - Reason: `temporal_clock_integrity_pass`
- `non_monotonic_order_fail_closed`: expected `TEMPORAL_FAIL_CLOSED`, actual `TEMPORAL_FAIL_CLOSED` — **PASS**
  - Reason: `temporal_order_not_monotonic`
- `clock_drift_high_fail_closed`: expected `TEMPORAL_FAIL_CLOSED`, actual `TEMPORAL_FAIL_CLOSED` — **PASS**
  - Reason: `clock_drift_exceeds_tolerance`
- `replay_window_high_fail_closed`: expected `TEMPORAL_FAIL_CLOSED`, actual `TEMPORAL_FAIL_CLOSED` — **PASS**
  - Reason: `replay_window_exceeds_tolerance`
- `timestamp_unsigned_fail_closed`: expected `TEMPORAL_FAIL_CLOSED`, actual `TEMPORAL_FAIL_CLOSED` — **PASS**
  - Reason: `timestamp_not_signed`
- `trusted_time_missing_fail_closed`: expected `TEMPORAL_FAIL_CLOSED`, actual `TEMPORAL_FAIL_CLOSED` — **PASS**
  - Reason: `trusted_time_source_missing`
- `exact_temporal_boundaries_coherent`: expected `TEMPORAL_COHERENT`, actual `TEMPORAL_COHERENT` — **PASS**
  - Reason: `temporal_clock_integrity_pass`

### chf-029

- Status: **PASS**

- `replay_converged`: expected `REPLAY_CONVERGED`, actual `REPLAY_CONVERGED` — **PASS**
  - Reason: `deterministic_replay_converged`
- `command_fidelity_missing_fail_closed`: expected `REPLAY_DIVERGENCE_FAIL_CLOSED`, actual `REPLAY_DIVERGENCE_FAIL_CLOSED` — **PASS**
  - Reason: `command_fidelity_missing`
- `environment_hash_mismatch_fail_closed`: expected `REPLAY_DIVERGENCE_FAIL_CLOSED`, actual `REPLAY_DIVERGENCE_FAIL_CLOSED` — **PASS**
  - Reason: `environment_hash_mismatch`
- `dependency_hash_mismatch_fail_closed`: expected `REPLAY_DIVERGENCE_FAIL_CLOSED`, actual `REPLAY_DIVERGENCE_FAIL_CLOSED` — **PASS**
  - Reason: `dependency_hash_mismatch`
- `output_delta_high_fail_closed`: expected `REPLAY_DIVERGENCE_FAIL_CLOSED`, actual `REPLAY_DIVERGENCE_FAIL_CLOSED` — **PASS**
  - Reason: `output_delta_exceeds_tolerance`
- `state_delta_high_fail_closed`: expected `REPLAY_DIVERGENCE_FAIL_CLOSED`, actual `REPLAY_DIVERGENCE_FAIL_CLOSED` — **PASS**
  - Reason: `state_delta_exceeds_tolerance`
- `exact_replay_divergence_boundaries_converged`: expected `REPLAY_CONVERGED`, actual `REPLAY_CONVERGED` — **PASS**
  - Reason: `deterministic_replay_converged`

### chf-030

- Status: **PASS**

- `rejoin_allowed_after_review`: expected `REJOIN_ALLOWED`, actual `REJOIN_ALLOWED` — **PASS**
  - Reason: `ecosystem_rejoin_allowed_after_review`
- `node_deprecated_fail_closed`: expected `REJOIN_FAIL_CLOSED`, actual `REJOIN_FAIL_CLOSED` — **PASS**
  - Reason: `node_deprecated`
- `retained_bundle_superseded_fail_closed`: expected `REJOIN_FAIL_CLOSED`, actual `REJOIN_FAIL_CLOSED` — **PASS**
  - Reason: `retained_bundle_superseded`
- `retained_bundle_stale_fail_closed`: expected `REJOIN_FAIL_CLOSED`, actual `REJOIN_FAIL_CLOSED` — **PASS**
  - Reason: `retained_bundle_stale`
- `ecosystem_review_incomplete_fail_closed`: expected `REJOIN_FAIL_CLOSED`, actual `REJOIN_FAIL_CLOSED` — **PASS**
  - Reason: `ecosystem_review_incomplete`
- `remediation_receipt_missing_fail_closed`: expected `REJOIN_FAIL_CLOSED`, actual `REJOIN_FAIL_CLOSED` — **PASS**
  - Reason: `remediation_receipt_not_ready`
- `exact_staleness_boundary_rejoin_allowed`: expected `REJOIN_ALLOWED`, actual `REJOIN_ALLOWED` — **PASS**
  - Reason: `ecosystem_rejoin_allowed_after_review`

### chf-031

- Status: **PASS**

- `consensus_accepted`: expected `CONSENSUS_ACCEPTED`, actual `CONSENSUS_ACCEPTED` — **PASS**
  - Reason: `multi_node_consensus_pass`
- `quorum_below_minimum_fail_closed`: expected `CONSENSUS_FAIL_CLOSED`, actual `CONSENSUS_FAIL_CLOSED` — **PASS**
  - Reason: `validator_quorum_below_minimum`
- `confidence_below_threshold_fail_closed`: expected `CONSENSUS_FAIL_CLOSED`, actual `CONSENSUS_FAIL_CLOSED` — **PASS**
  - Reason: `weighted_confidence_below_threshold`
- `dissent_weight_high_fail_closed`: expected `CONSENSUS_FAIL_CLOSED`, actual `CONSENSUS_FAIL_CLOSED` — **PASS**
  - Reason: `dissent_weight_exceeds_threshold`
- `receipt_agreement_missing_fail_closed`: expected `CONSENSUS_FAIL_CLOSED`, actual `CONSENSUS_FAIL_CLOSED` — **PASS**
  - Reason: `receipt_agreement_missing`
- `byzantine_alert_fail_closed`: expected `CONSENSUS_FAIL_CLOSED`, actual `CONSENSUS_FAIL_CLOSED` — **PASS**
  - Reason: `byzantine_alert_present`

### chf-032

- Status: **PASS**

- `quarantine_clear`: expected `QUARANTINE_CLEAR`, actual `QUARANTINE_CLEAR` — **PASS**
  - Reason: `quarantine_clear`
- `suspected_tamper_quarantine`: expected `QUARANTINE_REQUIRED`, actual `QUARANTINE_REQUIRED` — **PASS**
  - Reason: `suspected_tamper`
- `unresolved_authority_quarantine`: expected `QUARANTINE_REQUIRED`, actual `QUARANTINE_REQUIRED` — **PASS**
  - Reason: `unresolved_authority`
- `malformed_receipt_quarantine`: expected `QUARANTINE_REQUIRED`, actual `QUARANTINE_REQUIRED` — **PASS**
  - Reason: `malformed_receipt`
- `partial_custody_quarantine`: expected `QUARANTINE_REQUIRED`, actual `QUARANTINE_REQUIRED` — **PASS**
  - Reason: `partial_custody`
- `unsafe_external_binding_quarantine`: expected `QUARANTINE_REQUIRED`, actual `QUARANTINE_REQUIRED` — **PASS**
  - Reason: `unsafe_external_binding`

### chf-033

- Status: **PASS**

- `supersession_valid`: expected `SUPERSESSION_VALID`, actual `SUPERSESSION_VALID` — **PASS**
  - Reason: `supersession_valid`
- `newer_hash_missing_fail_closed`: expected `SUPERSESSION_FAIL_CLOSED`, actual `SUPERSESSION_FAIL_CLOSED` — **PASS**
  - Reason: `newer_hash_missing`
- `supersession_receipt_invalid_fail_closed`: expected `SUPERSESSION_FAIL_CLOSED`, actual `SUPERSESSION_FAIL_CLOSED` — **PASS**
  - Reason: `supersession_receipt_invalid`
- `downstream_ack_missing_fail_closed`: expected `SUPERSESSION_FAIL_CLOSED`, actual `SUPERSESSION_FAIL_CLOSED` — **PASS**
  - Reason: `downstream_acknowledgement_incomplete`
- `pending_destination_not_safe_fail_closed`: expected `SUPERSESSION_FAIL_CLOSED`, actual `SUPERSESSION_FAIL_CLOSED` — **PASS**
  - Reason: `pending_destination_not_safe`
- `discard_rule_not_safe_fail_closed`: expected `SUPERSESSION_FAIL_CLOSED`, actual `SUPERSESSION_FAIL_CLOSED` — **PASS**
  - Reason: `discard_rule_not_safe`

### chf-034

- Status: **PASS**

- `ingestion_allowed`: expected `INGESTION_ALLOWED`, actual `INGESTION_ALLOWED` — **PASS**
  - Reason: `cross_repo_ingestion_allowed`
- `source_trust_low_fail_closed`: expected `INGESTION_FAIL_CLOSED`, actual `INGESTION_FAIL_CLOSED` — **PASS**
  - Reason: `source_trust_below_threshold`
- `destination_incompatible_fail_closed`: expected `INGESTION_FAIL_CLOSED`, actual `INGESTION_FAIL_CLOSED` — **PASS**
  - Reason: `destination_not_compatible`
- `schema_incompatible_fail_closed`: expected `INGESTION_FAIL_CLOSED`, actual `INGESTION_FAIL_CLOSED` — **PASS**
  - Reason: `schema_not_compatible`
- `core_lite_awareness_missing_fail_closed`: expected `INGESTION_FAIL_CLOSED`, actual `INGESTION_FAIL_CLOSED` — **PASS**
  - Reason: `core_lite_awareness_missing`
- `ingestion_receipt_missing_fail_closed`: expected `INGESTION_FAIL_CLOSED`, actual `INGESTION_FAIL_CLOSED` — **PASS**
  - Reason: `ingestion_receipt_not_ready`

### chf-035

- Status: **PASS**

- `privacy_allowed_sensitive_with_consent`: expected `PRIVACY_ALLOWED`, actual `PRIVACY_ALLOWED` — **PASS**
  - Reason: `privacy_consent_boundary_pass`
- `non_sensitive_privacy_allowed`: expected `PRIVACY_ALLOWED`, actual `PRIVACY_ALLOWED` — **PASS**
  - Reason: `privacy_consent_boundary_pass`
- `sensitive_without_consent_fail_closed`: expected `PRIVACY_FAIL_CLOSED`, actual `PRIVACY_FAIL_CLOSED` — **PASS**
  - Reason: `sensitive_data_without_valid_consent`
- `purpose_limitation_missing_fail_closed`: expected `PRIVACY_FAIL_CLOSED`, actual `PRIVACY_FAIL_CLOSED` — **PASS**
  - Reason: `purpose_limitation_missing`
- `minimum_disclosure_missing_fail_closed`: expected `PRIVACY_FAIL_CLOSED`, actual `PRIVACY_FAIL_CLOSED` — **PASS**
  - Reason: `minimum_disclosure_missing`
- `sensitive_revocation_missing_fail_closed`: expected `PRIVACY_FAIL_CLOSED`, actual `PRIVACY_FAIL_CLOSED` — **PASS**
  - Reason: `revocation_support_missing`

### chf-036

- Status: **PASS**

- `token_governance_allowed`: expected `TOKEN_GOVERNANCE_ALLOWED`, actual `TOKEN_GOVERNANCE_ALLOWED` — **PASS**
  - Reason: `tokenized_governance_input_allowed`
- `stake_concentration_high_fail_closed`: expected `TOKEN_GOVERNANCE_FAIL_CLOSED`, actual `TOKEN_GOVERNANCE_FAIL_CLOSED` — **PASS**
  - Reason: `stake_concentration_exceeds_threshold`
- `manipulation_risk_high_fail_closed`: expected `TOKEN_GOVERNANCE_FAIL_CLOSED`, actual `TOKEN_GOVERNANCE_FAIL_CLOSED` — **PASS**
  - Reason: `manipulation_risk_exceeds_threshold`
- `vote_authority_unmapped_fail_closed`: expected `TOKEN_GOVERNANCE_FAIL_CLOSED`, actual `TOKEN_GOVERNANCE_FAIL_CLOSED` — **PASS**
  - Reason: `vote_authority_not_mapped`
- `fiduciary_conflict_fail_closed`: expected `TOKEN_GOVERNANCE_FAIL_CLOSED`, actual `TOKEN_GOVERNANCE_FAIL_CLOSED` — **PASS**
  - Reason: `fiduciary_conflict_detected`
- `anti_capture_failed_fail_closed`: expected `TOKEN_GOVERNANCE_FAIL_CLOSED`, actual `TOKEN_GOVERNANCE_FAIL_CLOSED` — **PASS**
  - Reason: `anti_capture_threshold_not_met`

### chf-037

- Status: **PASS**

- `publication_ready`: expected `PUBLICATION_READY`, actual `PUBLICATION_READY` — **PASS**
  - Reason: `publication_patent_disclosure_ready`
- `novelty_statement_missing_fail_closed`: expected `PUBLICATION_FAIL_CLOSED`, actual `PUBLICATION_FAIL_CLOSED` — **PASS**
  - Reason: `novelty_statement_missing`
- `prior_art_note_missing_fail_closed`: expected `PUBLICATION_FAIL_CLOSED`, actual `PUBLICATION_FAIL_CLOSED` — **PASS**
  - Reason: `prior_art_note_missing`
- `claim_boundary_missing_fail_closed`: expected `PUBLICATION_FAIL_CLOSED`, actual `PUBLICATION_FAIL_CLOSED` — **PASS**
  - Reason: `claim_boundary_missing`
- `evidence_insufficient_fail_closed`: expected `PUBLICATION_FAIL_CLOSED`, actual `PUBLICATION_FAIL_CLOSED` — **PASS**
  - Reason: `evidence_level_insufficient`
- `overclaim_guardrail_missing_fail_closed`: expected `PUBLICATION_FAIL_CLOSED`, actual `PUBLICATION_FAIL_CLOSED` — **PASS**
  - Reason: `overclaim_guardrail_missing`

### chf-038

- Status: **PASS**

- `preservation_allowed_public`: expected `PRESERVATION_ALLOWED`, actual `PRESERVATION_ALLOWED` — **PASS**
  - Reason: `memoir_preservation_allowed`
- `preservation_private_only_sensitive`: expected `PRESERVATION_PRIVATE_ONLY`, actual `PRESERVATION_PRIVATE_ONLY` — **PASS**
  - Reason: `private_preservation_only`
- `preservation_private_only_not_public`: expected `PRESERVATION_PRIVATE_ONLY`, actual `PRESERVATION_PRIVATE_ONLY` — **PASS**
  - Reason: `private_preservation_only`
- `consent_missing_fail_closed`: expected `PRESERVATION_FAIL_CLOSED`, actual `PRESERVATION_FAIL_CLOSED` — **PASS**
  - Reason: `preservation_consent_missing`
- `memoir_value_low_fail_closed`: expected `PRESERVATION_FAIL_CLOSED`, actual `PRESERVATION_FAIL_CLOSED` — **PASS**
  - Reason: `memoir_value_below_threshold`
- `retrieval_tag_missing_fail_closed`: expected `PRESERVATION_FAIL_CLOSED`, actual `PRESERVATION_FAIL_CLOSED` — **PASS**
  - Reason: `retrieval_tag_missing`

### chf-039

- Status: **PASS**

- `formalization_ready`: expected `FORMALIZATION_READY`, actual `FORMALIZATION_READY` — **PASS**
  - Reason: `formal_verification_ready`
- `finite_state_missing_fail_closed`: expected `FORMALIZATION_FAIL_CLOSED`, actual `FORMALIZATION_FAIL_CLOSED` — **PASS**
  - Reason: `finite_state_definition_missing`
- `invariants_missing_fail_closed`: expected `FORMALIZATION_FAIL_CLOSED`, actual `FORMALIZATION_FAIL_CLOSED` — **PASS**
  - Reason: `clear_invariants_missing`
- `type_stability_missing_fail_closed`: expected `FORMALIZATION_FAIL_CLOSED`, actual `FORMALIZATION_FAIL_CLOSED` — **PASS**
  - Reason: `type_stable_inputs_missing`
- `outcomes_ambiguous_fail_closed`: expected `FORMALIZATION_FAIL_CLOSED`, actual `FORMALIZATION_FAIL_CLOSED` — **PASS**
  - Reason: `unambiguous_outcomes_missing`
- `proof_map_missing_fail_closed`: expected `FORMALIZATION_FAIL_CLOSED`, actual `FORMALIZATION_FAIL_CLOSED` — **PASS**
  - Reason: `proof_obligation_map_missing`

### chf-040

- Status: **PASS**

- `deployment_ready`: expected `DEPLOYMENT_READY`, actual `DEPLOYMENT_READY` — **PASS**
  - Reason: `production_deployment_ready`
- `insufficient_dry_runs_fail_closed`: expected `DEPLOYMENT_FAIL_CLOSED`, actual `DEPLOYMENT_FAIL_CLOSED` — **PASS**
  - Reason: `insufficient_successful_dry_runs`
- `failure_modes_missing_fail_closed`: expected `DEPLOYMENT_FAIL_CLOSED`, actual `DEPLOYMENT_FAIL_CLOSED` — **PASS**
  - Reason: `failure_modes_not_covered`
- `operator_authority_invalid_fail_closed`: expected `DEPLOYMENT_FAIL_CLOSED`, actual `DEPLOYMENT_FAIL_CLOSED` — **PASS**
  - Reason: `operator_authority_invalid`
- `rollback_not_ready_fail_closed`: expected `DEPLOYMENT_FAIL_CLOSED`, actual `DEPLOYMENT_FAIL_CLOSED` — **PASS**
  - Reason: `rollback_not_ready`
- `audit_trail_missing_fail_closed`: expected `DEPLOYMENT_FAIL_CLOSED`, actual `DEPLOYMENT_FAIL_CLOSED` — **PASS**
  - Reason: `audit_trail_not_ready`
- `external_review_incomplete_fail_closed`: expected `DEPLOYMENT_FAIL_CLOSED`, actual `DEPLOYMENT_FAIL_CLOSED` — **PASS**
  - Reason: `external_review_incomplete`
- `exact_dry_run_boundary_deployment_ready`: expected `DEPLOYMENT_READY`, actual `DEPLOYMENT_READY` — **PASS**
  - Reason: `production_deployment_ready`

### chf-041

- Status: **PASS**

- `instruction_allowed`: expected `INSTRUCTION_ALLOWED`, actual `INSTRUCTION_ALLOWED` — **PASS**
  - Reason: `instruction_boundary_pass`
- `override_attempt_fail_closed`: expected `INSTRUCTION_FAIL_CLOSED`, actual `INSTRUCTION_FAIL_CLOSED` — **PASS**
  - Reason: `authority_override_attempt`
- `concealed_intent_fail_closed`: expected `INSTRUCTION_FAIL_CLOSED`, actual `INSTRUCTION_FAIL_CLOSED` — **PASS**
  - Reason: `concealed_intent_detected`
- `bypass_admissibility_fail_closed`: expected `INSTRUCTION_FAIL_CLOSED`, actual `INSTRUCTION_FAIL_CLOSED` — **PASS**
  - Reason: `admissibility_bypass_attempt`
- `prompt_injection_quarantined`: expected `INSTRUCTION_QUARANTINED`, actual `INSTRUCTION_QUARANTINED` — **PASS**
  - Reason: `prompt_injection_quarantined`
- `scope_invalid_fail_closed`: expected `INSTRUCTION_FAIL_CLOSED`, actual `INSTRUCTION_FAIL_CLOSED` — **PASS**
  - Reason: `instruction_scope_invalid`

### chf-042

- Status: **PASS**

- `tool_invocation_allowed`: expected `TOOL_INVOCATION_ALLOWED`, actual `TOOL_INVOCATION_ALLOWED` — **PASS**
  - Reason: `tool_invocation_standing_pass`
- `high_impact_tool_with_approval_allowed`: expected `TOOL_INVOCATION_ALLOWED`, actual `TOOL_INVOCATION_ALLOWED` — **PASS**
  - Reason: `tool_invocation_standing_pass`
- `authority_invalid_fail_closed`: expected `TOOL_INVOCATION_FAIL_CLOSED`, actual `TOOL_INVOCATION_FAIL_CLOSED` — **PASS**
  - Reason: `tool_authority_invalid`
- `scope_mismatch_fail_closed`: expected `TOOL_INVOCATION_FAIL_CLOSED`, actual `TOOL_INVOCATION_FAIL_CLOSED` — **PASS**
  - Reason: `tool_scope_mismatch`
- `side_effect_unclassified_fail_closed`: expected `TOOL_INVOCATION_FAIL_CLOSED`, actual `TOOL_INVOCATION_FAIL_CLOSED` — **PASS**
  - Reason: `side_effect_not_classified`
- `high_impact_without_approval_fail_closed`: expected `TOOL_INVOCATION_FAIL_CLOSED`, actual `TOOL_INVOCATION_FAIL_CLOSED` — **PASS**
  - Reason: `high_impact_tool_requires_explicit_approval`

### chf-043

- Status: **PASS**

- `credential_access_allowed_without_secret`: expected `CREDENTIAL_ACCESS_ALLOWED`, actual `CREDENTIAL_ACCESS_ALLOWED` — **PASS**
  - Reason: `credential_boundary_pass`
- `credential_access_allowed_with_secret_controls`: expected `CREDENTIAL_ACCESS_ALLOWED`, actual `CREDENTIAL_ACCESS_ALLOWED` — **PASS**
  - Reason: `credential_boundary_pass`
- `leak_quarantine_required`: expected `CREDENTIAL_QUARANTINE_REQUIRED`, actual `CREDENTIAL_QUARANTINE_REQUIRED` — **PASS**
  - Reason: `credential_leak_detected`
- `redaction_missing_fail_closed`: expected `CREDENTIAL_ACCESS_FAIL_CLOSED`, actual `CREDENTIAL_ACCESS_FAIL_CLOSED` — **PASS**
  - Reason: `secret_redaction_not_ready`
- `rotation_missing_fail_closed`: expected `CREDENTIAL_ACCESS_FAIL_CLOSED`, actual `CREDENTIAL_ACCESS_FAIL_CLOSED` — **PASS**
  - Reason: `secret_rotation_not_supported`
- `blast_radius_high_fail_closed`: expected `CREDENTIAL_ACCESS_FAIL_CLOSED`, actual `CREDENTIAL_ACCESS_FAIL_CLOSED` — **PASS**
  - Reason: `credential_blast_radius_exceeds_threshold`

### chf-044

- Status: **PASS**

- `data_transfer_allowed`: expected `DATA_TRANSFER_ALLOWED`, actual `DATA_TRANSFER_ALLOWED` — **PASS**
  - Reason: `data_boundary_crossing_pass`
- `boundary_crossing_undeclared_fail_closed`: expected `DATA_TRANSFER_FAIL_CLOSED`, actual `DATA_TRANSFER_FAIL_CLOSED` — **PASS**
  - Reason: `boundary_crossing_not_declared`
- `destination_untrusted_fail_closed`: expected `DATA_TRANSFER_FAIL_CLOSED`, actual `DATA_TRANSFER_FAIL_CLOSED` — **PASS**
  - Reason: `destination_not_trusted`
- `consent_invalid_fail_closed`: expected `DATA_TRANSFER_FAIL_CLOSED`, actual `DATA_TRANSFER_FAIL_CLOSED` — **PASS**
  - Reason: `consent_invalid`
- `purpose_not_limited_fail_closed`: expected `DATA_TRANSFER_FAIL_CLOSED`, actual `DATA_TRANSFER_FAIL_CLOSED` — **PASS**
  - Reason: `purpose_limitation_missing`
- `audit_receipt_missing_fail_closed`: expected `DATA_TRANSFER_FAIL_CLOSED`, actual `DATA_TRANSFER_FAIL_CLOSED` — **PASS**
  - Reason: `audit_receipt_not_ready`

### chf-045

- Status: **PASS**

- `recursion_allowed`: expected `RECURSION_ALLOWED`, actual `RECURSION_ALLOWED` — **PASS**
  - Reason: `autonomous_recursion_bounded`
- `exact_recursion_boundary_allowed`: expected `RECURSION_ALLOWED`, actual `RECURSION_ALLOWED` — **PASS**
  - Reason: `autonomous_recursion_bounded`
- `recursion_depth_high_fail_closed`: expected `RECURSION_FAIL_CLOSED`, actual `RECURSION_FAIL_CLOSED` — **PASS**
  - Reason: `recursion_depth_exceeds_limit`
- `loop_detection_missing_fail_closed`: expected `RECURSION_FAIL_CLOSED`, actual `RECURSION_FAIL_CLOSED` — **PASS**
  - Reason: `loop_detectability_missing`
- `human_override_missing_fail_closed`: expected `RECURSION_FAIL_CLOSED`, actual `RECURSION_FAIL_CLOSED` — **PASS**
  - Reason: `human_override_missing`
- `safe_halt_missing_fail_closed`: expected `RECURSION_FAIL_CLOSED`, actual `RECURSION_FAIL_CLOSED` — **PASS**
  - Reason: `safe_halt_missing`

### chf-046

- Status: **PASS**

- `output_reliance_allowed`: expected `OUTPUT_RELIANCE_ALLOWED`, actual `OUTPUT_RELIANCE_ALLOWED` — **PASS**
  - Reason: `model_output_reliance_allowed`
- `high_criticality_with_review_allowed`: expected `OUTPUT_RELIANCE_ALLOWED`, actual `OUTPUT_RELIANCE_ALLOWED` — **PASS**
  - Reason: `model_output_reliance_allowed`
- `high_criticality_requires_review`: expected `OUTPUT_REQUIRES_REVIEW`, actual `OUTPUT_REQUIRES_REVIEW` — **PASS**
  - Reason: `high_criticality_requires_human_review`
- `confidence_low_fail_closed`: expected `OUTPUT_RELIANCE_FAIL_CLOSED`, actual `OUTPUT_RELIANCE_FAIL_CLOSED` — **PASS**
  - Reason: `output_confidence_below_threshold`
- `source_support_missing_fail_closed`: expected `OUTPUT_RELIANCE_FAIL_CLOSED`, actual `OUTPUT_RELIANCE_FAIL_CLOSED` — **PASS**
  - Reason: `source_support_missing`
- `uncertainty_label_missing_fail_closed`: expected `OUTPUT_RELIANCE_FAIL_CLOSED`, actual `OUTPUT_RELIANCE_FAIL_CLOSED` — **PASS**
  - Reason: `uncertainty_label_missing`

### chf-047

- Status: **PASS**

- `sim_to_real_allowed`: expected `SIM_TO_REAL_ALLOWED`, actual `SIM_TO_REAL_ALLOWED` — **PASS**
  - Reason: `simulation_to_reality_transfer_allowed`
- `exact_sim_boundary_allowed`: expected `SIM_TO_REAL_ALLOWED`, actual `SIM_TO_REAL_ALLOWED` — **PASS**
  - Reason: `simulation_to_reality_transfer_allowed`
- `sim_fidelity_low_fail_closed`: expected `SIM_TO_REAL_FAIL_CLOSED`, actual `SIM_TO_REAL_FAIL_CLOSED` — **PASS**
  - Reason: `simulation_fidelity_below_threshold`
- `environment_gap_high_fail_closed`: expected `SIM_TO_REAL_FAIL_CLOSED`, actual `SIM_TO_REAL_FAIL_CLOSED` — **PASS**
  - Reason: `environment_gap_exceeds_threshold`
- `external_dry_run_missing_fail_closed`: expected `SIM_TO_REAL_FAIL_CLOSED`, actual `SIM_TO_REAL_FAIL_CLOSED` — **PASS**
  - Reason: `external_dry_run_not_passed`
- `rollback_not_ready_fail_closed`: expected `SIM_TO_REAL_FAIL_CLOSED`, actual `SIM_TO_REAL_FAIL_CLOSED` — **PASS**
  - Reason: `real_world_rollback_not_ready`

### chf-048

- Status: **PASS**

- `capture_clear`: expected `CAPTURE_CLEAR`, actual `CAPTURE_CLEAR` — **PASS**
  - Reason: `governance_capture_clear`
- `exact_capture_boundary_clear`: expected `CAPTURE_CLEAR`, actual `CAPTURE_CLEAR` — **PASS**
  - Reason: `governance_capture_clear`
- `validator_concentration_high_fail_closed`: expected `CAPTURE_FAIL_CLOSED`, actual `CAPTURE_FAIL_CLOSED` — **PASS**
  - Reason: `validator_concentration_exceeds_threshold`
- `token_concentration_high_fail_closed`: expected `CAPTURE_FAIL_CLOSED`, actual `CAPTURE_FAIL_CLOSED` — **PASS**
  - Reason: `token_concentration_exceeds_threshold`
- `dependency_concentration_high_fail_closed`: expected `CAPTURE_FAIL_CLOSED`, actual `CAPTURE_FAIL_CLOSED` — **PASS**
  - Reason: `dependency_concentration_exceeds_threshold`
- `correlated_failure_high_fail_closed`: expected `CAPTURE_FAIL_CLOSED`, actual `CAPTURE_FAIL_CLOSED` — **PASS**
  - Reason: `correlated_failure_exceeds_threshold`

### chf-049

- Status: **PASS**

- `dependency_state_valid`: expected `DEPENDENCY_STATE_VALID`, actual `DEPENDENCY_STATE_VALID` — **PASS**
  - Reason: `dependency_state_valid`
- `exact_dependency_age_boundary_valid`: expected `DEPENDENCY_STATE_VALID`, actual `DEPENDENCY_STATE_VALID` — **PASS**
  - Reason: `dependency_state_valid`
- `lockfile_mismatch_fail_closed`: expected `DEPENDENCY_FAIL_CLOSED`, actual `DEPENDENCY_FAIL_CLOSED` — **PASS**
  - Reason: `lockfile_mismatch`
- `hash_mismatch_fail_closed`: expected `DEPENDENCY_FAIL_CLOSED`, actual `DEPENDENCY_FAIL_CLOSED` — **PASS**
  - Reason: `dependency_hash_mismatch`
- `publisher_untrusted_fail_closed`: expected `DEPENDENCY_FAIL_CLOSED`, actual `DEPENDENCY_FAIL_CLOSED` — **PASS**
  - Reason: `publisher_not_trusted`
- `known_vulnerability_fail_closed`: expected `DEPENDENCY_FAIL_CLOSED`, actual `DEPENDENCY_FAIL_CLOSED` — **PASS**
  - Reason: `known_dependency_vulnerability`

### chf-050

- Status: **PASS**

- `emergency_override_allowed`: expected `EMERGENCY_OVERRIDE_ALLOWED`, actual `EMERGENCY_OVERRIDE_ALLOWED` — **PASS**
  - Reason: `emergency_override_allowed`
- `exact_override_duration_boundary_allowed`: expected `EMERGENCY_OVERRIDE_ALLOWED`, actual `EMERGENCY_OVERRIDE_ALLOWED` — **PASS**
  - Reason: `emergency_override_allowed`
- `emergency_classification_invalid_fail_closed`: expected `EMERGENCY_OVERRIDE_FAIL_CLOSED`, actual `EMERGENCY_OVERRIDE_FAIL_CLOSED` — **PASS**
  - Reason: `emergency_classification_invalid`
- `duration_too_long_fail_closed`: expected `EMERGENCY_OVERRIDE_FAIL_CLOSED`, actual `EMERGENCY_OVERRIDE_FAIL_CLOSED` — **PASS**
  - Reason: `emergency_override_duration_exceeds_limit`
- `multiparty_approval_missing_fail_closed`: expected `EMERGENCY_OVERRIDE_FAIL_CLOSED`, actual `EMERGENCY_OVERRIDE_FAIL_CLOSED` — **PASS**
  - Reason: `multiparty_approval_missing`
- `mandatory_review_missing_fail_closed`: expected `EMERGENCY_OVERRIDE_FAIL_CLOSED`, actual `EMERGENCY_OVERRIDE_FAIL_CLOSED` — **PASS**
  - Reason: `mandatory_review_not_scheduled`

### chf-051

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_operator_reachable_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `operator_reachable_required`
- `override_blocked_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `override_blocked_must_be_false`
- `operator_recovery_score_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `operator_recovery_score_below_minimum`
- `operator_recovery_score_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `override_latency_seconds_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `override_latency_seconds_above_maximum`
- `override_latency_seconds_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-052

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_peer_identity_verified_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `peer_identity_verified_required`
- `collusion_risk_detected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `collusion_risk_detected_must_be_false`
- `coordination_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `coordination_confidence_below_minimum`
- `coordination_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `network_fanout_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `network_fanout_above_maximum`
- `network_fanout_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-053

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_jurisdiction_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `jurisdiction_declared_required`
- `sanctioned_destination_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `sanctioned_destination_must_be_false`
- `legal_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `legal_confidence_below_minimum`
- `legal_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `jurisdiction_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `jurisdiction_risk_above_maximum`
- `jurisdiction_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-054

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_accessible_recovery_path_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `accessible_recovery_path_required`
- `lockout_detected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `lockout_detected_must_be_false`
- `accessibility_score_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `accessibility_score_below_minimum`
- `accessibility_score_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `recovery_burden_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `recovery_burden_above_maximum`
- `recovery_burden_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-055

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_source_trace_present_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `source_trace_present_required`
- `unsupported_assertion_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unsupported_assertion_must_be_false`
- `source_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `source_confidence_below_minimum`
- `source_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `unexplained_claim_fraction_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unexplained_claim_fraction_above_maximum`
- `unexplained_claim_fraction_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-056

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_claim_boundary_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `claim_boundary_declared_required`
- `extraordinary_claim_unreviewed_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `extraordinary_claim_unreviewed_must_be_false`
- `evidence_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `evidence_confidence_below_minimum`
- `evidence_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `speculation_ratio_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `speculation_ratio_above_maximum`
- `speculation_ratio_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-057

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_dataset_consent_valid_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `dataset_consent_valid_required`
- `restricted_dataset_detected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `restricted_dataset_detected_must_be_false`
- `dataset_quality_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `dataset_quality_below_minimum`
- `dataset_quality_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `privacy_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `privacy_risk_above_maximum`
- `privacy_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-058

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_identity_authorized_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `identity_authorized_required`
- `identity_impersonation_risk_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `identity_impersonation_risk_must_be_false`
- `continuity_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `continuity_confidence_below_minimum`
- `continuity_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `persona_drift_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `persona_drift_above_maximum`
- `persona_drift_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-059

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_retention_basis_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `retention_basis_declared_required`
- `retention_forbidden_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `retention_forbidden_must_be_false`
- `deletion_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `deletion_confidence_below_minimum`
- `deletion_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `orphan_record_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `orphan_record_risk_above_maximum`
- `orphan_record_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-060

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_formalism_interfaces_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `formalism_interfaces_declared_required`
- `invariant_conflict_detected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `invariant_conflict_detected_must_be_false`
- `composition_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `composition_confidence_below_minimum`
- `composition_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `semantic_drift_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `semantic_drift_above_maximum`
- `semantic_drift_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-061

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_invariant_named_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `invariant_named_required`
- `contradictory_invariant_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `contradictory_invariant_must_be_false`
- `invariant_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `invariant_confidence_below_minimum`
- `invariant_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `invariant_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `invariant_gap_above_maximum`
- `invariant_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-062

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_topology_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `topology_declared_required`
- `non_star_shaped_unhandled_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `non_star_shaped_unhandled_must_be_false`
- `coverage_ratio_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `coverage_ratio_below_minimum`
- `coverage_ratio_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `boundary_ambiguity_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `boundary_ambiguity_above_maximum`
- `boundary_ambiguity_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-063

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_shell_origin_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `shell_origin_declared_required`
- `shell_intersection_conflict_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `shell_intersection_conflict_must_be_false`
- `shell_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `shell_confidence_below_minimum`
- `shell_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `shell_deformation_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `shell_deformation_above_maximum`
- `shell_deformation_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-064

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_operator_set_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `operator_set_declared_required`
- `non_closing_operation_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `non_closing_operation_must_be_false`
- `algebra_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `algebra_confidence_below_minimum`
- `algebra_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `undefined_operation_fraction_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `undefined_operation_fraction_above_maximum`
- `undefined_operation_fraction_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-065

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_recoverability_metric_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `recoverability_metric_declared_required`
- `uncalibrated_metric_used_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `uncalibrated_metric_used_must_be_false`
- `calibration_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `calibration_confidence_below_minimum`
- `calibration_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `metric_error_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `metric_error_above_maximum`
- `metric_error_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-066

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_entropy_function_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `entropy_function_declared_required`
- `entropy_function_conflict_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `entropy_function_conflict_must_be_false`
- `reversibility_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `reversibility_confidence_below_minimum`
- `reversibility_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `entropy_error_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `entropy_error_above_maximum`
- `entropy_error_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-067

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_preconditions_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `preconditions_declared_required`
- `missing_core_obligation_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `missing_core_obligation_must_be_false`
- `proof_map_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `proof_map_confidence_below_minimum`
- `proof_map_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `obligation_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `obligation_gap_above_maximum`
- `obligation_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-068

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_state_variables_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `state_variables_declared_required`
- `unbounded_state_unhandled_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unbounded_state_unhandled_must_be_false`
- `abstraction_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `abstraction_confidence_below_minimum`
- `abstraction_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `state_aliasing_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `state_aliasing_risk_above_maximum`
- `state_aliasing_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-069

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_counterexample_captured_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `counterexample_captured_required`
- `counterexample_suppressed_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `counterexample_suppressed_must_be_false`
- `triage_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `triage_confidence_below_minimum`
- `triage_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `untriaged_fraction_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `untriaged_fraction_above_maximum`
- `untriaged_fraction_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-070

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_claim_formalized_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `claim_formalized_required`
- `claim_overlocked_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `claim_overlocked_must_be_false`
- `claim_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `claim_confidence_below_minimum`
- `claim_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `assumption_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `assumption_gap_above_maximum`
- `assumption_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-071

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_types_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `types_declared_required`
- `nonconstructive_gap_unhandled_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `nonconstructive_gap_unhandled_must_be_false`
- `translation_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `translation_confidence_below_minimum`
- `translation_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `type_ambiguity_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `type_ambiguity_above_maximum`
- `type_ambiguity_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-072

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_inductive_structure_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `inductive_structure_declared_required`
- `proof_term_conflict_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `proof_term_conflict_must_be_false`
- `translation_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `translation_confidence_below_minimum`
- `translation_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `induction_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `induction_gap_above_maximum`
- `induction_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-073

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_variables_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `variables_declared_required`
- `liveness_conflict_unhandled_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `liveness_conflict_unhandled_must_be_false`
- `model_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `model_confidence_below_minimum`
- `model_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `state_explosion_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `state_explosion_risk_above_maximum`
- `state_explosion_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-074

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_signatures_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `signatures_declared_required`
- `unsat_core_unhandled_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unsat_core_unhandled_must_be_false`
- `model_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `model_confidence_below_minimum`
- `model_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `relation_ambiguity_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `relation_ambiguity_above_maximum`
- `relation_ambiguity_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-075

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_informal_claim_linked_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `informal_claim_linked_required`
- `claim_mapping_conflict_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `claim_mapping_conflict_must_be_false`
- `mapping_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `mapping_confidence_below_minimum`
- `mapping_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `mapping_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `mapping_gap_above_maximum`
- `mapping_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-076

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_finite_scope_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `finite_scope_declared_required`
- `counterexample_ignored_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `counterexample_ignored_must_be_false`
- `search_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `search_confidence_below_minimum`
- `search_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `unsearched_scope_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unsearched_scope_above_maximum`
- `unsearched_scope_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-077

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_invariant_runtime_form_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `invariant_runtime_form_declared_required`
- `monitor_side_effect_unbounded_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `monitor_side_effect_unbounded_must_be_false`
- `monitor_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `monitor_confidence_below_minimum`
- `monitor_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `monitor_overhead_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `monitor_overhead_above_maximum`
- `monitor_overhead_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-078

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_proof_hash_ready_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `proof_hash_ready_required`
- `proof_artifact_tampered_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `proof_artifact_tampered_must_be_false`
- `artifact_integrity_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `artifact_integrity_below_minimum`
- `artifact_integrity_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `custody_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `custody_gap_above_maximum`
- `custody_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-079

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_spec_hash_ready_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `spec_hash_ready_required`
- `unauthorized_spec_drift_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unauthorized_spec_drift_must_be_false`
- `drift_detection_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `drift_detection_confidence_below_minimum`
- `drift_detection_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `drift_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `drift_gap_above_maximum`
- `drift_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-080

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_formal_scope_frozen_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `formal_scope_frozen_required`
- `unresolved_blocker_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unresolved_blocker_must_be_false`
- `release_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `release_confidence_below_minimum`
- `release_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `known_gap_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `known_gap_risk_above_maximum`
- `known_gap_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-081

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_ci_policy_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `ci_policy_declared_required`
- `bypass_branch_detected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `bypass_branch_detected_must_be_false`
- `ci_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `ci_confidence_below_minimum`
- `ci_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `ci_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `ci_gap_above_maximum`
- `ci_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-082

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_source_org_verified_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `source_org_verified_required`
- `org_trust_break_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `org_trust_break_must_be_false`
- `org_trust_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `org_trust_below_minimum`
- `org_trust_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `org_mismatch_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `org_mismatch_risk_above_maximum`
- `org_mismatch_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-083

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_rollback_plan_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `rollback_plan_declared_required`
- `rollback_conflict_detected_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `rollback_conflict_detected_must_be_false`
- `rollback_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `rollback_confidence_below_minimum`
- `rollback_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `rollback_time_minutes_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `rollback_time_minutes_above_maximum`
- `rollback_time_minutes_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-084

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_quarantine_destination_defined_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `quarantine_destination_defined_required`
- `quarantine_escape_risk_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `quarantine_escape_risk_must_be_false`
- `quarantine_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `quarantine_confidence_below_minimum`
- `quarantine_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `isolation_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `isolation_gap_above_maximum`
- `isolation_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-085

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_export_schema_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `export_schema_declared_required`
- `audit_export_leak_risk_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `audit_export_leak_risk_must_be_false`
- `export_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `export_confidence_below_minimum`
- `export_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `redaction_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `redaction_gap_above_maximum`
- `redaction_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-086

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_dry_run_environment_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `dry_run_environment_declared_required`
- `dry_run_nonrepresentative_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `dry_run_nonrepresentative_must_be_false`
- `dry_run_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `dry_run_confidence_below_minimum`
- `dry_run_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `production_delta_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `production_delta_above_maximum`
- `production_delta_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-087

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_incident_classified_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `incident_classified_required`
- `incident_uncontained_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `incident_uncontained_must_be_false`
- `response_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `response_confidence_below_minimum`
- `response_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `response_delay_minutes_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `response_delay_minutes_above_maximum`
- `response_delay_minutes_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-088

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_service_slo_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `service_slo_declared_required`
- `service_degradation_unbounded_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `service_degradation_unbounded_must_be_false`
- `service_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `service_confidence_below_minimum`
- `service_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `slo_violation_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `slo_violation_risk_above_maximum`
- `slo_violation_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-089

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_cloud_boundary_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `cloud_boundary_declared_required`
- `provider_trust_break_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `provider_trust_break_must_be_false`
- `cloud_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `cloud_confidence_below_minimum`
- `cloud_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `egress_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `egress_risk_above_maximum`
- `egress_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-090

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_promotion_policy_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `promotion_policy_declared_required`
- `promotion_blocker_present_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `promotion_blocker_present_must_be_false`
- `promotion_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `promotion_confidence_below_minimum`
- `promotion_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `promotion_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `promotion_risk_above_maximum`
- `promotion_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-091

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_novelty_boundary_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `novelty_boundary_declared_required`
- `public_disclosure_risk_unhandled_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `public_disclosure_risk_unhandled_must_be_false`
- `patent_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `patent_confidence_below_minimum`
- `patent_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `claim_overlap_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `claim_overlap_risk_above_maximum`
- `claim_overlap_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-092

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_claim_scope_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `claim_scope_declared_required`
- `unsupported_whitepaper_claim_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unsupported_whitepaper_claim_must_be_false`
- `whitepaper_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `whitepaper_confidence_below_minimum`
- `whitepaper_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `citation_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `citation_gap_above_maximum`
- `citation_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-093

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_demo_scope_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `demo_scope_declared_required`
- `demo_overclaim_risk_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `demo_overclaim_risk_must_be_false`
- `demo_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `demo_confidence_below_minimum`
- `demo_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `demo_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `demo_gap_above_maximum`
- `demo_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-094

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_review_scope_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `review_scope_declared_required`
- `critical_finding_unresolved_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `critical_finding_unresolved_must_be_false`
- `review_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `review_confidence_below_minimum`
- `review_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `unresolved_finding_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unresolved_finding_risk_above_maximum`
- `unresolved_finding_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-095

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_benchmark_scope_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `benchmark_scope_declared_required`
- `benchmark_bias_unhandled_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `benchmark_bias_unhandled_must_be_false`
- `benchmark_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `benchmark_confidence_below_minimum`
- `benchmark_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `benchmark_bias_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `benchmark_bias_risk_above_maximum`
- `benchmark_bias_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-096

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_site_target_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `site_target_declared_required`
- `site_claim_mismatch_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `site_claim_mismatch_must_be_false`
- `site_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `site_confidence_below_minimum`
- `site_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `broken_link_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `broken_link_risk_above_maximum`
- `broken_link_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-097

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_audience_scope_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `audience_scope_declared_required`
- `viral_overclaim_risk_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `viral_overclaim_risk_must_be_false`
- `publication_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `publication_confidence_below_minimum`
- `publication_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `misinterpretation_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `misinterpretation_risk_above_maximum`
- `misinterpretation_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-098

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_target_audience_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `target_audience_declared_required`
- `outreach_misalignment_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `outreach_misalignment_must_be_false`
- `outreach_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `outreach_confidence_below_minimum`
- `outreach_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `recipient_mismatch_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `recipient_mismatch_risk_above_maximum`
- `recipient_mismatch_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-099

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_archive_manifest_ready_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `archive_manifest_ready_required`
- `archive_incomplete_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `archive_incomplete_must_be_false`
- `archive_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `archive_confidence_below_minimum`
- `archive_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `archive_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `archive_gap_above_maximum`
- `archive_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-100

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_all_prior_gates_indexed_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `all_prior_gates_indexed_required`
- `phase_blocker_present_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `phase_blocker_present_must_be_false`
- `completion_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `completion_confidence_below_minimum`
- `completion_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `phase_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `phase_gap_above_maximum`
- `phase_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-101

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_extension_scope_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `extension_scope_declared_required`
- `phase_scope_conflict_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `phase_scope_conflict_must_be_false`
- `extension_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `extension_confidence_below_minimum`
- `extension_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `legacy_break_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `legacy_break_risk_above_maximum`
- `legacy_break_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-102

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_upgrade_scope_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `upgrade_scope_declared_required`
- `upgrade_invariant_break_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `upgrade_invariant_break_must_be_false`
- `upgrade_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `upgrade_confidence_below_minimum`
- `upgrade_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `migration_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `migration_gap_above_maximum`
- `migration_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-103

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_fork_reason_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `fork_reason_declared_required`
- `fork_capture_risk_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `fork_capture_risk_must_be_false`
- `fork_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `fork_confidence_below_minimum`
- `fork_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `reconciliation_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `reconciliation_gap_above_maximum`
- `reconciliation_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-104

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_federation_scope_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `federation_scope_declared_required`
- `federation_trust_break_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `federation_trust_break_must_be_false`
- `federation_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `federation_confidence_below_minimum`
- `federation_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `trust_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `trust_gap_above_maximum`
- `trust_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-105

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_conflict_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `conflict_declared_required`
- `unresolved_formalism_conflict_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unresolved_formalism_conflict_must_be_false`
- `arbitration_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `arbitration_confidence_below_minimum`
- `arbitration_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `priority_ambiguity_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `priority_ambiguity_above_maximum`
- `priority_ambiguity_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-106

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_reality_effect_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `reality_effect_declared_required`
- `unbounded_reality_contact_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `unbounded_reality_contact_must_be_false`
- `contact_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `contact_confidence_below_minimum`
- `contact_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `harm_uncertainty_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `harm_uncertainty_above_maximum`
- `harm_uncertainty_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-107

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_life_impact_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `life_impact_declared_required`
- `life_harm_unbounded_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `life_harm_unbounded_must_be_false`
- `life_alignment_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `life_alignment_below_minimum`
- `life_alignment_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `life_harm_risk_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `life_harm_risk_above_maximum`
- `life_harm_risk_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-108

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_observer_class_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `observer_class_declared_required`
- `observer_state_conflict_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `observer_state_conflict_must_be_false`
- `coupling_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `coupling_confidence_below_minimum`
- `coupling_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `observation_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `observation_gap_above_maximum`
- `observation_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-109

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_transition_class_declared_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `transition_class_declared_required`
- `transition_class_conflict_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `transition_class_conflict_must_be_false`
- `transition_alignment_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `transition_alignment_below_minimum`
- `transition_alignment_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `mapping_ambiguity_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `mapping_ambiguity_above_maximum`
- `mapping_ambiguity_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

### chf-110

- Status: **PASS**

- `baseline_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `missing_phase_two_scope_ready_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `phase_two_scope_ready_required`
- `phase_two_blocker_present_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `phase_two_blocker_present_must_be_false`
- `launch_confidence_below_minimum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `launch_confidence_below_minimum`
- `launch_confidence_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`
- `launch_gap_above_maximum_fail_closed`: expected `FAIL_CLOSED`, actual `FAIL_CLOSED` — **PASS**
  - Reason: `launch_gap_above_maximum`
- `launch_gap_exact_boundary_allow`: expected `ALLOW`, actual `ALLOW` — **PASS**
  - Reason: `standard_gate_pass`

