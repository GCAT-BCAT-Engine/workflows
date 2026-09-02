from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

CANDIDATE = {
    "task_id":"SV-RECON-001",
    "final_state":{"balance":75,"risk_score":3,"standing":"active"},
    "decisions":[
        {"event_id":"E01","status":"ALLOW","reason":"CREDIT_APPLIED"},
        {"event_id":"E02","status":"ALLOW","reason":"DEBIT_WITHIN_BOUNDARY"},
        {"event_id":"E03","status":"ALLOW","reason":"RISK_WITHIN_BOUNDARY"},
        {"event_id":"E04","status":"DENY","reason":"MINIMUM_BALANCE_VIOLATION"},
        {"event_id":"E05","status":"DENY","reason":"MAXIMUM_RISK_VIOLATION"},
        {"event_id":"E06","status":"ALLOW","reason":"DEBIT_WITHIN_BOUNDARY"},
    ],
    "applied_count":4,
    "denied_count":2,
    "claim_boundary":"DETERMINISTIC_RECONSTRUCTION_ONLY",
}

class AcquisitionToolsTest(unittest.TestCase):
    def test_hosted_ingestion_writes_credentialless_record(self):
        with tempfile.TemporaryDirectory() as td:
            td=pathlib.Path(td)
            src=td/"candidate.json"; src.write_text(json.dumps(CANDIDATE))
            dest=td/"hosted.json"
            cp=subprocess.run([
                sys.executable,str(TOOLS/"ingest_glm_hosted_candidate.py"),str(src),
                "--dest",str(dest),"--input-tokens","10","--output-tokens","5"
            ],capture_output=True,text=True)
            self.assertEqual(cp.returncode,0,cp.stderr)
            record=json.loads(dest.read_text())
            self.assertFalse(record["provider_api_key_transferred_to_stegverse"])
            self.assertEqual(record["provider"],"zai")
            self.assertEqual(record["candidate_output"],CANDIDATE)

    def test_hosted_ingestion_rejects_secret_like_fields(self):
        with tempfile.TemporaryDirectory() as td:
            td=pathlib.Path(td)
            src=td/"candidate.json"
            src.write_text(json.dumps({"api_key":"forbidden","candidate_output":CANDIDATE}))
            cp=subprocess.run([
                sys.executable,str(TOOLS/"ingest_glm_hosted_candidate.py"),str(src),
                "--dest",str(td/"out.json")
            ],capture_output=True,text=True)
            self.assertNotEqual(cp.returncode,0)

    def test_sovereign_builder_marks_vendor_credential_false(self):
        with tempfile.TemporaryDirectory() as td:
            td=pathlib.Path(td)
            src=td/"candidate.json"; src.write_text(json.dumps(CANDIDATE))
            dest=td/"sovereign.json"
            cp=subprocess.run([
                sys.executable,str(TOOLS/"build_glm_sovereign_evidence.py"),str(src),
                "--runtime-identity","test-runtime","--elapsed-seconds","1.25","--dest",str(dest)
            ],capture_output=True,text=True)
            self.assertEqual(cp.returncode,0,cp.stderr)
            record=json.loads(dest.read_text())
            self.assertFalse(record["vendor_api_credential_used"])
            self.assertEqual(record["runtime_identity"],"test-runtime")

if __name__ == "__main__":
    unittest.main()
