#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any, Dict, List

from gcat_bcat_candidate_validator import classify

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)

def stable_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    receipts = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                receipts.append(json.loads(line))
    return receipts

def verify_receipt_hash(receipt: Dict[str, Any]) -> bool:
    receipt_copy = dict(receipt)
    stored_hash = receipt_copy.pop("receipt_hash", None)
    return stored_hash == stable_hash(receipt_copy)

def build_replay_vector(receipt: Dict[str, Any]) -> Dict[str, Any]:
    basis = receipt.get("basis")
    if isinstance(basis, dict):
        return {"id": receipt.get("candidate_id"), "name": receipt.get("candidate_id"), "params": basis.get("params"), "state": basis.get("state"), "cost": basis.get("cost"), "expected": basis.get("expected")}
    return {"id": receipt.get("candidate_id"), "name": receipt.get("candidate_id"), "params": {}, "state": {}, "cost": {}, "expected": {}}

def replay_receipt(receipt: Dict[str, Any], expected_prev: str) -> Dict[str, Any]:
    hash_valid = verify_receipt_hash(receipt)
    prev_valid = receipt.get("prev_receipt_hash") == expected_prev
    basis_hash_valid = stable_hash(receipt.get("basis", {})) == receipt.get("basis_hash")
    replay_vector = build_replay_vector(receipt)
    replay_outcome, replay_reason, replay_metrics = classify(replay_vector)
    original_outcome = receipt.get("decision", {}).get("outcome")
    original_reason = receipt.get("decision", {}).get("reason")
    outcome_matches = replay_outcome == original_outcome
    reason_matches = replay_reason == original_reason
    return {"candidate_id": receipt.get("candidate_id"), "receipt_hash": receipt.get("receipt_hash"), "hash_valid": hash_valid, "prev_hash_valid": prev_valid, "basis_hash_valid": basis_hash_valid, "original_outcome": original_outcome, "replay_outcome": replay_outcome, "original_reason": original_reason, "replay_reason": replay_reason, "outcome_matches": outcome_matches, "reason_matches": reason_matches, "replay_passed": hash_valid and prev_valid and basis_hash_valid and outcome_matches and reason_matches, "replay_metrics": replay_metrics}

def build_summary(report: Dict[str, Any]) -> str:
    summary = report["summary"]
    lines = ["# GCAT/BCAT Adversarial Receipt Replay Summary", "", f"- Receipts replayed: **{summary['total']}**", f"- Replay passed: **{summary['passed']}**", f"- Replay failed: **{summary['failed']}**", f"- Chain valid: **{report['chain_valid']}**", "", "## Replay Results", "", "| ID | Original | Replay | Reason Match | Hash Valid | Basis Hash | Prev Valid | Passed |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in report["results"]:
        lines.append(f"| {r['candidate_id']} | {r['original_outcome']} | {r['replay_outcome']} | {'✅' if r['reason_matches'] else '❌'} | {'✅' if r['hash_valid'] else '❌'} | {'✅' if r['basis_hash_valid'] else '❌'} | {'✅' if r['prev_hash_valid'] else '❌'} | {'✅' if r['replay_passed'] else '❌'} |")
    lines.append("")
    return "\n".join(lines)

def run_replay(receipts_path: Path, out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    receipts = read_jsonl(receipts_path)
    expected_prev = "GENESIS"
    results = []
    for receipt in receipts:
        result = replay_receipt(receipt, expected_prev)
        results.append(result)
        expected_prev = receipt.get("receipt_hash")
    failed = [r for r in results if not r["replay_passed"]]
    report = {"schema": "stegverse.sandbox.gcat_bcat.adversarial_replay_report.v1", "summary": {"total": len(results), "passed": len(results) - len(failed), "failed": len(failed)}, "chain_valid": len(failed) == 0, "results": results}
    (out_dir / "gcat_bcat_replay_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "gcat_bcat_replay_summary.md").write_text(build_summary(report), encoding="utf-8")
    return report

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipts", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    report = run_replay(Path(args.receipts), Path(args.out_dir))
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    return 0 if report["summary"]["failed"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
