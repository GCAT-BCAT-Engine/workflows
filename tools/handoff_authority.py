#!/usr/bin/env python3
"""Verify one declared repository-wide handoff before orchestration."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

MANIFEST = Path(".handoff/current.json")
ARCHIVE = re.compile(r".*_\d{4}-\d{2}-\d{2}\.md$", re.IGNORECASE)
FORMAT_A = (
    "Source of truth",
    "Role",
    "Current installed files",
    "Current working path",
    "Done state for this repo",
    "Completed in latest pass",
    "Remaining work",
    "Destination installs",
    "Next task",
)


def stable_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def file_hash(data: bytes, algorithm: str) -> str:
    if algorithm == "git-blob-sha1":
        return git_blob_sha1(data)
    if algorithm == "sha256":
        return hashlib.sha256(data).hexdigest()
    raise ValueError("unsupported_hash_algorithm")


def relative_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("unsafe_repository_path")
    return path


def headings(text: str) -> set[str]:
    found: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            found.add(match.group(1).strip())
    return found


def discover(root: Path) -> list[str]:
    found: set[str] = set()
    for pattern in ("*_HANDOFF.md", "*_MIRROR_HANDOFF.md", "*.mirror.handoff.md"):
        for path in root.rglob(pattern):
            if ".git" in path.parts:
                continue
            found.add(path.relative_to(root).as_posix())
    return sorted(found)


def verify(root: Path, expected_repository: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    try:
        manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        receipt = {
            "receipt_type": "stegverse.handoff_verification.receipt.v1",
            "repository": expected_repository,
            "terminal_decision": "FAIL_CLOSED",
            "authority_verified": False,
            "failures": [f"manifest_unavailable:{type(exc).__name__}"],
            "checks": [],
            "discovered_handoffs": discover(root),
        }
        receipt["receipt_hash"] = stable_hash(receipt)
        return receipt

    if manifest.get("schema") != "stegverse.handoff.authority.v1":
        failures.append("manifest_schema_invalid")
    repository = manifest.get("repository")
    if expected_repository and repository != expected_repository:
        failures.append("repository_identity_mismatch")

    current = manifest.get("current_handoff")
    if not isinstance(current, dict):
        failures.append("current_handoff_invalid")
        current = {}
    try:
        current_path = relative_path(str(current.get("path", "")))
    except ValueError as exc:
        failures.append(str(exc))
        current_path = Path("__invalid__")
    current_rel = current_path.as_posix()

    try:
        data = (root / current_path).read_bytes()
    except OSError:
        data = None
        failures.append("current_handoff_missing_or_unreadable")

    observed_hash = None
    if data is not None:
        try:
            observed_hash = file_hash(data, str(current.get("hash_algorithm")))
        except ValueError as exc:
            failures.append(str(exc))
        else:
            if observed_hash != current.get("hash"):
                failures.append("current_handoff_hash_mismatch")
    checks.append(
        {
            "check": "current_handoff_hash",
            "passed": observed_hash is not None and observed_hash == current.get("hash"),
            "declared": current.get("hash"),
            "observed": observed_hash,
        }
    )

    profile = manifest.get("document_profile")
    missing_headings: list[str] = []
    if data is not None:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            failures.append("current_handoff_not_utf8")
        else:
            if profile == "format_a_v1":
                present = headings(text)
                missing_headings = [item for item in FORMAT_A if item not in present]
                if missing_headings:
                    failures.append("document_profile_heading_mismatch")
            elif profile != "goal_registry_v1":
                failures.append("document_profile_unsupported")
    checks.append(
        {
            "check": "document_profile",
            "passed": not missing_headings
            and profile in {"format_a_v1", "goal_registry_v1"},
            "profile": profile,
            "missing_headings": missing_headings,
        }
    )

    raw_scoped = manifest.get("scoped_handoffs")
    scoped: set[str] = set()
    if not isinstance(raw_scoped, list):
        failures.append("scoped_handoffs_invalid")
    else:
        for value in raw_scoped:
            try:
                scoped.add(relative_path(str(value)).as_posix())
            except ValueError as exc:
                failures.append(str(exc))
    missing_scoped = sorted(item for item in scoped if not (root / item).is_file())
    if missing_scoped:
        failures.append("declared_scoped_handoff_missing")

    discovered = discover(root)
    undeclared: list[str] = []
    archive_violations: list[str] = []
    for item in discovered:
        path = Path(item)
        if item == current_rel or item in scoped:
            continue
        if path.name.upper().startswith("SESSION_ARCHIVE_HANDOFF_"):
            continue
        if ARCHIVE.fullmatch(path.name):
            continue
        if path.name.upper().endswith("_MIRROR_HANDOFF.MD"):
            undeclared.append(item)
        elif "MIRROR_HANDOFF" in path.name.upper():
            archive_violations.append(item)
    if undeclared:
        failures.append("multiple_or_undeclared_current_handoffs")
    if archive_violations:
        failures.append("archive_naming_violation")

    checks.extend(
        [
            {
                "check": "exactly_one_current_handoff",
                "passed": bool(current_rel) and not undeclared,
                "declared_current": current_rel,
                "undeclared_candidates": undeclared,
            },
            {
                "check": "scoped_handoffs",
                "passed": not missing_scoped,
                "declared": sorted(scoped),
                "missing": missing_scoped,
            },
            {
                "check": "archive_convention",
                "passed": not archive_violations,
                "violations": archive_violations,
            },
        ]
    )

    decision = "ALLOW" if not failures else "DENY"
    receipt: dict[str, Any] = {
        "receipt_type": "stegverse.handoff_verification.receipt.v1",
        "repository": repository,
        "manifest_path": MANIFEST.as_posix(),
        "manifest_hash": hashlib.sha256(
            json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "current_handoff_path": current_rel,
        "current_handoff_hash": observed_hash,
        "source_of_truth_candidate_count": 1 + len(undeclared),
        "terminal_decision": decision,
        "authority_verified": decision == "ALLOW",
        "checks": checks,
        "failures": sorted(set(failures)),
        "discovered_handoffs": discovered,
    }
    receipt["receipt_hash"] = stable_hash(receipt)
    return receipt


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--repository")
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    receipt = verify(args.root, args.repository)
    output = args.output or args.root / "handoff-verification-receipt.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("HANDOFF_AUTHORITY=" + receipt["terminal_decision"])
    print("receipt_hash=" + receipt["receipt_hash"])
    return 0 if receipt["terminal_decision"] == "ALLOW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
