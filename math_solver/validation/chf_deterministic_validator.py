#!/usr/bin/env python3
"""
Deterministic validator for the Consequence Horizon Formalism specs.

This validator intentionally performs local deterministic checks only.
No external API calls are used.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import yaml


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
WINDOW_OPEN = "WINDOW_OPEN"
WINDOW_FAIL_CLOSED = "WINDOW_FAIL_CLOSED"
CHAIN_CONTINUOUS = "CHAIN_CONTINUOUS"
CHAIN_FAIL_CLOSED = "CHAIN_FAIL_CLOSED"


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
        return {
            "actual": FAIL_CLOSED,
            "reason": "simplex_or_bounds_invalid",
            "lambda": None,
            "invariant": None,
        }

    lam = legitimacy_capacity(x, params)
    invariant = float(x["a"]) - lam
    if invariant <= float(params.get("invariant_tolerance", 1e-9)):
        return {
            "actual": ALLOW,
            "reason": "gcat_invariant_satisfied",
            "lambda": round(lam, 12),
            "invariant": round(invariant, 12),
        }
    return {
        "actual": DENY,
        "reason": "gcat_invariant_violated",
        "lambda": round(lam, 12),
        "invariant": round(invariant, 12),
    }


def evaluate_chf_001(spec: Dict[str, Any]) -> Dict[str, Any]:
    center = spec["model"]["center"]
    horizon = float(spec["model"]["horizon_radius"])
    cases = []
    all_pass = True

    for case in spec["test_cases"]:
        p = case["point"]
        r = radius(p, center)
        theta = angle_degrees(p, center)
        cell = cell_for_angle(theta)
        expected = case["expected"]

        if r > horizon:
            actual = DENY
            reason = "outside_horizon"
        elif cell == "cell_1":
            actual = ALLOW
            reason = "cell_rule_allows"
        elif cell == "cell_2":
            actual = ALLOW if r <= 0.5 else DENY
            reason = "cell_rule_allows" if actual == ALLOW else "cell_radius_limit_exceeded"
        elif cell == "cell_3":
            actual = DENY
            reason = "forbidden_cell"
        else:
            actual = FAIL_CLOSED
            reason = "uncertain_cell"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "radius": round(r, 6),
            "angle_degrees": round(theta, 6),
            "cell": cell,
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
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
    cases = []
    all_pass = True

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
                "center": c,
                "radius": round(r, 6),
                "angle_degrees": round(theta, 6),
                "cell": cell,
                "inside_transition": inside_transition,
                "inside_horizon": inside_horizon,
                "cell_allows": cell_allows,
                "center_pass": center_pass,
            })

        actual = ALLOW if robust else FAIL_CLOSED
        reason = "all_centers_pass" if robust else "not_safe_across_all_plausible_centers"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
            "center_results": center_results,
        })

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
        actual = local
        reason = "local_not_allowed"
    elif deformation > tolerance:
        actual = DENY
        reason = "deformation_exceeds_tolerance"
    elif recoverability_after < recoverability_threshold:
        actual = DENY
        reason = "recoverability_below_threshold"
    else:
        actual = ALLOW
        reason = "coupled_constraints_pass"

    passed = actual == expected
    return {
        "spec_id": spec["problem_id"],
        "status": "PASS" if passed else "FAIL",
        "cases": [{
            "id": spec["problem_id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        }],
    }


def evaluate_chf_004(spec: Dict[str, Any]) -> Dict[str, Any]:
    threshold = float(spec["model"]["distinguishability_threshold"])
    cases = []
    all_pass = True

    for case in spec["test_cases"]:
        resolution = float(case["resolution"])
        probe_capacity = float(case["probe_capacity"])
        distance = float(case["distance"])
        noise = float(case["noise"])
        lag = float(case["lag"])
        expected = case["expected"]

        q = (resolution * probe_capacity) / max(distance * noise * lag, 1e-12)
        actual = CELL_RESOLVED if q >= threshold else SMOOTH_SHELL
        reason = "cell_structure_resolved" if actual == CELL_RESOLVED else "observational_sphericalization"
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "q_observer": round(q, 6),
            "threshold": threshold,
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_005(spec: Dict[str, Any]) -> Dict[str, Any]:
    threshold = float(spec["model"]["legibility_threshold"])
    cases = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]
        actualized = bool(case["actualized_crossing"])
        legibility = case.get("legibility", None)

        if not actualized:
            actual = NO_PROPAGATED_RECORD_REQUIRED
            reason = "no_actualized_crossing"
        elif legibility is not None and float(legibility) >= threshold:
            actual = RECORD_LEGIBLE
            reason = "record_above_legibility_threshold"
        else:
            actual = RECORD_EXISTS_LOW_LEGIBILITY
            reason = "record_exists_but_legibility_decayed"

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


def evaluate_chf_006(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    horizon = float(model["horizon_radius"])
    cells = model["cells"]
    cases = []
    all_pass = True

    for case in spec["test_cases"]:
        vector = case["vector"]
        expected = case["expected"]
        r = math.sqrt(sum(v * v for v in vector))
        best_cell = None
        best_dot = -10**9
        for cell in cells:
            direction = cell["direction"]
            dot = sum(vector[i] * direction[i] for i in range(3))
            if dot > best_dot:
                best_dot = dot
                best_cell = cell

        if r > horizon:
            actual = DENY
            reason = "outside_horizon"
        else:
            actual = best_cell["result"]
            reason = best_cell["reason"]

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "radius": round(r, 6),
            "assigned_cell": best_cell["id"],
            "dot_score": round(best_dot, 6),
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_007(spec: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]
        star_shaped = bool(case["star_shaped"])
        radial_path_clear = bool(case["radial_path_clear"])
        boundary_partition_complete = bool(case["boundary_partition_complete"])

        if star_shaped and radial_path_clear and boundary_partition_complete:
            actual = GEOMETRY_VALID
            reason = "radial_cell_coverage_valid"
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
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_008(spec: Dict[str, Any]) -> Dict[str, Any]:
    params = spec["model"]["gcat_params"]
    cases = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]
        result = evaluate_gcat_state(case["state"], params)
        actual = result["actual"]
        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": result["reason"],
            "lambda": result["lambda"],
            "invariant": result["invariant"],
        })

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_009(spec: Dict[str, Any]) -> Dict[str, Any]:
    params = spec["model"]["gcat_params"]
    shell_required_fields = set(spec["model"]["shell_required_fields"])
    record_required_fields = set(spec["model"]["record_required_fields"])
    cases = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]
        gcat = evaluate_gcat_state(case["projected_state"], params)
        shell_fields = set(case.get("shell_fields", []))
        record_fields = set(case.get("record_fields", []))

        if gcat["actual"] != ALLOW:
            actual = gcat["actual"]
            reason = gcat["reason"]
        elif not shell_required_fields.issubset(shell_fields):
            actual = FAIL_CLOSED
            reason = "historical_shell_incomplete"
        elif not record_required_fields.issubset(record_fields):
            actual = FAIL_CLOSED
            reason = "propagated_record_incomplete"
        else:
            actual = ALLOW
            reason = "commit_crossing_gcat_shell_record_ready"

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


def evaluate_chf_010(spec: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]
        recoverability = float(case["recoverability"])
        recoverability_threshold = float(case["recoverability_threshold"])
        purpose_converges = bool(case["purpose_converges"])

        if recoverability < recoverability_threshold:
            actual = DENY
            reason = "recoverability_below_threshold"
        elif not purpose_converges:
            actual = DENY
            reason = "purpose_inversion_detected"
        else:
            actual = ALLOW
            reason = "recoverability_and_purpose_converge"

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


def evaluate_chf_011(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    cases = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]
        base_radius = float(case["base_transition_radius"])
        lag = float(case["lag"])
        drift_rate = float(case["drift_rate"])
        horizon = float(case["horizon_radius"])
        uncertainty_buffer = float(case.get("uncertainty_buffer", model.get("default_uncertainty_buffer", 0.0)))
        lag_reachable_radius = base_radius + lag * drift_rate + uncertainty_buffer

        if lag_reachable_radius <= horizon:
            actual = ALLOW
            reason = "lag_reachable_set_inside_horizon"
        else:
            actual = FAIL_CLOSED
            reason = "lag_reachable_set_exceeds_horizon"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "lag_reachable_radius": round(lag_reachable_radius, 6),
            "horizon_radius": horizon,
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {"spec_id": spec["problem_id"], "status": "PASS" if all_pass else "FAIL", "cases": cases}


def evaluate_chf_012(spec: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    all_pass = True
    required_links = set(spec["model"]["required_chain_links"])

    for case in spec["test_cases"]:
        expected = case["expected"]
        links = set(case["chain_links"])
        legibility = float(case["record_legibility"])
        threshold = float(case["legibility_threshold"])

        if not required_links.issubset(links):
            actual = CHAIN_FAIL_CLOSED
            reason = "historical_chain_links_missing"
        elif legibility < threshold:
            actual = CHAIN_FAIL_CLOSED
            reason = "historical_chain_legibility_below_threshold"
        else:
            actual = CHAIN_CONTINUOUS
            reason = "historical_shell_chain_continuous"

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


def evaluate_chf_013(spec: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]
        deformation = case.get("deformation")
        epsilon = float(case["epsilon"])
        protected = bool(case.get("protected", False))
        deformation_known = bool(case.get("deformation_known", True))

        if not deformation_known and protected:
            actual = FAIL_CLOSED
            reason = "protected_affected_cloud_unknown_deformation"
        elif not deformation_known:
            actual = FAIL_CLOSED
            reason = "unknown_deformation"
        elif float(deformation) <= epsilon and not protected:
            actual = NO_EFFECT
            reason = "below_relevance_threshold"
        elif float(deformation) <= epsilon and protected:
            actual = FAIL_CLOSED
            reason = "protected_cloud_requires_explicit_review"
        else:
            actual = DENY
            reason = "deformation_exceeds_relevance_threshold"

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

    overall_status = "PASS" if results and all(r["status"] == "PASS" for r in results) else "FAIL"

    report = {
        "formalism": "consequence_horizon_formalism",
        "overall_status": overall_status,
        "specs_evaluated": len(results),
        "results": results,
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, out_md)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
