## #!/usr/bin/env python3
“””
chf_validator_merge_patch.py

This file documents all changes needed to chf_deterministic_validator.py
to complete Sprint A + Sprint B integration.

DO NOT add this file to the repo as-is.
Apply each section to chf_deterministic_validator.py directly.

Changes required:

1. Add new outcome constants (from chf_evaluators_sprint_a.py)
1. Add 7 evaluator functions (from chf_evaluators_sprint_a.py)
1. Replace EVALUATORS entries for chf-051 through chf-110
- chf-051 through chf-055: already standard_binary_gate, keep as-is
- chf-056: replace with evaluate_chf_056
- chf-057 through chf-058: already standard_binary_gate, keep as-is
- chf-059: replace with evaluate_chf_059
- chf-060 through chf-078: already standard_binary_gate, keep as-is
- chf-079: replace with evaluate_chf_079
- chf-080 through chf-083: already standard_binary_gate, keep as-is
- chf-084: replace with evaluate_chf_084
- chf-085 through chf-086: already standard_binary_gate, keep as-is
- chf-087: replace with evaluate_chf_087
- chf-088 through chf-093: already standard_binary_gate, keep as-is
- chf-094: replace with evaluate_chf_094
- chf-095 through chf-099: already standard_binary_gate, keep as-is
- chf-100: replace with evaluate_chf_100
  “””

# ===========================================================================

# SECTION 1: EVALUATORS dict replacement block

# Replace the existing chf-051 through chf-110 entries in EVALUATORS with:

# ===========================================================================

EVALUATORS_REPLACEMENT = “””
# — chf-051 through chf-060 —
“chf-051”: evaluate_standard_binary_gate,
“chf-052”: evaluate_standard_binary_gate,
“chf-053”: evaluate_standard_binary_gate,
“chf-054”: evaluate_standard_binary_gate,
“chf-055”: evaluate_standard_binary_gate,
“chf-056”: evaluate_chf_056,
“chf-057”: evaluate_standard_binary_gate,
“chf-058”: evaluate_standard_binary_gate,
“chf-059”: evaluate_chf_059,
“chf-060”: evaluate_standard_binary_gate,

```
# --- chf-061 through chf-070 ---
"chf-061": evaluate_standard_binary_gate,
"chf-062": evaluate_standard_binary_gate,
"chf-063": evaluate_standard_binary_gate,
"chf-064": evaluate_standard_binary_gate,
"chf-065": evaluate_standard_binary_gate,
"chf-066": evaluate_standard_binary_gate,
"chf-067": evaluate_standard_binary_gate,
"chf-068": evaluate_standard_binary_gate,
"chf-069": evaluate_standard_binary_gate,
"chf-070": evaluate_standard_binary_gate,

# --- chf-071 through chf-080 ---
"chf-071": evaluate_standard_binary_gate,
"chf-072": evaluate_standard_binary_gate,
"chf-073": evaluate_standard_binary_gate,
"chf-074": evaluate_standard_binary_gate,
"chf-075": evaluate_standard_binary_gate,
"chf-076": evaluate_standard_binary_gate,
"chf-077": evaluate_standard_binary_gate,
"chf-078": evaluate_standard_binary_gate,
"chf-079": evaluate_chf_079,
"chf-080": evaluate_standard_binary_gate,

# --- chf-081 through chf-090 ---
"chf-081": evaluate_standard_binary_gate,
"chf-082": evaluate_standard_binary_gate,
"chf-083": evaluate_standard_binary_gate,
"chf-084": evaluate_chf_084,
"chf-085": evaluate_standard_binary_gate,
"chf-086": evaluate_standard_binary_gate,
"chf-087": evaluate_chf_087,
"chf-088": evaluate_standard_binary_gate,
"chf-089": evaluate_standard_binary_gate,
"chf-090": evaluate_standard_binary_gate,

# --- chf-091 through chf-100 ---
"chf-091": evaluate_standard_binary_gate,
"chf-092": evaluate_standard_binary_gate,
"chf-093": evaluate_standard_binary_gate,
"chf-094": evaluate_chf_094,
"chf-095": evaluate_standard_binary_gate,
"chf-096": evaluate_standard_binary_gate,
"chf-097": evaluate_standard_binary_gate,
"chf-098": evaluate_standard_binary_gate,
"chf-099": evaluate_standard_binary_gate,
"chf-100": evaluate_chf_100,

# --- chf-101 through chf-110 (scaffold, unchanged) ---
"chf-101": evaluate_standard_binary_gate,
"chf-102": evaluate_standard_binary_gate,
"chf-103": evaluate_standard_binary_gate,
"chf-104": evaluate_standard_binary_gate,
"chf-105": evaluate_standard_binary_gate,
"chf-106": evaluate_standard_binary_gate,
"chf-107": evaluate_standard_binary_gate,
"chf-108": evaluate_standard_binary_gate,
"chf-109": evaluate_standard_binary_gate,
"chf-110": evaluate_standard_binary_gate,
```

“””

# ===========================================================================

# SECTION 2: problem_spec file placement

# Each of the 50 YAML files must be named exactly as follows and placed

# in math_solver/validation/:

# ===========================================================================

SPEC_FILE_NAMES = [
# From problem_spec_chf_051_060.yml — split into individual files:
“problem_spec_chf_051.yml”,
“problem_spec_chf_052.yml”,
“problem_spec_chf_053.yml”,
“problem_spec_chf_054.yml”,
“problem_spec_chf_055.yml”,
“problem_spec_chf_056.yml”,
“problem_spec_chf_057.yml”,
“problem_spec_chf_058.yml”,
“problem_spec_chf_059.yml”,
“problem_spec_chf_060.yml”,

```
# From problem_spec_chf_061_070.yml:
"problem_spec_chf_061.yml",
"problem_spec_chf_062.yml",
"problem_spec_chf_063.yml",
"problem_spec_chf_064.yml",
"problem_spec_chf_065.yml",
"problem_spec_chf_066.yml",
"problem_spec_chf_067.yml",
"problem_spec_chf_068.yml",
"problem_spec_chf_069.yml",
"problem_spec_chf_070.yml",

# From problem_spec_chf_071_080.yml:
"problem_spec_chf_071.yml",
"problem_spec_chf_072.yml",
"problem_spec_chf_073.yml",
"problem_spec_chf_074.yml",
"problem_spec_chf_075.yml",
"problem_spec_chf_076.yml",
"problem_spec_chf_077.yml",
"problem_spec_chf_078.yml",
"problem_spec_chf_079.yml",
"problem_spec_chf_080.yml",

# From problem_spec_chf_081_090.yml:
"problem_spec_chf_081.yml",
"problem_spec_chf_082.yml",
"problem_spec_chf_083.yml",
"problem_spec_chf_084.yml",
"problem_spec_chf_085.yml",
"problem_spec_chf_086.yml",
"problem_spec_chf_087.yml",
"problem_spec_chf_088.yml",
"problem_spec_chf_089.yml",
"problem_spec_chf_090.yml",

# From problem_spec_chf_091_100.yml:
"problem_spec_chf_091.yml",
"problem_spec_chf_092.yml",
"problem_spec_chf_093.yml",
"problem_spec_chf_094.yml",
"problem_spec_chf_095.yml",
"problem_spec_chf_096.yml",
"problem_spec_chf_097.yml",
"problem_spec_chf_098.yml",
"problem_spec_chf_099.yml",
"problem_spec_chf_100.yml",
```

]

# ===========================================================================

# SECTION 3: Note on multi-spec YAML files

# 

# The 4 batch files delivered contain multiple specs separated by —

# The validator’s load_specs() uses glob(“problem_spec_chf_*.yml”) and

# yaml.safe_load() which reads only the FIRST document in a multi-doc YAML.

# 

# Each spec MUST be split into its own individual file before committing.

# The batch files are for delivery convenience only.

# 

# Quick split command (run from math_solver/validation/):

# 

# python - <<‘EOF’

# import yaml, pathlib

# for batch in [‘051_060’,‘061_070’,‘071_080’,‘081_090’,‘091_100’]:

# text = pathlib.Path(f’problem_spec_chf_{batch}.yml’).read_text()

# for doc in yaml.safe_load_all(text):

# if doc:

# pid = doc[‘problem_id’].replace(’-’,’_’)

# pathlib.Path(f’problem_spec_{pid}.yml’).write_text(

# yaml.dump(doc, default_flow_style=False, sort_keys=False)

# )

# print(‘Split complete’)

# EOF

# 

# ===========================================================================

# ===========================================================================

# SECTION 4: Local preflight sequence

# 

# cd math_solver/validation

# 

# # 1. Split batch YAML files into individual spec files

# python chf_validator_merge_patch.py –split

# 

# # 2. Run sandbox standalone check

# python chf_sandbox_runner.py

# # Expected: 17 suites, ~4963 subtests, 0 failures

# 

# # 3. Run full deterministic validation

# python chf_deterministic_validator.py \

# –spec-dir . \

# –out-json brain_reports/chf_report.json \

# –out-md   brain_reports/chf_report.md

# # Expected: 160 specs evaluated (110 existing + 50 new), overall PASS

# 

# # 4. Emit Publisher status

# python chf_emit_status.py \

# –report brain_reports/chf_report.json \

# –out    brain_reports/chf_status.json

# 

# # 5. Push and dispatch chf_validation_run.yml

# # Expected: run #21+, PASS, specs_evaluated: 160

# ===========================================================================

import sys
import pathlib
import yaml as _yaml

def split_batch_files():
“”“Split the 4 delivered batch YAML files into individual spec files.”””
batches = [“051_060”, “061_070”, “071_080”, “081_090”, “091_100”]
split_count = 0
for batch in batches:
batch_path = pathlib.Path(f”problem_spec_chf_{batch}.yml”)
if not batch_path.exists():
print(f”  SKIP (not found): {batch_path}”)
continue
text = batch_path.read_text(encoding=“utf-8”)
for doc in *yaml.safe_load_all(text):
if doc and “problem_id” in doc:
pid = doc[“problem_id”].replace(”-”, “*”)
out_path = pathlib.Path(f”problem_spec_{pid}.yml”)
out_path.write_text(
_yaml.dump(doc, default_flow_style=False, sort_keys=False),
encoding=“utf-8”,
)
print(f”  WROTE: {out_path}”)
split_count += 1
print(f”\nSplit complete: {split_count} spec files written.”)

if **name** == “**main**”:
if “–split” in sys.argv:
split_batch_files()
else:
print(“Usage: python chf_validator_merge_patch.py –split”)
print(“Run from math_solver/validation/ after copying batch YAML files there.”)
