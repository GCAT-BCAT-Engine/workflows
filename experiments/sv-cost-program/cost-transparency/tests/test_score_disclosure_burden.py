from score_disclosure_burden import score


def obs(**overrides):
    base = {
        "protocol_complete": True,
        "actual_request_cost_directly_exposed": False,
        "request_usage_directly_exposed": False,
        "all_material_cost_components_disclosed": False,
        "provider_surfaces_consulted": [],
        "external_sources_required": False,
        "account_or_privilege_required": False,
        "reconstructable_actual_cost": False,
    }
    base.update(overrides)
    return base


def test_direct():
    assert score(obs(actual_request_cost_directly_exposed=True)) == (0, "FINAL")


def test_one_step():
    assert score(obs(
        request_usage_directly_exposed=True,
        all_material_cost_components_disclosed=True,
        reconstructable_actual_cost=True,
        provider_surfaces_consulted=["request", "pricing"],
    )) == (1, "FINAL")


def test_multi_source():
    assert score(obs(
        request_usage_directly_exposed=True,
        all_material_cost_components_disclosed=True,
        reconstructable_actual_cost=True,
        provider_surfaces_consulted=["request", "pricing", "billing-rules"],
    )) == (2, "FINAL")


def test_account_gated():
    assert score(obs(
        reconstructable_actual_cost=True,
        account_or_privilege_required=True,
    )) == (3, "FINAL")


def test_external_research():
    assert score(obs(
        reconstructable_actual_cost=True,
        external_sources_required=True,
    )) == (4, "FINAL")


def test_non_reconstructable():
    assert score(obs()) == (5, "FINAL")


def test_incomplete_protocol_is_not_scored():
    assert score(obs(protocol_complete=False)) == (None, "NOT_SCORED_PROTOCOL_INCOMPLETE")
