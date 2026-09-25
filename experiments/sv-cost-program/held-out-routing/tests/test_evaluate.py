"""Source-only oracle tests. These do not claim actual provider or sovereign runs."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("held_out_adjudicator", ROOT / "evaluate.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CASES = json.loads((ROOT / "cases.json").read_text())["cases"]


def observation(case):
    oracle = case["oracle"]
    return {
        "task_id": case["router_input"]["task_id"],
        "route": oracle["permitted_route"],
        "disposition": oracle["required_disposition"],
        "reason_code": oracle.get("reason_code", "EXPLICIT_POLICY_DISPOSITION"),
        "corrective_next_action": "obtain exact missing evidence and resubmit",
        "predecessor_receipt_hash": "sha256:fixture-predecessor-not-real",
        "manifest_sha256": "sha256:fixture-manifest-not-real",
        "route_decision_receipt_id": "fixture-only-not-runtime",
        "route_decision_elapsed_seconds": 0.01,
        "full_lifecycle_cost": {"status": "UNKNOWN", "total_usd": None}
    }


class SourceOnlyAdjudication(unittest.TestCase):
    def test_four_frozen_oracles(self):
        for case in CASES:
            with self.subTest(case=case["id"]):
                result = MODULE.adjudicate(case, observation(case))
                self.assertEqual(result["source_adjudication"], "PASS")
                self.assertEqual(result["authentic_runtime_state"], "NOT_VERIFIED_BY_OFFLINE_ADJUDICATOR")

    def test_mismatched_task_and_route_fail(self):
        case = CASES[0]
        obs = observation(case)
        obs["task_id"] = "OTHER-TASK"
        obs["route"] = "FRESH_INFERENCE"
        self.assertIn("TASK_ID_MISMATCH", MODULE.adjudicate(case, obs)["errors"])
        self.assertIn("ROUTE_ORACLE_MISMATCH", MODULE.adjudicate(case, obs)["errors"])

    def test_missing_predecessor_denied(self):
        case = CASES[0]
        obs = observation(case)
        obs.pop("predecessor_receipt_hash")
        self.assertIn("MISSING_PREDECESSOR_LINK", MODULE.adjudicate(case, obs)["errors"])

    def test_nonallow_must_be_actionable(self):
        case = CASES[2]
        obs = observation(case)
        obs.pop("corrective_next_action")
        self.assertIn("NON_ALLOW_NOT_ACTIONABLE", MODULE.adjudicate(case, obs)["errors"])

    def test_unknown_cost_is_not_free(self):
        case = CASES[0]
        obs = observation(case)
        obs["full_lifecycle_cost"]["total_usd"] = 0
        self.assertIn("UNKNOWN_COST_MUST_NOT_BE_ZERO_OR_NUMERIC", MODULE.adjudicate(case, obs)["errors"])

    def test_fail_closed_cannot_retry(self):
        case = CASES[2]
        obs = observation(case)
        obs["disposition"] = "FAIL_CLOSED"
        obs["retry_authorized"] = True
        self.assertIn("TERMINAL_FAIL_CLOSED_RETRY_FORBIDDEN", MODULE.adjudicate(case, obs)["errors"])


if __name__ == "__main__":
    unittest.main()
