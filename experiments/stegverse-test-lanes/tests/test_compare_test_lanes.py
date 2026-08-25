import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PLAN_SPEC = importlib.util.spec_from_file_location("plan_test_lanes", ROOT / "plan_test_lanes.py")
PLAN = importlib.util.module_from_spec(PLAN_SPEC)
assert PLAN_SPEC and PLAN_SPEC.loader
PLAN_SPEC.loader.exec_module(PLAN)

COMPARE_SPEC = importlib.util.spec_from_file_location("compare_test_lanes", ROOT / "compare_test_lanes.py")
COMPARE = importlib.util.module_from_spec(COMPARE_SPEC)
assert COMPARE_SPEC and COMPARE_SPEC.loader
COMPARE_SPEC.loader.exec_module(COMPARE)


def manifest():
    return json.loads((ROOT / "manifests" / "sv-cost-nine-lane.v1.json").read_text(encoding="utf-8"))


def capsule_resolution(capsule_id, provider, capability, state):
    return {
        "capsule_id": capsule_id,
        "provider": provider,
        "capability": capability,
        "state": state,
        "credential_material_returned": False,
    }


def all_external_unbound():
    return {"resolutions": [
        capsule_resolution("openai.user.default", "openai", "llm.measure.openai", "CREDENTIAL_BINDING_UNAVAILABLE"),
        capsule_resolution("anthropic.user.default", "anthropic", "llm.measure.anthropic", "CREDENTIAL_BINDING_UNAVAILABLE"),
        capsule_resolution("deepseek.user.default", "deepseek", "llm.measure.deepseek", "CREDENTIAL_BINDING_UNAVAILABLE"),
        capsule_resolution("kimi.user.default", "kimi", "llm.measure.kimi", "CREDENTIAL_BINDING_UNAVAILABLE"),
    ]}


def evidence_for(request, output="reference-output", *, model=None, governance_outcome="ALLOW"):
    governance = None
    if request["mode"] == "GOVERNED":
        governance = {"profile": request["governance_profile"], "outcome": governance_outcome}
    return {
        "schema": "stegverse.test-lane-evidence.v1",
        "test_id": request["test_id"],
        "lane_id": request["lane_id"],
        "request_hash": request["request_hash"],
        "provider": request["provider"],
        "provider_role": request["provider_role"],
        "mode": request["mode"],
        "model": request["model"] if request["model"] is not None else model,
        "task_source_blob_sha": request["task_source_blob_sha"],
        "output": output,
        "output_hash": COMPARE.output_hash(output),
        "latency_ms": 12.5,
        "usage": {"total_tokens": 10},
        "cost": {
            "schema": "stegverse.test-lanes-request-bound-cost.v1",
            "status": "MEASURED_LOCAL_COST" if request["provider"] == "stegverse_local" else "REQUEST_BOUND_COST",
            "calculated_request_cost_usd": "0.000001000000",
            "cost_basis": "MEASURED_LOCAL_RESOURCE_USAGE_X_OBSERVED_UNIT_COST" if request["provider"] == "stegverse_local" else "EXACT_PROVIDER_USAGE_X_OFFICIAL_MODEL_RATE_CARD",
        },
        "governance": governance,
        "provider_evidence": None,
        "credential_material_present": False,
        "execution_authority_granted": False,
    }


class TestLaneComparison(unittest.TestCase):
    def test_local_only_execution_passes_when_external_lanes_are_optional_unbound(self):
        plan = PLAN.plan_manifest(manifest(), capsule_resolutions=all_external_unbound())
        self.assertEqual(plan["state"], "READY")
        local = next(item for item in plan["lanes"] if item["state"] == "READY_LOCAL_PRIMARY")
        bundle = {
            "schema": "stegverse.test-lanes-evidence-bundle.v1",
            "test_id": plan["test_id"],
            "plan_hash": plan["plan_hash"],
            "credential_material_present": False,
            "lanes": [evidence_for(local)],
        }
        result = COMPARE.compare(plan, bundle)
        self.assertEqual(result["state"], "PASS")
        self.assertEqual(result["lane_evidence_count"], 1)
        self.assertEqual(result["blockers"], [])
        executed = [item for item in result["results"] if "output_hash" in item]
        self.assertEqual(len(executed), 1)
        self.assertTrue(executed[0]["matches_primary_output"])

    def test_bound_external_provider_compares_against_primary(self):
        resolutions = all_external_unbound()
        resolutions["resolutions"] = [
            item for item in resolutions["resolutions"] if item["provider"] != "deepseek"
        ] + [capsule_resolution("deepseek.user.default", "deepseek", "llm.measure.deepseek", "READY")]
        plan = PLAN.plan_manifest(manifest(), capsule_resolutions=resolutions)
        ready = [item for item in plan["lanes"] if item["state"] in COMPARE.READY_STATES]
        bundle_items = []
        for request in ready:
            output = "same" if request["provider"] != "deepseek" or request["mode"] == "RAW" else "different"
            bundle_items.append(evidence_for(request, output=output, model="deepseek-v4-flash"))
        bundle = {
            "schema": "stegverse.test-lanes-evidence-bundle.v1",
            "test_id": plan["test_id"],
            "plan_hash": plan["plan_hash"],
            "credential_material_present": False,
            "lanes": bundle_items,
        }
        result = COMPARE.compare(plan, bundle)
        self.assertEqual(result["state"], "PASS")
        deepseek = [item for item in result["results"] if item.get("provider") == "deepseek" and "output_hash" in item]
        self.assertEqual(len(deepseek), 2)
        self.assertTrue(any(item["matches_primary_output"] for item in deepseek))
        self.assertTrue(any(not item["matches_primary_output"] for item in deepseek))

    def test_missing_declared_request_bound_cost_fails_closed(self):
        plan = PLAN.plan_manifest(manifest(), capsule_resolutions=all_external_unbound())
        local = next(item for item in plan["lanes"] if item["state"] == "READY_LOCAL_PRIMARY")
        item = evidence_for(local)
        item["cost"] = None
        bundle = {
            "schema": "stegverse.test-lanes-evidence-bundle.v1",
            "test_id": plan["test_id"],
            "plan_hash": plan["plan_hash"],
            "credential_material_present": False,
            "lanes": [item],
        }
        with self.assertRaisesRegex(COMPARE.TestLaneEvidenceError, "request-bound cost missing"):
            COMPARE.compare(plan, bundle)

    def test_missing_ready_lane_evidence_blocks(self):
        plan = PLAN.plan_manifest(manifest(), capsule_resolutions=all_external_unbound())
        bundle = {
            "schema": "stegverse.test-lanes-evidence-bundle.v1",
            "test_id": plan["test_id"],
            "plan_hash": plan["plan_hash"],
            "credential_material_present": False,
            "lanes": [],
        }
        with self.assertRaisesRegex(COMPARE.TestLaneEvidenceError, "exactly one executed PRIMARY lane required"):
            COMPARE.compare(plan, bundle)

    def test_evidence_for_skipped_lane_blocks(self):
        plan = PLAN.plan_manifest(manifest(), capsule_resolutions=all_external_unbound())
        local = next(item for item in plan["lanes"] if item["state"] == "READY_LOCAL_PRIMARY")
        skipped = next(item for item in plan["lanes"] if item["state"] == "SKIPPED_OPTIONAL_CREDENTIAL_UNBOUND")
        bundle = {
            "schema": "stegverse.test-lanes-evidence-bundle.v1",
            "test_id": plan["test_id"],
            "plan_hash": plan["plan_hash"],
            "credential_material_present": False,
            "lanes": [evidence_for(local), evidence_for(skipped, model="external-model")],
        }
        result = COMPARE.compare(plan, bundle)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertIn(f"EVIDENCE_PRESENT_FOR_SKIPPED_LANE:{skipped['lane_id']}", result["blockers"])

    def test_output_hash_mismatch_rejected(self):
        plan = PLAN.plan_manifest(manifest(), capsule_resolutions=all_external_unbound())
        local = next(item for item in plan["lanes"] if item["state"] == "READY_LOCAL_PRIMARY")
        item = evidence_for(local)
        item["output_hash"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(COMPARE.TestLaneEvidenceError, "output hash mismatch"):
            COMPARE.validate_lane_evidence(local, item)

    def test_secret_like_evidence_field_rejected(self):
        plan = PLAN.plan_manifest(manifest(), capsule_resolutions=all_external_unbound())
        local = next(item for item in plan["lanes"] if item["state"] == "READY_LOCAL_PRIMARY")
        item = evidence_for(local)
        item["api_key"] = "not-a-real-key"
        with self.assertRaisesRegex(COMPARE.TestLaneEvidenceError, "credential-bearing evidence field prohibited"):
            COMPARE.validate_lane_evidence(local, item)

    def test_comparison_hash_is_deterministic(self):
        plan = PLAN.plan_manifest(manifest(), capsule_resolutions=all_external_unbound())
        local = next(item for item in plan["lanes"] if item["state"] == "READY_LOCAL_PRIMARY")
        bundle = {
            "schema": "stegverse.test-lanes-evidence-bundle.v1",
            "test_id": plan["test_id"],
            "plan_hash": plan["plan_hash"],
            "credential_material_present": False,
            "lanes": [evidence_for(local)],
        }
        first = COMPARE.compare(plan, bundle)
        second = COMPARE.compare(plan, bundle)
        self.assertEqual(first["comparison_hash"], second["comparison_hash"])


if __name__ == "__main__":
    unittest.main()
