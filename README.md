# GCAT-BCAT-Engine / Workflows

**Deterministic workflow orchestration for GCAT/BCAT formal validation and mathematical proof pipelines.**

This repository houses the GitHub Actions workflows, validation runners, and orchestration specs that power automated mathematical verification, problem-solving pipelines, and deterministic state-transition testing across the StegVerse ecosystem.

---

## Repository Structure

```
.github/workflows/
├── validation_run.yml              # Primary validation workflow
├── validation_run_inline.yml       # Inline (no external deps) validation

math_solver/
└── validation/
    ├── run_validation.sh           # Shell entrypoint for local/CI validation
    ├── validation_runner.py        # Core Python validation engine
    ├── problem_spec_sv_math_001.yml  # Problem specification template (SV-MATH-001)
    ├── stegverse_math_solver_orchestrator_v1.yml  # Orchestrator manifest
    └── validation_run_v1.yml       # Versioned validation run config

README.md
```

---

## Purpose

This repo serves as the **computational backbone** for:

- **GCAT/BCAT Formal Verification** — Automated validation of geometrically ontological divergence (GOD) proofs and admissibility criteria.
- **Mathematical Problem-Solving Pipelines** — Structured ingestion of unsolved problems, formalization, proof generation, and sandboxed verification.
- **Deterministic State-Transition Testing** — ALLOW / DENY / FAIL_CLOSED gate validation with seed-based reproducibility.
- **Cross-Org Orchestration** — Repo-agnostic, platform-agnostic workflow dispatch across StegVerse-Labs, StegVerse-org, and GCAT-BCAT-Engine.

---

## Workflows

| Workflow | File | Trigger | Purpose |
|---|---|---|---|
| Validation Run | `.github/workflows/validation_run.yml` | `push`, `pull_request`, `workflow_dispatch` | Full validation suite with external sandbox integration |
| Inline Validation | `.github/workflows/validation_run_inline.yml` | `workflow_dispatch` | Self-contained validation (no external sandbox deps) |

---

## Math Solver / Validation

The `math_solver/validation/` directory contains the core execution layer:

- **`validation_runner.py`** — Python engine that ingests `problem_spec_*.yml` files, executes deterministic tests, and emits structured results (ALLOW / DENY / NO_EFFECT / FAIL_CLOSED).
- **`run_validation.sh`** — POSIX-compliant shell wrapper for local execution or headless CI runners.
- **`problem_spec_sv_math_001.yml`** — Canonical problem specification format. Defines inputs, expected invariants, confidence thresholds, and sandbox requirements.
- **`stegverse_math_solver_orchestrator_v1.yml`** — Manifest-driven orchestration spec. Declares multi-stage pipelines: ingestion → formalization → proof → sandbox verification → publication readiness.
- **`validation_run_v1.yml`** — Version-locked runtime configuration. Pins dependencies, seeds, and sandbox endpoints for reproducible builds.

---

## Problem Specification Format

Problem specs (`problem_spec_sv_*.yml`) declare:

```yaml
problem_id: sv-math-001
domain: geometric_topology
status: open|in_progress|formalized|verified
invariants:
  - name: boundary_preservation
    type: gcat_admissibility
    threshold: 0.999
sandbox:
  required: true
  tier: 0|1|2|3
  timeout_seconds: 300
```

The orchestrator consumes these specs and dispatches stages to appropriate sandboxes within the StegVerse ecosystem.

---

## Secrets & Security

All secrets and tokens are managed via **TV/TVC (TrustVault / TrustVaultController)** as ephemeral artifacts.
No long-lived tokens are stored in this repository. The ecosystem is **platform-agnostic** — workflows run on GitHub Actions today, but the manifests and runners are portable to any CI/CD backend.

> For TV/TVC integration details, see the [StegVerse-Labs/TV](https://github.com/StegVerse-Labs/TV) and [StegVerse-Labs/TVC](https://github.com/StegVerse-Labs/TVC) repositories.

---

## Usage

### Local Validation
```bash
cd math_solver/validation
chmod +x run_validation.sh
./run_validation.sh --spec problem_spec_sv_math_001.yml
```

### Trigger via GitHub Actions
Navigate to **Actions → Validation Run → Run workflow** and select the problem spec and sandbox tier.

---

## Ecosystem Context

| Organization | Role |
|---|---|
| [StegVerse-Labs](https://github.com/StegVerse-Labs) | Core infrastructure, TV/TVC, SDK, experimental sandboxes |
| [StegVerse-org](https://github.com/StegVerse-org) | Customer-facing tools, SDK distribution, demo pages |
| [GCAT-BCAT-Engine](https://github.com/GCAT-BCAT-Engine) | **This org** — Production-grade formal verification, mathematical engines, publishable papers |
| [StegGhost](https://github.com/StegGhost) | Personal/experimental sandbox, entity-runner testing |
| [ECAT-ICAT-Formal](https://github.com/ECAT-ICAT-Formal) | Mathematical formalization with synthetic experimental data |

---

## Contributing

1. Fork and branch from `main`.
2. Add or update problem specs in `math_solver/validation/`.
3. Ensure `validation_runner.py` passes with your spec (seed-locked).
4. Open a PR. The `validation_run.yml` workflow will execute automatically.

---

## License

See [LICENSE](LICENSE) in the org-level `.github` repository.

---

**StegVerse — Geometrically Ontological Divergence, formalized.**
