"""
receipt_replay.py
-------------------

This module replays ECAT and ICAT sandbox receipts and verifies that the
original outcomes and reasons still hold.  It also validates the
receipt chain by recomputing each receipt hash and ensuring the
prev_receipt_hash links are consistent.  Any discrepancy between the
stored outcome/reason and the replayed outcome/reason will be flagged
as a mismatch.

Usage:

```
python -m ecat_icat.receipt_replay \
  --receipts ecat_icat/brain_reports/ecat_icat_receipts.jsonl \
  --report   ecat_icat/brain_reports/ecat_icat_replay_report.json \
  --summary  ecat_icat/brain_reports/ecat_icat_replay_summary.md
```

The script produces a JSON report summarising the replay results and
a Markdown summary table for quick inspection.  Both the chain
validity and per-receipt matches are reported.
"""

import json
import argparse
import hashlib
from typing import List, Dict

from ecat_icat.ecat_validator import validate_ecat_candidate, load_candidate as load_ecat
from ecat_icat.icat_validator import validate_icat_candidate, load_candidate as load_icat


def compute_hash(data: str) -> str:
    """Return SHA256 hex digest of the provided string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def verify_chain(receipts: List[Dict]) -> bool:
    """
    Verify the receipt chain by recomputing each receipt_hash and
    comparing with stored values.  Returns True if chain is valid,
    False otherwise.
    """
    prev_hash = None
    for receipt in receipts:
        cid = receipt['candidate_id']
        outcome = receipt['outcome']
        reason = receipt['reason']
        basis_hash = receipt['basis_hash']
        expected_prev = receipt['prev_receipt_hash']
        # Recompute receipt hash
        recomputed = compute_hash(cid + outcome + reason + basis_hash + (prev_hash or ''))
        if recomputed != receipt['receipt_hash'] or expected_prev != prev_hash:
            return False
        prev_hash = receipt['receipt_hash']
    return True


def replay_receipts(receipts_path: str, vectors_ecat: str, vectors_icat: str):
    """
    Replay receipts by re-running the appropriate validator for each
    candidate.  Returns a tuple (results, chain_valid) where results
    is a list of dictionaries summarising each replay and chain_valid
    indicates whether the chain hashes are consistent.
    """
    # Load receipts
    receipts = []
    with open(receipts_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            receipts.append(json.loads(line))

    chain_valid = verify_chain(receipts)

    # Build a lookup for candidate file paths (by candidate_id)
    # to support replaying without hardcoding file names.
    candidate_paths = {}
    import os
    # ECAT candidates
    for fname in os.listdir(vectors_ecat):
        if fname.lower().endswith('.json'):
            cid = os.path.splitext(fname)[0]
            candidate_paths[cid] = os.path.join(vectors_ecat, fname)
    # ICAT candidates
    for fname in os.listdir(vectors_icat):
        if fname.lower().endswith('.json'):
            cid = os.path.splitext(fname)[0]
            candidate_paths[cid] = os.path.join(vectors_icat, fname)

    replay_results = []
    mismatches = []

    for rec in receipts:
        cid = rec['candidate_id']
        layer = rec['layer']
        original_outcome = rec['outcome']
        original_reason = rec['reason']
        # Load candidate data
        path = candidate_paths.get(cid)
        if not path:
            # Missing candidate implies fail closed
            replay_outcome, replay_reason = 'FAIL_CLOSED', 'candidate_missing'
        else:
            if layer == 'ECAT':
                cand = load_ecat(path)
                replay_outcome, replay_reason, _ = validate_ecat_candidate(cand)
            else:
                cand = load_icat(path)
                replay_outcome, replay_reason, _ = validate_icat_candidate(cand)
        match = (replay_outcome == original_outcome) and (replay_reason == original_reason)
        if not match:
            mismatches.append({
                'candidate_id': cid,
                'layer': layer,
                'original_outcome': original_outcome,
                'replay_outcome': replay_outcome,
                'original_reason': original_reason,
                'replay_reason': replay_reason
            })
        replay_results.append({
            'candidate_id': cid,
            'layer': layer,
            'original_outcome': original_outcome,
            'replay_outcome': replay_outcome,
            'original_reason': original_reason,
            'replay_reason': replay_reason,
            'match': match
        })
    return replay_results, chain_valid, mismatches


def save_report_and_summary(replay_results: List[Dict], chain_valid: bool, mismatches: List[Dict], report_path: str, summary_path: str):
    """
    Save the replay report as JSON and a markdown summary.
    """
    total = len(replay_results)
    mismatches_count = len(mismatches)
    report = {
        'schema': 'stegverse.sandbox.ecat_icat.replay_report.v1',
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
        f.write('# ECAT/ICAT Replay Summary\n\n')
        f.write(f'- Receipts replayed: **{total}**\n')
        f.write(f'- Chain valid: **{chain_valid}**\n')
        f.write(f'- Mismatches found: **{mismatches_count}**\n\n')
        f.write('| ID | Layer | Original Outcome | Replay Outcome | Original Reason | Replay Reason | Match? |\n')
        f.write('|---|---|---|---|---|---|---|\n')
        for item in replay_results:
            cid = item['candidate_id']
            layer = item['layer']
            oo = item['original_outcome']
            ro = item['replay_outcome']
            orr = item['original_reason']
            rr = item['replay_reason']
            match = '✅' if item['match'] else '❌'
            f.write(f'| {cid} | {layer} | {oo} | {ro} | {orr} | {rr} | {match} |\n')


def main():
    parser = argparse.ArgumentParser(description='Replay ECAT/ICAT receipts and verify outcomes.')
    parser.add_argument('--receipts', required=True, help='Path to receipts JSONL file')
    parser.add_argument('--vectors_ecat', required=True, help='Path to ECAT candidate directory')
    parser.add_argument('--vectors_icat', required=True, help='Path to ICAT candidate directory')
    parser.add_argument('--report', required=True, help='Path to write replay report JSON')
    parser.add_argument('--summary', required=True, help='Path to write replay summary Markdown')
    args = parser.parse_args()

    results, chain_valid, mismatches = replay_receipts(args.receipts, args.vectors_ecat, args.vectors_icat)
    save_report_and_summary(results, chain_valid, mismatches, args.report, args.summary)
    print(f'Replay finished: {len(results)} receipts replayed, {len(mismatches)} mismatches, chain valid: {chain_valid}')


if __name__ == '__main__':
    main()