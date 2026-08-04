#!/usr/bin/env python3
"""Validate a commit-bound session change record and cross-repository references."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Iterable

CONFIG_SCHEMA = "stegverse.continuity.config.v1"
CHANGE_SCHEMA = "stegverse.session.change_record.v1"
REFERENCE_SCHEMA = "stegverse.cross_repository_reference_set.v1"
RECEIPT_TYPE = "stegverse.continuity.provenance_verification.v1"


class ContinuityError(RuntimeError):
    pass


def canonical_hash(payload: dict[str, Any], hash_field: str) -> str:
    clean = dict(payload)
    clean.pop(hash_field, None)
    encoded = json.dumps(
        clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def safe_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not value:
        raise ContinuityError(f"unsafe_repository_path:{value}")
    return path


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContinuityError(f"missing_file:{path.as_posix()}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContinuityError(f"invalid_json:{path.as_posix()}:{type(exc).__name__}") from exc
    if not isinstance(payload, dict):
        raise ContinuityError(f"json_object_required:{path.as_posix()}")
    return payload


def verify_file_hash(root: Path, path_value: str, algorithm: str, expected: str) -> str:
    path = root / safe_relative(path_value)
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise ContinuityError(f"unreadable_path:{path_value}:{type(exc).__name__}") from exc
    if algorithm == "git-blob-sha1":
        observed = git_blob_sha1(data)
    elif algorithm == "sha256":
        observed = hashlib.sha256(data).hexdigest()
    else:
        raise ContinuityError(f"unsupported_hash_algorithm:{algorithm}")
    if observed != expected:
        raise ContinuityError(f"content_hash_mismatch:{path_value}")
    return observed


def git_changed_paths(root: Path, base_commit: str) -> dict[str, str]:
    command = ["git", "-C", str(root), "diff", "--name-status", f"{base_commit}..HEAD"]
    try:
        completed = subprocess.run(command, check=True, text=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ContinuityError(f"git_diff_unavailable:{type(exc).__name__}") from exc
    changes: dict[str, str] = {}
    for raw in completed.stdout.splitlines():
        if not raw.strip():
            continue
        fields = raw.split("\t")
        status = fields[0]
        if status.startswith("R") and len(fields) == 3:
            changes[fields[1]] = "deleted"
            changes[fields[2]] = "added"
        elif len(fields) == 2:
            kind = {"A": "added", "M": "modified", "D": "deleted"}.get(status[0])
            if kind is None:
                raise ContinuityError(f"unsupported_git_status:{status}")
            changes[fields[1]] = kind
        else:
            raise ContinuityError(f"unparseable_git_diff:{raw}")
    return changes


def verify(root: Path, expected_repository: str | None, verify_diff: bool) -> dict[str, Any]:
    root = root.resolve()
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    try:
        config = load_json(root / ".continuity/config.json")
    except ContinuityError as exc:
        receipt = {
            "receipt_type": RECEIPT_TYPE,
            "repository": expected_repository,
            "terminal_decision": "FAIL_CLOSED",
            "checks": [],
            "failures": [str(exc)],
        }
        receipt["receipt_hash"] = canonical_hash(receipt, "receipt_hash")
        return receipt

    if config.get("schema") != CONFIG_SCHEMA:
        failures.append("config_schema_invalid")
    repository = config.get("repository")
    if expected_repository and repository != expected_repository:
        failures.append("repository_identity_mismatch")
    if config.get("enforcement_mode") != "ENFORCE":
        failures.append("enforcement_mode_not_enforce")

    try:
        record_rel = safe_relative(str(config.get("current_change_record", ""))).as_posix()
        record = load_json(root / record_rel)
    except ContinuityError as exc:
        failures.append(str(exc))
        record_rel = ""
        record = {}

    if record.get("schema") != CHANGE_SCHEMA:
        failures.append("change_record_schema_invalid")
    if record.get("repository") != repository:
        failures.append("change_record_repository_mismatch")
    if record.get("record_hash") != canonical_hash(record, "record_hash"):
        failures.append("change_record_hash_mismatch")

    base_commit = record.get("base_commit")
    if not isinstance(base_commit, str) or len(base_commit) != 40:
        failures.append("base_commit_invalid")

    actor = record.get("actor")
    if not isinstance(actor, dict):
        failures.append("actor_invalid")
    else:
        if actor.get("class") not in {"human", "chatgpt", "agent", "workflow", "mixed"}:
            failures.append("actor_class_invalid")
        if not isinstance(actor.get("instance"), str) or not actor.get("instance"):
            failures.append("actor_instance_invalid")

    handoff = record.get("governing_handoff")
    if not isinstance(handoff, dict):
        failures.append("governing_handoff_invalid")
    else:
        try:
            verify_file_hash(
                root,
                str(handoff.get("path", "")),
                str(handoff.get("hash_algorithm", "")),
                str(handoff.get("hash", "")),
            )
        except ContinuityError as exc:
            failures.append(str(exc))

    entries = record.get("changed_paths")
    declared: dict[str, str] = {}
    if not isinstance(entries, list):
        failures.append("changed_paths_invalid")
        entries = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            failures.append(f"changed_path_{index}_invalid")
            continue
        path_value = entry.get("path")
        change_type = entry.get("change_type")
        if not isinstance(path_value, str):
            failures.append(f"changed_path_{index}_path_invalid")
            continue
        try:
            normalized = safe_relative(path_value).as_posix()
        except ContinuityError as exc:
            failures.append(str(exc))
            continue
        if normalized in declared:
            failures.append("duplicate_changed_path")
        if change_type not in {"added", "modified", "deleted"}:
            failures.append(f"changed_path_{index}_type_invalid")
            continue
        declared[normalized] = change_type
        if change_type != "deleted":
            try:
                verify_file_hash(
                    root,
                    normalized,
                    str(entry.get("hash_algorithm", "")),
                    str(entry.get("hash", "")),
                )
            except ContinuityError as exc:
                failures.append(str(exc))

    exemptions = config.get("allowed_unrecorded_paths", [])
    if not isinstance(exemptions, list) or not all(isinstance(x, str) for x in exemptions):
        failures.append("allowed_unrecorded_paths_invalid")
        exemptions = []

    if verify_diff and isinstance(base_commit, str) and len(base_commit) == 40:
        try:
            actual = git_changed_paths(root, base_commit)
        except ContinuityError as exc:
            failures.append(str(exc))
        else:
            filtered = {
                path: kind
                for path, kind in actual.items()
                if path != record_rel
                and not any(fnmatch.fnmatch(path, pattern) for pattern in exemptions)
            }
            if filtered != declared:
                failures.append("declared_change_set_mismatch")
            checks.append(
                {
                    "check": "git_change_set",
                    "passed": filtered == declared,
                    "declared": declared,
                    "observed": filtered,
                    "excluded_record_path": record_rel,
                    "exemptions": exemptions,
                }
            )

    try:
        references_rel = safe_relative(str(config.get("cross_repository_references", ""))).as_posix()
        references = load_json(root / references_rel)
    except ContinuityError as exc:
        failures.append(str(exc))
        references_rel = ""
        references = {}

    if references.get("schema") != REFERENCE_SCHEMA:
        failures.append("reference_set_schema_invalid")
    if references.get("repository") != repository:
        failures.append("reference_set_repository_mismatch")
    if references.get("record_hash") != canonical_hash(references, "record_hash"):
        failures.append("reference_set_hash_mismatch")

    reference_entries = references.get("references")
    if not isinstance(reference_entries, list):
        failures.append("references_invalid")
        reference_entries = []
    reference_ids: set[str] = set()
    for index, ref in enumerate(reference_entries):
        if not isinstance(ref, dict):
            failures.append(f"reference_{index}_invalid")
            continue
        ref_id = ref.get("reference_id")
        if not isinstance(ref_id, str) or not ref_id:
            failures.append(f"reference_{index}_id_invalid")
        elif ref_id in reference_ids:
            failures.append("duplicate_reference_id")
        else:
            reference_ids.add(ref_id)
        required = ref.get("required")
        if not isinstance(required, bool):
            failures.append(f"reference_{index}_required_invalid")
        if not isinstance(ref.get("repository"), str) or "/" not in str(ref.get("repository", "")):
            failures.append(f"reference_{index}_repository_invalid")
        if not isinstance(ref.get("source_commit"), str) or len(str(ref.get("source_commit", ""))) != 40:
            failures.append(f"reference_{index}_commit_invalid")
        if not isinstance(ref.get("path"), str) or not ref.get("path"):
            failures.append(f"reference_{index}_path_invalid")
        if ref.get("hash_algorithm") not in {"git-blob-sha1", "sha256"}:
            failures.append(f"reference_{index}_hash_algorithm_invalid")
        expected_length = 40 if ref.get("hash_algorithm") == "git-blob-sha1" else 64
        if len(str(ref.get("content_hash", ""))) != expected_length:
            failures.append(f"reference_{index}_content_hash_invalid")
        if required and ref.get("verification_status") != "VERIFIED":
            failures.append(f"reference_{index}_required_not_verified")
        evidence = ref.get("verification_evidence")
        if required and (not isinstance(evidence, list) or not evidence):
            failures.append(f"reference_{index}_evidence_missing")

    decision = "ALLOW" if not failures else "DENY"
    receipt: dict[str, Any] = {
        "receipt_type": RECEIPT_TYPE,
        "repository": repository,
        "change_id": record.get("change_id"),
        "change_record_path": record_rel,
        "change_record_hash": record.get("record_hash"),
        "reference_set_path": references_rel,
        "reference_set_hash": references.get("record_hash"),
        "declared_changed_path_count": len(declared),
        "reference_count": len(reference_entries),
        "terminal_decision": decision,
        "provenance_verified": decision == "ALLOW",
        "checks": checks,
        "failures": sorted(set(failures)),
    }
    receipt["receipt_hash"] = canonical_hash(receipt, "receipt_hash")
    return receipt


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--repository")
    parser.add_argument("--verify-diff", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".continuity/provenance-verification-receipt.json"),
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    output = args.output if args.output.is_absolute() else args.root / args.output
    receipt = verify(args.root, args.repository, args.verify_diff)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("CONTINUITY_PROVENANCE=" + receipt["terminal_decision"])
    print("provenance_verified=" + str(receipt.get("provenance_verified", False)).lower())
    return 0 if receipt["terminal_decision"] == "ALLOW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
