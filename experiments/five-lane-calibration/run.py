#!/usr/bin/env python3
import hashlib,json,os,pathlib,re,time,urllib.request
R=pathlib.Path(__file__).parent; O=R/'results'; RAW=O/'raw'; RAW.mkdir(parents=True,exist_ok=True)
LANES=[('openai-raw','openai',False),('openai-governed','openai',True),('anthropic-raw','anthropic',False),('anthropic-governed','anthropic',True),('stegverse-only','stegverse',True)]
TASK='''Produce a full formal proof for SV-MATH-001: prove necessary and sufficient conditions for ALLOW gate admissibility in the GCAT/BCAT engine, establishing whether geometric boundary preservation, bounded divergence, and ontological consistency are jointly complete. Include definitions, theorem statements, proof reasoning, and formal or categorical rewriting content. Do not replace the proof with commentary about the prompt.'''
GOV='''StegVerse governed execution: preserve task identity and output type; state assumptions; separate generated claims from verified claims; identify evidence needed for Lean 4 verification; do not claim verification that was not performed; preserve a bounded claim boundary.'''
EST='''Do not solve the theorem. Estimate only model inference/search effort for a bounded autonomous attempt at quantum parallel repetition (TA-006). Exclude salaries, institutional overhead, procurement, and unspecified research-program costs. Return JSON with estimated_input_tokens, estimated_output_tokens, estimated_reasoning_tokens, estimated_branches, estimated_retries, cost_low_usd, cost_central_usd, cost_high_usd, elapsed_hours_low, elapsed_hours_central, elapsed_hours_high, success_probability, assumptions, uncertainty_drivers, verification_cost_usd, governance_overhead_usd. Show a bounded attempt, not an entire research institution.'''

def post(url,h,b):
 q=urllib.request.Request(url,data=json.dumps(b).encode(),headers=h,method='POST');
 with urllib.request.urlopen(q,timeout=600) as x:return json.loads(x.read())
def openai(text,maxout=4096):
 model=os.getenv('OPENAI_CALIBRATION_MODEL','gpt-5.6'); t=time.time(); d=post('https://api.openai.com/v1/responses',{'Authorization':'Bearer '+os.environ['OPENAI_API_KEY'],'Content-Type':'application/json'},{'model':model,'input':text,'max_output_tokens':maxout}); out=d.get('output_text') or ''.join(c.get('text','') for i in d.get('output',[]) for c in i.get('content',[]) if c.get('type')=='output_text'); u=d.get('usage',{}); return model,out,d,u.get('input_tokens',0),u.get('output_tokens',0),time.time()-t
def anthropic(text,maxout=4096):
 model=os.getenv('ANTHROPIC_CALIBRATION_MODEL','claude-sonnet-4-6'); t=time.time(); d=post('https://api.anthropic.com/v1/messages',{'x-api-key':os.environ['ANTHROPIC_API_KEY'],'anthropic-version':'2023-06-01','content-type':'application/json'},{'model':model,'max_tokens':maxout,'messages':[{'role':'user','content':text}]}); out=''.join(x.get('text','') for x in d.get('content',[]) if x.get('type')=='text'); u=d.get('usage',{}); return model,out,d,u.get('input_tokens',0),u.get('output_tokens',0),time.time()-t
def parsej(s):
 a=s.find('{');b=s.rfind('}');return json.loads(s[a:b+1])
def price(p,i,o): return (i*(5 if p=='openai' else 3)+o*(30 if p=='openai' else 15))/1e6
def receipt(raw):return 'sha256:'+hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest()
cal=[]; est=[]
for lid,p,g in LANES:
 if p=='stegverse':
  cal.append({'lane_id':lid,'provider':p,'status':'BLOCKED_NO_LOCAL_INFERENCE','input_tokens':0,'output_tokens':0,'latency_seconds':0,'observed_cost_usd':0,'task_identity_preserved':True,'output_type':'no_generated_proof','receipt_hash':receipt({'provider_denied':True})})
  est.append({'lane_id':lid,'provider':p,'status':'BLOCKED_CAPABILITY_INVENTORY','cost_low_usd':0,'cost_central_usd':0,'cost_high_usd':0,'success_probability':0,'assumptions':['No undeclared provider inference'],'uncertainty_drivers':['Installed local theorem-generation capability not established'],'receipt_hash':receipt({'provider_denied':True})});continue
 prompt=(GOV+'\n\n' if g else '')+TASK
 model,out,raw,i,o,lat=(openai(prompt) if p=='openai' else anthropic(prompt)); (RAW/f'calibration-{lid}.json').write_text(json.dumps(raw,indent=2));
 cal.append({'lane_id':lid,'provider':p,'model':model,'status':'EXECUTED','input_tokens':i,'output_tokens':o,'latency_seconds':lat,'observed_cost_usd':price(p,i,o),'task_identity_preserved':('proof' in out.lower() and len(out)>1000),'output_type':'formal_proof_candidate','receipt_hash':receipt(raw)})
 ep=(GOV+'\n\n' if g else '')+EST; model,eout,eraw,ei,eo,elat=(openai(ep,2500) if p=='openai' else anthropic(ep,2500)); (RAW/f'estimate-{lid}.json').write_text(json.dumps(eraw,indent=2)); rec=parsej(eout);rec.update({'lane_id':lid,'provider':p,'model':model,'observed_estimation_call_cost_usd':price(p,ei,eo),'observed_estimation_latency_seconds':elat,'receipt_hash':receipt(eraw)});est.append(rec)
 time.sleep(1)
(O/'calibration.json').write_text(json.dumps(cal,indent=2));(O/'ta006-estimates.json').write_text(json.dumps(est,indent=2))
valid=len(cal)==5 and len(est)==5 and all(x.get('receipt_hash') for x in cal+est)
report=['# Five-Lane Observed Calibration and TA-006 Estimate','',f'Status: {"VALID" if valid else "INVALID"}','','## Observed SV-MATH-001 calibration','','| Lane | Status | Input | Output | Latency s | Observed API cost |','|---|---|---:|---:|---:|---:|']
for x in cal:report.append(f"| {x['lane_id']} | {x['status']} | {x.get('input_tokens',0)} | {x.get('output_tokens',0)} | {x.get('latency_seconds',0):.2f} | ${x.get('observed_cost_usd',0):.6f} |")
report+=['','## TA-006 bounded estimates','','| Lane | Low | Central | High | Success probability | Estimation-call cost |','|---|---:|---:|---:|---:|---:|']
for x in est:report.append(f"| {x['lane_id']} | ${x.get('cost_low_usd',0):,.2f} | ${x.get('cost_central_usd',0):,.2f} | ${x.get('cost_high_usd',0):,.2f} | {x.get('success_probability',0)} | ${x.get('observed_estimation_call_cost_usd',0):.6f} |")
(O/'report.md').write_text('\n'.join(report)+'\n');print(json.dumps({'valid':valid,'calibration':len(cal),'estimates':len(est)}));raise SystemExit(0 if valid else 2)
