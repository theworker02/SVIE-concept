"""Tests for CVT comparison and AXIOM / e:HEV bridge."""

from __future__ import annotations

import pytest

from svie_physics.axiom_drive import run_axiom, run_bridge
from svie_physics.cvt_comparison import run_from_specs
from svie_physics.io_util import load_yaml, specs_dir


@pytest.fixture(scope="module")
def evidence():
    return load_yaml(specs_dir() / "cvt_evidence.yaml")


@pytest.fixture(scope="module")
def axiom():
    return load_yaml(specs_dir() / "axiom_drive.yaml")


@pytest.fixture(scope="module")
def bridge():
    return load_yaml(specs_dir() / "ehe_v_bridge.yaml")


def test_cvt_vs_hert_delta(evidence, axiom):
    g = evidence["golden"]
    r = run_from_specs(evidence, axiom, shaft_in_kw=100.0)
    assert r["cvt_eta"] == pytest.approx(g["eta_cvt_cycle"], abs=1e-6)
    assert r["hert_eta"] == pytest.approx(g["eta_hert"], abs=1e-6)
    assert r["delta_out_kw"] == pytest.approx(100.0 * (g["eta_hert"] - g["eta_cvt_cycle"]), abs=0.05)
    assert r["delta_parasitic_kw"] == pytest.approx(g["delta_parasitic_kw"], abs=0.05)
    assert r["rubber_band_index_axiom"] == 0.0
    assert r["torque_ceiling_advantage_nm"] > 400
    assert "HR-V-21-047" in r["honda_field_cases"]
    assert any("dog-clutch" in x.lower() or "12-speed" in x.lower() for x in r["honda_rd_gaps"])


def test_axiom_kills_rubber_band(axiom):
    r = run_axiom(axiom)
    assert r["rubber_band_index"] == 0.0
    assert r["shift_ms"] == pytest.approx(4.0)
    assert r["mech_efficiency"] >= 0.96


def test_ehe_v_bridge_no_belt(bridge):
    r = run_bridge(bridge)
    assert r["no_belt"] is True
    assert r["engine_direct_eta"] == pytest.approx(0.965)
    assert "metal pushing V-belt" in r["removes"]
