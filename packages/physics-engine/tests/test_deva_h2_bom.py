"""Golden tests for DEVA, H2 combustion, and BOM modules."""

from __future__ import annotations

import pytest

from svie_physics.bom_cost import run_from_spec as bom_run
from svie_physics.deva_power import run_from_spec as deva_run
from svie_physics.h2_combustion import run_case
from svie_physics.io_util import load_yaml, specs_dir


@pytest.fixture(scope="module")
def deva():
    return load_yaml(specs_dir() / "deva_valvetrain.yaml")


@pytest.fixture(scope="module")
def h2():
    return load_yaml(specs_dir() / "h2_combustion_control.yaml")


@pytest.fixture(scope="module")
def bom():
    return load_yaml(specs_dir() / "bom_cost_estimate.yaml")


def test_deva_wot_and_cruise(deva):
    g = deva["golden"]
    wot = deva_run(deva, rpm=8500, mode="wot")
    cruise = deva_run(deva, rpm=3000, mode="cruise")
    assert wot["events_per_s_per_valve"] == pytest.approx(
        g["events_per_s_per_valve_8500"], rel=1e-3
    )
    assert wot["total_electrical_kw"] == pytest.approx(
        g["power_electrical_kw_8500_wot"], rel=1e-2
    )
    assert cruise["total_electrical_kw"] == pytest.approx(
        g["power_electrical_kw_3000_cruise"], rel=2e-2
    )


def test_h2_lambda_and_water(h2):
    g = h2["golden"]
    mild = run_case(h2, lambda_value=1.05, water_fuel_ratio=0.0)
    lean = run_case(h2, lambda_value=2.8, water_fuel_ratio=0.0)
    wet = run_case(h2, lambda_value=1.05, water_fuel_ratio=0.15)
    assert mild["afr_mass"] == pytest.approx(g["afr_at_lambda_1_05"], rel=1e-3)
    assert lean["afr_mass"] == pytest.approx(g["afr_at_lambda_2_8"], rel=1e-3)
    assert wet["nox_reduction_pct"] == pytest.approx(
        g["water_ratio_0_15_nox_reduction_pct"], abs=0.5
    )
    assert wet["pre_ignition_strategy"] == g["pi_strategy"]
    assert lean["nox_index"] < mild["nox_index"]


def test_bom_rollup(bom):
    g = bom["golden"]
    r = bom_run(bom, include_chassis=False)
    full = bom_run(bom, include_chassis=True)
    assert r["powertrain_subtotal_usd"] == pytest.approx(g["powertrain_subtotal_usd"], abs=1)
    assert full["total_usd"] == pytest.approx(g["with_chassis_share_usd"], abs=1)
