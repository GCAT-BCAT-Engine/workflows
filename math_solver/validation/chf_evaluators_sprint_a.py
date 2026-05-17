#!/usr/bin/env python3
"""
chf_evaluators_sprint_a.py
--------------------------
Dedicated evaluator functions for the 7 gates in chf-051 through chf-100
that require multi-outcome or conditional logic beyond what
evaluate_standard_binary_gate can express.

Gates covered:
  chf-056  Scientific Claim Escalation Gate
  chf-059  Deletion / Forgetting / Retention Gate
  chf-079  Specification Drift Detection Gate
  chf-084  Quarantine Routing Gate
  chf-087  Incident Response Gate
  chf-094  Adversarial Review Gate
  chf-100  Phase-One Completion Gate

Integration:
  Copy these functions into chf_deterministic_validator.py and replace
  the corresponding evaluate_standard_binary_gate entries in EVALUATORS:

    "chf-056": evaluate_chf_056,
    "chf-059": evaluate_chf_059,
    "chf-079": evaluate_chf_079,
    "chf-084": evaluate_chf_084,
    "chf-087": evaluate_chf_087,
    "chf-094": evaluate_chf_094,
    "chf-100": evaluate_chf_100,

Stable dispatcher rule: no workflow changes. These are tools, not workflows.
"""

from __future__ import annotations
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# New outcome constants — add these to chf_deterministic_validator.py
# ---------------------------------------------------------------------------

ESCALATION_REQUIRED = "ESCALATION_REQUIRED"

DELETION_REQUIRED = "DELETION_REQUIRED"
RETENTION_ALLOWED = "RETENTION_ALLOWED"
RETENTION_FAIL_CLOSED = "RETENTION_FAIL_CLOSED"

DRIFT_QUARANTINE = "DRIFT_QUARANTINE"
DRIFT_ACCEPTABLE = "DRIFT_ACCEPTABLE"
DRIFT_FAIL_CLOSED = "DRIFT_FAIL_CLOSED"

ROUTE_TO_QUARANTINE = "ROUTE_TO_QUARANTINE"
ROUTE_TO_REVIEW = "ROUTE_TO_REVIEW"
ROUTING_CLEAR = "ROUTING_CLEAR"
ROUTING_FAIL_CLOSED = "ROUTING_FAIL_CLOSED"

INCIDENT_ESCALATE = "INCIDENT_ESCALATE"
INCIDENT_CONTAIN = "INCIDENT_CONTAIN"
INCIDENT_MONITOR = "INCIDENT_MONITOR"
INCIDENT_FAIL_CLOSED = "INCIDENT_FAIL_CLOSED"

FINDING_CRITICAL = "FINDING_CRITICAL"
FINDING_MINOR = "FINDING_MINOR"
REVIEW_CLEAR = "REVIEW_CLEAR"
REVIEW_FAIL_CLOSED = "REVIEW_FAIL_CLOSED"

PHASE_COMPLETE = "PHASE_COMPLETE"
PHASE_INCOMPLETE = "PHASE_INCOMPLETE"
PHASE_BLOCKED = "PHASE_BLOCKED"

ALLOW = "ALLOW"
FAIL_CLOSED = "FAIL_CLOSED"


# ---------------------------------------------------------------------------
# chf-056 — Scientific Claim Escalation Gate
#
# Purpose:
#   Validate whether a scientific or mathematical claim requires stronger
#   review before publication.
#
# Outcome classes:
#   ALLOW              — claim is within evidence bounds, no escalation needed
#   ESCALATION_REQUIRED — extraordinary claim detected or peer-review path missing
#   FAIL_CLOSED        — claim boundary undefined or overclaim guardrail absent
#
# Priority order:
#   1. NOT claim_boundary_defined       → FAIL_CLOSED
#   2. NOT overclaim_guardrail          → FAIL_CLOSED
#   3. speculation_ratio > max_spec     → FAIL_CLOSED
#   4. extraordinary_claim AND
#      NOT evidence_level_sufficient    → ESCALATION_REQUIRED
#   5. NOT peer_review_path_exists      → ESCALATION_REQUIRED
#   6. evidence_level_sufficient        → ALLOW
#   7. else                             → ESCALATION_REQUIRED
#
# Conditional logic:
#   extraordinary_claim triggers escalation only when
#   evidence_level_sufficient is false. If evidence is sufficient,
#   an extraordinary claim can still proceed (with guardrails).
# ---------------------------------------------------------------------------

def evaluate_chf_056(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    max_speculation = float(model.get("max_speculation_ratio", 0.2))
    cases: List[Dict[str, Any]] = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]

        claim_boundary_defined = bool(case.get("claim_boundary_defined", False))
        overclaim_guardrail = bool(case.get("overclaim_guardrail", False))
        speculation_ratio = float(case.get("speculation_ratio", 1.0))
        extraordinary_claim = bool(case.get("extraordinary_claim", False))
        evidence_level_sufficient = bool(case.get("evidence_level_sufficient", False))
        peer_review_path_exists = bool(case.get("peer_review_path_exists", False))

        if not claim_boundary_defined:
            actual, reason = FAIL_CLOSED, "claim_boundary_undefined"
        elif not overclaim_guardrail:
            actual, reason = FAIL_CLOSED, "overclaim_guardrail_missing"
        elif speculation_ratio > max_speculation:
            actual, reason = FAIL_CLOSED, "speculation_ratio_exceeds_ceiling"
        elif extraordinary_claim and not evidence_level_sufficient:
            actual, reason = ESCALATION_REQUIRED, "extraordinary_claim_requires_escalation"
        elif not peer_review_path_exists:
            actual, reason = ESCALATION_REQUIRED, "peer_review_path_missing"
        elif evidence_level_sufficient:
            actual, reason = ALLOW, "scientific_claim_within_evidence_bounds"
        else:
            actual, reason = ESCALATION_REQUIRED, "evidence_level_insufficient_for_publication"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {
        "spec_id": spec["problem_id"],
        "status": "PASS" if all_pass else "FAIL",
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# chf-059 — Deletion / Forgetting / Retention Gate
#
# Purpose:
#   Validate whether data should be retained, deleted, forgotten,
#   archived, tombstoned, or quarantined.
#
# Outcome classes:
#   RETENTION_ALLOWED   — data may be retained under valid basis
#   DELETION_REQUIRED   — data must be deleted (retention forbidden)
#   RETENTION_FAIL_CLOSED — retention status cannot be determined
#
# Priority order:
#   1. NOT retention_basis_valid AND
#      NOT deletion_path_exists        → RETENTION_FAIL_CLOSED
#   2. retention_forbidden             → DELETION_REQUIRED
#      (regardless of other fields — legal obligation trumps)
#   3. NOT tombstone_receipt_ready     → RETENTION_FAIL_CLOSED
#      (if deletion is needed but receipt not ready, block)
#      Only applies when deletion_path_exists is true
#   4. NOT downstream_notice_sent      → RETENTION_FAIL_CLOSED
#   5. orphan_record_risk > max_orphan → RETENTION_FAIL_CLOSED
#      (only meaningful when deletion_path_exists)
#   6. retention_basis_valid           → RETENTION_ALLOWED
#   7. else                            → RETENTION_FAIL_CLOSED
#
# Conditional logic:
#   tombstone_receipt_ready and orphan_record_risk only apply
#   when deletion_path_exists is true.
#   retention_forbidden is a hard trigger for DELETION_REQUIRED
#   regardless of whether receipts are ready.
# ---------------------------------------------------------------------------

def evaluate_chf_059(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    max_orphan = float(model.get("max_orphan_record_risk", 0.1))
    cases: List[Dict[str, Any]] = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]

        retention_basis_valid = bool(case.get("retention_basis_valid", False))
        deletion_path_exists = bool(case.get("deletion_path_exists", False))
        retention_forbidden = bool(case.get("retention_forbidden", False))
        tombstone_receipt_ready = bool(case.get("tombstone_receipt_ready", False))
        downstream_notice_sent = bool(case.get("downstream_notice_sent", False))
        orphan_record_risk = float(case.get("orphan_record_risk", 1.0))

        if not retention_basis_valid and not deletion_path_exists:
            actual, reason = RETENTION_FAIL_CLOSED, "no_retention_basis_and_no_deletion_path"
        elif retention_forbidden:
            actual, reason = DELETION_REQUIRED, "retention_legally_forbidden"
        elif deletion_path_exists and not tombstone_receipt_ready:
            actual, reason = RETENTION_FAIL_CLOSED, "tombstone_receipt_not_ready"
        elif not downstream_notice_sent:
            actual, reason = RETENTION_FAIL_CLOSED, "downstream_notice_not_sent"
        elif deletion_path_exists and orphan_record_risk > max_orphan:
            actual, reason = RETENTION_FAIL_CLOSED, "orphan_record_risk_exceeds_threshold"
        elif retention_basis_valid:
            actual, reason = RETENTION_ALLOWED, "retention_basis_valid_and_constraints_pass"
        else:
            actual, reason = RETENTION_FAIL_CLOSED, "retention_status_undetermined"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {
        "spec_id": spec["problem_id"],
        "status": "PASS" if all_pass else "FAIL",
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# chf-079 — Specification Drift Detection Gate
#
# Purpose:
#   Validate whether a specification has drifted from its validated
#   state in a way that requires quarantine or re-validation.
#
# Outcome classes:
#   DRIFT_ACCEPTABLE  — drift is within tolerance, no action required
#   DRIFT_QUARANTINE  — drift detected beyond tolerance, spec quarantined
#   DRIFT_FAIL_CLOSED — drift cannot be measured or baseline missing
#
# Priority order:
#   1. NOT baseline_hash_present        → DRIFT_FAIL_CLOSED
#   2. NOT drift_measurable             → DRIFT_FAIL_CLOSED
#   3. semantic_drift > critical_thresh → DRIFT_QUARANTINE
#      (unacceptable drift — quarantine immediately)
#   4. structural_drift > critical_thresh → DRIFT_QUARANTINE
#   5. semantic_drift > warn_thresh     → DRIFT_QUARANTINE
#      (warning-level drift also quarantines pending review)
#   6. re_validation_receipt_present
#      AND drift within tolerance       → DRIFT_ACCEPTABLE
#   7. drift within tolerance           → DRIFT_ACCEPTABLE
#   8. else                             → DRIFT_QUARANTINE
#
# Conditional logic:
#   Two drift dimensions (semantic, structural) each with their own
#   thresholds. Either exceeding critical triggers DRIFT_QUARANTINE.
#   re_validation_receipt can clear a warning-level drift only when
#   drift is within warning tolerance.
# ---------------------------------------------------------------------------

def evaluate_chf_079(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    warn_thresh = float(model.get("drift_warning_threshold", 0.05))
    critical_thresh = float(model.get("drift_critical_threshold", 0.15))
    cases: List[Dict[str, Any]] = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]

        baseline_hash_present = bool(case.get("baseline_hash_present", False))
        drift_measurable = bool(case.get("drift_measurable", False))
        semantic_drift = float(case.get("semantic_drift", 1.0))
        structural_drift = float(case.get("structural_drift", 1.0))
        re_validation_receipt_present = bool(
            case.get("re_validation_receipt_present", False)
        )

        if not baseline_hash_present:
            actual, reason = DRIFT_FAIL_CLOSED, "baseline_hash_missing"
        elif not drift_measurable:
            actual, reason = DRIFT_FAIL_CLOSED, "drift_not_measurable"
        elif semantic_drift > critical_thresh:
            actual, reason = DRIFT_QUARANTINE, "semantic_drift_exceeds_critical_threshold"
        elif structural_drift > critical_thresh:
            actual, reason = DRIFT_QUARANTINE, "structural_drift_exceeds_critical_threshold"
        elif semantic_drift > warn_thresh and not re_validation_receipt_present:
            actual, reason = DRIFT_QUARANTINE, "semantic_drift_in_warning_zone_no_revalidation"
        elif semantic_drift <= warn_thresh and structural_drift <= warn_thresh:
            actual, reason = DRIFT_ACCEPTABLE, "drift_within_acceptable_tolerance"
        elif re_validation_receipt_present:
            actual, reason = DRIFT_ACCEPTABLE, "drift_cleared_by_revalidation_receipt"
        else:
            actual, reason = DRIFT_QUARANTINE, "drift_exceeds_tolerance_no_receipt"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {
        "spec_id": spec["problem_id"],
        "status": "PASS" if all_pass else "FAIL",
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# chf-084 — Quarantine Routing Gate
#
# Purpose:
#   Determine where a flagged transition should be routed:
#   full quarantine, human review, or clear to proceed.
#
# Outcome classes:
#   ROUTE_TO_QUARANTINE — high-severity flag, isolate immediately
#   ROUTE_TO_REVIEW     — medium-severity flag, human review required
#   ROUTING_CLEAR       — no flags above threshold, proceed
#   ROUTING_FAIL_CLOSED — routing system cannot determine disposition
#
# Priority order:
#   1. NOT routing_system_available     → ROUTING_FAIL_CLOSED
#   2. NOT flag_classified              → ROUTING_FAIL_CLOSED
#   3. severity_score > critical_thresh → ROUTE_TO_QUARANTINE
#   4. tamper_suspected                 → ROUTE_TO_QUARANTINE
#   5. authority_unresolved             → ROUTE_TO_QUARANTINE
#   6. severity_score > review_thresh   → ROUTE_TO_REVIEW
#   7. human_review_requested           → ROUTE_TO_REVIEW
#   8. severity_score <= review_thresh  → ROUTING_CLEAR
#   9. else                             → ROUTING_FAIL_CLOSED
#
# Severity thresholds are model parameters.
# tamper_suspected and authority_unresolved are hard escalation triggers
# regardless of numeric severity.
# ---------------------------------------------------------------------------

def evaluate_chf_084(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    critical_thresh = float(model.get("severity_critical_threshold", 0.8))
    review_thresh = float(model.get("severity_review_threshold", 0.4))
    cases: List[Dict[str, Any]] = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]

        routing_system_available = bool(case.get("routing_system_available", False))
        flag_classified = bool(case.get("flag_classified", False))
        severity_score = float(case.get("severity_score", 1.0))
        tamper_suspected = bool(case.get("tamper_suspected", False))
        authority_unresolved = bool(case.get("authority_unresolved", False))
        human_review_requested = bool(case.get("human_review_requested", False))

        if not routing_system_available:
            actual, reason = ROUTING_FAIL_CLOSED, "routing_system_unavailable"
        elif not flag_classified:
            actual, reason = ROUTING_FAIL_CLOSED, "flag_not_classified"
        elif severity_score > critical_thresh:
            actual, reason = ROUTE_TO_QUARANTINE, "severity_exceeds_critical_threshold"
        elif tamper_suspected:
            actual, reason = ROUTE_TO_QUARANTINE, "tamper_suspected"
        elif authority_unresolved:
            actual, reason = ROUTE_TO_QUARANTINE, "authority_unresolved"
        elif severity_score > review_thresh:
            actual, reason = ROUTE_TO_REVIEW, "severity_in_review_range"
        elif human_review_requested:
            actual, reason = ROUTE_TO_REVIEW, "human_review_requested"
        elif severity_score <= review_thresh:
            actual, reason = ROUTING_CLEAR, "severity_below_review_threshold"
        else:
            actual, reason = ROUTING_FAIL_CLOSED, "routing_disposition_undetermined"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {
        "spec_id": spec["problem_id"],
        "status": "PASS" if all_pass else "FAIL",
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# chf-087 — Incident Response Gate
#
# Purpose:
#   Determine the correct incident response disposition:
#   escalate to external parties, contain within system,
#   or monitor without immediate action.
#
# Outcome classes:
#   INCIDENT_ESCALATE   — critical incident requiring external escalation
#   INCIDENT_CONTAIN    — incident contained within system boundary
#   INCIDENT_MONITOR    — low-severity, monitor only
#   INCIDENT_FAIL_CLOSED — incident class undetermined
#
# Priority order:
#   1. NOT incident_class_defined       → INCIDENT_FAIL_CLOSED
#   2. NOT response_plan_exists         → INCIDENT_FAIL_CLOSED
#   3. external_parties_affected        → INCIDENT_ESCALATE
#   4. severity_score > critical_thresh → INCIDENT_ESCALATE
#   5. data_breach_detected             → INCIDENT_ESCALATE
#      (regulatory obligation regardless of severity score)
#   6. severity_score > contain_thresh  → INCIDENT_CONTAIN
#   7. containment_path_available
#      AND rollback_ready               → INCIDENT_CONTAIN
#   8. severity_score <= monitor_thresh → INCIDENT_MONITOR
#   9. else                             → INCIDENT_FAIL_CLOSED
#
# Conditional logic:
#   data_breach_detected is a hard escalation trigger (regulatory).
#   containment requires both containment_path_available AND
#   rollback_ready — neither alone is sufficient.
# ---------------------------------------------------------------------------

def evaluate_chf_087(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    critical_thresh = float(model.get("severity_critical_threshold", 0.8))
    contain_thresh = float(model.get("severity_contain_threshold", 0.4))
    monitor_thresh = float(model.get("severity_monitor_threshold", 0.2))
    cases: List[Dict[str, Any]] = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]

        incident_class_defined = bool(case.get("incident_class_defined", False))
        response_plan_exists = bool(case.get("response_plan_exists", False))
        external_parties_affected = bool(case.get("external_parties_affected", False))
        severity_score = float(case.get("severity_score", 1.0))
        data_breach_detected = bool(case.get("data_breach_detected", False))
        containment_path_available = bool(case.get("containment_path_available", False))
        rollback_ready = bool(case.get("rollback_ready", False))

        if not incident_class_defined:
            actual, reason = INCIDENT_FAIL_CLOSED, "incident_class_undefined"
        elif not response_plan_exists:
            actual, reason = INCIDENT_FAIL_CLOSED, "response_plan_missing"
        elif external_parties_affected:
            actual, reason = INCIDENT_ESCALATE, "external_parties_affected"
        elif severity_score > critical_thresh:
            actual, reason = INCIDENT_ESCALATE, "severity_exceeds_critical_threshold"
        elif data_breach_detected:
            actual, reason = INCIDENT_ESCALATE, "data_breach_requires_escalation"
        elif severity_score > contain_thresh:
            actual, reason = INCIDENT_CONTAIN, "severity_in_containment_range"
        elif containment_path_available and rollback_ready:
            actual, reason = INCIDENT_CONTAIN, "containment_path_and_rollback_available"
        elif severity_score <= monitor_thresh:
            actual, reason = INCIDENT_MONITOR, "severity_below_monitor_threshold"
        else:
            actual, reason = INCIDENT_FAIL_CLOSED, "incident_disposition_undetermined"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {
        "spec_id": spec["problem_id"],
        "status": "PASS" if all_pass else "FAIL",
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# chf-094 — Adversarial Review Gate
#
# Purpose:
#   Evaluate whether adversarial review findings block, flag, or
#   clear a formalism claim or publication artifact.
#
# Outcome classes:
#   FINDING_CRITICAL  — critical finding blocks publication/deployment
#   FINDING_MINOR     — minor finding flagged, does not block
#   REVIEW_CLEAR      — no findings above threshold
#   REVIEW_FAIL_CLOSED — review incomplete or process invalid
#
# Priority order:
#   1. NOT review_process_valid         → REVIEW_FAIL_CLOSED
#   2. NOT review_completed             → REVIEW_FAIL_CLOSED
#   3. critical_finding_present         → FINDING_CRITICAL
#      (hard block regardless of other fields)
#   4. finding_severity > critical_thresh → FINDING_CRITICAL
#   5. finding_severity > minor_thresh  → FINDING_MINOR
#   6. minor_finding_present
#      AND finding_severity > minor_thresh → FINDING_MINOR
#   7. finding_severity <= minor_thresh
#      AND NOT minor_finding_present    → REVIEW_CLEAR
#   8. else                             → REVIEW_FAIL_CLOSED
#
# Conditional logic:
#   critical_finding_present is a hard block — even if severity_score
#   is below threshold, an explicit critical finding flag overrides.
#   minor_finding_present without severity above minor_thresh still
#   produces FINDING_MINOR (qualitative finding matters).
# ---------------------------------------------------------------------------

def evaluate_chf_094(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    critical_thresh = float(model.get("finding_critical_threshold", 0.7))
    minor_thresh = float(model.get("finding_minor_threshold", 0.3))
    cases: List[Dict[str, Any]] = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]

        review_process_valid = bool(case.get("review_process_valid", False))
        review_completed = bool(case.get("review_completed", False))
        critical_finding_present = bool(case.get("critical_finding_present", False))
        finding_severity = float(case.get("finding_severity", 0.0))
        minor_finding_present = bool(case.get("minor_finding_present", False))

        if not review_process_valid:
            actual, reason = REVIEW_FAIL_CLOSED, "review_process_invalid"
        elif not review_completed:
            actual, reason = REVIEW_FAIL_CLOSED, "review_not_completed"
        elif critical_finding_present:
            actual, reason = FINDING_CRITICAL, "critical_finding_blocks_publication"
        elif finding_severity > critical_thresh:
            actual, reason = FINDING_CRITICAL, "finding_severity_exceeds_critical_threshold"
        elif finding_severity > minor_thresh:
            actual, reason = FINDING_MINOR, "finding_severity_in_minor_range"
        elif minor_finding_present:
            actual, reason = FINDING_MINOR, "minor_finding_flagged"
        elif finding_severity <= minor_thresh and not minor_finding_present:
            actual, reason = REVIEW_CLEAR, "adversarial_review_clear"
        else:
            actual, reason = REVIEW_FAIL_CLOSED, "review_disposition_undetermined"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {
        "spec_id": spec["problem_id"],
        "status": "PASS" if all_pass else "FAIL",
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# chf-100 — Phase-One Completion Gate
#
# Purpose:
#   Validate whether CHF phase one (chf-001 through chf-100) is
#   complete to publication grade. This is the v0.30 phase receipt.
#
# Outcome classes:
#   PHASE_COMPLETE   — all conditions satisfied, phase one complete
#   PHASE_INCOMPLETE — conditions partially satisfied, work remaining
#   PHASE_BLOCKED    — critical gap prevents completion claim
#
# Priority order:
#   1. NOT all_specs_evaluated          → PHASE_BLOCKED
#   2. explicit_pass_fraction < 1.0     → PHASE_BLOCKED
#      (any explicit validation failure blocks completion)
#   3. sandbox_coverage_fraction < min_sandbox → PHASE_BLOCKED
#   4. publication_grade_count < min_pub_grade → PHASE_BLOCKED
#      (insufficient publication-grade gates)
#   5. NOT maturity_matrix_complete     → PHASE_INCOMPLETE
#   6. NOT whitepaper_outline_present   → PHASE_INCOMPLETE
#   7. NOT formal_methods_map_present   → PHASE_INCOMPLETE
#   8. NOT archive_receipt_ready        → PHASE_INCOMPLETE
#   9. All conditions satisfied         → PHASE_COMPLETE
#
# Derived metrics:
#   explicit_pass_fraction and sandbox_coverage_fraction are computed
#   from counts — the standard gate cannot express derived ratios.
#   publication_grade_count is a count threshold.
#
# The distinction between PHASE_BLOCKED (critical gap) and
# PHASE_INCOMPLETE (artifacts pending) is essential for the v0.30
# phase receipt to carry honest claims.
# ---------------------------------------------------------------------------

def evaluate_chf_100(spec: Dict[str, Any]) -> Dict[str, Any]:
    model = spec["model"]
    min_sandbox_coverage = float(model.get("min_sandbox_coverage_fraction", 1.0))
    min_pub_grade = int(model.get("min_publication_grade_count", 100))
    cases: List[Dict[str, Any]] = []
    all_pass = True

    for case in spec["test_cases"]:
        expected = case["expected"]

        all_specs_evaluated = bool(case.get("all_specs_evaluated", False))
        explicit_pass_fraction = float(case.get("explicit_pass_fraction", 0.0))
        sandbox_coverage_fraction = float(case.get("sandbox_coverage_fraction", 0.0))
        publication_grade_count = int(case.get("publication_grade_count", 0))
        maturity_matrix_complete = bool(case.get("maturity_matrix_complete", False))
        whitepaper_outline_present = bool(case.get("whitepaper_outline_present", False))
        formal_methods_map_present = bool(case.get("formal_methods_map_present", False))
        archive_receipt_ready = bool(case.get("archive_receipt_ready", False))

        if not all_specs_evaluated:
            actual, reason = PHASE_BLOCKED, "not_all_specs_evaluated"
        elif explicit_pass_fraction < 1.0:
            actual, reason = PHASE_BLOCKED, "explicit_validation_failures_present"
        elif sandbox_coverage_fraction < min_sandbox_coverage:
            actual, reason = PHASE_BLOCKED, "sandbox_coverage_below_minimum"
        elif publication_grade_count < min_pub_grade:
            actual, reason = PHASE_BLOCKED, "publication_grade_count_below_minimum"
        elif not maturity_matrix_complete:
            actual, reason = PHASE_INCOMPLETE, "maturity_matrix_not_complete"
        elif not whitepaper_outline_present:
            actual, reason = PHASE_INCOMPLETE, "whitepaper_outline_missing"
        elif not formal_methods_map_present:
            actual, reason = PHASE_INCOMPLETE, "formal_methods_map_missing"
        elif not archive_receipt_ready:
            actual, reason = PHASE_INCOMPLETE, "archive_receipt_not_ready"
        else:
            actual, reason = PHASE_COMPLETE, "phase_one_completion_conditions_satisfied"

        passed = actual == expected
        all_pass = all_pass and passed
        cases.append({
            "id": case["id"],
            "expected": expected,
            "actual": actual,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
        })

    return {
        "spec_id": spec["problem_id"],
        "status": "PASS" if all_pass else "FAIL",
        "cases": cases,
    }


# ---------------------------------------------------------------------------
# EVALUATORS patch — replace in chf_deterministic_validator.py EVALUATORS dict
# ---------------------------------------------------------------------------

EVALUATORS_PATCH = {
    "chf-056": evaluate_chf_056,
    "chf-059": evaluate_chf_059,
    "chf-079": evaluate_chf_079,
    "chf-084": evaluate_chf_084,
    "chf-087": evaluate_chf_087,
    "chf-094": evaluate_chf_094,
    "chf-100": evaluate_chf_100,
}

# ---------------------------------------------------------------------------
# New outcome constants to add to chf_deterministic_validator.py
# ---------------------------------------------------------------------------

NEW_OUTCOME_CONSTANTS = """
# chf-056
ESCALATION_REQUIRED = "ESCALATION_REQUIRED"

# chf-059
DELETION_REQUIRED = "DELETION_REQUIRED"
RETENTION_ALLOWED = "RETENTION_ALLOWED"
RETENTION_FAIL_CLOSED = "RETENTION_FAIL_CLOSED"

# chf-079
DRIFT_QUARANTINE = "DRIFT_QUARANTINE"
DRIFT_ACCEPTABLE = "DRIFT_ACCEPTABLE"
DRIFT_FAIL_CLOSED = "DRIFT_FAIL_CLOSED"

# chf-084
ROUTE_TO_QUARANTINE = "ROUTE_TO_QUARANTINE"
ROUTE_TO_REVIEW = "ROUTE_TO_REVIEW"
ROUTING_CLEAR = "ROUTING_CLEAR"
ROUTING_FAIL_CLOSED = "ROUTING_FAIL_CLOSED"

# chf-087
INCIDENT_ESCALATE = "INCIDENT_ESCALATE"
INCIDENT_CONTAIN = "INCIDENT_CONTAIN"
INCIDENT_MONITOR = "INCIDENT_MONITOR"
INCIDENT_FAIL_CLOSED = "INCIDENT_FAIL_CLOSED"

# chf-094
FINDING_CRITICAL = "FINDING_CRITICAL"
FINDING_MINOR = "FINDING_MINOR"
REVIEW_CLEAR = "REVIEW_CLEAR"
REVIEW_FAIL_CLOSED = "REVIEW_FAIL_CLOSED"

# chf-100
PHASE_COMPLETE = "PHASE_COMPLETE"
PHASE_INCOMPLETE = "PHASE_INCOMPLETE"
PHASE_BLOCKED = "PHASE_BLOCKED"
"""
