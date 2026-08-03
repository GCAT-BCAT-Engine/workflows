#!/usr/bin/env python3
import hashlib, json, os, pathlib, time, urllib.request
import tiktoken

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)
CONTRACT = json.loads((ROOT / "stage_contract.json").read_text())
ENC = tiktoken.get_encoding(CONTRACT["canonical_tokenizer"])

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
OPENAI_IN = float(os.getenv("OPENAI_INPUT_USD_PER_M", "5"))
OPENAI_OUT = float(os.getenv("OPENAI_OUTPUT_USD_PER_M", "30"))
ANTHROPIC_IN = float(os.getenv("ANTHROPIC_INPUT_USD_PER_M", "3"))
ANTHROPIC_OUT = float(os.getenv("ANTHROPIC_OUTPUT_USD_PER_M", "15"))
MAX_STAGE_OUTPUT = int(os.getenv("MAX_STAGE_OUTPUT", "900"))

LANES = [
    ("openai-only", "openai", False),
    ("stegverse-openai", "openai", True),
    ("anthropic-only", "anthropic", False),
    ("stegverse-anthropic", "anthropic", True),
]

GOVERNANCE = """STEGVERSE GOVERNANCE BLOCK:
Preserve the exact task identity and stipulated abstract evaluator. Work only on the requested stage. Reuse admitted prior-stage artifacts without redefining the mathematical universe. Separate stipulated assumptions, generated claims, verified claims, and unresolved implementation evidence. Do not claim a deployed GCAT/BCAT implementation conforms. End with a compact stage receipt containing STAGE_STATUS, REUSED_ARTIFACTS, NEW_CLAIMS, UNRESOLVED, and NEXT_STAGE.
"""

def tok(text): return len(ENC.encode(text))
def sha(text): return "sha256:" + hashlib.sha256(text.encode()).hexdigest()

def post(url, headers, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())

def call_openai(prompt):
    raw = post("https://api.openai.com/v1/responses", {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": "application/json"
    }, {"model": OPENAI_MODEL, "input": prompt, "max_output_tokens": MAX_STAGE_OUTPUT})
    text = "".join(x.get("text", "") for item in raw.get("output", []) for x in item.get("content", []) if x.get("type") == "output_text")
    u = raw.get("usage", {})
    return raw, text, int(u.get("input_tokens", 0)), int(u.get("output_tokens", 0)), raw.get("status", "unknown")

def call_anthropic(prompt):
    raw = post("https://api.anthropic.com/v1/messages", {
        "x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "Content-Type": "application/json"
    }, {"model": ANTHROPIC_MODEL, "max_tokens": MAX_STAGE_OUTPUT, "messages": [{"role": "user", "content": prompt}]})
    text = "".join(x.get("text", "") for x in raw.get("content", []) if x.get("type") == "text")
    u = raw.get("usage", {})
    return raw, text, int(u.get("input_tokens", 0)), int(u.get("output_tokens", 0)), raw.get("stop_reason", "unknown")

def validate(stage, text):
    low = text.lower()
    missing = [x for x in stage["required"] if x.lower() not in low]
    forbidden = any(x in low for x in ["deployed engine satisfies", "production engine satisfies", "verified deployed implementation"])
    return {"admitted": not missing and not forbidden, "missing_evidence": missing, "forbidden_claim": forbidden}

def prompt_for(stage, admitted, governed):
    prior = "\n\n".join(f"[{x['stage_id']} ADMITTED]\n{x['output']}" for x in admitted)
    return f"""EXPERIMENT: {CONTRACT['experiment_id']}
PROBLEM: {CONTRACT['canonical_problem']}
CURRENT STAGE: {stage['id']} — {stage['name']}
REQUIRED EVIDENCE: {json.dumps(stage['required'])}

Produce only the artifact needed to complete the current stage. Be concise because every serialized token is charged to the normalized budget. Do not skip ahead except where a definition or statement is strictly required for coherence.

ADMITTED PRIOR ARTIFACTS:
{prior or '[none]'}

{GOVERNANCE if governed else ''}
Return a self-contained stage artifact headed exactly: {stage['id']}: {stage['name']}.
"""

def run_lane(lane_id, provider, governed):
    admitted, records = [], []
    native_in = native_out = canonical_in = canonical_out = 0
    cost = latency = 0.0
    reached = "NONE"
    checkpoint_rows = []
    for stage in CONTRACT["stages"]:
        prompt = prompt_for(stage, admitted, governed)
        pin = tok(prompt)
        start = time.perf_counter()
        if provider == "openai": raw, text, ni, no, status = call_openai(prompt)
        else: raw, text, ni, no, status = call_anthropic(prompt)
        elapsed = time.perf_counter() - start
        pout = tok(text)
        v = validate(stage, text)
        native_in += ni; native_out += no; canonical_in += pin; canonical_out += pout; latency += elapsed
        if provider == "openai": stage_cost = ni/1e6*OPENAI_IN + no/1e6*OPENAI_OUT
        else: stage_cost = ni/1e6*ANTHROPIC_IN + no/1e6*ANTHROPIC_OUT
        cost += stage_cost
        rec = {"stage_id": stage["id"], "name": stage["name"], "provider_status": status,
               "native_input_tokens": ni, "native_output_tokens": no,
               "canonical_input_tokens": pin, "canonical_output_tokens": pout,
               "canonical_cumulative_tokens": canonical_in + canonical_out,
               "observed_api_cost_usd": stage_cost, "cumulative_cost_usd": cost,
               "latency_seconds": elapsed, "validation": v, "prompt_hash": sha(prompt), "output_hash": sha(text), "output": text}
        records.append(rec)
        (OUT / f"{lane_id}-{stage['id']}.txt").write_text(text)
        (OUT / f"{lane_id}-{stage['id']}-raw.json").write_text(json.dumps(raw, indent=2))
        if v["admitted"]:
            admitted.append(rec); reached = stage["id"]
        else:
            break
        cumulative = canonical_in + canonical_out
        for cp in CONTRACT["checkpoints"]:
            if cp <= cumulative and not any(x["checkpoint"] == cp for x in checkpoint_rows):
                checkpoint_rows.append({"checkpoint": cp, "highest_admitted_stage": reached, "actual_canonical_tokens_at_observation": cumulative, "cumulative_cost_usd": cost})
    return {"lane_id": lane_id, "provider": provider, "governed": governed, "highest_admitted_stage": reached,
            "admitted_stage_count": len(admitted), "canonical_input_tokens": canonical_in, "canonical_output_tokens": canonical_out,
            "canonical_total_tokens": canonical_in + canonical_out, "native_input_tokens": native_in, "native_output_tokens": native_out,
            "observed_api_cost_usd": cost, "latency_seconds": latency, "checkpoints": checkpoint_rows, "stages": records}

results = [run_lane(*lane) for lane in LANES]
(OUT / "staged-results.json").write_text(json.dumps(results, indent=2))
lines = ["# Staged Mathematical Progress Benchmark", "", "Status: MEASURED", "", "| Lane | Highest admitted stage | Admitted stages | Canonical tokens | API cost | Latency s |", "|---|---:|---:|---:|---:|---:|"]
for r in results:
    lines.append(f"| {r['lane_id']} | {r['highest_admitted_stage']} | {r['admitted_stage_count']} | {r['canonical_total_tokens']:,} | ${r['observed_api_cost_usd']:.6f} | {r['latency_seconds']:.2f} |")
lines += ["", "## Boundary", "", CONTRACT["claim_boundary"], "", "A stage is counted only after deterministic evidence-string validation. The benchmark measures serialized progress and observed provider cost; it does not expose or equate hidden provider reasoning."]
(OUT / "report.md").write_text("\n".join(lines) + "\n")
print(json.dumps([{k:v for k,v in r.items() if k != 'stages'} for r in results], indent=2))
