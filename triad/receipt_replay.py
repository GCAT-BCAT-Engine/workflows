"""
triad/receipt_replay.py
-----------------------

This script replays Triad sandbox receipts and verifies that the original
outcomes and reasons still hold.  It also validates the receipt chain by
recomputing each receipt hash and ensuring the ``prev_receipt_hash`` links
are consistent.  Any discrepancy between the stored outcome/reason and the
replayed outcome/reason will be flagged as a mismatch.

Usage example:

```
python triad/receipt_replay.py \
  --receipts triad/brain_reports/triad_receipts.jsonl \
  --vectors triad/candidate_vectors \
  --report triad/brain_reports/triad_replay_report.json \
  --summary triad/brain_reports/triad_replay_summary.md
```
"""

import json
import argparse
import hashlib
import os
from typing import List, Dict, Tuple

from triad_validator import validate_triad_candidate, load_candidate as load_triad


def compute_hash(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def verify_chain(receipts: List[Dict[str, any]]) -> bool:
    """Recompute receipt hashes and verify the chain."""
    prev_hash = None
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


def replay_receipts(receipts_path: str, vectors_dir: str) -> Tuple[List[Dict[str, any]], bool, List[Dict[str, any]]]:
    """
    Replay Triad receipts by re-running the validator on the original candidates.

    Returns (replay_results, chain_valid, mismatches).
    """
    receipts: List[Dict[str, any]] = []
    with open(receipts_path, 'r') as f:
        for line in f:
            if line.strip():
                receipts.append(json.loads(line))
    chain_valid = verify_chain(receipts)
    # Build lookup: candidate_id -> file path
    candidate_paths: Dict[str, str] = {}
    for fname in os.listdir(vectors_dir):
        if fname.lower().endswith('.json'):
            cid = json.load(open(os.path.join(vectors_dir, fname))).get('candidate_id', os.path.splitext(fname)[0])
            candidate_paths[cid] = os.path.join(vectors_dir, fname)
    replay_results: List[Dict[str, any]] = []
    mismatches: List[Dict[str, any]] = []
    for rec in receipts:
        cid = rec['candidate_id']
        original_outcome = rec['outcome']
        original_reason = rec['reason']
        path = candidate_paths.get(cid)
        if not path:
            replay_outcome, replay_reason = 'FAIL_CLOSED', 'candidate_missing'
        else:
            cand = load_triad(path)
            replay_outcome, replay_reason, _ = validate_triad_candidate(cand)
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


def save_report_and_summary(replay_results: List[Dict[str, any]], chain_valid: bool, mismatches: List[Dict[str, any]], report_path: str, summary_path: str) -> None:
    total = len(replay_results)
    mismatches_count = len(mismatches)
    report = {
        'schema': 'stegverse.sandbox.triad.replay_report.v1',
        'total': total,
        'matches': total - mismatches_count,
        'mismatches': mismatches_count,
        'chain_valid': chain_valid,
        'mismatch_details': mismatches,
        'replay': replay_results
    }
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    # Markdown summary
    with open(summary_path, 'w') as f:
        f.write('# Triad Replay Summary\n\n')
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
            match = '✅' if item['match'] else '❌'
            f.write(f'| {cid} | {oo} | {ro} | {orr} | {rr} | {match} |\n')


def main():
    parser = argparse.ArgumentParser(description='Replay Triad receipts and verify outcomes.')
    parser.add_argument('--receipts', required=True, help='Path to receipts JSONL file')
    parser.add_argument('--vectors', required=True, help='Path to Triad candidate directory')
    parser.add_argument('--report', required=True, help='Path to write replay report JSON')
    parser.add_argument('--summary', required=True, help='Path to write replay summary Markdown')
    args = parser.parse_args()
    results, chain_valid, mismatches = replay_receipts(args.receipts, args.vectors)
    save_report_and_summary(results, chain_valid, mismatches, args.report, args.summary)
    print(f'Replay finished: {len(results)} receipts replayed, {len(mismatches)} mismatches, chain valid: {chain_valid}')


if __name__ == '__main__':
    main()