#!/usr/bin/env python3
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import harness


class HarnessTests(unittest.TestCase):
    def receipt(self, text: str, platform: str = "openai") -> harness.NativeReceipt:
        return harness.NativeReceipt(
            lane_id=platform,
            platform=platform,
            route="synchronous",
            model="fixture",
            attempt=1,
            started_at_epoch=0.0,
            latency_seconds=1.0,
            request_id="fixture-id",
            status="completed",
            input_tokens=100,
            output_tokens=50,
            cached_input_tokens=0,
            native_text=text,
            native_payload={"fixture": True},
            prompt_hash="sha256:prompt",
            output_hash=harness.sha256_text(text),
        )

    def valid_object(self):
        return {
            "task_identity": "SV-COST-NORMALIZED-001:1.0.0",
            "conclusion": "ALLOW(t) iff GBP(t) and BD(t) and OC(t).",
            "claims": ["necessity", "sufficiency"],
            "evidence": ["stipulated evaluator contract"],
            "unresolved": ["deployed implementation binding is unresolved"],
            "boundary": ["abstract logical core only"],
            "lean_candidate": "theorem x : True := by trivial",
            "obligations": {name: True for name in harness.CONTRACT["required_obligations"]},
        }

    def test_json_fence_is_normalized(self):
        text = "```json\n" + json.dumps(self.valid_object()) + "\n```"
        normalized = harness.normalize(self.receipt(text))
        self.assertEqual(normalized["lane_id"], "openai")
        self.assertTrue(normalized["obligations"]["allow_iff"])

    def test_phrase_variation_does_not_block(self):
        obj = self.valid_object()
        obj["claims"] = ["The forward direction holds.", "The converse direction holds."]
        normalized = harness.normalize(self.receipt(json.dumps(obj)))
        decision = harness.adjudicate(normalized)
        self.assertEqual(decision["classification"], "comparable")

    def test_missing_obligation_is_structured(self):
        obj = self.valid_object()
        obj["obligations"]["lean_candidate"] = False
        normalized = harness.normalize(self.receipt(json.dumps(obj)))
        decision = harness.adjudicate(normalized)
        self.assertEqual(decision["classification"], "non-comparable")
        self.assertIn("lean_candidate", decision["missing_obligations"])

    def test_provider_cost_is_deterministic(self):
        receipt = self.receipt(json.dumps(self.valid_object()), "openai")
        cost = harness.provider_cost(receipt)
        expected = (100 * 5.0 + 50 * 30.0) / 1_000_000
        self.assertAlmostEqual(cost["observed_provider_cost_usd"], expected)
        self.assertAlmostEqual(cost["batch_normalized_cost_usd"], expected * 0.5)

    def test_stegverse_has_zero_external_provider_cost(self):
        receipt = self.receipt(json.dumps(self.valid_object()), "stegverse-only")
        receipt.route = "repository-native"
        cost = harness.provider_cost(receipt)
        self.assertEqual(cost["observed_provider_cost_usd"], 0.0)
        self.assertIsNone(cost["batch_normalized_cost_usd"])
        self.assertEqual(cost["local_cost_status"], "UNMEASURED_LOCAL_RUNTIME")


if __name__ == "__main__":
    unittest.main()
