# GCAT-BCAT Workflows Security Mirror Handoff

Status: ACTIVE — TV/TVC PROVIDER AUTHORITY MIGRATION / HISTORICAL PROVENANCE AUDIT

Established: 2026-08-19
Canonical repository: `GCAT-BCAT-Engine/workflows`
Parent handoff: `docs/WORKFLOWS_MIRROR_HANDOFF.md`
Canonical provider consumer handoff: `docs/TVC_PROVIDER_CAPABILITY_CONSUMER_MIRROR_HANDOFF.md`
Canonical security task: issue `#16`

## Governing boundary

- Provider-capability and provider-credential authority belongs to `StegVerse-Labs/TVC`.
- Consumer policy authority is false.
- Provider credentials must not be interpolated directly into this repository's GitHub Actions workflows.
- GitHub Actions success is evidence only; it is not provider execution authority, TVC authority, admissibility, publication, mutation, release, or activation authority.
- Route/provider availability is non-authorizing evidence.
- Missing TVC/provider execution/mutation authority fails closed.
- Historical experiment outputs remain evidence and are not invalidated merely because their execution boundary is now contained.

## Containment completed 2026-08-19

The following live provider-secret or authority-substitution workflows were converted to manual, read-only, fail-closed placeholders:

- `.github/workflows/llm-adapter-gate.yml`
- `.github/workflows/llm-provider-check.yml`
- `.github/workflows/provider-token-normalization.yml`
- `.github/workflows/sv-cost-live-openai-anthropic-stream.yml`
- `.github/workflows/sv-cost-normalized.yml`
- `.github/workflows/staged-math-progress.yml`
- `.github/workflows/five-lane-calibration.yml`
- `.github/workflows/ten-advances-estimation.yml`
- `.github/workflows/governed-cost-evaluation.yml`
- `.github/workflows/sv-cost-five-lane-results.yml`
- `.github/workflows/stegverse-compact-progress.yml`
- `.github/workflows/four-lane-equivalent-output.yml`
- `.github/workflows/sv-cost-r2-direct-vs-batch.yml`
- `.github/workflows/sv-cost-r3-full-vs-managed.yml`
- `.github/workflows/sv-cost-historical-rerun.yml`
- `.github/workflows/validation_run.yml`
- `.github/workflows/validation_run_inline.yml`

The prior workflows contained one or more of:

- direct provider API secret interpolation from repository/Actions secrets;
- provider network calls from the consumer workflow;
- `contents: write` authority;
- result commits/pushes to `main` from GitHub-hosted execution;
- local structures labeled as TVC/CGE/admissibility/verification without canonical independently reconstructable authority evidence;
- mutable third-party Action references.

Containment does not classify historical actors as malicious or unauthorized.

## Confirmed integrity-control defects

### Local pseudo-TVC decision

The legacy `llm-adapter-gate.yml` locally created a structure labeled as a TVC boundary and could produce `ALLOW` from local `authority_ref` / `policy_ref` presence plus prompt checks. Canonical TVC resolver/receipt evidence was not required.

Classification: authority/integrity overclaim. Malicious intent is not established.

### Local publication/admissibility gate

The legacy `sv-cost-five-lane-results.yml` treated locally generated `admissible` and publication-state fields as a publication gate. Any future admissibility/publication claim must bind independent governance evidence rather than self-attesting result fields.

### Static source-verification claim

The legacy `validation_run.yml` recorded a static source list and set a positive source-verification state without independently reconstructable source retrieval/verification evidence.

## Preserved live credential-free validation

The following lanes remain live because they do not consume provider credentials or mutate repository state under provider authority:

- `.github/workflows/sv-cost-generation-3-control-validation.yml`
  - anonymous public checkout;
  - `permissions: {}`;
  - no provider secret authority;
  - validation-only.
- `.github/workflows/stegverse-test-lanes-validation.yml`
  - anonymous public checkout;
  - `permissions: {}`;
  - no provider secret authority;
  - validation-only.
- `.github/workflows/sv-cost-nine-lane-candidate-proof.yml`
  - credentialless candidate boundary;
  - `contents: read`;
  - immutable checkout and artifact Action SHAs;
  - bounded timeout/concurrency;
  - artifact-only evidence;
  - publication blocks when the full evidence set is absent.

## Replacement architecture

Canonical provider capability remains the already-released TVC consumer contract described in `docs/TVC_PROVIDER_CAPABILITY_CONSUMER_MIRROR_HANDOFF.md`.

A replacement provider-execution lane must add a separately admitted execution surface that:

1. keeps provider credential material inside TV/TVC-owned execution;
2. binds exact provider/model/capability/policy source;
3. exports only secret-free provider result/evidence surfaces;
4. records actor/application/execution provenance;
5. grants no mutation or publication authority by virtue of provider execution alone.

Any durable result publication requires a separate target-scoped mutation capability binding exact source evidence, target repository/ref/path set, operation, decision, expiry, and result receipt.

## Historical audit requirements

For consequential historical provider-execution workflows, reconstruct where evidence permits:

- exact workflow source commit;
- triggering actor/application;
- credential/application authority or token provenance;
- provider/model actually called;
- third-party Action/dependency versions;
- result artifact and committed result hashes;
- repository visibility at event time;
- whether any TVC/CGE/admissibility/publication claim was externally evidenced or only locally synthesized.

Organization audit-log evidence remains required to close actor/token/visibility gaps.

## Completion gate

This security lane is not complete until:

- direct provider-secret consumer workflows remain absent from all active paths;
- required provider experiments are reintroduced only through admitted TV/TVC provider execution, or retired permanently;
- result publication is separately authorized and attributable;
- all active third-party Actions/containers are immutably bound;
- no local TVC/CGE/admissibility/verification label is accepted as authority without canonical evidence;
- historical provenance gaps are reconciled as far as retained audit evidence permits.

Do not restore provider API secrets directly into consumer GitHub Actions as a shortcut.


## Provider-secret regression guard — 2026-09-02

Issue: #16

A repository-wide active-workflow guard is now installed:

```text
tools/verify_no_direct_provider_secrets.py
tests/test_provider_secret_boundary.py
.github/workflows/provider-secret-boundary-validation.yml
```

The guard fails closed on:
- GitHub secret interpolation such as `${{ secrets.* }}` in active workflows;
- provider credential assignments/references for OpenAI, Anthropic, DeepSeek, Moonshot/Kimi, or Z.ai.

Negative validation markers that merely scan for forbidden names are not treated as credential use.

The workflow is validation-only:
- `permissions: {}`;
- pinned checkout action;
- no provider execution;
- no repository mutation;
- no credential authority.

This converts the "direct provider-secret consumer workflows remain absent from all active paths" completion criterion into a continuously machine-checked invariant.
