# CHF Roadmap — chf-041 through chf-060

## Assumptions

1. `chf-001` through `chf-040` establish the current validated base.
2. Future specs should continue the same pattern: explicit spec first, generated sandbox second.
3. Workflow remains unchanged.
4. Every new gate must have deterministic outcome labels.

## Proposed chf-041 through chf-050

### chf-041 — Adversarial Prompt / Instruction Boundary Gate

Purpose:

```text
Validate whether an incoming instruction attempts to override admissibility, conceal intent, or bypass authority.
```

Candidate outcomes:

```text
INSTRUCTION_ALLOWED
INSTRUCTION_FAIL_CLOSED
INSTRUCTION_QUARANTINED
```

### chf-042 — Tool Invocation Standing Gate

Purpose:

```text
Validate whether an agent has standing to invoke a tool before tool execution.
```

Candidate checks:

```text
tool authority
scope match
side-effect classification
rollback path
receipt readiness
```

### chf-043 — Secret / Credential Exposure Gate

Purpose:

```text
Validate whether a transition touches secrets, tokens, keys, or credentials.
```

Candidate checks:

```text
secret detection
least privilege
redaction readiness
rotation support
leak blast radius
```

### chf-044 — Data Exfiltration / Boundary Crossing Gate

Purpose:

```text
Validate whether data leaves an allowed boundary.
```

Candidate checks:

```text
destination trust
data classification
consent
purpose limitation
audit receipt
```

### chf-045 — Autonomous Recursion Limit Gate

Purpose:

```text
Validate whether recursive or self-triggering agent behavior remains bounded.
```

Candidate checks:

```text
recursion depth
loop detectability
human override
budget exhaustion
safe halt
```

### chf-046 — Model Output Reliance Gate

Purpose:

```text
Validate whether a generated output is allowed to become relied-upon operational state.
```

Candidate checks:

```text
confidence
source support
uncertainty labeling
domain criticality
human review requirement
```

### chf-047 — Simulation-to-Reality Transfer Gate

Purpose:

```text
Validate whether a transition proven in simulation may bind real-world effects.
```

Candidate checks:

```text
sim fidelity
environment gap
external dry run
bounded effect
rollback readiness
```

### chf-048 — Governance Capture / Influence Concentration Gate

Purpose:

```text
Detect concentrated control over governance or validation outcomes.
```

Candidate checks:

```text
validator concentration
token concentration
maintainer concentration
dependency concentration
correlated failure
```

### chf-049 — Dependency Drift / Supply Chain Gate

Purpose:

```text
Validate whether dependency or supply-chain state changed since evaluation.
```

Candidate checks:

```text
lockfile match
hash match
publisher trust
dependency age
vulnerability status
```

### chf-050 — Emergency Override / Break-Glass Gate

Purpose:

```text
Validate whether emergency action may bypass normal gates.
```

Candidate checks:

```text
emergency classification
bounded duration
multi-party approval
post-action receipt
mandatory review
```

## Proposed chf-051 through chf-060

### chf-051 — Human Override and Operator Recovery Gate

Purpose:

```text
Validate whether a human operator can interrupt, recover, or revoke an agent transition.
```

### chf-052 — AI-to-AI Coordination Boundary Gate

Purpose:

```text
Validate whether multiple AI entities coordinating over a network remain within admissible interaction bounds.
```

### chf-053 — Cross-Jurisdiction / Legal Boundary Gate

Purpose:

```text
Validate whether a transition crosses legal or jurisdictional boundaries.
```

### chf-054 — Accessibility and Degraded-Authority Recovery Gate

Purpose:

```text
Validate whether affected users retain recoverability under degraded capability, access, or authority.
```

### chf-055 — Epistemic Provenance Gate

Purpose:

```text
Validate whether the information basis for a transition is sufficiently sourced and traceable.
```

### chf-056 — Scientific Claim Escalation Gate

Purpose:

```text
Validate whether a scientific or mathematical claim requires stronger review before publication.
```

### chf-057 — Dataset Ingestion and Training Boundary Gate

Purpose:

```text
Validate whether data may be used for training, indexing, embedding, or model adaptation.
```

### chf-058 — Identity / Persona Continuity Gate

Purpose:

```text
Validate whether a persistent identity, persona, or agent memory remains coherent and authorized.
```

### chf-059 — Deletion / Forgetting / Retention Gate

Purpose:

```text
Validate whether data should be retained, deleted, forgotten, archived, or quarantined.
```

### chf-060 — Cross-Formalism Composition Gate

Purpose:

```text
Validate whether CHF can safely compose with GCAT/BCAT, ECAT/ICAT, Existence, Triad, Inference Window, and Transition Periodic Table formalisms.
```

## Recommended build cadence

```text
v0.16:
  chf-041 through chf-050 explicit specs

v0.17:
  generated sandbox suites for chf-041 through chf-050

v0.18:
  chf-051 through chf-060 explicit specs

v0.19:
  generated sandbox suites for chf-051 through chf-060

v0.20:
  formal verification readiness package
```
