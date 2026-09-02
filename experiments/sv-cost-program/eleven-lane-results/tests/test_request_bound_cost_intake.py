from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
TOOL=ROOT/"tools"/"ingest_request_bound_provider_candidate.py"

CANDIDATE={
    "task_id":"SV-RECON-001",
    "final_state":{"balance":75,"risk_score":3,"standing":"active"},
    "decisions":[
        {"event_id":"E01","status":"ALLOW","reason":"x"},
        {"event_id":"E02","status":"ALLOW","reason":"x"},
        {"event_id":"E03","status":"ALLOW","reason":"x"},
        {"event_id":"E04","status":"DENY","reason":"x"},
        {"event_id":"E05","status":"DENY","reason":"x"},
        {"event_id":"E06","status":"ALLOW","reason":"x"},
    ],
    "applied_count":4,
    "denied_count":2,
    "claim_boundary":"DETERMINISTIC_RECONSTRUCTION_ONLY",
}


def wrapper(provider,model,usage):
    return {
        "provider":provider,
        "model":model,
        "task_id":"SV-RECON-001",
        "provider_api_key_transferred_to_stegverse":False,
        "provider_response_id":"response-safe-id",
        "provider_latency_seconds":0.25,
        "provider_usage":usage,
        "candidate_output":CANDIDATE,
    }


class RequestBoundCostIntakeTests(unittest.TestCase):
    def run_tool(self,payload,*extra):
        with tempfile.TemporaryDirectory() as td:
            td=pathlib.Path(td)
            src=td/"source.json"; src.write_text(json.dumps(payload))
            candidate=td/"candidate.json"; cost=td/"cost.json"
            cp=subprocess.run(
                [sys.executable,str(TOOL),str(src),"--candidate-dest",str(candidate),"--cost-dest",str(cost),*extra],
                capture_output=True,text=True
            )
            return cp, (json.loads(candidate.read_text()) if candidate.exists() else None), (json.loads(cost.read_text()) if cost.exists() else None)

    def test_openai_exact_usage_uses_bound_rate(self):
        cp,candidate,cost=self.run_tool(
            wrapper("openai","gpt-5.6-sol",{"input_tokens":1000,"output_tokens":200}),
            "--rate-key","openai:gpt-5.6-sol"
        )
        self.assertEqual(cp.returncode,0,cp.stderr)
        self.assertEqual(cost["basis"],"EXACT_USAGE_PLUS_BOUND_VERSIONED_RATE_CARD")
        self.assertEqual(cost["cost_usd"],0.008)
        self.assertFalse(candidate["provider_api_key_transferred_to_stegverse"])

    def test_anthropic_exact_usage_uses_bound_rate(self):
        cp,_,cost=self.run_tool(
            wrapper("anthropic","claude-opus-5",{"input_tokens":1000,"output_tokens":200}),
            "--rate-key","anthropic:claude-opus-5"
        )
        self.assertEqual(cp.returncode,0,cp.stderr)
        self.assertEqual(cost["cost_usd"],0.01)

    def test_deepseek_unspecified_model_is_rejected_by_rate_binding(self):
        cp,_,_=self.run_tool(
            wrapper("deepseek","DeepSeek (UI model unspecified)",{"input_tokens":1000,"output_tokens":200}),
            "--rate-key","deepseek:deepseek-v4-flash:peak:cache_miss"
        )
        self.assertNotEqual(cp.returncode,0)

    def test_credential_material_is_rejected(self):
        payload=wrapper("openai","gpt-5.6-sol",{"input_tokens":1000,"output_tokens":200})
        payload["api_key"]="forbidden"
        cp,_,_=self.run_tool(payload,"--rate-key","openai:gpt-5.6-sol")
        self.assertNotEqual(cp.returncode,0)

    def test_estimated_tokens_do_not_satisfy_exact_usage(self):
        payload=wrapper("openai","gpt-5.6-sol",{"estimated_input_tokens":1000,"estimated_output_tokens":200})
        cp,_,_=self.run_tool(payload,"--rate-key","openai:gpt-5.6-sol")
        self.assertNotEqual(cp.returncode,0)

    def test_zai_without_bound_rate_or_reported_cost_fails_closed(self):
        cp,_,_=self.run_tool(wrapper("zai","GLM-5.3-Flash",{}))
        self.assertNotEqual(cp.returncode,0)

    def test_provider_reported_cost_does_not_need_rate_card(self):
        cp,_,cost=self.run_tool(
            wrapper("zai","GLM-5.3-Flash",{}),
            "--reported-cost-usd","0.0025"
        )
        self.assertEqual(cp.returncode,0,cp.stderr)
        self.assertEqual(cost["basis"],"PROVIDER_REPORTED_REQUEST_COST_USD")
        self.assertEqual(cost["cost_usd"],0.0025)


if __name__=="__main__":
    unittest.main()
