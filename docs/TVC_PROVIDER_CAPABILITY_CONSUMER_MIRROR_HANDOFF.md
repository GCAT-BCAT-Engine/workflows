# TVC Provider Capability Consumer Mirror Handoff

## Authority and scope

This scoped handoff is subordinate to `docs/WORKFLOWS_MIRROR_HANDOFF.md` and authoritative for `GCAT-TVC-PROVIDER-CAPABILITY-CONSUMER-001`.

```text
goal_id: GCAT-TVC-PROVIDER-CAPABILITY-CONSUMER-001
repository: GCAT-BCAT-Engine/workflows
branch: main
claim state: COMPLETE_RELEASED
canonical provider-capability authority: StegVerse-Labs/TVC
canonical source task: TVC-PROVIDER-CAPABILITY-RESOLUTION-001
credential authority: TC/TVC
consumer policy authority: false
GitHub token production requirement: false
```

## Installed surfaces

```text
contracts/tvc-provider-capability-v1.json
tools/tvc_provider_capability_consumer.py
tests/test_tvc_provider_capability_consumer.py
tasks/GCAT-TVC-PROVIDER-CAPABILITY-CONSUMER-001.json
docs/TVC_PROVIDER_CAPABILITY_CONSUMER_MIRROR_HANDOFF.md
```

The contract pin identifies immutable TVC source commit `1c5ed9f83405a8d76f4759810162f7def4959f33`, the canonical resolver/policy/schema/task paths, and policy stable hash `1f1f9deaa2355d118231647a14e87673137ef3ad5f25809af0444798e741e6ab`.

## Consumer behavior

The consumer discovers only locally materialized TVC source, verifies the pinned policy hash and current `StegVerse-Labs/TVC` / `TC/TVC` authority contract, imports TVC's resolver, submits non-secret capability/provider-inventory requests, and accepts only TVC-verifiable receipts with no GitHub-token requirement and no execution authority.

There is no network source checkout and no workflows-local policy fallback. Missing TVC or policy drift fails closed.

## Historical resolver disposition

`experiments/sv-cost-program/stream-governance/resolve_provider_routes.py` and `experiments/sv-cost-program/cost-model/provider-capability-policy.json` remain historical research/prototype evidence. They are **SUPERSEDED_AS_CANONICAL_PROVIDER_CAPABILITY_AUTHORITY** by the pinned TVC contract.

## Validation and release evidence

```text
pinned TVC policy hash enforced: PASS
TVC resolver rather than consumer policy selects route: PASS
policy drift fail-closed: PASS
consumer-local policy fallback prohibited: PASS
GitHub-token production dependency false: PASS
TC/TVC credential semantics preserved: PASS
route selection grants no execution authority: PASS
continuity provenance: PASS
PR: #14
merge: d96ffcbd3b8d879ef8554e22777e73ecd6125996
source TVC PR: StegVerse-Labs/TVC#18
source TVC merge: 8f9067b8cc40e65147117dfe53b0b3dc3c8ba714
claim state: COMPLETE_RELEASED
```

## Continuation

No integration claim remains. StegFin may consume canonical `base.quote.0x` route receipts through TVC only after fresh governed Inventory N exists, while provider capability material remains non-exportable and is delivered only through the separately authorized TC/TVC/vault inherited-FD boundary. User wallet signing and broadcast remain USER_ONLY.
