import importlib.util
import json
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("plan_test_lanes", ROOT / "plan_test_lanes.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)

TestLanesError = MODULE.TestLanesError
plan_manifest = MODULE.plan_manifest
validate_manifest = MODULE.validate_manifest


def reference_manifest():
    return json.loads((ROOT / "manifests" / "sv-cost-nine-lane.v1.json").read_text(encoding="utf-8"))


def resolution(capsule_id, provider, capability, state):
    return {
        "capsule_id": capsule_id,
        "provider": provider,
        "capability": capability,
        "state": state,
        "credential_material_returned": False,
    }


class TestPortableTestLanes(unittest.TestCase):
    def test_reference_manifest_is_valid_nine_lane_stegverse_primary(self):
        result = validate_manifest(reference_manifest())
        self.assertEqual(result["state"], "VALID")
        self.assertEqual(result["lane_count"], 9)
        self.assertEqual(result["primary_lane_count"], 1)
        self.assertFalse(result["manifest_contains_credentials"])

    def test_portable_plan_requires_only_capsule_resolution_for_external_lanes(self):
        result = plan_manifest(reference_manifest())
        self.assertEqual(result["state"], "CAPSULE_RESOLUTION_REQUIRED")
        local = next(item for item in result["lanes"] if item["provider"] == "stegverse_local")
        self.assertEqual(local["state"], "READY_LOCAL_PRIMARY")
        self.assertEqual(local["credential_material_in_request"], False)
        external = [item for item in result["lanes"] if item["provider"] != "stegverse_local"]
        self.assertEqual(len(external), 8)
        self.assertTrue(all(item["state"] == "READY_FOR_TVC_CAPSULE_RESOLUTION" for item in external))

    def test_unbound_optional_provider_lanes_skip_without_blocking_primary(self):
        manifest = reference_manifest()
        resolutions = {"resolutions": [
            resolution("openai.user.default", "openai", "llm.measure.openai", "CREDENTIAL_BINDING_UNAVAILABLE"),
            resolution("anthropic.user.default", "anthropic", "llm.measure.anthropic", "CREDENTIAL_BINDING_UNAVAILABLE"),
            resolution("deepseek.user.default", "deepseek", "llm.measure.deepseek", "CREDENTIAL_BINDING_UNAVAILABLE"),
            resolution("kimi.user.default", "kimi", "llm.measure.kimi", "CREDENTIAL_BINDING_UNAVAILABLE"),
        ]}
        result = plan_manifest(manifest, capsule_resolutions=resolutions)
        self.assertEqual(result["state"], "READY")
        self.assertEqual(result["blockers"], [])
        external = [item for item in result["lanes"] if item["provider"] != "stegverse_local"]
        self.assertTrue(all(item["state"] == "SKIPPED_OPTIONAL_CREDENTIAL_UNBOUND" for item in external))

    def test_user_bound_provider_enables_its_lanes_only(self):
        resolutions = {"resolutions": [
            resolution("deepseek.user.default", "deepseek", "llm.measure.deepseek", "READY")
        ]}
        result = plan_manifest(reference_manifest(), capsule_resolutions=resolutions)
        deepseek = [item for item in result["lanes"] if item["provider"] == "deepseek"]
        self.assertTrue(all(item["state"] == "READY_FOR_TVC_EXECUTION" for item in deepseek))
        openai = [item for item in result["lanes"] if item["provider"] == "openai"]
        self.assertTrue(all(item["state"] == "READY_FOR_TVC_CAPSULE_RESOLUTION" for item in openai))

    def test_required_external_lane_fails_closed_when_unbound(self):
        manifest = reference_manifest()
        manifest["lanes"][0]["required"] = True
        resolutions = {"resolutions": [
            resolution("openai.user.default", "openai", "llm.measure.openai", "CREDENTIAL_BINDING_UNAVAILABLE")
        ]}
        result = plan_manifest(manifest, capsule_resolutions=resolutions)
        self.assertEqual(result["state"], "BLOCKED")
        self.assertIn("REQUIRED_CREDENTIAL_BINDING_UNAVAILABLE:openai-raw", result["blockers"])

    def test_manifest_rejects_credential_reference_or_secret_value(self):
        manifest = reference_manifest()
        manifest["credential_ref"] = "vault://tvc/providers/openai/api-key"
        with self.assertRaisesRegex(TestLanesError, "credential-bearing field prohibited"):
            validate_manifest(manifest)

    def test_third_party_cannot_be_promoted_to_primary(self):
        manifest = reference_manifest()
        manifest["lanes"][0]["provider_role"] = "PRIMARY"
        with self.assertRaisesRegex(TestLanesError, "third-party lane must be control/fallback only"):
            validate_manifest(manifest)

    def test_raw_lane_cannot_claim_governance_profile(self):
        manifest = reference_manifest()
        manifest["lanes"][0]["governance_profile"] = "fake-governance"
        with self.assertRaisesRegex(TestLanesError, "raw lane cannot claim governance_profile"):
            validate_manifest(manifest)

    def test_plan_hash_is_deterministic(self):
        first = plan_manifest(reference_manifest())
        second = plan_manifest(reference_manifest())
        self.assertEqual(first["manifest_hash"], second["manifest_hash"])
        self.assertEqual(first["plan_hash"], second["plan_hash"])
        self.assertEqual([x["request_hash"] for x in first["lanes"]], [x["request_hash"] for x in second["lanes"]])

    def test_reference_manifest_contains_no_vault_or_provider_key_labels(self):
        text = (ROOT / "manifests" / "sv-cost-nine-lane.v1.json").read_text(encoding="utf-8")
        self.assertNotIn("vault://", text)
        for label in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY", "MOONSHOT_API_KEY"):
            self.assertNotIn(label, text)


if __name__ == "__main__":
    unittest.main()
