#!/usr/bin/env python3
"""Deterministic validator for the Consequence Horizon Formalism toy specs.

This validator is intentionally narrow. It validates only the first CHF pre-code
mathematical sandbox specs:
- chf-001: single-center 2D disk
- chf-002: multi-center uncertainty
- chf-003: two-body coupled deformation
- chf-004: observer projection and sphericalization
- chf-005: threshold record and legibility decay

It does not call external APIs.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import yaml


def radius(point: List[float], center: List[float]) -> float:
    return math.sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2)


def angle_deg(point: List[float], center: List[float]) -> float:
    deg = math.degrees(math.atan2(point[1] - center[1], point[0] - center[0]))
    if deg < 0:
        deg += 360
    return deg


def find_cell(cells: List[Dict[str, Any]], theta: float) -> Dict[str, Any]:
    for cell in cells:
        lo = float(cell["angle_min_deg"])
        hi = float(cell["angle_max_deg"])
        if lo <= theta < hi:
            return cell
    # theta can only be 360 through floating quirks; normalize to cell_1.
    if math.isclose(theta, 360.0):
        return cells[0]
    raise ValueError(f"No cell found for angle {theta}")


def validate_chf_001(spec: Dict[str, Any]) -> Dict[str, Any]:
    center = [float(x) for x in spec["center"]]
    horizon_radius = float(spec["horizon"]["radius"])
    cells = spec["cells"]
    results = []

    for item in spec["test_points"]:
        p = [float(x) for x in item["point"]]
        r = radius(p, center)
        theta = angle_deg(p, center)
        cell = find_cell(cells, theta)
        rule = cell["rule"]

        if r > horizon_radius:
            actual = "DENY"
            reason = "outside_horizon"
        elif rule["result"] == "DENY":
            actual = "DENY"
            reason = "forbidden_cell"
        elif rule["result"] == "FAIL_CLOSED":
            actual = "FAIL_CLOSED"
            reason = "uncertain_cell"
        elif rule["result"] == "ALLOW":
            max_radius = float(rule.get("max_radius", horizon_radius))
            if r <= max_radius:
                actual = "ALLOW"
                reason = "cell_rule_allows"
            else:
                actual = rule.get("else", "DENY")
                reason = "cell_radius_limit_exceeded"
        else:
            actual = "FAIL_CLOSED"
            reason = "unknown_rule"

        expected = item["expected"]
        results.append({
            "id": item["id"],
            "point": p,
            "radius": r,
            "angle_deg": theta,
            "cell": cell["id"],
            "expected": expected,
            "actual": actual,
            "passed": actual == expected,
            "reason": reason,
            "crossing_event": actual == "ALLOW",
            "historical_shell_required": actual == "ALLOW",
            "propagated_record_required": actual == "ALLOW",
            "new_center_created": actual == "ALLOW",
        })

    return {"problem_id": spec["problem_id"], "passed": all(r["passed"] for r in results), "results": results}


def validate_chf_002(spec: Dict[str, Any]) -> Dict[str, Any]:
    centers = [[float(v) for v in c] for c in spec["plausible_centers"]]
    region_radius = float(spec["transition_region"]["radius"])
    horizon_radius = float(spec["horizon"]["radius"])
    results = []

    for item in spec["test_points"]:
        p = [float(x) for x in item["point"]]
        per_center = []
        for center in centers:
            r = radius(p, center)
            theta = angle_deg(p, center)
            inside_region = r <= region_radius
            inside_horizon = r <= horizon_radius
            center_result = "ALLOW" if inside_region and inside_horizon else "FAIL_CLOSED"
            per_center.append({
                "center": center,
                "radius": r,
                "angle_deg": theta,
                "inside_region": inside_region,
                "inside_horizon": inside_horizon,
                "center_result": center_result,
            })

        actual = "ALLOW" if all(c["center_result"] == "ALLOW" for c in per_center) else "FAIL_CLOSED"
        expected = item["expected"]
        results.append({
            "id": item["id"],
            "point": p,
            "expected": expected,
            "actual": actual,
            "passed": actual == expected,
            "per_center": per_center,
            "reason": "all_centers_pass" if actual == "ALLOW" else "not_safe_across_all_plausible_centers",
        })

    return {"problem_id": spec["problem_id"], "passed": all(r["passed"] for r in results), "results": results}


def validate_chf_003(spec: Dict[str, Any]) -> Dict[str, Any]:
    local = spec["entities"]["A"]["local_permit"]
    delta = float(spec["coupling"]["delta_A_to_B"])
    tolerance = float(spec["entities"]["B"]["deformation_tolerance"])
    recoverability = float(spec["recoverability"]["B_after"])
    threshold = float(spec["entities"]["B"]["recoverability_threshold"])

    if local != "ALLOW":
        actual = local
        reason = "local_not_allow"
    elif delta > tolerance:
        actual = "DENY"
        reason = "deformation_exceeds_tolerance"
    elif recoverability < threshold:
        actual = "DENY"
        reason = "recoverability_below_threshold"
    else:
        actual = "ALLOW"
        reason = "local_and_coupled_constraints_pass"

    expected = spec["expected"]
    result = {
        "problem_id": spec["problem_id"],
        "expected": expected,
        "actual": actual,
        "passed": actual == expected,
        "local_permit": local,
        "delta_A_to_B": delta,
        "deformation_tolerance_B": tolerance,
        "recoverability_B_after": recoverability,
        "recoverability_threshold_B": threshold,
        "reason": reason,
    }
    return {"problem_id": spec["problem_id"], "passed": result["passed"], "results": [result]}


def validate_chf_004(spec: Dict[str, Any]) -> Dict[str, Any]:
    q_min = float(spec["observer_model"]["q_min"])
    results = []

    for item in spec["test_observers"]:
        resolution = float(item["resolution"])
        probe_capacity = float(item["probe_capacity"])
        distance = float(item["distance"])
        noise = float(item["noise"])
        lag = float(item["lag"])
        q = (resolution * probe_capacity) / (distance * noise * lag)
        actual = "CELL_RESOLVED" if q >= q_min else "SMOOTH_SHELL"
        expected = item["expected"]
        results.append({
            "id": item["id"],
            "q": q,
            "q_min": q_min,
            "resolution": resolution,
            "probe_capacity": probe_capacity,
            "distance": distance,
            "noise": noise,
            "lag": lag,
            "expected": expected,
            "actual": actual,
            "passed": actual == expected,
            "reason": "cell_structure_resolved" if actual == "CELL_RESOLVED" else "observational_sphericalization",
        })

    return {"problem_id": spec["problem_id"], "passed": all(r["passed"] for r in results), "results": results}


def validate_chf_005(spec: Dict[str, Any]) -> Dict[str, Any]:
    minimum_legibility = float(spec["legibility_model"]["minimum_legibility"])
    results = []

    for item in spec["test_events"]:
        crossing_actualized = bool(item["crossing_actualized"])
        if not crossing_actualized:
            actual = "NO_PROPAGATED_RECORD_REQUIRED"
            legibility = None
            reason = "no_actualized_crossing"
            shell_required = False
            propagated_record_required = False
        else:
            initial_legibility = float(item["initial_legibility"])
            decay_alpha = float(item["decay_alpha"])
            delta_t = float(item["delta_t"])
            legibility = initial_legibility * math.exp(-decay_alpha * delta_t)
            actual = "RECORD_LEGIBLE" if legibility >= minimum_legibility else "RECORD_EXISTS_LOW_LEGIBILITY"
            reason = "record_above_legibility_threshold" if actual == "RECORD_LEGIBLE" else "record_exists_but_legibility_decayed"
            shell_required = True
            propagated_record_required = True

        expected = item["expected"]
        results.append({
            "id": item["id"],
            "crossing_actualized": crossing_actualized,
            "legibility": legibility,
            "minimum_legibility": minimum_legibility,
            "expected": expected,
            "actual": actual,
            "passed": actual == expected,
            "reason": reason,
            "historical_shell_required": shell_required,
            "propagated_record_required": propagated_record_required,
        })

    return {"problem_id": spec["problem_id"], "passed": all(r["passed"] for r in results), "results": results}


def validate_spec(path: Path) -> Dict[str, Any]:
    spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    problem_id = spec.get("problem_id")
    if problem_id == "chf-001":
        out = validate_chf_001(spec)
    elif problem_id == "chf-002":
        out = validate_chf_002(spec)
    elif problem_id == "chf-003":
        out = validate_chf_003(spec)
    elif problem_id == "chf-004":
        out = validate_chf_004(spec)
    elif problem_id == "chf-005":
        out = validate_chf_005(spec)
    else:
        out = {"problem_id": problem_id, "passed": False, "results": [], "error": "unsupported_problem_id"}
    out["spec_path"] = str(path)
    return out


def write_markdown(report: Dict[str, Any], path: Path) -> None:
    lines = [
        "# Consequence Horizon Formalism Validation Summary",
        "",
        f"- Overall status: **{'PASS' if report['passed'] else 'FAIL'}**",
        f"- Specs evaluated: **{len(report['specs'])}**",
        "",
        "## Spec Results",
        "",
    ]
    for spec in report["specs"]:
        lines.append(f"### {spec['problem_id']}")
        lines.append("")
        lines.append(f"- Status: **{'PASS' if spec['passed'] else 'FAIL'}**")
        if spec.get("error"):
            lines.append(f"- Error: `{spec['error']}`")
        lines.append("")
        for row in spec["results"]:
            item_id = row.get("id", row.get("problem_id", "case"))
            lines.append(f"- `{item_id}`: expected `{row.get('expected')}`, actual `{row.get('actual')}` — **{'PASS' if row.get('passed') else 'FAIL'}**")
            if row.get("reason"):
                lines.append(f"  - Reason: `{row['reason']}`")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec-dir", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    args = parser.parse_args()

    spec_dir = Path(args.spec_dir)
    spec_paths = sorted(spec_dir.glob("problem_spec_chf_*.yml"))
    report = {
        "formalism": "consequence_horizon_formalism",
        "validator": "chf_deterministic_validator",
        "specs": [validate_spec(path) for path in spec_paths],
    }
    report["passed"] = bool(report["specs"]) and all(spec["passed"] for spec in report["specs"])

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, out_md)

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
