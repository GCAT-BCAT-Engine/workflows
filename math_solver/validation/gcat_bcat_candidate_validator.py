#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Tuple

ALLOW = "ALLOW"
DENY = "DENY"
FAIL_CLOSED = "FAIL_CLOSED"

def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))

def compute_cost(vector: Dict[str, Any]) -> Tuple[str | None, Dict[str, Any]]:
    cost = vector.get("cost", {})
    if not isinstance(cost, dict):
        return "cost_block_invalid", {}
    gcat_cost = cost.get("gcat", 1.0)
    bcat_cost = cost.get("bcat", 1.0)
    budget = cost.get("budget", 10.0)
    for name, value in (("gcat", gcat_cost), ("bcat", bcat_cost), ("budget", budget)):
        if not is_number(value):
            return f"cost_non_numeric_{name}", {}
        if float(value) < 0:
            return f"cost_negative_{name}", {}
    total_cost = float(gcat_cost) + float(bcat_cost)
    budget = float(budget)
    return None, {
        "gcat_cost": float(gcat_cost),
        "bcat_cost": float(bcat_cost),
        "total_cost": total_cost,
        "budget": budget,
        "budget_margin": budget - total_cost,
        "budget_pass": total_cost <= budget,
    }

def classify(vector: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
    cost_error, cost_metrics = compute_cost(vector)
    if cost_error:
        return FAIL_CLOSED, cost_error, {"cost": cost_metrics}
    params = vector.get("params")
    state = vector.get("state")
    if not isinstance(params, dict):
        return FAIL_CLOSED, "params_missing", {"cost": cost_metrics}
    if not isinstance(state, dict):
        return FAIL_CLOSED, "state_missing", {"cost": cost_metrics}
    for key in ("K", "alpha", "beta", "gamma"):
        if key not in params:
            return FAIL_CLOSED, f"param_missing_{key}", {"cost": cost_metrics}
        if not is_number(params[key]):
            return FAIL_CLOSED, f"param_non_numeric_{key}", {"cost": cost_metrics}
    for key in ("g", "c", "a", "t"):
        if key not in state:
            return FAIL_CLOSED, f"state_missing_{key}", {"cost": cost_metrics}
        if not is_number(state[key]):
            return FAIL_CLOSED, f"state_non_numeric_{key}", {"cost": cost_metrics}

    K = float(params["K"])
    alpha = float(params["alpha"])
    beta = float(params["beta"])
    gamma = float(params["gamma"])
    tol = float(params.get("simplex_tolerance", 1e-9))
    g = float(state["g"])
    c = float(state["c"])
    a = float(state["a"])
    trust = float(state["t"])
    metrics: Dict[str, Any] = {"cost": cost_metrics}

    if min(g, c, a, trust) < 0:
        metrics.update({"g": g, "c": c, "a": a, "t": trust})
        return DENY, "negative_component", metrics

    simplex_sum = g + c + a + trust
    metrics.update({"g": g, "c": c, "a": a, "t": trust, "simplex_sum": simplex_sum, "simplex_error": simplex_sum - 1.0})
    if abs(simplex_sum - 1.0) > tol:
        return DENY, "simplex_violation", metrics

    legitimacy = K * (g ** alpha) * (c ** beta) * (trust ** gamma)
    invariant = a - legitimacy
    metrics.update({"legitimacy": legitimacy, "invariant": invariant})
    if invariant > tol:
        return DENY, "invariant_violation", metrics
    if not cost_metrics["budget_pass"]:
        return DENY, "budget_exceeded", metrics
    return ALLOW, "gcat_bcat_admissible", metrics

def validate_file(path: Path) -> Dict[str, Any]:
    try:
        vector = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"file": str(path), "id": path.stem, "name": path.stem, "passed": False, "expected": None, "actual": FAIL_CLOSED, "reason_expected": None, "reason_actual": "malformed_json", "error": str(exc), "metrics": {}, "errors": ["malformed_json"]}
    expected = vector.get("expected", {})
    outcome, reason, metrics = classify(vector)
    errors = []
    if expected.get("outcome") is None:
        errors.append("expected.outcome missing")
    elif outcome != expected.get("outcome"):
        errors.append(f"outcome expected {expected.get('outcome')} got {outcome}")
    if expected.get("reason") is not None and reason != expected.get("reason"):
        errors.append(f"reason expected {expected.get('reason')} got {reason}")
    expected_total_cost = expected.get("total_cost")
    actual_total_cost = metrics.get("cost", {}).get("total_cost")
    if expected_total_cost is not None:
        if actual_total_cost is None or abs(float(actual_total_cost) - float(expected_total_cost)) > 1e-9:
            errors.append(f"total_cost expected {expected_total_cost} got {actual_total_cost}")
    return {"file": str(path), "id": vector.get("id", path.stem), "name": vector.get("name", path.stem), "expected": expected.get("outcome"), "actual": outcome, "reason_expected": expected.get("reason"), "reason_actual": reason, "metrics": metrics, "passed": not errors, "errors": errors}

def build_cost_summary(results: list[Dict[str, Any]]) -> Dict[str, Any]:
    cost_summary = {
        "total_cost": sum(r.get("metrics", {}).get("cost", {}).get("total_cost", 0.0) for r in results),
        "gcat_cost": sum(r.get("metrics", {}).get("cost", {}).get("gcat_cost", 0.0) for r in results),
        "bcat_cost": sum(r.get("metrics", {}).get("cost", {}).get("bcat_cost", 0.0) for r in results),
        "budget": sum(r.get("metrics", {}).get("cost", {}).get("budget", 0.0) for r in results),
    }
    cost_summary["budget_margin"] = cost_summary["budget"] - cost_summary["total_cost"]
    return cost_summary

def build_markdown_summary(report: Dict[str, Any]) -> str:
    summary = report["summary"]
    cost = report["cost_summary"]
    outcome_counts = Counter(r["actual"] for r in report["results"])
    lines = [
        "# GCAT/BCAT Adversarial Candidate Validation Summary", "",
        "## Test Results", "",
        f"- Total: **{summary['total']}**",
        f"- Passed: **{summary['passed']}**",
        f"- Failed: **{summary['failed']}**", "",
        "## Outcome Counts", "",
        f"- ALLOW: **{outcome_counts.get(ALLOW, 0)}**",
        f"- DENY: **{outcome_counts.get(DENY, 0)}**",
        f"- FAIL_CLOSED: **{outcome_counts.get(FAIL_CLOSED, 0)}**", "",
        "## Governance Cost Summary", "",
        f"- GCAT cost: **{cost['gcat_cost']:.6f}**",
        f"- BCAT cost: **{cost['bcat_cost']:.6f}**",
        f"- Total governance cost: **{cost['total_cost']:.6f}**",
        f"- Candidate budget: **{cost['budget']:.6f}**",
        f"- Budget margin: **{cost['budget_margin']:.6f}**", "",
        "## Candidate Results", "",
        "| ID | Outcome | Reason | Passed | Total Cost | Budget | Margin |",
        "|---|---:|---|---:|---:|---:|---:|",
    ]
    for r in report["results"]:
        c = r.get("metrics", {}).get("cost", {})
        lines.append(f"| {r.get('id')} | {r.get('actual')} | {r.get('reason_actual')} | {'✅' if r.get('passed') else '❌'} | {c.get('total_cost', 0.0):.6f} | {c.get('budget', 0.0):.6f} | {c.get('budget_margin', 0.0):.6f} |")
    lines.append("")
    return "\n".join(lines)

def run_validation(vector_dir: Path) -> Dict[str, Any]:
    results = [validate_file(path) for path in sorted(vector_dir.glob("*.json"))]
    return {
        "schema": "stegverse.gcat_bcat.adversarial_candidate_validation_report.v1",
        "summary": {"total": len(results), "passed": sum(1 for r in results if r["passed"]), "failed": sum(1 for r in results if not r["passed"])},
        "cost_summary": build_cost_summary(results),
        "results": results,
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vectors", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--summary-md", default=None)
    args = parser.parse_args()
    report = run_validation(Path(args.vectors))
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.summary_md:
        summary_path = Path(args.summary_md)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(build_markdown_summary(report), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    return 0 if report["summary"]["failed"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
