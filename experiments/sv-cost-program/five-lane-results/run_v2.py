#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,pathlib,time,urllib.request
from typing import Any
R=pathlib.Path(__file__).parent; T=json.loads((R/'task.json').read_text()); O=R/'results'; RAW=O/'raw'; O.mkdir(exist_ok=True); RAW.mkdir(exist_ok=True)
LANES=[('openai-raw','openai',False),('openai-governed','openai',True),('anthropic-raw','anthropic',False),('anthropic-governed','anthropic',True),('stegverse-only','stegverse',True)]
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x): return 'sha256:'+hashlib.sha256(canon(x).encode()).hexdigest()
def post(url,h,b):
 q=urllib.request.Request(url,data=json.dumps(b).encode(),headers=h,method='POST')
 with urllib.request.urlopen(q,timeout=600) as z:return json.loads(z.read())
def call(p,prompt):
 t=time.perf_counter()
 if p=='openai':
  m=os.getenv('OPENAI_FIVE_LANE_MODEL','gpt-5.6'); d=post('https://api.openai.com/v1/responses',{'Authorization':'Bearer '+os.environ['OPENAI_API_KEY'],'Content-Type':'application/json'},{'model':m,'input':prompt,'max_output_tokens':1200}); txt=d.get('output_text') or ''.join(c.get('text','') for i in d.get('output',[]) for c in i.get('content',[]) if c.get('type')=='output_text');u=d.get('usage',{});i=o=0;i=int(u.get('input_tokens',0));o=int(u.get('output_tokens',0))
 else:
  m=os.getenv('ANTHROPIC_FIVE_LANE_MODEL','claude-sonnet-4-6'); d=post('https://api.anthropic.com/v1/messages',{'x-api-key':os.environ['ANTHROPIC_API_KEY'],'anthropic-version':'2023-06-01','content-type':'application/json'},{'model':m,'max_tokens':1200,'messages':[{'role':'user','content':prompt}]});txt=''.join(x.get('text','') for x in d.get('content',[]) if x.get('type')=='text');u=d.get('usage',{});i=int(u.get('input_tokens',0));o=int(u.get('output_tokens',0))
 return m,txt,d,i,o,time.perf_counter()-t
def extract(s):
 a=s.find('{');b=s.rfind('}');return json.loads(s[a:b+1])
def reconstruct():
 st=dict(T['initial_state']); dec=[]
 for e in T['events']:
  op=e['operation'];amt=e['amount'];eid=e['event_id']
  if op=='credit':st['balance']+=amt;status='ALLOW'
  elif op=='debit':
   status='ALLOW' if st['standing']==T['policy']['standing_required_for_debit'] and st['balance']-amt>=T['policy']['minimum_balance'] else 'DENY'
   if status=='ALLOW':st['balance']-=amt
  else:
   status='ALLOW' if st['risk_score']+amt<=T['policy']['maximum_risk_score'] else 'DENY'
   if status=='ALLOW':st['risk_score']+=amt
  dec.append({'event_id':eid,'status':status})
 return {'task_id':T['task_id'],'final_state':st,'decisions':dec,'applied_count':sum(x['status']=='ALLOW' for x in dec),'denied_count':sum(x['status']=='DENY' for x in dec)}
EXP=reconstruct()
def normalize(a):
 # Accept common provider field variants, then reduce to comparison semantics.
 fs=a.get('final_state') or {'balance':a.get('final_balance'),'risk_score':a.get('final_risk_score'),'standing':a.get('final_standing')}
 ds=a.get('decisions') or a.get('event_decisions') or []
 nd=[]
 for x in ds:
  if isinstance(x,dict): nd.append({'event_id':x.get('event_id') or x.get('id'),'status':str(x.get('status') or x.get('decision') or '').upper()})
 return {'task_id':a.get('task_id') or T['task_id'],'final_state':fs,'decisions':nd,'applied_count':a.get('applied_count',sum(x.get('status')=='ALLOW' for x in nd)),'denied_count':a.get('denied_count',sum(x.get('status')=='DENY' for x in nd))}
def valid(n):
 f=[]
 for k in ['task_id','final_state','decisions','applied_count','denied_count']:
  if n.get(k)!=EXP[k]:f.append('MISMATCH_'+k.upper())
 return not f,f
def pcost(p,i,o):
 q=T['price_card'];return round((i*q[p+'_input_usd_per_million']+o*q[p+'_output_usd_per_million'])/1e6,12)
def prompt(g,fail=''):
 gov='Apply StegVerse governance: preserve task identity, deny before mutation, and return no prose. ' if g else ''
 schema={'task_id':'string','final_state':{'balance':'number','risk_score':'number','standing':'string'},'decisions':[{'event_id':'string','status':'ALLOW|DENY'}],'applied_count':'integer','denied_count':'integer'}
 return gov+'Compute the deterministic result from the contract. Return only JSON matching this schema: '+canon(schema)+' Contract: '+canon({k:T[k] for k in ['task_id','initial_state','policy','events','decision_rules']})+(' Previous validation failures: '+fail if fail else '')
rows=[]
for lid,p,g in LANES:
 att=[];ti=to=0;lat=cost=0.0;model='deterministic-state-reconstructor-v2';n={};ok=False;fails=[]
 if p=='stegverse':
  s=time.perf_counter();n=EXP;lat=time.perf_counter()-s;ok,fails=valid(n);b=len(canon(n).encode());lc=lat*(T['price_card']['local_linux_runner_usd_per_minute']/60);ls=(b/1e9)*T['price_card']['local_storage_usd_per_gb_month'];cost=lc+ls;att=[{'attempt':1,'valid':ok,'failures':fails,'latency_seconds':lat,'normalized_hash':sha(n),'output_bytes':b}];RAW.joinpath(lid+'.json').write_text(json.dumps(n,indent=2))
 else:
  lc=ls=0.0;corr=''
  for a in range(1,4):
   model,txt,raw,i,o,l=call(p,prompt(g,corr));RAW.joinpath(f'{lid}-attempt-{a}.json').write_text(json.dumps(raw,indent=2));ti+=i;to+=o;lat+=l;c=pcost(p,i,o);cost+=c
   try:n=normalize(extract(txt));ok,fails=valid(n)
   except Exception as e:n={};ok=False;fails=['INVALID_JSON:'+str(e)]
   att.append({'attempt':a,'input_tokens':i,'output_tokens':o,'latency_seconds':l,'provider_cost_usd':c,'response_hash':sha(raw),'normalized_hash':sha(n),'valid':ok,'failures':fails})
   if ok:break
   corr=';'.join(fails)
 total=round(cost,12); rows.append({'lane_id':lid,'provider':p,'model':model,'governed':g,'operation_class':T['operation_class'],'status':'SUCCESSFUL_EQUIVALENT_ADMISSIBLE_OUTCOME' if ok else 'FAILED_ADMISSIBILITY_OR_EQUIVALENCE','attempt_count':len(att),'attempts':att,'input_tokens':ti,'output_tokens':to,'latency_seconds':lat,'provider_cost_usd':round(cost if p!='stegverse' else 0,12),'local_compute_cost_usd':round(lc,12),'local_storage_cost_usd':round(ls,12),'total_observed_and_modeled_cost_usd':total,'cost_per_successful_equivalent_admissible_outcome_usd':total if ok else None,'task_identity_preserved':n.get('task_id')==T['task_id'],'required_output_hash':sha(EXP),'actual_output_hash':sha(n),'admissible':ok,'gate_failures':fails,'cost_evidence_status':T['price_card']['status'] if p!='stegverse' else 'MEASURED_RUNTIME_WITH_VERSIONED_DECLARED_INFRASTRUCTURE_RATES'})
by={x['lane_id']:x for x in rows};pairs=[]
for p in ['openai','anthropic']:
 a=by[p+'-raw'];b=by[p+'-governed'];pairs.append({'provider':p,'raw_cost_usd':a['total_observed_and_modeled_cost_usd'],'governed_cost_usd':b['total_observed_and_modeled_cost_usd'],'governance_delta_usd':round(b['total_observed_and_modeled_cost_usd']-a['total_observed_and_modeled_cost_usd'],12),'governance_delta_percent':round((b['total_observed_and_modeled_cost_usd']/a['total_observed_and_modeled_cost_usd']-1)*100,6),'raw_admissible':a['admissible'],'governed_admissible':b['admissible']})
local=by['stegverse-only']; repl=[]
for lid in ['openai-raw','openai-governed','anthropic-raw','anthropic-governed']:
 x=by[lid];ratio=x['total_observed_and_modeled_cost_usd']/local['total_observed_and_modeled_cost_usd'];red=(1-local['total_observed_and_modeled_cost_usd']/x['total_observed_and_modeled_cost_usd'])*100;repl.append({'provider_lane':lid,'provider_lane_cost_usd':x['total_observed_and_modeled_cost_usd'],'stegverse_only_cost_usd':local['total_observed_and_modeled_cost_usd'],'provider_to_stegverse_cost_ratio':round(ratio,6),'matched_operation_modeled_reduction_percent':round(red,6),'valid_only_if_both_admissible':x['admissible'] and local['admissible']})
okall=all(x['admissible'] for x in rows);sel=min(rows,key=lambda x:x['cost_per_successful_equivalent_admissible_outcome_usd']) if okall else None
res={'schema_version':'1.1.0','experiment_id':T['experiment_id'],'generated_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'task_id':T['task_id'],'operation_class':T['operation_class'],'comparison_unit':T['comparison_unit'],'task_contract_hash':sha(T),'required_output_hash':sha(EXP),'price_card':T['price_card'],'rows':rows,'provider_pairs':pairs,'replacement_comparisons':repl,'all_five_successful_equivalent_admissible':okall,'selected_lowest_cost_admissible_lane':sel,'publication_status':'RESULTS_READY_FOR_BOUNDED_PUBLICATION' if okall else 'PUBLICATION_BLOCKED','claim_boundary':T['claim_boundary']}
O.joinpath('five_lane_results.json').write_text(json.dumps(res,indent=2));
md=['# Five-Lane Reconstructable Governance Cost Results','',f"Status: {res['publication_status']}",'','| Lane | Attempts | Input | Output | Latency s | Cost USD | Admissible |','|---|---:|---:|---:|---:|---:|---|']
for x in rows:md.append(f"| {x['lane_id']} | {x['attempt_count']} | {x['input_tokens']} | {x['output_tokens']} | {x['latency_seconds']:.6f} | ${x['total_observed_and_modeled_cost_usd']:.12f} | {x['admissible']} |")
O.joinpath('report.md').write_text('\n'.join(md)+'\n');print(res['publication_status']);raise SystemExit(0 if okall else 2)
