#!/usr/bin/env python3
import hashlib,json,os,pathlib,time,urllib.request
import tiktoken
ROOT=pathlib.Path(__file__).parent; OUT=ROOT/'results'; RAW=OUT/'raw'; RAW.mkdir(parents=True,exist_ok=True)
ENC=tiktoken.get_encoding('cl100k_base')
TASK='''Produce a full formal proof for SV-MATH-001: prove necessary and sufficient conditions for ALLOW gate admissibility in the GCAT/BCAT engine, establishing whether geometric boundary preservation, bounded divergence, and ontological consistency are jointly complete. Include definitions, theorem statements, proof reasoning, and formal or categorical rewriting content. Do not replace the proof with commentary about the prompt.'''
GOV='''StegVerse governed execution requirements: preserve task identity and output type; state assumptions; distinguish generated claims from verified claims; identify evidence needed for Lean 4 verification; do not claim verification that was not performed; preserve a bounded claim boundary; emit a proof candidate plus a concise verification ledger.'''

def ct(s): return len(ENC.encode(s))
def h(x): return 'sha256:'+hashlib.sha256(x.encode()).hexdigest()
def post(url,headers,body):
    q=urllib.request.Request(url,data=json.dumps(body).encode(),headers=headers,method='POST')
    with urllib.request.urlopen(q,timeout=600) as r:return json.loads(r.read())
def split_output(text):
    marks=['verification ledger','verification status','claim boundary','assumptions']
    low=text.lower(); idx=min([low.find(m) for m in marks if low.find(m)>=0] or [len(text)])
    return text[:idx],text[idx:]
def openai():
    model=os.getenv('OPENAI_CALIBRATION_MODEL','gpt-5.6'); start=time.time(); prompt=GOV+'\n\n'+TASK
    raw=post('https://api.openai.com/v1/responses',{'Authorization':'Bearer '+os.environ['OPENAI_API_KEY'],'Content-Type':'application/json'},{'model':model,'input':prompt,'max_output_tokens':4096})
    text=raw.get('output_text') or ''.join(c.get('text','') for i in raw.get('output',[]) for c in i.get('content',[]) if c.get('type')=='output_text')
    u=raw.get('usage',{}); return 'stegverse-openai','openai',model,prompt,text,raw,u.get('input_tokens',0),u.get('output_tokens',0),time.time()-start

def anthropic():
    model=os.getenv('ANTHROPIC_CALIBRATION_MODEL','claude-sonnet-4-6'); start=time.time(); prompt=GOV+'\n\n'+TASK
    raw=post('https://api.anthropic.com/v1/messages',{'x-api-key':os.environ['ANTHROPIC_API_KEY'],'anthropic-version':'2023-06-01','content-type':'application/json'},{'model':model,'max_tokens':4096,'messages':[{'role':'user','content':prompt}]})
    text=''.join(x.get('text','') for x in raw.get('content',[]) if x.get('type')=='text'); u=raw.get('usage',{})
    return 'stegverse-anthropic','anthropic',model,prompt,text,raw,u.get('input_tokens',0),u.get('output_tokens',0),time.time()-start

def priced(provider,i,o): return (i*(5 if provider=='openai' else 3)+o*(30 if provider=='openai' else 15))/1e6
records=[]
for fn in (openai,anthropic):
    lane,p,model,prompt,text,raw,ni,no,lat=fn(); proof,ledger=split_output(text)
    rec={'lane_id':lane,'provider':p,'model':model,'native_input_tokens':ni,'native_output_tokens':no,'native_total_tokens':ni+no,'canonical_shared_task_input_tokens':ct(TASK),'canonical_incremental_governance_input_tokens':ct(GOV),'canonical_total_input_tokens':ct(prompt),'canonical_proof_output_tokens':ct(proof),'canonical_governance_output_tokens':ct(ledger),'canonical_total_output_tokens':ct(text),'canonical_total_tokens':ct(prompt)+ct(text),'observed_api_cost_usd':priced(p,ni,no),'latency_seconds':lat,'task_identity_preserved':('proof' in text.lower() and len(text)>1000),'prompt_hash':h(prompt),'output_hash':h(text),'raw_receipt_hash':'sha256:'+hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest()}
    records.append(rec); (RAW/f'{lane}.json').write_text(json.dumps(raw,indent=2)); (RAW/f'{lane}-output.txt').write_text(text)
(OUT/'normalized-comparison.json').write_text(json.dumps(records,indent=2))
valid=len(records)==2 and all(r['task_identity_preserved'] for r in records)
lines=['# Normalized StegVerse Provider Token Comparison','',f'Status: {"VALID" if valid else "INVALID"}','','| Lane | Native in | Native out | Canonical task in | Canonical governance in | Canonical proof out | Canonical governance out | API cost | Latency s |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in records: lines.append(f"| {r['lane_id']} | {r['native_input_tokens']} | {r['native_output_tokens']} | {r['canonical_shared_task_input_tokens']} | {r['canonical_incremental_governance_input_tokens']} | {r['canonical_proof_output_tokens']} | {r['canonical_governance_output_tokens']} | ${r['observed_api_cost_usd']:.6f} | {r['latency_seconds']:.2f} |")
lines+=['','## Accounting boundary','','Shared task content is counted once. Incremental StegVerse governance input is isolated from the task. Output is divided heuristically into proof content and governance/verification ledger content; raw responses and hashes are preserved for reconstruction. Native provider tokens remain billing receipts while cl100k_base counts provide the cross-lane comparison.']
(OUT/'report.md').write_text('\n'.join(lines)+'\n'); print(json.dumps({'valid':valid,'records':2})); raise SystemExit(0 if valid else 2)
