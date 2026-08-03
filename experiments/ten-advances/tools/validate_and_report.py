#!/usr/bin/env python3
import json, pathlib, statistics, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]; result=ROOT/'results/estimates.json'; report=ROOT.parents[1]/'reports/ten-advances-estimation-summary.md'
records=json.loads(result.read_text()) if result.exists() else []
keys={(r.get('problem_id'),r.get('lane_id')) for r in records}; expected={(f'TA-{i:03d}',l) for i in range(1,11) for l in ['openai-raw','openai-governed','anthropic-raw','anthropic-governed','stegverse-only']}
errors=[]
if keys!=expected: errors.append(f'missing_or_extra={sorted(expected-keys)}')
for r in records:
  for k in ['estimated_total_cost_low','estimated_total_cost_central','estimated_total_cost_high','estimated_success_probability','confidence','assumptions','uncertainty_drivers','minimum_evidence','receipt_hash']:
    if k not in r: errors.append(f"{r.get('problem_id')}/{r.get('lane_id')} missing {k}")
  if all(k in r for k in ['estimated_total_cost_low','estimated_total_cost_central','estimated_total_cost_high']) and not (r['estimated_total_cost_low']<=r['estimated_total_cost_central']<=r['estimated_total_cost_high']): errors.append(f"{r['problem_id']}/{r['lane_id']} invalid cost interval")
lines=['# Ten Advances Cost and Feasibility Estimation','',f'Status: {"VALID" if not errors else "INCOMPLETE"}',f'Records: {len(records)}/50','', '## Lane totals','', '| Lane | Low | Central | High | Mean success probability |','|---|---:|---:|---:|---:|']
for lane in ['openai-raw','openai-governed','anthropic-raw','anthropic-governed','stegverse-only']:
  rs=[r for r in records if r.get('lane_id')==lane]
  if rs: lines.append(f"| {lane} | ${sum(r['estimated_total_cost_low'] for r in rs):,.2f} | ${sum(r['estimated_total_cost_central'] for r in rs):,.2f} | ${sum(r['estimated_total_cost_high'] for r in rs):,.2f} | {statistics.mean(r['estimated_success_probability'] for r in rs):.3f} |")
lines += ['', '## Per-problem central estimates','', '| Problem | OpenAI raw | OpenAI governed | Anthropic raw | Anthropic governed | StegVerse-only |','|---|---:|---:|---:|---:|---:|']
for i in range(1,11):
 p=f'TA-{i:03d}'; vals={r['lane_id']:r['estimated_total_cost_central'] for r in records if r['problem_id']==p}; lines.append('| '+p+' | '+' | '.join(f"${vals.get(l,0):,.2f}" for l in ['openai-raw','openai-governed','anthropic-raw','anthropic-governed','stegverse-only'])+' |')
lines += ['', '## Validation findings',''] + (['- All required records and intervals validated.'] if not errors else [f'- {e}' for e in errors])
report.parent.mkdir(exist_ok=True); report.write_text('\n'.join(lines)+'\n')
print(json.dumps({'valid':not errors,'errors':errors,'report':str(report)})); sys.exit(0 if not errors else 2)
