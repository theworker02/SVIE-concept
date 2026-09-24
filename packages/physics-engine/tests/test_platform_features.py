"""Golden tests for platform next-wave + manufacturing."""

from __future__ import annotations

import pytest

from svie_physics.io_util import load_yaml, specs_dir
from svie_physics.manufacturing import run_manufacturing
from svie_physics.platform_features import (
    run_aether_ign,
    run_aero_skin,
    run_all,
    run_cell_vault,
    run_cryo_rail,
    run_flux_shift,
    run_gear_mesh_am,
    run_jet_bearing,
    run_node_cast,
    run_oil_spine,
    run_ring_zero,
    run_thermal_skin,
)


def test_cryo_rail():
    g = load_yaml(specs_dir() / "engine_cryo_rail.yaml")["golden"]
    r = run_cryo_rail(load_yaml(specs_dir() / "engine_cryo_rail.yaml"))
    assert r["delta_t_k"] == pytest.approx(g["delta_t_k"])
    assert r["buffer_effectiveness"] == pytest.approx(g["buffer_effectiveness"], rel=2e-2)
    assert r["pressure_droop_mpa"] == pytest.approx(g["pressure_droop_mpa"], rel=5e-2)


def test_ring_zero():
    g = load_yaml(specs_dir() / "ring_zero.yaml")["golden"]
    r = run_ring_zero(load_yaml(specs_dir() / "ring_zero.yaml"))
    assert r["fmep_delta_frac"] == pytest.approx(g["fmep_delta_frac"], abs=1e-3)
    assert r["oil_index"] == pytest.approx(g["oil_index"])


def test_oil_spine_and_aether():
    os_ = run_oil_spine(load_yaml(specs_dir() / "oil_spine.yaml"))
    assert os_["pressure_bar"] >= 4.5
    assert os_["jet_l_min"] >= 1.2
    ae = run_aether_ign(load_yaml(specs_dir() / "aether_ign.yaml"))
    assert ae["lean_extension_lambda"] == pytest.approx(0.3)


def test_transmission_wave():
    fx = run_flux_shift(load_yaml(specs_dir() / "flux_shift.yaml"))
    assert fx["interrupt_ms"] <= 8.0
    assert fx["rubber_band_index"] == 0
    gm = run_gear_mesh_am(load_yaml(specs_dir() / "gear_mesh_am.yaml"))
    assert gm["mass_delta_frac"] == pytest.approx(-0.18, abs=1e-3)
    assert gm["harmonic_delta_frac"] == pytest.approx(-0.25, abs=1e-3)
    jb = run_jet_bearing(load_yaml(specs_dir() / "jet_bearing.yaml"))
    assert jb["ok"] is True


def test_body_wave():
    nc = run_node_cast(load_yaml(specs_dir() / "node_cast_body.yaml"))
    assert nc["torsion_nm_per_deg"] == 38000
    assert nc["node_sf"] >= 1.8
    aero = run_aero_skin(load_yaml(specs_dir() / "aero_skin.yaml"))
    assert aero["delta_downforce_n"] == 420
    cv = run_cell_vault(load_yaml(specs_dir() / "cell_vault.yaml"))
    assert cv["ok"] is True
    ts = run_thermal_skin(load_yaml(specs_dir() / "thermal_skin.yaml"))
    assert ts["rejection_kw"] == pytest.approx(1.8)


def test_manufacturing_master():
    r = run_manufacturing()
    assert r["annual_units"] == 5000
    assert r["ptwa_mm"] == pytest.approx(0.15)
    assert r["cell_count"] == 5
    assert r["route_count"] == 15


def test_platform_all_keys():
    all_ = run_all()
    assert set(all_["engine"]) == {"cryo_rail", "ring_zero", "oil_spine", "aether_ign"}
    assert set(all_["transmission"]) == {"flux_shift", "gear_mesh_am", "jet_bearing"}
    assert set(all_["body"]) == {"node_cast", "aero_skin", "cell_vault", "thermal_skin"}
