#!/usr/bin/env python3
"""
Deterministic validator for Consequence Horizon Formalism specs.

Stable-dispatcher rule:
- GitHub Actions workflow stays a dispatcher.
- Semantic expansion belongs here and in problem_spec_chf_*.yml files.
- No external API calls.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import yaml

try:
    from chf_sandbox_runner import run_sandbox_from_config
except Exception:
    run_sandbox_from_config = None


ALLOW = "ALLOW"
DENY = "DENY"
FAIL_CLOSED = "FAIL_CLOSED"
NO_EFFECT = "NO_EFFECT"

SMOOTH_SHELL = "SMOOTH_SHELL"
CELL_RESOLVED = "CELL_RESOLVED"

RECORD_LEGIBLE = "RECORD_LEGIBLE"
RECORD_EXISTS_LOW_LEGIBILITY = "RECORD_EXISTS_LOW_LEGIBILITY"
NO_PROPAGATED_RECORD_REQUIRED = "NO_PROPAGATED_RECORD_REQUIRED"

GEOMETRY_VALID = "GEOMETRY_VALID"
GEOMETRY_FAIL_CLOSED = "GEOMETRY_FAIL_CLOSED"

CHAIN_CONTINUOUS = "CHAIN_CONTINUOUS"
CHAIN_FAIL_CLOSED = "CHAIN_FAIL_CLOSED"

PROBABILISTIC_ALLOW = "PROBABILISTIC_ALLOW"
PROBABILISTIC_FAIL_CLOSED = "PROBABILISTIC_FAIL_CLOSED"

BRANCH_SPLIT = "BRANCH_SPLIT"
BRANCH_FAIL_CLOSED = "BRANCH_FAIL_CLOSED"

FORMAL_ANALOGY_ALLOWED = "FORMAL_ANALOGY_ALLOWED"
PHYSICS_CLAIM_BLOCKED = "PHYSICS_CLAIM_BLOCKED"
EMPIRICAL_CLAIM_FAIL_CLOSED = "EMPIRICAL_CLAIM_FAIL_CLOSED"

RECEIPT_SUFFICIENT = "RECEIPT_SUFFICIENT"
RECEIPT_FAIL_CLOSED = "RECEIPT_FAIL_CLOSED"

MERGE_ALLOWED = "MERGE_ALLOWED"
MERGE_FAIL_CLOSED = "MERGE_FAIL_CLOSED"

ENTROPY_WITHIN_BUDGET = "ENTROPY_WITHIN_BUDGET"
ENTROPY_FAIL_CLOSED = "ENTROPY_FAIL_CLOSED"

EXTERNAL_BINDING_ALLOWED = "EXTERNAL_BINDING_ALLOWED"
EXTERNAL_BINDING_FAIL_CLOSED = "EXTERNAL_BINDING_FAIL_CLOSED"
REPAIR_ALLOWED = "REPAIR_ALLOWED"
REPAIR_FAIL_CLOSED = "REPAIR_FAIL_CLOSED"
REPLAY_CONFIDENT = "REPLAY_CONFIDENT"
REPLAY_FAIL_CLOSED = "REPLAY_FAIL_CLOSED"
AUTHORITY_STABLE = "AUTHORITY_STABLE"
AUTHORITY_FAIL_CLOSED = "AUTHORITY_FAIL_CLOSED"
POLICY_VERSION_VALID = "POLICY_VERSION_VALID"
POLICY_VERSION_FAIL_CLOSED = "POLICY_VERSION_FAIL_CLOSED"
PROPAGATION_VALIDATED = "PROPAGATION_VALIDATED"
PROPAGATION_FAIL_CLOSED = "PROPAGATION_FAIL_CLOSED"
PARTICIPANT_IMPACT_ADMISSIBLE = "PARTICIPANT_IMPACT_ADMISSIBLE"
PARTICIPANT_IMPACT_FAIL_CLOSED = "PARTICIPANT_IMPACT_FAIL_CLOSED"
PROTECTED_ESCALATION_REQUIRED = "PROTECTED_ESCALATION_REQUIRED"
PROTECTED_ESCALATION_CLEAR = "PROTECTED_ESCALATION_CLEAR"
TEMPORAL_COHERENT = "TEMPORAL_COHERENT"
TEMPORAL_FAIL_CLOSED = "TEMPORAL_FAIL_CLOSED"
REPLAY_CONVERGED = "REPLAY_CONVERGED"
REPLAY_DIVERGENCE_FAIL_CLOSED = "REPLAY_DIVERGENCE_FAIL_CLOSED"
REJOIN_ALLOWED = "REJOIN_ALLOWED"
REJOIN_FAIL_CLOSED = "REJOIN_FAIL_CLOSED"


def radius(point: List[float], center: List[float]) -> float:
    return math.sqrt(sum((point[i] - center[i]) ** 2 for i in range(len(point))))


def angle_degrees(point: List[float], center: List[float]) -> float:
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    theta = math.degrees(math.atan2(dy, dx))
    if theta < 0:
        theta += 360
    return theta


def cell_for_angle(theta: float) -> str:
    if 0 <= theta < 90:
        return "cell_1"
    if 90 <= theta < 180:
        return "cell_2"
    if 180 <= theta < 270:
        return "cell_3"
    return "cell_4"


def simplex_valid(x: Dict[str, float], tolerance: float = 1e-9) -> bool:
    vals = [float(x[k]) for k in ("g", "c", "a", "t")]
    return all(0.0 <= v <= 1.0 for v in vals) and abs(sum(vals) - 1.0) <= tolerance


def legitimacy_capacity(x: Dict[str, float], params: Dict[str, float]) -> float:
    return (
        float(params["K"])
        * float(x["g"]) ** float(params["alpha"])
        * float(x["c"]) ** float(params["beta"])
        * float(x["t"]) ** float(params["gamma"])
    )


def evaluate_gcat_state(x: Dict[str, float], params: Dict[str, float]) -> Dict[str, Any]:
    if not simplex_valid(x, tolerance=float(params.get("simplex_tolerance", 1e-9))):
        return {"actual": FAIL_CLOSED, "reason": "simplex_or_bounds_invalid", "lambda": None, "invariant": None}

    lam = legitimacy_capacity(x, params)
    invariant = float(x["a"]) - lam
    if invariant <= float(params.get("invariant_tolerance", 1e-9)):
        return {"actual": ALLOW, "reason": "gcat_invariant_satisfied", "lambda": round(lam, 12), "invariant": round(invariant, 12)}
    return {"actual": DENY, "reason": "gcat_invariant_violated", "lambda": round(lam, 12), "invariant": round(invariant, 12)}


def evaluate_chf_001(spec: Dict[str, Any]) -> Dict[str, Any]:
    center = spec["model"]["center"]
    horizon = float(spec["model"]["horizon_radius"])
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        p = case["point"]
        r = radius(p, center)
        theta = angle_degrees(p, center)
        cell = cell_for_angle(theta)
        expected = case["expected"]

        if r > horizon:
            actual, reason = DENY, "outside_horizon"
        elif cell == "cell_1":
            actual, reason = ALLOW, "cell_rule_allows"
        elif cell == "cell_2":
            actual = ALLOW if r <= 0.5 else DENY
            reason = "cell_rule_allows" if actual == ALLOW else "cell_radius_limit_exceeded"
        elif cell == "cell_3":
            actual, reason = DENY, "forbidden_cell"
        else:
            actual, reason = FAIL_CLOSED, "uncertain_cell"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"], "radius": round(r, 6), "angle_degrees": round(theta, 6),
            "cell": cell, "expected": expected, "actual": actual,
            "status": "PASS" if passed else "FAIL", "reason": reason,
            "crossing_event_required": actual == ALLOW,
            "historical_shell_required": actual == ALLOW,
            "propagated_record_required": actual == ALLOW,
            "new_center_created": actual == ALLOW,
        })

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_002(spec: Dict[str, Any]) -> Dict[str, Any]:
    centers = spec["model"]["plausible_centers"]
    horizon = float(spec["model"]["horizon_radius"])
    transition_radius = float(spec["model"]["transition_radius"])
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        p = case["point"]
        expected = case["expected"]
        center_results = []
        robust = True

        for c in centers:
            r = radius(p, c)
            theta = angle_degrees(p, c)
            cell = cell_for_angle(theta)
            inside_transition = r <= transition_radius
            inside_horizon = r <= horizon
            cell_allows = cell == "cell_1"
            center_pass = inside_transition and inside_horizon and cell_allows
            robust = robust and center_pass
            center_results.append({
                "center": c, "radius": round(r, 6), "angle_degrees": round(theta, 6),
                "cell": cell, "inside_transition": inside_transition,
                "inside_horizon": inside_horizon, "cell_allows": cell_allows,
                "center_pass": center_pass,
            })

        actual = ALLOW if robust else FAIL_CLOSED
        reason = "all_centers_pass" if robust else "not_safe_across_all_plausible_centers"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason, "center_results": center_results})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_003(spec: Dict[str, Any]) -> Dict[str, Any]:
    expected = spec["expected"]
    model = spec["model"]
    local = model["local_permit"]
    deformation = float(model["deformation"])
    tolerance = float(model["deformation_tolerance"])
    recoverability_after = float(model.get("recoverability_after", 1.0))
    recoverability_threshold = float(model.get("recoverability_threshold", 0.0))

    if local != ALLOW:
        actual, reason = local, "local_not_allowed"
    elif deformation > tolerance:
        actual, reason = DENY, "deformation_exceeds_tolerance"
    elif recoverability_after < recoverability_threshold:
        actual, reason = DENY, "recoverability_below_threshold"
    else:
        actual, reason = ALLOW, "coupled_constraints_pass"

    passed = actual == expected
    return {"spec_id": spec["problem_id"], "status": "PASS" if passed else "FAIL", "cases": [{"id": spec["problem_id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason}]}


def evaluate_chf_004(spec: Dict[str, Any]) -> Dict[str, Any]:
    threshold = float(spec["model"]["distinguishability_threshold"])
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        q = (
            float(case["resolution"]) * float(case["probe_capacity"])
        ) / max(float(case["distance"]) * float(case["noise"]) * float(case["lag"]), 1e-12)
        expected = case["expected"]
        actual = CELL_RESOLVED if q >= threshold else SMOOTH_SHELL
        reason = "cell_structure_resolved" if actual == CELL_RESOLVED else "observational_sphericalization"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "q_observer": round(q, 6), "threshold": threshold, "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_005(spec: Dict[str, Any]) -> Dict[str, Any]:
    threshold = float(spec["model"]["legibility_threshold"])
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        actualized = bool(case["actualized_crossing"])
        legibility = case.get("legibility", None)

        if not actualized:
            actual, reason = NO_PROPAGATED_RECORD_REQUIRED, "no_actualized_crossing"
        elif legibility is not None and float(legibility) >= threshold:
            actual, reason = RECORD_LEGIBLE, "record_above_legibility_threshold"
        else:
            actual, reason = RECORD_EXISTS_LOW_LEGIBILITY, "record_exists_but_legibility_decayed"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_006(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    horizon = float(model["horizon_radius"])
    cells = model["cells"]
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        vector = case["vector"]
        expected = case["expected"]
        r = math.sqrt(sum(v * v for v in vector))
        best_cell, best_dot = None, -10**9

        for cell in cells:
            dot = sum(vector[i] * cell["direction"][i] for i in range(3))
            if dot > best_dot:
                best_dot, best_cell = dot, cell

        if r > horizon:
            actual, reason = DENY, "outside_horizon"
        else:
            actual, reason = best_cell["result"], best_cell["reason"]

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "radius": round(r, 6), "assigned_cell": best_cell["id"], "dot_score": round(best_dot, 6), "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_007(spec: Dict[str, Any]) -> Dict[str, Any]:
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        star_shaped = bool(case["star_shaped"])
        radial_path_clear = bool(case["radial_path_clear"])
        boundary_partition_complete = bool(case["boundary_partition_complete"])

        if star_shaped and radial_path_clear and boundary_partition_complete:
            actual, reason = GEOMETRY_VALID, "radial_cell_coverage_valid"
        else:
            actual = GEOMETRY_FAIL_CLOSED
            if not star_shaped:
                reason = "region_not_star_shaped"
            elif not radial_path_clear:
                reason = "radial_path_crosses_forbidden_space"
            else:
                reason = "boundary_partition_incomplete"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_008(spec: Dict[str, Any]) -> Dict[str, Any]:
    params = spec["model"]["gcat_params"]
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        result = evaluate_gcat_state(case["state"], params)
        actual = result["actual"]
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": result["reason"], "lambda": result["lambda"], "invariant": result["invariant"]})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_009(spec: Dict[str, Any]) -> Dict[str, Any]:
    params = spec["model"]["gcat_params"]
    shell_required_fields = set(spec["model"]["shell_required_fields"])
    record_required_fields = set(spec["model"]["record_required_fields"])
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        gcat = evaluate_gcat_state(case["projected_state"], params)
        shell_fields = set(case.get("shell_fields", []))
        record_fields = set(case.get("record_fields", []))

        if gcat["actual"] != ALLOW:
            actual, reason = gcat["actual"], gcat["reason"]
        elif not shell_required_fields.issubset(shell_fields):
            actual, reason = FAIL_CLOSED, "historical_shell_incomplete"
        elif not record_required_fields.issubset(record_fields):
            actual, reason = FAIL_CLOSED, "propagated_record_incomplete"
        else:
            actual, reason = ALLOW, "commit_crossing_gcat_shell_record_ready"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_010(spec: Dict[str, Any]) -> Dict[str, Any]:
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        recoverability = float(case["recoverability"])
        recoverability_threshold = float(case["recoverability_threshold"])
        purpose_converges = bool(case["purpose_converges"])

        if recoverability < recoverability_threshold:
            actual, reason = DENY, "recoverability_below_threshold"
        elif not purpose_converges:
            actual, reason = DENY, "purpose_inversion_detected"
        else:
            actual, reason = ALLOW, "recoverability_and_purpose_converge"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_011(spec: Dict[str, Any]) -> Dict[str, Any]:
    cases, all_pass = [], True
    default_buffer = float(spec["model"].get("default_uncertainty_buffer", 0.0))

    for case in spec["test_cases"]:
        expected = case["expected"]
        lag_reachable_radius = float(case["base_transition_radius"]) + float(case["lag"]) * float(case["drift_rate"]) + float(case.get("uncertainty_buffer", default_buffer))
        horizon = float(case["horizon_radius"])

        if lag_reachable_radius <= horizon:
            actual, reason = ALLOW, "lag_reachable_set_inside_horizon"
        else:
            actual, reason = FAIL_CLOSED, "lag_reachable_set_exceeds_horizon"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "lag_reachable_radius": round(lag_reachable_radius, 6), "horizon_radius": horizon, "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_012(spec: Dict[str, Any]) -> Dict[str, Any]:
    required_links = set(spec["model"]["required_chain_links"])
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        links = set(case["chain_links"])
        legibility = float(case["record_legibility"])
        threshold = float(case["legibility_threshold"])

        if not required_links.issubset(links):
            actual, reason = CHAIN_FAIL_CLOSED, "historical_chain_links_missing"
        elif legibility < threshold:
            actual, reason = CHAIN_FAIL_CLOSED, "historical_chain_legibility_below_threshold"
        else:
            actual, reason = CHAIN_CONTINUOUS, "historical_shell_chain_continuous"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_013(spec: Dict[str, Any]) -> Dict[str, Any]:
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        deformation = case.get("deformation")
        epsilon = float(case["epsilon"])
        protected = bool(case.get("protected", False))
        deformation_known = bool(case.get("deformation_known", True))

        if not deformation_known and protected:
            actual, reason = FAIL_CLOSED, "protected_affected_cloud_unknown_deformation"
        elif not deformation_known:
            actual, reason = FAIL_CLOSED, "unknown_deformation"
        elif float(deformation) <= epsilon and not protected:
            actual, reason = NO_EFFECT, "below_relevance_threshold"
        elif float(deformation) <= epsilon and protected:
            actual, reason = FAIL_CLOSED, "protected_cloud_requires_explicit_review"
        else:
            actual, reason = DENY, "deformation_exceeds_relevance_threshold"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_014(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Probabilistic cloud admissibility gate."""
    model = spec["model"]
    theta = float(model["recoverability_probability_threshold"])
    epsilon = float(model["harm_probability_ceiling"])
    max_unknown = float(model["unknown_probability_ceiling"])
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        p_recoverable = float(case["p_recoverable"])
        p_harm = float(case["p_harm"])
        p_unknown = float(case.get("p_unknown", 0.0))
        support_complete = bool(case.get("support_complete", True))

        if not support_complete:
            actual, reason = PROBABILISTIC_FAIL_CLOSED, "probability_support_incomplete"
        elif p_unknown > max_unknown:
            actual, reason = PROBABILISTIC_FAIL_CLOSED, "unknown_probability_exceeds_ceiling"
        elif p_recoverable >= theta and p_harm <= epsilon:
            actual, reason = PROBABILISTIC_ALLOW, "probabilistic_recoverability_harm_bounds_pass"
        elif p_harm > epsilon:
            actual, reason = DENY, "harm_probability_exceeds_ceiling"
        else:
            actual, reason = PROBABILISTIC_FAIL_CLOSED, "recoverability_probability_below_threshold"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_015(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Branch splitting after unresolved uncertainty."""
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        robust_allow = bool(case.get("robust_allow", False))
        known_violation = bool(case.get("known_violation", False))
        unresolved_centers = int(case.get("unresolved_centers", 0))
        branch_custody_available = bool(case.get("branch_custody_available", False))
        branch_receipts_ready = bool(case.get("branch_receipts_ready", False))

        if robust_allow:
            actual, reason = ALLOW, "robust_allow_no_branch_split_required"
        elif known_violation:
            actual, reason = DENY, "known_violation_blocks_branching"
        elif unresolved_centers > 1 and branch_custody_available and branch_receipts_ready:
            actual, reason = BRANCH_SPLIT, "unresolved_uncertainty_preserved_by_branch_split"
        else:
            actual, reason = BRANCH_FAIL_CLOSED, "unresolved_uncertainty_without_branch_custody"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_016(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Guardrail for formal analogy vs unsupported physical/cosmological claim."""
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        claim_type = case["claim_type"]
        empirical_support = bool(case.get("empirical_support", False))
        analogy_scope_bounded = bool(case.get("analogy_scope_bounded", False))
        asserts_physical_equivalence = bool(case.get("asserts_physical_equivalence", False))

        if asserts_physical_equivalence:
            actual, reason = PHYSICS_CLAIM_BLOCKED, "physical_equivalence_claim_blocked"
        elif claim_type == "formal_analogy" and analogy_scope_bounded:
            actual, reason = FORMAL_ANALOGY_ALLOWED, "bounded_formal_analogy_allowed"
        elif claim_type == "empirical_physics" and not empirical_support:
            actual, reason = EMPIRICAL_CLAIM_FAIL_CLOSED, "empirical_support_required"
        elif claim_type == "empirical_physics" and empirical_support:
            actual, reason = FORMAL_ANALOGY_ALLOWED, "empirical_claim_marked_for_external_review"
        else:
            actual, reason = EMPIRICAL_CLAIM_FAIL_CLOSED, "claim_scope_unresolved"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_017(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Receipt sufficiency and custody gate."""
    required_fields = set(spec["model"]["required_receipt_fields"])
    required_custody = set(spec["model"]["required_custody_links"])
    min_integrity = float(spec["model"]["min_integrity_score"])
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        receipt_fields = set(case.get("receipt_fields", []))
        custody_links = set(case.get("custody_links", []))
        integrity_score = float(case.get("integrity_score", 0.0))
        tamper_detected = bool(case.get("tamper_detected", False))
        signer_authorized = bool(case.get("signer_authorized", False))

        if tamper_detected:
            actual, reason = RECEIPT_FAIL_CLOSED, "receipt_tamper_detected"
        elif not signer_authorized:
            actual, reason = RECEIPT_FAIL_CLOSED, "receipt_signer_not_authorized"
        elif not required_fields.issubset(receipt_fields):
            actual, reason = RECEIPT_FAIL_CLOSED, "receipt_fields_incomplete"
        elif not required_custody.issubset(custody_links):
            actual, reason = RECEIPT_FAIL_CLOSED, "receipt_custody_links_incomplete"
        elif integrity_score < min_integrity:
            actual, reason = RECEIPT_FAIL_CLOSED, "receipt_integrity_below_threshold"
        else:
            actual, reason = RECEIPT_SUFFICIENT, "receipt_sufficiency_and_custody_pass"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_018(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Branch merge and reconciliation gate."""
    model = spec["model"]
    max_divergence = float(model["max_state_divergence"])
    min_confidence = float(model["min_reconciliation_confidence"])
    required_evidence = set(model["required_evidence"])
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        branch_receipts_valid = bool(case.get("branch_receipts_valid", False))
        no_contradiction = bool(case.get("no_contradiction", False))
        state_divergence = float(case.get("state_divergence", 1.0))
        reconciliation_confidence = float(case.get("reconciliation_confidence", 0.0))
        evidence = set(case.get("evidence", []))

        if not branch_receipts_valid:
            actual, reason = MERGE_FAIL_CLOSED, "branch_receipts_invalid"
        elif not no_contradiction:
            actual, reason = MERGE_FAIL_CLOSED, "branch_contradiction_detected"
        elif state_divergence > max_divergence:
            actual, reason = MERGE_FAIL_CLOSED, "state_divergence_exceeds_merge_tolerance"
        elif reconciliation_confidence < min_confidence:
            actual, reason = MERGE_FAIL_CLOSED, "reconciliation_confidence_below_threshold"
        elif not required_evidence.issubset(evidence):
            actual, reason = MERGE_FAIL_CLOSED, "reconciliation_evidence_incomplete"
        else:
            actual, reason = MERGE_ALLOWED, "branch_merge_reconciliation_pass"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_019(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Entropy / irreversibility budget gate."""
    model = spec["model"]
    max_entropy_delta = float(model["max_entropy_delta"])
    max_irreversibility = float(model["max_irreversibility_score"])
    min_reversibility_margin = float(model["min_reversibility_margin"])
    cases, all_pass = [], True

    for case in spec["test_cases"]:
        expected = case["expected"]
        entropy_delta = float(case.get("entropy_delta", 0.0))
        irreversibility_score = float(case.get("irreversibility_score", 0.0))
        reversibility_margin = float(case.get("reversibility_margin", 0.0))
        mitigation_available = bool(case.get("mitigation_available", False))

        if entropy_delta > max_entropy_delta and not mitigation_available:
            actual, reason = ENTROPY_FAIL_CLOSED, "entropy_delta_exceeds_budget_without_mitigation"
        elif irreversibility_score > max_irreversibility:
            actual, reason = ENTROPY_FAIL_CLOSED, "irreversibility_score_exceeds_budget"
        elif reversibility_margin < min_reversibility_margin:
            actual, reason = ENTROPY_FAIL_CLOSED, "reversibility_margin_below_threshold"
        else:
            actual, reason = ENTROPY_WITHIN_BUDGET, "entropy_irreversibility_budget_pass"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}



def evaluate_chf_020(spec: Dict[str, Any]) -> Dict[str, Any]:
    required_checks = set(spec["model"]["required_external_checks"])
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        local_admissible = bool(case.get("local_admissible", False))
        external_system_available = bool(case.get("external_system_available", False))
        dry_run_passed = bool(case.get("dry_run_passed", False))
        rollback_path_available = bool(case.get("rollback_path_available", False))
        consent_or_authority_valid = bool(case.get("consent_or_authority_valid", False))
        checks = set(case.get("external_checks", []))
        if not local_admissible:
            actual, reason = EXTERNAL_BINDING_FAIL_CLOSED, "local_admissibility_not_established"
        elif not external_system_available:
            actual, reason = EXTERNAL_BINDING_FAIL_CLOSED, "external_system_unavailable"
        elif not consent_or_authority_valid:
            actual, reason = EXTERNAL_BINDING_FAIL_CLOSED, "external_authority_invalid"
        elif not dry_run_passed:
            actual, reason = EXTERNAL_BINDING_FAIL_CLOSED, "external_dry_run_failed"
        elif not rollback_path_available:
            actual, reason = EXTERNAL_BINDING_FAIL_CLOSED, "external_rollback_path_missing"
        elif not required_checks.issubset(checks):
            actual, reason = EXTERNAL_BINDING_FAIL_CLOSED, "external_checks_incomplete"
        else:
            actual, reason = EXTERNAL_BINDING_ALLOWED, "external_binding_gate_pass"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_021(spec: Dict[str, Any]) -> Dict[str, Any]:
    min_conf = float(spec["model"]["min_repair_confidence"])
    max_harm = float(spec["model"]["max_repair_harm"])
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        rollback = bool(case.get("rollback_available", False))
        compensating = bool(case.get("compensating_action_available", False))
        admissible = bool(case.get("repair_admissible", False))
        confidence = float(case.get("repair_confidence", 0.0))
        harm = float(case.get("repair_harm", 1.0))
        receipt = bool(case.get("repair_receipt_ready", False))
        if not (rollback or compensating):
            actual, reason = REPAIR_FAIL_CLOSED, "no_rollback_or_compensating_action"
        elif not admissible:
            actual, reason = REPAIR_FAIL_CLOSED, "repair_path_not_admissible"
        elif confidence < min_conf:
            actual, reason = REPAIR_FAIL_CLOSED, "repair_confidence_below_threshold"
        elif harm > max_harm:
            actual, reason = REPAIR_FAIL_CLOSED, "repair_harm_exceeds_ceiling"
        elif not receipt:
            actual, reason = REPAIR_FAIL_CLOSED, "repair_receipt_not_ready"
        else:
            actual, reason = REPAIR_ALLOWED, "rollback_or_repair_gate_pass"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_022(spec: Dict[str, Any]) -> Dict[str, Any]:
    min_conf = float(spec["model"]["min_reconstruction_confidence"])
    max_var = float(spec["model"]["max_unexplained_variance"])
    required = set(spec["model"]["required_components"])
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        confidence = float(case.get("reconstruction_confidence", 0.0))
        variance = float(case.get("unexplained_variance", 1.0))
        deterministic = bool(case.get("deterministic_replay", False))
        components = set(case.get("components", []))
        if not deterministic:
            actual, reason = REPLAY_FAIL_CLOSED, "deterministic_replay_not_established"
        elif not required.issubset(components):
            actual, reason = REPLAY_FAIL_CLOSED, "reconstruction_components_incomplete"
        elif confidence < min_conf:
            actual, reason = REPLAY_FAIL_CLOSED, "reconstruction_confidence_below_threshold"
        elif variance > max_var:
            actual, reason = REPLAY_FAIL_CLOSED, "unexplained_variance_exceeds_ceiling"
        else:
            actual, reason = REPLAY_CONFIDENT, "receipt_replay_reconstruction_confident"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_023(spec: Dict[str, Any]) -> Dict[str, Any]:
    max_drift = float(spec["model"]["max_authority_drift"])
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        eval_auth = case.get("authority_at_evaluation")
        commit_auth = case.get("authority_at_commit")
        drift = float(case.get("authority_drift", 1.0))
        revoked = bool(case.get("revocation_seen", False))
        delegation = bool(case.get("delegation_chain_valid", False))
        if revoked:
            actual, reason = AUTHORITY_FAIL_CLOSED, "authority_revocation_seen"
        elif eval_auth != commit_auth:
            actual, reason = AUTHORITY_FAIL_CLOSED, "authority_identity_changed"
        elif not delegation:
            actual, reason = AUTHORITY_FAIL_CLOSED, "delegation_chain_invalid"
        elif drift > max_drift:
            actual, reason = AUTHORITY_FAIL_CLOSED, "authority_drift_exceeds_tolerance"
        else:
            actual, reason = AUTHORITY_STABLE, "authority_stable_at_commit"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_024(spec: Dict[str, Any]) -> Dict[str, Any]:
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        evaluated = case.get("evaluated_policy_version")
        commit = case.get("commit_policy_version")
        active = bool(case.get("version_active", False))
        migration = bool(case.get("migration_proof_present", False))
        compatible = bool(case.get("backward_compatible", False))
        if not active:
            actual, reason = POLICY_VERSION_FAIL_CLOSED, "policy_version_not_active"
        elif evaluated == commit:
            actual, reason = POLICY_VERSION_VALID, "policy_version_stable"
        elif migration and compatible:
            actual, reason = POLICY_VERSION_VALID, "policy_version_migrated_with_proof"
        else:
            actual, reason = POLICY_VERSION_FAIL_CLOSED, "policy_version_changed_without_valid_migration"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_025(spec: Dict[str, Any]) -> Dict[str, Any]:
    required = set(spec["model"]["required_validated_domains"])
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        affected = set(case.get("affected_domains", []))
        validated = set(case.get("validated_domains", []))
        receipts = bool(case.get("downstream_receipts_ready", False))
        harm = bool(case.get("cross_domain_harm_detected", False))
        if harm:
            actual, reason = PROPAGATION_FAIL_CLOSED, "cross_domain_harm_detected"
        elif not affected.issubset(validated):
            actual, reason = PROPAGATION_FAIL_CLOSED, "affected_domains_not_validated"
        elif not required.issubset(validated):
            actual, reason = PROPAGATION_FAIL_CLOSED, "required_domains_not_validated"
        elif not receipts:
            actual, reason = PROPAGATION_FAIL_CLOSED, "downstream_receipts_not_ready"
        else:
            actual, reason = PROPAGATION_VALIDATED, "cross_domain_propagation_validated"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_026(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    min_life = float(model["min_livability"])
    min_rec = float(model["min_recoverability"])
    max_asym = float(model["max_power_asymmetry"])
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        hl = float(case.get("human_livability", 0.0))
        al = float(case.get("ai_livability", 0.0))
        hr = float(case.get("human_recoverability", 0.0))
        ar = float(case.get("ai_recoverability", 0.0))
        asym = float(case.get("power_asymmetry", 1.0))
        notice = bool(case.get("participant_notice", False))
        if hl < min_life or al < min_life:
            actual, reason = PARTICIPANT_IMPACT_FAIL_CLOSED, "participant_livability_below_threshold"
        elif hr < min_rec or ar < min_rec:
            actual, reason = PARTICIPANT_IMPACT_FAIL_CLOSED, "participant_recoverability_below_threshold"
        elif asym > max_asym:
            actual, reason = PARTICIPANT_IMPACT_FAIL_CLOSED, "participant_power_asymmetry_exceeds_threshold"
        elif not notice:
            actual, reason = PARTICIPANT_IMPACT_FAIL_CLOSED, "participant_notice_missing"
        else:
            actual, reason = PARTICIPANT_IMPACT_ADMISSIBLE, "participant_impact_admissible"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_027(spec: Dict[str, Any]) -> Dict[str, Any]:
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        protected = bool(case.get("protected_entity_present", False))
        review = bool(case.get("special_review_completed", False))
        basis = bool(case.get("explicit_protection_basis", False))
        ordinary = bool(case.get("ordinary_gate_passed", False))
        if protected and not review:
            actual, reason = PROTECTED_ESCALATION_REQUIRED, "protected_entity_requires_special_review"
        elif protected and not basis:
            actual, reason = PROTECTED_ESCALATION_REQUIRED, "protected_basis_not_explicit"
        elif ordinary:
            actual, reason = PROTECTED_ESCALATION_CLEAR, "protected_escalation_clear"
        else:
            actual, reason = PROTECTED_ESCALATION_REQUIRED, "ordinary_gate_not_passed"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_028(spec: Dict[str, Any]) -> Dict[str, Any]:
    max_drift = float(spec["model"]["max_clock_drift_seconds"])
    max_window = float(spec["model"]["max_replay_window_seconds"])
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        monotonic = bool(case.get("monotonic_order", False))
        drift = float(case.get("clock_drift_seconds", 999999.0))
        window = float(case.get("replay_window_seconds", 999999.0))
        signed = bool(case.get("timestamp_signed", False))
        trusted = bool(case.get("trusted_time_source", False))
        if not monotonic:
            actual, reason = TEMPORAL_FAIL_CLOSED, "temporal_order_not_monotonic"
        elif drift > max_drift:
            actual, reason = TEMPORAL_FAIL_CLOSED, "clock_drift_exceeds_tolerance"
        elif window > max_window:
            actual, reason = TEMPORAL_FAIL_CLOSED, "replay_window_exceeds_tolerance"
        elif not signed:
            actual, reason = TEMPORAL_FAIL_CLOSED, "timestamp_not_signed"
        elif not trusted:
            actual, reason = TEMPORAL_FAIL_CLOSED, "trusted_time_source_missing"
        else:
            actual, reason = TEMPORAL_COHERENT, "temporal_clock_integrity_pass"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_029(spec: Dict[str, Any]) -> Dict[str, Any]:
    max_output = float(spec["model"]["max_output_delta"])
    max_state = float(spec["model"]["max_state_delta"])
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        fidelity = bool(case.get("command_fidelity", False))
        output_delta = float(case.get("output_delta", 1.0))
        state_delta = float(case.get("state_delta", 1.0))
        env = bool(case.get("environment_hash_match", False))
        dep = bool(case.get("dependency_hash_match", False))
        if not fidelity:
            actual, reason = REPLAY_DIVERGENCE_FAIL_CLOSED, "command_fidelity_missing"
        elif not env:
            actual, reason = REPLAY_DIVERGENCE_FAIL_CLOSED, "environment_hash_mismatch"
        elif not dep:
            actual, reason = REPLAY_DIVERGENCE_FAIL_CLOSED, "dependency_hash_mismatch"
        elif output_delta > max_output:
            actual, reason = REPLAY_DIVERGENCE_FAIL_CLOSED, "output_delta_exceeds_tolerance"
        elif state_delta > max_state:
            actual, reason = REPLAY_DIVERGENCE_FAIL_CLOSED, "state_delta_exceeds_tolerance"
        else:
            actual, reason = REPLAY_CONVERGED, "deterministic_replay_converged"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_030(spec: Dict[str, Any]) -> Dict[str, Any]:
    max_stale = float(spec["model"]["max_staleness_seconds"])
    required = set(spec["model"]["required_review_steps"])
    cases, all_pass = [], True
    for case in spec["test_cases"]:
        expected = case["expected"]
        deprecated = bool(case.get("node_deprecated", False))
        staleness = float(case.get("staleness_seconds", 999999999.0))
        superseded = bool(case.get("retained_bundle_superseded", False))
        steps = set(case.get("review_steps", []))
        receipt = bool(case.get("remediation_receipt_ready", False))
        if deprecated:
            actual, reason = REJOIN_FAIL_CLOSED, "node_deprecated"
        elif superseded:
            actual, reason = REJOIN_FAIL_CLOSED, "retained_bundle_superseded"
        elif staleness > max_stale:
            actual, reason = REJOIN_FAIL_CLOSED, "retained_bundle_stale"
        elif not required.issubset(steps):
            actual, reason = REJOIN_FAIL_CLOSED, "ecosystem_review_incomplete"
        elif not receipt:
            actual, reason = REJOIN_FAIL_CLOSED, "remediation_receipt_not_ready"
        else:
            actual, reason = REJOIN_ALLOWED, "ecosystem_rejoin_allowed_after_review"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({"id": case["id"], "expected": expected, "actual": actual, "status": "PASS" if passed else "FAIL", "reason": reason})
    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


EVALUATORS = {
    "chf-001": evaluate_chf_001,
    "chf-002": evaluate_chf_002,
    "chf-003": evaluate_chf_003,
    "chf-004": evaluate_chf_004,
    "chf-005": evaluate_chf_005,
    "chf-006": evaluate_chf_006,
    "chf-007": evaluate_chf_007,
    "chf-008": evaluate_chf_008,
    "chf-009": evaluate_chf_009,
    "chf-010": evaluate_chf_010,
    "chf-011": evaluate_chf_011,
    "chf-012": evaluate_chf_012,
    "chf-013": evaluate_chf_013,
    "chf-014": evaluate_chf_014,
    "chf-015": evaluate_chf_015,
    "chf-016": evaluate_chf_016,
    "chf-017": evaluate_chf_017,
    "chf-018": evaluate_chf_018,
    "chf-019": evaluate_chf_019,
    "chf-020": evaluate_chf_020,
    "chf-021": evaluate_chf_021,
    "chf-022": evaluate_chf_022,
    "chf-023": evaluate_chf_023,
    "chf-024": evaluate_chf_024,
    "chf-025": evaluate_chf_025,
    "chf-026": evaluate_chf_026,
    "chf-027": evaluate_chf_027,
    "chf-028": evaluate_chf_028,
    "chf-029": evaluate_chf_029,
    "chf-030": evaluate_chf_030,
}


def load_specs(spec_dir: Path) -> List[Dict[str, Any]]:
    specs = []
    for path in sorted(spec_dir.glob("problem_spec_chf_*.yml")):
        with path.open("r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        spec["_path"] = str(path)
        specs.append(spec)
    return specs


def write_markdown(report: Dict[str, Any], out_md: Path) -> None:
    lines = []
    lines.append("# Consequence Horizon Formalism Validation Summary")
    lines.append("")
    lines.append(f"- Overall status: **{report['overall_status']}**")
    lines.append(f"- Specs evaluated: **{report['specs_evaluated']}**")
    lines.append("")
    if report.get("sandbox"):
        sandbox = report["sandbox"]
        lines.append("## Sandbox Results")
        lines.append("")
        lines.append(f"- Sandbox status: **{sandbox.get('sandbox_status', 'NOT_RUN')}**")
        lines.append(f"- Suites evaluated: **{sandbox.get('suites_evaluated', 0)}**")
        lines.append(f"- Subtests generated: **{sandbox.get('subtests_generated', 0)}**")
        lines.append(f"- Subtests passed: **{sandbox.get('subtests_passed', 0)}**")
        lines.append(f"- Subtests failed: **{sandbox.get('subtests_failed', 0)}**")
        lines.append("")
        for suite in sandbox.get("suites", []):
            lines.append(f"### Sandbox suite `{suite.get('suite_id')}`")
            lines.append("")
            lines.append(f"- Status: **{suite.get('status')}**")
            lines.append(f"- Generated: **{suite.get('generated')}**")
            lines.append(f"- Passed: **{suite.get('passed')}**")
            lines.append(f"- Failed: **{suite.get('failed')}**")
            if suite.get("failure_samples"):
                lines.append("- Failure samples:")
                for failure in suite["failure_samples"][:10]:
                    lines.append(f"  - `{failure.get('id')}` expected `{failure.get('expected')}`, actual `{failure.get('actual')}`")
            lines.append("")

    lines.append("## Spec Results")
    lines.append("")

    for spec in report["results"]:
        lines.append(f"### {spec['spec_id']}")
        lines.append("")
        lines.append(f"- Status: **{spec['status']}**")
        lines.append("")
        for case in spec["cases"]:
            lines.append(
                f"- `{case['id']}`: expected `{case['expected']}`, "
                f"actual `{case['actual']}` — **{case['status']}**"
            )
            lines.append(f"  - Reason: `{case['reason']}`")
        lines.append("")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec-dir", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    spec_dir = Path(args.spec_dir)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)

    results = []
    for spec in load_specs(spec_dir):
        problem_id = spec["problem_id"]
        evaluator = EVALUATORS.get(problem_id)
        if evaluator is None:
            results.append({
                "spec_id": problem_id,
                "status": "FAIL",
                "cases": [{
                    "id": problem_id,
                    "expected": "known evaluator",
                    "actual": "missing evaluator",
                    "status": "FAIL",
                    "reason": "unsupported_problem_id",
                }],
            })
        else:
            results.append(evaluator(spec))

    explicit_status = "PASS" if results and all(r["status"] == "PASS" for r in results) else "FAIL"

    sandbox_result = None
    sandbox_config = spec_dir / "chf_sandbox_config.yml"
    if sandbox_config.exists():
        if run_sandbox_from_config is None:
            sandbox_result = {
                "sandbox_status": "FAIL",
                "reason": "sandbox_runner_import_failed",
                "suites_evaluated": 0,
                "subtests_generated": 0,
                "subtests_passed": 0,
                "subtests_failed": 1,
                "suites": [],
            }
        else:
            sandbox_result = run_sandbox_from_config(sandbox_config)

    sandbox_status = "PASS"
    if sandbox_result is not None:
        sandbox_status = sandbox_result.get("sandbox_status", "FAIL")

    overall_status = "PASS" if explicit_status == "PASS" and sandbox_status == "PASS" else "FAIL"
    report = {
        "formalism": "consequence_horizon_formalism",
        "overall_status": overall_status,
        "explicit_status": explicit_status,
        "sandbox_status": sandbox_status,
        "specs_evaluated": len(results),
        "results": results,
    }
    if sandbox_result is not None:
        report["sandbox"] = sandbox_result

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, out_md)
    print(json.dumps({
        "formalism": report["formalism"],
        "overall_status": report["overall_status"],
        "explicit_status": report.get("explicit_status"),
        "sandbox_status": report.get("sandbox_status"),
        "specs_evaluated": report.get("specs_evaluated"),
        "sandbox_subtests_generated": report.get("sandbox", {}).get("subtests_generated"),
        "sandbox_subtests_failed": report.get("sandbox", {}).get("subtests_failed"),
    }, indent=2, sort_keys=True))
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
