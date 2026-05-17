# CHF Validation Matrix

## CHF-001 — Minimal 2D Consequence Horizon Model

| Case | Point | Expected | Meaning |
|---|---:|---|---|
| p1 | (0.4, 0.4) | ALLOW | Stable cell and inside horizon |
| p2 | (-0.4, 0.4) | DENY | Limited cell radius exceeded |
| p3 | (-0.4, -0.4) | DENY | Forbidden cell |
| p4 | (0.7, -0.2) | FAIL_CLOSED | Uncertain cell without confidence |
| p5 | (0.9, 0.1) | DENY | Outside consequence horizon |

## CHF-002 — Multi-Center Uncertainty Extension

| Case | Point | Expected | Meaning |
|---|---:|---|---|
| pA | (0.4, 0.4) | ALLOW | Safe under both plausible centers |
| pB | (-0.9, 0) | FAIL_CLOSED | Not inside all plausible transition regions |
| pC | (0.85, 0) | FAIL_CLOSED | Horizon status depends on unresolved center |

## CHF-003 — Two-Body Coupled Cloud Deformation

| Local Permit | Deformation | Tolerance | Recoverability | Threshold | Expected |
|---|---:|---:|---:|---:|---|
| ALLOW | 0.25 | 0.20 | 0.65 | 0.70 | DENY |

## Done Criteria

A successful run produces:

1. `chf_validation_report_<RUN_ID>.json`
2. `chf_validation_summary_<RUN_ID>.md`
3. PASS status for CHF-001, CHF-002, and CHF-003
