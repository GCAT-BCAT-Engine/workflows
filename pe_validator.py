"""
pe_validator.py
-----------------

This module implements a simple validator for a hypothetical
"Probability of Existence" (PE) admissibility transform.  It checks whether
a candidate's probability of existence meets a minimum threshold and
computes a cost penalty based on the gap between certainty and the
candidate's reported probability.  If the probability is missing or
invalid, the validator returns a FAIL_CLOSED outcome.  If the
probability is below the required threshold, the outcome is DENY.  A
budget may be supplied to cap the permissible cost; if the cost
exceeds the budget, the outcome is also DENY.

Candidate format:

```
{
  "candidate_id": "PE_001",
  "existence": {
    "probability": 0.9
  },
  "params": {
    "prob_min": 0.8,
    "lambda_p": 1.0,
    "base_cost": 1.0
  },
  "budget": {
    "existence_cost": 1.0
  }
}
```

Validation logic:

* Hard gates:
  - If `probability` is missing -> FAIL_CLOSED (reason: `probability_unavailable`).
  - If `probability` is not a number or outside [0, 1] -> FAIL_CLOSED (reason: `probability_invalid`).
  - If `probability` < `prob_min` -> DENY (reason: `probability_below_threshold`).
* Cost calculation:
  - cost_P = lambda_p * base_cost * (1 - probability)
  - total_cost = cost_P
  - If `existence_cost` budget is provided and total_cost > budget -> DENY (reason: `budget_exceeded`).
  - Else -> ALLOW (reason: `pe_admissible`).

The validator returns a tuple (outcome, reason, cost_dict).

"""

from __future__ import annotations

import argparse
import json
import os
from typing import Dict, Tuple, Any


def validate_pe_candidate(candidate: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
    """Validate a single PE candidate.

    Returns a tuple (outcome, reason, cost_dict).
    """
    cid = candidate.get("candidate_id", "unknown")
    existence = candidate.get("existence", {}) or {}
    params = candidate.get("params", {}) or {}
    budget = candidate.get("budget", {}) or {}

    probability = existence.get("probability")
    prob_min = params.get("prob_min", 0.0)
    lambda_p = params.get("lambda_p", 1.0)
    base_cost = params.get("base_cost", 1.0)
    existence_budget = budget.get("existence_cost")

    # Hard gates: missing probability
    if probability is None:
        return "FAIL_CLOSED", "probability_unavailable", {}
    # Probability invalid if not numeric or outside [0,1]
    if not isinstance(probability, (int, float)):
        return "FAIL_CLOSED", "probability_invalid", {}
    if probability < 0.0 or probability > 1.0:
        return "FAIL_CLOSED", "probability_invalid", {}
    # Check threshold
    if probability < prob_min:
        return "DENY", "probability_below_threshold", {}

    # Cost calculation
    cost_P = lambda_p * base_cost * (1.0 - probability)
    total_cost = cost_P
    cost_detail = {
        "cost_P": cost_P,
        "total_cost": total_cost,
        "budget": existence_budget
    }
    if existence_budget is not None and total_cost > existence_budget:
        return "DENY", "budget_exceeded", cost_detail

    return "ALLOW", "pe_admissible", cost_detail


def load_candidate(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Validate PE candidates")
    parser.add_argument("--vectors", required=True, help="Path to directory containing PE candidate JSON files")
    parser.add_argument("--report", help="Path to write JSON report", default=None)
    parser.add_argument("--summary", help="Path to write Markdown summary", default=None)
    args = parser.parse_args()

    vector_dir = args.vectors
    results = []
    counts = {"ALLOW": 0, "DENY": 0, "FAIL_CLOSED": 0}

    for fname in sorted(os.listdir(vector_dir)):
        if not fname.lower().endswith('.json'):
            continue
        fpath = os.path.join(vector_dir, fname)
        try:
            candidate = load_candidate(fpath)
        except Exception as e:
            results.append({
                "candidate_id": fname,
                "outcome": "FAIL_CLOSED",
                "reason": "invalid_json",
                "error": str(e),
                "cost": {}
            })
            counts["FAIL_CLOSED"] += 1
            continue
        outcome, reason, cost = validate_pe_candidate(candidate)
        cid = candidate.get("candidate_id", fname)
        results.append({
            "candidate_id": cid,
            "outcome": outcome,
            "reason": reason,
            "cost": cost
        })
        counts[outcome] += 1

    report = {
        "schema": "stegverse.sandbox.pe.validation_report.v1",
        "total": len(results),
        "allow": counts["ALLOW"],
        "deny": counts["DENY"],
        "fail_closed": counts["FAIL_CLOSED"],
        "results": results
    }

    if args.report:
        with open(args.report, 'w') as f:
            json.dump(report, f, indent=2)
    else:
        print(json.dumps(report, indent=2))

    if args.summary:
        with open(args.summary, 'w') as f:
            f.write("# PE Validation Summary\n\n")
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
                cost = res.get('cost', {})
                total_cost = cost.get('total_cost', '')
                budget = cost.get('budget', '')
                pass_indicator = '✅' if outcome == 'ALLOW' else '❌'
                f.write(f"| {cid} | {outcome} | {reason} | {total_cost} | {budget} | {pass_indicator} |\n")


if __name__ == '__main__':
    main()