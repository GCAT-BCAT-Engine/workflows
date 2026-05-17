# Consequence Horizon Formalism — Validation Package

## Assumptions

- This package belongs under `GCAT-BCAT-Engine/workflows/math_solver/validation/`.
- It extends the existing math-solver/problem-solver path with a formalism-specific problem-spec family.
- It does not replace GCAT/BCAT.
- GCAT/BCAT should be treated as a local admissibility operator inside the broader Consequence Horizon Formalism.
- This package is spec-first. A Python adapter should only be added after these mathematical expectations are accepted.

## Done Criteria

This package is complete for the current step when the following files exist:

```text
math_solver/validation/problem_spec_chf_001.yml
math_solver/validation/problem_spec_chf_002.yml
math_solver/validation/problem_spec_chf_003.yml
math_solver/validation/chf_proof_obligations.md
math_solver/validation/chf_validation_matrix.md
math_solver/validation/chf_readme.md
```

## Purpose

The Consequence Horizon Formalism models a transition as:

```text
state-cloud
  → operational center
    → radial transition region
      → radial cell
        → consequence horizon
          → threshold crossing
            → historical shell
            → propagated record
            → new state-cloud
```

The first validation objective is not to prove cosmology. It is to make the mathematical transition grammar precise enough for deterministic solver validation.

## File Roles

### `problem_spec_chf_001.yml`

Minimal 2D model.

Validates:

- radial cells,
- consequence horizon,
- ALLOW / DENY / FAIL_CLOSED distinction,
- crossing event creation,
- historical shell and propagated record requirements.

### `problem_spec_chf_002.yml`

Multi-center uncertainty model.

Validates:

- multiple plausible centers,
- conservative safe region,
- uncertainty-preserving FAIL_CLOSED behavior,
- no cherry-picking of convenient state estimates.

### `problem_spec_chf_003.yml`

Two-body coupled-cloud deformation model.

Validates:

- local ALLOW versus coupled DENY,
- affected-cloud deformation thresholds,
- affected-entity recoverability thresholds,
- FAIL_CLOSED for unknown relevant deformation.

### `chf_proof_obligations.md`

Defines the proof obligations the specs are intended to support.

### `chf_validation_matrix.md`

Defines expected outcomes across all current CHF specs.

## Integration With GCAT/BCAT

GCAT/BCAT remains the local governance/admissibility model.

Consequence Horizon Formalism adds:

- geometry of transition potential,
- radial consequence cells,
- category-change horizon,
- shell/record semantics,
- uncertainty-safe state-cloud handling,
- many-body coupled-cloud deformation,
- observer projection in future CHF-004.

The combined future predicate should be:

```text
ALLOW only if:
  GeometryValid
  CellAssigned
  HorizonDefined
  GCAT_BCAT_Valid
  RecoverabilityValid
  UncertaintySafe
  CoupledCloudSafe
  ShellReady
  RecordReady
```

Otherwise:

```text
DENY       when a known violation exists
FAIL_CLOSED when the system lacks enough information to allow
```

## Next Step

After these specs are added, run the existing validation path against the new problem specs if the current runner supports them directly. If the current runner does not support these CHF fields, the minimal next change should be a narrow `chf_validator.py` adapter under `math_solver/validation/`.
