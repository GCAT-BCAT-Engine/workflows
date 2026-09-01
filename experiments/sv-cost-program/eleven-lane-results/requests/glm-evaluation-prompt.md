# GLM-5.3-Flash SV-RECON-001 evaluation prompt

Use this exact task for both GLM-5.3-Flash Hosted and GLM-5.3-Flash Sovereign.

Do not add commentary. Return only one JSON object.

## Initial state

```json
{"balance":100,"risk_score":1,"standing":"active"}
```

## Policy

```json
{"minimum_balance":0,"maximum_risk_score":5,"standing_required_for_debit":"active"}
```

## Events

```json
[
  {"event_id":"E01","operation":"credit","amount":25},
  {"event_id":"E02","operation":"debit","amount":40},
  {"event_id":"E03","operation":"risk_add","amount":2},
  {"event_id":"E04","operation":"debit","amount":100},
  {"event_id":"E05","operation":"risk_add","amount":3},
  {"event_id":"E06","operation":"debit","amount":10}
]
```

## Rules

1. Process events in listed order.
2. A credit is ALLOW and increases balance.
3. A debit is ALLOW only when standing is active and resulting balance is not below minimum_balance; otherwise DENY and do not mutate state.
4. A risk_add is ALLOW only when resulting risk_score is not above maximum_risk_score; otherwise DENY and do not mutate state.
5. Denied events never mutate state.
6. Return only the required JSON object.

## Required output shape

```json
{
  "task_id":"SV-RECON-001",
  "final_state":{"balance":0,"risk_score":0,"standing":"active"},
  "decisions":[
    {"event_id":"E01","status":"ALLOW|DENY","reason":"..."}
  ],
  "applied_count":0,
  "denied_count":0,
  "claim_boundary":"DETERMINISTIC_RECONSTRUCTION_ONLY"
}
```

The numeric/example placeholders in the required output shape are not expected answers. Derive the result from the task.
