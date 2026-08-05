import copy
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_session_inventory",
    ROOT / "tools/verify_session_execution_inventory.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SessionInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(
            (
                ROOT
                / "data/session-consolidation/handoff-orchestration-session-20260804.json"
            ).read_text(encoding="utf-8")
        )

    @staticmethod
    def make_active(value):
        task = next(t for t in value["tasks"] if t["claim_state"] == "COMPLETE")
        task["claim_state"] = "CLAIMED_FOR_IMPLEMENTATION"
        task["claim_timestamp"] = "2026-08-05T02:05:00Z"
        task["claim_expiration_or_release_condition"] = "release after test evidence"
        task["expected_evidence"] = "test receipt"
        task["collision_boundaries"] = "test-only synthetic claim"
        task["next_task_after_release"] = "none"
        value["summary"]["complete"] -= 1
        value["summary"]["active_distinct_support"] += 1
        return task

    def test_current_inventory_allows(self):
        self.assertEqual(
            MODULE.verify(copy.deepcopy(self.payload))["terminal_decision"], "ALLOW"
        )

    def test_unassigned_task_denies(self):
        value = copy.deepcopy(self.payload)
        value["tasks"][0]["claim_state"] = "UNCLAIMED"
        value["inventory_hash"] = MODULE.canonical_hash(value, "inventory_hash")
        self.assertEqual(MODULE.verify(value)["terminal_decision"], "DENY")

    def test_active_claim_without_expiry_denies(self):
        value = copy.deepcopy(self.payload)
        active = self.make_active(value)
        active.pop("claim_expiration_or_release_condition")
        value["inventory_hash"] = MODULE.canonical_hash(value, "inventory_hash")
        result = MODULE.verify(value)
        self.assertEqual(result["terminal_decision"], "DENY")
        self.assertTrue(
            any(failure.endswith("claim_expiration_or_release_condition_missing") for failure in result["failures"])
        )

    def test_archive_ready_with_active_claim_denies(self):
        value = copy.deepcopy(self.payload)
        self.make_active(value)
        value["archive_state"] = "READY"
        value["inventory_hash"] = MODULE.canonical_hash(value, "inventory_hash")
        result = MODULE.verify(value)
        self.assertEqual(result["terminal_decision"], "DENY")
        self.assertIn("archive_ready_with_active_claims", result["failures"])


if __name__ == "__main__":
    unittest.main()
