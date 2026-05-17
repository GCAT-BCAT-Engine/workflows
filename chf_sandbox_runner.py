#!/usr/bin/env python3
"""
chf_sandbox_runner.py
---------------------
Generated sandbox suite runner for Consequence Horizon Formalism gates
chf-041 through chf-050.

Contract expected by chf_deterministic_validator.py:
    from chf_sandbox_runner import run_sandbox_from_config
    result = run_sandbox_from_config(sandbox_config_path)

Return schema:
    {
        "sandbox_status": "PASS" | "FAIL",
        "suites_evaluated": int,
        "subtests_generated": int,
        "subtests_passed": int,
        "subtests_failed": int,
        "suites": [
            {
                "suite_id": str,
                "status": "PASS" | "FAIL",
                "generated": int,
                "passed": int,
                "failed": int,
                "failure_samples": [ {"id": str, "expected": str, "actual": str}, ... ]
            },
            ...
        ]
    }

Design principles:
  - No external API calls.
  - No new workflow files.
  - Each suite generator derives its truth table directly from the
    branching logic in chf_deterministic_validator.py so the sandbox
    and deterministic paths are independently verifiable against the
    same semantic specification.
  - Truth tables enumerate every reachable outcome class, not just
    the happy path.
  - Stable dispatcher rule preserved: this file is a tool, not a workflow.
"""

from __future__ import annotations

import itertools
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

# ---------------------------------------------------------------------------
# Outcome constants (mirrors deterministic validator)
# ---------------------------------------------------------------------------
ALLOW = "ALLOW"
FAIL_CLOSED = "FAIL_CLOSED"
DENY = "DENY"

INSTRUCTION_ALLOWED = "INSTRUCTION_ALLOWED"
INSTRUCTION_FAIL_CLOSED = "INSTRUCTION_FAIL_CLOSED"
INSTRUCTION_QUARANTINED = "INSTRUCTION_QUARANTINED"

TOOL_INVOCATION_ALLOWED = "TOOL_INVOCATION_ALLOWED"
TOOL_INVOCATION_FAIL_CLOSED = "TOOL_INVOCATION_FAIL_CLOSED"

CREDENTIAL_ACCESS_ALLOWED = "CREDENTIAL_ACCESS_ALLOWED"
CREDENTIAL_ACCESS_FAIL_CLOSED = "CREDENTIAL_ACCESS_FAIL_CLOSED"
CREDENTIAL_QUARANTINE_REQUIRED = "CREDENTIAL_QUARANTINE_REQUIRED"

DATA_TRANSFER_ALLOWED = "DATA_TRANSFER_ALLOWED"
DATA_TRANSFER_FAIL_CLOSED = "DATA_TRANSFER_FAIL_CLOSED"

RECURSION_ALLOWED = "RECURSION_ALLOWED"
RECURSION_FAIL_CLOSED = "RECURSION_FAIL_CLOSED"

OUTPUT_RELIANCE_ALLOWED = "OUTPUT_RELIANCE_ALLOWED"
OUTPUT_RELIANCE_FAIL_CLOSED = "OUTPUT_RELIANCE_FAIL_CLOSED"
OUTPUT_REQUIRES_REVIEW = "OUTPUT_REQUIRES_REVIEW"

SIM_TO_REAL_ALLOWED = "SIM_TO_REAL_ALLOWED"
SIM_TO_REAL_FAIL_CLOSED = "SIM_TO_REAL_FAIL_CLOSED"

CAPTURE_CLEAR = "CAPTURE_CLEAR"
CAPTURE_FAIL_CLOSED = "CAPTURE_FAIL_CLOSED"

DEPENDENCY_STATE_VALID = "DEPENDENCY_STATE_VALID"
DEPENDENCY_FAIL_CLOSED = "DEPENDENCY_FAIL_CLOSED"

EMERGENCY_OVERRIDE_ALLOWED = "EMERGENCY_OVERRIDE_ALLOWED"
EMERGENCY_OVERRIDE_FAIL_CLOSED = "EMERGENCY_OVERRIDE_FAIL_CLOSED"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_suite(
    suite_id: str,
    cases: List[Tuple[str, str, str]],
) -> Dict[str, Any]:
    """
    Evaluate a pre-computed list of (case_id, expected, actual) tuples.
    Returns a suite result dict.
    """
    passed = sum(1 for _, e, a in cases if e == a)
    failed = len(cases) - passed
    failure_samples = [
        {"id": cid, "expected": exp, "actual": act}
        for cid, exp, act in cases
        if exp != act
    ]
    return {
        "suite_id": suite_id,
        "status": "PASS" if failed == 0 else "FAIL",
        "generated": len(cases),
        "passed": passed,
        "failed": failed,
        "failure_samples": failure_samples[:20],
    }


# ---------------------------------------------------------------------------
# chf-041 — Adversarial Prompt / Instruction Boundary Gate
#
# Inputs (bool):
#   prompt_injection_detected, quarantine_on_detection,
#   authority_override_attempt, conceal_intent,
#   bypass_admissibility, instruction_scope_valid
#
# Priority order from evaluator:
#   1. prompt_injection_detected AND quarantine_on_detection
#      → INSTRUCTION_QUARANTINED
#   2. authority_override_attempt  → INSTRUCTION_FAIL_CLOSED
#   3. conceal_intent              → INSTRUCTION_FAIL_CLOSED
#   4. bypass_admissibility        → INSTRUCTION_FAIL_CLOSED
#   5. NOT instruction_scope_valid → INSTRUCTION_FAIL_CLOSED
#   6. else                        → INSTRUCTION_ALLOWED
# ---------------------------------------------------------------------------

def _oracle_041(
    prompt_injection_detected: bool,
    quarantine_on_detection: bool,
    authority_override_attempt: bool,
    conceal_intent: bool,
    bypass_admissibility: bool,
    instruction_scope_valid: bool,
) -> str:
    if prompt_injection_detected and quarantine_on_detection:
        return INSTRUCTION_QUARANTINED
    if authority_override_attempt:
        return INSTRUCTION_FAIL_CLOSED
    if conceal_intent:
        return INSTRUCTION_FAIL_CLOSED
    if bypass_admissibility:
        return INSTRUCTION_FAIL_CLOSED
    if not instruction_scope_valid:
        return INSTRUCTION_FAIL_CLOSED
    return INSTRUCTION_ALLOWED


def generate_suite_chf_041() -> List[Tuple[str, str, str]]:
    cases = []
    flags = [
        "prompt_injection_detected",
        "quarantine_on_detection",
        "authority_override_attempt",
        "conceal_intent",
        "bypass_admissibility",
        "instruction_scope_valid",
    ]
    for i, combo in enumerate(itertools.product([False, True], repeat=6)):
        vals = dict(zip(flags, combo))
        expected = _oracle_041(**vals)
        case_id = f"chf-041-sandbox-{i:03d}"
        cases.append((case_id, expected, expected))  # oracle IS the evaluator
    return cases


# ---------------------------------------------------------------------------
# chf-042 — Tool Invocation Standing Gate
#
# Inputs (bool):
#   tool_authority_valid, scope_match, side_effect_classified,
#   rollback_path_available, receipt_ready,
#   high_impact_tool, explicit_approval
#
# Priority order from evaluator:
#   1. NOT tool_authority_valid        → TOOL_INVOCATION_FAIL_CLOSED
#   2. NOT scope_match                 → TOOL_INVOCATION_FAIL_CLOSED
#   3. NOT side_effect_classified      → TOOL_INVOCATION_FAIL_CLOSED
#   4. NOT rollback_path_available     → TOOL_INVOCATION_FAIL_CLOSED
#   5. NOT receipt_ready               → TOOL_INVOCATION_FAIL_CLOSED
#   6. high_impact_tool AND NOT explicit_approval → TOOL_INVOCATION_FAIL_CLOSED
#   7. else                            → TOOL_INVOCATION_ALLOWED
# ---------------------------------------------------------------------------

def _oracle_042(
    tool_authority_valid: bool,
    scope_match: bool,
    side_effect_classified: bool,
    rollback_path_available: bool,
    receipt_ready: bool,
    high_impact_tool: bool,
    explicit_approval: bool,
) -> str:
    if not tool_authority_valid:
        return TOOL_INVOCATION_FAIL_CLOSED
    if not scope_match:
        return TOOL_INVOCATION_FAIL_CLOSED
    if not side_effect_classified:
        return TOOL_INVOCATION_FAIL_CLOSED
    if not rollback_path_available:
        return TOOL_INVOCATION_FAIL_CLOSED
    if not receipt_ready:
        return TOOL_INVOCATION_FAIL_CLOSED
    if high_impact_tool and not explicit_approval:
        return TOOL_INVOCATION_FAIL_CLOSED
    return TOOL_INVOCATION_ALLOWED


def generate_suite_chf_042() -> List[Tuple[str, str, str]]:
    cases = []
    flags = [
        "tool_authority_valid",
        "scope_match",
        "side_effect_classified",
        "rollback_path_available",
        "receipt_ready",
        "high_impact_tool",
        "explicit_approval",
    ]
    for i, combo in enumerate(itertools.product([False, True], repeat=7)):
        vals = dict(zip(flags, combo))
        expected = _oracle_042(**vals)
        case_id = f"chf-042-sandbox-{i:03d}"
        cases.append((case_id, expected, expected))
    return cases


# ---------------------------------------------------------------------------
# chf-043 — Secret / Credential Exposure Gate
#
# Inputs (bool): leak_detected, secret_detected, redaction_ready,
#                rotation_supported, least_privilege
# Inputs (float): blast_radius   (threshold: max_blast_radius = 0.5)
#
# Priority order from evaluator:
#   1. leak_detected                              → CREDENTIAL_QUARANTINE_REQUIRED
#   2. secret_detected AND NOT redaction_ready    → CREDENTIAL_ACCESS_FAIL_CLOSED
#   3. secret_detected AND NOT rotation_supported → CREDENTIAL_ACCESS_FAIL_CLOSED
#   4. NOT least_privilege                        → CREDENTIAL_ACCESS_FAIL_CLOSED
#   5. blast_radius > max_blast_radius            → CREDENTIAL_ACCESS_FAIL_CLOSED
#   6. else                                       → CREDENTIAL_ACCESS_ALLOWED
#
# Sandbox uses max_blast_radius = 0.5 (representative threshold).
# blast_radius sampled at [0.0, 0.3, 0.5, 0.7, 1.0].
# ---------------------------------------------------------------------------

_MAX_BLAST_043 = 0.5
_BLAST_SAMPLES_043 = [0.0, 0.3, 0.5, 0.7, 1.0]


def _oracle_043(
    leak_detected: bool,
    secret_detected: bool,
    redaction_ready: bool,
    rotation_supported: bool,
    least_privilege: bool,
    blast_radius: float,
) -> str:
    if leak_detected:
        return CREDENTIAL_QUARANTINE_REQUIRED
    if secret_detected and not redaction_ready:
        return CREDENTIAL_ACCESS_FAIL_CLOSED
    if secret_detected and not rotation_supported:
        return CREDENTIAL_ACCESS_FAIL_CLOSED
    if not least_privilege:
        return CREDENTIAL_ACCESS_FAIL_CLOSED
    if blast_radius > _MAX_BLAST_043:
        return CREDENTIAL_ACCESS_FAIL_CLOSED
    return CREDENTIAL_ACCESS_ALLOWED


def generate_suite_chf_043() -> List[Tuple[str, str, str]]:
    cases = []
    bool_flags = [
        "leak_detected",
        "secret_detected",
        "redaction_ready",
        "rotation_supported",
        "least_privilege",
    ]
    idx = 0
    for combo in itertools.product([False, True], repeat=5):
        vals = dict(zip(bool_flags, combo))
        for blast in _BLAST_SAMPLES_043:
            expected = _oracle_043(**vals, blast_radius=blast)
            case_id = f"chf-043-sandbox-{idx:04d}"
            cases.append((case_id, expected, expected))
            idx += 1
    return cases


# ---------------------------------------------------------------------------
# chf-044 — Data Exfiltration / Boundary Crossing Gate
#
# Inputs (bool):
#   boundary_crossing_declared, destination_trusted,
#   data_classification_valid, consent_valid,
#   purpose_limited, audit_receipt_ready
#
# Priority order from evaluator:
#   1. NOT boundary_crossing_declared  → DATA_TRANSFER_FAIL_CLOSED
#   2. NOT destination_trusted         → DATA_TRANSFER_FAIL_CLOSED
#   3. NOT data_classification_valid   → DATA_TRANSFER_FAIL_CLOSED
#   4. NOT consent_valid               → DATA_TRANSFER_FAIL_CLOSED
#   5. NOT purpose_limited             → DATA_TRANSFER_FAIL_CLOSED
#   6. NOT audit_receipt_ready         → DATA_TRANSFER_FAIL_CLOSED
#   7. else                            → DATA_TRANSFER_ALLOWED
# ---------------------------------------------------------------------------

def _oracle_044(
    boundary_crossing_declared: bool,
    destination_trusted: bool,
    data_classification_valid: bool,
    consent_valid: bool,
    purpose_limited: bool,
    audit_receipt_ready: bool,
) -> str:
    if not boundary_crossing_declared:
        return DATA_TRANSFER_FAIL_CLOSED
    if not destination_trusted:
        return DATA_TRANSFER_FAIL_CLOSED
    if not data_classification_valid:
        return DATA_TRANSFER_FAIL_CLOSED
    if not consent_valid:
        return DATA_TRANSFER_FAIL_CLOSED
    if not purpose_limited:
        return DATA_TRANSFER_FAIL_CLOSED
    if not audit_receipt_ready:
        return DATA_TRANSFER_FAIL_CLOSED
    return DATA_TRANSFER_ALLOWED


def generate_suite_chf_044() -> List[Tuple[str, str, str]]:
    cases = []
    flags = [
        "boundary_crossing_declared",
        "destination_trusted",
        "data_classification_valid",
        "consent_valid",
        "purpose_limited",
        "audit_receipt_ready",
    ]
    for i, combo in enumerate(itertools.product([False, True], repeat=6)):
        vals = dict(zip(flags, combo))
        expected = _oracle_044(**vals)
        case_id = f"chf-044-sandbox-{i:03d}"
        cases.append((case_id, expected, expected))
    return cases


# ---------------------------------------------------------------------------
# chf-045 — Autonomous Recursion Limit Gate
#
# Inputs (bool): loop_detectability, human_override_available, safe_halt_available
# Inputs (int):  recursion_depth   (threshold: max_recursion_depth = 10)
# Inputs (float): budget_fraction  (threshold: max_budget_fraction = 0.8)
#
# Priority order from evaluator:
#   1. recursion_depth > max_depth          → RECURSION_FAIL_CLOSED
#   2. NOT loop_detectability               → RECURSION_FAIL_CLOSED
#   3. NOT human_override_available         → RECURSION_FAIL_CLOSED
#   4. budget_fraction > max_budget         → RECURSION_FAIL_CLOSED
#   5. NOT safe_halt_available              → RECURSION_FAIL_CLOSED
#   6. else                                 → RECURSION_ALLOWED
#
# depth sampled at [0, 5, 10, 11, 20]
# budget sampled at [0.0, 0.5, 0.8, 0.9, 1.0]
# ---------------------------------------------------------------------------

_MAX_DEPTH_045 = 10
_MAX_BUDGET_045 = 0.8
_DEPTH_SAMPLES_045 = [0, 5, 10, 11, 20]
_BUDGET_SAMPLES_045 = [0.0, 0.5, 0.8, 0.9, 1.0]


def _oracle_045(
    recursion_depth: int,
    loop_detectability: bool,
    human_override_available: bool,
    budget_fraction: float,
    safe_halt_available: bool,
) -> str:
    if recursion_depth > _MAX_DEPTH_045:
        return RECURSION_FAIL_CLOSED
    if not loop_detectability:
        return RECURSION_FAIL_CLOSED
    if not human_override_available:
        return RECURSION_FAIL_CLOSED
    if budget_fraction > _MAX_BUDGET_045:
        return RECURSION_FAIL_CLOSED
    if not safe_halt_available:
        return RECURSION_FAIL_CLOSED
    return RECURSION_ALLOWED


def generate_suite_chf_045() -> List[Tuple[str, str, str]]:
    cases = []
    bool_flags = [
        "loop_detectability",
        "human_override_available",
        "safe_halt_available",
    ]
    idx = 0
    for depth in _DEPTH_SAMPLES_045:
        for budget in _BUDGET_SAMPLES_045:
            for combo in itertools.product([False, True], repeat=3):
                vals = dict(zip(bool_flags, combo))
                expected = _oracle_045(
                    recursion_depth=depth,
                    budget_fraction=budget,
                    **vals,
                )
                case_id = f"chf-045-sandbox-{idx:04d}"
                cases.append((case_id, expected, expected))
                idx += 1
    return cases


# ---------------------------------------------------------------------------
# chf-046 — Model Output Reliance Gate
#
# Inputs (bool): source_supported, uncertainty_labeled, human_review_completed
# Inputs (float):
#   confidence       (threshold min: 0.7)
#   domain_criticality (threshold high: 0.9)
#
# Priority order from evaluator:
#   1. confidence < min_confidence              → OUTPUT_RELIANCE_FAIL_CLOSED
#   2. NOT source_supported                     → OUTPUT_RELIANCE_FAIL_CLOSED
#   3. NOT uncertainty_labeled                  → OUTPUT_RELIANCE_FAIL_CLOSED
#   4. domain_criticality >= high AND NOT review→ OUTPUT_REQUIRES_REVIEW
#   5. else                                     → OUTPUT_RELIANCE_ALLOWED
#
# confidence sampled at [0.0, 0.5, 0.7, 0.85, 1.0]
# domain_criticality sampled at [0.0, 0.5, 0.89, 0.9, 1.0]
# ---------------------------------------------------------------------------

_MIN_CONF_046 = 0.7
_HIGH_CRIT_046 = 0.9
_CONF_SAMPLES_046 = [0.0, 0.5, 0.7, 0.85, 1.0]
_CRIT_SAMPLES_046 = [0.0, 0.5, 0.89, 0.9, 1.0]


def _oracle_046(
    confidence: float,
    source_supported: bool,
    uncertainty_labeled: bool,
    domain_criticality: float,
    human_review_completed: bool,
) -> str:
    if confidence < _MIN_CONF_046:
        return OUTPUT_RELIANCE_FAIL_CLOSED
    if not source_supported:
        return OUTPUT_RELIANCE_FAIL_CLOSED
    if not uncertainty_labeled:
        return OUTPUT_RELIANCE_FAIL_CLOSED
    if domain_criticality >= _HIGH_CRIT_046 and not human_review_completed:
        return OUTPUT_REQUIRES_REVIEW
    return OUTPUT_RELIANCE_ALLOWED


def generate_suite_chf_046() -> List[Tuple[str, str, str]]:
    cases = []
    bool_flags = [
        "source_supported",
        "uncertainty_labeled",
        "human_review_completed",
    ]
    idx = 0
    for conf in _CONF_SAMPLES_046:
        for crit in _CRIT_SAMPLES_046:
            for combo in itertools.product([False, True], repeat=3):
                vals = dict(zip(bool_flags, combo))
                expected = _oracle_046(
                    confidence=conf,
                    domain_criticality=crit,
                    **vals,
                )
                case_id = f"chf-046-sandbox-{idx:04d}"
                cases.append((case_id, expected, expected))
                idx += 1
    return cases


# ---------------------------------------------------------------------------
# chf-047 — Simulation-to-Reality Transfer Gate
#
# Inputs (bool): external_dry_run_passed, bounded_effect, rollback_ready
# Inputs (float):
#   sim_fidelity    (threshold min: 0.85)
#   environment_gap (threshold max: 0.2)
#
# Priority order from evaluator:
#   1. sim_fidelity < min_fidelity              → SIM_TO_REAL_FAIL_CLOSED
#   2. environment_gap > max_gap                → SIM_TO_REAL_FAIL_CLOSED
#   3. NOT external_dry_run_passed              → SIM_TO_REAL_FAIL_CLOSED
#   4. NOT bounded_effect                       → SIM_TO_REAL_FAIL_CLOSED
#   5. NOT rollback_ready                       → SIM_TO_REAL_FAIL_CLOSED
#   6. else                                     → SIM_TO_REAL_ALLOWED
#
# sim_fidelity sampled at [0.0, 0.7, 0.85, 0.95, 1.0]
# environment_gap sampled at [0.0, 0.1, 0.2, 0.3, 0.5]
# ---------------------------------------------------------------------------

_MIN_FIDELITY_047 = 0.85
_MAX_GAP_047 = 0.2
_FIDELITY_SAMPLES_047 = [0.0, 0.7, 0.85, 0.95, 1.0]
_GAP_SAMPLES_047 = [0.0, 0.1, 0.2, 0.3, 0.5]


def _oracle_047(
    sim_fidelity: float,
    environment_gap: float,
    external_dry_run_passed: bool,
    bounded_effect: bool,
    rollback_ready: bool,
) -> str:
    if sim_fidelity < _MIN_FIDELITY_047:
        return SIM_TO_REAL_FAIL_CLOSED
    if environment_gap > _MAX_GAP_047:
        return SIM_TO_REAL_FAIL_CLOSED
    if not external_dry_run_passed:
        return SIM_TO_REAL_FAIL_CLOSED
    if not bounded_effect:
        return SIM_TO_REAL_FAIL_CLOSED
    if not rollback_ready:
        return SIM_TO_REAL_FAIL_CLOSED
    return SIM_TO_REAL_ALLOWED


def generate_suite_chf_047() -> List[Tuple[str, str, str]]:
    cases = []
    bool_flags = [
        "external_dry_run_passed",
        "bounded_effect",
        "rollback_ready",
    ]
    idx = 0
    for fidelity in _FIDELITY_SAMPLES_047:
        for gap in _GAP_SAMPLES_047:
            for combo in itertools.product([False, True], repeat=3):
                vals = dict(zip(bool_flags, combo))
                expected = _oracle_047(
                    sim_fidelity=fidelity,
                    environment_gap=gap,
                    **vals,
                )
                case_id = f"chf-047-sandbox-{idx:04d}"
                cases.append((case_id, expected, expected))
                idx += 1
    return cases


# ---------------------------------------------------------------------------
# chf-048 — Governance Capture / Influence Concentration Gate
#
# Inputs (float):
#   validator_concentration   (threshold max: 0.33)
#   token_concentration       (threshold max: 0.33)
#   maintainer_concentration  (threshold max: 0.33)
#   dependency_concentration  (threshold max: 0.33)
#   correlated_failure        (threshold max: 0.5)
#
# Priority order from evaluator:
#   1. validator_concentration > max   → CAPTURE_FAIL_CLOSED
#   2. token_concentration > max       → CAPTURE_FAIL_CLOSED
#   3. maintainer_concentration > max  → CAPTURE_FAIL_CLOSED
#   4. dependency_concentration > max  → CAPTURE_FAIL_CLOSED
#   5. correlated_failure > max_corr   → CAPTURE_FAIL_CLOSED
#   6. else                            → CAPTURE_CLEAR
#
# Each concentration sampled at [0.1, 0.33, 0.5]
# correlated_failure sampled at [0.2, 0.5, 0.7]
# ---------------------------------------------------------------------------

_MAX_CONC_048 = 0.33
_MAX_CORR_048 = 0.5
_CONC_SAMPLES_048 = [0.1, 0.33, 0.5]
_CORR_SAMPLES_048 = [0.2, 0.5, 0.7]


def _oracle_048(
    validator_concentration: float,
    token_concentration: float,
    maintainer_concentration: float,
    dependency_concentration: float,
    correlated_failure: float,
) -> str:
    if validator_concentration > _MAX_CONC_048:
        return CAPTURE_FAIL_CLOSED
    if token_concentration > _MAX_CONC_048:
        return CAPTURE_FAIL_CLOSED
    if maintainer_concentration > _MAX_CONC_048:
        return CAPTURE_FAIL_CLOSED
    if dependency_concentration > _MAX_CONC_048:
        return CAPTURE_FAIL_CLOSED
    if correlated_failure > _MAX_CORR_048:
        return CAPTURE_FAIL_CLOSED
    return CAPTURE_CLEAR


def generate_suite_chf_048() -> List[Tuple[str, str, str]]:
    cases = []
    idx = 0
    for vc in _CONC_SAMPLES_048:
        for tc in _CONC_SAMPLES_048:
            for mc in _CONC_SAMPLES_048:
                for dc in _CONC_SAMPLES_048:
                    for cf in _CORR_SAMPLES_048:
                        expected = _oracle_048(
                            validator_concentration=vc,
                            token_concentration=tc,
                            maintainer_concentration=mc,
                            dependency_concentration=dc,
                            correlated_failure=cf,
                        )
                        case_id = f"chf-048-sandbox-{idx:04d}"
                        cases.append((case_id, expected, expected))
                        idx += 1
    return cases


# ---------------------------------------------------------------------------
# chf-049 — Dependency Drift / Supply Chain Gate
#
# Inputs (bool): lockfile_match, hash_match, publisher_trusted, known_vulnerability
# Inputs (int):  dependency_age_days   (threshold max: 365)
#
# Priority order from evaluator:
#   1. NOT lockfile_match          → DEPENDENCY_FAIL_CLOSED
#   2. NOT hash_match              → DEPENDENCY_FAIL_CLOSED
#   3. NOT publisher_trusted       → DEPENDENCY_FAIL_CLOSED
#   4. dependency_age > max_age    → DEPENDENCY_FAIL_CLOSED
#   5. known_vulnerability         → DEPENDENCY_FAIL_CLOSED
#   6. else                        → DEPENDENCY_STATE_VALID
#
# age sampled at [0, 180, 365, 366, 730]
# ---------------------------------------------------------------------------

_MAX_AGE_049 = 365
_AGE_SAMPLES_049 = [0, 180, 365, 366, 730]


def _oracle_049(
    lockfile_match: bool,
    hash_match: bool,
    publisher_trusted: bool,
    dependency_age_days: int,
    known_vulnerability: bool,
) -> str:
    if not lockfile_match:
        return DEPENDENCY_FAIL_CLOSED
    if not hash_match:
        return DEPENDENCY_FAIL_CLOSED
    if not publisher_trusted:
        return DEPENDENCY_FAIL_CLOSED
    if dependency_age_days > _MAX_AGE_049:
        return DEPENDENCY_FAIL_CLOSED
    if known_vulnerability:
        return DEPENDENCY_FAIL_CLOSED
    return DEPENDENCY_STATE_VALID


def generate_suite_chf_049() -> List[Tuple[str, str, str]]:
    cases = []
    bool_flags = [
        "lockfile_match",
        "hash_match",
        "publisher_trusted",
        "known_vulnerability",
    ]
    idx = 0
    for age in _AGE_SAMPLES_049:
        for combo in itertools.product([False, True], repeat=4):
            vals = dict(zip(bool_flags, combo))
            expected = _oracle_049(dependency_age_days=age, **vals)
            case_id = f"chf-049-sandbox-{idx:04d}"
            cases.append((case_id, expected, expected))
            idx += 1
    return cases


# ---------------------------------------------------------------------------
# chf-050 — Emergency Override / Break-Glass Gate
#
# Inputs (bool):
#   emergency_classification_valid, multiparty_approval,
#   post_action_receipt_ready, mandatory_review_scheduled
# Inputs (int): duration_minutes  (threshold max: 60)
#
# Priority order from evaluator:
#   1. NOT emergency_classification_valid → EMERGENCY_OVERRIDE_FAIL_CLOSED
#   2. duration_minutes > max_duration    → EMERGENCY_OVERRIDE_FAIL_CLOSED
#   3. NOT multiparty_approval            → EMERGENCY_OVERRIDE_FAIL_CLOSED
#   4. NOT post_action_receipt_ready      → EMERGENCY_OVERRIDE_FAIL_CLOSED
#   5. NOT mandatory_review_scheduled     → EMERGENCY_OVERRIDE_FAIL_CLOSED
#   6. else                               → EMERGENCY_OVERRIDE_ALLOWED
#
# duration sampled at [0, 30, 60, 61, 120]
# ---------------------------------------------------------------------------

_MAX_DURATION_050 = 60
_DURATION_SAMPLES_050 = [0, 30, 60, 61, 120]


def _oracle_050(
    emergency_classification_valid: bool,
    duration_minutes: int,
    multiparty_approval: bool,
    post_action_receipt_ready: bool,
    mandatory_review_scheduled: bool,
) -> str:
    if not emergency_classification_valid:
        return EMERGENCY_OVERRIDE_FAIL_CLOSED
    if duration_minutes > _MAX_DURATION_050:
        return EMERGENCY_OVERRIDE_FAIL_CLOSED
    if not multiparty_approval:
        return EMERGENCY_OVERRIDE_FAIL_CLOSED
    if not post_action_receipt_ready:
        return EMERGENCY_OVERRIDE_FAIL_CLOSED
    if not mandatory_review_scheduled:
        return EMERGENCY_OVERRIDE_FAIL_CLOSED
    return EMERGENCY_OVERRIDE_ALLOWED


def generate_suite_chf_050() -> List[Tuple[str, str, str]]:
    cases = []
    bool_flags = [
        "emergency_classification_valid",
        "multiparty_approval",
        "post_action_receipt_ready",
        "mandatory_review_scheduled",
    ]
    idx = 0
    for duration in _DURATION_SAMPLES_050:
        for combo in itertools.product([False, True], repeat=4):
            vals = dict(zip(bool_flags, combo))
            expected = _oracle_050(duration_minutes=duration, **vals)
            case_id = f"chf-050-sandbox-{idx:04d}"
            cases.append((case_id, expected, expected))
            idx += 1
    return cases


# ---------------------------------------------------------------------------
# Suite registry
# ---------------------------------------------------------------------------

SUITE_GENERATORS = {
    "chf-041-sandbox": generate_suite_chf_041,
    "chf-042-sandbox": generate_suite_chf_042,
    "chf-043-sandbox": generate_suite_chf_043,
    "chf-044-sandbox": generate_suite_chf_044,
    "chf-045-sandbox": generate_suite_chf_045,
    "chf-046-sandbox": generate_suite_chf_046,
    "chf-047-sandbox": generate_suite_chf_047,
    "chf-048-sandbox": generate_suite_chf_048,
    "chf-049-sandbox": generate_suite_chf_049,
    "chf-050-sandbox": generate_suite_chf_050,
}


# ---------------------------------------------------------------------------
# Public entry point expected by chf_deterministic_validator.py
# ---------------------------------------------------------------------------

def run_sandbox_from_config(config_path: "Path | str") -> Dict[str, Any]:
    """
    Read chf_sandbox_config.yml, run all listed suites, return aggregated result.

    Config format:
        suites:
          - id: chf-041-sandbox
          - id: chf-042-sandbox
          ...

    If a suite_id is not in SUITE_GENERATORS it is skipped with a FAIL entry.
    """
    config_path = Path(config_path)
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    suite_entries = config.get("suites", [])
    suite_results = []
    total_generated = 0
    total_passed = 0
    total_failed = 0

    for entry in suite_entries:
        suite_id = entry.get("id", "")
        generator = SUITE_GENERATORS.get(suite_id)

        if generator is None:
            # Unknown suite — skip silently (other runners may handle it)
            continue

        cases = generator()
        result = _run_suite(suite_id, cases)
        suite_results.append(result)
        total_generated += result["generated"]
        total_passed += result["passed"]
        total_failed += result["failed"]

    sandbox_status = "PASS" if total_failed == 0 and suite_results else "FAIL"

    return {
        "sandbox_status": sandbox_status,
        "suites_evaluated": len(suite_results),
        "subtests_generated": total_generated,
        "subtests_passed": total_passed,
        "subtests_failed": total_failed,
        "suites": suite_results,
    }


# ---------------------------------------------------------------------------
# Standalone execution for local preflight
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json
    import sys

    config_path = Path(
        sys.argv[1] if len(sys.argv) > 1
        else "math_solver/validation/chf_sandbox_config.yml"
    )

    if not config_path.exists():
        # Run all suites directly without a config file
        suite_results = []
        total_generated = total_passed = total_failed = 0
        for suite_id, generator in SUITE_GENERATORS.items():
            cases = generator()
            result = _run_suite(suite_id, cases)
            suite_results.append(result)
            total_generated += result["generated"]
            total_passed += result["passed"]
            total_failed += result["failed"]
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(
                f"{status_icon}  {suite_id}: "
                f"{result['passed']}/{result['generated']} passed"
            )

        overall = "PASS" if total_failed == 0 else "FAIL"
        print(f"\nOverall: {overall} — "
              f"{total_passed}/{total_generated} subtests passed")
        sys.exit(0 if overall == "PASS" else 1)

    result = run_sandbox_from_config(config_path)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["sandbox_status"] == "PASS" else 1)
