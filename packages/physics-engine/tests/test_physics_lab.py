"""Physics lab golden / sweep tests."""

from __future__ import annotations

import pytest

from svie_physics.physics_lab import compute_point, run_sweep, run_wot_anchor


def test_wot_anchor_near_golden():
    p = run_wot_anchor()
    # Coupled lab should stay near locked WOT design envelope
    assert p["m_dot_fuel_g_s"] == pytest.approx(28.28, rel=0.08)
    assert p["brake_power_kw"] == pytest.approx(522, rel=0.12)
    assert p["bte"] == pytest.approx(0.42, abs=0.02)
    assert p["eta_v"] == pytest.approx(1.05, abs=0.01)
    assert p["choked_orifice_ok"] is True


def test_sweep_and_maps():
    s = run_sweep(points=20)
    assert len(s["series"]) == 20
    assert s["peak_power_kw"] > 200
    low = compute_point(rpm=2000, afr=16.2, load=1.0)
    high = compute_point(rpm=8500, afr=16.2, load=1.0)
    assert high["brake_power_kw"] > low["brake_power_kw"]
    lean = compute_point(rpm=8500, afr=20.0, load=1.0)
    assert lean["bte"] < high["bte"]
    cold = compute_point(rpm=8500, afr=16.2, temp_c=-10)
    hot = compute_point(rpm=8500, afr=16.2, temp_c=40)
    assert cold["m_dot_air_kg_s"] > hot["m_dot_air_kg_s"]
