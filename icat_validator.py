import json
import os
import argparse


def validate_icat_candidate(candidate: dict):
    """
    Validate an ICAT candidate according to simple integrity admissibility rules.

    A candidate must contain:
      - candidate_id: unique identifier
      - integrity: dict with keys:
          proof_sufficient (bool or null),
          attestation_witnesses (int or null),
          conservation (bool or null),
          inverse (bool or null)
      - params: dict with keys:
          proof_required (bool),
          witness_quorum (int),
          conservation_required (bool),
          inverse_required (bool),
          lambda_p, lambda_a, lambda_k, lambda_x, base_cost
      - budget: dict with key 'integrity_cost' specifying cost limit

    Validation logic:
      Hard gates:
        * If proof_required and proof_sufficient is None -> FAIL_CLOSED
        * If proof_required and proof_sufficient is False -> DENY
        * If attestation_witnesses is None -> FAIL_CLOSED
        * If witness_quorum > attestation_witnesses -> DENY
        * If conservation_required and conservation is None -> FAIL_CLOSED
        * If conservation_required and conservation is False -> DENY
        * If inverse_required and inverse is None -> FAIL_CLOSED
        * If inverse_required and inverse is False -> DENY
      Cost calculation:
        * cost_P = lambda_p * base_cost
        * cost_A = lambda_a * base_cost * attestation_witnesses
        * cost_K = lambda_k * base_cost
        * cost_X = lambda_x * base_cost
        * total_cost = cost_P + cost_A + cost_K + cost_X
        * If total_cost > integrity_cost budget -> DENY
        * Else -> ALLOW
    Returns (outcome, reason, cost_dict).
    """
    cid = candidate.get("candidate_id", "unknown")
    integrity = candidate.get("integrity", {})
    params = candidate.get("params", {})
    budget = candidate.get("budget", {})

    proof_sufficient = integrity.get("proof_sufficient")
    witnesses = integrity.get("attestation_witnesses")
    conservation = integrity.get("conservation")
    inverse = integrity.get("inverse")

    proof_required = params.get("proof_required", True)
    witness_quorum = params.get("witness_quorum", 0)
    conservation_required = params.get("conservation_required", True)
    inverse_required = params.get("inverse_required", True)
    lambda_p = params.get("lambda_p", 1.0)
    lambda_a = params.get("lambda_a", 1.0)
    lambda_k = params.get("lambda_k", 1.0)
    lambda_x = params.get("lambda_x", 1.0)
    base_cost = params.get("base_cost", 1.0)
    integrity_budget = budget.get("integrity_cost", None)

    # Hard gates
    if proof_required:
        if proof_sufficient is None:
            return "FAIL_CLOSED", "proof_unavailable", {}
        if proof_sufficient is False:
            return "DENY", "proof_invalid", {}
    if witnesses is None:
        return "FAIL_CLOSED", "attestation_unavailable", {}
    if witness_quorum > witnesses:
        return "DENY", "attestation_quorum_failed", {}
    if conservation_required:
        if conservation is None:
            return "FAIL_CLOSED", "conservation_unavailable", {}
        if conservation is False:
            return "DENY", "conservation_failed", {}
    if inverse_required:
        if inverse is None:
            return "FAIL_CLOSED", "inverse_unavailable", {}
        if inverse is False:
            return "DENY", "inverse_failed", {}

    # Cost calculation
    cost_P = lambda_p * base_cost
    cost_A = lambda_a * base_cost * (witnesses if witnesses is not None else 0)
    cost_K = lambda_k * base_cost
    cost_X = lambda_x * base_cost
    total_cost = cost_P + cost_A + cost_K + cost_X
    cost_detail = {
        "cost_P": cost_P,
        "cost_A": cost_A,
        "cost_K": cost_K,
        "cost_X": cost_X,
        "total_cost": total_cost,
        "budget": integrity_budget
    }
    if integrity_budget is not None and total_cost > integrity_budget:
        return "DENY", "budget_exceeded", cost_detail

    return "ALLOW", "icat_admissible", cost_detail


def load_candidate(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Validate ICAT candidates")
    parser.add_argument("--vectors", required=True, help="Path to directory containing ICAT candidate JSON files")
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
        outcome, reason, cost = validate_icat_candidate(candidate)
        cid = candidate.get("candidate_id", fname)
        results.append({
            "candidate_id": cid,
            "outcome": outcome,
            "reason": reason,
            "cost": cost
        })
        counts[outcome] += 1

    report = {
        "schema": "stegverse.sandbox.icat.validation_report.v1",
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
            f.write("# ICAT Validation Summary\n\n")
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