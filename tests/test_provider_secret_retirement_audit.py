from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]


class ProviderSecretRetirementAuditTests(unittest.TestCase):
    def test_audit_validates(self):
        cp=subprocess.run(
            [sys.executable,str(ROOT/"tools/validate_provider_secret_retirement_audit.py")],
            cwd=ROOT,capture_output=True,text=True
        )
        self.assertEqual(cp.returncode,0,cp.stderr+cp.stdout)
        self.assertIn("retired_workflows=17",cp.stdout)
        self.assertIn("active_direct_provider_secret_workflows=0",cp.stdout)

    def test_all_retired_paths_are_absent(self):
        doc=json.loads((ROOT/"security/provider-secret-workflow-retirement-audit.v1.json").read_text())
        self.assertEqual(len(doc["retired_workflows"]),17)
        for entry in doc["retired_workflows"]:
            self.assertFalse((ROOT/entry["path"]).exists(),entry["path"])


if __name__=="__main__":
    unittest.main()
