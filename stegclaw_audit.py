#!/usr/bin/env python3
"""StegClaw audit runner.

This is a minimal, dependency-free repo inspection tool for StegVerse repos.
It is intentionally read-only: it scans the target module, detects imports and
references, then emits downloadable audit artifacts for the next build step.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REFERENCE_TERMS = [
    "gcat",
    "bcat",
    "ecat",
    "icat",
    "iw",
    "inference_window",
    "triad",
    "full_pipeline",
    "receipt",
    "receipts",
    "sandbox",
    "admissibility",
    "allow",
    "deny",
    "fail_closed",
    "fail-closed",
]

TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".cfg",
    ".ini",
}


@dataclass(frozen=True)
class FileRecord:
    path: str
    kind: str
    size_bytes: int
    sha256: str
    imports: list[str]
    references: list[str]


@dataclass(frozen=True)
class AuditReport:
    tool: str
    version: str
    generated_at: str
    root: str
    target: str
    target_exists: bool
    file_count: int
    python_file_count: int
    test_file_count: int
    markdown_file_count: int
    files: list[FileRecord]
    repo_level_signals: dict[str, Any]
    next_issues: list[dict[str, str]]


def stable_hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError:
        return b""


def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def path_kind(path: Path) -> str:
    if path.name.startswith("test_") or "/tests/" in path.as_posix() or path.as_posix().endswith("_test.py"):
        return "test"
    if path.suffix == ".py":
        return "python"
    if path.suffix == ".md":
        return "markdown"
    return "other"


def parse_imports(path: Path) -> list[str]:
    if path.suffix != ".py":
        return []
    source = safe_read_text(path)
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ["<syntax-error>"]

    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            prefix = "." * node.level + module
            imports.add(prefix)
    return sorted(imports)


def detect_references(path: Path) -> list[str]:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return []
    text = safe_read_text(path).lower()
    return sorted({term for term in REFERENCE_TERMS if term in text})


def iter_target_files(target_dir: Path) -> list[Path]:
    if not target_dir.exists():
        return []
    ignored_dirs = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules"}
    results: list[Path] = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for file_name in files:
            path = Path(root) / file_name
            if path.suffix.lower() in TEXT_EXTENSIONS:
                results.append(path)
    return sorted(results)


def repo_signals(root: Path) -> dict[str, Any]:
    candidates = [
        "README.md",
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "pytest.ini",
        ".github/workflows",
        "full_pipeline",
        "triad",
        "ecat_validator.py",
        "icat_validator.py",
        "iw_validator.py",
        "gcat_validator.py",
        "bcat_validator.py",
    ]
    return {candidate: (root / candidate).exists() for candidate in candidates}


def build_next_issues(target_exists: bool) -> list[dict[str, str]]:
    if not target_exists:
        return [
            {
                "title": "Create math_solver module boundary",
                "done": "Create math_solver/__init__.py and a minimal README describing the module boundary. Do not implement solving yet.",
            }
        ]

    return [
        {
            "title": "Add sandbox receipt primitives to math_solver",
            "done": "A run produces run_id, problem_id, input_hash, output_hash, started_at, completed_at, status, and classifier. Add deterministic hashing tests.",
        },
        {
            "title": "Add problem packet intake for math_solver",
            "done": "Accept JSON packets with id, title, domain, target, assumptions, constraints, and allowed_formalisms. Invalid packets fail closed.",
        },
        {
            "title": "Add Collatz calibration encoder to math_solver",
            "done": "Given n and max_steps, emit transition sequence, classify steps, detect termination/repeated states, and produce receipt-compatible output. Do not claim proof.",
        },
    ]


def render_markdown(report: AuditReport) -> str:
    lines: list[str] = []
    lines.append("# StegClaw Audit")
    lines.append("")
    lines.append(f"Generated: `{report.generated_at}`")
    lines.append(f"Root: `{report.root}`")
    lines.append(f"Target: `{report.target}`")
    lines.append(f"Target exists: `{report.target_exists}`")
    lines.append("")
    lines.append("## Done definition")
    lines.append("")
    lines.append("This audit is complete when it identifies the current math_solver structure, detects repo-level integration signals, and emits next issue packets without modifying source files.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Files scanned: `{report.file_count}`")
    lines.append(f"- Python files: `{report.python_file_count}`")
    lines.append(f"- Test files: `{report.test_file_count}`")
    lines.append(f"- Markdown files: `{report.markdown_file_count}`")
    lines.append("")
    lines.append("## Repo-level signals")
    lines.append("")
    for key, value in sorted(report.repo_level_signals.items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Files")
    lines.append("")
    if not report.files:
        lines.append("No files were found under the target path.")
    else:
        for record in report.files:
            lines.append(f"### `{record.path}`")
            lines.append("")
            lines.append(f"- Kind: `{record.kind}`")
            lines.append(f"- Size: `{record.size_bytes}` bytes")
            lines.append(f"- SHA-256: `{record.sha256}`")
            lines.append(f"- Imports: `{', '.join(record.imports) if record.imports else 'none'}`")
            lines.append(f"- References: `{', '.join(record.references) if record.references else 'none'}`")
            lines.append("")
    lines.append("## Next issue packets")
    lines.append("")
    for index, issue in enumerate(report.next_issues, start=1):
        lines.append(f"### Issue {index}: {issue['title']}")
        lines.append("")
        lines.append("Done means:")
        lines.append("")
        lines.append(f"- {issue['done']}")
        lines.append("- Do not delete or replace existing working files unless this audit shows they are unused and the PR explains why.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_issues_markdown(issues: list[dict[str, str]]) -> str:
    lines = ["# StegClaw Next Issues", ""]
    for index, issue in enumerate(issues, start=1):
        lines.append(f"## {index}. {issue['title']}")
        lines.append("")
        lines.append("Done means:")
        lines.append("")
        lines.append(f"- {issue['done']}")
        lines.append("- Keep the change minimal.")
        lines.append("- Add or update tests where behavior changes.")
        lines.append("- Do not claim a mathematical proof from bounded computation.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run(root: Path, target: str, out: Path) -> AuditReport:
    root = root.resolve()
    target_dir = (root / target).resolve()
    target_exists = target_dir.exists()
    files = iter_target_files(target_dir)

    records: list[FileRecord] = []
    for path in files:
        data = read_bytes(path)
        rel = path.relative_to(root).as_posix()
        records.append(
            FileRecord(
                path=rel,
                kind=path_kind(path),
                size_bytes=len(data),
                sha256=stable_hash_bytes(data),
                imports=parse_imports(path),
                references=detect_references(path),
            )
        )

    report = AuditReport(
        tool="StegClaw",
        version="0.1.0",
        generated_at=datetime.now(timezone.utc).isoformat(),
        root=".",
        target=target,
        target_exists=target_exists,
        file_count=len(records),
        python_file_count=sum(1 for r in records if r.kind == "python"),
        test_file_count=sum(1 for r in records if r.kind == "test"),
        markdown_file_count=sum(1 for r in records if r.kind == "markdown"),
        files=records,
        repo_level_signals=repo_signals(root),
        next_issues=build_next_issues(target_exists),
    )

    out.mkdir(parents=True, exist_ok=True)
    (out / "stegclaw_audit.json").write_text(json.dumps(asdict(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "STEGCLAW_AUDIT.md").write_text(render_markdown(report), encoding="utf-8")
    (out / "STEGCLAW_NEXT_ISSUES.md").write_text(render_issues_markdown(report.next_issues), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a read-only StegClaw repository audit.")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--target", default="math_solver", help="Target module or directory to audit")
    parser.add_argument("--out", default="stegclaw_out", help="Output directory")
    args = parser.parse_args()

    report = run(Path(args.root), args.target, Path(args.out))
    print(f"StegClaw audit complete: {report.file_count} files scanned under {report.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
