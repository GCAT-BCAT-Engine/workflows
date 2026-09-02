# SV-COST Eleven-Lane Generation 3

Canonical continuation: `ELEVEN_LANE_MIRROR_HANDOFF.md`.

## Fastest credentialless run

```bash
python validate_schema.py
python run.py
```

The harness immediately reuses the frozen Generation-2 candidate evidence for lanes 1-9. It emits all 11 rows and fail-closes lanes 10-11 when GLM evidence is absent.

## Completing lane 10 — GLM-5.3-Flash Hosted

1. Submit `requests/glm-evaluation-prompt.md` to GLM-5.3-Flash through an existing external provider relationship, or through a TV/TVC-authorized hosted provider operation whose credential remains process-local and non-exportable.
2. Preserve the returned task JSON in a record matching `candidate-input.schema.json`.
3. Set `provider=zai`, `model=GLM-5.3-Flash`, `task_id=SV-RECON-001`, and `provider_api_key_transferred_to_stegverse=false`.
4. Install as `candidate-inputs/glm-hosted.json`.
5. Re-run `run.py`.

No provider credential belongs in this repository.

## Completing lane 11 — GLM-5.3-Flash Sovereign

1. Materialize GLM-5.3-Flash behind an eligible sovereign OpenAI-compatible inference endpoint.
2. Submit the exact same `requests/glm-evaluation-prompt.md`.
3. Capture the exact output and runtime measurements under `sovereign-runtime-evidence.schema.json`.
4. Install as `runtime-evidence/glm-sovereign.json`.
5. Re-run `run.py`.

Vendor API credential use must remain false.

## Result

`results/generation-3-eleven-lane/eleven_lane_generation_3_results.json`

Publication remains blocked until all eleven evidence lanes and bounded cost evidence are complete.


## Hosted candidate acquired — 2026-09-02

The exact user-supplied GLM-5.3-Flash hosted JSON output is installed at `candidate-inputs/glm-hosted.json` with no provider credential, usage, latency, response ID, or cost inferred. Free-form reason prose is preserved in the raw candidate while semantic validation compares event IDs, ALLOW/DENY outcomes, final state, and counts against the deterministic contract.
