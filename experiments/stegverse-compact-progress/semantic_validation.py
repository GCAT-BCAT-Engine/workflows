#!/usr/bin/env python3
import re

FORBIDDEN = [
    r"deployed (?:engine|implementation).{0,40}(?:satisfies|verified|conforms)",
    r"production (?:engine|implementation).{0,40}(?:satisfies|verified|conforms)",
]


def _has(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, re.I | re.S) for p in patterns)


def validate(stage_id: str, text: str) -> dict:
    checks: dict[str, bool] = {}
    if stage_id == "S0":
        checks = {
            "task": _has(text, [r"task identity", r"characterize.{0,120}allow", r"abstract gcat/bcat evaluator"]),
            "formula": all(x.lower() in text.lower() for x in ["ALLOW", "GBP", "BD", "OC"]) and _has(text, [r"↔", r"iff", r"if and only if", r"exactly when"]),
            "abstract_scope": _has(text, [r"abstract evaluator", r"stipulat", r"axiomatic", r"source problem"]),
            "deployment_boundary": _has(text, [r"no claim.{0,100}deployed", r"does not establish.{0,100}deployed", r"out of scope", r"implementation validity.{0,80}(?:separate|unresolved|evidence)"]),
        }
    elif stage_id == "S1":
        checks = {x: x.lower() in text.lower() for x in ["GBP", "BD", "OC", "ALLOW"]}
        checks["predicate_types_or_definitions"] = _has(text, [r"(?:→|->)\s*Prop", r"predicate", r"definition", r"define"])
    elif stage_id == "S2":
        checks = {
            "necessity": _has(text, [r"necessary", r"necessity", r"forward implication"]),
            "sufficiency": _has(text, [r"sufficient", r"sufficiency", r"reverse implication"]),
            "biconditional": _has(text, [r"↔", r"iff", r"if and only if"]),
            "symbols": all(x.lower() in text.lower() for x in ["ALLOW", "GBP", "BD", "OC"]),
        }
    elif stage_id == "S3":
        checks = {
            "forward": _has(text, [r"forward", r"necessity"]),
            "reverse": _has(text, [r"reverse", r"sufficiency"]),
            "strategy_or_lemma": _has(text, [r"strategy", r"lemma", r"decomposition", r"proof architecture"]),
        }
    elif stage_id == "S4":
        checks = {
            "proof": _has(text, [r"proof"]),
            "forward": _has(text, [r"forward", r"necessity"]),
            "reverse": _has(text, [r"reverse", r"sufficiency"]),
            "boundary": _has(text, [r"deployed", r"implementation", r"claim boundary", r"out of scope"]),
        }
    elif stage_id == "S5":
        checks = {
            "lean_block": _has(text, [r"```lean", r"```lean4"]),
            "theorem": _has(text, [r"\btheorem\b"]),
            "symbols": all(x.lower() in text.lower() for x in ["ALLOW", "GBP", "BD", "OC"]),
        }
    elif stage_id == "S6":
        checks = {
            "verification_status": _has(text, [r"verified", r"verification", r"compiled", r"kernel", r"not verified", r"unverified"]),
            "evidence": _has(text, [r"evidence", r"receipt", r"hash", r"artifact"]),
            "implementation_boundary": _has(text, [r"implementation", r"deployed", r"unresolved", r"out of scope"]),
        }
    else:
        checks = {"known_stage": False}

    forbidden_hits = [p for p in FORBIDDEN if re.search(p, text, re.I | re.S)]
    missing = [name for name, passed in checks.items() if not passed]
    return {
        "admitted": not missing and not forbidden_hits,
        "checks": checks,
        "missing": missing,
        "forbidden_claim": bool(forbidden_hits),
        "forbidden_hits": forbidden_hits,
        "validator": "semantic-structural-v2",
    }
