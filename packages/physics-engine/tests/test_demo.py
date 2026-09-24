"""Demo program smoke test for acquisition walkthrough."""

from __future__ import annotations

import pytest

from svie_physics.demo import build_steps, main


def test_demo_steps_shape():
    steps = build_steps()
    assert len(steps) == 6
    assert steps[0].metrics["m_dot_fuel_g_s"] == pytest.approx(28.28, rel=1e-3)
    assert steps[1].metrics["q_hex_kw"] == pytest.approx(23.2, abs=0.05)
    assert steps[3].metrics["rubber_band_index"] == 0
    assert steps[4].metrics["current_trl"] == 3
    assert steps[5].metrics["production_ready_acquisition"] is True


def test_demo_main_exit_zero(capsys):
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "SVIE DEMO" in out
    assert "28.28" in out


def test_demo_json(capsys):
    assert main(["--json"]) == 0
    out = capsys.readouterr().out
    assert '"version": "1.3.0"' in out
    assert "01-sfv-wot" in out
    assert "06-acquire" in out
