from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
TOOL=ROOT/"tools"/"build_credentialless_ui_cost_evidence.py"


def base(provider="zai",model="GLM-5.3-Flash",mode="QUOTA_PERCENT"):
    return {
        "schema":"stegverse.credentialless-ui-cost-observation/v1",
        "provider":provider,
        "model":model,
        "task_id":"SV-RECON-001",
        "candidate_ref":f"candidate-inputs/{'glm-hosted' if provider=='zai' else provider}.json",
        "observation_mode":mode,
        "isolated_single_candidate_window":True,
        "before":{},
        "after":{},
        "subscription_monthly_equivalent_usd":None,
        "rate_key":None,
        "source_observation":{"provided_by":"user provider UI","before_sha256":"a","after_sha256":"b"},
        "provider_api_key_transferred_to_stegverse":False,
        "non_tv_tvc_secret_or_token_used":False,
        "claim_boundary":"CREDENTIALLESS_PROVIDER_UI_REQUEST_BOUND_OBSERVATION_ONLY",
    }


class CredentiallessUiCostBuilderTests(unittest.TestCase):
    def run_tool(self,payload):
        with tempfile.TemporaryDirectory() as td:
            td=pathlib.Path(td)
            src=td/"obs.json"; out=td/"cost.json"
            src.write_text(json.dumps(payload))
            cp=subprocess.run([sys.executable,str(TOOL),str(src),"--write",str(out)],capture_output=True,text=True)
            return cp, json.loads(out.read_text()) if out.exists() else None

    def test_quota_delta_allocates_subscription_effective_cost(self):
        x=base()
        x["before"]={"quota_percent_used":10.00}
        x["after"]={"quota_percent_used":10.02}
        x["subscription_monthly_equivalent_usd"]=31.249166666667
        cp,out=self.run_tool(x)
        self.assertEqual(cp.returncode,0,cp.stderr)
        self.assertEqual(out["basis"],"PROVIDER_UI_SUBSCRIPTION_QUOTA_ALLOCATED_EFFECTIVE_COST")
        self.assertEqual(out["cost_usd"],0.006249833333)
        self.assertTrue(out["observation_provenance"]["credentialless"])

    def test_usage_credit_delta_is_direct_request_cost(self):
        x=base("anthropic","claude-opus-5","USAGE_CREDIT_SPENT_USD")
        x["before"]={"usage_credit_spent_usd":0.54}
        x["after"]={"usage_credit_spent_usd":0.57}
        cp,out=self.run_tool(x)
        self.assertEqual(cp.returncode,0,cp.stderr)
        self.assertEqual(out["basis"],"PROVIDER_REPORTED_REQUEST_COST_USD")
        self.assertEqual(out["cost_usd"],0.03)

    def test_direct_request_cost_delta(self):
        x=base("openai","gpt-5.6-sol","DIRECT_REQUEST_COST_USD")
        x["before"]={"request_cost_usd":1.0000}
        x["after"]={"request_cost_usd":1.0025}
        cp,out=self.run_tool(x)
        self.assertEqual(cp.returncode,0,cp.stderr)
        self.assertEqual(out["cost_usd"],0.0025)

    def test_exact_token_delta_uses_bound_rate_card(self):
        x=base("openai","gpt-5.6-sol","EXACT_TOKENS")
        x["before"]={"input_tokens":10000,"cached_input_tokens":1000,"output_tokens":5000}
        x["after"]={"input_tokens":11000,"cached_input_tokens":1100,"output_tokens":5200}
        x["rate_key"]="openai:gpt-5.6-sol"
        cp,out=self.run_tool(x)
        self.assertEqual(cp.returncode,0,cp.stderr)
        self.assertEqual(out["basis"],"EXACT_USAGE_PLUS_BOUND_VERSIONED_RATE_CARD")
        self.assertEqual(out["provider_usage"],{"input_tokens":1000,"output_tokens":200,"cached_input_tokens":100})
        self.assertEqual(out["cost_usd"],0.00764)

    def test_nonisolated_window_is_rejected(self):
        x=base()
        x["isolated_single_candidate_window"]=False
        x["before"]={"quota_percent_used":10}
        x["after"]={"quota_percent_used":11}
        x["subscription_monthly_equivalent_usd"]=20
        cp,_=self.run_tool(x)
        self.assertNotEqual(cp.returncode,0)
        self.assertIn("isolate exactly one candidate",cp.stderr+cp.stdout)

    def test_decreasing_counter_is_rejected(self):
        x=base("anthropic","claude-opus-5","USAGE_CREDIT_SPENT_USD")
        x["before"]={"usage_credit_spent_usd":1.0}
        x["after"]={"usage_credit_spent_usd":0.9}
        cp,_=self.run_tool(x)
        self.assertNotEqual(cp.returncode,0)

    def test_secret_like_field_is_rejected(self):
        x=base()
        x["api_key"]="forbidden"
        x["before"]={"quota_percent_used":10}
        x["after"]={"quota_percent_used":11}
        x["subscription_monthly_equivalent_usd"]=20
        cp,_=self.run_tool(x)
        self.assertNotEqual(cp.returncode,0)
        self.assertIn("protected field prohibited",cp.stderr+cp.stdout)

    def test_zai_exact_tokens_without_verified_rate_key_is_rejected(self):
        x=base("zai","GLM-5.3-Flash","EXACT_TOKENS")
        x["before"]={"input_tokens":0,"output_tokens":0}
        x["after"]={"input_tokens":100,"output_tokens":50}
        x["rate_key"]="zai:GLM-5.3-Flash"
        cp,_=self.run_tool(x)
        self.assertNotEqual(cp.returncode,0)
        self.assertIn("unknown or unverified rate key",cp.stderr+cp.stdout)


if __name__=="__main__":
    unittest.main()
