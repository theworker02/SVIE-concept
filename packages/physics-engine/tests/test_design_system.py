"""Vehicle design system golden tests."""

from __future__ import annotations

import pytest

from svie_physics.design_system import run_all, run_harness, run_lighting
from svie_physics.io_util import load_yaml, specs_dir


def test_design_all():
    all_ = run_all()
    assert all_["body"]["length_m"] == pytest.approx(4.52)
    assert all_["body"]["character_lines"] == 1
    assert all_["lighting"]["ok"] is True
    assert all_["cabin"]["seats"] == 2
    assert all_["packaging"]["zone_count"] == 7
    assert all_["harness"]["ok"] is True
    assert all_["system"]["render_count"] == 7


def test_harness_and_lamps():
    h = run_harness(load_yaml(specs_dir() / "wiring_harness.yaml"))
    assert h["zone_count"] == 6
    assert h["copper_km"] <= 1.8
    lamp = run_lighting(load_yaml(specs_dir() / "lighting_headlamp.yaml"))
    assert lamp["low_beam_lm"] >= 1100
