# Consequence Horizon Formalism Validation Package

## Purpose

This package adds a deterministic validation lane for the Consequence Horizon Formalism inside `GCAT-BCAT-Engine/workflows`.

It does not replace the existing real API validation workflow. It adds an offline mathematical validation path for the first CHF toy models.

## Files

- `github/workflows/chf_validation_run.yml` — displayed without the leading dot; the bundle preserves the real `.github/workflows/` path.
- `math_solver/validation/problem_spec_chf_001.yml`
- `math_solver/validation/problem_spec_chf_002.yml`
- `math_solver/validation/problem_spec_chf_003.yml`
- `math_solver/validation/chf_deterministic_validator.py`
- `math_solver/validation/chf_proof_obligations.md`
- `math_solver/validation/chf_validation_matrix.md`

## Done Criteria

Run the `Consequence Horizon Formalism Validation` workflow manually. The run is successful when the uploaded artifact contains a JSON report and Markdown summary showing all CHF specs passed.
