#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from gcat_bcat_candidate_validator import validate_file, build_cost_summary

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)

def stable_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def load_vector(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"id": path.stem, "name": path.stem, "malformed": True, "raw_hash": hashlib.sha256(path.read_bytes()).hexdigest()}

def receipt_basis(vector: Dict[str, Any]) -> Dict[str, Any]:
    return {"state": vector.get("state"), "params": vector.get("params"), "cost": vector.get("cost"), "expected": vector.get("expected")}

def build_receipt(vector_path: Path, result: Dict[str, Any], vector: Dict[str, Any], prev_hash: str) -> Dict[str, Any]:
    basis = receipt_basis(vector)
    payload = {
        "schema": "stegverse.sandbox.gcat_bcat.receipt.v2",
        "receipt_kind": "gcat_bcat_candidate_validation",
        "candidate_id": result.get("id"),
        "candidate_file": str(vector_path),
        "candidate_hash": stable_hash(vector),
        "basis": basis,
        "basis_hash": stable_hash(basis),
        "decision": {"outcome": result.get("actual"), "reason": result.get("reason_actual"), "passed": result.get("passed"), "errors": result.get("errors", [])},
        "metrics": result.get("metrics", {}),
        "validator": {"name": "gcat_bcat_candidate_validator.py", "version": "0.5.0-tamper"},
        "prev_receipt_hash": prev_hash,
        "emitted_at": datetime.now(timezone.utc).isoformat(),
    }
    payload["receipt_hash"] = stable_hash(payload)
    return payload

def verify_chain(receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
    expected_prev = "GENESIS"
    failures = []
    for index, receipt in enumerate(receipts):
        if receipt.get("prev_receipt_hash") != expected_prev:
            failures.append({"index": index, "candidate_id": receipt.get("candidate_id"), "expected_prev": expected_prev, "actual_prev": receipt.get("prev_receipt_hash")})
        receipt_copy = dict(receipt)
        stored_hash = receipt_copy.pop("receipt_hash", None)
        recomputed_hash = stable_hash(receipt_copy)
        if stored_hash != recomputed_hash:
            failures.append({"index": index, "candidate_id": receipt.get("candidate_id"), "reason": "receipt_hash_mismatch", "stored_hash": stored_hash, "recomputed_hash": recomputed_hash})
        if stable_hash(receipt.get("basis", {})) != receipt.get("basis_hash"):
            failures.append({"index": index, "candidate_id": receipt.get("candidate_id"), "reason": "basis_hash_mismatch"})
        expected_prev = receipt.get("receipt_hash")
    return {"schema": "stegverse.sandbox.receipt_chain_verification.v2", "receipt_count": len(receipts), "chain_valid": len(failures) == 0, "failures": failures, "head_receipt_hash": receipts[-1]["receipt_hash"] if receipts else None}

def build_summary(report: Dict[str, Any], chain_report: Dict[str, Any]) -> str:
    summary = report["summary"]
    cost = report["cost_summary"]
    outcome_counts = Counter(r["actual"] for r in report["results"])
    lines = [
        "# GCAT/BCAT Sandbox Summary", "",
        "## Sandbox Status", "",
        f"- Receipts emitted: **{chain_report['receipt_count']}**",
        f"- Receipt chain valid: **{chain_report['chain_valid']}**",
        f"- Head receipt hash: `{chain_report.get('head_receipt_hash')}`", "",
        "## Validation Results", "",
        f"- Total: **{summary['total']}**",
        f"- Passed: **{summary['passed']}**",
        f"- Failed: **{summary['failed']}**", "",
        "## Outcome Counts", "",
        f"- ALLOW: **{outcome_counts.get('ALLOW', 0)}**",
        f"- DENY: **{outcome_counts.get('DENY', 0)}**",
        f"- FAIL_CLOSED: **{outcome_counts.get('FAIL_CLOSED', 0)}**", "",
        "## Governance Cost Summary", "",
        f"- GCAT cost: **{cost['gcat_cost']:.6f}**",
        f"- BCAT cost: **{cost['bcat_cost']:.6f}**",
        f"- Total governance cost: **{cost['total_cost']:.6f}**",
        f"- Candidate budget: **{cost['budget']:.6f}**",
        f"- Budget margin: **{cost['budget_margin']:.6f}**", "",
    ]
    return "\n".join(lines)

def run_sandbox(vectors: Path, out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    receipts = []
    prev_hash = "GENESIS"
    for path in sorted(vectors.glob("*.json")):
        result = validate_file(path)
        vector = load_vector(path)
        receipt = build_receipt(path, result, vector, prev_hash)
        prev_hash = receipt["receipt_hash"]
        results.append(result)
        receipts.append(receipt)
    chain_report = verify_chain(receipts)
    report = {"schema": "stegverse.sandbox.gcat_bcat.report.v2", "summary": {"total": len(results), "passed": sum(1 for r in results if r["passed"]), "failed": sum(1 for r in results if not r["passed"])}, "cost_summary": build_cost_summary(results), "chain": chain_report, "results": results, "receipts": receipts}
    (out_dir / "gcat_bcat_sandbox_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (out_dir / "gcat_bcat_sandbox_receipts.jsonl").open("w", encoding="utf-8") as f:
        for receipt in receipts:
            f.write(canonical_json(receipt) + "\n")
    (out_dir / "gcat_bcat_sandbox_chain_report.json").write_text(json.dumps(chain_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "gcat_bcat_sandbox_summary.md").write_text(build_summary(report, chain_report), encoding="utf-8")
    return report

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vectors", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    report = run_sandbox(Path(args.vectors), Path(args.out_dir))
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    if not report["chain"]["chain_valid"]:
        return 1
    return 0 if report["summary"]["failed"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
