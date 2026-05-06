"""
triad_validator.py
-------------------

This module implements validation logic for the "Triad" admissibility
transform.  The Triad combines five lower‑level governance layers:

* GCAT – a global invariant check: a ≤ K·g^α·c^β·t^γ
* BCAT – a normalization check: g + c + a + t = 1 and all non‑negative
* ECAT – an entity fitness check (imported from ``ecat_icat.ecat_validator``)
* ICAT – an integrity/proof check (imported from ``ecat_icat.icat_validator``)
* PE   – a probability‑of‑existence check (imported from ``ecat_icat.pe_validator``)

Each Triad candidate JSON must contain the following top‑level keys:

```
{
  "candidate_id": "TRIAD_001",
  "gcat": {"state": {...}, "params": {...}},
  "bcat": {"state": {...}},
  "ecat": {<ECAT candidate body>},
  "icat": {<ICAT candidate body>},
  "pe":   {<PE candidate body>}
}
```

The GCAT section must define ``state`` with keys ``g``, ``c``, ``a`` and ``t``
(all floats) and ``params`` with keys ``K``, ``alpha``, ``beta`` and
``gamma``.  The BCAT section must define ``state`` with the same keys.
The ECAT, ICAT and PE sections are passed directly to their
respective validators from the ``ecat_icat`` package.

Validation proceeds by running each layer in the order GCAT → BCAT →
ECAT → ICAT → PE.  A ``FAIL_CLOSED`` result takes precedence over
``DENY``; ``DENY`` takes precedence over ``ALLOW``.  If all layers
return ``ALLOW`` the Triad outcome is ``ALLOW``.

The Triad also reports whether a scalar constant exists across the
five layers.  In this context, the scalar constant is defined as the
shared base cost used by ECAT, ICAT and PE (the GCAT and BCAT layers
do not use base_cost directly but are assumed to conform if the other
three agree).  If the ``base_cost`` parameters supplied to ECAT,
ICAT and PE are all equal (within a small tolerance), the constant
exists and its value is reported.  Otherwise, the constant is
considered undefined.

The ``validate_triad_candidate`` function returns a tuple
``(outcome, reason, details)`` where ``details`` is a dictionary
containing per‑layer results, the aggregated total cost, budgets (if
any), and the discovered scalar constant (or ``None``).

When executed as a script this module will load all JSON files in a
specified directory, validate them, and emit a JSON report and an
optional Markdown summary similar to the other validation modules.

"""

from __future__ import annotations

import argparse
from typing import Any, Dict
import json
import os
from typing import Dict, Any, Tuple, Optional

# Import ECAT/ICAT/PE validators
from ecat_icat.ecat_validator import validate_ecat_candidate
from ecat_icat.icat_validator import validate_icat_candidate
from ecat_icat.pe_validator import validate_pe_candidate

# ---------------------------------------------------------------------------
# Helper function
#
# The Triad sandbox adapter expects a ``load_candidate`` function to load
# individual candidate JSON files.  Provide a simple implementation here
# rather than duplicating JSON loading logic in multiple modules.  See
# :func:`load_candidate` for details.

def load_candidate(path: str) -> Dict[str, Any]:
    """Load a Triad candidate from a JSON file.

    Parameters
    ----------
    path : str
        Path to the JSON file.

    Returns
    -------
    Dict[str, Any]
        Parsed JSON content as a dictionary.

    Raises
    ------
    Exception
        If the file cannot be read or parsed.
    """
    with open(path, 'r') as f:
        return json.load(f)


def validate_gcat_layer(section: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
    """Validate the GCAT portion of a Triad candidate.

    GCAT uses the invariant a ≤ K·g^α·c^β·t^γ.  If any state field is
    missing or non‑numeric the outcome is FAIL_CLOSED.  If any field is
    negative, or if the invariant is violated, the outcome is DENY.
    Otherwise the outcome is ALLOW.  No cost is currently computed for
    GCAT.
    """
    if section is None:
        return "FAIL_CLOSED", "gcat_section_missing", {}
    state = section.get("state", {}) or {}
    params = section.get("params", {}) or {}
    required_fields = ["g", "c", "a", "t"]
    # Check presence and numeric
    values = {}
    for key in required_fields:
        val = state.get(key)
        if val is None:
            return "FAIL_CLOSED", f"gcat_missing_{key}", {}
        if not isinstance(val, (int, float)):
            return "FAIL_CLOSED", f"gcat_invalid_{key}", {}
        values[key] = float(val)
        if values[key] < 0.0:
            return "DENY", f"gcat_negative_{key}", {}
    g = values["g"]
    c = values["c"]
    a = values["a"]
    t = values["t"]
    # Extract parameters
    K = params.get("K")
    alpha = params.get("alpha")
    beta = params.get("beta")
    gamma = params.get("gamma")
    # Require numeric parameters; missing yields FAIL_CLOSED
    for name, p in [("K", K), ("alpha", alpha), ("beta", beta), ("gamma", gamma)]:
        if p is None:
            return "FAIL_CLOSED", f"gcat_missing_{name}", {}
        if not isinstance(p, (int, float)):
            return "FAIL_CLOSED", f"gcat_invalid_{name}", {}
    K = float(K)
    alpha = float(alpha)
    beta = float(beta)
    gamma = float(gamma)
    try:
        # Compute invariant value
        invariant_value = a - K * (g ** alpha) * (c ** beta) * (t ** gamma)
    except Exception as e:
        return "FAIL_CLOSED", "gcat_computation_error", {}
    if invariant_value <= 0.0:
        return "ALLOW", "gcat_admissible", {"invariant": invariant_value}
    return "DENY", "gcat_invariant_violation", {"invariant": invariant_value}


def validate_bcat_layer(section: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
    """Validate the BCAT portion of a Triad candidate.

    BCAT ensures that g + c + a + t == 1 (within tolerance) and that
    all components are non‑negative.  Missing fields are considered
    FAIL_CLOSED.  If the sum deviates significantly from 1.0 (> 1e‑6)
    or any field is negative, the outcome is DENY.  No cost is
    computed.
    """
    if section is None:
        return "FAIL_CLOSED", "bcat_section_missing", {}
    state = section.get("state", {}) or {}
    required_fields = ["g", "c", "a", "t"]
    values = {}
    for key in required_fields:
        val = state.get(key)
        if val is None:
            return "FAIL_CLOSED", f"bcat_missing_{key}", {}
        if not isinstance(val, (int, float)):
            return "FAIL_CLOSED", f"bcat_invalid_{key}", {}
        values[key] = float(val)
        if values[key] < 0.0:
            return "DENY", f"bcat_negative_{key}", {}
    total = values["g"] + values["c"] + values["a"] + values["t"]
    if abs(total - 1.0) > 1e-6:
        return "DENY", "bcat_simplex_violation", {"sum": total}
    return "ALLOW", "bcat_admissible", {"sum": total}


def extract_base_costs(ecat_section: Dict[str, Any],
                       icat_section: Dict[str, Any],
                       pe_section: Dict[str, Any]) -> Tuple[bool, Optional[float]]:
    """Check whether ECAT, ICAT and PE share a common base_cost.

    Returns (exists, value).  ``exists`` is True if all three base
    costs are present and equal within a small tolerance; ``value``
    provides the common cost or None.
    """
    costs = []
    # ECAT base_cost
    if ecat_section is not None:
        params = ecat_section.get("params", {}) or {}
        bc = params.get("base_cost")
        if bc is not None:
            costs.append(float(bc))
    # ICAT base_cost
    if icat_section is not None:
        params = icat_section.get("params", {}) or {}
        bc = params.get("base_cost")
        if bc is not None:
            costs.append(float(bc))
    # PE base_cost
    if pe_section is not None:
        params = pe_section.get("params", {}) or {}
        bc = params.get("base_cost")
        if bc is not None:
            costs.append(float(bc))
    if len(costs) != 3:
        return False, None
    # Check all equal within tolerance
    first = costs[0]
    for c in costs[1:]:
        if abs(c - first) > 1e-6:
            return False, None
    return True, first


def validate_triad_candidate(candidate: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
    """Validate a Triad candidate.

    Returns (outcome, reason, details).  ``details`` contains per‑layer
    outcomes, reasons and costs; a scalar constant (if one exists);
    total cost across ECAT/ICAT/PE layers; and budgets.  Costs are
    aggregated only for ECAT, ICAT and PE, as GCAT and BCAT currently
    do not compute costs.
    """
    cid = candidate.get("candidate_id", "unknown")
    # Unpack sections
    # In early Triad candidate drafts the GCAT and BCAT inputs were combined
    # into a single ``gcat_bcat`` section.  Accept either separate
    # ``gcat``/``bcat`` keys or a single ``gcat_bcat`` key.  If
    # ``gcat_bcat`` is provided, use it for both GCAT and BCAT.
    gcat_section = candidate.get("gcat") or candidate.get("gcat_bcat")
    bcat_section = candidate.get("bcat") or candidate.get("gcat_bcat")
    ecat_section = candidate.get("ecat")
    icat_section = candidate.get("icat")
    pe_section = candidate.get("pe")
    # Validate each layer
    gcat_outcome, gcat_reason, gcat_cost = validate_gcat_layer(gcat_section)
    bcat_outcome, bcat_reason, bcat_cost = validate_bcat_layer(bcat_section)
    # ECAT/ICAT/PE may not run if earlier layer already fails closed
    ecat_outcome = ecat_reason = None
    ecat_cost = {}
    if gcat_outcome == "FAIL_CLOSED" or bcat_outcome == "FAIL_CLOSED":
        # propagate fail_closed to subsequent layers
        ecat_outcome = "FAIL_CLOSED"
        ecat_reason = "upstream_fail_closed"
    else:
        ecat_outcome, ecat_reason, ecat_cost = validate_ecat_candidate(ecat_section)
    icat_outcome = icat_reason = None
    icat_cost = {}
    if gcat_outcome == "FAIL_CLOSED" or bcat_outcome == "FAIL_CLOSED" or ecat_outcome == "FAIL_CLOSED":
        icat_outcome = "FAIL_CLOSED"
        icat_reason = "upstream_fail_closed"
    else:
        icat_outcome, icat_reason, icat_cost = validate_icat_candidate(icat_section)
    pe_outcome = pe_reason = None
    pe_cost = {}
    if (
        gcat_outcome == "FAIL_CLOSED" or bcat_outcome == "FAIL_CLOSED" or
        ecat_outcome == "FAIL_CLOSED" or icat_outcome == "FAIL_CLOSED"
    ):
        pe_outcome = "FAIL_CLOSED"
        pe_reason = "upstream_fail_closed"
    else:
        pe_outcome, pe_reason, pe_cost = validate_pe_candidate(pe_section)
    # Determine overall outcome
    layer_results = {
        "gcat": {"outcome": gcat_outcome, "reason": gcat_reason, "cost": gcat_cost},
        "bcat": {"outcome": bcat_outcome, "reason": bcat_reason, "cost": bcat_cost},
        "ecat": {"outcome": ecat_outcome, "reason": ecat_reason, "cost": ecat_cost},
        "icat": {"outcome": icat_outcome, "reason": icat_reason, "cost": icat_cost},
        "pe":   {"outcome": pe_outcome, "reason": pe_reason, "cost": pe_cost},
    }
    # Evaluate precedence: any FAIL_CLOSED → overall FAIL_CLOSED; else any DENY → DENY; else ALLOW
    if any(layer_results[layer]["outcome"] == "FAIL_CLOSED" for layer in layer_results):
        overall_outcome = "FAIL_CLOSED"
        # Use the first FAIL_CLOSED reason encountered in GCAT→PE order
        for name in ["gcat", "bcat", "ecat", "icat", "pe"]:
            if layer_results[name]["outcome"] == "FAIL_CLOSED":
                overall_reason = layer_results[name]["reason"]
                break
    elif any(layer_results[layer]["outcome"] == "DENY" for layer in layer_results):
        overall_outcome = "DENY"
        for name in ["gcat", "bcat", "ecat", "icat", "pe"]:
            if layer_results[name]["outcome"] == "DENY":
                overall_reason = layer_results[name]["reason"]
                break
    else:
        overall_outcome = "ALLOW"
        overall_reason = "triad_admissible"
    # Aggregate cost across ECAT/ICAT/PE
    total_cost = 0.0
    budgets = {}
    for layer, res in layer_results.items():
        cost = res.get("cost", {}) or {}
        if "total_cost" in cost:
            total_cost += cost["total_cost"]
        # collect budgets keyed by layer
        if "budget" in cost and cost["budget"] is not None:
            budgets[layer] = cost["budget"]
    # Determine scalar constant
    constant_exists, constant_value = extract_base_costs(ecat_section, icat_section, pe_section)
    # Build details
    details = {
        "layer_results": layer_results,
        "total_cost": total_cost,
        "budgets": budgets,
        "scalar_constant_exists": constant_exists,
        "scalar_constant": constant_value,
    }
    return overall_outcome, overall_reason, details


def main():
    parser = argparse.ArgumentParser(description="Validate Triad candidates")
    parser.add_argument("--vectors", required=True, help="Path to directory containing Triad candidate JSON files")
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
            with open(fpath, 'r') as f:
                candidate = json.load(f)
        except Exception as e:
            results.append({
                "candidate_id": fname,
                "outcome": "FAIL_CLOSED",
                "reason": "invalid_json",
                "error": str(e),
                "details": {}
            })
            counts["FAIL_CLOSED"] += 1
            continue
        outcome, reason, details = validate_triad_candidate(candidate)
        cid = candidate.get("candidate_id", fname)
        results.append({
            "candidate_id": cid,
            "outcome": outcome,
            "reason": reason,
            "details": details
        })
        counts[outcome] += 1
    report = {
        "schema": "stegverse.sandbox.triad.validation_report.v1",
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
            f.write("# Triad Validation Summary\n\n")
            f.write(f"- Total candidates: **{report['total']}**\n")
            f.write(f"- Allowed: **{report['allow']}**\n")
            f.write(f"- Denied: **{report['deny']}**\n")
            f.write(f"- Fail Closed: **{report['fail_closed']}**\n\n")
            f.write("| ID | Outcome | Reason | Total Cost | Scalar Constant Exists | Scalar Constant | Pass? |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            for res in results:
                cid = res['candidate_id']
                outcome = res['outcome']
                reason = res['reason']
                details = res['details'] or {}
                total_cost = details.get('total_cost', '')
                exists = details.get('scalar_constant_exists', False)
                const_val = details.get('scalar_constant', '')
                pass_indicator = '✅' if outcome == 'ALLOW' else '❌'
                f.write(f"| {cid} | {outcome} | {reason} | {total_cost} | {exists} | {const_val} | {pass_indicator} |\n")


if __name__ == '__main__':
    main()