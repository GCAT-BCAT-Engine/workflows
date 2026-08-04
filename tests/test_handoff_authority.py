from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from handoff_authority import git_blob_sha1, verify  # noqa: E402


FORMAT_A = """# Example

## Source of truth
x
## Role
x
## Current installed files
x
## Current working path
x
## Done state for this repo
x
## Completed in latest pass
x
## Remaining work
x
## Destination installs
x
## Next task
x
"""


class AuthorityTests(unittest.TestCase):
    def repo(self, *, declared_hash: str | None = None) -> Path:
        root = Path(tempfile.mkdtemp())
        (root / ".handoff").mkdir()
        (root / "docs").mkdir()
        current = root / "docs" / "EXAMPLE_MIRROR_HANDOFF.md"
        current.write_text(FORMAT_A, encoding="utf-8")
        digest = git_blob_sha1(current.read_bytes())
        manifest = {
            "schema": "stegverse.handoff.authority.v1",
            "repository": "Example/Repo",
            "current_handoff": {
                "path": "docs/EXAMPLE_MIRROR_HANDOFF.md",
                "hash_algorithm": "git-blob-sha1",
                "hash": declared_hash or digest,
            },
            "document_profile": "format_a_v1",
            "scoped_handoffs": [],
            "archive_policy": {
                "date_suffix_required": True,
                "session_archive_prefix_allowed": True,
            },
            "declared_at": "2026-08-04T23:15:00Z",
        }
        (root / ".handoff" / "current.json").write_text(json.dumps(manifest))
        return root

    def test_valid_repository_allows(self) -> None:
        receipt = verify(self.repo(), "Example/Repo")
        self.assertEqual("ALLOW", receipt["terminal_decision"])

    def test_duplicate_current_denies(self) -> None:
        root = self.repo()
        (root / "SECOND_MIRROR_HANDOFF.md").write_text(FORMAT_A)
        receipt = verify(root)
        self.assertEqual("DENY", receipt["terminal_decision"])
        self.assertIn("multiple_or_undeclared_current_handoffs", receipt["failures"])

    def test_hash_mismatch_denies(self) -> None:
        receipt = verify(self.repo(declared_hash="0" * 40))
        self.assertEqual("DENY", receipt["terminal_decision"])

    def test_missing_manifest_fails_closed(self) -> None:
        receipt = verify(Path(tempfile.mkdtemp()))
        self.assertEqual("FAIL_CLOSED", receipt["terminal_decision"])

    def test_scoped_handoff_is_not_competing_authority(self) -> None:
        root = self.repo()
        scoped = root / "PROGRAM_MIRROR_HANDOFF.md"
        scoped.write_text("# Program")
        manifest_path = root / ".handoff" / "current.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["scoped_handoffs"] = ["PROGRAM_MIRROR_HANDOFF.md"]
        manifest_path.write_text(json.dumps(manifest))
        receipt = verify(root)
        self.assertEqual("ALLOW", receipt["terminal_decision"])

    def test_receipt_is_deterministic(self) -> None:
        root = self.repo()
        self.assertEqual(verify(root)["receipt_hash"], verify(root)["receipt_hash"])


if __name__ == "__main__":
    unittest.main()
