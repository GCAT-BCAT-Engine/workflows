#!/usr/bin/env python3
import hashlib, json, pathlib, time

ROOT = pathlib.Path(__file__).parent
SECTIONS = ROOT / "approved_sections"
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

ORDER = [
    ("01-assumptions.md", "SECTION 1: ASSUMPTIONS AND CLAIM BOUNDARY"),
    ("02-definitions.md", "SECTION 2: DEFINITIONS"),
    ("03-theorem.md", "SECTION 3: THEOREM STATEMENT"),
    ("04-proof.md", "SECTION 4: MATHEMATICAL PROOF"),
    ("05-lean.md", "SECTION 5: LEAN 4 CANDIDATE"),
    ("06-ledger.md", "SECTION 6: VERIFICATION LEDGER"),
    ("07-claim-boundary.md", "SECTION 7: FINAL CLAIM BOUNDARY"),
]

def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()

start = time.perf_counter()
missing = [name for name, _ in ORDER if not (SECTIONS / name).exists()]
if missing:
    readiness = {
        "status": "BLOCKED_MISSING_APPROVED_COMPONENTS",
        "missing": missing,
        "artifact_generated": False,
        "claim_boundary": "No equivalent artifact is claimed until all approved repository-native components exist and validate."
    }
    (RESULTS / "readiness.json").write_text(json.dumps(readiness, indent=2))
    print(json.dumps(readiness))
    raise SystemExit(3)

parts = []
source_records = []
bytes_read = 0
for name, heading in ORDER:
    p = SECTIONS / name
    raw = p.read_bytes()
    text = raw.decode()
    bytes_read += len(raw)
    if heading not in text:
        text = heading + "\n\n" + text
    parts.append(text.rstrip())
    source_records.append({"path": str(p.relative_to(ROOT)), "sha256": sha256(raw), "bytes": len(raw)})

artifact = "\n\n".join(parts) + "\n\nEND_OF_ARTIFACT\n"
artifact_path = RESULTS / "sv-math-001-native.md"
artifact_path.write_text(artifact)
elapsed = time.perf_counter() - start
receipt = {
    "status": "ASSEMBLED_PENDING_VALIDATION",
    "artifact_generated": True,
    "artifact_path": str(artifact_path.relative_to(ROOT)),
    "artifact_sha256": sha256(artifact.encode()),
    "source_records": source_records,
    "repository_files_read": len(source_records),
    "repository_bytes_read": bytes_read,
    "artifact_storage_bytes": len(artifact.encode()),
    "deterministic_runtime_seconds": elapsed,
    "external_provider_calls": 0,
    "actual_provider_api_cost_usd": 0.0,
    "claim_boundary": "This artifact is deterministic reconstruction from approved repository-native components; it is not evidence of independent native inference."
}
(RESULTS / "assembly-receipt.json").write_text(json.dumps(receipt, indent=2))
print(json.dumps(receipt))
