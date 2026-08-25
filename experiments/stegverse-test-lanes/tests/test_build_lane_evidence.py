import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SPEC = importlib.util.spec_from_file_location("builder", ROOT / "build_lane_evidence.py")
BUILDER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(BUILDER)

CSPEC = importlib.util.spec_from_file_location("comparator", ROOT / "compare_test_lanes.py")
COMPARATOR = importlib.util.module_from_spec(CSPEC)
assert CSPEC and CSPEC.loader
CSPEC.loader.exec_module(COMPARATOR)


REQUIRED = {
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
TASK = {"task_id": "SV-RECON-001", "required_output": REQUIRED}
OUTPUT = json.dumps(REQUIRED, sort_keys=True, separators=(",", ":"))


def lane(lane_id, provider, role, mode, governance_profile=None, model=None):
    return {
        "test_id": "SV-COST-NINE-LANE-v1",
        "lane_id": lane_id,
        "state": "READY_LOCAL_PRIMARY" if provider == "stegverse_local" else "READY_FOR_TVC_EXECUTION",
        "provider": provider,
        "provider_role": role,
        "mode": mode,
        "model": model,
        "governance_profile": governance_profile,
        "request_hash": BUILDER.digest_text("request:" + lane_id),
        "task_source_blob_sha": "1bd5a640bf067ffad87c427a5c12cb57c029b214",
    }


def plan():
    lanes = []
    for provider in ("openai", "anthropic"):
        lanes.append(lane(f"{provider}-raw", provider, "CONTROL_OR_FALLBACK_ONLY", "RAW"))
        lanes.append(lane(f"{provider}-governed", provider, "CONTROL_OR_FALLBACK_ONLY", "GOVERNED", "stegverse.default-governed.v1"))
    lanes.append(lane("stegverse-primary", "stegverse_local", "PRIMARY", "REFERENCE", "stegverse.default-governed.v1", "stegverse-reference-lm-v1"))
    for provider in ("deepseek", "kimi"):
        lanes.append(lane(f"{provider}-raw", provider, "CONTROL_OR_FALLBACK_ONLY", "RAW"))
        lanes.append(lane(f"{provider}-governed", provider, "CONTROL_OR_FALLBACK_ONLY", "GOVERNED", "stegverse.default-governed.v1"))
    return {
        "schema": "stegverse.test-lanes-plan.v1",
        "state": "READY",
        "test_id": "SV-COST-NINE-LANE-v1",
        "plan_hash": BUILDER.digest_text("plan"),
        "manifest_hash": BUILDER.digest_text("manifest"),
        "primary_provider": "stegverse_local",
        "credential_authority": "TV/TVC",
        "credential_material_present": False,
        "comparison": {"metrics": ["output_hash", "latency", "actual_usage", "request_bound_cost", "governance_outcome"]},
        "lanes": lanes,
    }


def primary(p):
    return {
        "schema": "stegverse.test-lanes-primary-candidate.v1",
        "plan_hash": p["plan_hash"],
        "provider": "stegverse_local",
        "provider_role": "PRIMARY",
        "model": "stegverse-reference-lm-v1",
        "model_hash": BUILDER.digest_text("model"),
        "candidate_output": OUTPUT,
        "latency_ms": 2.5,
        "provider_usage": {"total_tokens": 32},
        "request_bound_cost": {
            "schema": "stegverse.test-lanes-request-bound-cost.v1",
            "status": "MEASURED_LOCAL_COST",
            "calculated_request_cost_usd": "0.000001000000",
            "cost_basis": "MEASURED_LOCAL_RESOURCE_USAGE_X_OBSERVED_UNIT_COST",
        },
        "credential_material_present": False,
        "third_party_inference_required": False,
    }


def external(p, provider):
    return {
        "schema": "stegverse.tvc.test-lane-external-candidate.v1",
        "plan_hash": p["plan_hash"],
        "provider": provider,
        "provider_role": "CONTROL_OR_FALLBACK_ONLY",
        "model": provider + "-model",
        "lane_ids": [f"{provider}-raw", f"{provider}-governed"],
        "candidate_output": OUTPUT,
        "provider_response_id": provider + "-response",
        "provider_usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
        "request_bound_cost": {
            "schema": "stegverse.test-lanes-request-bound-cost.v1",
            "status": "REQUEST_BOUND_COST",
            "calculated_request_cost_usd": "0.000002000000",
            "cost_basis": "EXACT_PROVIDER_USAGE_X_OFFICIAL_MODEL_RATE_CARD",
        },
        "lease_receipt_sha256": BUILDER.digest_text(provider + "-lease"),
        "use_receipt": {"started_ns": 1000, "finished_ns": 2001000},
        "credential_material_present": False,
    }


class EvidenceBuilderTests(unittest.TestCase):
    def test_builds_nine_records_and_comparator_passes(self):
        p = plan()
        bundle = BUILDER.build_bundle(
            plan=p,
            task=TASK,
            primary_candidate=primary(p),
            external_candidates=[external(p, x) for x in ("openai", "anthropic", "deepseek", "kimi")],
        )
        self.assertEqual(bundle["lane_count"], 9)
        self.assertEqual(len(bundle["lanes"]), 9)
        self.assertFalse(bundle["credential_material_present"])
        for provider in ("openai", "anthropic", "deepseek", "kimi"):
            raw = next(x for x in bundle["lanes"] if x["lane_id"] == f"{provider}-raw")
            governed = next(x for x in bundle["lanes"] if x["lane_id"] == f"{provider}-governed")
            self.assertEqual(raw["output_hash"], governed["output_hash"])
            self.assertIsNone(raw["governance"])
            self.assertEqual(governed["governance"]["outcome"], "ALLOW")
        comparison = COMPARATOR.compare(p, bundle)
        self.assertEqual(comparison["state"], "PASS")
        self.assertEqual(comparison["lane_evidence_count"], 9)
        self.assertEqual(comparison["blockers"], [])

    def test_missing_request_bound_cost_fails_closed(self):
        p = plan()
        candidate = external(p, "openai")
        candidate.pop("request_bound_cost")
        with self.assertRaisesRegex(BUILDER.LaneEvidenceBuildError, "request-bound cost missing: openai"):
            BUILDER.build_bundle(
                plan=p,
                task=TASK,
                primary_candidate=primary(p),
                external_candidates=[candidate, external(p, "anthropic"), external(p, "deepseek"), external(p, "kimi")],
            )

    def test_missing_external_candidate_fails_closed(self):
        p = plan()
        with self.assertRaisesRegex(BUILDER.LaneEvidenceBuildError, "missing external candidate"):
            BUILDER.build_bundle(
                plan=p,
                task=TASK,
                primary_candidate=primary(p),
                external_candidates=[external(p, x) for x in ("openai", "anthropic", "deepseek")],
            )

    def test_governance_denies_wrong_candidate_without_changing_candidate_hash(self):
        p = plan()
        bad = external(p, "openai")
        bad["candidate_output"] = '{"task_id":"SV-RECON-001","final_state":{}}'
        bundle = BUILDER.build_bundle(
            plan=p,
            task=TASK,
            primary_candidate=primary(p),
            external_candidates=[bad, external(p, "anthropic"), external(p, "deepseek"), external(p, "kimi")],
        )
        raw = next(x for x in bundle["lanes"] if x["lane_id"] == "openai-raw")
        governed = next(x for x in bundle["lanes"] if x["lane_id"] == "openai-governed")
        self.assertEqual(raw["output_hash"], governed["output_hash"])
        self.assertEqual(governed["governance"]["outcome"], "DENY")


if __name__ == "__main__":
    unittest.main()
