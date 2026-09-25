# SDK manifest-first capability review for held-out execution-path selection

**Review class:** existing-SDK-capability applicability / possible general SDK extension. **No new task owner or runtime authority is created by this review.** Coordinated under StegVerse-Labs/.github#2722 and draft GCAT-BCAT-Engine/workflows#61. SDK owner must approve any new generic processing capability and schema/route installation.

## Mandatory test/demo contract

EVERY SDK test/demo run must begin with a **canonical SDK manifest**, produced and validated by the installed SDK Manifest Builder + `stegverse.ingress-manifest.v1` validator. A fixture description, Python script, GitHub workflow, route choice or raw provider request **does not count as an SDK test**. Test participants and generated results must bind the same original manifest/request hashes through the SDK run-manifest lineage. A non-ALLOW result is an explicit transition disposition with actionable reason/repair when nonterminal; terminal FAIL_CLOSED stops attempted execution. Only authentic InTr and Master Records original receipts establish live result/reconstruction. Return/Publisher/far-side completion must follow the manifest's declared `completion` requirements when applicable.

The four existing held-out JSON cases are **pre-manifest task-design oracles only**, usable for independent offline oracle-adjudicator tests. They are NOT SDK-submitted tests, SDK manifests, permitted runtime dispatch requests, or valid evidence of true routing. The oracle must never appear in runtime-facing payload, request or environment.

## Reviewed SDK source at 2026-09-25 main

- `StegVerse-org/StegVerse-SDK/stegverse/route_resolution.py` published/installed binding list: `governance` / `stegverse.route.canonical-governed.v1`; `ecosystem_diagnostic` / `stegverse.route.ecosystem-diagnostic.v1`; `purpose_bound_worker` / `stegverse.route.purpose-bound-worker.v1`; `atomic_task_worker` / `stegverse.route.atomic-task-worker.v1`. No published installed `execution_path_selection`, native evidence-reconstruction-vs-fresh-inference selector, or manifest-declared mixed/composite processor is present in this inspected list.
- `stegverse/manifest_builder.py` exposes those four `PROCESSOR_ROUTES` and refuses unknown capabilities. `stegverse/manifest_contract.py` already accepts processor-generic source-native payloads and requires `processing.capability` and `processing.route_id == extensions.stegverse_route.route_id`. `stegverse/manifest_execution.py` validates route + installed runtime binding and independently preserves canonical manifest/request/processor-result lineage; it refuses SDK-local worker semantic demonstrations as governed terminal completion.
- `stegverse/ecosystem_diagnostic_runtime.py` is installed **read-only diagnostic transport**, not an inference-vs-reconstruction selector, not a native continuity decision and not a substitute for an authoritative state reconstruction.
- `docs/UNIVERSAL_ENTRY_ROUTING_CONTRACT.md` specifies universal envelope capability/policy classification, multiple selected lanes, receipt-directed continuity and independent authority. This source-level contract does not prove a general SDK manifested composite route is installed or authentic live dispatch.
- `GENERIC_MANIFEST_PROCESSING_MIRROR_HANDOFF.md` and `ECOSYSTEM_DIAGNOSTIC_PROCESSOR_MIRROR_HANDOFF.md` distinguish structural acceptance and local semantic processor tests from actual governed execution/communication completion. Preserve them and their native ownership.

**Source-review disposition:** `GENERAL_SDK_EXTENSION_REVIEW_REQUIRED` for the actual held-out adaptive route-selection run. The SDK can manifest existing installed routes individually, but the inspected source does not establish an installed single manifest-owned choice between reconstruction and new inference and a mixed successor. Do not fake `processing.capability`, use a provider's identity to select processor semantics, or bypass the SDK by calling a provider/StegBrowser directly from the benchmark harness.

## General expansion review — not a benchmark-specific processor

The existing SDK generic-manifest owner should assess whether the universal entry router and existing installed processors can compose this operation *without* a new capability. If not, extend the SDK through one **general-purpose, reusable, manifest-directed evidence-sensitive processing capability**, suitable for arbitrary external frameworks/task classes, not an SV-COST-specific route or hardcoded four-fixture dispatcher.

Suggested behavior for review (not installed or authorized):
1. Caller declares `processing.capability`, explicit published route, bounded permitted successor-capability set, evidence requirements, allowed external consequences, budget/cost observation requirements, return projection and complete communication lifecycle inside one SDK manifest. Keep source-native payload and policy authority distinct.
2. SDK validates full manifest and locks its hash *before* any route evaluation. Route selection is an **execution decision within an admitted declared processor**; runtime cannot rewrite original `processing.route_id` after admission. Each selected successor operation receives its own manifest-bound request/predecessor and applicable authorization, not an implicit second route.
3. Evaluate evidence sufficiency against supplied/canonically accessible predecessor and policy with explicit dispositions. Choose existing installed reconstruction if complete, manifest-authorized new inference only when needed and actually available, mixed execution only if the manifest permits declared stages, otherwise DENY/REVIEW_REQUIRED with precise corrective requirement. An initial classifier decision by itself cannot grant execution authority.
4. Reuse existing SDK state-transition derivation/run-manifest binding, existing universal entry route/policy classification, InTr, WorkerCoordinator, StegBrowser bounded lease, TV/TVC credentials, provider adapters, organization ledger and Master Records; no additional scheduler, authority, ledger, device or SDK demo-only execution path.
5. Return per-stage processor/route selection, evidence sufficiency predicate, actual candidate output, latency, attempts/repair/cleanup and cost basis with missing measurements UNKNOWN, separately attributable participant receipts, exact predecessor chain, matching Master Records reconstruction and manifest-declared final return/far-side completion when required.
6. Incompatibility/non-installed runtime must return an actionable, precise non-ALLOW disposition **before any provider call**. The SDK expansion decision itself is not runtime authority. Preserve independently declared oracle outside routed runtime payload for later evaluation.

## General acceptance tests to request from native SDK owner

- Canonical SDK builder+validator generate/accept each of the four different task classes; each has unique original manifest/request hash and includes a reusable processing declaration. For currently unsupported selection, fail closed before runtime instead of manufacturing a successful manifest.
- Reject absent manifest, processing/route mismatch, uninstalled capability, oracle leaked into runtime input, forged predecessor hash, unauthorized second-stage provider execution and missing explicit stage authorization.
- Preserve source-native semantics and mixed stage order, conditional manifest-declared Publisher and far-side InTr egress; do not equate a local SDK source PASS with authentic live execution.
- Independently reconstruct one authentic sample in each class from original organization HEAD/predecessor-linked receipts + Master Records. Costs and latency must be per-stage and full lifecycle when measured; missing billed usage remains UNKNOWN, not zero.
- Use current SDK owner to decide if this is source extension, already-installed capability composition, or an exact non-ALLOW due to missing installation/authorization. Do not introduce an extra task ID or derive COSV from this review.

## Adjacent native ownership

- SDK generic manifest / Manifest Builder / run-manifest route lineage (existing SDK ownership, e.g. completed generic processor source review `StegVerse-org/StegVerse-SDK#126`; native SDK reviewer must resolve successor authority).
- `StegVerse-org/StegVerse-SDK#215` existing concurrent-manifest source/relationship invariants, where multiple stages or providers must stay disjoint.
- `StegVerse-org/StegVerse-SDK#315` existing SDK resource-cost linkage acceptance; central `WORKER-TASK-RESOURCE-COST-LINKAGE-001` remains active/unclaimed with no observed canonical COSV at Registry generation 246.
- `StegVerse-002/micro-node-runtime#69` current lane-11 sovereign GLM evidence; existing TVC request-bound measurement owner and original eleven-lane producer. Keep all existing authorship and no duplicate owners.

## Explicit nonclaims

No authentic ChatGPT session-origin check-in, COSV, production SDK expansion, governed trial, routing decision, provider receipt, complete lifecycle cost or Master Records readback is established by this review. Four fixture oracles and source-only CI are research prep, not SDK testing/demonstration or license to run.
