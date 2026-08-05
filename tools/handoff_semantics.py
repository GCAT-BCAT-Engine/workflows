#!/usr/bin/env python3
"""Read-only Format A conformance, state-delta, and convergence verifier."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from typing import Any, Iterable
try:
    from handoff_authority import canonical_json, verify_repository
except ImportError:
    from runtime.orchestrator.handoff_authority import canonical_json, verify_repository

HEADINGS=(
("source_of_truth","Source of truth"),("role","Role"),
("current_installed_files","Current installed files"),
("current_working_path","Current working path"),
("done_state_for_this_repo","Done state for this repo"),
("completed_in_latest_pass","Completed in latest pass"),
("remaining_work","Remaining work"),
("destination_installs","Destination installs"),("next_task","Next task"))
H2F={h:f for f,h in HEADINGS}
TABLE=Path("config/handoff-field-authority.format-a-v1.json")
FENCE=re.compile(r"^```(?:[\w.+-]+)?\s*$")
PATH=re.compile(r"^(?:[\w.-]+/)+[\w.@+ -]+/?$")
FILE=re.compile(r"^[\w.-]+\.[\w.-]+$")
DISPLAY=re.compile(r"(?:displayed|shown).{0,80}(?:without|omit(?:ted|s)?).{0,40}(?:leading\s+)?(?:dot|period)",re.I|re.S)

class SemanticError(RuntimeError): pass

def stable(payload:Any)->str:
    return hashlib.sha256(canonical_json(payload)).hexdigest()

def load(path:Path)->dict[str,Any]:
    try: value=json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e: raise SemanticError(f"missing_file:{path.as_posix()}") from e
    except (OSError,UnicodeError,json.JSONDecodeError) as e: raise SemanticError(f"invalid_json:{path.as_posix()}:{type(e).__name__}") from e
    if not isinstance(value,dict): raise SemanticError(f"json_object_required:{path.as_posix()}")
    return value

def parse(text:str)->tuple[dict[str,str],dict[str,int],list[str]]:
    parts={f:[] for f,_ in HEADINGS}; counts={f:0 for f,_ in HEADINGS}; unknown=[]; active=None
    for line in text.splitlines():
        m=re.match(r"^#{1,6}\s+(.+?)\s*$",line)
        if m:
            active=H2F.get(m.group(1).strip())
            if active: counts[active]+=1
            else: unknown.append(m.group(1).strip())
        elif active: parts[active].append(line)
    return {k:"\n".join(v).strip() for k,v in parts.items()},counts,unknown

def lines(section:str)->list[str]:
    out=[]; fenced=False
    for raw in section.splitlines():
        s=raw.strip()
        if FENCE.fullmatch(s): fenced=not fenced; continue
        if not s or s.startswith("<!--"): continue
        if fenced: out.append(s); continue
        m=re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)(.+)$",s)
        if m: out.append(m.group(1).strip())
    return out

def claims(section:str)->list[str]:
    out=[]
    for raw in lines(section):
        value=re.sub(r"\s+#.*$","",raw.strip().strip("`")).strip().rstrip("/")
        if not value or value in {"...","…"} or "…" in value or value.endswith(":") or " = " in value: continue
        if PATH.fullmatch(value) or FILE.fullmatch(value): out.append(value)
    return out

def table(root:Path,override:Path|None=None)->dict[str,Any]:
    value=load(override or root/TABLE)
    expected={f for f,_ in HEADINGS}
    if value.get("schema")!="stegverse.handoff.field_authority.v1": raise SemanticError("field_authority_schema_invalid")
    if value.get("document_profile")!="format_a_v1": raise SemanticError("field_authority_profile_invalid")
    if not isinstance(value.get("fields"),dict) or set(value["fields"])!=expected: raise SemanticError("field_authority_field_set_mismatch")
    return value

def finish(payload:dict[str,Any])->dict[str,Any]: payload["receipt_hash"]=stable(payload); return payload

def conformance(repository:str,path:str,text:str,authority:dict[str,Any])->dict[str,Any]:
    sections,counts,unknown=parse(text); deltas=[]
    for field,heading in HEADINGS:
        if counts[field]==0: deltas.append({"delta_type":"CONFORMANCE","field":field,"code":"REQUIRED_SECTION_MISSING","expected":heading,"observed":None,"repair_eligible":False})
        elif counts[field]>1: deltas.append({"delta_type":"CONFORMANCE","field":field,"code":"DUPLICATE_SECTION","expected":1,"observed":counts[field],"repair_eligible":False})
    installed=sections["current_installed_files"]
    if counts["current_installed_files"]==1 and not claims(installed):
        deltas.append({"delta_type":"CONFORMANCE","field":"current_installed_files","code":"PATH_LIST_EMPTY_OR_UNPARSEABLE","expected":"canonical repository-relative paths","observed":lines(installed),"repair_eligible":False})
    if DISPLAY.search(installed):
        deltas.append({"delta_type":"CONFORMANCE","field":"current_installed_files","code":"DISPLAY_TRANSFORM_EMBEDDED_IN_STORED_DATA","expected":"stored paths equal repository paths","observed":"leading-dot display transformation note","repair_eligible":False})
    for field in ("current_installed_files","completed_in_latest_pass"):
        for value in claims(sections[field]):
            code=None; p=Path(value)
            if p.is_absolute(): code="ABSOLUTE_PATH_FORBIDDEN"
            elif ".." in p.parts: code="PARENT_TRAVERSAL_FORBIDDEN"
            elif "\\" in value: code="BACKSLASH_PATH_FORBIDDEN"
            elif value.startswith("./"): code="NON_CANONICAL_DOT_PREFIX"
            if code: deltas.append({"delta_type":"CONFORMANCE","field":field,"code":code,"expected":"canonical repository-relative path","observed":value,"repair_eligible":False})
    decision="ALLOW" if not deltas else "FAIL_CLOSED"
    return finish({"receipt_type":"stegverse.handoff_conformance.receipt.v1","repository":repository,"handoff_path":path,"document_profile":"format_a_v1","field_authority_hash":stable(authority),"terminal_decision":decision,"processing_disposition":"NONE" if decision=="ALLOW" else "REVIEW_REQUIRED","conformant":decision=="ALLOW","delta_count":len(deltas),"deltas":deltas,"section_counts":counts,"unknown_headings":unknown})

def state(root:Path,repository:str,path:str,text:str,authority:dict[str,Any],conf:dict[str,Any])->dict[str,Any]:
    if conf["terminal_decision"]!="ALLOW":
        return finish({"receipt_type":"stegverse.handoff_state_delta.receipt.v1","repository":repository,"handoff_path":path,"field_authority_hash":stable(authority),"terminal_decision":"FAIL_CLOSED","processing_disposition":"BLOCKED","state_verified":False,"blocked_by":conf["receipt_hash"],"delta_count":0,"deltas":[]})
    sections,_,_=parse(text); deltas=[]
    for field in ("current_installed_files","completed_in_latest_pass"):
        if authority["fields"][field]["authority_source"] not in {"repository_tree","repository_tree_and_receipts"}: continue
        for value in claims(sections[field]):
            if (root/value).exists(): continue
            suggested="."+value if value.startswith("github/") and (root/("."+value)).exists() else None
            deltas.append({"delta_type":"STATE","field":field,"code":"DISPLAY_PATH_TRANSFORM_DETECTED" if suggested else "CLAIMED_PATH_MISSING","claim":value,"observed":"MISSING","suggested_path":suggested,"authority_source":"repository_tree","repair_eligible":True,"repair_mode":"PROPOSAL_ONLY"})
    decision="ALLOW" if not deltas else "DENY"
    return finish({"receipt_type":"stegverse.handoff_state_delta.receipt.v1","repository":repository,"handoff_path":path,"field_authority_hash":stable(authority),"terminal_decision":decision,"processing_disposition":"NONE" if decision=="ALLOW" else "BLOCKED","state_verified":decision=="ALLOW","delta_count":len(deltas),"deltas":deltas,"checked_fields":["current_installed_files","completed_in_latest_pass"],"read_only":True})

def fingerprint(*receipts:dict[str,Any])->str:
    items=[]
    for receipt in receipts:
        for delta in receipt.get("deltas",[]): items.append({"receipt_type":receipt.get("receipt_type"),"field":delta.get("field"),"code":delta.get("code"),"claim":delta.get("claim")})
    items.sort(key=lambda x:json.dumps(x,sort_keys=True)); return hashlib.sha256(canonical_json(items)).hexdigest()

def reconciliation(repository:str,pass_number:int,max_passes:int,conf:dict[str,Any],st:dict[str,Any],prior:list[str]|None=None)->dict[str,Any]:
    if pass_number<1 or max_passes<1: raise SemanticError("reconciliation_pass_values_invalid")
    prior=list(prior or []); fp=fingerprint(conf,st)
    fixed=conf["terminal_decision"]==st["terminal_decision"]=="ALLOW" and conf["delta_count"]==st["delta_count"]==0
    oscillating=len(prior)>1 and fp in prior[:-1]
    if fixed: decision,disp,status="ALLOW","NONE","FIXED_POINT_REACHED"
    elif pass_number>=max_passes: decision,disp,status="FAIL_CLOSED","BLOCKED","MAX_PASSES_EXCEEDED"
    elif oscillating: decision,disp,status="FAIL_CLOSED","REVIEW_REQUIRED","OSCILLATION_DETECTED"
    else: decision,disp,status="CONDITIONAL","REVIEW_REQUIRED","DELTAS_REMAIN"
    return finish({"receipt_type":"stegverse.handoff_reconciliation.receipt.v1","repository":repository,"pass_number":pass_number,"max_reconciliation_passes":max_passes,"delta_fingerprint":fp,"prior_fingerprints":prior,"fixed_point_reached":fixed,"status":status,"terminal_decision":decision,"processing_disposition":disp,"repair_enabled":False})

def evaluate(root:Path,expected_repository:str|None=None,authority_table:Path|None=None,pass_number:int=1,max_passes:int=3,prior:list[str]|None=None)->dict[str,Any]:
    root=root.resolve(); auth=verify_repository(root,expected_repository=expected_repository); repository=str(auth.get("repository") or expected_repository or "")
    if auth.get("terminal_decision")!="ALLOW": return finish({"receipt_type":"stegverse.handoff_semantic_admission.receipt.v1","repository":repository,"terminal_decision":"FAIL_CLOSED","processing_disposition":"BLOCKED","semantic_evaluated":False,"blocked_by_authority_receipt":auth.get("receipt_hash"),"authority_receipt":auth})
    manifest=load(root/".handoff/current.json")
    if manifest.get("document_profile")!="format_a_v1": return finish({"receipt_type":"stegverse.handoff_semantic_admission.receipt.v1","repository":repository,"terminal_decision":"ALLOW","processing_disposition":"DEFER","semantic_evaluated":False,"reason":"DOCUMENT_PROFILE_NOT_FORMAT_A","authority_receipt":auth})
    authority=table(root,authority_table); path=str(auth["current_handoff_path"])
    try: text=(root/path).read_text(encoding="utf-8")
    except (OSError,UnicodeError) as e: raise SemanticError(f"handoff_unreadable:{type(e).__name__}") from e
    conf=conformance(repository,path,text,authority); st=state(root,repository,path,text,authority,conf); rec=reconciliation(repository,pass_number,max_passes,conf,st,prior)
    decisions={conf["terminal_decision"],st["terminal_decision"]}
    decision="FAIL_CLOSED" if "FAIL_CLOSED" in decisions else "DENY" if "DENY" in decisions else "ALLOW"
    return finish({"receipt_type":"stegverse.handoff_semantic_admission.receipt.v1","repository":repository,"terminal_decision":decision,"processing_disposition":"NONE" if decision=="ALLOW" else "BLOCKED","semantic_evaluated":True,"authority_receipt_hash":auth.get("receipt_hash"),"conformance_receipt":conf,"state_delta_receipt":st,"reconciliation_receipt":rec,"read_only":True})

def write(output:Path,admission:dict[str,Any])->None:
    output.mkdir(parents=True,exist_ok=True); mapping={"semantic-admission-receipt.json":admission}
    if admission.get("semantic_evaluated"): mapping.update({"handoff-conformance-receipt.json":admission["conformance_receipt"],"handoff-state-delta-receipt.json":admission["state_delta_receipt"],"handoff-reconciliation-receipt.json":admission["reconciliation_receipt"]})
    for name,payload in mapping.items(): (output/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def args(argv:Iterable[str]|None=None)->argparse.Namespace:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]); p.add_argument("--repository"); p.add_argument("--authority-table",type=Path); p.add_argument("--output-dir",type=Path,default=Path("runtime/orchestrator/semantic-receipts")); p.add_argument("--pass-number",type=int,default=1); p.add_argument("--max-passes",type=int,default=3); p.add_argument("--prior-fingerprint",action="append",default=[]); return p.parse_args(argv)

def main(argv:Iterable[str]|None=None)->int:
    a=args(argv); root=a.root.resolve(); authority=a.authority_table
    if authority is not None and not authority.is_absolute(): authority=root/authority
    output=a.output_dir if a.output_dir.is_absolute() else root/a.output_dir
    try: admission=evaluate(root,a.repository,authority,a.pass_number,a.max_passes,a.prior_fingerprint)
    except SemanticError as e: admission=finish({"receipt_type":"stegverse.handoff_semantic_admission.receipt.v1","repository":a.repository,"terminal_decision":"FAIL_CLOSED","processing_disposition":"BLOCKED","semantic_evaluated":False,"failures":[str(e)]})
    write(output,admission); print("HANDOFF_SEMANTICS="+admission["terminal_decision"]); print("semantic_evaluated="+str(admission.get("semantic_evaluated",False)).lower()); return 0 if admission["terminal_decision"]=="ALLOW" else 1
if __name__=="__main__": raise SystemExit(main())
