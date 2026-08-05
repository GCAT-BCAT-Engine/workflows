import copy
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verify_session_inventory", ROOT / "tools/verify_session_execution_inventory.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

class SessionInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads((ROOT / "data/session-consolidation/handoff-orchestration-session-20260804.json").read_text())

    def test_current_inventory_allows(self):
        self.assertEqual(MODULE.verify(copy.deepcopy(self.payload))["terminal_decision"], "ALLOW")

    def test_unassigned_task_denies(self):
        value = copy.deepcopy(self.payload)
        value["tasks"][0]["claim_state"] = "UNCLAIMED"
        value["inventory_hash"] = MODULE.canonical_hash(value, "inventory_hash")
        self.assertEqual(MODULE.verify(value)["terminal_decision"], "DENY")

    def test_active_claim_without_expiry_denies(self):
        value = copy.deepcopy(self.payload)
        active = next(t for t in value["tasks"] if t["claim_state"] == "CLAIMED_FOR_IMPLEMENTATION")
        active.pop("claim_expiration_or_release_condition")
        value["inventory_hash"] = MODULE.canonical_hash(value, "inventory_hash")
        self.assertEqual(MODULE.verify(value)["terminal_decision"], "DENY")

    def test_archive_ready_with_active_claim_denies(self):
        value = copy.deepcopy(self.payload)
        value["archive_state"] = "READY"
        value["inventory_hash"] = MODULE.canonical_hash(value, "inventory_hash")
        self.assertEqual(MODULE.verify(value)["terminal_decision"], "DENY")

if __name__ == "__main__":
    unittest.main()
