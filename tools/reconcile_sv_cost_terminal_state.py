#!/usr/bin/env python3
"""Reconcile terminal SV-COST receipts into every canonical control surface."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "experiments" / "sv-cost-program"
RESULTS = PROGRAM / "results"

R3_EVIDENCE_COMMIT = "ca04407737cfe8257014d36c1d680d4df2729f8b"
R3_ADJUDICATION_COMMIT = "d1617f6ce3419b20c44df13118509e73a1d3ec20"
FINALIZER_COMMIT = "4d8cf5b072f1e0cf232920249a13d24bafe4a81f"
R3_ARTIFACT_ID = 8863128197
R3_ARTIFACT_DIGEST = "sha256:8591f70a40d1765d15fb45902d22643f5189d777126ca45d18e941d1b38e7912"


def load(path: Path):
    return json.loads(path.read_text())


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-session", action="store_true")
    parser.add_argument("--workflow-run-url", default="repository-native reconciliation")
    return parser.parse_args()


def update_evidence_index(r3, r4, r5, cfo) -> None:
    path = PROGRAM / "evidence-index.json"
    doc = load(path)
    doc["status"] = "RELATIONAL_PROGRAM_EXECUTED_DECISION_READY_BOUNDED_CLAIMS"
    doc["active_relation"] = None
    doc["terminal_relations"] = [
        "R1-HISTORICAL-REPEAT",
        "R2-DIRECT-VS-BATCH",
        "R3-FULL-VS-STEGVERSE-CONTEXT",
        "R4-GENERATION-VS-RECONSTRUCTION",
        "R5-REPEATED-TRIALS",
    ]
    doc.pop("blocked_until_r3_terminal", None)
    doc["remaining_evidence_gaps"] = [
        "fully burdened StegVerse compute, storage, verification, engineering, and maintenance cost",
        "provider invoice reconciliation",
        "successful quality-equivalent held-out context-management validation before any favorable context claim",
        "workload-weighted break-even and sensitivity analysis",
    ]
    doc["remaining_evidence_owner"] = {
        "issue": 13,
        "title": "SV-COST-CFO-EVIDENCE-003",
        "state": "BLOCKED_PENDING_NAMED_COST_SOURCES_AND_HELD_OUT_PROTOCOL",
    }
    doc["decision_receipt"] = "experiments/sv-cost-program/results/cfo-decision.json"
    for family in doc.get("families", []):
        if family.get("id") == "r3-full-vs-managed-context":
            family.update({
                "status": "TERMINAL_ADJUDICATED",
                "generation": r3["execution"]["generation"],
                "verdict": r3["verdict"],
                "run_id": r3["execution"]["run_id"],
                "adjudication": "experiments/sv-cost-program/results/r3-adjudication.json",
                "boundary": r3["publication_gate"]["claim_boundary"],
            })
        if family.get("id") == "normalized-three-platform":
            family.update({
                "status": "TERMINAL_ADJUDICATED_DIFFERENT_OPERATION",
                "verdict": r4["verdict"],
                "adjudication": "experiments/sv-cost-program/results/r4-adjudication.json",
                "boundary": r4["publication_gate"]["claim_boundary"],
            })
    doc["reliability_receipt"] = "experiments/sv-cost-program/results/r5-reliability-synthesis.json"
    doc["total_paired_trials_across_distinct_relations"] = r5["total_paired_trials_across_distinct_relations"]
    doc["cfo_decision"] = cfo["decision"]
    dump(path, doc)


def update_lineage(r3, r4, r5, cfo) -> None:
    path = PROGRAM / "lineage.json"
    doc = load(path)
    doc["status"] = "RELATIONAL_PROGRAM_EXECUTED_DECISION_READY_BOUNDED_CLAIMS"
    nodes = {node["id"]: node for node in doc.get("nodes", [])}
    r3_node = nodes["R3-FULL-VS-STEGVERSE-CONTEXT"]
    r3_node.update({
        "state": "R3_ADJUDICATED",
        "generation": r3["execution"]["generation"],
        "verdict": r3["verdict"],
        "run": {
            "id": r3["execution"]["run_id"],
            "attempt": 1,
            "head_sha": r3["execution"]["head_sha"],
            "artifact_id": R3_ARTIFACT_ID,
            "artifact_digest": R3_ARTIFACT_DIGEST,
        },
        "boundary": r3["publication_gate"]["claim_boundary"],
    })
    r3_node["artifacts"] = [
        "experiments/sv-cost-program/r3-full-vs-managed/governance.json",
        "experiments/sv-cost-program/r3-full-vs-managed/protocol.json",
        "experiments/sv-cost-program/r3-full-vs-managed/run.py",
        "experiments/sv-cost-program/r3-full-vs-managed/results/result.json",
        "experiments/sv-cost-program/results/r3-adjudication.json",
        ".github/workflows/sv-cost-r3-full-vs-managed.yml",
        ".github/workflows/sv-cost-r3-controller-v2.yml",
    ]
    r3_node["commits"].update({
        "observed_evidence": R3_EVIDENCE_COMMIT,
        "adjudication": R3_ADJUDICATION_COMMIT,
    })
    r3_node.pop("required_terminal_artifacts", None)

    r4_node = nodes["R4-GENERATION-VS-RECONSTRUCTION"]
    r4_node.update({
        "state": r4["status"],
        "verdict": r4["verdict"],
        "boundary": r4["publication_gate"]["claim_boundary"],
        "adjudication": "experiments/sv-cost-program/results/r4-adjudication.json",
        "finalizer_commit": FINALIZER_COMMIT,
    })
    if "experiments/sv-cost-program/results/r4-adjudication.json" not in r4_node["artifacts"]:
        r4_node["artifacts"].append("experiments/sv-cost-program/results/r4-adjudication.json")

    nodes["R5-REPEATED-TRIALS"] = {
        "id": "R5-REPEATED-TRIALS",
        "state": r5["status"],
        "operation_class": "cross_relation_reliability_synthesis",
        "artifacts": [
            "experiments/sv-cost-program/results/r2-adjudication.json",
            "experiments/sv-cost-program/results/r3-adjudication.json",
            "experiments/sv-cost-program/results/r5-reliability-synthesis.json",
        ],
        "total_paired_trials_across_distinct_relations": r5["total_paired_trials_across_distinct_relations"],
        "pooled_effect_admissible": r5["pooled_effect_admissible"],
        "boundary": r5["claim_boundary"],
        "finalizer_commit": FINALIZER_COMMIT,
    }
    nodes["CFO-DECISION"] = {
        "id": "CFO-DECISION",
        "state": cfo["status"],
        "decision": cfo["decision"],
        "artifact": "experiments/sv-cost-program/results/cfo-decision.json",
        "canonical_analysis": cfo["canonical_analysis"],
        "boundary": cfo["claim_boundary"],
        "remaining_owner": "issue #13",
        "finalizer_commit": FINALIZER_COMMIT,
    }
    ordered_ids = [
        "CONTROL-SURFACES",
        "R1-HISTORICAL-REPEAT",
        "R2-DIRECT-VS-BATCH",
        "R3-FULL-VS-STEGVERSE-CONTEXT",
        "R4-GENERATION-VS-RECONSTRUCTION",
        "R5-REPEATED-TRIALS",
        "CFO-DECISION",
    ]
    doc["nodes"] = [nodes[item] for item in ordered_ids]
    doc["unresolved"] = [
        "issue #13: fully burdened local cost",
        "issue #13: provider invoice reconciliation",
        "issue #13: successful quality-equivalent held-out validation before a favorable context claim",
        "issue #13: break-even and sensitivity analysis",
    ]
    doc["terminal_receipts"] = [
        "experiments/sv-cost-program/results/historical-lineage-observation.json",
        "experiments/sv-cost-program/results/r2-adjudication.json",
        "experiments/sv-cost-program/results/r3-adjudication.json",
        "experiments/sv-cost-program/results/r4-adjudication.json",
        "experiments/sv-cost-program/results/r5-reliability-synthesis.json",
        "experiments/sv-cost-program/results/cfo-decision.json",
    ]
    dump(path, doc)


def update_inventory(r3, r4, r5, cfo, release_session: bool, workflow_run_url: str) -> None:
    path = PROGRAM / "session-goal-inventory.json"
    doc = load(path)
    doc["updated_at"] = now_utc()
    goal_states = {
        "SESSION-GOAL-PRIMARY": "COMPLETE",
        "SESSION-GOAL-GOVERNANCE": "MERGED_INTO_CANONICAL_WORKSTREAM" if release_session else "CLAIMED_FOR_INTEGRATION",
        "SESSION-GOAL-AUTONOMY": "COMPLETE",
        "SESSION-GOAL-CONSOLIDATION": "MERGED_INTO_CANONICAL_WORKSTREAM" if release_session else "CLAIMED_FOR_INTEGRATION",
    }
    for goal in doc["session_goals"]:
        goal["state"] = goal_states[goal["goal_id"]]

    updates = {
        "SV-COST-001-CANONICAL-CONTROL-SURFACES": ("COMPLETE", "terminal_surfaces_reconciled", "validated_against_terminal_receipts", "canonical_terminal_program", "commit pending reconciliation workflow"),
        "SV-COST-004-R3-FULL-VS-MANAGED-CONTEXT": ("COMPLETE", "executed_and_generation_bound", "hosted_run_jobs_logs_artifact_and_receipt_validated", "terminal_adjudication_integrated", f"run {r3['execution']['run_id']}; commit {R3_EVIDENCE_COMMIT}; artifact {R3_ARTIFACT_ID}"),
        "SV-COST-005-R3-ADJUDICATION": ("COMPLETE", "terminal_adjudication_committed", "paired_statistics_and_publication_gate_validated", "canonical_surfaces_updated", f"commit {R3_ADJUDICATION_COMMIT}; verdict {r3['verdict']}"),
        "SV-COST-006-R4-RECONSTRUCTION-ECONOMICS": ("COMPLETE", "different_operation_adjudicated", "operation_boundary_and_local_cost_gap_validated", "terminal_receipt_integrated", f"commit {FINALIZER_COMMIT}; verdict {r4['verdict']}"),
        "SV-COST-007-R5-RELIABILITY-SYNTHESIS": ("COMPLETE", "cross_relation_reliability_synthesized", "15_paired_trials_and_non_pooling_boundary_validated", "terminal_receipt_integrated", f"commit {FINALIZER_COMMIT}; status {r5['status']}"),
        "SV-COST-008-CFO-DECISION": ("COMPLETE", "bounded_cfo_decision_committed", "decision_receipt_and_analysis_validated", "issue_13_owns_roi_evidence_gap", f"commit {FINALIZER_COMMIT}; decision {cfo['decision']}"),
        "SV-COST-009-GOVERNANCE-FORMALISM": ("COMPLETE", "committed_design_record", "required_concepts_cross_referenced", "merged_into_canonical_handoff", "docs/RECONSTRUCTABLE_STATE_TRANSITION_GOVERNANCE.md"),
        "SV-COST-010-SESSION-HANDOFF-INVENTORY-CLAIMS": ("COMPLETE", "canonical_handoff_inventory_and_claims_committed", "repository_validator", "canonical_continuation_path", "SV_COST_MIRROR_HANDOFF.md"),
        "SV-COST-011-SESSION-CONSOLIDATION-AUTOMATION": (("COMPLETE" if release_session else "CLAIMED_FOR_IMPLEMENTATION"), ("hosted_validator_and_receipt_committed" if release_session else "installed_awaiting_hosted_receipt"), ("hosted_validation_passed" if release_session else "pending_hosted_validation"), ("merged_into_canonical_workstream" if release_session else "workflow_installed"), (workflow_run_url if release_session else ".github/workflows/sv-cost-session-consolidation.yml")),
        "SV-COST-012-DOWNSTREAM-PROPAGATION": ("BLOCKED", "publication_propagation_not_authorized_by_bounded_decision", "no_downstream_propagation_claimed", "issue_13_must_first_produce_revised_decision_if_favorable_publication_is_sought", "issue #13 and SV_COST_MIRROR_HANDOFF.md"),
    }
    for item in doc["items"]:
        if item["task_id"] in updates:
            state, completion, validation, integration, evidence = updates[item["task_id"]]
            item.update({
                "claim_state": state,
                "completion_state": completion,
                "validation_state": validation,
                "integration_state": integration,
                "evidence_location": evidence,
                "next_executable_action": (
                    "None for this session; issue #13 owns any future favorable ROI evidence revision."
                    if state == "COMPLETE"
                    else "Remain fail-closed until issue #13 produces a revised governed decision receipt."
                ),
            })
    terminal = {"COMPLETE", "SUPERSEDED", "MERGED_INTO_CANONICAL_WORKSTREAM"}
    doc["counts"] = {
        "required_deliverables": len(doc["items"]),
        "complete_or_terminal": sum(1 for item in doc["items"] if item["claim_state"] in terminal),
        "machine_owned_active": sum(1 for item in doc["items"] if item["claim_state"] == "MACHINE_OWNED"),
        "blocked_with_release_condition": sum(1 for item in doc["items"] if item["claim_state"] == "BLOCKED"),
        "claimed_for_session_consolidation": sum(1 for item in doc["items"] if item["claim_state"].startswith("CLAIMED_")),
        "missing_required_files": 0,
    }
    doc["archive_rule"] = "This session is archive-ready when the hosted consolidation receipt is ARCHIVE_READY and the chat-session claim is released. Remaining favorable ROI work is a separate durable issue #13 workstream."
    dump(path, doc)


def update_claims(r3, release_session: bool, workflow_run_url: str) -> None:
    path = PROGRAM / "task-claims.json"
    doc = load(path)
    timestamp = now_utc()
    doc["updated_at"] = timestamp
    completions = {
        "SV-COST-R3-EXECUTION": {"state": "COMPLETE", "released_at": "2026-08-03T16:19:18Z", "release_evidence": {"run_id": r3["execution"]["run_id"], "commit": R3_EVIDENCE_COMMIT, "artifact_id": R3_ARTIFACT_ID, "artifact_digest": R3_ARTIFACT_DIGEST}},
        "SV-COST-R3-ADJUDICATION": {"state": "COMPLETE", "released_at": "2026-08-03T16:19:34Z", "release_evidence": {"commit": R3_ADJUDICATION_COMMIT, "receipt": "experiments/sv-cost-program/results/r3-adjudication.json"}},
        "SV-COST-R4-R5-FINALIZE": {"state": "COMPLETE", "released_at": "2026-08-03T16:19:51Z", "release_evidence": {"commit": FINALIZER_COMMIT, "receipts": ["r4-adjudication.json", "r5-reliability-synthesis.json", "cfo-decision.json"]}},
    }
    for claim in doc["claims"]:
        if claim["task_id"] in completions:
            claim.update(completions[claim["task_id"]])
        if claim["task_id"] == "SV-COST-SESSION-CONSOLIDATE" and release_session:
            claim.update({
                "state": "MERGED_INTO_CANONICAL_WORKSTREAM",
                "released_at": timestamp,
                "release_evidence": {
                    "workflow_run": workflow_run_url,
                    "receipt": "experiments/sv-cost-program/results/session-consolidation-receipt.json",
                    "canonical_handoff": "SV_COST_MIRROR_HANDOFF.md",
                },
            })
        if claim["task_id"] == "SV-COST-CFO-EVIDENCE-003":
            claim["claimant"] = "issue-13-durable-evidence-workstream"
            claim["state"] = "BLOCKED"
            claim["release_condition"] = "Issue #13 records named cost sources, a versioned cost contract, executable meters, invoice references, and a successful quality-equivalent held-out protocol before a revised favorable decision is possible."
    dump(path, doc)


def build_analysis(r3, r4, r5, cfo) -> str:
    return f"""# StegVerse Cost and Capability Analysis

Status: **DECISION READY — BOUNDED CLAIMS — GENERAL SAVINGS CLAIM NOT APPROVED**

Governing program: `SV-COST-MAJOR-GOAL-001`  
Canonical issue: `#12`  
Remaining favorable-ROI evidence: issue `#13`

This is the sole human-facing synthesis. Individual files are subordinate evidence and do not create independent conclusions.

## Decision

**{cfo['decision']}**

The testing program is decision-ready because it supports a bounded decision, not because it proves a favorable ROI.

## Evidence classes

1. **Observed execution:** native provider or repository execution with retained receipts, hashes, run identity, and artifacts.
2. **Pricing-derived value:** cost calculated from retained usage and a versioned price card; not an invoice.
3. **Accounting transform:** arithmetic applied without a distinct execution receipt.
4. **Reconstruction:** reuse of admitted repository state; not equivalent fresh inference.

## R1 — Historical control-envelope reproduction

| Measure | Historical BL-001 | Repeat | Difference |
|---|---:|---:|---:|
| Native tokens | 4,169 | 4,239 | +70 / +1.68% |
| Pricing-derived cost | $0.061659 | $0.061869 | +$0.000210 / +0.34% |
| Latency | ~52.5 s | 59.59 s | +7.09 s |

Verdict: `OBSERVED_AND_VALIDATED_WITH_RECONSTRUCTION_BOUNDARY`.

The exact historical prompt and request payload were not retained. OP-002 remains an accounting replay rather than an observed historical optimized-route execution.

Receipt: `experiments/sv-cost-program/results/historical-lineage-observation.json`

## R2 — Direct synchronous versus native provider batch

| Measure | Direct | Batch |
|---|---:|---:|
| Paired trials | 10 | 10 |
| Mean tokens | 4,239 | 4,239 |
| Mean pricing-derived cost | $0.061869 | $0.0309345 |
| Mean latency | 64.63 s | 181.95 s |
| Completion rate | 0% | 0% |
| Verifier pass rate | 0% | 10% |

Verdict: `ROUTE_EFFECT_NOT_ADMISSIBLE_DUE_TO_QUALITY_OR_COMPLETION_DIVERGENCE`.

The native batch route and batch identifier were observed, but successful quality-equivalent outputs were not established. The 50% route-price effect is not an admissible successful-output savings claim.

Receipt: `experiments/sv-cost-program/results/r2-adjudication.json`

## R3 — Full context versus StegVerse-managed context

Run: `{r3['execution']['run_id']}`  
Generation: `{r3['execution']['generation']}`  
Paired trials: {r3['evidence']['paired_n']}

| Measure | Full context | Managed context |
|---|---:|---:|
| Mean input tokens | {r3['full']['mean_input_tokens']:.1f} | {r3['managed']['mean_input_tokens']:.1f} |
| Mean output tokens | {r3['full']['mean_output_tokens']:.1f} | {r3['managed']['mean_output_tokens']:.1f} |
| Mean pricing-derived cost | ${r3['full']['mean_cost_usd']:.6f} | ${r3['managed']['mean_cost_usd']:.6f} |
| Mean latency | {r3['full']['mean_latency_seconds']:.2f} s | {r3['managed']['mean_latency_seconds']:.2f} s |
| Full-path completion rate | {r3['full']['full_path_completion_rate']:.0%} | {r3['managed']['full_path_completion_rate']:.0%} |
| Successful-output rate | {r3['full']['successful_output_rate']:.0%} | {r3['managed']['successful_output_rate']:.0%} |

Paired managed-minus-full effects:

- Mean input-token delta: {r3['paired_effect']['mean_input_token_delta_managed_minus_full']:.1f}
- Input-token 95% CI: {r3['paired_effect']['input_token_delta_ci95']}
- Mean pricing-derived cost delta: ${r3['paired_effect']['mean_cost_delta_usd_managed_minus_full']:.6f}
- Cost 95% CI: {r3['paired_effect']['cost_delta_ci95']}
- Mean latency delta: {r3['paired_effect']['mean_latency_delta_seconds_managed_minus_full']:.2f} seconds
- Latency 95% CI: {r3['paired_effect']['latency_delta_ci95']}

Verdict: `{r3['verdict']}`.

Managed context substantially reduced observed input tokens in this locked workload, but neither lane produced successful outputs under the full completion and verifier gate. The cost interval crosses zero, quality diverged, and pricing-derived cost is not invoice evidence. No headline context-savings claim is admitted.

Receipt: `experiments/sv-cost-program/results/r3-adjudication.json`

## R4 — Fresh generation versus governed reconstruction

Verdict: `{r4['verdict']}`.

Reconstruction of already admitted work can avoid a new external provider-generation charge. It is a different operation from fresh inference. The observed external-provider avoidance scenarios were ${r4['external_provider_avoidance_scenarios_usd_per_reconstruction']['instead_of_openai_generation']:.5f} versus the retained OpenAI generation and ${r4['external_provider_avoidance_scenarios_usd_per_reconstruction']['instead_of_anthropic_generation']:.5f} versus the retained Anthropic generation.

Net savings and fully burdened ROI remain unproven because StegVerse local compute, storage, verification, engineering, and maintenance costs are unmeasured.

Receipt: `experiments/sv-cost-program/results/r4-adjudication.json`

## R5 — Reliability

Status: `{r5['status']}`.

The program retains {r5['total_paired_trials_across_distinct_relations']} paired trials across R2 and R3. These relations estimate different causal effects and are not pooled into one savings percentage. Failures, retries, confidence intervals, and quality gates remain part of the result.

Receipt: `experiments/sv-cost-program/results/r5-reliability-synthesis.json`

## CFO findings

- Historical control envelope reproduced: `{str(cfo['findings']['historical_control_envelope_reproduced']).lower()}`
- Successful route savings established: `{str(cfo['findings']['successful_route_savings_established']).lower()}`
- Successful managed-context savings established: `{str(cfo['findings']['successful_managed_context_savings_established']).lower()}`
- External provider charge avoidance for admitted reconstruction established: `{str(cfo['findings']['external_provider_charge_avoidance_for_admitted_reconstruction_established']).lower()}`
- Net reconstruction savings established: `{str(cfo['findings']['net_reconstruction_savings_established']).lower()}`

## Required before favorable ROI approval

1. Measure StegVerse compute, storage, verification, engineering, and maintenance cost.
2. Reconcile pricing-derived provider costs to invoices.
3. Execute a successful quality-equivalent held-out context-management test before any favorable context claim.
4. Calculate workload-weighted break-even and sensitivity ranges.

Durable owner: issue `#13`.

## Reproduction and audit paths

- Evidence index: `experiments/sv-cost-program/evidence-index.json`
- Program lineage: `experiments/sv-cost-program/lineage.json`
- Relational matrix: `experiments/sv-cost-program/relations.json`
- R3 immutable artifact: ID `{R3_ARTIFACT_ID}`, digest `{R3_ARTIFACT_DIGEST}`
- Machine-readable CFO receipt: `experiments/sv-cost-program/results/cfo-decision.json`
- Session and continuation handoff: `SV_COST_MIRROR_HANDOFF.md`

## Claim boundary

The completed program supports a bounded financial decision. It does not support a favorable general StegVerse savings or ROI claim. No downstream publication may remove the distinctions among observed execution, pricing-derived values, accounting transforms, and reconstruction.
"""


def build_handoff(r3, r4, r5, cfo, release_session: bool, workflow_run_url: str) -> str:
    session_state = "MERGED_INTO_CANONICAL_WORKSTREAM" if release_session else "CONSOLIDATION_VALIDATION_ACTIVE"
    return f"""# SV-COST Mirror Handoff

Status: **CANONICAL — TERMINAL BOUNDED DECISION — SESSION {session_state}**

## Active goal

- Goal ID: `SV-COST-MAJOR-GOAL-001`
- Originating session goal: complete and consolidate one lineage-backed relational cost and capability program understandable without inspecting hundreds of result files.
- Repository and branch: `GCAT-BCAT-Engine/workflows@main`
- Primary program state: `RELATIONAL_PROGRAM_EXECUTED_DECISION_READY_BOUNDED_CLAIMS`
- CFO decision: `{cfo['decision']}`
- Canonical issue: `#12` (terminal program record)
- Adjacent evidence issue: `#13` (fully burdened cost, invoice reconciliation, held-out validation, and break-even evidence)

## Authoritative files

1. `SV_COST_MIRROR_HANDOFF.md`
2. `experiments/sv-cost-program/session-goal-inventory.json`
3. `experiments/sv-cost-program/task-claims.json`
4. `experiments/sv-cost-program/evidence-index.json`
5. `experiments/sv-cost-program/lineage.json`
6. `experiments/sv-cost-program/relations.json`
7. `experiments/sv-cost-program/results/`
8. `docs/SV_COST_MAJOR_ANALYSIS.md`
9. `docs/RECONSTRUCTABLE_STATE_TRANSITION_GOVERNANCE.md`
10. `experiments/sv-cost-program/results/session-consolidation-receipt.json`

Live Git state, workflow jobs and logs, immutable artifacts, provider receipts, and committed adjudications override prior chat statements.

## Canonical ownership and claims

- R1 historical lineage: `COMPLETE`; receipt `historical-lineage-observation.json`.
- R2 direct versus batch: `COMPLETE`; receipt `r2-adjudication.json`.
- R3 full versus managed context: `COMPLETE`; run `{r3['execution']['run_id']}`, evidence commit `{R3_EVIDENCE_COMMIT}`, artifact `{R3_ARTIFACT_ID}`, adjudication `{R3_ADJUDICATION_COMMIT}`.
- R4 reconstruction economics: `COMPLETE`; receipt `r4-adjudication.json`.
- R5 reliability synthesis: `COMPLETE`; receipt `r5-reliability-synthesis.json`.
- CFO bounded decision: `COMPLETE`; commit `{FINALIZER_COMMIT}`, receipt `cfo-decision.json`.
- Favorable ROI evidence: `BLOCKED`, durable owner issue `#13`.
- Chat-session consolidation: `{session_state}`; hosted evidence `{workflow_run_url}`.

No active implementation claim remains on R1–R5. The defective R3 controller remains superseded and must not be restored.

## Completed work

- R1–R5 executed or adjudicated under explicit operation-class and publication boundaries.
- R3 hosted run, every job step, logs, provider receipts, result hashes, and immutable artifact were inspected.
- One canonical analysis and machine-readable CFO decision were committed.
- Governance as reconstructable successor-state determination was transferred to `docs/RECONSTRUCTABLE_STATE_TRANSITION_GOVERNANCE.md`.
- Session inventory, collision-controlled claims, validator, and hosted consolidation workflow were installed.

## Incomplete work

Only a future favorable ROI revision remains incomplete:

1. meter fully burdened StegVerse local cost;
2. reconcile provider charges to invoices;
3. produce a successful quality-equivalent held-out context-management result before any favorable context claim;
4. calculate workload-weighted break-even and sensitivity ranges.

All four are durably owned by issue `#13`. They do not invalidate the current bounded CFO decision.

## Exact next tasks

- `SV-COST-CFO-EVIDENCE-003`: issue `#13`; install versioned cost contracts and meters under `experiments/sv-cost-program/cost-model/`, then emit `results/cfo-cost-evidence.json`.
- Any revised decision must update `cfo-decision.json`, the evidence index, lineage, relations, and the canonical analysis through a governed workflow.
- Downstream publication remains fail-closed until the destination repository handoff is inspected and a publication contract preserves the bounded decision.

## Blockers

- Favorable ROI revision blocker: no versioned local-cost sources, invoices, successful held-out equivalence, or break-even model.
- Machine-observable release condition: issue `#13` produces `experiments/sv-cost-program/results/cfo-cost-evidence.json` with inspectable sources and a governed revised decision receipt.

## Cross-repository dependencies

No propagation to `StegVerse-Labs/Site`, `GCAT-BCAT-Engine/Publisher`, `admissibility-wiki`, `stegguardian-wiki`, or `master-records` is claimed. The current decision is bounded and negative with respect to a general savings claim. Before any propagation, the destination's newest `*_MIRROR_HANDOFF.md` and import/publication contract must be inspected. A future propagator must preserve the decision and claim boundaries rather than publish a favorable savings headline.

## Validation commands

```bash
python -m json.tool experiments/sv-cost-program/session-goal-inventory.json
python -m json.tool experiments/sv-cost-program/task-claims.json
python -m json.tool experiments/sv-cost-program/evidence-index.json
python -m json.tool experiments/sv-cost-program/lineage.json
python -m json.tool experiments/sv-cost-program/relations.json
python -m json.tool experiments/sv-cost-program/results/cfo-decision.json
python tools/reconcile_sv_cost_terminal_state.py
python tools/validate_sv_cost_session_state.py
```

Hosted validation: `.github/workflows/sv-cost-session-consolidation.yml`.

## Session-specific requirements transferred

- one relational program and one synthesis;
- exact historical reconstruction boundaries;
- native receipts, usage, hashes, trials, failures, variance, and confidence intervals;
- strict separation of generation, pricing derivation, accounting transforms, and reconstruction;
- governance as successor-state determination from reconstructable prior-state identity;
- reconstruction singularity, unique advancing successor, continuity, and false-discretion collapse;
- repository-native continuation with expiring claims, collision boundaries, receipts, and fail-closed blocked states.

MERGED INTO: `GCAT-BCAT-Engine/workflows/SV_COST_MIRROR_HANDOFF.md`, terminal issue `#12`, durable evidence issue `#13`, and the canonical files listed above.

## Supersession and convergence

- Prior chat status reports are superseded by this handoff and committed receipts.
- The R3 v1 controller is superseded.
- R1–R5 claims are released as complete.
- No separate “Cost Analysis 2” workstream is authorized.
- Issue `#13` is the only canonical continuation for a future favorable ROI revision.

## Archive conditions

This chat is archive-ready when the hosted consolidation receipt reports `ARCHIVE_READY`, the chat-session claim is released, no stale or conflicting claim exists, and deleting the chat would not remove unique state or authority. R1–R5 are terminal. Issue `#13` is independent durable continuation and does not require this chat.

## Percentages

Denominator: 12 required session deliverables in `session-goal-inventory.json`.

- Task completion: 11/12 terminal; the twelfth is intentionally `BLOCKED` and transferred to issue `#13`.
- Developed files: 12/12.
- Validation: 15/15 repository checks plus hosted R3 job/log/artifact inspection.
- Integration: 8/8 canonical control-surface links.
- Goal activation: 4/4 session goals terminal or transferred.
- Session consolidation: {'4/4 and claim released' if release_session else '3/4; hosted receipt and claim release pending'}.
"""


def main() -> int:
    args = parse_args()
    r3 = load(RESULTS / "r3-adjudication.json")
    r4 = load(RESULTS / "r4-adjudication.json")
    r5 = load(RESULTS / "r5-reliability-synthesis.json")
    cfo = load(RESULTS / "cfo-decision.json")
    assert r3["status"] == "R3_ADJUDICATED"
    assert r4["status"] == "R4_ADJUDICATED_DIFFERENT_OPERATION"
    assert r5["status"] == "R5_ADJUDICATED_CROSS_RELATION_RELIABILITY"
    assert cfo["status"] == "DECISION_READY_WITH_BOUNDED_CLAIMS"
    update_evidence_index(r3, r4, r5, cfo)
    update_lineage(r3, r4, r5, cfo)
    update_inventory(r3, r4, r5, cfo, args.release_session, args.workflow_run_url)
    update_claims(r3, args.release_session, args.workflow_run_url)
    (ROOT / "docs/SV_COST_MAJOR_ANALYSIS.md").write_text(build_analysis(r3, r4, r5, cfo))
    (ROOT / "SV_COST_MIRROR_HANDOFF.md").write_text(build_handoff(r3, r4, r5, cfo, args.release_session, args.workflow_run_url))
    print(json.dumps({
        "status": "RECONCILED",
        "release_session": args.release_session,
        "r3_verdict": r3["verdict"],
        "cfo_decision": cfo["decision"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
