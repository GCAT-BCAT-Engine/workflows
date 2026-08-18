import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("primary_runner", ROOT / "run_stegverse_primary_candidate.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def plan():
    group = {
        "schema": "stegverse.test-lanes-execution-group.v1",
        "execution_group_id": "group:primary",
        "provider": "stegverse_local",
        "provider_role": "PRIMARY",
        "capsule_id": "stegverse.local.default",
        "capability": "local.model.inference",
        "model": "stegverse-reference-lm-v1",
        "parameters": {},
        "task_id": "SV-RECON-001",
        "task_source": "task.json",
        "task_source_blob_sha": "PLACEHOLDER",
        "prompt_profile": "stegverse.sv-recon-001.prompt.v1",
        "lane_ids": ["stegverse-primary"],
        "modes": ["REFERENCE"],
        "member_request_hashes": ["sha256:request"],
        "required": True,
        "candidate_reuse": False,
        "credential_material_present": False,
        "execution_authority_granted_by_group": False,
        "state": "READY_LOCAL_PRIMARY",
    }
    value = {
        "schema": "stegverse.test-lanes-plan.v1",
        "state": "READY",
        "test_id": "SV-COST-NINE-LANE-v1",
        "manifest_hash": "sha256:manifest",
        "primary_provider": "stegverse_local",
        "credential_authority": "TV/TVC",
        "credential_material_present": False,
        "lane_count": 1,
        "execution_group_count": 1,
        "blockers": [],
        "lanes": [],
        "execution_groups": [group],
    }
    return value


def task_bytes():
    return json.dumps({"task_id": "SV-RECON-001", "events": []}, sort_keys=True).encode()


def finalize(value, task):
    group = value["execution_groups"][0]
    group["task_source_blob_sha"] = MODULE.git_blob_sha(task)
    group["group_hash"] = MODULE.sha256_json(group)
    value["plan_hash"] = MODULE.sha256_json(value)
    return value


def fake_http(url, *, payload=None, timeout=30):
    if url.endswith("/health"):
        return {
            "state": "READY",
            "model": "stegverse-reference-lm-v1",
            "private_endpoint_only": True,
            "third_party_inference_required": False,
            "authority_effect": "NONE",
        }
    return {
        "model": "stegverse-reference-lm-v1",
        "choices": [{"message": {"content": "{\"ok\":true}"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14},
        "stegverse": {
            "model_hash": "sha256:model",
            "third_party_inference_required": False,
            "authority_effect": "NONE",
        },
    }


class PrimaryRunnerTests(unittest.TestCase):
    def test_primary_candidate_is_credential_free_and_sovereign(self):
        task = task_bytes()
        value = finalize(plan(), task)
        with patch.object(MODULE, "http_json", side_effect=fake_http):
            result = MODULE.run_primary_candidate(plan=value, task_bytes=task, endpoint="http://127.0.0.1:11435")
        self.assertEqual(result["state"], "PRIMARY_CANDIDATE_COMPLETE")
        self.assertEqual(result["provider"], "stegverse_local")
        self.assertEqual(result["provider_role"], "PRIMARY")
        self.assertEqual(result["credential_requirement"], "NONE")
        self.assertFalse(result["credential_material_present"])
        self.assertFalse(result["third_party_inference_required"])
        self.assertEqual(result["candidate_output"], '{"ok":true}')

    def test_non_loopback_endpoint_is_rejected(self):
        task = task_bytes()
        value = finalize(plan(), task)
        with patch.object(MODULE, "http_json", side_effect=fake_http):
            with self.assertRaisesRegex(MODULE.PrimaryCandidateError, "loopback-local"):
                MODULE.run_primary_candidate(plan=value, task_bytes=task, endpoint="https://example.com")

    def test_third_party_health_drift_is_rejected(self):
        task = task_bytes()
        value = finalize(plan(), task)
        def drift(url, *, payload=None, timeout=30):
            if url.endswith("/health"):
                health = dict(fake_http(url, payload=payload, timeout=timeout))
                health["third_party_inference_required"] = True
                return health
            return fake_http(url, payload=payload, timeout=timeout)
        with patch.object(MODULE, "http_json", side_effect=drift):
            with self.assertRaisesRegex(MODULE.PrimaryCandidateError, "third-party inference"):
                MODULE.run_primary_candidate(plan=value, task_bytes=task, endpoint="http://localhost:11435")

    def test_plan_hash_tamper_is_rejected(self):
        task = task_bytes()
        value = finalize(plan(), task)
        value["manifest_hash"] = "sha256:tampered"
        with patch.object(MODULE, "http_json", side_effect=fake_http):
            with self.assertRaisesRegex(MODULE.PrimaryCandidateError, "plan hash mismatch"):
                MODULE.run_primary_candidate(plan=value, task_bytes=task, endpoint="http://127.0.0.1:11435")

    def test_task_blob_tamper_is_rejected(self):
        task = task_bytes()
        value = finalize(plan(), task)
        with patch.object(MODULE, "http_json", side_effect=fake_http):
            with self.assertRaisesRegex(MODULE.PrimaryCandidateError, "task source blob mismatch"):
                MODULE.run_primary_candidate(plan=value, task_bytes=b'{"task_id":"SV-RECON-001","events":[1]}', endpoint="http://127.0.0.1:11435")


if __name__ == "__main__":
    unittest.main()
