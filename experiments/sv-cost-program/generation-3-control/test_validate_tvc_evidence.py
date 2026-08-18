from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from validate_tvc_evidence import EvidenceError, validate_bundle, validate_packet

CANONICAL = {
    "task_id": "SV-RECON-001",
    "final_state": {"balance": 75, "risk_score": 3, "standing": "active"},
    "decisions": [
        {"event_id": "E01", "status": "ALLOW", "reason": "CREDIT_APPLIED"},
        {"event_id": "E02", "status": "ALLOW", "reason": "DEBIT_WITHIN_BOUNDARY"},
        {"event_id": "E03", "status": "ALLOW", "reason": "RISK_WITHIN_BOUNDARY"},
        {"event_id": "E04", "status": "DENY", "reason": "MINIMUM_BALANCE_VIOLATION"},
        {"event_id": "E05", "status": "DENY", "reason": "MAXIMUM_RISK_VIOLATION"},
        {"event_id": "E06", "status": "ALLOW", "reason": "DEBIT_WITHIN_BOUNDARY"},
    ],
    "applied_count": 4,
    "denied_count": 2,
    "claim_boundary": "DETERMINISTIC_RECONSTRUCTION_ONLY",
}


def packet(provider: str) -> dict:
    model = {
        "openai": "control-openai-model",
        "anthropic": "control-anthropic-model",
        "deepseek": "control-deepseek-model",
        "kimi": "control-kimi-model",
    }[provider]
    return {
        "schema": "stegverse.tvc.provider-measurement-evidence.v1",
        "provider": provider,
        "provider_response_id": f"resp-{provider}",
        "model": model,
        "candidate_output": json.dumps(CANONICAL, separators=(",", ":")),
        "provider_usage": {"actual": 1},
        "normalized_usage": {"input_tokens": 10, "output_tokens": 5},
        "provider_api_key_transferred_to_consumer": False,
        "secret_material_returned": False,
        "cost_status": "REQUEST_BOUND_COST",
        "cost_basis": "EXACT_PROVIDER_USAGE_X_OFFICIAL_MODEL_RATE_CARD",
        "calculated_request_cost_usd": "0.000001000000",
        "rate_card": {
            "provider": provider,
            "model": model,
            "source": f"https://example.invalid/{provider}/official-rate-card",
            "observed_at": "2026-08-18T07:58:00-05:00",
        },
    }


class Generation3EvidenceValidatorTests(unittest.TestCase):
    def test_accepts_exact_control_packet(self) -> None:
        result = validate_packet(packet("deepseek"), "deepseek")
        self.assertEqual(result["secret_boundary"], "PASS")
        self.assertEqual(result["provider_authority_effect"], "NONE_CONTROL_EVIDENCE_ONLY")

    def test_rejects_secret_like_field(self) -> None:
        value = packet("openai")
        value["api_key"] = "forbidden"
        with self.assertRaises(EvidenceError):
            validate_packet(value, "openai")

    def test_rejects_non_request_bound_cost(self) -> None:
        value = packet("anthropic")
        value["cost_status"] = "ESTIMATE"
        with self.assertRaises(EvidenceError):
            validate_packet(value, "anthropic")

    def test_rejects_candidate_drift(self) -> None:
        value = packet("kimi")
        candidate = copy.deepcopy(CANONICAL)
        candidate["final_state"]["balance"] = 74
        value["candidate_output"] = json.dumps(candidate)
        with self.assertRaises(EvidenceError):
            validate_packet(value, "kimi")

    def test_bundle_requires_all_four_and_preserves_stegverse_primary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for provider in ("openai", "anthropic", "deepseek", "kimi"):
                (root / f"{provider}.json").write_text(json.dumps(packet(provider)), encoding="utf-8")
            result = validate_bundle(root)
            self.assertEqual(result["state"], "PASS_ALL_FOUR_TVC_CONTROL_ENVELOPES")
            self.assertEqual(result["primary_provider"], "stegverse_local")
            self.assertEqual(result["third_party_role"], "CONTROL_OR_FALLBACK_ONLY")
            self.assertFalse(result["provider_credentials_received"])
            self.assertFalse(result["publication_authority_granted"])


if __name__ == "__main__":
    unittest.main()
