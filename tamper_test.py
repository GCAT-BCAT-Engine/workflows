"""
ECAT/ICAT tamper detection test.

This utility demonstrates how tampering with the receipt chain for ECAT and ICAT
candidates will be detected by the replay verifier.  It loads the receipts
produced by the sandbox adapter, writes a tampered copy of those receipts
with the outcome of the first receipt flipped, then runs the replay script
against the tampered receipts.  The summary of the replay is printed to
stdout so it can be reviewed by CI workflows or invoked manually.

Usage (from repository root)::

    python -m ecat_icat.tamper_test \
      --original_receipts ecat_icat/brain_reports/ecat_icat_receipts.jsonl \
      --tampered_receipts ecat_icat/brain_reports/ecat_icat_receipts_tampered.jsonl \
      --vectors_ecat ecat_icat/candidate_vectors/ecat \
      --vectors_icat ecat_icat/candidate_vectors/icat \
      --report ecat_icat/brain_reports/ecat_icat_tamper_replay_report.json \
      --summary ecat_icat/brain_reports/ecat_icat_tamper_replay_summary.md

The script exits with a non‑zero status code if the tampered replay does not
detect any mismatches.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def flip_outcome(outcome: str) -> str:
    """Flip an outcome from ALLOW to DENY/FAIL_CLOSED or vice versa.

    For simplicity, this function toggles between 'ALLOW' and 'DENY'.
    If the outcome is neither, it returns 'DENY'.
    """
    outcome_upper = outcome.upper()
    if outcome_upper == "ALLOW":
        return "DENY"
    # Fail closed and deny are both treated as non‑allow; return ALLOW to
    # maximise contrast and guarantee a mismatch.
    return "ALLOW"


def create_tampered_receipts(original_receipts: Path, tampered_receipts: Path) -> None:
    """Read receipts JSONL from original_receipts and write a tampered copy.

    The tampered copy will have the outcome (and reason) of the first
    receipt flipped to ensure replay mismatch.
    """
    with original_receipts.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        raise ValueError("No receipts found in original file")

    first_receipt = json.loads(lines[0])
    # Flip outcome
    orig_outcome = first_receipt.get("outcome", "DENY")
    flipped_outcome = flip_outcome(orig_outcome)
    first_receipt["outcome"] = flipped_outcome
    # Update reason to reflect tampering
    first_receipt["reason"] = "tampered"
    lines[0] = json.dumps(first_receipt) + "\n"

    # Write tampered receipts file
    with tampered_receipts.open("w", encoding="utf-8") as f:
        f.writelines(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="ECAT/ICAT tamper detection test")
    parser.add_argument("--original_receipts", type=Path, required=True,
                        help="Path to the original receipts JSONL file")
    parser.add_argument("--tampered_receipts", type=Path, required=True,
                        help="Path where the tampered receipts JSONL will be written")
    parser.add_argument("--vectors_ecat", type=Path, required=True,
                        help="Path to ECAT candidate vectors directory")
    parser.add_argument("--vectors_icat", type=Path, required=True,
                        help="Path to ICAT candidate vectors directory")
    parser.add_argument("--report", type=Path, required=True,
                        help="Path to write the tamper replay report JSON")
    parser.add_argument("--summary", type=Path, required=True,
                        help="Path to write the tamper replay summary markdown")
    args = parser.parse_args(argv)

    # Copy original receipts to tampered and modify
    create_tampered_receipts(args.original_receipts, args.tampered_receipts)

    # Run the replay script on the tampered receipts
    try:
        subprocess.run([
            sys.executable,
            "-m",
            "ecat_icat.receipt_replay",
            "--receipts",
            str(args.tampered_receipts),
            "--vectors_ecat",
            str(args.vectors_ecat),
            "--vectors_icat",
            str(args.vectors_icat),
            "--report",
            str(args.report),
            "--summary",
            str(args.summary),
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running receipt replay: {e}")
        return 1

    # Load the replay report to determine whether mismatches were detected
    try:
        with args.report.open("r", encoding="utf-8") as f:
            replay_report = json.load(f)
    except Exception as exc:
        print(f"Failed to read replay report: {exc}")
        return 1

    # The replay report stores the number of mismatches as an integer under
    # the key "mismatches".  Interpret a positive count as detection of
    # tampering.
    mismatches_count = replay_report.get("mismatches", 0)
    if mismatches_count:
        print(f"Tamper detection passed: {mismatches_count} mismatches detected.")
        return 0
    else:
        print("Tamper detection failed: no mismatches detected in tampered receipts.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))