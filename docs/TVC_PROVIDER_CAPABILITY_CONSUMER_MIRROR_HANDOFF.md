# TVC Provider Capability Consumer Mirror Handoff

## Authority and scope

This scoped handoff is subordinate to `docs/WORKFLOWS_MIRROR_HANDOFF.md` and authoritative for `GCAT-TVC-PROVIDER-CAPABILITY-CONSUMER-001`. It is a new successor integration after the prior workflows session was archived; it does not reopen superseded historical task ownership.

```text
goal_id: GCAT-TVC-PROVIDER-CAPABILITY-CONSUMER-001
repository: GCAT-BCAT-Engine/workflows
branch: integration/tvc-provider-capability-consumer-20260810
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

Those experiment surfaces may still gather provider inventories or support historical replay, but any new governed provider-capability route decision must pass through `tools/tvc_provider_capability_consumer.py` and canonical TVC policy.

## Validation

Tests prove:

```text
pinned TVC policy hash is enforced
TVC resolver rather than consumer policy selects the route
policy drift fails closed
consumer-local policy fallback is prohibited
GitHub-token production dependency is false
TC/TVC credential semantics are preserved
route selection grants no execution authority
```

## Claim release condition

Merge the pinned contract, adapter, equivalence tests, task, and this handoff. Then mark this integration claim COMPLETE_RELEASED and allow TVC task `TVC-PROVIDER-CAPABILITY-RESOLUTION-001` to release its implementation claim.

## Continuation

After release, StegFin may consume canonical `base.quote.0x` route receipts through TVC while provider capability material itself remains non-exportable and is delivered only through the separately authorized TC/TVC/vault inherited-FD boundary. User wallet signing and broadcast remain USER_ONLY.
