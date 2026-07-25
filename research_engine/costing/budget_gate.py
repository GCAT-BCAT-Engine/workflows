#!/usr/bin/env python3
"""Fail-closed stage authorization and cumulative-spend gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any

CENT = Decimal("0.01")


def money(value: Any) -> Decimal:
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def evaluate(budget: dict[str, Any], stage_id: str, requested: Decimal) -> dict[str, Any]:
    hard_limit = money(budget["hard_limit"])
    spent = money(budget["spent"])
    reserved = money(budget["reserved"])
    stop = budget["automatic_stop"]
    threshold = money(stop["threshold"])

    stage = next((s for s in budget["stage_authorizations"] if s["stage_id"] == stage_id), None)
    reasons: list[str] = []

    if stop.get("triggered"):
        reasons.append("Automatic stop was already triggered.")
    if stage is None:
        reasons.append("Requested stage is not present in the budget record.")
    elif stage.get("status") != "authorized":
        reasons.append("Requested stage is not in authorized status.")
    elif requested > money(stage["authorized_amount"]):
        reasons.append("Requested amount exceeds the stage authorization.")

    projected = spent + requested
    if projected > hard_limit:
        reasons.append("Projected cumulative spend exceeds the hard budget limit.")
    if stop.get("enabled") and projected > threshold:
        reasons.append("Projected cumulative spend exceeds the automatic-stop threshold.")
    if reserved > hard_limit:
        reasons.append("Reserved amount exceeds the hard budget limit.")

    decision = "ALLOW" if not reasons else "FAIL_CLOSED"
    receipt = {
        "schema": "stegverse.research_budget_gate.v1",
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "budget_id": budget["budget_id"],
        "research_id": budget["research_id"],
        "stage_id": stage_id,
        "currency": "USD",
        "requested_amount": float(requested),
        "spent_before": float(spent),
        "projected_spend": float(projected),
        "hard_limit": float(hard_limit),
        "automatic_stop_threshold": float(threshold),
        "decision": decision,
        "reasons": reasons or ["Stage authorization and cumulative-spend boundaries passed."],
        "execution_authority_effect": "stage_only" if decision == "ALLOW" else "none",
    }
    receipt["receipt_hash"] = sha256(receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget", required=True, type=Path)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--requested-usd", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    budget = json.loads(args.budget.read_text(encoding="utf-8"))
    receipt = evaluate(budget, args.stage, money(args.requested_usd))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["decision"] == "ALLOW" else 2


if __name__ == "__main__":
    raise SystemExit(main())
