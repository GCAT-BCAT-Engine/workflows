# Triad Validation and Sandbox

This directory contains a simple proof‑of‑concept implementation of a
**Triad** admissibility gate.  The Triad combines six separate
governance/admissibility transforms—**GCAT**, **BCAT**, **ECAT**, **ICAT**,
**Probability of Existence** and **Inference Window**—into a single
layer.  A transition is only allowed if all six pieces individually
pass.  Costs from the entity, integrity, existence and inference
window layers are normalised by their `base_cost` and aggregated
into a single Triad cost.  An optional top‑level `triad_cost`
budget can override the outcome if the aggregated cost exceeds the
allotted budget.

## Contents

* `triad_validator.py` – Defines the Triad validator and command‑line
  interface for validating a directory of Triad candidates.
* `candidate_vectors/` – Sample Triad candidate JSON files.  See
  [Candidate format](#candidate-format) for details.
* `sandbox_adapter.py` – Generates receipts for Triad candidates,
  chains them and writes both JSON and Markdown summaries.
* `receipt_replay.py` – Replays Triad receipts, verifying the chain
  and checking that outcomes/reasons match upon re‑validation.
* `tamper_test.py` – Creates a tampered copy of a receipts file and
  verifies that the replay script detects the mismatch.  This shows
  that the receipt chain is integrity‑sensitive.

## Candidate format

Each Triad candidate is a JSON object containing sub‑objects for the
individual pieces.  The top‑level `candidate_id` uniquely identifies
the candidate.  See `candidate_vectors/TRIAD_001.json` for a working
example.  Fields for each piece correspond to the inputs expected by
the individual validators (`state` and `params` for GCAT/BCAT,
`entity` and `params` for ECAT, etc.).  An optional `iw` object may
be provided for the inference‑window layer; it should contain
`inference_window`, `params` and `budget` keys as described in
`inference_window/iw_validator.py`.  If `iw` is omitted the IW
layer defaults to `ALLOW` with zero cost.

## Scalar constant

All six pieces use a `base_cost` to scale their cost calculations.
For ECAT, ICAT, PE and IW the `base_cost` defaults to `1.0`.  When
aggregating costs across pieces the Triad validator divides each
piece’s total cost by its `base_cost` to express them in a common
unit.  This normalisation acts as a **scalar constant** shared by
all four cost‑bearing pieces.  Candidates may specify larger
`base_cost` values to emphasise a layer’s contribution, but the
Triad still reduces each cost back to the same scale before summing
them.  The default constant is therefore `1.0`.

## New in this revision

This revision introduces the Triad layer and associated sandbox
infrastructure.  The following files have been added:

| File | Description |
|-----|-------------|
| `triad_validator.py` | Triad validator combining GCAT/BCAT, ECAT, ICAT, PE and IW |
| `sandbox_adapter.py` | Generates receipt chains for Triad candidates |
| `receipt_replay.py` | Replays receipts and verifies chain integrity |
| `tamper_test.py` | Demonstrates tamper detection for Triad receipts |
| `candidate_vectors/TRIAD_*.json` | Sample Triad candidate vectors |

## Running the validator

To validate all Triad candidates in the `candidate_vectors` directory and
generate a report and summary table:

```
python triad_validator.py --vectors triad/candidate_vectors \
    --report triad_report.json --summary triad_summary.md
```

## Running the sandbox adapter

To generate receipts and a summary from the same candidates:

```
python triad/sandbox_adapter.py \
    --vectors triad/candidate_vectors \
    --receipts triad/brain_reports/triad_receipts.jsonl \
    --report triad/brain_reports/triad_sandbox_report.json \
    --summary triad/brain_reports/triad_sandbox_summary.md
```

## Replaying receipts

To replay the receipts and verify outcomes:

```
python triad/receipt_replay.py \
    --receipts triad/brain_reports/triad_receipts.jsonl \
    --vectors triad/candidate_vectors \
    --report triad/brain_reports/triad_replay_report.json \
    --summary triad/brain_reports/triad_replay_summary.md
```

## Tamper detection

To verify that the receipt chain detects tampering:

```
python triad/tamper_test.py \
    --original_receipts triad/brain_reports/triad_receipts.jsonl \
    --tampered_receipts triad/brain_reports/triad_receipts_tampered.jsonl \
    --vectors triad/candidate_vectors \
    --report triad/brain_reports/triad_tamper_replay_report.json \
    --summary triad/brain_reports/triad_tamper_replay_summary.md
```

This will flip the outcome of the first receipt, replay the modified
receipts and confirm that the mismatch is detected.
