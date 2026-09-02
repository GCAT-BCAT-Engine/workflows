# GLM evidence acquisition tools

These tools reduce candidate installation to local JSON ingestion and never request or persist provider credentials.

## Hosted lane

Save the exact GLM-5.3-Flash JSON response to a file, then run:

```bash
python tools/ingest_glm_hosted_candidate.py /path/to/glm-output.json
```

Add provider-observed usage only when actually available:

```bash
python tools/ingest_glm_hosted_candidate.py /path/to/glm-output.json \
  --response-id <provider-response-id> \
  --latency-seconds <observed-seconds> \
  --input-tokens <provider-reported-input> \
  --output-tokens <provider-reported-output> \
  --reported-cost-usd <provider-reported-cost>
```

Do not estimate omitted fields.

## Sovereign lane

After an eligible sovereign runtime produces the exact candidate JSON:

```bash
python tools/build_glm_sovereign_evidence.py /path/to/glm-output.json \
  --runtime-identity <exact-runtime-identity> \
  --elapsed-seconds <measured-runtime>
```

Add energy/hardware/network/storage costs only when measured or bounded by the runtime evidence source.

Both tools are evidence packaging helpers only. They do not call providers, launch models, grant authority, or convert missing runtime evidence into proof.
