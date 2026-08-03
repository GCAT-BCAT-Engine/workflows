#!/usr/bin/env python3
import hashlib, json, os, pathlib, time, urllib.request
import tiktoken

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "results"
RAW = OUT / "raw"
TEXT = OUT / "outputs"
for p in (RAW, TEXT): p.mkdir(parents=True, exist_ok=True)

ENC = tiktoken.get_encoding("cl100k_base")
MAX_OUT = int(os.getenv("FOUR_LANE_MAX_OUTPUT_TOKENS", "8192"))

TASK = """Produce SV-MATH-001 as one complete mathematical artifact. Prove necessary and sufficient conditions for ALLOW gate admissibility in the GCAT/BCAT engine, addressing whether geometric boundary preservation, bounded divergence, and ontological consistency are jointly complete. Include a Lean 4 proof candidate. Do not substitute commentary for the requested artifact.

Return exactly these sections in order:
SECTION 1: ASSUMPTIONS AND CLAIM BOUNDARY
SECTION 2: DEFINITIONS
SECTION 3: THEOREM STATEMENT
SECTION 4: MATHEMATICAL PROOF
SECTION 5: LEAN 4 CANDIDATE
SECTION 6: VERIFICATION LEDGER
SECTION 7: FINAL CLAIM BOUNDARY
END_OF_ARTIFACT
"""

GOV = """StegVerse governed execution requirements:
- preserve task identity and the exact output contract;
- distinguish stipulated assumptions, generated claims, and verified claims;
- do not claim Lean compilation unless it was actually performed;
- identify evidence needed to bind the abstract theorem to a deployed GCAT/BCAT engine;
- retain a bounded public claim;
- include reconstruction-ready verification entries and explicit unresolved dependencies.
"""

SECTIONS = [
    "SECTION 1: ASSUMPTIONS AND CLAIM BOUNDARY",
    "SECTION 2: DEFINITIONS",
    "SECTION 3: THEOREM STATEMENT",
    "SECTION 4: MATHEMATICAL PROOF",
    "SECTION 5: LEAN 4 CANDIDATE",
    "SECTION 6: VERIFICATION LEDGER",
    "SECTION 7: FINAL CLAIM BOUNDARY",
]

def post(url, headers, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=1200) as r:
        return json.loads(r.read())

def digest(x):
    data = x if isinstance(x, bytes) else json.dumps(x, sort_keys=True).encode()
    return "sha256:" + hashlib.sha256(data).hexdigest()

def count(s): return len(ENC.encode(s or ""))

def extract_openai(raw):
    text = raw.get("output_text") or "".join(
        c.get("text", "") for item in raw.get("output", [])
        for c in item.get("content", []) if c.get("type") == "output_text"
    )
    u = raw.get("usage", {})
    return text, int(u.get("input_tokens", 0)), int(u.get("output_tokens", 0)), raw.get("status")

def extract_anthropic(raw):
    text = "".join(x.get("text", "") for x in raw.get("content", []) if x.get("type") == "text")
    u = raw.get("usage", {})
    stop = raw.get("stop_reason")
    status = "completed" if stop == "end_turn" else f"stopped:{stop}"
    return text, int(u.get("input_tokens", 0)), int(u.get("output_tokens", 0)), status

def validate(text, provider_status):
    missing = [s for s in SECTIONS if s not in text]
    marker = text.rstrip().endswith("END_OF_ARTIFACT")
    lean = "```lean" in text.lower() or "namespace " in text
    proof = "SECTION 4: MATHEMATICAL PROOF" in text and len(text.split("SECTION 4: MATHEMATICAL PROOF",1)[-1]) > 1000
    complete = not missing and marker and lean and proof and provider_status in ("completed", "completed")
    return {"complete": complete, "missing_sections": missing, "end_marker": marker, "lean_candidate_present": lean, "substantive_proof_present": proof}

def run_openai(governed):
    model = os.getenv("OPENAI_EQUIVALENT_MODEL", "gpt-5.6")
    prompt = (GOV + "\n\n" if governed else "") + TASK
    start = time.time()
    raw = post("https://api.openai.com/v1/responses", {
        "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"],
        "Content-Type": "application/json",
    }, {"model": model, "input": prompt, "max_output_tokens": MAX_OUT})
    latency = time.time() - start
    text, native_in, native_out, status = extract_openai(raw)
    lane = "stegverse-openai" if governed else "openai-only"
    return lane, model, prompt, text, native_in, native_out, status, latency, raw

def run_anthropic(governed):
    model = os.getenv("ANTHROPIC_EQUIVALENT_MODEL", "claude-sonnet-4-6")
    prompt = (GOV + "\n\n" if governed else "") + TASK
    start = time.time()
    raw = post("https://api.anthropic.com/v1/messages", {
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }, {"model": model, "max_tokens": MAX_OUT, "messages": [{"role": "user", "content": prompt}]})
    latency = time.time() - start
    text, native_in, native_out, status = extract_anthropic(raw)
    lane = "stegverse-anthropic" if governed else "anthropic-only"
    return lane, model, prompt, text, native_in, native_out, status, latency, raw

records = []
for fn, governed in ((run_openai, False), (run_openai, True), (run_anthropic, False), (run_anthropic, True)):
    lane, model, prompt, text, ni, no, pstatus, latency, raw = fn(governed)
    validation = validate(text, pstatus)
    task_tokens = count(TASK)
    gov_tokens = count(GOV) if governed else 0
    canonical_out = count(text)
    if lane.endswith("openai") or lane == "openai-only":
        in_rate = float(os.getenv("OPENAI_INPUT_USD_PER_M", "5")); out_rate = float(os.getenv("OPENAI_OUTPUT_USD_PER_M", "30"))
    else:
        in_rate = float(os.getenv("ANTHROPIC_INPUT_USD_PER_M", "3")); out_rate = float(os.getenv("ANTHROPIC_OUTPUT_USD_PER_M", "15"))
    rec = {
        "lane_id": lane, "provider": "openai" if "openai" in lane else "anthropic", "model": model,
        "governed": governed, "provider_status": pstatus, "max_output_tokens": MAX_OUT,
        "native_input_tokens": ni, "native_output_tokens": no, "native_total_tokens": ni + no,
        "canonical_shared_task_input_tokens": task_tokens,
        "canonical_incremental_governance_input_tokens": gov_tokens,
        "canonical_total_input_tokens": count(prompt), "canonical_total_output_tokens": canonical_out,
        "canonical_total_tokens": count(prompt) + canonical_out,
        "observed_api_cost_usd": (ni * in_rate + no * out_rate) / 1_000_000,
        "pricing_assumption": {"input_usd_per_million": in_rate, "output_usd_per_million": out_rate},
        "latency_seconds": latency, "validation": validation,
        "prompt_hash": digest(prompt.encode()), "output_hash": digest(text.encode()), "raw_receipt_hash": digest(raw),
    }
    records.append(rec)
    (RAW / f"{lane}.json").write_text(json.dumps(raw, indent=2))
    (TEXT / f"{lane}.md").write_text(text)

(OUT / "four-lane-results.json").write_text(json.dumps(records, indent=2))
valid_measurement = len(records) == 4 and all(r["native_total_tokens"] > 0 and r["raw_receipt_hash"] for r in records)
complete = all(r["validation"]["complete"] for r in records)
status = "VALID_EQUIVALENT_OUTPUT" if complete else "VALID_MEASUREMENT_INCOMPLETE_OUTPUT"
lines = ["# Four-Lane Equivalent-Output Benchmark", "", f"Status: {status}", "", "| Lane | Complete | Native in | Native out | Canonical in | Canonical out | API cost | Latency s |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
for r in records:
    lines.append(f"| {r['lane_id']} | {str(r['validation']['complete']).upper()} | {r['native_input_tokens']} | {r['native_output_tokens']} | {r['canonical_total_input_tokens']} | {r['canonical_total_output_tokens']} | ${r['observed_api_cost_usd']:.6f} | {r['latency_seconds']:.2f} |")
lines += ["", "## Interpretation boundary", "", "Costs are observed API charges under the recorded pricing assumptions. A lane enters the cost-per-equivalent-output comparison only when every required section and END_OF_ARTIFACT are present. Governed and ungoverned lanes use the same task; governed lanes add only the pinned StegVerse governance block."]
(OUT / "report.md").write_text("\n".join(lines) + "\n")
print(json.dumps({"measurement_valid": valid_measurement, "all_complete": complete, "status": status}))
raise SystemExit(0 if valid_measurement else 2)
