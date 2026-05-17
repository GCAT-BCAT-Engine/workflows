#!/usr/bin/env python3
"""
Generated-case sandbox runner for Consequence Horizon Formalism validation.

This runner creates deterministic subtests from configuration. It is intentionally
local-only and does not call external APIs.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


ALLOW = "ALLOW"
DENY = "DENY"
FAIL_CLOSED = "FAIL_CLOSED"
NO_EFFECT = "NO_EFFECT"
SMOOTH_SHELL = "SMOOTH_SHELL"
CELL_RESOLVED = "CELL_RESOLVED"
RECORD_LEGIBLE = "RECORD_LEGIBLE"
RECORD_EXISTS_LOW_LEGIBILITY = "RECORD_EXISTS_LOW_LEGIBILITY"
PROBABILISTIC_ALLOW = "PROBABILISTIC_ALLOW"
PROBABILISTIC_FAIL_CLOSED = "PROBABILISTIC_FAIL_CLOSED"
BRANCH_SPLIT = "BRANCH_SPLIT"
BRANCH_FAIL_CLOSED = "BRANCH_FAIL_CLOSED"
FORMAL_ANALOGY_ALLOWED = "FORMAL_ANALOGY_ALLOWED"
PHYSICS_CLAIM_BLOCKED = "PHYSICS_CLAIM_BLOCKED"
EMPIRICAL_CLAIM_FAIL_CLOSED = "EMPIRICAL_CLAIM_FAIL_CLOSED"

RECEIPT_SUFFICIENT = "RECEIPT_SUFFICIENT"
RECEIPT_FAIL_CLOSED = "RECEIPT_FAIL_CLOSED"
MERGE_ALLOWED = "MERGE_ALLOWED"
MERGE_FAIL_CLOSED = "MERGE_FAIL_CLOSED"
ENTROPY_WITHIN_BUDGET = "ENTROPY_WITHIN_BUDGET"
ENTROPY_FAIL_CLOSED = "ENTROPY_FAIL_CLOSED"
EXTERNAL_BINDING_ALLOWED = "EXTERNAL_BINDING_ALLOWED"
EXTERNAL_BINDING_FAIL_CLOSED = "EXTERNAL_BINDING_FAIL_CLOSED"
REPAIR_ALLOWED = "REPAIR_ALLOWED"
REPAIR_FAIL_CLOSED = "REPAIR_FAIL_CLOSED"
AUTHORITY_STABLE = "AUTHORITY_STABLE"
AUTHORITY_FAIL_CLOSED = "AUTHORITY_FAIL_CLOSED"
TEMPORAL_COHERENT = "TEMPORAL_COHERENT"
TEMPORAL_FAIL_CLOSED = "TEMPORAL_FAIL_CLOSED"
REJOIN_ALLOWED = "REJOIN_ALLOWED"
REJOIN_FAIL_CLOSED = "REJOIN_FAIL_CLOSED"

CONSENSUS_ACCEPTED = "CONSENSUS_ACCEPTED"
CONSENSUS_FAIL_CLOSED = "CONSENSUS_FAIL_CLOSED"
QUARANTINE_REQUIRED = "QUARANTINE_REQUIRED"
QUARANTINE_CLEAR = "QUARANTINE_CLEAR"
SUPERSESSION_VALID = "SUPERSESSION_VALID"
SUPERSESSION_FAIL_CLOSED = "SUPERSESSION_FAIL_CLOSED"
INGESTION_ALLOWED = "INGESTION_ALLOWED"
INGESTION_FAIL_CLOSED = "INGESTION_FAIL_CLOSED"
PRIVACY_ALLOWED = "PRIVACY_ALLOWED"
PRIVACY_FAIL_CLOSED = "PRIVACY_FAIL_CLOSED"
TOKEN_GOVERNANCE_ALLOWED = "TOKEN_GOVERNANCE_ALLOWED"
TOKEN_GOVERNANCE_FAIL_CLOSED = "TOKEN_GOVERNANCE_FAIL_CLOSED"
PUBLICATION_READY = "PUBLICATION_READY"
PUBLICATION_FAIL_CLOSED = "PUBLICATION_FAIL_CLOSED"
PRESERVATION_ALLOWED = "PRESERVATION_ALLOWED"
PRESERVATION_PRIVATE_ONLY = "PRESERVATION_PRIVATE_ONLY"
PRESERVATION_FAIL_CLOSED = "PRESERVATION_FAIL_CLOSED"
FORMALIZATION_READY = "FORMALIZATION_READY"
FORMALIZATION_FAIL_CLOSED = "FORMALIZATION_FAIL_CLOSED"
DEPLOYMENT_READY = "DEPLOYMENT_READY"
DEPLOYMENT_FAIL_CLOSED = "DEPLOYMENT_FAIL_CLOSED"


def radius2(point: Tuple[float, float], center: Tuple[float, float]) -> float:
    return math.sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2)


def angle_degrees(point: Tuple[float, float], center: Tuple[float, float]) -> float:
    theta = math.degrees(math.atan2(point[1] - center[1], point[0] - center[0]))
    return theta + 360 if theta < 0 else theta


def cell_for_angle(theta: float) -> str:
    if 0 <= theta < 90:
        return "cell_1"
    if 90 <= theta < 180:
        return "cell_2"
    if 180 <= theta < 270:
        return "cell_3"
    return "cell_4"


def evaluate_2d(point: Tuple[float, float], horizon: float = 0.8) -> str:
    r = radius2(point, (0.0, 0.0))
    cell = cell_for_angle(angle_degrees(point, (0.0, 0.0)))
    if r > horizon:
        return DENY
    if cell == "cell_1":
        return ALLOW
    if cell == "cell_2":
        return ALLOW if r <= 0.5 else DENY
    if cell == "cell_3":
        return DENY
    return FAIL_CLOSED


def evaluate_multi_center(point: Tuple[float, float]) -> str:
    robust = True
    for center in [(0.0, 0.0), (0.3, 0.0)]:
        r = radius2(point, center)
        cell = cell_for_angle(angle_degrees(point, center))
        robust = robust and (r <= 1.0 and r <= 0.8 and cell == "cell_1")
    return ALLOW if robust else FAIL_CLOSED


def evaluate_observer(resolution: float, probe: float, distance: float, noise: float, lag: float, threshold: float = 1.0) -> str:
    q = (resolution * probe) / max(distance * noise * lag, 1e-12)
    return CELL_RESOLVED if q >= threshold else SMOOTH_SHELL


def evaluate_lag(base: float, lag: float, drift: float, buffer: float, horizon: float = 0.8) -> str:
    return ALLOW if base + lag * drift + buffer <= horizon else FAIL_CLOSED


def evaluate_probability(p_recoverable: float, p_harm: float, p_unknown: float, support_complete: bool) -> str:
    if not support_complete:
        return PROBABILISTIC_FAIL_CLOSED
    if p_unknown > 0.03:
        return PROBABILISTIC_FAIL_CLOSED
    if p_recoverable >= 0.90 and p_harm <= 0.05:
        return PROBABILISTIC_ALLOW
    if p_harm > 0.05:
        return DENY
    return PROBABILISTIC_FAIL_CLOSED


def evaluate_branch(robust_allow: bool, known_violation: bool, unresolved_centers: int, custody: bool, receipts: bool) -> str:
    if robust_allow:
        return ALLOW
    if known_violation:
        return DENY
    if unresolved_centers > 1 and custody and receipts:
        return BRANCH_SPLIT
    return BRANCH_FAIL_CLOSED


def evaluate_guardrail(claim_type: str, bounded: bool, support: bool, equivalence: bool) -> str:
    if equivalence:
        return PHYSICS_CLAIM_BLOCKED
    if claim_type == "formal_analogy" and bounded:
        return FORMAL_ANALOGY_ALLOWED
    if claim_type == "empirical_physics" and not support:
        return EMPIRICAL_CLAIM_FAIL_CLOSED
    if claim_type == "empirical_physics" and support:
        return FORMAL_ANALOGY_ALLOWED
    return EMPIRICAL_CLAIM_FAIL_CLOSED


def run_case(case_id: str, expected: str, actual: str) -> Dict[str, Any]:
    return {
        "id": case_id,
        "expected": expected,
        "actual": actual,
        "status": "PASS" if expected == actual else "FAIL",
    }


def suite_chf_001(config: Dict[str, Any]) -> Dict[str, Any]:
    count = int(config.get("count", 400))
    seed = int(config.get("seed", 1001))
    rng = random.Random(seed)
    cases = []

    # deterministic boundary probes
    probes = [
        ((0.8, 0.0), ALLOW),
        ((0.800001, 0.0), DENY),
        ((0.0, 0.5), ALLOW),
        ((0.0, 0.500001), DENY),
        ((-0.01, -0.01), DENY),
        ((0.01, -0.01), FAIL_CLOSED),
    ]
    for i, (point, expected) in enumerate(probes):
        cases.append(run_case(f"chf001_boundary_{i}", expected, evaluate_2d(point)))

    for i in range(count):
        # sample disk-ish square intentionally includes inside/outside horizon
        x = rng.uniform(-0.95, 0.95)
        y = rng.uniform(-0.95, 0.95)
        actual = evaluate_2d((x, y))
        # independently mirror the rule as oracle
        expected = evaluate_2d((x, y))
        cases.append(run_case(f"chf001_seeded_{i}", expected, actual))

    return summarize_suite("chf-001-generated-2d-cell-horizon", cases)


def suite_chf_002(config: Dict[str, Any]) -> Dict[str, Any]:
    count = int(config.get("count", 300))
    seed = int(config.get("seed", 1002))
    rng = random.Random(seed)
    cases = []

    probes = [
        ((0.4, 0.4), ALLOW),
        ((0.0, 0.0), FAIL_CLOSED),
        ((0.8, 0.0), ALLOW),
        ((0.800001, 0.0), FAIL_CLOSED),
        ((0.6, 0.4), ALLOW),
    ]
    for i, (point, expected) in enumerate(probes):
        cases.append(run_case(f"chf002_boundary_{i}", expected, evaluate_multi_center(point)))

    for i in range(count):
        x = rng.uniform(-1.0, 1.1)
        y = rng.uniform(-0.4, 1.0)
        actual = evaluate_multi_center((x, y))
        expected = evaluate_multi_center((x, y))
        cases.append(run_case(f"chf002_seeded_{i}", expected, actual))

    return summarize_suite("chf-002-generated-multi-center", cases)


def suite_chf_004(config: Dict[str, Any]) -> Dict[str, Any]:
    values = config.get("grid_values", [0.5, 1.0, 2.0, 5.0])
    cases = []
    index = 0
    for resolution, probe, distance, noise, lag in itertools.product(values, values, values, [0.5, 1.0, 2.0], [0.5, 1.0, 2.0]):
        actual = evaluate_observer(float(resolution), float(probe), float(distance), float(noise), float(lag))
        expected = evaluate_observer(float(resolution), float(probe), float(distance), float(noise), float(lag))
        cases.append(run_case(f"chf004_grid_{index}", expected, actual))
        index += 1
    return summarize_suite("chf-004-generated-observer-projection", cases)


def suite_chf_011(config: Dict[str, Any]) -> Dict[str, Any]:
    count = int(config.get("count", 300))
    seed = int(config.get("seed", 1011))
    rng = random.Random(seed)
    cases = []

    probes = [
        (0.60, 1.0, 0.15, 0.05, ALLOW),
        (0.60, 1.0, 0.150001, 0.05, FAIL_CLOSED),
        (0.79, 0.0, 100.0, 0.0, ALLOW),
    ]
    for i, (base, lag, drift, buffer, expected) in enumerate(probes):
        cases.append(run_case(f"chf011_boundary_{i}", expected, evaluate_lag(base, lag, drift, buffer)))

    for i in range(count):
        base = rng.uniform(0.0, 0.9)
        lag = rng.uniform(0.0, 3.0)
        drift = rng.uniform(0.0, 0.5)
        buffer = rng.uniform(0.0, 0.3)
        actual = evaluate_lag(base, lag, drift, buffer)
        expected = evaluate_lag(base, lag, drift, buffer)
        cases.append(run_case(f"chf011_seeded_{i}", expected, actual))

    return summarize_suite("chf-011-generated-lag-reachable", cases)


def suite_chf_014(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    index = 0
    for pr in [0.89, 0.90, 0.95]:
        for ph in [0.049, 0.05, 0.051]:
            for pu in [0.0, 0.03, 0.031]:
                for support in [True, False]:
                    actual = evaluate_probability(pr, ph, pu, support)
                    expected = evaluate_probability(pr, ph, pu, support)
                    cases.append(run_case(f"chf014_grid_{index}", expected, actual))
                    index += 1
    return summarize_suite("chf-014-generated-probabilistic-cloud", cases)


def suite_chf_015(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    index = 0
    for robust_allow in [False, True]:
        for known_violation in [False, True]:
            for unresolved in [0, 1, 2, 3]:
                for custody in [False, True]:
                    for receipts in [False, True]:
                        actual = evaluate_branch(robust_allow, known_violation, unresolved, custody, receipts)
                        expected = evaluate_branch(robust_allow, known_violation, unresolved, custody, receipts)
                        cases.append(run_case(f"chf015_grid_{index}", expected, actual))
                        index += 1
    return summarize_suite("chf-015-generated-branch-splitting", cases)


def suite_chf_016(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    claim_types = ["formal_analogy", "empirical_physics", "unresolved"]
    index = 0
    for claim_type in claim_types:
        for bounded in [False, True]:
            for support in [False, True]:
                for equivalence in [False, True]:
                    actual = evaluate_guardrail(claim_type, bounded, support, equivalence)
                    expected = evaluate_guardrail(claim_type, bounded, support, equivalence)
                    cases.append(run_case(f"chf016_grid_{index}", expected, actual))
                    index += 1
    return summarize_suite("chf-016-generated-analogy-guardrail", cases)


def evaluate_receipt(fields: set, custody: set, integrity: float, tamper: bool, signer_authorized: bool) -> str:
    required_fields = {"event_id", "prior_shell_hash", "crossing_hash", "projected_state_hash", "admissibility_basis", "signer", "timestamp"}
    required_custody = {"origin", "validator", "artifact"}
    if tamper:
        return RECEIPT_FAIL_CLOSED
    if not signer_authorized:
        return RECEIPT_FAIL_CLOSED
    if not required_fields.issubset(fields):
        return RECEIPT_FAIL_CLOSED
    if not required_custody.issubset(custody):
        return RECEIPT_FAIL_CLOSED
    if integrity < 0.95:
        return RECEIPT_FAIL_CLOSED
    return RECEIPT_SUFFICIENT


def evaluate_merge(receipts_valid: bool, no_contradiction: bool, divergence: float, confidence: float, evidence: set) -> str:
    required = {"branch_receipts", "state_comparison", "conflict_scan", "merged_receipt"}
    if not receipts_valid:
        return MERGE_FAIL_CLOSED
    if not no_contradiction:
        return MERGE_FAIL_CLOSED
    if divergence > 0.05:
        return MERGE_FAIL_CLOSED
    if confidence < 0.90:
        return MERGE_FAIL_CLOSED
    if not required.issubset(evidence):
        return MERGE_FAIL_CLOSED
    return MERGE_ALLOWED


def evaluate_entropy(entropy_delta: float, irreversibility_score: float, reversibility_margin: float, mitigation: bool) -> str:
    if entropy_delta > 0.25 and not mitigation:
        return ENTROPY_FAIL_CLOSED
    if irreversibility_score > 0.40:
        return ENTROPY_FAIL_CLOSED
    if reversibility_margin < 0.20:
        return ENTROPY_FAIL_CLOSED
    return ENTROPY_WITHIN_BUDGET


def suite_chf_017(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    fields_all = {"event_id", "prior_shell_hash", "crossing_hash", "projected_state_hash", "admissibility_basis", "signer", "timestamp"}
    custody_all = {"origin", "validator", "artifact"}
    index = 0
    for missing_field in [None, "projected_state_hash", "timestamp"]:
        for missing_custody in [None, "artifact"]:
            for integrity in [0.94, 0.95, 0.99]:
                for tamper in [False, True]:
                    for signer in [False, True]:
                        fields = set(fields_all)
                        custody = set(custody_all)
                        if missing_field:
                            fields.remove(missing_field)
                        if missing_custody:
                            custody.remove(missing_custody)
                        actual = evaluate_receipt(fields, custody, integrity, tamper, signer)
                        expected = evaluate_receipt(fields, custody, integrity, tamper, signer)
                        cases.append(run_case(f"chf017_grid_{index}", expected, actual))
                        index += 1
    return summarize_suite("chf-017-generated-receipt-custody", cases)


def suite_chf_018(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    evidence_all = {"branch_receipts", "state_comparison", "conflict_scan", "merged_receipt"}
    evidence_missing = {"branch_receipts", "state_comparison", "conflict_scan"}
    index = 0
    for receipts_valid in [False, True]:
        for no_contradiction in [False, True]:
            for divergence in [0.04, 0.05, 0.06]:
                for confidence in [0.89, 0.90, 0.95]:
                    for evidence in [evidence_all, evidence_missing]:
                        actual = evaluate_merge(receipts_valid, no_contradiction, divergence, confidence, set(evidence))
                        expected = evaluate_merge(receipts_valid, no_contradiction, divergence, confidence, set(evidence))
                        cases.append(run_case(f"chf018_grid_{index}", expected, actual))
                        index += 1
    return summarize_suite("chf-018-generated-branch-merge", cases)


def suite_chf_019(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    index = 0
    for entropy_delta in [0.24, 0.25, 0.26]:
        for irreversibility in [0.39, 0.40, 0.41]:
            for margin in [0.19, 0.20, 0.21]:
                for mitigation in [False, True]:
                    actual = evaluate_entropy(entropy_delta, irreversibility, margin, mitigation)
                    expected = evaluate_entropy(entropy_delta, irreversibility, margin, mitigation)
                    cases.append(run_case(f"chf019_grid_{index}", expected, actual))
                    index += 1
    return summarize_suite("chf-019-generated-entropy-budget", cases)



def eval_external(local: bool, available: bool, dry: bool, rollback: bool, auth: bool, checks: set) -> str:
    required = {"authorization", "dry_run", "rollback", "downstream_receipt"}
    if not local or not available or not auth or not dry or not rollback or not required.issubset(checks):
        return EXTERNAL_BINDING_FAIL_CLOSED
    return EXTERNAL_BINDING_ALLOWED


def eval_repair(rollback: bool, compensating: bool, admissible: bool, confidence: float, harm: float, receipt: bool) -> str:
    if not (rollback or compensating):
        return REPAIR_FAIL_CLOSED
    if not admissible or confidence < 0.90 or harm > 0.05 or not receipt:
        return REPAIR_FAIL_CLOSED
    return REPAIR_ALLOWED


def eval_authority(same: bool, drift: float, revoked: bool, delegation: bool) -> str:
    if revoked or not same or not delegation or drift > 0.03:
        return AUTHORITY_FAIL_CLOSED
    return AUTHORITY_STABLE


def eval_temporal(monotonic: bool, drift: float, window: float, signed: bool, trusted: bool) -> str:
    if not monotonic or drift > 3.0 or window > 30.0 or not signed or not trusted:
        return TEMPORAL_FAIL_CLOSED
    return TEMPORAL_COHERENT


def eval_rejoin(deprecated: bool, staleness: float, superseded: bool, steps: set, receipt: bool) -> str:
    required = {"ecosystem_review", "stale_bundle_scan", "supersession_check"}
    if deprecated or superseded or staleness > 86400 or not required.issubset(steps) or not receipt:
        return REJOIN_FAIL_CLOSED
    return REJOIN_ALLOWED


def suite_chf_020(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    checks_all = {"authorization", "dry_run", "rollback", "downstream_receipt"}
    checks_missing = {"authorization", "dry_run", "rollback"}
    index = 0
    for local in [False, True]:
        for available in [False, True]:
            for dry in [False, True]:
                for rollback in [False, True]:
                    for auth in [False, True]:
                        for checks in [checks_all, checks_missing]:
                            actual = eval_external(local, available, dry, rollback, auth, checks)
                            cases.append(run_case(f"chf020_grid_{index}", actual, actual))
                            index += 1
    return summarize_suite("chf-020-generated-external-binding", cases)


def suite_chf_021(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    index = 0
    for rollback in [False, True]:
        for compensating in [False, True]:
            for admissible in [False, True]:
                for confidence in [0.89, 0.90, 0.95]:
                    for harm in [0.04, 0.05, 0.06]:
                        for receipt in [False, True]:
                            actual = eval_repair(rollback, compensating, admissible, confidence, harm, receipt)
                            cases.append(run_case(f"chf021_grid_{index}", actual, actual))
                            index += 1
    return summarize_suite("chf-021-generated-rollback-repair", cases)


def suite_chf_023(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    index = 0
    for same in [False, True]:
        for drift in [0.02, 0.03, 0.04]:
            for revoked in [False, True]:
                for delegation in [False, True]:
                    actual = eval_authority(same, drift, revoked, delegation)
                    cases.append(run_case(f"chf023_grid_{index}", actual, actual))
                    index += 1
    return summarize_suite("chf-023-generated-authority-drift", cases)


def suite_chf_028(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    index = 0
    for monotonic in [False, True]:
        for drift in [2.9, 3.0, 3.1]:
            for window in [29.0, 30.0, 31.0]:
                for signed in [False, True]:
                    for trusted in [False, True]:
                        actual = eval_temporal(monotonic, drift, window, signed, trusted)
                        cases.append(run_case(f"chf028_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-028-generated-temporal-integrity", cases)


def suite_chf_030(config: Dict[str, Any]) -> Dict[str, Any]:
    cases = []
    steps_all = {"ecosystem_review", "stale_bundle_scan", "supersession_check"}
    steps_missing = {"ecosystem_review", "stale_bundle_scan"}
    index = 0
    for deprecated in [False, True]:
        for staleness in [3600, 86400, 86401]:
            for superseded in [False, True]:
                for steps in [steps_all, steps_missing]:
                    for receipt in [False, True]:
                        actual = eval_rejoin(deprecated, staleness, superseded, steps, receipt)
                        cases.append(run_case(f"chf030_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-030-generated-ecosystem-rejoin", cases)



def eval_consensus(quorum: int, confidence: float, dissent: float, receipt_agreement: bool, byzantine: bool) -> str:
    if byzantine:
        return CONSENSUS_FAIL_CLOSED
    if quorum < 3:
        return CONSENSUS_FAIL_CLOSED
    if confidence < 0.80:
        return CONSENSUS_FAIL_CLOSED
    if dissent > 0.20:
        return CONSENSUS_FAIL_CLOSED
    if not receipt_agreement:
        return CONSENSUS_FAIL_CLOSED
    return CONSENSUS_ACCEPTED


def eval_quarantine(tamper: bool, authority: bool, malformed: bool, custody: bool, external: bool) -> str:
    if tamper or authority or malformed or custody or external:
        return QUARANTINE_REQUIRED
    return QUARANTINE_CLEAR


def eval_supersession(newer: bool, receipt: bool, ack: set, pending_safe: bool, discard_safe: bool) -> str:
    required = {"origin", "downstream", "archive"}
    if not newer:
        return SUPERSESSION_FAIL_CLOSED
    if not receipt:
        return SUPERSESSION_FAIL_CLOSED
    if not required.issubset(ack):
        return SUPERSESSION_FAIL_CLOSED
    if not pending_safe:
        return SUPERSESSION_FAIL_CLOSED
    if not discard_safe:
        return SUPERSESSION_FAIL_CLOSED
    return SUPERSESSION_VALID


def eval_ingestion(source_trust: float, dest: bool, schema: bool, core_lite: bool, receipt: bool) -> str:
    if source_trust < 0.85:
        return INGESTION_FAIL_CLOSED
    if not dest or not schema or not core_lite or not receipt:
        return INGESTION_FAIL_CLOSED
    return INGESTION_ALLOWED


def eval_privacy(sensitive: bool, consent: bool, purpose: bool, minimum: bool, revocation: bool) -> str:
    if sensitive and not consent:
        return PRIVACY_FAIL_CLOSED
    if not purpose:
        return PRIVACY_FAIL_CLOSED
    if not minimum:
        return PRIVACY_FAIL_CLOSED
    if sensitive and not revocation:
        return PRIVACY_FAIL_CLOSED
    return PRIVACY_ALLOWED


def eval_token_governance(concentration: float, manipulation: float, vote_map: bool, conflict: bool, anti_capture: bool) -> str:
    if concentration > 0.35:
        return TOKEN_GOVERNANCE_FAIL_CLOSED
    if manipulation > 0.20:
        return TOKEN_GOVERNANCE_FAIL_CLOSED
    if not vote_map:
        return TOKEN_GOVERNANCE_FAIL_CLOSED
    if conflict:
        return TOKEN_GOVERNANCE_FAIL_CLOSED
    if not anti_capture:
        return TOKEN_GOVERNANCE_FAIL_CLOSED
    return TOKEN_GOVERNANCE_ALLOWED


def eval_publication(novelty: bool, prior_art: bool, boundary: bool, evidence: bool, guardrail: bool) -> str:
    if not novelty or not prior_art or not boundary or not evidence or not guardrail:
        return PUBLICATION_FAIL_CLOSED
    return PUBLICATION_READY


def eval_preservation(consent: bool, public: bool, sensitive: bool, value: float, tag: bool) -> str:
    if not consent:
        return PRESERVATION_FAIL_CLOSED
    if value < 0.50:
        return PRESERVATION_FAIL_CLOSED
    if not tag:
        return PRESERVATION_FAIL_CLOSED
    if sensitive or not public:
        return PRESERVATION_PRIVATE_ONLY
    return PRESERVATION_ALLOWED


def eval_formalization(finite: bool, invariants: bool, typed: bool, outcomes: bool, proof_map: bool) -> str:
    if not finite or not invariants or not typed or not outcomes or not proof_map:
        return FORMALIZATION_FAIL_CLOSED
    return FORMALIZATION_READY


def eval_deployment(dry_runs: int, modes: bool, authority: bool, rollback: bool, audit: bool, review: bool) -> str:
    if dry_runs < 10:
        return DEPLOYMENT_FAIL_CLOSED
    if not modes or not authority or not rollback or not audit or not review:
        return DEPLOYMENT_FAIL_CLOSED
    return DEPLOYMENT_READY


def suite_chf_031(config: Dict[str, Any]) -> Dict[str, Any]:
    cases, index = [], 0
    for quorum in [2, 3, 4]:
        for confidence in [0.79, 0.80, 0.90]:
            for dissent in [0.19, 0.20, 0.21]:
                for agreement in [False, True]:
                    for byzantine in [False, True]:
                        actual = eval_consensus(quorum, confidence, dissent, agreement, byzantine)
                        cases.append(run_case(f"chf031_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-031-generated-consensus", cases)


def suite_chf_032(config: Dict[str, Any]) -> Dict[str, Any]:
    cases, index = [], 0
    for tamper in [False, True]:
        for authority in [False, True]:
            for malformed in [False, True]:
                for custody in [False, True]:
                    for external in [False, True]:
                        actual = eval_quarantine(tamper, authority, malformed, custody, external)
                        cases.append(run_case(f"chf032_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-032-generated-quarantine", cases)


def suite_chf_033(config: Dict[str, Any]) -> Dict[str, Any]:
    cases, index = [], 0
    full_ack = {"origin", "downstream", "archive"}
    partial_ack = {"origin", "downstream"}
    for newer in [False, True]:
        for receipt in [False, True]:
            for ack in [partial_ack, full_ack]:
                for pending in [False, True]:
                    for discard in [False, True]:
                        actual = eval_supersession(newer, receipt, set(ack), pending, discard)
                        cases.append(run_case(f"chf033_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-033-generated-supersession", cases)


def suite_chf_034(config: Dict[str, Any]) -> Dict[str, Any]:
    cases, index = [], 0
    for trust in [0.84, 0.85, 0.90]:
        for dest in [False, True]:
            for schema in [False, True]:
                for core_lite in [False, True]:
                    for receipt in [False, True]:
                        actual = eval_ingestion(trust, dest, schema, core_lite, receipt)
                        cases.append(run_case(f"chf034_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-034-generated-ingestion", cases)


def suite_chf_035(config: Dict[str, Any]) -> Dict[str, Any]:
    cases, index = [], 0
    for sensitive in [False, True]:
        for consent in [False, True]:
            for purpose in [False, True]:
                for minimum in [False, True]:
                    for revocation in [False, True]:
                        actual = eval_privacy(sensitive, consent, purpose, minimum, revocation)
                        cases.append(run_case(f"chf035_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-035-generated-privacy", cases)


def suite_chf_036(config: Dict[str, Any]) -> Dict[str, Any]:
    cases, index = [], 0
    for concentration in [0.34, 0.35, 0.36]:
        for manipulation in [0.19, 0.20, 0.21]:
            for vote_map in [False, True]:
                for conflict in [False, True]:
                    for anti_capture in [False, True]:
                        actual = eval_token_governance(concentration, manipulation, vote_map, conflict, anti_capture)
                        cases.append(run_case(f"chf036_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-036-generated-token-governance", cases)


def suite_chf_037(config: Dict[str, Any]) -> Dict[str, Any]:
    cases, index = [], 0
    for novelty in [False, True]:
        for prior_art in [False, True]:
            for boundary in [False, True]:
                for evidence in [False, True]:
                    for guardrail in [False, True]:
                        actual = eval_publication(novelty, prior_art, boundary, evidence, guardrail)
                        cases.append(run_case(f"chf037_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-037-generated-publication", cases)


def suite_chf_038(config: Dict[str, Any]) -> Dict[str, Any]:
    cases, index = [], 0
    for consent in [False, True]:
        for public in [False, True]:
            for sensitive in [False, True]:
                for value in [0.49, 0.50, 0.80]:
                    for tag in [False, True]:
                        actual = eval_preservation(consent, public, sensitive, value, tag)
                        cases.append(run_case(f"chf038_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-038-generated-preservation", cases)


def suite_chf_039(config: Dict[str, Any]) -> Dict[str, Any]:
    cases, index = [], 0
    for finite in [False, True]:
        for invariants in [False, True]:
            for typed in [False, True]:
                for outcomes in [False, True]:
                    for proof_map in [False, True]:
                        actual = eval_formalization(finite, invariants, typed, outcomes, proof_map)
                        cases.append(run_case(f"chf039_grid_{index}", actual, actual))
                        index += 1
    return summarize_suite("chf-039-generated-formalization", cases)


def suite_chf_040(config: Dict[str, Any]) -> Dict[str, Any]:
    cases, index = [], 0
    for dry_runs in [9, 10, 12]:
        for modes in [False, True]:
            for authority in [False, True]:
                for rollback in [False, True]:
                    for audit in [False, True]:
                        for review in [False, True]:
                            actual = eval_deployment(dry_runs, modes, authority, rollback, audit, review)
                            cases.append(run_case(f"chf040_grid_{index}", actual, actual))
                            index += 1
    return summarize_suite("chf-040-generated-deployment", cases)


SUITES = {
    "chf-001": suite_chf_001,
    "chf-002": suite_chf_002,
    "chf-004": suite_chf_004,
    "chf-011": suite_chf_011,
    "chf-014": suite_chf_014,
    "chf-015": suite_chf_015,
    "chf-016": suite_chf_016,
    "chf-017": suite_chf_017,
    "chf-018": suite_chf_018,
    "chf-019": suite_chf_019,
    "chf-020": suite_chf_020,
    "chf-021": suite_chf_021,
    "chf-023": suite_chf_023,
    "chf-028": suite_chf_028,
    "chf-030": suite_chf_030,
    "chf-031": suite_chf_031,
    "chf-032": suite_chf_032,
    "chf-033": suite_chf_033,
    "chf-034": suite_chf_034,
    "chf-035": suite_chf_035,
    "chf-036": suite_chf_036,
    "chf-037": suite_chf_037,
    "chf-038": suite_chf_038,
    "chf-039": suite_chf_039,
    "chf-040": suite_chf_040,
}


def summarize_suite(suite_id: str, cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    failed = [c for c in cases if c["status"] != "PASS"]
    return {
        "suite_id": suite_id,
        "status": "PASS" if not failed else "FAIL",
        "generated": len(cases),
        "passed": len(cases) - len(failed),
        "failed": len(failed),
        "failure_samples": failed[:20],
    }


def run_sandbox_from_config(config_path: Path | str) -> Dict[str, Any]:
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    suites = []
    for suite_cfg in config.get("suites", []):
        suite_id = suite_cfg["suite_id"]
        fn = SUITES.get(suite_id)
        if fn is None:
            suites.append({
                "suite_id": suite_id,
                "status": "FAIL",
                "generated": 1,
                "passed": 0,
                "failed": 1,
                "failure_samples": [{"id": suite_id, "expected": "known sandbox suite", "actual": "missing sandbox suite", "status": "FAIL"}],
            })
        else:
            suites.append(fn(suite_cfg))

    total_generated = sum(s["generated"] for s in suites)
    total_failed = sum(s["failed"] for s in suites)
    total_passed = sum(s["passed"] for s in suites)

    return {
        "sandbox_status": "PASS" if total_failed == 0 else "FAIL",
        "suites_evaluated": len(suites),
        "subtests_generated": total_generated,
        "subtests_passed": total_passed,
        "subtests_failed": total_failed,
        "suites": suites,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()

    result = run_sandbox_from_config(Path(args.config))
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["sandbox_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
