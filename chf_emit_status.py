#!/usr/bin/env python3
"""
chf_emit_status.py
------------------
Projects a CHF validation brain report (JSON) into the Publisher
status.json intake schema defined in PUBLISHER_INTEGRATION_SPEC.md.

Usage:
    python chf_emit_status.py \
        --report  math_solver/validation/brain_reports/chf_report.json \
        --out     math_solver/validation/brain_reports/chf_status.json \
        --repo    GCAT-BCAT-Engine/workflows \
        --run-id  $GITHUB_RUN_ID \
        --commit  $GITHUB_SHA

Called as the final step of the validation run.
No workflow changes required — invoke from the existing dispatcher.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


# Maturity bands derived from CHF README confirmed classification.
# Update version numbers here as gates advance.
_MATURE_GATES = {f"chf-{i:03d}" for i in range(1, 41)}          # 001-040
_EXPLICIT_GATES = {f"chf-{i:03d}" for i in range(41, 51)}        # 041-050
_PROVISIONAL_GATES = {f"chf-{i:03d}" for i in range(51, 111)}    # 051-110


def _maturity_class(spec_id: str) -> str:
    if spec_id in _MATURE_GATES:
        return "mature"
    if spec_id in _EXPLICIT_GATES:
        return "explicit_validated"
    if spec_id in _PROVISIONAL_GATES:
        return "provisional"
    return "unknown"


def _publication_grade(spec_id: str) -> bool:
    return spec_id in _MATURE_GATES


def _build_traces(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert spec results into trace entries matching the Publisher
    status.json traces[] schema.
    """
    traces = []
    for result in results:
        spec_id = result.get("spec_id", "unknown")
        status = result.get("status", "FAIL")
        cases = result.get("cases", [])
        pass_count = sum(1 for c in cases if c.get("status") == "PASS")
        fail_count = len(cases) - pass_count

        # Collect unique outcome classes seen in this spec
        outcomes = sorted({c.get("actual", "") for c in cases})

        traces.append({
            "spec_id": spec_id,
            "decision": status,
            "maturity": _maturity_class(spec_id),
            "publication_grade": _publication_grade(spec_id),
            "cases_total": len(cases),
            "cases_passed": pass_count,
            "cases_failed": fail_count,
            "outcome_classes": outcomes,
        })
    return traces


def _build_sandbox_trace(sandbox: Dict[str, Any]) -> Dict[str, Any]:
    """Summarise sandbox result for Publisher intake."""
    return {
        "spec_id": "chf-sandbox-aggregate",
        "decision": sandbox.get("sandbox_status", "FAIL"),
        "maturity": "sandbox_expansion",
        "publication_grade": False,
        "suites_evaluated": sandbox.get("suites_evaluated", 0),
        "subtests_generated": sandbox.get("subtests_generated", 0),
        "subtests_passed": sandbox.get("subtests_passed", 0),
        "subtests_failed": sandbox.get("subtests_failed", 0),
    }


def _count_by_maturity(traces: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for t in traces:
        m = t.get("maturity", "unknown")
        counts[m] = counts.get(m, 0) + 1
    return counts


def emit_status(
    report_path: Path,
    out_path: Path,
    repo: str,
    run_id: str,
    commit_sha: str,
) -> Dict[str, Any]:
    with report_path.open("r", encoding="utf-8") as f:
        report = json.load(f)

    overall_status = report.get("overall_status", "FAIL")
    explicit_status = report.get("explicit_status", "FAIL")
    sandbox_status = report.get("sandbox_status", "NOT_RUN")
    specs_evaluated = report.get("specs_evaluated", 0)
    results = report.get("results", [])
    sandbox = report.get("sandbox", {})

    traces = _build_traces(results)
    if sandbox:
        traces.append(_build_sandbox_trace(sandbox))

    maturity_counts = _count_by_maturity(
        [t for t in traces if t.get("spec_id") != "chf-sandbox-aggregate"]
    )

    status_doc: Dict[str, Any] = {
        "schema_version": "1.0.0",
        "formalism": "consequence_horizon_formalism",
        "repo": repo,
        "run_id": run_id,
        "commit_sha": commit_sha,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": overall_status,
        "explicit_status": explicit_status,
        "sandbox_status": sandbox_status,
        "specs_evaluated": specs_evaluated,
        "maturity_counts": maturity_counts,
        "publication_grade_count": sum(
            1 for t in traces if t.get("publication_grade")
        ),
        "traces": traces,
        "ecosystem": {
            "org": "GCAT-BCAT-Engine",
            "upstream": "GCAT-BCAT-Engine/workflows",
            "publisher": "GCAT-BCAT-Engine/Publisher",
            "sibling_repos": [
                "GCAT-BCAT-Engine/Publisher",
                "GCAT-BCAT-Engine/StegSim",
                "StegGhost/entity-sandbox-runner",
                "StegGhost/stegverse-sandbox",
            ],
        },
        "publication_intake": {
            "target_manifest": "papers_manifest.yml",
            "paper_id": "chf-formalism",
            "category": "formal_methods",
            "status_on_pass": "draft",
            "status_on_fail": "under_review",
            "paper_status": "draft" if overall_status == "PASS" else "under_review",
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(status_doc, f, indent=2)

    return status_doc


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Emit CHF validation status for Publisher intake."
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Path to CHF brain report JSON",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Path to write chf_status.json",
    )
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", "GCAT-BCAT-Engine/workflows"),
    )
    parser.add_argument(
        "--run-id",
        default=os.environ.get("GITHUB_RUN_ID", "local"),
    )
    parser.add_argument(
        "--commit",
        default=os.environ.get("GITHUB_SHA", "unknown"),
    )
    args = parser.parse_args()

    status_doc = emit_status(
        report_path=Path(args.report),
        out_path=Path(args.out),
        repo=args.repo,
        run_id=args.run_id,
        commit_sha=args.commit,
    )

    print(json.dumps({
        "status": status_doc["status"],
        "specs_evaluated": status_doc["specs_evaluated"],
        "maturity_counts": status_doc["maturity_counts"],
        "publication_grade_count": status_doc["publication_grade_count"],
        "paper_status": status_doc["publication_intake"]["paper_status"],
    }, indent=2))

    return 0 if status_doc["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
