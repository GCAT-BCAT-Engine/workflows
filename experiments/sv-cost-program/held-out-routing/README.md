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
