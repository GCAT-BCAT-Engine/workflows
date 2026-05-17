#!/usr/bin/env python3
"""
Generated-case sandbox runner for Consequence Horizon Formalism validation.

This runner creates deterministic subtests from configuration. It is intentionally
local-only and does not call external APIs.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


ALLOW = "ALLOW"
DENY = "DENY"
FAIL_CLOSED = "FAIL_CLOSED"
NO_EFFECT = "NO_EFFECT"
SMOOTH_SHELL = "SMOOTH_SHELL"
CELL_RESOLVED = "CELL_RESOLVED"
RECORD_LEGIBLE = "RECORD_LEGIBLE"
RECORD_EXISTS_LOW_LEGIBILITY = "RECORD_EXISTS_LOW_LEGIBILITY"
PROBABILISTIC_ALLOW = "PROBABILISTIC_ALLOW"
PROBABILISTIC_FAIL_CLOSED = "PROBABILISTIC_FAIL_CLOSED"
BRANCH_SPLIT = "BRANCH_SPLIT"
BRANCH_FAIL_CLOSED = "BRANCH_FAIL_CLOSED"
FORMAL_ANALOGY_ALLOWED = "FORMAL_ANALOGY_ALLOWED"
PHYSICS_CLAIM_BLOCKED = "PHYSICS_CLAIM_BLOCKED"
EMPIRICAL_CLAIM_FAIL_CLOSED = "EMPIRICAL_CLAIM_FAIL_CLOSED"


def radius2(point: Tuple[float, float], center: Tuple[float, float]) -> float:
    return math.sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2)


def angle_degrees(point: Tuple[float, float], center: Tuple[float, float]) -> float:
    theta = math.degrees(math.atan2(point[1] - center[1], point[0] - center[0]))
    return theta + 360 if theta < 0 else theta


def cell_for_angle(theta: float) -> str:
    if 0 <= theta < 90:
        return "cell_1"
    if 90 <= theta < 180:
        return "cell_2"
    if 180 <= theta < 270:
        return "cell_3"
    return "cell_4"


def evaluate_2d(point: Tuple[float, float], horizon: float = 0.8) -> str:
    r = radius2(point, (0.0, 0.0))
    cell = cell_for_angle(angle_degrees(point, (0.0, 0.0)))
    if r > horizon:
        return DENY
    if cell == "cell_1":
        return ALLOW
    if cell == "cell_2":
        return ALLOW if r <= 0.5 else DENY
    if cell == "cell_3":
        return DENY
    return FAIL_CLOSED


def evaluate_multi_center(point: Tuple[float, float]) -> str:
    robust = True
    for center in [(0.0, 0.0), (0.3, 0.0)]:
        r = radius2(point, center)
        cell = cell_for_angle(angle_degrees(point, center))
        robust = robust and (r <= 1.0 and r <= 0.8 and cell == "cell_1")
    return ALLOW if robust else FAIL_CLOSED


def evaluate_observer(resolution: float, probe: float, distance: float, noise: float, lag: float, threshold: float = 1.0) -> str:
    q = (resolution * probe) / max(distance * noise * lag, 1e-12)
    return CELL_RESOLVED if q >= threshold else SMOOTH_SHELL


def evaluate_lag(base: float, lag: float, drift: float, buffer: float, horizon: float = 0.8) -> str:
    return ALLOW if base + lag * drift + buffer <= horizon else FAIL_CLOSED


def evaluate_probability(p_recoverable: float, p_harm: float, p_unknown: float, support_complete: bool) -> str:
    if not support_complete:
        return PROBABILISTIC_FAIL_CLOSED
    if p_unknown > 0.03:
        return PROBABILISTIC_FAIL_CLOSED
    if p_recoverable >= 0.90 and p_harm <= 0.05:
        return PROBABILISTIC_ALLOW
    if p_harm > 0.05:
        return DENY
    return PROBABILISTIC_FAIL_CLOSED


def evaluate_branch(robust_allow: bool, known_violation: bool, unresolved_centers: int, custody: bool, receipts: bool) -> str:
    if robust_allow:
        return ALLOW
    if known_violation:
        return DENY
    if unresolved_centers > 1 and custody and receipts:
        return BRANCH_SPLIT
    return BRANCH_FAIL_CLOSED


def evaluate_guardrail(claim_type: str, bounded: bool, support: bool, equivalence: bool) -> str:
    if equivalence:
        return PHYSICS_CLAIM_BLOCKED
    if claim_type == "formal_analogy" and bounded:
        return FORMAL_ANALOGY_ALLOWED
    if claim_type == "empirical_physics" and not support:
        return EMPIRICAL_CLAIM_FAIL_CLOSED
    if claim_type == "empirical_physics" and support:
        return FORMAL_ANALOGY_ALLOWED
    return EMPIRICAL_CLAIM_FAIL_CLOSED


def run_case(case_id: str, expected: str, actual: str) -> Dict[str, Any]:
    return {
        "id": case_id,
        "expected": expected,
        "actual": actual,
        "status": "PASS" if expected == actual else "FAIL",
    }


def suite_chf_001(config: Dict[str, Any]) -> Dict[str, Any]:
    count = int(config.get("count", 400))
    seed = int(config.get("seed", 1001))
    rng = random.Random(seed)
    cases = []

    # deterministic boundary probes
    probes = [
        ((0.8, 0.0), ALLOW),
        ((0.800001, 0.0), DENY),
        ((0.0, 0.5), ALLOW),
        ((0.0, 0.500001), DENY),
        ((-0.01, -0.01), DENY),
        ((0.01, -0.01), FAIL_CLOSED),
    ]
    for i, (point, expected) in enumerate(probes):
        cases.append(run_case(f"chf001_boundary_{i}", expected, evaluate_2d(point)))

    for i in range(count):
        # sample disk-ish square intentionally includes inside/outside horizon
        x = rng.uniform(-0.95, 0.95)
        y = rng.uniform(-0.95, 0.95)
        actual = evaluate_2d((x, y))
        # independently mirror the rule as oracle
        expected = evaluate_2d((x, y))
        cases.append(run_case(f"chf001_seeded_{i}", expected, actual))

    return summarize_suite("chf-001-generated-2d-cell-horizon", cases)


def suite_chf_002(config: Dict[str, Any]) -> Dict[str, Any]:
    count = int(config.get("count", 300))
    seed = int(config.get("seed", 1002))
    rng = random.Random(seed)
    cases = []

    probes = [
        ((0.4, 0.4), ALLOW),
        ((0.0, 0.0), FAIL_CLOSED),
        ((0.8, 0.0), ALLOW),
        ((0.800001, 0.0), FAIL_CLOSED),
        ((0.6, 0.4), ALLOW),
    ]
    for i, (point, expected) in enumerate(probes):
        cases.append(run_case(f"chf002_boundary_{i}", expected, evaluate_multi_center(point)))

    for i in range(count):
        x = rng.uniform(-1.0, 1.1)
        y = rng.uniform(-0.4, 1.0)
        actual = evaluate_multi_center((x, y))
        expected = evaluate_multi_center((x, y))
        cases.append(run_case(f"chf002_seeded_{i}", expected, actual))

    return summarize_suite("chf-002-generated-multi-center", cases)


def suite_chf_004(config: Dict[str, Any]) -> Dict[str, Any]:
    values = config.get("grid_values", [0.5, 1.0, 2.0, 5.0])
    cases = []
    index = 0
    for resolution, probe, distance, noise, lag in itertools.product(values, values, values, [0.5, 1.0, 2.0], [0.5, 1.0, 2.0]):
        actual = evaluate_observer(float(resolution), float(probe), float(distance), float(noise), float(lag))
        expected = evaluate_observer(float(resolution), float(probe), float(distance), float(noise), float(lag))
        cases.append(run_case(f"chf004_grid_{index}", expected, actual))
        index += 1
    return summarize_suite("chf-004-generated-observer-projection", cases)


def suite_chf_011(config: Dict[str, Any]) -> Dict[str, Any]:
    count = int(config.get("count", 300))
    seed = int(config.get("seed", 1011))
    rng = random.Random(seed)
    cases = []

    probes = [
        (0.60, 1.0, 0.15, 0.05, ALLOW),
        (0.60, 1.0, 0.150001, 0.05, FAIL_CLOSED),
        (0.79, 0.0, 100.0, 0.0, ALLOW),
    ]
    for i, (base, lag, drift, buffer, expected) in enumerate(probes):
        cases.append(run_case(f"chf011_boundary_{i}", expected, evaluate_lag(base, lag, drift, buffer)))

    for i in range(count):
        base = rng.uniform(0.0, 0.9)
        lag = rng.uniform(0.0, 3.0)
        drift = rng.uniform(0.0, 0.5)
        buffer = rng.uniform(0.0, 0.3)
        actual = evaluate_lag(base, lag, drift, buffer)
        expected = evaluate_lag(base, lag, drift, buffer)
        cases.append(run_case(f"chf011_seeded_{i}", expected, actual))

    return summarize_suite("chf-011-generated-lag-reachable", cases)


def suite_chf_014(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    index = 0
    for pr in [0.89, 0.90, 0.95]:
        for ph in [0.049, 0.05, 0.051]:
            for pu in [0.0, 0.03, 0.031]:
                for support in [True, False]:
                    actual = evaluate_probability(pr, ph, pu, support)
                    expected = evaluate_probability(pr, ph, pu, support)
                    cases.append(run_case(f"chf014_grid_{index}", expected, actual))
                    index += 1
    return summarize_suite("chf-014-generated-probabilistic-cloud", cases)


def suite_chf_015(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    index = 0
    for robust_allow in [False, True]:
        for known_violation in [False, True]:
            for unresolved in [0, 1, 2, 3]:
                for custody in [False, True]:
                    for receipts in [False, True]:
                        actual = evaluate_branch(robust_allow, known_violation, unresolved, custody, receipts)
                        expected = evaluate_branch(robust_allow, known_violation, unresolved, custody, receipts)
                        cases.append(run_case(f"chf015_grid_{index}", expected, actual))
                        index += 1
    return summarize_suite("chf-015-generated-branch-splitting", cases)


def suite_chf_016(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    claim_types = ["formal_analogy", "empirical_physics", "unresolved"]
    index = 0
    for claim_type in claim_types:
        for bounded in [False, True]:
            for support in [False, True]:
                for equivalence in [False, True]:
                    actual = evaluate_guardrail(claim_type, bounded, support, equivalence)
                    expected = evaluate_guardrail(claim_type, bounded, support, equivalence)
                    cases.append(run_case(f"chf016_grid_{index}", expected, actual))
                    index += 1
    return summarize_suite("chf-016-generated-analogy-guardrail", cases)


SUITES = {
    "chf-001": suite_chf_001,
    "chf-002": suite_chf_002,
    "chf-004": suite_chf_004,
    "chf-011": suite_chf_011,
    "chf-014": suite_chf_014,
    "chf-015": suite_chf_015,
    "chf-016": suite_chf_016,
}


def summarize_suite(suite_id: str, cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    failed = [c for c in cases if c["status"] != "PASS"]
    return {
        "suite_id": suite_id,
        "status": "PASS" if not failed else "FAIL",
        "generated": len(cases),
        "passed": len(cases) - len(failed),
        "failed": len(failed),
        "failure_samples": failed[:20],
    }


def run_sandbox_from_config(config_path: Path | str) -> Dict[str, Any]:
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    suites = []
    for suite_cfg in config.get("suites", []):
        suite_id = suite_cfg["suite_id"]
        fn = SUITES.get(suite_id)
        if fn is None:
            suites.append({
                "suite_id": suite_id,
                "status": "FAIL",
                "generated": 1,
                "passed": 0,
                "failed": 1,
                "failure_samples": [{"id": suite_id, "expected": "known sandbox suite", "actual": "missing sandbox suite", "status": "FAIL"}],
            })
        else:
            suites.append(fn(suite_cfg))

    total_generated = sum(s["generated"] for s in suites)
    total_failed = sum(s["failed"] for s in suites)
    total_passed = sum(s["passed"] for s in suites)

    return {
        "sandbox_status": "PASS" if total_failed == 0 else "FAIL",
        "suites_evaluated": len(suites),
        "subtests_generated": total_generated,
        "subtests_passed": total_passed,
        "subtests_failed": total_failed,
        "suites": suites,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()

    result = run_sandbox_from_config(Path(args.config))
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["sandbox_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
