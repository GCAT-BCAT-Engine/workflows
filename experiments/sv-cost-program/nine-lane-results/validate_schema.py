#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT=pathlib.Path(__file__).parent
T=json.loads((ROOT/'task.json').read_text())
EXPECTED=[
(1,'openai-raw','OpenAI',False,'EXTERNAL'),(2,'openai-governed','OpenAI/StegVerse',True,'EXTERNAL'),
(3,'anthropic-raw','Anthropic',False,'EXTERNAL'),(4,'anthropic-governed','Anthropic/StegVerse',True,'EXTERNAL'),
(5,'stegverse-only','StegVerse deterministic reconstruction',True,'NONE'),
(6,'deepseek-raw','DeepSeek',False,'EXTERNAL'),(7,'deepseek-governed','DeepSeek/StegVerse',True,'EXTERNAL'),
(8,'kimi-raw','Kimi (Moonshot AI)',False,'EXTERNAL'),(9,'kimi-governed','Kimi (Moonshot AI)/StegVerse',True,'EXTERNAL')]
f=[]
if T.get('schema_version')!='4.0.0': f.append('SCHEMA_VERSION')
if T.get('credential_invariant')!='NO_PROVIDER_API_KEY_POSSESSED_OR_CONSUMED_BY_STEGVERSE_TEST_WORKLOAD': f.append('CREDENTIAL_INVARIANT')
lanes=T.get('lane_schema',[])
if len(lanes)!=9:f.append(f'EXPECTED_9_LANES_GOT_{len(lanes)}')
for i,e in enumerate(EXPECTED):
    if i>=len(lanes): continue
    a=lanes[i]; actual=(a.get('lane'),a.get('lane_id'),a.get('model_interest'),a.get('stegverse_governed'),a.get('credential_mode'))
    if actual!=e:f.append(f'LANE_{e[0]}_MISMATCH:{actual!r}')
files=T.get('candidate_source_contract',{}).get('required_candidate_files',[])
for p in ('openai','anthropic','deepseek','kimi'):
    if f'candidate-inputs/{p}.json' not in files:f.append('MISSING_CANDIDATE_FILE:'+p)
runner=(ROOT/'run_candidate_outputs.py').read_text()
for marker in ('PROVIDERS = ("openai", "anthropic", "deepseek", "kimi")','all_nine_present','provider credential transfer is forbidden'):
    if marker not in runner:f.append('RUNNER_MARKER:'+marker)
for forbidden in ('OPENAI_API_KEY','ANTHROPIC_API_KEY','DEEPSEEK_API_KEY','MOONSHOT_API_KEY','KIMI_API_KEY','api.openai.com','api.anthropic.com','api.deepseek.com'):
    if forbidden in runner:f.append('FORBIDDEN_PROVIDER_PATH:'+forbidden)
if f:
    print(json.dumps({'status':'FAIL','failures':f},indent=2));sys.exit(2)
print(json.dumps({'status':'PASS','experiment_id':T['experiment_id'],'lane_count':9,'new_lanes':['kimi-raw','kimi-governed'],'historical_seven_lane_preserved':True},indent=2))
