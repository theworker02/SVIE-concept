"""Validation harness + addon feature golden tests."""

from __future__ import annotations

import pytest

from svie_physics.addon_features import (
    run_all,
    run_dry_sump,
    run_kers_blend,
    run_pulse_egr,
    run_range_bridge,
    run_silk_mount,
)
from svie_physics.io_util import load_yaml, specs_dir
from svie_physics.validate import main as validate_main
from svie_physics.validate import run_validation


def test_validation_all_ok():
    r = run_validation()
    assert r["all_ok"] is True
    assert r["passed"] == r["total"]
    assert r["total"] >= 6


def test_validate_cli(capsys):
    assert validate_main([]) == 0
    out = capsys.readouterr().out
    assert "SVIE VALIDATE" in out
    assert "OK" in out


def test_dry_sump_and_egr():
    ds = run_dry_sump(load_yaml(specs_dir() / "dry_sump_x.yaml"))
    assert ds["ok"] is True
    assert ds["stages"] == 3
    egr = run_pulse_egr(load_yaml(specs_dir() / "pulse_egr.yaml"))
    assert egr["nox_reduction_frac"] == pytest.approx(0.42)
    assert egr["egr_frac"] <= 0.25


def test_silk_range_kers():
    silk = run_silk_mount(load_yaml(specs_dir() / "silk_mount.yaml"))
    assert silk["isolation_gain_db"] == pytest.approx(10.0)
    rb = run_range_bridge(load_yaml(specs_dir() / "range_bridge.yaml"))
    assert rb["dc_bus_kw"] == pytest.approx(51.15, rel=1e-3)
    kers = run_kers_blend(load_yaml(specs_dir() / "kers_blend.yaml"))
    assert kers["captured_kj"] == pytest.approx(111.6, rel=1e-3)


def test_addon_bundle_keys():
    all_ = run_all()
    assert set(all_) >= {
        "dry_sump_x",
        "pulse_egr",
        "silk_mount",
        "range_bridge",
        "kers_blend",
    }
