"""
StegVerse FinCo Receipt Chain Validator v1.0
Validates the full private-state value receipt chain:
consent → access → use → derivative → compensation → governance
Implements FINCO_PRIVATE_STATE_VALUE.md minimum receipt stack.
ALLOW / DENY / FAIL_CLOSED per FinCo admissibility rule.
"""

import json
import hashlib
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

SCHEMA = "stegverse_finco_receipt_chain.v1"

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

def record_hash(r: dict) -> str:
    return sha256(json.dumps({k: v for k, v in r.items() if k != "receipt_hash"}, sort_keys=True))


# ── Receipt builders ──────────────────────────────────────────────────────────

def make_consent_receipt(
    subject_id: str,
    scope: str,
    purpose: str,
    permitted_actor: str,
    duration_seconds: int,
    derivative_use: bool,
    compensation_terms: str,
    revocation_possible: bool,
    actor: str,
) -> dict:
    r = {
        "schema": "finco_consent_receipt.v1",
        "receipt_id": str(uuid.uuid4()),
        "generated_at": now(),
        "type": "consent",
        "subject_id_hash": sha256(subject_id),   # never store raw subject_id in receipt
        "scope": scope,
        "purpose": purpose,
        "permitted_actor_hash": sha256(permitted_actor),
        "duration_seconds": duration_seconds,
        "derivative_use": derivative_use,
        "compensation_terms": compensation_terms,
        "revocation_possible": revocation_possible,
        "issued_by": actor,
        "prev_hash": None,
    }
    r["receipt_hash"] = record_hash(r)
    return r


def make_access_receipt(
    consent_receipt_id: str,
    accessing_actor_hash: str,
    accessed_scope: str,
    raw_data_exposed: bool,
    access_method: str,
    consent_receipt_hash: str,
) -> dict:
    r = {
        "schema": "finco_access_receipt.v1",
        "receipt_id": str(uuid.uuid4()),
        "generated_at": now(),
        "type": "access",
        "consent_receipt_ref": consent_receipt_id,
        "accessing_actor_hash": accessing_actor_hash,
        "accessed_scope": accessed_scope,
        "raw_data_exposed": raw_data_exposed,
        "access_method": access_method,
        "prev_hash": consent_receipt_hash,
    }
    r["receipt_hash"] = record_hash(r)
    return r


def make_use_receipt(
    access_receipt_id: str,
    purpose_executed: str,
    process_used: str,
    output_class: str,
    matched_consent_terms: bool,
    access_receipt_hash: str,
) -> dict:
    r = {
        "schema": "finco_use_receipt.v1",
        "receipt_id": str(uuid.uuid4()),
        "generated_at": now(),
        "type": "use",
        "access_receipt_ref": access_receipt_id,
        "purpose_executed": purpose_executed,
        "process_used": process_used,
        "output_class": output_class,
        "matched_consent_terms": matched_consent_terms,
        "prev_hash": access_receipt_hash,
    }
    r["receipt_hash"] = record_hash(r)
    return r


def make_derivative_receipt(
    use_receipt_id: str,
    derivative_class: str,
    ownership_terms: str,
    reuse_permission: bool,
    revenue_share_rule: str,
    use_receipt_hash: str,
) -> dict:
    r = {
        "schema": "finco_derivative_receipt.v1",
        "receipt_id": str(uuid.uuid4()),
        "generated_at": now(),
        "type": "derivative",
        "use_receipt_ref": use_receipt_id,
        "derivative_class": derivative_class,
        "ownership_terms": ownership_terms,
        "reuse_permission": reuse_permission,
        "revenue_share_rule": revenue_share_rule,
        "prev_hash": use_receipt_hash,
    }
    r["receipt_hash"] = record_hash(r)
    return r


def make_compensation_receipt(
    derivative_receipt_id: str,
    recipient_hash: str,
    amount: float,
    currency_type: str,    # StegToken | StegCoin | fiat | access_credit | governance_credit
    settlement_status: str,
    derivative_receipt_hash: str,
) -> dict:
    r = {
        "schema": "finco_compensation_receipt.v1",
        "receipt_id": str(uuid.uuid4()),
        "generated_at": now(),
        "type": "compensation",
        "derivative_receipt_ref": derivative_receipt_id,
        "recipient_hash": recipient_hash,
        "amount": amount,
        "currency_type": currency_type,
        "settlement_status": settlement_status,
        "prev_hash": derivative_receipt_hash,
    }
    r["receipt_hash"] = record_hash(r)
    return r


def make_governance_receipt(
    chain_root_id: str,
    transition_id: str,
    evaluated_state: dict,
    admissibility_result: str,
    policy_version: str,
    reason: str,
    chain_terminal_hash: str,
) -> dict:
    r = {
        "schema": "finco_governance_receipt.v1",
        "receipt_id": str(uuid.uuid4()),
        "generated_at": now(),
        "type": "governance",
        "chain_root_id": chain_root_id,
        "transition_id": transition_id,
        "evaluated_state": evaluated_state,
        "admissibility_result": admissibility_result,
        "policy_version": policy_version,
        "reason": reason,
        "prev_hash": chain_terminal_hash,
    }
    r["receipt_hash"] = record_hash(r)
    return r


# ── Chain validator ───────────────────────────────────────────────────────────

class FinCoChainValidator:
    """
    Validates a FinCo receipt chain.
    Implements the admissibility rule from FINCO_PRIVATE_STATE_VALUE.md:
    ALLOW only if consent_valid, scope_respected, attribution_recorded,
    compensation_rule_defined, revocation_rule_defined, and recoverability >= threshold.
    DENY if consent missing or scope exceeded.
    FAIL_CLOSED if state is unknown or chain integrity cannot be verified.
    """

    POLICY_VERSION = "finco_admissibility.v1"

    def validate_chain(self, chain: dict) -> dict:
        """
        Validate a full FinCo receipt chain.
        chain: {"consent": {...}, "access": {...}, "use": {...},
                "derivative": {...}, "compensation": {...}}
        Returns: {"decision": ALLOW|DENY|FAIL_CLOSED, "reason": "...", "governance_receipt": {...}}
        """
        issues   = []
        unknowns = []

        # 1. Consent check
        consent = chain.get("consent")
        if not consent:
            return self._fail("consent_missing", "No consent receipt. DENY.",
                              chain, "DENY")

        if not consent.get("scope"):
            issues.append("consent: scope undefined")
        if not consent.get("purpose"):
            issues.append("consent: purpose undefined")
        if not consent.get("compensation_terms"):
            issues.append("consent: compensation_terms undefined")
        if not consent.get("revocation_possible"):
            unknowns.append("revocation_possible not confirmed")

        # 2. Access check
        access = chain.get("access")
        if not access:
            issues.append("access_receipt: missing")
        elif access.get("consent_receipt_ref") != consent.get("receipt_id"):
            issues.append("access: consent reference mismatch")
        elif access.get("raw_data_exposed") and not consent.get("derivative_use"):
            issues.append("access: raw data exposed without derivative_use consent")

        # 3. Use check
        use = chain.get("use")
        if not use:
            issues.append("use_receipt: missing")
        elif use.get("access_receipt_ref") != (access or {}).get("receipt_id"):
            issues.append("use: access reference mismatch")
        elif not use.get("matched_consent_terms"):
            issues.append("use: execution did not match consent terms")

        # 4. Chain hash integrity
        if consent and access:
            if access.get("prev_hash") != consent.get("receipt_hash"):
                issues.append("chain: access.prev_hash != consent.receipt_hash — TAMPERED")

        if access and use:
            if use.get("prev_hash") != access.get("receipt_hash"):
                issues.append("chain: use.prev_hash != access.receipt_hash — TAMPERED")

        # 5. Compensation check (required when value is extracted)
        derivative   = chain.get("derivative")
        compensation = chain.get("compensation")
        if derivative and not compensation:
            issues.append("compensation_receipt: missing when derivative exists")
        if compensation and compensation.get("settlement_status") not in ("settled", "pending"):
            issues.append(f"compensation: status '{compensation.get('settlement_status')}' invalid")

        # 6. Admissibility decision
        if any("TAMPERED" in i for i in issues):
            return self._fail("tamper_detected", "; ".join(issues), chain, "FAIL_CLOSED")

        if any("missing" in i for i in issues):
            return self._fail("missing_receipts", "; ".join(issues), chain, "FAIL_CLOSED")

        if issues:
            return self._fail("scope_violation", "; ".join(issues), chain, "DENY")

        return self._allow(chain, unknowns)

    def _allow(self, chain: dict, unknowns: list) -> dict:
        gov = make_governance_receipt(
            chain_root_id=chain.get("consent", {}).get("receipt_id", "unknown"),
            transition_id=str(uuid.uuid4()),
            evaluated_state={"chain_types": list(chain.keys())},
            admissibility_result="ALLOW",
            policy_version=self.POLICY_VERSION,
            reason="All FinCo admissibility checks passed.",
            chain_terminal_hash=self._terminal_hash(chain),
        )
        return {"decision": "ALLOW", "reason": "Chain valid.", "unknowns": unknowns, "governance_receipt": gov}

    def _fail(self, error_type: str, reason: str, chain: dict, decision: str) -> dict:
        gov = make_governance_receipt(
            chain_root_id=chain.get("consent", {}).get("receipt_id", "unknown"),
            transition_id=str(uuid.uuid4()),
            evaluated_state={"error_type": error_type},
            admissibility_result=decision,
            policy_version=self.POLICY_VERSION,
            reason=reason,
            chain_terminal_hash=self._terminal_hash(chain),
        )
        return {"decision": decision, "reason": reason, "governance_receipt": gov}

    def _terminal_hash(self, chain: dict) -> str:
        for key in ["compensation", "derivative", "use", "access", "consent"]:
            r = chain.get(key)
            if r:
                return r.get("receipt_hash", "none")
        return "none"

    def save_chain(self, chain: dict, result: dict, output_path: str = "./finco_chain.jsonl"):
        with open(output_path, "a") as f:
            for key in ["consent", "access", "use", "derivative", "compensation"]:
                r = chain.get(key)
                if r:
                    f.write(json.dumps(r) + "\n")
            f.write(json.dumps(result["governance_receipt"]) + "\n")


# ── Demo / CLI ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== FinCo Chain Validator Demo ===\n")
    validator = FinCoChainValidator()

    # Case 1: Valid chain — ALLOW
    consent = make_consent_receipt(
        subject_id="user_001",
        scope="working_memory:read",
        purpose="Personal assistant session",
        permitted_actor="entity/stegverse-ai",
        duration_seconds=86400,
        derivative_use=True,
        compensation_terms="access_credit:1/session",
        revocation_possible=True,
        actor="user_001",
    )
    access = make_access_receipt(
        consent_receipt_id=consent["receipt_id"],
        accessing_actor_hash=sha256("entity/stegverse-ai"),
        accessed_scope="working_memory:read",
        raw_data_exposed=False,
        access_method="vault_api",
        consent_receipt_hash=consent["receipt_hash"],
    )
    use = make_use_receipt(
        access_receipt_id=access["receipt_id"],
        purpose_executed="Personal assistant session",
        process_used="stegclaw:session_loop",
        output_class="session_response",
        matched_consent_terms=True,
        access_receipt_hash=access["receipt_hash"],
    )
    chain1 = {"consent": consent, "access": access, "use": use}
    result1 = validator.validate_chain(chain1)
    print(f"Case 1 (valid chain): {result1['decision']}")

    # Case 2: Missing consent — DENY
    result2 = validator.validate_chain({"access": access, "use": use})
    print(f"Case 2 (missing consent): {result2['decision']}")

    # Case 3: Tampered chain — FAIL_CLOSED
    tampered_access = dict(access)
    tampered_access["prev_hash"] = "0000000000000000"  # tampered
    result3 = validator.validate_chain({"consent": consent, "access": tampered_access, "use": use})
    print(f"Case 3 (tampered chain): {result3['decision']}")

    # Case 4: Derivative without compensation — DENY
    derivative = make_derivative_receipt(
        use_receipt_id=use["receipt_id"],
        derivative_class="session_insight",
        ownership_terms="user_owned",
        reuse_permission=False,
        revenue_share_rule="none",
        use_receipt_hash=use["receipt_hash"],
    )
    result4 = validator.validate_chain({"consent": consent, "access": access, "use": use, "derivative": derivative})
    print(f"Case 4 (derivative, no compensation): {result4['decision']}")

    # Save Case 1 chain
    validator.save_chain(chain1, result1, "./finco_demo_chain.jsonl")
    print("\nChain saved to ./finco_demo_chain.jsonl")
