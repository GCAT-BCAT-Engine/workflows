#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> None:
    validation_root = ROOT / "math_solver" / "validation"
    problem_spec = (validation_root / "problem_spec_rtg_001.yml").read_text(encoding="utf-8")
    candidate_vector = read_json(validation_root / "candidate_vectors" / "rtg" / "rtg_001.json")
    manifest = read_json(validation_root / "rtg_handoff_manifest.json")
    cost = read_json(validation_root / "cost_estimates" / "rtg_001_cost_estimate.json")
    declared_tasks = read_json(validation_root / "rtg_declared_tasks.json")

    for marker in [
        "problem_id: RTG-001",
        "source_repo: Data-Continuation/RTG-Tests",
        "target_repo: GCAT-BCAT-Engine/workflows",
        "required_secret: ANTHROPIC_API_KEY",
        "runner: ubuntu-latest",
        "actual_dispatch_performed: false",
        "false_execution_claim_blocked: true",
    ]:
        require(marker in problem_spec, f"Problem spec missing marker: {marker}")

    require(candidate_vector["candidate_id"] == "RTG-001-CV-001", "Wrong candidate id")
    require(candidate_vector["current_stage"] == "contract_ready", "Initial stage must be contract_ready")
    require(candidate_vector["dead_basis_guard"]["enabled"] is True, "Dead-basis guard must be enabled")
    require(candidate_vector["dead_basis_guard"]["requires_external_artifact_for_solver_claim"] is True, "Solver claim must require external artifact")
    stages = [stage["stage"] for stage in candidate_vector["transition_path"]]
    require(stages == ["contract_ready", "dispatch_attempted", "artifact_returned", "artifact_ingested", "rtg_state_updated"], "Unexpected transition path")

    require(manifest["install_target_repo"] == "GCAT-BCAT-Engine/workflows", "Wrong install target")
    require(manifest["workflow"] == ".github/workflows/validation_run.yml", "Wrong workflow")
    require(manifest["dispatch"]["trigger"] == "workflow_dispatch", "Wrong dispatch trigger")
    require(manifest["dispatch"]["inputs"]["run_id"] == "RTG-001", "Wrong run_id")
    require(manifest["expected_runner"] == "ubuntu-latest", "Wrong runner")
    require(manifest["required_secret"] == "ANTHROPIC_API_KEY", "Wrong secret")
    require(manifest["claim_boundary"]["actual_dispatch_performed"] is False, "Install package must not claim dispatch")
    require(manifest["claim_boundary"]["external_solver_execution_claimed"] is False, "Install package must not claim solver execution")

    expected_files = set(manifest["expected_artifact"]["files"])
    require({"ext2_phase1.json", "ext2_sources.json", "ext2_phase3.json", "ext2_report.json"}.issubset(expected_files), "Returned artifact file set incomplete")

    require(cost["estimate_type"] == "pre_execution_reference_estimate", "Cost must be pre-execution reference estimate")
    require(float(cost["recommended_budget_gate"]["hard_budget_ceiling_usd"]) == 50.00, "Wrong hard budget ceiling")
    require(cost["recommended_budget_gate"]["status"] == "within_budget", "Budget gate not within budget")
    require(cost["receipt_requirement"]["actual_cost_must_be_read_from_returned_artifact"] is True, "Actual cost must require returned artifact")
    require(cost["receipt_requirement"]["pre_execution_estimate_is_not_receipt"] is True, "Estimate must not be treated as receipt")

    tasks = declared_tasks.get("tasks", [])
    require(len(tasks) == 1, "Expected exactly one declared task")
    require(tasks[0]["name"] == "rtg_001_workflows_install_contract_tests", "Wrong declared task name")
    require(tasks[0]["command"] == ["python", "math_solver/validation/tests/test_rtg_001_workflows_install_contract.py"], "Wrong declared task command")

    print("RTG-001 workflows install contract test passed.")

if __name__ == "__main__":
    main()
