# Consequence Horizon Formalism Validation Summary

- Overall status: **PASS**
- Specs evaluated: **19**

## Sandbox Results

- Sandbox status: **PASS**
- Suites evaluated: **10**
- Subtests generated: **1930**
- Subtests passed: **1930**
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

