#!/usr/bin/env python3
"""Deterministic ACTUAL_COST_DISCLOSURE_BURDEN scorer."""

def score(observation: dict) -> tuple[int | None, str]:
    if observation.get("actual_request_cost_directly_exposed") is True:
        return 0, "PROVISIONAL_DIRECT_EVIDENCE" if not observation.get("protocol_complete") else "FINAL"

    if not observation.get("protocol_complete"):
        return None, "NOT_SCORED_PROTOCOL_INCOMPLETE"

    reconstructable = observation.get("reconstructable_actual_cost") is True
    usage = observation.get("request_usage_directly_exposed") is True
    material = observation.get("all_material_cost_components_disclosed") is True
    account = observation.get("account_or_privilege_required") is True
    external = observation.get("external_sources_required") is True
    surfaces = observation.get("provider_surfaces_consulted") or []

    if reconstructable and usage and material and not account and not external and len(surfaces) <= 2:
        return 1, "FINAL"
    if reconstructable and not account and not external:
        return 2, "FINAL"
    if reconstructable and account:
        return 3, "FINAL"
    if reconstructable and external:
        return 4, "FINAL"
    return 5, "FINAL"


if __name__ == "__main__":
    import json, sys
    observation = json.load(sys.stdin)
    rating, state = score(observation)
    print(json.dumps({"disclosure_burden_rating": rating, "rating_state": state}, separators=(",", ":")))
