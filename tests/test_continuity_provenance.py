from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from continuity_provenance import canonical_hash, git_blob_sha1, verify  # noqa: E402


class ContinuityProvenanceTests(unittest.TestCase):
    def git(self, root: Path, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()

    def make_repo(self) -> Path:
        root = Path(tempfile.mkdtemp())
        self.git(root, "init")
        self.git(root, "config", "user.email", "test@example.com")
        self.git(root, "config", "user.name", "Test")
        (root / "docs").mkdir()
        (root / "docs/HANDOFF.md").write_text("# Handoff\n", encoding="utf-8")
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", "base")
        base = self.git(root, "rev-parse", "HEAD")

        (root / ".continuity/change-records").mkdir(parents=True)
        (root / "src").mkdir()
        (root / "src/example.py").write_text("VALUE = 1\n", encoding="utf-8")
        refs = {
            "schema": "stegverse.cross_repository_reference_set.v1",
            "repository": "Example/Repo",
            "references": [
                {
                    "reference_id": "source-contract",
                    "repository": "Source/Repo",
                    "source_commit": "a" * 40,
                    "path": "contract.json",
                    "hash_algorithm": "git-blob-sha1",
                    "content_hash": "b" * 40,
                    "required": True,
                    "verification_status": "VERIFIED",
                    "verification_evidence": ["workflow:1"],
                }
            ],
        }
        refs["record_hash"] = canonical_hash(refs, "record_hash")
        (root / ".continuity/cross-repository-references.json").write_text(
            json.dumps(refs), encoding="utf-8"
        )
        config = {
            "schema": "stegverse.continuity.config.v1",
            "repository": "Example/Repo",
            "enforcement_mode": "ENFORCE",
            "current_change_record": ".continuity/change-records/test.json",
            "cross_repository_references": ".continuity/cross-repository-references.json",
            "allowed_unrecorded_paths": [
                ".continuity/provenance-verification-receipt.json"
            ],
        }
        (root / ".continuity/config.json").write_text(json.dumps(config), encoding="utf-8")

        handoff_hash = git_blob_sha1((root / "docs/HANDOFF.md").read_bytes())
        changed = []
        for path in [
            ".continuity/config.json",
            ".continuity/cross-repository-references.json",
            "src/example.py",
        ]:
            changed.append(
                {
                    "path": path,
                    "change_type": "added",
                    "hash_algorithm": "git-blob-sha1",
                    "hash": git_blob_sha1((root / path).read_bytes()),
                }
            )
        record = {
            "schema": "stegverse.session.change_record.v1",
            "change_id": "TEST-001",
            "repository": "Example/Repo",
            "base_commit": base,
            "actor": {"class": "agent", "instance": "unit-test"},
            "governing_handoff": {
                "path": "docs/HANDOFF.md",
                "hash_algorithm": "git-blob-sha1",
                "hash": handoff_hash,
            },
            "changed_paths": changed,
            "claims": [{"claim": "test bootstrap", "state": "IMPLEMENTED"}],
            "unresolved_tasks": [],
            "created_at": "2026-08-04T00:00:00Z",
        }
        record["record_hash"] = canonical_hash(record, "record_hash")
        (root / ".continuity/change-records/test.json").write_text(
            json.dumps(record), encoding="utf-8"
        )
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", "change")
        return root

    def test_valid_record_allows(self) -> None:
        result = verify(self.make_repo(), "Example/Repo", True)
        self.assertEqual("ALLOW", result["terminal_decision"])
        self.assertTrue(result["provenance_verified"])

    def test_unlisted_change_denies(self) -> None:
        root = self.make_repo()
        record_path = root / ".continuity/change-records/test.json"
        record = json.loads(record_path.read_text())
        record["changed_paths"] = [
            item for item in record["changed_paths"] if item["path"] != "src/example.py"
        ]
        record["record_hash"] = canonical_hash(record, "record_hash")
        record_path.write_text(json.dumps(record))
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", "tamper record")
        result = verify(root, "Example/Repo", True)
        self.assertEqual("DENY", result["terminal_decision"])
        self.assertIn("declared_change_set_mismatch", result["failures"])

    def test_handoff_hash_mismatch_denies(self) -> None:
        root = self.make_repo()
        (root / "docs/HANDOFF.md").write_text("# Changed\n")
        result = verify(root, "Example/Repo", False)
        self.assertEqual("DENY", result["terminal_decision"])
        self.assertIn("content_hash_mismatch:docs/HANDOFF.md", result["failures"])

    def test_required_unverified_reference_denies(self) -> None:
        root = self.make_repo()
        path = root / ".continuity/cross-repository-references.json"
        refs = json.loads(path.read_text())
        refs["references"][0]["verification_status"] = "UNVERIFIED"
        refs["record_hash"] = canonical_hash(refs, "record_hash")
        path.write_text(json.dumps(refs))
        result = verify(root, "Example/Repo", False)
        self.assertEqual("DENY", result["terminal_decision"])
        self.assertIn("reference_0_required_not_verified", result["failures"])

    def test_reference_hash_tampering_denies(self) -> None:
        root = self.make_repo()
        path = root / ".continuity/cross-repository-references.json"
        refs = json.loads(path.read_text())
        refs["references"][0]["content_hash"] = "c" * 40
        path.write_text(json.dumps(refs))
        result = verify(root, "Example/Repo", False)
        self.assertEqual("DENY", result["terminal_decision"])
        self.assertIn("reference_set_hash_mismatch", result["failures"])

    def test_missing_config_fails_closed(self) -> None:
        root = Path(tempfile.mkdtemp())
        result = verify(root, "Example/Repo", False)
        self.assertEqual("FAIL_CLOSED", result["terminal_decision"])

    def test_duplicate_declared_path_denies(self) -> None:
        root = self.make_repo()
        path = root / ".continuity/change-records/test.json"
        record = json.loads(path.read_text())
        record["changed_paths"].append(copy.deepcopy(record["changed_paths"][0]))
        record["record_hash"] = canonical_hash(record, "record_hash")
        path.write_text(json.dumps(record))
        result = verify(root, "Example/Repo", False)
        self.assertEqual("DENY", result["terminal_decision"])
        self.assertIn("duplicate_changed_path", result["failures"])

    def test_receipt_is_deterministic(self) -> None:
        root = self.make_repo()
        first = verify(root, "Example/Repo", True)
        second = verify(root, "Example/Repo", True)
        self.assertEqual(first["receipt_hash"], second["receipt_hash"])


if __name__ == "__main__":
    unittest.main()
