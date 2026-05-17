# CHF Validation Matrix

## CHF-001 — Minimal 2D Consequence Horizon Model

| Case | Expected | Meaning |
|---|---|---|
| `p1` | `ALLOW` | stable cell and inside horizon |
| `p2` | `DENY` | cell-specific radius limit exceeded |
| `p3` | `DENY` | forbidden cell |
| `p4` | `FAIL_CLOSED` | uncertain cell |
| `p5` | `DENY` | outside consequence horizon |

## CHF-002 — Multi-Center Uncertainty

| Case | Expected | Meaning |
|---|---|---|
| `pA` | `ALLOW` | all plausible centers pass |
| `pB` | `FAIL_CLOSED` | not safe across all plausible centers |
| `pC` | `FAIL_CLOSED` | horizon safety differs across plausible centers |

## CHF-003 — Two-Body Coupled Cloud Deformation

| Case | Expected | Meaning |
|---|---|---|
| `chf-003` | `DENY` | deformation exceeds affected cloud tolerance |

## CHF-004 — Observer Projection and Sphericalization

| Case | Expected | Meaning |
|---|---|---|
| `O_far_low_resolution` | `SMOOTH_SHELL` | far/low-resolution observer sees sphericalized shell |
| `O_near_high_resolution` | `CELL_RESOLVED` | near/high-resolution observer resolves cell structure |
| `O_noisy_intermediate` | `SMOOTH_SHELL` | noise suppresses cell recovery |

## CHF-005 — Threshold Record and Legibility Decay

| Case | Expected | Meaning |
|---|---|---|
| `chi_allow_legible` | `RECORD_LEGIBLE` | actualized crossing has shell and readable record |
| `chi_allow_low_legibility` | `RECORD_EXISTS_LOW_LEGIBILITY` | record exists, but legibility decayed below threshold |
| `denied_attempt` | `NO_PROPAGATED_RECORD_REQUIRED` | no actualized crossing, so no propagated record is required |
