"""
Triad tamper detection test.

This utility demonstrates how tampering with the receipt chain for Triad
candidates will be detected by the replay verifier.  It loads the receipts
produced by the Triad sandbox adapter, writes a tampered copy of those
receipts with the outcome of the first receipt flipped, then runs the
replay script against the tampered receipts.  The summary of the replay
is printed to stdout so it can be reviewed by CI workflows or invoked
manually.

Usage (from repository root)::

    python triad/tamper_test.py \
      --original_receipts triad/brain_reports/triad_receipts.jsonl \
      --tampered_receipts triad/brain_reports/triad_receipts_tampered.jsonl \
      --vectors triad/candidate_vectors \
      --report triad/brain_reports/triad_tamper_replay_report.json \
      --summary triad/brain_reports/triad_tamper_replay_summary.md

The script exits with a non‑zero status code if the tampered replay does not
detect any mismatches.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def flip_outcome(outcome: str) -> str:
    """Flip between ALLOW and DENY to create a mismatch."""
    outcome_upper = outcome.upper()
    if outcome_upper == "ALLOW":
        return "DENY"
    return "ALLOW"


def create_tampered_receipts(original_receipts: Path, tampered_receipts: Path) -> None:
    """Read receipts JSONL and write a tampered copy.

    The tampered copy will have the outcome (and reason) of the first
    receipt flipped to ensure replay mismatch.
    """
    with original_receipts.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        raise ValueError("No receipts found in original file")
    first = json.loads(lines[0])
    orig_outcome = first.get("outcome", "DENY")
    first["outcome"] = flip_outcome(orig_outcome)
    first["reason"] = "tampered"
    lines[0] = json.dumps(first) + "\n"
    with tampered_receipts.open("w", encoding="utf-8") as f:
        f.writelines(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Triad tamper detection test")
    parser.add_argument("--original_receipts", type=Path, required=True,
                        help="Path to the original receipts JSONL file")
    parser.add_argument("--tampered_receipts", type=Path, required=True,
                        help="Path where the tampered receipts JSONL will be written")
    parser.add_argument("--vectors", type=Path, required=True,
                        help="Path to Triad candidate vectors directory")
    parser.add_argument("--report", type=Path, required=True,
                        help="Path to write the tamper replay report JSON")
    parser.add_argument("--summary", type=Path, required=True,
                        help="Path to write the tamper replay summary markdown")
    args = parser.parse_args(argv)
    # Create tampered receipts file
    create_tampered_receipts(args.original_receipts, args.tampered_receipts)
    # Run the Triad replay
    try:
        subprocess.run([
            sys.executable,
            "triad/receipt_replay.py",
            "--receipts",
            str(args.tampered_receipts),
            "--vectors",
            str(args.vectors),
            "--report",
            str(args.report),
            "--summary",
            str(args.summary)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Triad receipt replay: {e}")
        return 1
    # Analyse the replay report
    try:
        with args.report.open("r", encoding="utf-8") as f:
            report = json.load(f)
    except Exception as exc:
        print(f"Failed to read replay report: {exc}")
        return 1
    mismatches_count = report.get("mismatches", 0)
    if mismatches_count:
        print(f"Tamper detection passed: {mismatches_count} mismatches detected.")
        return 0
    else:
        print("Tamper detection failed: no mismatches detected in tampered receipts.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))