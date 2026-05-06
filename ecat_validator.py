import json
import os
import argparse


def validate_ecat_candidate(candidate: dict):
    """
    Validate an ECAT candidate according to simple admissibility rules.

    A candidate must contain the following keys:
      - candidate_id: unique identifier
      - entity: dict with keys 'reputation', 'stake', 'history' and optional
        'co_owner_rejection' (boolean)
      - params: dict with keys 'reputation_min', 'stake_min', 'history_max',
        and optional lambda weights and base_cost
      - budget: dict with key 'entity_cost' specifying the maximum allowable cost

    The validation logic proceeds in this order:
      1. Hard gates:
         * If co_owner_rejection is True, outcome is DENY.
         * If reputation is missing (None), outcome is FAIL_CLOSED.
         * If reputation < reputation_min, outcome is DENY.
         * If stake < stake_min, outcome is DENY.
         * If history is missing (None), outcome is FAIL_CLOSED.
         * If history > history_max, outcome is DENY.
      2. Cost calculation:
         * Compute cost_R = lambda_r * base_cost * (1 - reputation).
         * Compute cost_S = lambda_s * base_cost * max(0, stake_min - stake).
         * Compute cost_H = lambda_h * base_cost * history.
         * Total cost = cost_R + cost_S + cost_H.
         * If total cost > entity_cost budget, outcome is DENY.
         * Otherwise, outcome is ALLOW.

    Returns a tuple (outcome, reason, cost_dict).
    """
    cid = candidate.get("candidate_id", "unknown")
    entity = candidate.get("entity", {})
    params = candidate.get("params", {})
    budget = candidate.get("budget", {})

    # Extract entity metrics
    reputation = entity.get("reputation")
    stake = entity.get("stake")
    history = entity.get("history")
    co_owner_rejection = entity.get("co_owner_rejection", False)

    # Extract params and thresholds
    reputation_min = params.get("reputation_min")
    stake_min = params.get("stake_min")
    history_max = params.get("history_max")
    lambda_r = params.get("lambda_r", 1.0)
    lambda_s = params.get("lambda_s", 1.0)
    lambda_h = params.get("lambda_h", 1.0)
    base_cost = params.get("base_cost", 1.0)

    entity_cost_budget = budget.get("entity_cost", None)

    # Hard gates
    if co_owner_rejection:
        return "DENY", "co_owner_rejection", {}
    if reputation is None:
        return "FAIL_CLOSED", "missing_reputation", {}
    if reputation_min is not None and reputation < reputation_min:
        return "DENY", "low_reputation", {}
    if stake is None:
        return "FAIL_CLOSED", "missing_stake", {}
    if stake_min is not None and stake < stake_min:
        return "DENY", "insufficient_stake", {}
    if history is None:
        return "FAIL_CLOSED", "missing_history", {}
    if history_max is not None and history > history_max:
        return "DENY", "history_divergence_high", {}

    # Cost calculation
    cost_R = lambda_r * base_cost * (1.0 - reputation)
    cost_S = lambda_s * base_cost * max(0.0, (stake_min - stake) if stake_min is not None else 0.0)
    cost_H = lambda_h * base_cost * history
    total_cost = cost_R + cost_S + cost_H
    cost_detail = {
        "cost_R": cost_R,
        "cost_S": cost_S,
        "cost_H": cost_H,
        "total_cost": total_cost,
        "budget": entity_cost_budget,
    }
    if entity_cost_budget is not None and total_cost > entity_cost_budget:
        return "DENY", "budget_exceeded", cost_detail

    return "ALLOW", "ecat_admissible", cost_detail


def load_candidate(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Validate ECAT candidates")
    parser.add_argument("--vectors", required=True, help="Path to directory containing ECAT candidate JSON files")
    parser.add_argument("--report", default=None, help="Path to write JSON report")
    parser.add_argument("--summary", default=None, help="Path to write markdown summary")
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
        outcome, reason, cost = validate_ecat_candidate(candidate)
        cid = candidate.get("candidate_id", fname)
        results.append({
            "candidate_id": cid,
            "outcome": outcome,
            "reason": reason,
            "cost": cost
        })
        counts[outcome] += 1

    report = {
        "schema": "stegverse.sandbox.ecat.validation_report.v1",
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

    # Write markdown summary
    if args.summary:
        with open(args.summary, 'w') as f:
            f.write("# ECAT Validation Summary\n\n")
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


if __name__ == "__main__":
    main()