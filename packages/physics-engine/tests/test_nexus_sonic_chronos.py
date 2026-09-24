"""Tests for NEXUS-48, SONIC, CHRONOS, SENTINEL, TRL."""

from __future__ import annotations

import pytest

from svie_physics.chronos_sentinel import run_chronos, run_sentinel, run_trl
from svie_physics.io_util import load_yaml, specs_dir
from svie_physics.nexus_48 import run_nexus
from svie_physics.sonic_nvh import run_from_spec as sonic_run, secondary_index


def test_nexus_covers_deva():
    nexus = load_yaml(specs_dir() / "nexus_48.yaml")
    g = nexus["golden"]
    r = run_nexus(nexus, rpm=8500, mode="wot")
    assert r["total_draw_kw"] == pytest.approx(g["total_draw_wot_kw"], rel=2e-2)
    assert r["margin_kw"] == pytest.approx(g["margin_kw"], abs=0.15)
    assert r["feeds_ok"] is True
    assert r["voltage_v"] == 48


def test_sonic_secondary_vs_gt350_stroke():
    spec = load_yaml(specs_dir() / "sonic_nvh.yaml")
    g = spec["golden"]
    r = sonic_run(spec)
    assert r["pulse_spacing_deg"] == g["pulse_spacing_deg"]
    assert r["secondary_index_vs_93mm_stroke"] == pytest.approx(
        g["secondary_index_vs_93mm_stroke"], abs=0.01
    )
    assert secondary_index(75.0, 93.0) == pytest.approx((75 / 93) ** 2)


def test_chronos_sentinel_trl():
    chronos = load_yaml(specs_dir() / "chronos_cold_start.yaml")
    sentinel = load_yaml(specs_dir() / "sentinel_safety.yaml")
    trl = load_yaml(specs_dir() / "trl_roadmap.yaml")
    c = run_chronos(chronos)
    s = run_sentinel(sentinel)
    t = run_trl(trl)
    assert c["time_to_first_fire_s"] == pytest.approx(chronos["golden"]["time_to_first_fire_s"])
    assert c["time_to_aftertreatment_active_s"] == pytest.approx(chronos["golden"]["time_to_aft_s"])
    assert s["isolation_ms"] == sentinel["golden"]["isolation_ms"]
    assert s["sensors_total"] == sentinel["golden"]["sensors_total"]
    assert t["current_trl"] == trl["golden"]["current_trl"]
    assert t["stages"] == trl["golden"]["stages"]
