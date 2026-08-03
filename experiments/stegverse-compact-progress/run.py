#!/usr/bin/env python3
import hashlib
import json
import os
import pathlib
import re
import time
import urllib.request

import tiktoken

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)
PROTOCOL = json.loads((ROOT / "protocol.json").read_text())
STAGES = json.loads((ROOT.parent / "staged-math-progress" / "stage_contract.json").read_text())["stages"]
ENC = tiktoken.get_encoding(PROTOCOL["canonical_tokenizer"])
MAX_OUT = int(os.getenv("MAX_STAGE_OUTPUT", str(PROTOCOL["max_stage_output_tokens"])))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", PROTOCOL["models"]["openai"])
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", PROTOCOL["models"]["anthropic"])
RATES = {
    "openai": (float(os.getenv("OPENAI_INPUT_USD_PER_M", "5")), float(os.getenv("OPENAI_OUTPUT_USD_PER_M", "30"))),
    "anthropic": (float(os.getenv("ANTHROPIC_INPUT_USD_PER_M", "3")), float(os.getenv("ANTHROPIC_OUTPUT_USD_PER_M", "15"))),
}
PROBLEM = "Characterize ALLOW admissibility for an abstract GCAT/BCAT evaluator. Let GBP, BD, and OC be predicates on a candidate transition. The evaluator returns ALLOW exactly when GBP and BD and OC all hold. Establish the necessary-and-sufficient characterization, state the claim boundary, and prepare a Lean 4 candidate for the logical core. Do not claim implementation validity."
GOVERNANCE = "Preserve task identity. Separate stipulations, generated claims, verified claims, and unresolved implementation evidence. Reuse admitted artifacts. Do not claim any deployed GCAT/BCAT implementation conforms."


def tok(text):
    return len(ENC.encode(text))


def sha(text):
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()


def post(url, headers, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=600) as response:
        return json.loads(response.read())


def call(provider, prompt):
    if provider == "openai":
        raw = post("https://api.openai.com/v1/responses", {
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": "application/json"
        }, {"model": OPENAI_MODEL, "input": prompt, "max_output_tokens": MAX_OUT})
        text = "".join(x.get("text", "") for item in raw.get("output", []) for x in item.get("content", []) if x.get("type") == "output_text")
        usage = raw.get("usage", {})
        return raw, text, int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0)), raw.get("status", "unknown")
    raw = post("https://api.anthropic.com/v1/messages", {
        "x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "Content-Type": "application/json"
    }, {"model": ANTHROPIC_MODEL, "max_tokens": MAX_OUT, "messages": [{"role": "user", "content": prompt}]})
    text = "".join(x.get("text", "") for x in raw.get("content", []) if x.get("type") == "text")
    usage = raw.get("usage", {})
    return raw, text, int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0)), raw.get("stop_reason", "unknown")


def validate(stage_id, text):
    low = text.lower()
    groups = {
        "S0": [["sv-cost-staged-001", "task identity"], ["abstract evaluator", "stipulated"], ["deployed", "implementation"], ["unresolved", "out of scope"]],
        "S1": [["gbp"], ["bd"], ["oc"], ["allow"]],
        "S2": [["necessary", "necessity"], ["sufficient", "sufficiency"], ["if and only if", "iff", "↔"]],
        "S3": [["forward", "necessity"], ["reverse", "sufficiency"]],
        "S4": [["proof"], ["forward", "necessity"], ["reverse", "sufficiency"], ["boundary", "implementation"]],
        "S5": [["```lean", "```lean4"], ["theorem"], ["allow"], ["gbp"], ["bd"], ["oc"]],
        "S6": [["verified", "verification"], ["unresolved"], ["evidence"], ["implementation", "deployed"]],
    }
    missing = []
    for alternatives in groups[stage_id]:
        if not any(term in low for term in alternatives):
            missing.append(" OR ".join(alternatives))
    forbidden = any(term in low for term in ["deployed engine satisfies", "production engine satisfies", "verified deployed implementation"])
    return {"admitted": not missing and not forbidden, "missing": missing, "forbidden_claim": forbidden}


def compact_excerpt(stage_id, text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    selected = []
    terms = {
        "S0": ["claim boundary", "deployed", "unresolved", "allow"],
        "S1": ["gbp", "bd", "oc", "allow", "admissible"],
        "S2": ["theorem", "necessary", "sufficient", "iff", "↔"],
        "S3": ["forward", "reverse", "necessity", "sufficiency", "lemma"],
        "S4": ["proof", "therefore", "hence", "conclusion"],
        "S5": ["theorem", "def ", "```lean", "by", "unfold"],
        "S6": ["verified", "unresolved", "evidence", "implementation"],
    }[stage_id]
    for line in lines:
        if any(term in line.lower() for term in terms) and line not in selected:
            selected.append(line)
        if len(selected) >= 8:
            break
    if not selected:
        selected = lines[:4]
    return "\n".join(selected)[:1800]


def ledger_text(ledger):
    slim = [{k: item[k] for k in ["artifact_id", "stage_id", "sha256", "admitted", "claims", "definitions", "unresolved", "next_stage"]} for item in ledger]
    return json.dumps(slim, separators=(",", ":"), ensure_ascii=False)


def context_for(mode, records, ledger, stage_id):
    if not records:
        return "[none]"
    if mode == "full":
        return "\n\n".join(f"[{r['stage_id']} ADMITTED {r['output_hash']}]\n{r['output']}" for r in records)
    needed = {
        "S1": ["S0"], "S2": ["S1"], "S3": ["S1", "S2"], "S4": ["S2", "S3"],
        "S5": ["S1", "S2", "S4"], "S6": ["S4", "S5"]
    }.get(stage_id, [])
    snippets = [f"[{r['stage_id']} SELECTED {r['output_hash']}]\n{r['compact_excerpt']}" for r in records if r["stage_id"] in needed]
    return "ARTIFACT_LEDGER=" + ledger_text(ledger) + "\nSELECTED_RETRIEVAL:\n" + ("\n\n".join(snippets) or "[hash references only]")


def prompt_for(stage, mode, records, ledger):
    prior = context_for(mode, records, ledger, stage["id"])
    return f"""EXPERIMENT: SV-COST-STAGED-001
CAPABILITY TEST: {PROTOCOL['experiment_id']}
PROBLEM: {PROBLEM}
CURRENT STAGE: {stage['id']} — {stage['name']}
CONTEXT MODE: {mode}
GOVERNANCE: {GOVERNANCE}

Produce only the self-contained artifact required for the current stage. Do not skip ahead. A hash proves artifact identity, not semantic content; rely only on selected retrieved content for mathematical dependencies.

ADMITTED STATE:
{prior}

Head the response exactly: {stage['id']}: {stage['name']}.
"""


def run_lane(lane):
    records, ledger = [], []
    cin = cout = nin = nout = 0
    cost = latency = 0.0
    highest = "NONE"
    for stage in STAGES:
        prompt = prompt_for(stage, lane["context_mode"], records, ledger)
        started = time.perf_counter()
        raw, text, ni, no, status = call(lane["provider"], prompt)
        elapsed = time.perf_counter() - started
        validation = validate(stage["id"], text)
        pi, po = tok(prompt), tok(text)
        in_rate, out_rate = RATES[lane["provider"]]
        stage_cost = ni / 1e6 * in_rate + no / 1e6 * out_rate
        rec = {
            "stage_id": stage["id"], "name": stage["name"], "provider_status": status,
            "native_input_tokens": ni, "native_output_tokens": no,
            "canonical_input_tokens": pi, "canonical_output_tokens": po,
            "observed_api_cost_usd": stage_cost, "latency_seconds": elapsed,
            "prompt_hash": sha(prompt), "output_hash": sha(text), "validation": validation,
            "compact_excerpt": compact_excerpt(stage["id"], text), "output": text,
        }
        records.append(rec)
        artifact = {
            "artifact_id": f"{lane['id']}:{stage['id']}", "stage_id": stage["id"], "sha256": rec["output_hash"],
            "admitted": validation["admitted"], "claims": rec["compact_excerpt"][:420],
            "definitions": rec["compact_excerpt"][:420] if stage["id"] == "S1" else "reference prior definitions",
            "unresolved": "implementation binding remains unresolved", "next_stage": f"S{int(stage['id'][1:]) + 1}" if stage["id"] != "S6" else "complete",
        }
        ledger.append(artifact)
        cin += pi; cout += po; nin += ni; nout += no; cost += stage_cost; latency += elapsed
        (OUT / f"{lane['id']}-{stage['id']}.txt").write_text(text)
        (OUT / f"{lane['id']}-{stage['id']}-raw.json").write_text(json.dumps(raw, indent=2))
        if validation["admitted"]:
            highest = stage["id"]
        else:
            break
    (OUT / f"{lane['id']}-ledger.json").write_text(json.dumps(ledger, indent=2))
    return {
        "lane_id": lane["id"], "provider": lane["provider"], "context_mode": lane["context_mode"],
        "highest_admitted_stage": highest, "admitted_stage_count": sum(1 for r in records if r["validation"]["admitted"]),
        "canonical_input_tokens": cin, "canonical_output_tokens": cout, "canonical_total_tokens": cin + cout,
        "native_input_tokens": nin, "native_output_tokens": nout, "observed_api_cost_usd": cost,
        "latency_seconds": latency, "artifact_count": len(records), "ledger_hash": sha(json.dumps(ledger, sort_keys=True)), "stages": records,
    }


results = [run_lane(lane) for lane in PROTOCOL["lanes"]]
comparisons = []
for provider in ["openai", "anthropic"]:
    full = next(r for r in results if r["provider"] == provider and r["context_mode"] == "full")
    compact = next(r for r in results if r["provider"] == provider and r["context_mode"] == "compact")
    comparisons.append({
        "provider": provider,
        "same_highest_stage": full["highest_admitted_stage"] == compact["highest_admitted_stage"],
        "full_highest_stage": full["highest_admitted_stage"], "compact_highest_stage": compact["highest_admitted_stage"],
        "canonical_input_token_delta": compact["canonical_input_tokens"] - full["canonical_input_tokens"],
        "canonical_input_reduction_percent": (1 - compact["canonical_input_tokens"] / full["canonical_input_tokens"]) * 100 if full["canonical_input_tokens"] else 0,
        "cost_delta_usd": compact["observed_api_cost_usd"] - full["observed_api_cost_usd"],
        "cost_reduction_percent": (1 - compact["observed_api_cost_usd"] / full["observed_api_cost_usd"]) * 100 if full["observed_api_cost_usd"] else 0,
    })
summary = {"experiment_id": PROTOCOL["experiment_id"], "results": results, "comparisons": comparisons, "claim_boundary": PROTOCOL["success_criteria"]["claim_boundary"]}
(OUT / "results.json").write_text(json.dumps(summary, indent=2))
lines = ["# StegVerse Compact-Context Capability Benchmark", "", "| Lane | Stage | Canonical input | Canonical total | Cost | Latency s |", "|---|---:|---:|---:|---:|---:|"]
for r in results:
    lines.append(f"| {r['lane_id']} | {r['highest_admitted_stage']} | {r['canonical_input_tokens']:,} | {r['canonical_total_tokens']:,} | ${r['observed_api_cost_usd']:.6f} | {r['latency_seconds']:.2f} |")
lines += ["", "## Full versus compact", ""]
for c in comparisons:
    lines.append(f"- {c['provider']}: same stage={c['same_highest_stage']}; canonical input reduction={c['canonical_input_reduction_percent']:.2f}%; cost reduction={c['cost_reduction_percent']:.2f}%")
lines += ["", "## Boundary", "", PROTOCOL["success_criteria"]["claim_boundary"]]
(OUT / "report.md").write_text("\n".join(lines) + "\n")
print(json.dumps({"comparisons": comparisons}, indent=2))
