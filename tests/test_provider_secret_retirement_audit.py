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
        self.assertIn("active_direct_provider_secret_consumers=0",cp.stdout)

    def test_all_retired_paths_are_contained_fail_closed(self):
        doc=json.loads((ROOT/"security/provider-secret-workflow-retirement-audit.v1.json").read_text())
        self.assertEqual(len(doc["retired_workflows"]),17)
        for entry in doc["retired_workflows"]:
            path=ROOT/entry["path"]
            self.assertTrue(path.exists(),entry["path"])
            text=path.read_text()
            self.assertIn("workflow_dispatch",text)
            self.assertIn("exit 1",text)
            self.assertFalse(entry["active_provider_execution_allowed"])
            self.assertFalse(entry["provider_secret_consumption_allowed"])


if __name__=="__main__":
    unittest.main()
