# Ten Advances Cost Estimation Mirror Handoff

## Authority and scope

This file is the current task source of truth for estimating the cost and feasibility of reproducing the ten mathematical advances described by OpenAI using controlled StegVerse workflows.

Incoming problem descriptions are research candidates, not claims that StegVerse or any provider can reproduce the published results.

## Active goal

```text
goal_id: TEN-ADVANCES-DUAL-PROVIDER-ESTIMATION-001
goal: obtain comparable provider estimates and StegVerse-governed estimates for attempting the ten mathematical problems, then determine whether the StegVerse sandbox and ecosystem can independently attempt any problem within a declared budget
repository: GCAT-BCAT-Engine/workflows
branch: main
state: SPECIFIED_NOT_EXECUTED
manual_user_action_required: false unless provider credentials or spend authorization are absent
```

## Experimental matrix

Each of the ten problems must be evaluated in five distinct lanes:

1. OpenAI, non-governed baseline.
2. OpenAI, StegVerse-governed execution.
3. Anthropic, non-governed baseline.
4. Anthropic, StegVerse-governed execution.
5. StegVerse sandbox/ecosystem-only attempt, using only installed local or ecosystem capabilities and no undeclared external provider inference.

Governed and non-governed lanes must use the same problem statement, target output, success criteria, and budget ceiling. Governance overhead must be measured separately from inference/search cost.

## Estimation-only first phase

Providers must not attempt to solve the problems during the first phase. Each request must independently estimate:

- recommended model and execution mode;
- expected input, output, reasoning, search, and verification tokens;
- expected candidate branches, failed branches, retries, and escalation count;
- expected wall-clock duration;
- expected API cost with low, central, and high estimates;
- expected formalization, replication, and independent-review cost;
- probability of producing a publishable result under the declared budget;
- probability of reproducing the known result versus finding an independent valid result;
- principal uncertainty drivers;
- minimum evidence required before a result may be called solved.

Prompts must prohibit anchoring on OpenAI's published aggregate cost estimate. Provider estimates must be produced independently from the stated mathematical scope.

## Five-lane comparison outputs

For each problem, preserve:

```text
problem_id
lane_id
provider
model_or_runtime
execution_posture
estimated_search_cost
estimated_governance_overhead
estimated_verification_cost
estimated_total_cost_low
estimated_total_cost_central
estimated_total_cost_high
estimated_elapsed_time
estimated_success_probability
confidence
assumptions
blockers
receipt_hash
```

The comparison report must distinguish:

- token price from capability-adjusted cost;
- successful-path cost from total search cost;
- inference cost from governance and verification overhead;
- provider-estimated feasibility from observed feasibility;
- reproduction of a published result from an independent discovery.

## StegVerse-only feasibility gate

A problem may proceed to a bounded StegVerse-only attempt only when all of the following are true:

1. Required mathematical domain tools are installed or explicitly declared unavailable.
2. The sandbox can preserve problem identity, branch history, evidence, and deterministic receipts.
3. A bounded budget and timeout are declared.
4. Success and failure criteria are machine-readable.
5. The attempt cannot silently invoke OpenAI, Anthropic, or another undeclared provider.
6. Verification can be performed independently of the generating path.
7. The expected value of the attempt justifies the compute and review cost.

The first candidate should be selected by feasibility, not prestige: lowest estimated search cost, highest verification tractability, strongest available tool support, and clearest bounded subproblem.

## Required implementation files

```text
experiments/ten-advances/problems.json
experiments/ten-advances/estimation-schema.json
experiments/ten-advances/prompts/openai-estimate.md
experiments/ten-advances/prompts/anthropic-estimate.md
experiments/ten-advances/prompts/governed-estimate.md
experiments/ten-advances/config/lanes.json
experiments/ten-advances/tools/run_estimation_matrix.py
experiments/ten-advances/tools/normalize_estimates.py
experiments/ten-advances/tools/select_sandbox_candidate.py
experiments/ten-advances/tools/validate_estimation_receipts.py
.github/workflows/ten-advances-estimation.yml
reports/ten-advances-estimation-summary.md
```

## Validation requirements

- All ten problems present exactly once.
- All five lanes represented for every problem.
- No estimate accepted without assumptions and uncertainty bounds.
- No provider estimate represented as observed cost.
- No sandbox-only result represented as provider-independent if an undeclared external model was invoked.
- All raw responses retained with hashes and normalized records.
- Comparison calculations reproducible from repository artifacts.

## Exact remaining tasks

1. Install the ten normalized problem records.
2. Install provider-neutral and provider-specific estimation prompts.
3. Install the five-lane execution configuration.
4. Implement the estimation runner and normalization validators.
5. Add provider credential and spend-boundary checks.
6. Execute estimation-only runs for OpenAI and Anthropic.
7. Produce the governed versus non-governed comparison.
8. Rank the ten problems for bounded StegVerse-only feasibility.
9. Execute no solve attempt until the selected candidate passes the feasibility gate.
10. Publish results through Publisher and mirror to Site only after evidence validation.

## Completion accounting

```text
task_completion: 1/10
required_developed_files: 12
developed_files: 1
scaffolding_or_stubs: 0
missing_required_files: 11
goal_activation: 10%
```

## Archive condition

This handoff preserves the complete experimental intent. The originating chat may be archived once subsequent implementation state is recorded here or in successor receipts; no unstored conceptual dependency should remain in the chat.
