from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "tvc_provider_capability_consumer",
    ROOT / "tools" / "tvc_provider_capability_consumer.py",
)
assert SPEC and SPEC.loader
consumer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(consumer)


def materialize_tvc(root: Path) -> None:
    pin = consumer.load_pin()
    policy = {
        "schema_version": "stegverse.tvc.provider-capability-policy.v1",
        "policy_id": "TVC-PROVIDER-CAPABILITY-POLICY-001",
        "authority": "StegVerse-Labs/TVC",
        "credential_authority": "TC/TVC",
        "selection_rule": "priority_then_provider_id",
        "receipt_secret_fields_prohibited": True,
        "route_grants_execution_authority": False,
        "capabilities": {
            "base.quote.0x": {
                "allowed_provider_classes": ["zeroex_v2"],
                "excluded_model_classes": [],
                "credential_requirement": "NON_EXPORTABLE_PROVIDER_CAPABILITY",
                "credential_delivery": "INHERITED_FILE_DESCRIPTOR",
                "network": "base-mainnet",
                "operation": "firm_quote",
            },
            "local.model.inference": {
                "allowed_provider_classes": ["stegverse_local"],
                "excluded_model_classes": [],
                "credential_requirement": "NONE",
                "credential_delivery": "NONE",
                "network": "local-private",
                "operation": "inference",
            },
        },
    }
    assert consumer.stable_hash(policy) == pin["policy_stable_sha256"]
    policy_path = root / pin["policy_path"]
    policy_path.parent.mkdir(parents=True, exist_ok=True)
    policy_path.write_text(json.dumps(policy), encoding="utf-8")
    for path_key in ("request_schema_path", "receipt_schema_path", "source_task"):
        path = root / pin[path_key]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
    resolver = root / pin["resolver_path"]
    resolver.parent.mkdir(parents=True, exist_ok=True)
    resolver.write_text(
        "import hashlib,json\n"
        "def stable_hash(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()\n"
        "def resolve(req,policy=None):\n"
        " p=sorted([r for r in req['provider_inventory'] if r['available']],key=lambda r:(r['priority'],r['provider_id']))[0]\n"
        " out={'schema_version':'stegverse.tvc.provider-route-receipt.v1','state':'ROUTE_ADMITTED','request_id':req['request_id'],'capability':req['capability'],'consumer':req['consumer'],'route_authority':'StegVerse-Labs/TVC','credential_authority':'TC/TVC','provider_id':p['provider_id'],'provider_class':p['provider_class'],'route_ref':p.get('route_ref'),'credential_requirement':'NON_EXPORTABLE_PROVIDER_CAPABILITY','credential_delivery':'INHERITED_FILE_DESCRIPTOR','network':'base-mainnet','operation':'firm_quote','policy_hash':stable_hash(policy),'inventory_hash':stable_hash(req['provider_inventory']),'github_token_required':False,'secret_material_present':False,'execution_authority':False,'authority_effect':'NONE','reason':'CAPABILITY_ROUTE_RESOLVED'}\n"
        " out['receipt_hash']=stable_hash(out); return out\n"
        "def verify_receipt(r):\n"
        " c=dict(r); expected=c.pop('receipt_hash',None); return expected==stable_hash(c) and r.get('github_token_required') is False and r.get('execution_authority') is False\n",
        encoding="utf-8",
    )


def test_consumer_uses_pinned_tvc_contract_and_not_local_policy() -> None:
    with tempfile.TemporaryDirectory() as temp:
        tvc = Path(temp)
        materialize_tvc(tvc)
        request = {
            "schema_version": "stegverse.tvc.provider-capability-request.v1",
            "request_id": "consumer-test",
            "capability": "base.quote.0x",
            "consumer": "GCAT-BCAT-Engine/workflows",
            "provider_inventory": [
                {"provider_id":"b","provider_class":"zeroex_v2","model_class":None,"capabilities":["base.quote.0x"],"available":True,"priority":20,"route_ref":"https://api.0x.org/quote"},
                {"provider_id":"a","provider_class":"zeroex_v2","model_class":None,"capabilities":["base.quote.0x"],"available":True,"priority":10,"route_ref":"https://api.0x.org/quote"},
            ],
        }
        receipt = consumer.resolve_via_tvc(request, tvc_root=tvc)
        assert receipt["provider_id"] == "a"
        assert receipt["credential_authority"] == "TC/TVC"
        assert receipt["github_token_required"] is False
        assert receipt["execution_authority"] is False


def test_policy_drift_fails_closed() -> None:
    with tempfile.TemporaryDirectory() as temp:
        tvc = Path(temp)
        materialize_tvc(tvc)
        pin = consumer.load_pin()
        policy_path = tvc / pin["policy_path"]
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        policy["credential_authority"] = "legacy"
        policy_path.write_text(json.dumps(policy), encoding="utf-8")
        try:
            consumer.load_tvc(tvc)
        except RuntimeError as exc:
            assert str(exc) == "tvc_provider_capability_policy_hash_mismatch"
        else:
            raise AssertionError("policy drift must fail closed")


def test_pin_forbids_consumer_policy_fallback_and_github_dependency() -> None:
    pin = consumer.load_pin()
    assert pin["consumer_policy_authority"] is False
    assert pin["fallback_to_local_policy_allowed"] is False
    assert pin["github_token_required"] is False
    assert pin["credential_authority"] == "TC/TVC"
