from __future__ import annotations

import importlib.util
import pathlib
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("guard",ROOT/"tools"/"verify_no_direct_provider_secrets.py")
guard=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(guard)

class ProviderSecretBoundaryTests(unittest.TestCase):
    def write(self,root,name,text):
        p=root/".github"/"workflows"/name
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text)
        return p

    def test_actual_repository_has_no_direct_provider_secret_reference(self):
        self.assertEqual(guard.violations(ROOT),[])

    def test_direct_secret_interpolation_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)
            self.write(root,"bad.yml","env:\n  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}\n")
            bad=guard.violations(root)
            self.assertTrue(bad)
            self.assertIn("direct GitHub secret interpolation",bad[0])

    def test_shell_provider_key_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)
            self.write(root,"bad.yml","run: echo $ANTHROPIC_API_KEY\n")
            bad=guard.violations(root)
            self.assertTrue(any("provider credential reference" in x for x in bad))

    def test_negative_marker_scan_is_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)
            self.write(root,"good.yml","run: grep -E 'OPENAI_API_KEY|ANTHROPIC_API_KEY' target.py\n")
            self.assertEqual(guard.violations(root),[])

if __name__=="__main__":
    unittest.main()
