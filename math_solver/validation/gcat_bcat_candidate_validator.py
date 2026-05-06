#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path
from typing import Any, Dict, Tuple

ALLOW = "ALLOW"
DENY = "DENY"
FAIL_CLOSED = "FAIL_CLOSED"

def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))

def classify(vector: Dict[str, Any]) -> Tuple[str, str, Dict[str, float]]:
    params = vector.get("params")
    state = vector.get("state")
    if not isinstance(params, dict):
        return FAIL_CLOSED, "params_missing", {}
    if not isinstance(state, dict):
        return FAIL_CLOSED, "state_missing", {}

    for key in ("K", "alpha", "beta", "gamma"):
        if key not in params:
            return FAIL_CLOSED, f"param_missing_{key}", {}
        if not is_number(params[key]):
            return FAIL_CLOSED, f"param_non_numeric_{key}", {}

    for key in ("g", "c", "a", "t"):
        if key not in state:
            return FAIL_CLOSED, f"state_missing_{key}", {}
        if not is_number(state[key]):
            return FAIL_CLOSED, f"state_non_numeric_{key}", {}

    K = float(params["K"])
    alpha = float(params["alpha"])
    beta = float(params["beta"])
    gamma = float(params["gamma"])
    tol = float(params.get("simplex_tolerance", 1e-9))
    g = float(state["g"])
    c = float(state["c"])
    a = float(state["a"])
    trust = float(state["t"])

    if min(g, c, a, trust) < 0:
        return DENY, "negative_component", {"g": g, "c": c, "a": a, "t": trust}

    simplex_sum = g + c + a + trust
    if abs(simplex_sum - 1.0) > tol:
        return DENY, "simplex_violation", {"simplex_sum": simplex_sum, "simplex_error": simplex_sum - 1.0}

    legitimacy = K * (g ** alpha) * (c ** beta) * (trust ** gamma)
    invariant = a - legitimacy
    metrics = {"g": g, "c": c, "a": a, "t": trust, "simplex_sum": simplex_sum, "legitimacy": legitimacy, "invariant": invariant}

    if invariant > tol:
        return DENY, "invariant_violation", metrics

    return ALLOW, "gcat_bcat_admissible", metrics

def validate_file(path: Path) -> Dict[str, Any]:
    try:
        vector = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"file": str(path), "id": path.stem, "passed": False, "actual": FAIL_CLOSED, "reason_actual": "malformed_json", "error": str(exc)}

    expected = vector.get("expected", {})
    outcome, reason, metrics = classify(vector)
    errors = []

    if expected.get("outcome") is None:
        errors.append("expected.outcome missing")
    elif outcome != expected.get("outcome"):
        errors.append(f"outcome expected {expected.get('outcome')} got {outcome}")

    if expected.get("reason") is not None and reason != expected.get("reason"):
        errors.append(f"reason expected {expected.get('reason')} got {reason}")

    return {
        "file": str(path),
        "id": vector.get("id", path.stem),
        "name": vector.get("name", path.stem),
        "expected": expected.get("outcome"),
        "actual": outcome,
        "reason_expected": expected.get("reason"),
        "reason_actual": reason,
        "metrics": metrics,
        "passed": not errors,
        "errors": errors,
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vectors", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    vector_dir = Path(args.vectors)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    results = [validate_file(path) for path in sorted(vector_dir.glob("*.json"))]
    report = {
        "schema": "stegverse.gcat_bcat.candidate_validation_report.v1",
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r["passed"]),
            "failed": sum(1 for r in results if not r["passed"]),
        },
        "results": results,
    }
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    return 0 if report["summary"]["failed"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
