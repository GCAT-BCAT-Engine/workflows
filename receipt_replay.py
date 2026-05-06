"""
inference_window/receipt_replay.py
---------------------------------

Replay inference window receipts and verify their integrity.  This
script re-evaluates each candidate referenced by a receipt using
``validate_iw_candidate`` from ``iw_validator.py`` and checks that the
stored outcome and reason still hold.  It also validates the receipt
chain by recomputing each ``receipt_hash`` and ensuring the
``prev_receipt_hash`` links are consistent.  Any discrepancy between
the stored outcome/reason and the replayed outcome/reason is flagged
as a mismatch.  A report summarising the replay and a Markdown
summary are generated.

Usage::

    python -m inference_window.receipt_replay \
      --receipts inference_window/brain_reports/iw_receipts.jsonl \
      --vectors  inference_window/candidate_vectors \
      --report   inference_window/brain_reports/iw_replay_report.json \
      --summary  inference_window/brain_reports/iw_replay_summary.md

The JSON report includes the number of matches/mismatches and
details for any mismatched receipts.  The Markdown summary provides
a table for quick visual inspection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from typing import List, Dict

from inference_window.iw_validator import validate_iw_candidate, load_candidate as load_iw


def compute_hash(data: str) -> str:
    """Return SHA256 hex digest of the provided string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def verify_chain(receipts: List[Dict]) -> bool:
    """
    Verify the receipt chain by recomputing each ``receipt_hash`` and
    comparing with stored values.  Returns True if the chain is valid.
    """
    prev_hash: str | None = None
    for rec in receipts:
        cid = rec['candidate_id']
        outcome = rec['outcome']
        reason = rec['reason']
        basis_hash = rec['basis_hash']
        expected_prev = rec['prev_receipt_hash']
        recomputed = compute_hash(cid + outcome + reason + basis_hash + (prev_hash or ''))
        if recomputed != rec['receipt_hash'] or expected_prev != prev_hash:
            return False
        prev_hash = rec['receipt_hash']
    return True


def replay_receipts(receipts_path: str, vectors_dir: str):
    """
    Replay receipts by re-running the IW validator for each candidate.
    Returns a tuple (results, chain_valid, mismatches).
    """
    # Load receipts
    receipts: List[Dict] = []
    with open(receipts_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            receipts.append(json.loads(line))
    chain_valid = verify_chain(receipts)
    # Build a lookup for candidate paths
    candidate_paths: Dict[str, str] = {}
    for fname in os.listdir(vectors_dir):
        if fname.lower().endswith('.json'):
            cid = os.path.splitext(fname)[0]
            candidate_paths[cid] = os.path.join(vectors_dir, fname)
    replay_results: List[Dict] = []
    mismatches: List[Dict] = []
    for rec in receipts:
        cid = rec['candidate_id']
        original_outcome = rec['outcome']
        original_reason = rec['reason']
        # Load candidate
        path = candidate_paths.get(cid)
        if not path:
            replay_outcome, replay_reason = 'FAIL_CLOSED', 'candidate_missing'
        else:
            cand = load_iw(path)
            replay_outcome, replay_reason, _ = validate_iw_candidate(cand)
        match = (replay_outcome == original_outcome) and (replay_reason == original_reason)
        if not match:
            mismatches.append({
                'candidate_id': cid,
                'original_outcome': original_outcome,
                'replay_outcome': replay_outcome,
                'original_reason': original_reason,
                'replay_reason': replay_reason
            })
        replay_results.append({
            'candidate_id': cid,
            'original_outcome': original_outcome,
            'replay_outcome': replay_outcome,
            'original_reason': original_reason,
            'replay_reason': replay_reason,
            'match': match
        })
    return replay_results, chain_valid, mismatches


def save_report_and_summary(replay_results: List[Dict], chain_valid: bool, mismatches: List[Dict], report_path: str, summary_path: str) -> None:
    """
    Save the replay results and mismatches to a JSON report and a
    Markdown summary table.  The report records the total number of
    receipts replayed, the number of matches/mismatches, chain
    validity, and details of mismatches.
    """
    total = len(replay_results)
    mismatches_count = len(mismatches)
    report = {
        'schema': 'stegverse.sandbox.iw.replay_report.v1',
        'total': total,
        'matches': total - mismatches_count,
        'mismatches': mismatches_count,
        'chain_valid': chain_valid,
        'mismatch_details': mismatches,
        'replay': replay_results
    }
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    # Markdown summary
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write('# Inference Window Replay Summary\n\n')
        f.write(f'- Receipts replayed: **{total}**\n')
        f.write(f'- Chain valid: **{chain_valid}**\n')
        f.write(f'- Mismatches found: **{mismatches_count}**\n\n')
        f.write('| ID | Original Outcome | Replay Outcome | Original Reason | Replay Reason | Match? |\n')
        f.write('|---|---|---|---|---|---|\n')
        for item in replay_results:
            cid = item['candidate_id']
            oo = item['original_outcome']
            ro = item['replay_outcome']
            orr = item['original_reason']
            rr = item['replay_reason']
            match_indicator = '✅' if item['match'] else '❌'
            f.write(f'| {cid} | {oo} | {ro} | {orr} | {rr} | {match_indicator} |\n')


def main() -> None:
    parser = argparse.ArgumentParser(description='Replay IW receipts and verify outcomes.')
    parser.add_argument('--receipts', required=True, help='Path to receipts JSONL file')
    parser.add_argument('--vectors', required=True, help='Path to IW candidate directory')
    parser.add_argument('--report', required=True, help='Path to write replay report JSON')
    parser.add_argument('--summary', required=True, help='Path to write replay summary Markdown')
    args = parser.parse_args()
    results, chain_valid, mismatches = replay_receipts(args.receipts, args.vectors)
    save_report_and_summary(results, chain_valid, mismatches, args.report, args.summary)
    print(f'Replay finished: {len(results)} receipts replayed, {len(mismatches)} mismatches, chain valid: {chain_valid}')


if __name__ == '__main__':
    main()