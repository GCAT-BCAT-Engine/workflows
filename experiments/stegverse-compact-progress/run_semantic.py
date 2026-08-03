#!/usr/bin/env python3
import pathlib
import re

root = pathlib.Path(__file__).parent
source = (root / "run.py").read_text()
replacement = '''def validate(stage_id, text):
    from semantic_validation import validate as semantic_validate
    return semantic_validate(stage_id, text)


def compact_excerpt'''
patched, count = re.subn(
    r"def validate\(stage_id, text\):.*?\n\ndef compact_excerpt",
    replacement,
    source,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f"expected one validator replacement, got {count}")
exec(compile(patched, str(root / "run.py"), "exec"), {"__name__": "__main__", "__file__": str(root / "run.py")})
