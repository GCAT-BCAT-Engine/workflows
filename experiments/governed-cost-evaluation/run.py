#!/usr/bin/env python3
import hashlib,json,os,pathlib,time,urllib.request
ROOT=pathlib.Path(__file__).parent
OUT=ROOT/'results'; RAW=OUT/'raw'; RAW.mkdir(parents=True,exist_ok=True)
TASK='''Produce a full formal proof for SV-MATH-001: prove necessary and sufficient conditions for ALLOW gate admissibility in the GCAT/BCAT engine, establishing whether geometric boundary preservation, bounded divergence, and ontological consistency are jointly complete. Include definitions, theorem statements, proof reasoning, and formal or categorical rewriting content. Do not replace the proof with commentary about the prompt.'''
GOV='''StegVerse governed execution requirements: preserve task identity and output type; state assumptions; distinguish generated claims from verified claims; identify evidence needed for Lean 4 verification; do not claim verification that was not performed; preserve a bounded claim boundary; emit a proof candidate plus a concise verification ledger.'''

def post(url,headers,body):
    req=urllib.request.Request(url,data=json.dumps(body).encode(),headers=headers,method='POST')
    with urllib.request.urlopen(req,timeout=600) as r:return json.loads(r.read())

def sha(raw):return 'sha256:'+hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest()

def openai():
    model=os.getenv('OPENAI_CALIBRATION_MODEL','gpt-5.6'); start=time.time()
    raw=post('https://api.openai.com/v1/responses',{'Authorization':'Bearer '+os.environ['OPENAI_API_KEY'],'Content-Type':'application/json'},{'model':model,'input':GOV+'\n\n'+TASK,'max_output_tokens':4096})
    text=raw.get('output_text') or ''.join(c.get('text','') for i in raw.get('output',[]) for c in i.get('content',[]) if c.get('type')=='output_text')
    u=raw.get('usage',{}); i=u.get('input_tokens',0); o=u.get('output_tokens',0)
    return {'lane_id':'stegverse-openai','provider':'openai','model':model,'input_tokens':i,'output_tokens':o,'latency_seconds':time.time()-start,'observed_api_cost_usd':(i*5+o*30)/1e6,'task_identity_preserved':('proof' in text.lower() and len(text)>1000),'output_type':'formal_proof_candidate','receipt_hash':sha(raw)},raw

def anthropic():
    model=os.getenv('ANTHROPIC_CALIBRATION_MODEL','claude-sonnet-4-6'); start=time.time()
    raw=post('https://api.anthropic.com/v1/messages',{'x-api-key':os.environ['ANTHROPIC_API_KEY'],'anthropic-version':'2023-06-01','content-type':'application/json'},{'model':model,'max_tokens':4096,'messages':[{'role':'user','content':GOV+'\n\n'+TASK}]})
    text=''.join(x.get('text','') for x in raw.get('content',[]) if x.get('type')=='text')
    u=raw.get('usage',{}); i=u.get('input_tokens',0); o=u.get('output_tokens',0)
    return {'lane_id':'stegverse-anthropic','provider':'anthropic','model':model,'input_tokens':i,'output_tokens':o,'latency_seconds':time.time()-start,'observed_api_cost_usd':(i*3+o*15)/1e6,'task_identity_preserved':('proof' in text.lower() and len(text)>1000),'output_type':'formal_proof_candidate','receipt_hash':sha(raw)},raw

records=[]
for fn in (openai,anthropic):
    rec,raw=fn(); records.append(rec); (RAW/f"{rec['lane_id']}.json").write_text(json.dumps(raw,indent=2))
(OUT/'cost-evaluation.json').write_text(json.dumps(records,indent=2))
valid=len(records)==2 and all(r['task_identity_preserved'] and r['receipt_hash'] for r in records)
lines=['# StegVerse-Governed Cost Evaluation','',f'Status: {"VALID" if valid else "INVALID"}','','| Lane | Model | Input tokens | Output tokens | Latency (s) | Observed API cost |','|---|---|---:|---:|---:|---:|']
for r in records:lines.append(f"| {r['lane_id']} | {r['model']} | {r['input_tokens']} | {r['output_tokens']} | {r['latency_seconds']:.2f} | ${r['observed_api_cost_usd']:.6f} |")
(OUT/'report.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'valid':valid,'records':2})); raise SystemExit(0 if valid else 2)
