# SV-COST Mirror Handoff

Status: **CANONICAL — CROSS-MODEL GOVERNANCE INTEGRATION ACTIVE**

## Active goal

- Goal ID: `SV-COST-MAJOR-GOAL-001`
- Current subgoal: `SV-COST-CROSS-MODEL-SESSION-001`
- Originating goal: compare every model and route under the same task, outcome, admissibility, evidence, and cost rules so governance is demonstrated by refusing the cheapest invalid result.
- Repository and branch: `GCAT-BCAT-Engine/workflows@main`
- Canonical issue: `#13`
- Canonical continuation: this handoff, issue `#13`, and `experiments/sv-cost-program/cross-model-session-inventory.json`.

The earlier R1–R5 relational program remains terminal. The current work does not amend its receipts. It installs a reusable cross-model admission-and-cost review layer on top of existing observed evidence.

## Authoritative files

1. `SV_COST_MIRROR_HANDOFF.md`
2. `experiments/sv-cost-program/session-goal-inventory.json`
3. `experiments/sv-cost-program/cross-model-session-inventory.json`
4. `experiments/sv-cost-program/task-claims.json`
5. `experiments/sv-cost-program/cost-model/governance-vs-no-governance-contract.json`
6. `experiments/sv-cost-program/cost-model/model-registry.json`
7. `experiments/sv-cost-program/cost-model/canonical-task-set.json`
8. `experiments/sv-cost-program/results/governance-cross-model-matrix.json`
9. `experiments/sv-cost-program/results/normalized-operation-class-matrix.json`
10. `experiments/sv-cost-program/results/cross-model-session-receipt.json`
11. `docs/SV_COST_MAJOR_ANALYSIS.md`
12. issue `#13`

Live Git state, workflow jobs and logs, committed matrices, provider receipts, and immutable artifacts override prior chat statements.

## Session goal inventory

### Primary goal

Install a standard model-review method whose comparison unit is `successful equivalent admissible outcome` and whose selection order is:

1. preserve task identity;
2. complete the required operation;
3. satisfy output and quality obligations;
4. satisfy evidence, auditability, and admissibility gates;
5. compare cost only among passing lanes;
6. accept a justified premium when it purchases required capability or production obligations.

### Adjacent goals

- preserve the first cost-analysis finding that the cheapest admissible run is not the cheapest observed run;
- compare native and StegVerse-governed lanes for each registered model;
- separate fresh inference, admitted reconstruction, and prospective estimation into distinct operation and evidence classes;
- retain token data only as provider-interface metadata, not as compute, energy, useful-work, or profitability evidence;
- demonstrate governance through explicit refusal of zero-cost, lower-cost, failed, incomplete, or task-changing lanes;
- automate matrix generation, invariants, receipts, and continuation without chat supervision;
- durably transfer all unique requirements and execution authority so this session can close when the repository receipt reports `ARCHIVE_READY`.

## Canonical ownership and claims

- R1–R5 relational program: `COMPLETE`; terminal issue `#12` and existing receipts remain authoritative.
- Cross-model comparison contract: `COMPLETE`; commit `03fb4a7621f84879be8353f94bbda10ca85968c7`.
- Model registry: `COMPLETE`; commit `c53c0ddb68de7115eec14ea74de3f9176bc6a3e2`.
- Canonical task classes: `COMPLETE`; commit `8f6b12453fd585c663236fcc187e128d3d467dea`.
- Fresh formal-proof calibration matrix: `COMPLETE`; commit `ce9c8e59a3541f939a59584a47f7506196c084f8`.
- Fresh matrix invariant validation: `COMPLETE`; workflow commit `47c9f5eebd7af5a2dddea31395bdd03e17f682e7` and green hosted run.
- Normalized reconstruction/characterization matrix: `MACHINE_OWNED`; owner `.github/workflows/sv-cost-normalized-operation-adjudication.yml`.
- Cross-model session consolidation: `MACHINE_OWNED`; owner `.github/workflows/sv-cost-cross-model-session-consolidation.yml`.
- Favorable general ROI evidence: `BLOCKED`; durable owner issue `#13`.

No alternate cost-analysis family is authorized. No chat session is an implementation authority. Repository workflows, issue `#13`, and this handoff are the coordination layer.

## Completed implementation

- Installed `governance-vs-no-governance-contract.json` with the original 50% validated batch finding, the rejected 95% apparent saving, and the rule that price is considered only after admissibility.
- Installed `model-registry.json` and `canonical-task-set.json`.
- Installed `adjudicate_cross_model_governance.py` and its hosted workflow.
- Corrected untracked-output commit detection and added machine-enforced invariants.
- Committed `governance-cross-model-matrix.json` and `reports/governance-cross-model-matrix.md`.
- The observed calibration rejected `openai-raw` for task-identity failure and `stegverse-only` for no execution and no required output, despite the latter's zero provider charge.
- The bounded structurally admissible selection was `anthropic-raw` at `$0.061713`.
- Installed `adjudicate_normalized_operation_class.py` and a hosted workflow for the distinct reconstruction/characterization operation class.
- Corrected the normalized workflow's push-race handling and added failure diagnostics in commit `c975b393762e792b205ba5a610c8ee790c5f42cf`.
- Installed `cross-model-session-inventory.json` and `tools/validate_sv_cost_cross_model_session.py`.

## Incomplete work

### Machine-owned completion required for this session

1. `.github/workflows/sv-cost-normalized-operation-adjudication.yml` must commit:
   - `experiments/sv-cost-program/results/normalized-operation-class-matrix.json`
   - `reports/normalized-operation-class-matrix.md`
2. `.github/workflows/sv-cost-cross-model-session-consolidation.yml` must validate both matrices and commit:
   - `experiments/sv-cost-program/results/cross-model-session-receipt.json`
3. The receipt must report `ARCHIVE_READY` before this session may be archived.

### Independent future evidence work

Issue `#13` owns additional observed models, held-out quality-equivalent tasks, fully burdened local cost, invoice reconciliation, and break-even analysis. That continuation does not require this chat once the cross-model session receipt is archive-ready.

## Exact next tasks

- Observe the normalized adjudication workflow triggered by commit `c975b393762e792b205ba5a610c8ee790c5f42cf`.
- If it fails, inspect its job logs and repair the exact failing step; do not infer the cause from the workflow status alone.
- After its output is committed, run the cross-model session consolidation workflow.
- Future model additions must update `model-registry.json`, use a canonical task from `canonical-task-set.json`, and pass the same admission-before-cost validators.

## Blockers and release conditions

- Current archival blocker: `normalized-operation-class-matrix.json` is not yet committed.
- Owner: `.github/workflows/sv-cost-normalized-operation-adjudication.yml`.
- Machine-observable release condition: the workflow commits the matrix and report after all operation-class assertions pass.
- Final archival release condition: `cross-model-session-receipt.json.status == ARCHIVE_READY`.
- Favorable ROI blocker remains independent: issue `#13` must produce inspectable cost sources, meters, invoices, held-out equivalence, and break-even evidence before a favorable general economic claim.

## Cross-repository dependencies

The bounded negative/general-claim decision was previously mirrored to `StegVerse-Labs/Site`, but live deployment was not established by repository mutation alone. No new propagation to Publisher, admissibility-wiki, stegguardian-wiki, or master-records is claimed in this continuation. Any future propagator must inspect the destination's newest mirror handoff and preserve operation-class and claim boundaries.

## Validation commands

```bash
python -m json.tool experiments/sv-cost-program/cross-model-session-inventory.json
python -m json.tool experiments/sv-cost-program/cost-model/governance-vs-no-governance-contract.json
python -m json.tool experiments/sv-cost-program/cost-model/model-registry.json
python -m json.tool experiments/sv-cost-program/cost-model/canonical-task-set.json
python experiments/sv-cost-program/tools/adjudicate_cross_model_governance.py
python experiments/sv-cost-program/tools/validate_cross_model_matrix.py
python experiments/sv-cost-program/tools/adjudicate_normalized_operation_class.py
python tools/validate_sv_cost_cross_model_session.py
```

Hosted validation:

- `.github/workflows/sv-cost-cross-model-adjudication.yml`
- `.github/workflows/sv-cost-normalized-operation-adjudication.yml`
- `.github/workflows/sv-cost-cross-model-session-consolidation.yml`

## Requirements transferred from this session

- all models reviewed under the same task and output obligations;
- cost differences allowed only when the capability or production difference is explicit;
- cheapest observed output cannot win merely because it is cheapest;
- governance is demonstrated by refusal at the selection boundary;
- tokens are not a physical or useful-work unit and cannot determine the winner;
- pricing contains unknown margin and is not provider-resource evidence;
- fresh inference and reconstruction cannot silently compete as equivalent operations;
- estimates cannot be pooled with observed execution;
- repository-native automation owns continuation and archival determination.

MERGED INTO: `GCAT-BCAT-Engine/workflows/SV_COST_MIRROR_HANDOFF.md`, `experiments/sv-cost-program/cross-model-session-inventory.json`, issue `#13`, and the workflows and result locations named above.

## Supersession and convergence

- Prior chat interpretations that centered token reduction as the main efficiency result are superseded.
- Prior framing that reduced the objective to fear-based mistake prevention is superseded.
- The canonical objective is an evidence-visible, admission-first comparison across models and StegVerse governance.
- Existing R1–R5 receipts remain unchanged.
- This continuation is merged into issue `#13`; no duplicate issue or experiment family should be created.

## Archive conditions

This session is archive-ready only when:

1. the normalized operation-class matrix and report are committed;
2. both cross-model matrices pass their repository validators;
3. `cross-model-session-receipt.json` reports `ARCHIVE_READY`;
4. no active chat-owned claim remains;
5. issue `#13` is recorded as the independent durable continuation for future model expansion and economic evidence.

## Percentages

Denominator for this continuation: 6 required tasks in `cross-model-session-inventory.json`.

- Task completion: 4/6 complete; 2/6 machine-owned.
- Developed files: 9/10 installed; normalized matrix/report count as one required output group.
- Validation: 4/6 validated.
- Integration: 5/6 linked into canonical controls.
- Goal activation: 5/6.
- Session consolidation: 5/6 unique goal groups transferred or complete.
