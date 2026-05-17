# Consequence Horizon Formalism Validation

This directory contains deterministic pre-code validation specs for the Consequence Horizon Formalism.

The validation lane is intentionally local and deterministic. It does not call external APIs.

## Current specs

| Spec | Purpose |
|---|---|
| `problem_spec_chf_001.yml` | Minimal 2D consequence horizon model |
| `problem_spec_chf_002.yml` | Multi-center uncertainty extension |
| `problem_spec_chf_003.yml` | Two-body coupled cloud deformation |
| `problem_spec_chf_004.yml` | Observer projection and sphericalization |
| `problem_spec_chf_005.yml` | Threshold record and legibility decay |
| `problem_spec_chf_006.yml` | 3D radial consequence cell assignment |
| `problem_spec_chf_007.yml` | Star-shaped geometry gate and radial coverage failure modes |
| `problem_spec_chf_008.yml` | GCAT/BCAT local admissibility operator inside a radial cell |
| `problem_spec_chf_009.yml` | Commit crossing requires GCAT pass, historical shell, and propagated record |
| `problem_spec_chf_010.yml` | Recoverability and purpose-convergence gate |
| `problem_spec_chf_011.yml` | Lag-reachable set commit gate |
| `problem_spec_chf_012.yml` | Historical shell chain continuity |
| `problem_spec_chf_013.yml` | Many-body relevance threshold gate |

## Current validation target

The validator should report:

```text
Overall status: PASS
Specs evaluated: 13
```

## Formal interpretation

The current lane validates these claims:

1. A proposed transition can be assigned to a radial consequence cell.
2. ALLOW, DENY, FAIL_CLOSED, and NO_EFFECT remain distinct.
3. Potential does not become actual without a threshold crossing.
4. Multi-center uncertainty blocks non-robust permission.
5. Local admissibility is not global admissibility.
6. Observer distance and resolution affect whether the shell appears smooth or cell-resolved.
7. Actualized crossings require records, while record legibility can decay.
8. 3D radial cell assignment can be checked deterministically.
9. Non-star-shaped geometry fails closed before cell coverage is assumed.
10. GCAT/BCAT can operate as a local admissibility operator inside a CHF radial cell.
11. Commit crossing requires both admissibility and shell/record readiness.
12. Recoverability and purpose-convergence can independently block a transition.
13. Lag-reachable uncertainty can fail closed before commit.
14. Historical shell chains require continuity and sufficient legibility.
15. Many-body effects below threshold may be NO_EFFECT, while protected/unknown effects fail closed.
