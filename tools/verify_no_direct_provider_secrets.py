#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

SECRET_EXPR=re.compile(r"\$\{\{\s*secrets\.[A-Za-z0-9_]+\s*\}\}")
PROVIDER_NAMES=("OPENAI","ANTHROPIC","DEEPSEEK","MOONSHOT","KIMI","ZAI")
PROVIDER_KEY_NAME=r"(?:"+"|".join(PROVIDER_NAMES)+r")_(?:API_)?KEY"
PROVIDER_ASSIGN=re.compile(r"^\\s*"+PROVIDER_KEY_NAME+r"\\s*[:=]")
PROVIDER_SHELL_REF=re.compile(r"\\$(?:\\{)?"+PROVIDER_KEY_NAME+r"(?:\\})?")


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
            stripped=line.strip()
            if stripped.startswith("#"):
                continue
            if PROVIDER_ASSIGN.search(line) or PROVIDER_SHELL_REF.search(line):
                out.append(f"{rel}:{lineno}:provider credential reference in active workflow")
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
