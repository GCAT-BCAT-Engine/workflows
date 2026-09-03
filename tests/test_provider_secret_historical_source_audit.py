from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]

class HistoricalSourceAuditTests(unittest.TestCase):
    def test_validator_passes(self):
        cp=subprocess.run(
            [sys.executable,str(ROOT/"tools/validate_provider_secret_historical_source_audit.py")],
            cwd=ROOT,capture_output=True,text=True
        )
        self.assertEqual(cp.returncode,0,cp.stderr+cp.stdout)
        self.assertIn("workflows=17",cp.stdout)
        self.assertIn("runtime_actor_token_visibility=UNRESOLVED_REQUIRES_ORG_AUDIT_LOG",cp.stdout)

    def test_every_entry_has_source_risk_and_explicit_runtime_boundary(self):
        doc=json.loads((ROOT/"security/provider-secret-historical-source-audit.v1.json").read_text())
        for e in doc["entries"]:
            self.assertTrue(e["secret_names"],e["path"])
            self.assertEqual(e["historical_runtime_actor"],"UNRESOLVED_REQUIRES_ORG_AUDIT_LOG")
            self.assertEqual(e["historical_token_provenance"],"UNRESOLVED_REQUIRES_ORG_AUDIT_LOG")
            self.assertEqual(e["repository_visibility_at_execution"],"UNRESOLVED_REQUIRES_ORG_AUDIT_LOG")

if __name__=="__main__":
    unittest.main()
