"""
pe_sandbox_adapter.py
-----------------------

This script generates sandbox receipts for Probability of Existence (PE) candidates.
It mirrors the functionality of the ECAT/ICAT sandbox adapter but operates
solely on PE candidate vectors.  Each candidate is validated using
``validate_pe_candidate`` from ``pe_validator.py``.  A receipt is produced
containing the candidate ID, outcome, reason, cost breakdown, and a
cryptographic chain linking each receipt via a ``prev_receipt_hash``.

Usage (from repository root)::

    python -m ecat_icat.pe_sandbox_adapter \
      --vectors ecat_icat/candidate_vectors/pe \
      --receipts ecat_icat/brain_reports/pe_receipts.jsonl \
      --report   ecat_icat/brain_reports/pe_sandbox_report.json \
      --summary  ecat_icat/brain_reports/pe_sandbox_summary.md

The script emits three files:

- A ``JSONL`` file with one receipt per line.
- A ``JSON`` report summarising counts of outcomes and chain validity.
- A Markdown summary table for quick review.

Receipts are chained by computing a SHA256 hash over the candidate ID,
outcome, reason, basis hash (hash of the sorted JSON candidate), and the
previous receipt hash.  This ensures tampering with any receipt breaks
the chain.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from typing import Dict, Any, List

from ecat_icat.pe_validator import validate_pe_candidate, load_candidate as load_pe


def compute_hash(data: str) -> str:
    """Return SHA256 hex digest of the provided string."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def generate_receipts(vector_dir: str) -> List[Dict[str, Any]]:
    """
    Generate receipts for all PE candidate vectors in ``vector_dir``.

    Returns a list of receipt dictionaries.  Each receipt contains a
    cryptographic hash linking to the previous receipt, so that any
    alteration of a receipt can be detected when the chain is verified.
    """
    receipts: List[Dict[str, Any]] = []
    prev_hash: str | None = None
    # Load candidates in sorted order for reproducible chain
    for fname in sorted(os.listdir(vector_dir)):
        if not fname.lower().endswith('.json'):
            continue
        fpath = os.path.join(vector_dir, fname)
        try:
            candidate = load_pe(fpath)
        except Exception:
            # Skip files that cannot be parsed
            continue
        cid = candidate.get('candidate_id', os.path.splitext(fname)[0])
        # Validate candidate
        outcome, reason, cost = validate_pe_candidate(candidate)
        # Compute basis hash as hash of sorted JSON candidate
        basis_str = json.dumps(candidate, sort_keys=True)
        basis_hash = compute_hash(basis_str)
        # Compute receipt hash linking previous receipt
        receipt_str = cid + outcome + reason + basis_hash + (prev_hash or '')
        receipt_hash = compute_hash(receipt_str)
        receipt = {
            'candidate_id': cid,
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


def verify_chain(receipts: List[Dict[str, Any]]) -> bool:
    """
    Verify the receipt chain by recomputing each ``receipt_hash`` and
    comparing with stored values.  Returns True if the chain is valid
    and False otherwise.
    """
    prev_hash: str | None = None
    for rec in receipts:
        cid = rec['candidate_id']
        outcome = rec['outcome']
        reason = rec['reason']
        basis_hash = rec['basis_hash']
        expected_prev = rec['prev_receipt_hash']
        # Recompute hash string
        recomputed = compute_hash(cid + outcome + reason + basis_hash + (prev_hash or ''))
        if recomputed != rec['receipt_hash'] or expected_prev != prev_hash:
            return False
        prev_hash = rec['receipt_hash']
    return True


def save_receipts(receipts: List[Dict[str, Any]], path: str) -> None:
    """Write receipts to ``path`` in JSONL format."""
    with open(path, 'w', encoding='utf-8') as f:
        for rec in receipts:
            f.write(json.dumps(rec) + '\n')


def save_summary(receipts: List[Dict[str, Any]], report_path: str, summary_path: str) -> None:
    """
    Save a JSON report and Markdown summary summarising the receipts.
    The report includes counts of outcomes and whether the chain is valid.
    """
    total = len(receipts)
    counts = {'ALLOW': 0, 'DENY': 0, 'FAIL_CLOSED': 0}
    for rec in receipts:
        outcome = rec['outcome']
        counts[outcome] = counts.get(outcome, 0) + 1
    chain_valid = verify_chain(receipts)
    # JSON report
    report = {
        'schema': 'stegverse.sandbox.pe.sandbox_report.v1',
        'total': total,
        'allow': counts.get('ALLOW', 0),
        'deny': counts.get('DENY', 0),
        'fail_closed': counts.get('FAIL_CLOSED', 0),
        'chain_valid': chain_valid,
        'receipts': receipts
    }
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    # Markdown summary
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write('# PE Sandbox Summary\n\n')
        f.write(f'- Receipts emitted: **{total}**\n')
        f.write(f'- Chain valid: **{chain_valid}**\n')
        f.write(f'- Allowed: **{counts.get("ALLOW", 0)}**\n')
        f.write(f'- Denied: **{counts.get("DENY", 0)}**\n')
        f.write(f'- Fail Closed: **{counts.get("FAIL_CLOSED", 0)}**\n\n')
        f.write('| ID | Outcome | Reason | Total Cost | Budget | Pass? |\n')
        f.write('|---|---|---|---|---|---|\n')
        for rec in receipts:
            cid = rec['candidate_id']
            outcome = rec['outcome']
            reason = rec['reason']
            cost_dict = rec.get('cost', {}) or {}
            total_cost = cost_dict.get('total_cost', '')
            budget = cost_dict.get('budget', '')
            pass_indicator = '✅' if outcome == 'ALLOW' else '❌'
            f.write(f'| {cid} | {outcome} | {reason} | {total_cost} | {budget} | {pass_indicator} |\n')


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate PE sandbox receipts and summary.')
    parser.add_argument('--vectors', required=True, help='Directory containing PE candidate JSON files')
    parser.add_argument('--receipts', required=True, help='Path to write receipts JSONL')
    parser.add_argument('--report', required=True, help='Path to write summary report JSON')
    parser.add_argument('--summary', required=True, help='Path to write summary Markdown')
    args = parser.parse_args()
    receipts = generate_receipts(args.vectors)
    save_receipts(receipts, args.receipts)
    save_summary(receipts, args.report, args.summary)
    print(f'Receipts generated: {len(receipts)}. Chain valid: {verify_chain(receipts)}')


if __name__ == '__main__':
    main()