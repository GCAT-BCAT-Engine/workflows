"""
iw_validator.py
----------------

This module defines a simple admissibility validator for **Inference Window (IW)**
candidates.  The inference window gate assesses whether a model's
information window is sufficiently broad to support a decision.  A
candidate must specify the size of its inference window (as a fraction
between 0 and 1) and a minimum acceptable threshold.  Costs are
computed based on how far the window size is from the maximum (1.0),
weighted by a configurable factor.  If the window size falls below
``window_min`` then the candidate is denied outright.  Otherwise the
computed cost is compared against a budget; if the cost exceeds the
budget the candidate is denied, otherwise it is allowed.

The expected candidate JSON structure is:

.. code-block:: json

    {
      "candidate_id": "IW_001",
      "inference_window": {
        "size": 0.9
      },
      "params": {
        "window_min": 0.5,
        "lambda_w": 1.0,
        "base_cost": 1.0
      },
      "budget": {
        "window_cost": 0.6
      }
    }

The validator proceeds in the following order:

1. **Hard gates**:
   * If the window size is missing or not a number, outcome is
     ``FAIL_CLOSED`` with a reason of ``missing_size`` or
     ``invalid_size``.
   * If ``size`` is outside the inclusive range [0, 1], outcome is
     ``FAIL_CLOSED`` with reason ``invalid_size``.
   * If a ``window_min`` threshold is provided and ``size`` is less
     than ``window_min``, outcome is ``DENY`` with reason
     ``window_size_below_threshold``.
2. **Cost calculation**:
   * Compute ``cost_W = lambda_w * base_cost * (1 - size)``.  This
     yields zero cost when the window size is 1.0, and higher cost as
     the size shrinks toward 0.
   * Total cost is just ``cost_W`` for this layer.  A cost budget may
     be specified in ``budget['window_cost']``.
   * If a budget is provided and the computed cost exceeds it, the
     outcome is ``DENY`` with reason ``budget_exceeded``.
   * Otherwise the candidate is ``ALLOW`` and the reason is
     ``iw_admissible``.

The module also provides a command-line interface allowing bulk
validation of a directory of candidate files.  It emits a JSON report
and a Markdown summary when invoked with the appropriate arguments.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Dict, Tuple


def validate_iw_candidate(candidate: Dict) -> Tuple[str, str, Dict[str, float]]:
    """Validate an inference window candidate.

    Parameters
    ----------
    candidate : dict
        A dictionary containing the keys ``candidate_id``,
        ``inference_window``, ``params``, and ``budget`` as described
        above.

    Returns
    -------
    outcome : str
        One of ``ALLOW``, ``DENY`` or ``FAIL_CLOSED``.
    reason : str
        A short machine‑friendly reason string.
    cost : dict
        A dictionary with keys ``cost_W``, ``total_cost``, and
        ``budget``, populated only for ``ALLOW`` and ``DENY`` outcomes.
    """
    cid = candidate.get("candidate_id", "unknown")
    inference = candidate.get("inference_window", {}) or {}
    params = candidate.get("params", {}) or {}
    budget = candidate.get("budget", {}) or {}

    size = inference.get("size")
    window_min = params.get("window_min")
    lambda_w = params.get("lambda_w", 1.0)
    base_cost = params.get("base_cost", 1.0)
    window_budget = budget.get("window_cost")

    # Hard gates: ensure size exists and is a number within [0, 1]
    if size is None:
        return "FAIL_CLOSED", "missing_size", {}
    if not isinstance(size, (int, float)):
        return "FAIL_CLOSED", "invalid_size", {}
    if size < 0.0 or size > 1.0:
        return "FAIL_CLOSED", "invalid_size", {}
    # Check minimum threshold if provided
    if window_min is not None and isinstance(window_min, (int, float)):
        if size < window_min:
            return "DENY", "window_size_below_threshold", {}

    # Compute cost
    cost_W = lambda_w * base_cost * (1.0 - size)
    total_cost = cost_W
    cost_detail = {
        "cost_W": cost_W,
        "total_cost": total_cost,
        "budget": window_budget,
    }
    if window_budget is not None and total_cost > window_budget:
        return "DENY", "budget_exceeded", cost_detail
    return "ALLOW", "iw_admissible", cost_detail


def load_candidate(file_path: str) -> Dict:
    """Load a candidate JSON file and return a dictionary."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    """Command-line entry point for validating a directory of candidates."""
    parser = argparse.ArgumentParser(description="Validate Inference Window candidates")
    parser.add_argument("--vectors", required=True, help="Directory containing candidate JSON files")
    parser.add_argument("--report", default=None, help="Path to write JSON report")
    parser.add_argument("--summary", default=None, help="Path to write summary Markdown")
    args = parser.parse_args()

    vector_dir = args.vectors
    results = []
    counts = {"ALLOW": 0, "DENY": 0, "FAIL_CLOSED": 0}

    for fname in sorted(os.listdir(vector_dir)):
        if not fname.lower().endswith(".json"):
            continue
        fpath = os.path.join(vector_dir, fname)
        try:
            candidate = load_candidate(fpath)
        except Exception as exc:
            results.append({
                "candidate_id": fname,
                "outcome": "FAIL_CLOSED",
                "reason": "invalid_json",
                "error": str(exc),
                "cost": {},
            })
            counts["FAIL_CLOSED"] += 1
            continue
        outcome, reason, cost = validate_iw_candidate(candidate)
        cid = candidate.get("candidate_id", os.path.splitext(fname)[0])
        results.append({
            "candidate_id": cid,
            "outcome": outcome,
            "reason": reason,
            "cost": cost,
        })
        counts[outcome] = counts.get(outcome, 0) + 1

    report = {
        "schema": "stegverse.sandbox.iw.validation_report.v1",
        "total": len(results),
        "allow": counts.get("ALLOW", 0),
        "deny": counts.get("DENY", 0),
        "fail_closed": counts.get("FAIL_CLOSED", 0),
        "results": results,
    }

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    else:
        print(json.dumps(report, indent=2))

    # Write markdown summary
    if args.summary:
        with open(args.summary, "w", encoding="utf-8") as f:
            f.write("# Inference Window Validation Summary\n\n")
            f.write(f"- Total candidates: **{report['total']}**\n")
            f.write(f"- Allowed: **{report['allow']}**\n")
            f.write(f"- Denied: **{report['deny']}**\n")
            f.write(f"- Fail Closed: **{report['fail_closed']}**\n\n")
            f.write("| ID | Outcome | Reason | Total Cost | Budget | Pass? |\n")
            f.write("|---|---|---|---|---|---|\n")
            for res in results:
                cid = res['candidate_id']
                outcome = res['outcome']
                reason = res['reason']
                cost = res.get('cost', {}) or {}
                total_cost = cost.get('total_cost', '')
                budget = cost.get('budget', '')
                pass_indicator = '✅' if outcome == 'ALLOW' else '❌'
                f.write(f"| {cid} | {outcome} | {reason} | {total_cost} | {budget} | {pass_indicator} |\n")


if __name__ == "__main__":
    main()