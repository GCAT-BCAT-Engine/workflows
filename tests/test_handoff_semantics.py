from __future__ import annotations
import json, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from handoff_authority import git_blob_sha1
from handoff_semantics import conformance,evaluate,fingerprint,parse,reconciliation,state,table

HANDOFF='''# Example

## Source of truth
Declared by `.handoff/current.json`.

## Role
Example role.

## Current installed files
```text
README.md
.github/workflows/check.yml
```

## Current working path
```text
input -> verify -> output
```

## Done state for this repo
1. Verify state.

## Completed in latest pass
```text
README.md
```

## Remaining work
```text
Finish the next governed task.
```

## Destination installs
```text
example/downstream — PENDING
```

## Next task
Run the read-only verifier.
'''

def repo(root:Path,handoff:str=HANDOFF)->None:
    (root/'docs').mkdir(parents=True); (root/'.handoff').mkdir(); (root/'.github/workflows').mkdir(parents=True); (root/'config').mkdir()
    (root/'README.md').write_text('ok\n'); (root/'.github/workflows/check.yml').write_text('name: check\n')
    hp=root/'docs/EXAMPLE_MIRROR_HANDOFF.md'; hp.write_text(handoff)
    manifest={'schema':'stegverse.handoff.authority.v1','repository':'example/repo','current_handoff':{'path':'docs/EXAMPLE_MIRROR_HANDOFF.md','hash_algorithm':'git-blob-sha1','hash':git_blob_sha1(hp.read_bytes())},'document_profile':'format_a_v1','scoped_handoffs':[],'archive_policy':{'date_suffix_required':True,'session_archive_prefix_allowed':True},'declared_at':'2026-08-04T23:00:00Z'}
    (root/'.handoff/current.json').write_text(json.dumps(manifest))
    (root/'config/handoff-field-authority.format-a-v1.json').write_text((ROOT/'config/handoff-field-authority.format-a-v1.json').read_text())

class Tests(unittest.TestCase):
    def test_parser(self):
        sections,counts,_=parse(HANDOFF); self.assertEqual(9,sum(x==1 for x in counts.values())); self.assertIn('README.md',sections['current_installed_files'])
    def test_missing_section(self):
        authority=json.loads((ROOT/'config/handoff-field-authority.format-a-v1.json').read_text())
        r=conformance('example/repo','docs/x.md',HANDOFF.replace('## Next task','## Later task'),authority)
        self.assertEqual('FAIL_CLOSED',r['terminal_decision'])
    def test_display_transform(self):
        authority=json.loads((ROOT/'config/handoff-field-authority.format-a-v1.json').read_text())
        text=HANDOFF.replace('.github/workflows/check.yml','github/workflows/check.yml\n```\n\nNote: displayed without the leading dot.\n\n```text')
        r=conformance('example/repo','docs/x.md',text,authority); self.assertIn('DISPLAY_TRANSFORM_EMBEDDED_IN_STORED_DATA',{d['code'] for d in r['deltas']})
    def test_missing_file_denies(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); repo(root,HANDOFF.replace('README.md\n.github','MISSING.md\n.github')); r=evaluate(root,'example/repo'); self.assertEqual('DENY',r['terminal_decision'])
    def test_leading_dot_suggestion(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); repo(root); authority=table(root); text=HANDOFF.replace('.github/workflows/check.yml','github/workflows/check.yml'); c=conformance('example/repo','x',text,authority); r=state(root,'example/repo','x',text,authority,c); delta=next(x for x in r['deltas'] if x['claim'].startswith('github/')); self.assertEqual('.github/workflows/check.yml',delta['suggested_path'])
    def test_next_task_not_reconciled(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); repo(root,HANDOFF.replace('Run the read-only verifier.','missing/not-built.py')); self.assertEqual('ALLOW',evaluate(root,'example/repo')['terminal_decision'])
    def test_authority_blocks(self):
        with tempfile.TemporaryDirectory() as d: self.assertEqual('FAIL_CLOSED',evaluate(Path(d),'example/repo')['terminal_decision'])
    def test_fixed_point(self):
        empty={'receipt_type':'x','terminal_decision':'ALLOW','delta_count':0,'deltas':[]}; r=reconciliation('example/repo',1,3,empty,empty); self.assertEqual('FIXED_POINT_REACHED',r['status'])
    def test_max_passes(self):
        delta={'receipt_type':'x','terminal_decision':'DENY','delta_count':1,'deltas':[{'field':'current_installed_files','code':'CLAIMED_PATH_MISSING'}]}; self.assertEqual('FAIL_CLOSED',reconciliation('example/repo',3,3,delta,delta)['terminal_decision'])
    def test_oscillation(self):
        delta={'receipt_type':'x','terminal_decision':'DENY','delta_count':1,'deltas':[{'field':'current_installed_files','code':'CLAIMED_PATH_MISSING'}]}; fp=fingerprint(delta,delta); self.assertEqual('OSCILLATION_DETECTED',reconciliation('example/repo',2,4,delta,delta,[fp,'other',fp])['status'])
    def test_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); repo(root); self.assertEqual(evaluate(root,'example/repo')['receipt_hash'],evaluate(root,'example/repo')['receipt_hash'])
if __name__=='__main__': unittest.main()
