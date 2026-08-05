import copy
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_handoff_semantic_adoption",
    ROOT / "tools/verify_handoff_semantic_adoption.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SemanticAdoptionRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(
            (ROOT / "data/handoff-semantic-adoption.json").read_text(encoding="utf-8")
        )

    def test_current_registry_allows(self):
        self.assertEqual(MODULE.verify(copy.deepcopy(self.payload))["terminal_decision"], "ALLOW")

    def test_pending_repository_denies(self):
        value = copy.deepcopy(self.payload)
        value["repositories"][0]["state"] = "PENDING_READ_ONLY"
        value["registry_hash"] = MODULE.canonical_hash(value, "registry_hash")
        self.assertEqual(MODULE.verify(value)["terminal_decision"], "DENY")

    def test_repair_enabled_denies(self):
        value = copy.deepcopy(self.payload)
        value["repositories"][0]["repair_enabled"] = True
        value["registry_hash"] = MODULE.canonical_hash(value, "registry_hash")
        self.assertEqual(MODULE.verify(value)["terminal_decision"], "DENY")

    def test_registry_tampering_denies(self):
        value = copy.deepcopy(self.payload)
        value["completion"]["complete_read_only"] = 4
        self.assertEqual(MODULE.verify(value)["terminal_decision"], "DENY")


if __name__ == "__main__":
    unittest.main()
