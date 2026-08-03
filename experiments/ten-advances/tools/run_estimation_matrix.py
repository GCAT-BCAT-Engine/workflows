#!/usr/bin/env python3
import hashlib, json, os, pathlib, re, sys, time, urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'results'; RAW=OUT/'raw'; OUT.mkdir(exist_ok=True); RAW.mkdir(exist_ok=True)
problems=json.loads((ROOT/'problems.json').read_text())['problems']
lanes=json.loads((ROOT/'config/lanes.json').read_text())['lanes']
prompt=(ROOT/'prompts/provider-estimate.md').read_text()

def post(url, headers, body):
    req=urllib.request.Request(url,data=json.dumps(body).encode(),headers=headers,method='POST')
    with urllib.request.urlopen(req,timeout=240) as r: return json.loads(r.read())

def extract_json(text):
    text=text.strip(); text=re.sub(r'^```(?:json)?\s*|\s*```$','',text,flags=re.S)
    a=text.find('{'); b=text.rfind('}')
    if a<0 or b<a: raise ValueError('no JSON object in response')
    return json.loads(text[a:b+1])

def call_openai(text):
    key=os.environ['OPENAI_API_KEY']; model=os.getenv('OPENAI_ESTIMATION_MODEL','gpt-5.6')
    data=post('https://api.openai.com/v1/responses',{'Authorization':'Bearer '+key,'Content-Type':'application/json'},{'model':model,'input':text})
    output=data.get('output_text')
    if not output:
        output=''.join(c.get('text','') for i in data.get('output',[]) for c in i.get('content',[]) if c.get('type')=='output_text')
    return model, output, data

def call_anthropic(text):
    key=os.environ['ANTHROPIC_API_KEY']; model=os.getenv('ANTHROPIC_ESTIMATION_MODEL','claude-sonnet-4-6')
    data=post('https://api.anthropic.com/v1/messages',{'x-api-key':key,'anthropic-version':'2023-06-01','content-type':'application/json'},{'model':model,'max_tokens':5000,'messages':[{'role':'user','content':text}]})
    output=''.join(x.get('text','') for x in data.get('content',[]) if x.get('type')=='text')
    return model, output, data

def local_estimate(problem,lane):
    blockers=['No provider inference allowed','Domain-specific theorem prover/tool inventory not yet proven complete']
    return {'problem_id':problem['problem_id'],'lane_id':lane['lane_id'],'provider':'stegverse','model_or_runtime':'installed-sandbox-inventory','execution_posture':'stegverse_only','estimated_input_tokens':0,'estimated_output_tokens':0,'estimated_reasoning_tokens':0,'estimated_candidate_branches':0,'estimated_failed_branches':0,'estimated_retries':0,'estimated_search_cost':0,'estimated_governance_overhead':0,'estimated_verification_cost':0,'estimated_total_cost_low':0,'estimated_total_cost_central':0,'estimated_total_cost_high':0,'estimated_elapsed_hours_low':0,'estimated_elapsed_hours_central':0,'estimated_elapsed_hours_high':0,'estimated_success_probability':0,'estimated_reproduction_probability':0,'estimated_independent_result_probability':0,'confidence':0.25,'assumptions':['Estimate remains blocked until installed capability inventory is validated'],'uncertainty_drivers':['Unknown local symbolic and formalization capacity'],'minimum_evidence':['Provider-deny network receipt','Tool inventory','Bounded subproblem','Independent checker'],'blockers':blockers}

records=[]; failures=[]
for p in problems:
  for lane in lanes:
    base=f"{prompt}\n\nproblem_id: {p['problem_id']}\nlane_id: {lane['lane_id']}\nprovider: {lane['provider']}\nexecution_posture: {'governed' if lane['governed'] else 'non_governed'}\nproblem: {p['title']}\nstatement: {p['statement']}\n"
    try:
      if lane['provider']=='stegverse': rec=local_estimate(p,lane); raw={'local':True}
      elif lane['provider']=='openai': model,text,raw=call_openai(base); rec=extract_json(text)
      else: model,text,raw=call_anthropic(base); rec=extract_json(text)
      rec.update({'problem_id':p['problem_id'],'lane_id':lane['lane_id'],'provider':lane['provider'],'execution_posture':'stegverse_only' if lane['provider']=='stegverse' else ('governed' if lane['governed'] else 'non_governed')})
      raw_bytes=json.dumps(raw,sort_keys=True).encode(); rec['receipt_hash']='sha256:'+hashlib.sha256(raw_bytes).hexdigest()
      (RAW/f"{p['problem_id']}-{lane['lane_id']}.json").write_text(json.dumps(raw,indent=2))
      records.append(rec)
    except Exception as e: failures.append({'problem_id':p['problem_id'],'lane_id':lane['lane_id'],'error':str(e)})
    time.sleep(1)
(OUT/'estimates.json').write_text(json.dumps(records,indent=2))
(OUT/'failures.json').write_text(json.dumps(failures,indent=2))
print(json.dumps({'records':len(records),'expected':50,'failures':len(failures)}))
sys.exit(0 if len(records)==50 else 2)
