"""AETHER-OS and analog HMI golden tests."""

from __future__ import annotations

import pytest

from svie_physics.aether_os import run_all, run_analog_hmi, run_carplay_ultra


def test_aether_bundle():
    all_ = run_all()
    assert all_["aether_os"]["analog_primacy"] is True
    assert all_["aether_os"]["max_screens"] == 1
    assert all_["aether_os"]["door_screens"] == 0
    assert all_["aether_os"]["center_in"] == pytest.approx(10.25)
    assert all_["aether_os"]["modules"] == 6
    assert all_["carplay_ultra"]["physical_wins"] is True
    assert all_["carplay_ultra"]["door_screens"] == 0
    assert all_["carplay_ultra"]["theme_tokens"] == 3
    assert all_["analog_hmi"]["screens_in_stack"] == 0
    assert all_["analog_hmi"]["physical_controls"] == 13


def test_carplay_and_analog_specs():
    ultra = run_carplay_ultra()
    assert ultra["wireless"] is True
    assert ultra["oem_theme"] is True
    hmi = run_analog_hmi()
    assert hmi["gauges"] == 4
    assert hmi["rotaries"] == 4
