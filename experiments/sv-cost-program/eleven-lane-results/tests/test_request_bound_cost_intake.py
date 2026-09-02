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


    def test_harness_consumes_installed_request_bound_cost(self):
        candidate_path=ROOT/"candidate-inputs"/"openai.json"
        cost_path=ROOT/"cost-evidence"/"openai.json"
        result_path=ROOT/"results"/"generation-3-eleven-lane"/"eleven_lane_generation_3_results.json"
        old_candidate=candidate_path.read_bytes() if candidate_path.exists() else None
        old_cost=cost_path.read_bytes() if cost_path.exists() else None
        try:
            candidate_path.parent.mkdir(parents=True,exist_ok=True)
            cost_path.parent.mkdir(parents=True,exist_ok=True)
            candidate_path.write_text(json.dumps(wrapper("openai","gpt-5.6-sol",{"input_tokens":1000,"output_tokens":200})))
            cost_path.write_text(json.dumps({
                "schema":"stegverse.request-bound-provider-cost-evidence/v1",
                "provider":"openai",
                "model":"gpt-5.6-sol",
                "task_id":"SV-RECON-001",
                "basis":"EXACT_USAGE_PLUS_BOUND_VERSIONED_RATE_CARD",
                "cost_usd":0.008,
                "provider_usage":{"input_tokens":1000,"output_tokens":200},
                "rate_card_ref":{"rate_key":"openai:gpt-5.6-sol"},
                "candidate_ref":"candidate-inputs/openai.json",
                "provider_api_key_transferred_to_stegverse":False,
                "non_tv_tvc_secret_or_token_used":False,
                "claim_boundary":"REQUEST_BOUND_EFFECTIVE_COST_ONLY",
            }))
            cp=subprocess.run([sys.executable,str(ROOT/"run.py")],capture_output=True,text=True)
            self.assertEqual(cp.returncode,0,cp.stderr)
            result=json.loads(result_path.read_text())
            raw=next(row for row in result["rows"] if row["lane_id"]=="openai-raw")
            governed=next(row for row in result["rows"] if row["lane_id"]=="openai-governed")
            self.assertEqual(raw["provider_cost_usd"],0.008)
            self.assertEqual(governed["provider_cost_usd"],0.008)
            self.assertEqual(raw["cost_evidence_ref"],"cost-evidence/openai.json")
            self.assertNotIn("MISSING_COST_EVIDENCE:openai-raw",result["cost_blockers"])
        finally:
            if old_candidate is None:
                candidate_path.unlink(missing_ok=True)
            else:
                candidate_path.write_bytes(old_candidate)
            if old_cost is None:
                cost_path.unlink(missing_ok=True)
            else:
                cost_path.write_bytes(old_cost)

    def test_harness_rejects_cost_bound_to_wrong_candidate(self):
        candidate_path=ROOT/"candidate-inputs"/"openai.json"
        cost_path=ROOT/"cost-evidence"/"openai.json"
        old_candidate=candidate_path.read_bytes() if candidate_path.exists() else None
        old_cost=cost_path.read_bytes() if cost_path.exists() else None
        try:
            candidate_path.parent.mkdir(parents=True,exist_ok=True)
            cost_path.parent.mkdir(parents=True,exist_ok=True)
            candidate_path.write_text(json.dumps(wrapper("openai","gpt-5.6-sol",{"input_tokens":1000,"output_tokens":200})))
            cost_path.write_text(json.dumps({
                "schema":"stegverse.request-bound-provider-cost-evidence/v1",
                "provider":"openai",
                "model":"gpt-5.6-sol",
                "task_id":"SV-RECON-001",
                "basis":"EXACT_USAGE_PLUS_BOUND_VERSIONED_RATE_CARD",
                "cost_usd":0.008,
                "provider_usage":{"input_tokens":1000,"output_tokens":200},
                "rate_card_ref":{"rate_key":"openai:gpt-5.6-sol"},
                "candidate_ref":"candidate-inputs/anthropic.json",
                "provider_api_key_transferred_to_stegverse":False,
                "non_tv_tvc_secret_or_token_used":False,
                "claim_boundary":"REQUEST_BOUND_EFFECTIVE_COST_ONLY",
            }))
            cp=subprocess.run([sys.executable,str(ROOT/"run.py")],capture_output=True,text=True)
            self.assertNotEqual(cp.returncode,0)
            self.assertIn("candidate binding mismatch",cp.stderr+cp.stdout)
        finally:
            if old_candidate is None:
                candidate_path.unlink(missing_ok=True)
            else:
                candidate_path.write_bytes(old_candidate)
            if old_cost is None:
                cost_path.unlink(missing_ok=True)
            else:
                cost_path.write_bytes(old_cost)


if __name__=="__main__":
    unittest.main()
