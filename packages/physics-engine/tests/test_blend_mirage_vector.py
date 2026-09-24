"""Tests for BLEND, MIRAGE, VECTOR."""

from __future__ import annotations

import pytest

from svie_physics.blend_mirage_vector import mirage_step_response, run_blend, run_mirage, run_vector
from svie_physics.io_util import load_yaml, specs_dir


def test_blend_force_and_hole():
    spec = load_yaml(specs_dir() / "blend_brake.yaml")
    g = spec["golden"]
    r = run_blend(spec)
    assert r["shift_ms"] == g["shift_ms"]
    assert r["continuity_window_ms"] == g["continuity_window_ms"]
    assert r["target_brake_force_n"] == pytest.approx(g["target_brake_force_n"], rel=1e-3)
    assert r["hole_reduction_factor"] == pytest.approx(150 / 4.0, abs=0.1)


def test_mirage_tau_and_nodes():
    spec = load_yaml(specs_dir() / "mirage_twin.yaml")
    r = run_mirage(spec, t_s=12.0)
    assert r["node_count"] == spec["golden"]["node_count"]
    inj = next(n for n in r["nodes"] if n["id"] == "injector_boss")
    # At t=τ, response is 63.2% of the way from T0 to Tinf
    t0, t_inf, tau = 90.0, 140.0 - 8.0, 12.0
    expected = mirage_step_response(12.0, t0, t_inf, tau)
    assert inj["temp_c_at_t"] == pytest.approx(expected, abs=0.05)
    assert inj["headroom_c"] > 0


def test_vector_domains():
    spec = load_yaml(specs_dir() / "vector_hcp.yaml")
    r = run_vector(spec)
    assert r["domain_count"] == spec["golden"]["domain_count"]
    assert r["cycle_ms"] == spec["golden"]["cycle_ms"]
    assert "AXIOM_HERT" in r["domains"]
    assert "SENTINEL" in r["domains"]
