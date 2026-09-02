from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "ingest_glm_sovereign_resident_evidence.py"

CANDIDATE = {
    "task_id": "SV-RECON-001",
    "final_state": {"balance": 75, "risk_score": 3, "standing": "active"},
    "decisions": [
        {"event_id": "E01", "status": "ALLOW", "reason": "CREDIT_APPLIED"},
        {"event_id": "E02", "status": "ALLOW", "reason": "DEBIT_WITHIN_BOUNDARY"},
        {"event_id": "E03", "status": "ALLOW", "reason": "RISK_WITHIN_BOUNDARY"},
        {"event_id": "E04", "status": "DENY", "reason": "MINIMUM_BALANCE_VIOLATION"},
        {"event_id": "E05", "status": "DENY", "reason": "MAXIMUM_RISK_VIOLATION"},
        {"event_id": "E06", "status": "ALLOW", "reason": "DEBIT_WITHIN_BOUNDARY"},
    ],
    "applied_count": 4,
    "denied_count": 2,
    "claim_boundary": "DETERMINISTIC_RECONSTRUCTION_ONLY",
}

EVIDENCE = {
    "model": "GLM-5.3-Flash",
    "task_id": "SV-RECON-001",
    "vendor_api_credential_used": False,
    "runtime_identity": "resident-glm53",
    "endpoint_class": "SOVEREIGN_OPENAI_COMPATIBLE",
    "candidate_output": CANDIDATE,
    "metrics": {
        "elapsed_seconds": 1.25,
        "energy_kwh": None,
        "hardware_amortization_usd": None,
        "energy_cost_usd": None,
        "storage_network_runtime_overhead_usd": None,
    },
}


class SovereignResidentEvidenceIntakeTests(unittest.TestCase):
    def run_tool(self, source: pathlib.Path, dest: pathlib.Path, receipt: pathlib.Path):
        return subprocess.run(
            [sys.executable, str(TOOL), str(source), "--dest", str(dest), "--receipt", str(receipt)],
            capture_output=True,
            text=True,
        )

    def test_installs_exact_resident_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            td = pathlib.Path(td)
            source = td / "source.json"
            dest = td / "runtime-evidence" / "glm-sovereign.json"
            receipt = td / "evidence" / "intake.json"
            source.write_text(json.dumps(EVIDENCE))
            cp = self.run_tool(source, dest, receipt)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            installed = json.loads(dest.read_text())
            result = json.loads(receipt.read_text())
            self.assertEqual(installed["candidate_output"], CANDIDATE)
            self.assertFalse(installed["vendor_api_credential_used"])
            self.assertEqual(result["state"], "INSTALLED")
            self.assertFalse(result["network_fetch_performed"])
            self.assertFalse(result["provider_operation_performed"])
            self.assertEqual(result["credential_authority"], "TV/TVC")
            self.assertEqual(result["authority_effect"], "NONE_EVIDENCE_INTAKE_ONLY")

    def test_accepts_micro_node_receipt_wrapper(self):
        with tempfile.TemporaryDirectory() as td:
            td = pathlib.Path(td)
            source = td / "receipt.json"
            dest = td / "out.json"
            receipt = td / "intake.json"
            source.write_text(json.dumps({
                "schema": "stegverse.glm53-sovereign-lane-evidence-receipt/v1",
                "state": "EVIDENCE_READY",
                "consumer_evidence": EVIDENCE,
                "credential_authority": "TV/TVC",
                "authority_effect": "NONE_EVIDENCE_ONLY",
            }))
            cp = self.run_tool(source, dest, receipt)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(json.loads(dest.read_text())["runtime_identity"], "resident-glm53")

    def test_rejects_credential_like_material(self):
        with tempfile.TemporaryDirectory() as td:
            td = pathlib.Path(td)
            source = td / "source.json"
            bad = json.loads(json.dumps(EVIDENCE))
            bad["candidate_output"]["api_key"] = "forbidden"
            source.write_text(json.dumps(bad))
            cp = self.run_tool(source, td / "out.json", td / "receipt.json")
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("forbidden credential-like fields", cp.stderr)

    def test_rejects_semantic_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            td = pathlib.Path(td)
            source = td / "source.json"
            bad = json.loads(json.dumps(EVIDENCE))
            bad["candidate_output"]["final_state"]["balance"] = 74
            source.write_text(json.dumps(bad))
            cp = self.run_tool(source, td / "out.json", td / "receipt.json")
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn("final_state mismatch", cp.stderr)

    def test_first_write_wins_for_different_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            td = pathlib.Path(td)
            source = td / "source.json"
            dest = td / "out.json"
            receipt = td / "receipt.json"
            source.write_text(json.dumps(EVIDENCE))
            first = self.run_tool(source, dest, receipt)
            self.assertEqual(first.returncode, 0, first.stderr)
            different = json.loads(json.dumps(EVIDENCE))
            different["runtime_identity"] = "different-runtime"
            source.write_text(json.dumps(different))
            second = self.run_tool(source, dest, receipt)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("different sovereign evidence", second.stderr)

    def test_identical_reingest_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            td = pathlib.Path(td)
            source = td / "source.json"
            dest = td / "out.json"
            receipt = td / "receipt.json"
            source.write_text(json.dumps(EVIDENCE))
            self.assertEqual(self.run_tool(source, dest, receipt).returncode, 0)
            second = self.run_tool(source, dest, receipt)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(json.loads(receipt.read_text())["state"], "ALREADY_INSTALLED_IDENTICAL")


if __name__ == "__main__":
    unittest.main()
