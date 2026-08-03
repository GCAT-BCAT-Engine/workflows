#!/usr/bin/env python3
import hashlib, json, pathlib, re, subprocess, tempfile, time

ROOT = pathlib.Path(__file__).parent
RESULTS = ROOT / "results"
ARTIFACT = RESULTS / "sv-math-001-native.md"
REQUIRED = [
    "SECTION 1: ASSUMPTIONS AND CLAIM BOUNDARY",
    "SECTION 2: DEFINITIONS",
    "SECTION 3: THEOREM STATEMENT",
    "SECTION 4: MATHEMATICAL PROOF",
    "SECTION 5: LEAN 4 CANDIDATE",
    "SECTION 6: VERIFICATION LEDGER",
    "SECTION 7: FINAL CLAIM BOUNDARY",
    "END_OF_ARTIFACT",
]

def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()

start = time.perf_counter()
if not ARTIFACT.exists():
    result = {"status": "BLOCKED_NO_ARTIFACT", "valid": False}
    (RESULTS / "validation-receipt.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result)); raise SystemExit(3)

text = ARTIFACT.read_text()
missing = [x for x in REQUIRED if x not in text]
ordered_positions = [text.find(x) for x in REQUIRED]
ordered = all(a < b for a, b in zip(ordered_positions, ordered_positions[1:])) and not missing
claim_boundary_ok = any(k in text.lower() for k in ("stipulat", "conforming implementation", "authoritative specification"))
proof_substantive = len(text.split("SECTION 4: MATHEMATICAL PROOF", 1)[-1].split("SECTION 5: LEAN 4 CANDIDATE", 1)[0]) >= 1000 if "SECTION 4: MATHEMATICAL PROOF" in text and "SECTION 5: LEAN 4 CANDIDATE" in text else False

lean_blocks = re.findall(r"```lean\s*(.*?)```", text, flags=re.S | re.I)
lean_status = "NOT_PRESENT"
lean_returncode = None
lean_stdout = ""
if lean_blocks:
    lean_status = "PRESENT_NOT_EXECUTED"
    if subprocess.run(["bash", "-lc", "command -v lake >/dev/null 2>&1"], check=False).returncode == 0:
        with tempfile.TemporaryDirectory() as td:
            p = pathlib.Path(td) / "Main.lean"
            p.write_text("\n\n".join(lean_blocks))
            proc = subprocess.run(["lake", "env", "lean", str(p)], capture_output=True, text=True, timeout=300)
            lean_returncode = proc.returncode
            lean_stdout = (proc.stdout + "\n" + proc.stderr)[-12000:]
            lean_status = "PASS" if proc.returncode == 0 else "FAIL"

valid_structure = not missing and ordered and proof_substantive and claim_boundary_ok
valid_equivalent_artifact = valid_structure and lean_status == "PASS"
result = {
    "status": "VALID_EQUIVALENT_ARTIFACT" if valid_equivalent_artifact else "STRUCTURE_VALID_PENDING_LEAN" if valid_structure else "INVALID_ARTIFACT",
    "valid_structure": valid_structure,
    "valid_equivalent_artifact": valid_equivalent_artifact,
    "missing_contract_items": missing,
    "sections_ordered": ordered,
    "substantive_proof_present": proof_substantive,
    "claim_boundary_present": claim_boundary_ok,
    "lean_status": lean_status,
    "lean_returncode": lean_returncode,
    "lean_output_tail": lean_stdout,
    "artifact_sha256": sha256(text.encode()),
    "validation_runtime_seconds": time.perf_counter() - start,
    "claim_boundary": "Equivalent-output status requires structural validity and an actually executed Lean PASS."
}
(RESULTS / "validation-receipt.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result))
raise SystemExit(0 if valid_structure else 2)
