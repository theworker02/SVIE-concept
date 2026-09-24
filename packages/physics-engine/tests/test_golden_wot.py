"""Golden-vector tests locking the published SVIE V8 WOT baseline."""

from __future__ import annotations

import math

import pytest

from svie_physics.air_fuel import compute_air_fuel, inputs_from_spec
from svie_physics.heat_exchanger import run_coupled as hex_coupled
from svie_physics.hem_choked_flow import cavitation_number, run_coupled as hem_coupled
from svie_physics.io_util import load_yaml, specs_dir
from svie_physics.piezo_driver import run_from_spec as driver_run
from svie_physics.piezo_dynamics import run_from_spec as piezo_run


@pytest.fixture(scope="module")
def engine():
    return load_yaml(specs_dir() / "svie_v8_52L.yaml")


@pytest.fixture(scope="module")
def sfv():
    return load_yaml(specs_dir() / "sfv_fuel_system.yaml")


@pytest.fixture(scope="module")
def piezo():
    return load_yaml(specs_dir() / "piezo_injector.yaml")


def test_air_fuel_wot_baseline(engine):
    g = engine["golden"]
    r = compute_air_fuel(inputs_from_spec(engine))
    assert r.cycles_per_s == pytest.approx(g["cycles_per_s"], rel=1e-3)
    assert r.v_dot_air_m3_s == pytest.approx(g["v_dot_air_m3_s"], rel=2e-3)
    assert r.m_dot_air_kg_s == pytest.approx(g["m_dot_air_kg_s"], rel=2e-3)
    assert r.m_dot_fuel_g_s == pytest.approx(g["m_dot_fuel_g_s"], rel=2e-3)
    assert r.m_dot_fuel_kg_h == pytest.approx(g["m_dot_fuel_kg_h"], rel=2e-3)
    assert r.liquid_equiv_L_h == pytest.approx(g["liquid_equiv_L_h"], rel=2e-2)
    assert r.mg_per_stroke == pytest.approx(g["mg_per_stroke"], rel=5e-3)
    assert r.e_in_kw == pytest.approx(g["e_in_kw"], rel=2e-3)
    assert r.m_dot_per_injector_g_s == pytest.approx(3.535, rel=2e-3)


def test_heat_exchanger_duty(engine, sfv):
    g = sfv["golden"]
    eg = engine["golden"]
    r = hex_coupled(engine, sfv)
    assert r["q_hex_kw"] == pytest.approx(g["q_hex_kw"], rel=2e-3)
    assert r["q_hex_per_bank_kw"] == pytest.approx(g["q_hex_per_bank_kw"], rel=2e-3)
    assert r["exhaust_energy_kw"] == pytest.approx(eg["exhaust_kw"], rel=2e-3)
    assert r["exhaust_recovery_ratio"] == pytest.approx(g["exhaust_recovery_ratio"], rel=2e-2)
    assert r["brake_power_kw"] == pytest.approx(eg["brake_power_kw"], rel=2e-3)
    assert r["combined_surface_area_m2"] == pytest.approx(0.28, rel=1e-6)


def test_hem_choked_and_orifice(engine, piezo):
    g = piezo["golden"]
    r = hem_coupled(engine, piezo)
    assert r["pressure_ratio"] == pytest.approx(g["pressure_ratio"], rel=1e-3)
    assert r["is_choked"] is True
    assert r["sigma_c"] == pytest.approx(g["sigma_c"], rel=2e-3)
    assert r["flash_boiling"] is True
    assert r["a_o_required_mm2"] == pytest.approx(g["a_o_required_mm2"], rel=2e-2)
    assert r["m_dot_kg_s"] * 1000 == pytest.approx(g["m_dot_per_injector_g_s"], rel=2e-3)


def test_cavitation_formula():
    assert cavitation_number(7.0, 1.0, 3.2) == pytest.approx(-0.579, abs=5e-4)


def test_piezo_stroke_and_area(piezo):
    g = piezo["golden"]
    r = piezo_run(piezo)
    assert r["delta_z_m"] == pytest.approx(g["delta_z_max_m"], rel=1e-6)
    assert r["a_o_mm2"] == pytest.approx(g["a_o_max_mm2"], rel=5e-3)
    assert r["delta_p_acoustic_mpa"] == pytest.approx(g["delta_p_acoustic_mpa"], rel=1e-2)
    # Envelope check vs required orifice
    assert r["a_o_mm2"] > g["a_o_required_mm2"]


def test_piezo_driver(piezo):
    g = piezo["golden"]
    r = driver_run(piezo, n_injectors=8)
    assert r["e_c_mj"] == pytest.approx(g["e_c_mj"], rel=1e-4)
    assert r["p_raw_w"] == pytest.approx(g["p_raw_w"], rel=2e-3)
    assert r["p_total_w"] == pytest.approx(g["p_total_8_injectors_w"], rel=3e-2)
    assert r["l_r_uh"] == pytest.approx(g["l_r_uh"], rel=2e-3)
    assert r["i_peak_a"] == pytest.approx(g["i_peak_a"], rel=5e-3)
    assert r["p_dissipated_estimate_w"] < 2.2


def test_specs_exist():
    required = [
        "svie_v8_52L.yaml",
        "sfv_fuel_system.yaml",
        "piezo_injector.yaml",
        "12m_ds_transmission.yaml",
        "9a_mc_transmission.yaml",
        "chassis_monocoque.yaml",
        "hert_transaxle.yaml",
        "breakthrough_subsystems.yaml",
        "svie_v8_hr_357.yaml",
        "deva_valvetrain.yaml",
        "h2_combustion_control.yaml",
        "thermal_oil_system.yaml",
        "bom_cost_estimate.yaml",
        "cvt_evidence.yaml",
        "axiom_drive.yaml",
        "ehe_v_bridge.yaml",
        "nexus_48.yaml",
        "sonic_nvh.yaml",
        "sentinel_safety.yaml",
        "chronos_cold_start.yaml",
        "trl_roadmap.yaml",
        "blend_brake.yaml",
        "mirage_twin.yaml",
        "vector_hcp.yaml",
    ]
    for name in required:
        assert (specs_dir() / name).is_file()
