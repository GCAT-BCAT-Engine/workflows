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

    def test_installed_glm_hosted_candidate_matches_deterministic_semantics(self):
        path=ROOT/"candidate-inputs"/"glm-hosted.json"
        self.assertTrue(path.exists())
        record=json.loads(path.read_text())
        self.assertEqual(record["provider"],"zai")
        self.assertEqual(record["model"],"GLM-5.3-Flash")
        self.assertFalse(record["provider_api_key_transferred_to_stegverse"])
        candidate=record["candidate_output"]
        self.assertEqual(candidate["task_id"],"SV-RECON-001")
        self.assertEqual(candidate["final_state"],{"balance":75,"risk_score":3,"standing":"active"})
        self.assertEqual(
            [(x["event_id"],x["status"]) for x in candidate["decisions"]],
            [("E01","ALLOW"),("E02","ALLOW"),("E03","ALLOW"),("E04","DENY"),("E05","DENY"),("E06","ALLOW")]
        )
        self.assertEqual(candidate["applied_count"],4)
        self.assertEqual(candidate["denied_count"],2)
        self.assertEqual(candidate["claim_boundary"],"DETERMINISTIC_RECONSTRUCTION_ONLY")


    def test_resident_intake_installs_exact_sovereign_evidence(self):
        evidence={"model":"GLM-5.3-Flash","task_id":"SV-RECON-001","vendor_api_credential_used":False,"runtime_identity":"resident-glm53","endpoint_class":"SOVEREIGN_OPENAI_COMPATIBLE","candidate_output":CANDIDATE,"metrics":{"elapsed_seconds":1.25,"energy_kwh":None,"hardware_amortization_usd":None,"energy_cost_usd":None,"storage_network_runtime_overhead_usd":None}}
        with tempfile.TemporaryDirectory() as td:
            td=pathlib.Path(td); src=td/"resident.json"; src.write_text(json.dumps(evidence))
            dest=td/"runtime-evidence"/"glm-sovereign.json"; receipt=td/"evidence"/"intake.json"
            cp=subprocess.run([sys.executable,str(TOOLS/"ingest_glm_sovereign_resident_evidence.py"),str(src),"--dest",str(dest),"--receipt",str(receipt)],capture_output=True,text=True)
            self.assertEqual(cp.returncode,0,cp.stderr)
            installed=json.loads(dest.read_text()); result=json.loads(receipt.read_text())
            self.assertEqual(installed["candidate_output"],CANDIDATE)
            self.assertFalse(installed["vendor_api_credential_used"])
            self.assertEqual(result["authority_effect"],"NONE_EVIDENCE_INTAKE_ONLY")
            self.assertFalse(result["network_fetch_performed"])
            self.assertFalse(result["provider_operation_performed"])

    def test_resident_intake_rejects_secret_and_semantic_mismatch(self):
        evidence={"model":"GLM-5.3-Flash","task_id":"SV-RECON-001","vendor_api_credential_used":False,"runtime_identity":"resident-glm53","endpoint_class":"SOVEREIGN_OPENAI_COMPATIBLE","candidate_output":CANDIDATE,"metrics":{"elapsed_seconds":1.0}}
        with tempfile.TemporaryDirectory() as td:
            td=pathlib.Path(td); src=td/"resident.json"
            bad=json.loads(json.dumps(evidence)); bad["candidate_output"]["api_key"]="forbidden"; src.write_text(json.dumps(bad))
            cp=subprocess.run([sys.executable,str(TOOLS/"ingest_glm_sovereign_resident_evidence.py"),str(src),"--dest",str(td/"out.json"),"--receipt",str(td/"receipt.json")],capture_output=True,text=True)
            self.assertNotEqual(cp.returncode,0)
            bad=json.loads(json.dumps(evidence)); bad["candidate_output"]["final_state"]["balance"]=74; src.write_text(json.dumps(bad))
            cp=subprocess.run([sys.executable,str(TOOLS/"ingest_glm_sovereign_resident_evidence.py"),str(src),"--dest",str(td/"out2.json"),"--receipt",str(td/"receipt2.json")],capture_output=True,text=True)
            self.assertNotEqual(cp.returncode,0)

if __name__ == "__main__":
    unittest.main()
