# Held-out reconstruction-versus-fresh-inference routing (SOURCE PROPOSAL)

**Not a registered task or an executable StegVerse runtime.** Read [the proposed handoff](EXECUTION_PATH_ROUTING_MIRROR_HANDOFF.md) first. Central Task Registry admission and COSV allocation are pending at generation 243 observation. The historical Generation-2 nine-lane and Generation-3 eleven-lane experiment files are frozen and unchanged.

This directory contains the independently committed task oracle and an **offline adjudicator for supplied route observations**. It does not select production routes, make provider calls, synthesize cost, issue InTr decisions, fabricate receipts or prove Master Records custody.

The dataset distinguishes: exact reconstructable history; genuinely missing information requiring fresh inference; incomplete or conflicting evidence requiring an actionable non-ALLOW result; and mixed reconstruction-plus-fresh-inference. `cases.json` contains held-out reference oracle data for the evaluator only. A future router receives only the declared `router_input` fields, never `oracle`.

Run focused source-only checks after checking out this proposal branch:

```bash
python -m unittest discover -s experiments/sv-cost-program/held-out-routing/tests -v
python experiments/sv-cost-program/held-out-routing/evaluate.py --help
```

When admitted, the already-owned SDK manifest should declare `processing.capability` and `processing.route_id`, match `extensions.stegverse_route.route_id`, and use existing WorkerCoordinator / InTr / StegBrowser / LLM Adapter paths. Preserve authentic route, timing, custody and cost packets separately. Historical consumer UI surfaces without request-bound billing should remain exhausted, not become mandatory manual collection.

**Publication gate:** source-only adjudication is never actual routing. Authentic samples need exact manifest, routed processor, admissibility disposition, original predecessor-linked receipt, same-execution Master Records reconstruction and comparable request-bound full lifecycle costs. Missing cost stays UNKNOWN.

## Source validation evidence

The source-only evaluator's six focused tests passed on byte-identical checked source locally and in [the existing eleven-lane candidate-proof workflow run](https://github.com/GCAT-BCAT-Engine/workflows/actions/runs/36182218098) at proposal head `942b52b4344e3991c275ea510dc922515554e443`. Four negative-path tests and the four frozen case oracles are covered; tests do not prove that the runtime selected a route. Canonical admission remains [central issue #2722](https://github.com/StegVerse-Labs/.github/issues/2722), pending authenticated AI-session gate and authorized COSV derivation.

## Required SDK manifest gate

No `cases.json` row is an SDK test/demo. The four rows are hidden-oracle research designs for the offline adjudicator. **Every actual SDK test or demonstration must start with a validated canonical SDK manifest.** See [the SDK applicability review](SDK_MANIFEST_FIRST_CAPABILITY_REVIEW.md) and native SDK review [#332](https://github.com/StegVerse-org/StegVerse-SDK/issues/332). An installed manifest-bound generic evidence-sensitive reconstruction/new-inference selector is not established in inspected SDK source; this work is a source-only proposal until the existing SDK owner approves an existing composition or general SDK extension and central Registry admission succeeds. Do not route a provider call directly from this harness or classify offline fixture proof as a manifested SDK demonstration.

## Exact source-only continuation (Registry generation 248)

The four held-out oracle classes remain pre-manifest research only, NOT SDK demonstrations. Added independent source regressions for oracle leakage, NaN/infinite route latency, partial costs falsely claiming complete totals and invalid complete-cost measurement. **10/10 focused tests PASS** in existing eleven-lane candidate-proof [run 36195714940](https://github.com/GCAT-BCAT-Engine/workflows/actions/runs/36195714940), exact head `dbbafe5bb4bb68cc2eaa5424b2ce9ee6a2f2be16`; all five validation gates passed on that head. No consumer/runtime bytes, true route, billable cost or original organization/Master Records receipts were produced by these source checks. Central admission #2722 remains unassigned and SDK general capability review #332 is pending an owner decision. Do not construct a misleading `processing.capability` / route for the four real SDK experiment manifests while there is no installed processor or owner-approved composition; after SDK review, use only the SDK Manifest Builder and validator to create the canonical manifests before any actual SDK trial.
