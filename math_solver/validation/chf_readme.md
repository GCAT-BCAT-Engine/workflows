# Consequence Horizon Formalism Validation

This directory contains deterministic pre-code validation specs for the Consequence Horizon Formalism (CHF).

CHF models transition logic as:

```text
cloud -> center -> radial transition region -> cell -> horizon -> crossing -> shell -> record -> new center
```

The current validation suite is intentionally narrow and deterministic. It does not call external APIs.

## Included specs

| Spec | Purpose | Core claim |
|---|---|---|
| `problem_spec_chf_001.yml` | Minimal 2D disk model | ALLOW / DENY / FAIL_CLOSED category grammar |
| `problem_spec_chf_002.yml` | Multi-center uncertainty | uncertainty must not become permission |
| `problem_spec_chf_003.yml` | Two-body coupling | local ALLOW is not global ALLOW |
| `problem_spec_chf_004.yml` | Observer projection | distance sphericalizes, resolution re-cellularizes |
| `problem_spec_chf_005.yml` | Threshold record | crossings require shell and record; legibility may decay |

## Run locally

```bash
python math_solver/validation/chf_deterministic_validator.py \
  --spec-dir math_solver/validation \
  --out-json math_solver/validation/brain_reports/chf_validation_report_LOCAL.json \
  --out-md math_solver/validation/brain_reports/chf_validation_summary_LOCAL.md
```

## GitHub Actions

The workflow file is installed at:

```text
.github/workflows/chf_validation_run.yml
```

For iOS-safe upload workflows, the same file is mirrored at:

```text
iosnoperiod/github/workflows/chf_validation_run.yml
```

The mirror path is for visibility only. The canonical GitHub Actions path remains `.github/workflows/chf_validation_run.yml`.
