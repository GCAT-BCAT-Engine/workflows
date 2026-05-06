import json
import os
import argparse
import hashlib
from ecat_icat.ecat_validator import validate_ecat_candidate, load_candidate as load_ecat
from ecat_icat.icat_validator import validate_icat_candidate, load_candidate as load_icat


def compute_hash(data: str) -> str:
    """Return SHA256 hex digest of the provided string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def load_candidates_from_dir(directory: str):
    """
    Load all JSON candidate files from a directory. Returns a list of (candidate_id, candidate_dict, layer).
    The layer is inferred from the file name prefix (ECAT or ICAT).
    """
    candidates = []
    for fname in sorted(os.listdir(directory)):
        if not fname.lower().endswith('.json'):
            continue
        fpath = os.path.join(directory, fname)
        try:
            candidate = load_ecat(fpath) if fname.startswith('ECAT') else load_icat(fpath)
        except Exception:
            continue
        cid = candidate.get('candidate_id', fname)
        layer = 'ECAT' if fname.startswith('ECAT') else 'ICAT'
        candidates.append((cid, candidate, layer))
    return candidates


def generate_receipts(ecat_dir: str, icat_dir: str):
    """
    Generate a list of receipts for all candidates in ECAT and ICAT directories.
    Receipts are chained via prev_receipt_hash.
    """
    receipts = []
    prev_hash = None
    # Load ECAT candidates first, then ICAT
    for directory in [ecat_dir, icat_dir]:
        candidates = load_candidates_from_dir(directory)
        for cid, cand, layer in candidates:
            # Validate candidate
            if layer == 'ECAT':
                outcome, reason, cost = validate_ecat_candidate(cand)
            else:
                outcome, reason, cost = validate_icat_candidate(cand)
            # Basis hash is hash of sorted JSON candidate
            basis_str = json.dumps(cand, sort_keys=True)
            basis_hash = compute_hash(basis_str)
            # Compute receipt hash
            receipt_str = cid + outcome + reason + basis_hash + (prev_hash or '')
            receipt_hash = compute_hash(receipt_str)
            receipt = {
                "candidate_id": cid,
                "layer": layer,
                "outcome": outcome,
                "reason": reason,
                "basis_hash": basis_hash,
                "prev_receipt_hash": prev_hash,
                "receipt_hash": receipt_hash,
                "cost": cost
            }
            receipts.append(receipt)
            prev_hash = receipt_hash
    return receipts


def verify_chain(receipts):
    """
    Verify the receipt chain by recomputing each receipt_hash and comparing with stored values.
    Returns True if chain is valid, False otherwise.
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


def save_receipts(receipts, path):
    with open(path, 'w') as f:
        for rec in receipts:
            f.write(json.dumps(rec) + '\n')


def save_summary(receipts, report_path, summary_path):
    total = len(receipts)
    counts = {'ALLOW': 0, 'DENY': 0, 'FAIL_CLOSED': 0}
    for rec in receipts:
        counts[rec['outcome']] += 1
    chain_valid = verify_chain(receipts)
    report = {
        'schema': 'stegverse.sandbox.ecat_icat.sandbox_report.v1',
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
        f.write('# ECAT/ICAT Sandbox Summary\n\n')
        f.write(f'- Receipts emitted: **{total}**\n')
        f.write(f'- Chain valid: **{chain_valid}**\n')
        f.write(f'- Allowed: **{counts["ALLOW"]}**\n')
        f.write(f'- Denied: **{counts["DENY"]}**\n')
        f.write(f'- Fail Closed: **{counts["FAIL_CLOSED"]}**\n\n')
        # Table
        f.write('| ID | Layer | Outcome | Reason | Total Cost | Budget | Pass? |\n')
        f.write('|---|---|---|---|---|---|---|\n')
        for rec in receipts:
            cid = rec['candidate_id']
            layer = rec['layer']
            outcome = rec['outcome']
            reason = rec['reason']
            cost_dict = rec.get('cost', {})
            total_cost = cost_dict.get('total_cost', '')
            budget = cost_dict.get('budget', '')
            pass_indicator = '✅' if outcome == 'ALLOW' else '❌'
            f.write(f'| {cid} | {layer} | {outcome} | {reason} | {total_cost} | {budget} | {pass_indicator} |\n')


def main():
    parser = argparse.ArgumentParser(description='Generate receipts and summary for ECAT and ICAT candidates.')
    parser.add_argument('--vectors_ecat', required=True, help='Path to ECAT candidate directory')
    parser.add_argument('--vectors_icat', required=True, help='Path to ICAT candidate directory')
    parser.add_argument('--receipts', required=True, help='Path to write receipts JSONL file')
    parser.add_argument('--report', required=True, help='Path to write summary report JSON')
    parser.add_argument('--summary', required=True, help='Path to write summary markdown')
    args = parser.parse_args()

    receipts = generate_receipts(args.vectors_ecat, args.vectors_icat)
    save_receipts(receipts, args.receipts)
    save_summary(receipts, args.report, args.summary)

    print(f'Receipts generated: {len(receipts)}. Chain valid: {verify_chain(receipts)}')


if __name__ == '__main__':
    main()