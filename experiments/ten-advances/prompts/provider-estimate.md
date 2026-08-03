# Ten Advances — Independent Resource Estimate

Do not solve the mathematical problem. Do not rely on, quote, or anchor to any published aggregate cost estimate.

Estimate the resources required for an autonomous research system using your provider's models to independently reproduce or derive a publishable result matching the stated target. Include literature ingestion, exploratory search, failed branches, critic passes, computational experiments, proof reconstruction, independent verification, formalization, replication, and manuscript preparation.

Return exactly one JSON object. Required fields:

problem_id, lane_id, provider, model_or_runtime, execution_posture, estimated_input_tokens, estimated_output_tokens, estimated_reasoning_tokens, estimated_candidate_branches, estimated_failed_branches, estimated_retries, estimated_search_cost, estimated_governance_overhead, estimated_verification_cost, estimated_total_cost_low, estimated_total_cost_central, estimated_total_cost_high, estimated_elapsed_hours_low, estimated_elapsed_hours_central, estimated_elapsed_hours_high, estimated_success_probability, estimated_reproduction_probability, estimated_independent_result_probability, confidence, assumptions, uncertainty_drivers, minimum_evidence, blockers.

Use probabilities from 0 to 1 and USD for all costs. Distinguish reproduction of a known published proof from independent rediscovery. Do not claim observed feasibility. For a governed lane, separately price the overhead of identity hashing, budget enforcement, branch receipts, evidence preservation, policy checks, and independent verification. For a non-governed lane, set governance overhead to zero but do not omit verification needed for publication.
