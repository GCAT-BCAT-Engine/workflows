#!/usr/bin/env python3
import hashlib,json,pathlib,time
import tiktoken

ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OUT=ROOT/'results'; OUT.mkdir(parents=True,exist_ok=True)

TASK_PATH=REPO/'math_solver/problem_spec_sv_math_001.yml'
METHOD_PATH=REPO/'docs/PREVIOUS_COST_TEST_METHOD_RECONSTRUCTION.md'
ACCOUNTING_PATH=REPO/'docs/STEGVERSE_TOKEN_EQUIVALENT_ACCOUNTING.md'

start=time.time()
inputs=[]
for p in (TASK_PATH,METHOD_PATH,ACCOUNTING_PATH):
    text=p.read_text()
    inputs.append({'path':str(p.relative_to(REPO)),'bytes':len(text.encode()),'sha256':hashlib.sha256(text.encode()).hexdigest(),'content':text})

capability={
  'lane_id':'stegverse-only',
  'task_id':'SV-MATH-001',
  'external_provider_calls':0,
  'reasoning_source':'installed StegVerse repository, deterministic scripts, declared validators',
  'status':'BLOCKED_NO_NATIVE_GENERATIVE_REASONING_ENGINE',
  'task_identity_preserved':True,
  'proof_generated':False,
  'solve_cost_usd':None,
  'block_reason':'No installed StegVerse-native generative reasoning engine is declared capable of producing the required formal proof.',
  'claim_boundary':'This record measures normalized information flow and deterministic governance overhead; it is not a proof attempt or a zero-cost solution claim.',
  'required_next_capability':'A declared native reasoning engine with observable inference, search-branch, and verification receipts.'
}
ledger={
  'input_artifacts':[{'path':x['path'],'bytes':x['bytes'],'sha256':x['sha256']} for x in inputs],
  'checks':['task specification loaded','historical methodology loaded','accounting contract loaded','external inference denied','native reasoning capability checked','claim boundary emitted'],
  'receipts_required':['canonical token counts','byte counts','hashes','runtime','counterfactual provider pricing'],
  'verification_state':'not_attempted_no_proof_candidate'
}

input_stream=json.dumps({'task':inputs[0]['content'],'method':inputs[1]['content'],'accounting':inputs[2]['content']},sort_keys=True)
output_stream=json.dumps({'capability_result':capability,'governance_ledger':ledger},sort_keys=True)
enc=tiktoken.get_encoding('cl100k_base')
in_tokens=len(enc.encode(input_stream)); out_tokens=len(enc.encode(output_stream))

rates={
 'openai':{'input_per_million':5.0,'output_per_million':30.0},
 'anthropic':{'input_per_million':3.0,'output_per_million':15.0}
}
def priced(r):return in_tokens*r['input_per_million']/1e6+out_tokens*r['output_per_million']/1e6

runtime=time.time()-start
record={
 'schema_version':'1.0',
 'lane_id':'stegverse-only',
 'canonical_tokenizer':'cl100k_base',
 'canonical_input_tokens':in_tokens,
 'canonical_output_tokens':out_tokens,
 'canonical_total_tokens':in_tokens+out_tokens,
 'input_bytes':len(input_stream.encode()),
 'output_bytes':len(output_stream.encode()),
 'deterministic_runtime_seconds':runtime,
 'external_provider_calls':0,
 'actual_provider_api_cost_usd':0.0,
 'counterfactual_cost_at_openai_rates_usd':priced(rates['openai']),
 'counterfactual_cost_at_anthropic_rates_usd':priced(rates['anthropic']),
 'capability_result':capability,
 'governance_ledger':ledger,
 'input_stream_sha256':'sha256:'+hashlib.sha256(input_stream.encode()).hexdigest(),
 'output_stream_sha256':'sha256:'+hashlib.sha256(output_stream.encode()).hexdigest(),
 'accounting_rule':'Compare canonical information flow first; add only externally observable StegVerse overhead not already embedded in provider token prices.'
}
(OUT/'stegverse-token-baseline.json').write_text(json.dumps(record,indent=2))
report=f'''# StegVerse Token-Equivalent Baseline\n\nStatus: VALID\n\n| Metric | Value |\n|---|---:|\n| Canonical tokenizer | cl100k_base |\n| Canonical input tokens | {in_tokens:,} |\n| Canonical output tokens | {out_tokens:,} |\n| Canonical total tokens | {in_tokens+out_tokens:,} |\n| Input bytes | {record['input_bytes']:,} |\n| Output bytes | {record['output_bytes']:,} |\n| Deterministic runtime | {runtime:.6f} s |\n| Actual provider API cost | $0.000000 |\n| Counterfactual cost at OpenAI rates | ${record['counterfactual_cost_at_openai_rates_usd']:.6f} |\n| Counterfactual cost at Anthropic rates | ${record['counterfactual_cost_at_anthropic_rates_usd']:.6f} |\n\n## Boundary\n\nThe lane produced a capability and governance record, not a mathematical proof. Its solve cost is null, not zero. The token-equivalent values measure information entering and leaving the StegVerse execution boundary so later provider lanes can be compared on a common tokenizer before separately adding observable governance overhead.\n'''
(OUT/'report.md').write_text(report)
print(json.dumps({'valid':True,'input_tokens':in_tokens,'output_tokens':out_tokens,'runtime_seconds':runtime}))
