# StegClaw

StegClaw is a minimal repo-local substitute for a cloud coding agent when Copilot cloud agent assignment is unavailable.

It does not try to solve mathematics directly. Its first job is to inspect the existing StegVerse math-solver surface, emit receipts about what exists, and produce bounded next issue packets.

## Assumptions

- The target repo already contains or will contain `math_solver/`.
- `math_solver/` is the existing artifact to evolve, not replace.
- The first useful action is audit before modification.
- GitHub Actions is available.

## Done definition

StegClaw v0.1 is done when a manual GitHub Actions run produces a downloadable artifact named `stegclaw-audit` containing:

- `STEGCLAW_AUDIT.md`
- `STEGCLAW_NEXT_ISSUES.md`
- `stegclaw_audit.json`

## Files in this bundle

- `tools/stegclaw_audit.py`
- `.github/workflows/stegclaw-audit.yml`
- `STEGCLAW.md`

## How to install on iPhone through GitHub web

1. Open the repo: `GCAT-BCAT-Engine`.
2. Add `tools/stegclaw_audit.py` using the full file replacement from this bundle.
3. Add `.github/workflows/stegclaw-audit.yml` using the full file replacement from this bundle.
4. Commit both files to `main`.
5. Open the Actions tab.
6. Run `StegClaw Audit` manually.
7. Download the `stegclaw-audit` artifact.

## What StegClaw does

- Scans `math_solver/`.
- Lists files, sizes, SHA-256 hashes, Python imports, and StegVerse references.
- Detects repo-level signals such as `triad/`, `full_pipeline/`, validator files, and workflows.
- Emits next issue packets for the bounded build sequence.

## What StegClaw does not do

- It does not call external APIs.
- It does not modify source files.
- It does not claim mathematical proofs.
- It does not replace Copilot, Codex, or a human reviewer.

## Next build after v0.1

After the audit artifact is downloaded, the next build should add sandbox receipt primitives to `math_solver/`.
