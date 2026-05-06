"""
PE tamper detection test.

This utility demonstrates tampering detection for Probability of Existence (PE)
sandbox receipts.  It loads the receipts emitted by ``pe_sandbox_adapter``,
writes a tampered copy with the outcome of the first receipt flipped, then
runs the replay verifier to confirm that the mismatch is detected.

Usage::

    python -m ecat_icat.pe_tamper_test \
      --original_receipts ecat_icat/brain_reports/pe_receipts.jsonl \
      --tampered_receipts ecat_icat/brain_reports/pe_receipts_tampered.jsonl \
      --vectors ecat_icat/candidate_vectors/pe \
      --report ecat_icat/brain_reports/pe_tamper_replay_report.json \
      --summary ecat_icat/brain_reports/pe_tamper_replay_summary.md

The script exits with a non-zero status code if the tampered replay
does not detect any mismatches, signalling a failure of the tamper
detection mechanism.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def flip_outcome(outcome: str) -> str:
    """Flip an outcome between ALLOW and DENY/FAIL_CLOSED.

    This helper toggles ``ALLOW`` to ``DENY`` and any non-allow
    outcome to ``ALLOW``, thereby guaranteeing a mismatch.
    """
    outcome_upper = outcome.upper()
    if outcome_upper == 'ALLOW':
        return 'DENY'
    # Treat any non-allow as DENY; flip to ALLOW for maximum contrast
    return 'ALLOW'


def create_tampered_receipts(original_receipts: Path, tampered_receipts: Path) -> None:
    """Read a receipts JSONL file and write a tampered copy.

    The first receipt has its outcome flipped and reason set to ``tampered``.
    """
    with original_receipts.open('r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines:
        raise ValueError('No receipts found in original file')
    first = json.loads(lines[0])
    orig_outcome = first.get('outcome', 'DENY')
    flipped = flip_outcome(orig_outcome)
    first['outcome'] = flipped
    first['reason'] = 'tampered'
    lines[0] = json.dumps(first) + '\n'
    with tampered_receipts.open('w', encoding='utf-8') as f:
        f.writelines(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description='PE tamper detection test')
    parser.add_argument('--original_receipts', type=Path, required=True, help='Path to original receipts JSONL')
    parser.add_argument('--tampered_receipts', type=Path, required=True, help='Path to write tampered receipts')
    parser.add_argument('--vectors', type=Path, required=True, help='Directory of PE candidate vectors')
    parser.add_argument('--report', type=Path, required=True, help='Path to write tamper replay report JSON')
    parser.add_argument('--summary', type=Path, required=True, help='Path to write tamper replay summary Markdown')
    args = parser.parse_args(argv)
    # Create tampered receipts file
    create_tampered_receipts(args.original_receipts, args.tampered_receipts)
    # Run replay script on tampered receipts
    try:
        subprocess.run([
            sys.executable,
            '-m',
            'ecat_icat.pe_receipt_replay',
            '--receipts', str(args.tampered_receipts),
            '--vectors', str(args.vectors),
            '--report', str(args.report),
            '--summary', str(args.summary),
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error running PE receipt replay: {e}')
        return 1
    # Read the replay report
    try:
        with args.report.open('r', encoding='utf-8') as f:
            replay_report = json.load(f)
    except Exception as exc:
        print(f'Failed to read replay report: {exc}')
        return 1
    # Determine mismatches
    mismatches_count = replay_report.get('mismatches', 0)
    if mismatches_count:
        print(f'Tamper detection passed: {mismatches_count} mismatches detected.')
        return 0
    else:
        print('Tamper detection failed: no mismatches detected in tampered receipts.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))