import json
import os
import argparse
import hashlib
from typing import Dict, List

from triad_validator import validate_triad_candidate, load_candidate as load_triad


def compute_hash(data: str) -> str:
    """Return SHA256 hex digest of the provided string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def load_candidates_from_dir(directory: str) -> List[Dict[str, any]]:
    """
    Load all JSON candidate files from a directory. Returns a list of candidate dicts.
    """
    candidates = []
    for fname in sorted(os.listdir(directory)):
        if not fname.lower().endswith('.json'):
            continue
        fpath = os.path.join(directory, fname)
        try:
            candidate = load_triad(fpath)
            candidates.append(candidate)
        except Exception:
            continue
    return candidates


def generate_receipts(directory: str) -> List[Dict[str, any]]:
    """
    Generate a list of receipts for all Triad candidates in the given directory.
    Receipts are chained via prev_receipt_hash.
    """
    receipts: List[Dict[str, any]] = []
    prev_hash = None
    candidates = load_candidates_from_dir(directory)
    for cand in candidates:
        cid = cand.get('candidate_id', 'unknown')
        outcome, reason, cost = validate_triad_candidate(cand)
        # Basis hash is hash of sorted JSON candidate
        basis_str = json.dumps(cand, sort_keys=True)
        basis_hash = compute_hash(basis_str)
        # Compute receipt hash
        receipt_str = cid + outcome + reason + basis_hash + (prev_hash or '')
        receipt_hash = compute_hash(receipt_str)
        receipt = {
            'candidate_id': cid,
            'layer': 'TRIAD',
            'outcome': outcome,
            'reason': reason,
            'basis_hash': basis_hash,
            'prev_receipt_hash': prev_hash,
            'receipt_hash': receipt_hash,
            'cost': cost
        }
        receipts.append(receipt)
        prev_hash = receipt_hash
    return receipts


def verify_chain(receipts: List[Dict[str, any]]) -> bool:
    """
    Verify the receipt chain by recomputing each receipt_hash and comparing with stored values.
    Returns True if chain is valid, False otherwise.
    """
    prev_hash = None
    for rec in receipts:
        cid = rec['candidate_id']
        outcome = rec['outcome']
        reason = rec['reason']
        basis_hash = rec['basis_hash']
        expected_prev = rec['prev_receipt_hash']
        # Recompute
        recomputed = compute_hash(cid + outcome + reason + basis_hash + (prev_hash or ''))
        if recomputed != rec['receipt_hash'] or expected_prev != prev_hash:
            return False
        prev_hash = rec['receipt_hash']
    return True


def save_receipts(receipts: List[Dict[str, any]], path: str) -> None:
    with open(path, 'w') as f:
        for rec in receipts:
            f.write(json.dumps(rec) + '\n')


def save_summary(receipts: List[Dict[str, any]], report_path: str, summary_path: str) -> None:
    total = len(receipts)
    counts = {'ALLOW': 0, 'DENY': 0, 'FAIL_CLOSED': 0}
    for rec in receipts:
        counts[rec['outcome']] += 1
    chain_valid = verify_chain(receipts)
    report = {
        'schema': 'stegverse.sandbox.triad.sandbox_report.v1',
        'total': total,
        'allow': counts['ALLOW'],
        'deny': counts['DENY'],
        'fail_closed': counts['FAIL_CLOSED'],
        'chain_valid': chain_valid,
        'receipts': receipts
    }
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    # Markdown summary
    with open(summary_path, 'w') as f:
        f.write('# Triad Sandbox Summary\n\n')
        f.write(f'- Receipts emitted: **{total}**\n')
        f.write(f'- Chain valid: **{chain_valid}**\n')
        f.write(f'- Allowed: **{counts["ALLOW"]}**\n')
        f.write(f'- Denied: **{counts["DENY"]}**\n')
        f.write(f'- Fail Closed: **{counts["FAIL_CLOSED"]}**\n\n')
        # Table
        f.write('| ID | Outcome | Reason | Aggregated Cost | Budget | Pass? |\n')
        f.write('|---|---|---|---|---|---|\n')
        for rec in receipts:
            cid = rec['candidate_id']
            outcome = rec['outcome']
            reason = rec['reason']
            cost_dict = rec.get('cost', {})
            agg_cost = cost_dict.get('aggregated_cost', '')
            budget = cost_dict.get('budget', '')
            pass_indicator = '✅' if outcome == 'ALLOW' else '❌'
            f.write(f'| {cid} | {outcome} | {reason} | {agg_cost} | {budget} | {pass_indicator} |\n')


def main():
    parser = argparse.ArgumentParser(description='Generate receipts and summary for Triad candidates.')
    parser.add_argument('--vectors', required=True, help='Path to Triad candidate directory')
    parser.add_argument('--receipts', required=True, help='Path to write receipts JSONL file')
    parser.add_argument('--report', required=True, help='Path to write summary report JSON')
    parser.add_argument('--summary', required=True, help='Path to write summary markdown')
    args = parser.parse_args()
    receipts = generate_receipts(args.vectors)
    save_receipts(receipts, args.receipts)
    save_summary(receipts, args.report, args.summary)
    print(f'Receipts generated: {len(receipts)}. Chain valid: {verify_chain(receipts)}')


if __name__ == '__main__':
    main()