#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

SECRET_EXPR=re.compile(r"\$\{\{\s*secrets\.[A-Za-z0-9_]+\s*\}\}")
PROVIDER_NAMES=("OPENAI","ANTHROPIC","DEEPSEEK","MOONSHOT","KIMI","ZAI")
PROVIDER_ENV=re.compile(r"\b("+ "|".join(PROVIDER_NAMES) +r")_(?:API_)?KEY\b")
SAFE_NEGATION_HINTS=("grep -E", "assert marker not in", "forbidden =", "for marker in forbidden")


def violations(root: Path) -> list[str]:
    out=[]
    wf=root/".github"/"workflows"
    for path in sorted(wf.glob("*.y*ml")):
        text=path.read_text(encoding="utf-8")
        rel=path.relative_to(root).as_posix()
        for lineno,line in enumerate(text.splitlines(),1):
            if SECRET_EXPR.search(line):
                out.append(f"{rel}:{lineno}:direct GitHub secret interpolation")
                continue
            if PROVIDER_ENV.search(line):
                stripped=line.strip()
                if any(hint in stripped for hint in SAFE_NEGATION_HINTS):
                    continue
                # Marker-only negative validation tuples are allowed when the same line
                # explicitly asserts absence rather than exporting/reading a value.
                if "assert" in stripped and "not in" in stripped:
                    continue
                if stripped.startswith("#"):
                    continue
                out.append(f"{rel}:{lineno}:provider credential name in active workflow")
    return out


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=Path,default=Path("."))
    ns=ap.parse_args()
    bad=violations(ns.root.resolve())
    if bad:
        print("PROVIDER_SECRET_BOUNDARY=DENY")
        for item in bad: print(item)
        return 1
    print("PROVIDER_SECRET_BOUNDARY=ALLOW")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
