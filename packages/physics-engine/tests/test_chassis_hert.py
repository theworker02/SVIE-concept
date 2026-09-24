"""Golden tests for chassis, HERT, GDSA, gear map, breakthrough features."""

from __future__ import annotations

import pytest

from svie_physics.breakthrough import run_breakthrough_bundle
from svie_physics.chassis_torsion import run_from_spec as chassis_run
from svie_physics.gdsa_shift import run_from_spec as gdsa_run
from svie_physics.gear_map import run_from_spec as gear_run
from svie_physics.hert_expansion import run_from_spec as hert_run
from svie_physics.io_util import load_yaml, specs_dir


@pytest.fixture(scope="module")
def chassis():
    return load_yaml(specs_dir() / "chassis_monocoque.yaml")


@pytest.fixture(scope="module")
def hert():
    return load_yaml(specs_dir() / "hert_transaxle.yaml")


@pytest.fixture(scope="module")
def breakthrough():
    return load_yaml(specs_dir() / "breakthrough_subsystems.yaml")


def test_chassis_torsion_and_bending(chassis):
    g = chassis["golden"]
    r = chassis_run(chassis)
    assert r["t_twist_nm"] == pytest.approx(g["t_twist_nm"], rel=1e-3)
    assert r["k_theta_from_bump_nm_per_deg"] == pytest.approx(34704, rel=1e-3)
    assert r["k_theta_design_nm_per_deg"] == pytest.approx(
        g["k_theta_target_nm_per_deg"], abs=1
    )
    assert r["f_z_total_n"] == pytest.approx(g["f_z_total_n"], rel=1e-3)
    assert r["m_b_max_nm"] == pytest.approx(g["m_b_max_nm"], rel=2e-3)
    assert r["min_node_sf"] == pytest.approx(g["min_node_sf"], rel=1e-2)
    assert r["node_safety_factors"]["A"] == pytest.approx(2.05, rel=1e-2)
    assert r["node_safety_factors"]["D"] == pytest.approx(1.70, rel=1e-2)


def test_hert_cold_and_ceb(hert):
    g = hert["golden"]
    r = hert_run(hert)
    assert r["cold"]["t_out_ideal_k"] == pytest.approx(g["t2s_cold_k"], rel=5e-3)
    assert r["cold"]["delta_h_kj_kg"] == pytest.approx(g["delta_h_cold_kj_kg"], rel=5e-3)
    assert r["cold"]["power_kw"] == pytest.approx(g["cold_power_kw"], rel=1e-2)
    assert r["cold"]["power_hp"] == pytest.approx(g["cold_power_hp"], rel=2e-2)
    assert r["ceb"]["power_kw"] == pytest.approx(g["ceb_power_kw"], rel=1e-2)
    assert r["ceb"]["power_hp"] == pytest.approx(g["ceb_power_hp"], rel=2e-2)


def test_gdsa_force(hert):
    g = hert["golden"]
    r = gdsa_run(hert)
    assert r["peak_force_n"] == pytest.approx(g["shift_force_n"], rel=5e-3)
    assert r["total_shift_time_ms"] == pytest.approx(g["shift_time_ms"], abs=0.01)
    assert r["piston_area_cm2"] == pytest.approx(3.14, rel=1e-2)


def test_gear_map_splitter_drop(hert):
    g = hert["golden"]
    r = gear_run(hert, rpm_pre=8500)
    assert r["main_ratios_consistent"] is True
    assert r["ratios"]["1L"] == pytest.approx(4.3832, rel=1e-3)
    assert r["ratios"]["6H"] == pytest.approx(0.5238, rel=1e-3)
    # First splitter shift 1L→1H
    step0 = r["shift_steps"][0]
    assert step0["frm"] == "1L" and step0["to"] == "1H"
    assert step0["rpm_drop"] == pytest.approx(g["rpm_drop_splitter"], abs=5)


def test_breakthrough_ccd_and_dkis(hert, chassis, breakthrough):
    r = run_breakthrough_bundle(hert, chassis, breakthrough)
    assert "CCD" in r["features_catalog"]
    assert "CASMIR" in r["features_catalog"]
    assert "PSI" in r["features_catalog"]
    assert r["ccd"]["density_gain_pct"] == pytest.approx(8.5, rel=5e-2)
    assert r["dkis_tff"]["coupling_ratio"] == pytest.approx(14.0, rel=1e-3)
    assert r["dkis_tff"]["meets_12x_criterion"] == 1.0
