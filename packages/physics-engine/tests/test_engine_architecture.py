"""Golden tests for SVIE-V8-HR high-RPM architecture."""

from __future__ import annotations

import pytest

from svie_physics.engine_architecture import (
    ArchitectureInputs,
    compute_architecture,
    displacement_cc,
    mean_piston_speed_m_s,
    run_from_spec,
)
from svie_physics.io_util import load_yaml, specs_dir


@pytest.fixture(scope="module")
def hr():
    return load_yaml(specs_dir() / "svie_v8_hr_357.yaml")


def test_displacement_formula():
    # Exact π formula → 3566.8 cc; blueprint rounds to 3567.3
    assert displacement_cc(87.0, 75.0, 8) == pytest.approx(3566.8, abs=0.05)
    assert displacement_cc(87.0, 75.0, 8) == pytest.approx(3567.3, abs=1.0)


def test_mean_piston_speed_10000():
    assert mean_piston_speed_m_s(75.0, 10000.0) == pytest.approx(25.0, abs=1e-9)


def test_hr_architecture_golden(hr):
    g = hr["golden"]
    r = run_from_spec(hr)
    assert r["displacement_cc"] == pytest.approx(g["displacement_cc"], abs=0.05)
    assert r["displacement_cc"] == pytest.approx(g["displacement_cc_published"], abs=1.0)
    assert r["rod_to_stroke"] == pytest.approx(g["rod_to_stroke"], abs=1e-3)
    assert r["mean_piston_speed_m_s"] == pytest.approx(g["mps_10000_m_s"], abs=1e-6)
    assert r["side_load_reduction_pct"] == pytest.approx(
        g["side_load_reduction_pct"], abs=0.5
    )
    assert r["ptwa_weight_save_lb"] == pytest.approx(g["ptwa_save_lb"], abs=0.01)
    assert r["compression_ratio"] == pytest.approx(g["compression_ratio"], abs=1e-6)


def test_side_load_vs_b16_and_short_rod():
    r = compute_architecture(
        ArchitectureInputs(
            bore_mm=87.0,
            stroke_mm=75.0,
            rod_length_mm=138.0,
            cylinders=8,
            rpm=10000.0,
            reference_rod_to_stroke=1.74,
            short_rod_to_stroke=1.32,
        )
    )
    assert r.side_load_reduction_pct_vs_b16 == pytest.approx(5.435, abs=0.05)
    assert r.side_load_reduction_pct == pytest.approx(28.26, abs=0.1)
