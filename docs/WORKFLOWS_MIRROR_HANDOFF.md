# GCAT-BCAT-Engine/workflows Mirror Handoff

Generated: 2026-05-15

## Purpose

This handoff is the source of truth for workflow-side continuation work that is not part of `StegVerse-Labs/Site` or Publisher-to-Site mirroring.

Use this file before continuing work in `GCAT-BCAT-Engine/workflows` so future sessions do not duplicate or reset the current direction.

## Current Goal

Build one reusable, organization/repository-agnostic sandbox builder that can target any repo by input instead of creating a custom bootstrap workflow per repo.

The builder must:

```text
accept target_repo
accept target_branch
accept build_profile
accept mode = artifact_only | commit
clone the target repo
build in an isolated sandbox directory
run tests inside the sandbox
zip tested generated files
emit manifest/checksum/test/receipt artifacts
commit only after sandbox tests pass and only when mode=commit
```

## Repo Roles

```text
GCAT-BCAT-Engine/workflows
  reusable orchestration workflows
  LLM Adapter Gate
  future org/repo-agnostic sandbox builder

GCAT-BCAT-Engine/core-lite-prod
  operational core services surface
  must be proven before user-facing core-lite is augmented

GCAT-BCAT-Engine/core-lite
  public/user-facing production package source
  should only receive tested, core-lite-prod-derived updates
```

## Confirmed Existing Workflow Layer

`GCAT-BCAT-Engine/workflows` already has provider secrets confirmed:

```text
OPENAI_API_KEY configured
ANTHROPIC_API_KEY configured
```

Existing installed layer:

```text
.github/workflows/llm-provider-check.yml
.github/workflows/llm-adapter-gate.yml
.github/workflows/validation_run.yml
```

## Current Blocker

Manual bundle/file-layer uploading is not acceptable as the primary build path.

The next build must not require per-repo manual bundle extraction or repo-specific workflow rewriting.

## Next Required Build

Create:

```text
.github/workflows/stegverse-sandbox-builder.yml
```

The first target run should be:

```text
target_repo = GCAT-BCAT-Engine/core-lite-prod
target_branch = main
build_profile = core-lite-prod
mode = artifact_only
target_path = .
```

## Required Done Criteria

The sandbox builder is not done until it produces these artifacts from a GitHub Ubuntu run:

```text
generated-files.zip
generated-files-manifest.json
test-report.json
selftest-report.json
receipt.json
artifact-manifest.json
confidence-report.json
```

No target repo mutation may occur in `artifact_only` mode.

`commit` mode is allowed only after the artifact-only run is clean.

## Build Rules

```text
No clean-repo baseline into populated repos.
No manual file-layer upload as primary workflow.
No repo-specific bootstrap if the reusable builder can do it.
No mutation before sandbox tests pass.
No bundle without manifest/checksum.
No working claim without test output.
No LLM provider output gets authority without TVC/CGE/receipt boundary.
```

## Archive Readiness

This handoff is sufficient for the next session to continue without needing the prior chat thread.
