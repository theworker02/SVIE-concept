"""Acquisition suite + compliance + supply-chain golden tests."""

from __future__ import annotations

import pytest

from svie_physics.acquisition_suite import run_all as acq_all
from svie_physics.compliance import run_all as compliance_all
from svie_physics.supply_chain import run_supply_chain


def test_acquisition_suite():
    all_ = acq_all()
    assert all_["readiness"]["weighted_score"] >= 85
    assert all_["readiness"]["gates_pass"] is True
    assert all_["readiness"]["production_ready_acquisition"] is True
    assert all_["readiness"]["hardware_trl_ceiling"] == 3
    assert all_["deal"]["preferred_structure"] == "exclusive_fou_plus_option"
    assert all_["deal"]["structures"] == 3
    assert all_["deal"]["escrow"] is True
    assert all_["data_room"]["folders"] == 8
    assert all_["data_room"]["term_sheet_present"] is True


def test_compliance_and_supply():
    c = compliance_all()
    assert c["homologation"]["markets"] == 3
    assert c["iso26262"]["max_asil"] == "D"
    assert c["iso26262"]["certificate"] is False
    assert c["iso21434"]["guest_untrusted"] is True
    assert c["ota"]["signed_only"] is True
    assert c["durability"]["g3_hours"] == 2000
    s = run_supply_chain()
    assert s["critical_parts"] == 6
    assert s["max_lead_weeks"] == 32
    assert s["dual_source_targets"] == 5
