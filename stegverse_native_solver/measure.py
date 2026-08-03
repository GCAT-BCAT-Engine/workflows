#!/usr/bin/env python3
import hashlib, json, pathlib, time

import tiktoken

ROOT = pathlib.Path(__file__).parent
RESULTS = ROOT / "results"
ARTIFACT = RESULTS / "sv-math-001-native.md"
ASSEMBLY = RESULTS / "assembly-receipt.json"
VALIDATION = RESULTS / "validation-receipt.json"

start = time.perf_counter()
artifact = ARTIFACT.read_text()
assembly = json.loads(ASSEMBLY.read_text())
validation = json.loads(VALIDATION.read_text())
enc = tiktoken.get_encoding("cl100k_base")
output_tokens = len(enc.encode(artifact))
source_tokens = 0
for source in assembly["source_records"]:
    source_tokens += len(enc.encode((ROOT / source["path"]).read_text()))

record = {
    "lane_id": "stegverse-only",
    "capability_type": "deterministic_repository_native_reconstruction",
    "canonical_tokenizer": "cl100k_base",
    "canonical_source_input_tokens": source_tokens,
    "canonical_artifact_output_tokens": output_tokens,
    "canonical_total_tokens": source_tokens + output_tokens,
    "repository_files_read": assembly["repository_files_read"],
    "repository_bytes_read": assembly["repository_bytes_read"],
    "artifact_storage_bytes": assembly["artifact_storage_bytes"],
    "assembly_runtime_seconds": assembly["deterministic_runtime_seconds"],
    "validation_runtime_seconds": validation["validation_runtime_seconds"],
    "measurement_runtime_seconds": time.perf_counter() - start,
    "external_provider_calls": 0,
    "actual_provider_api_cost_usd": 0.0,
    "valid_equivalent_artifact": validation["valid_equivalent_artifact"],
    "lean_status": validation["lean_status"],
    "artifact_sha256": "sha256:" + hashlib.sha256(artifact.encode()).hexdigest(),
    "claim_boundary": "Cost covers deterministic repository-native reconstruction and verification, not independent native theorem discovery."
}
(RESULTS / "native-cost-record.json").write_text(json.dumps(record, indent=2))
print(json.dumps(record))
raise SystemExit(0 if record["valid_equivalent_artifact"] else 2)
