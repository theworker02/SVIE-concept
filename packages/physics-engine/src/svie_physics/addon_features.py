"""Add-on features wave — dry sump, pulse EGR, silk mounts, range bridge, KERS."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_dry_sump(spec: dict[str, Any]) -> dict[str, Any]:
    s = spec["scavenge"]
    return {
        "stages": int(s["stages"]),
        "flow_l_min": float(s["pump_flow_l_min_at_10k"]),
        "crankcase_kpa": float(s["crankcase_pressure_kpa"]),
        "feeds_oil_spine": bool(spec["integration"]["feeds_oil_spine"]),
        "ok": float(s["pump_flow_l_min_at_10k"]) >= float(s["min_flow_l_min"]),
        "meta": {"module": "dry_sump_x"},
    }


def run_pulse_egr(spec: dict[str, Any]) -> dict[str, Any]:
    c = spec["cruise_lean"]
    return {
        "egr_frac": float(c["egr_mass_frac"]),
        "nox_reduction_frac": float(c["nox_reduction_frac"]),
        "pulse_hz": float(c["pulse_hz"]),
        "cooler_effectiveness": float(c["cooler_effectiveness"]),
        "meta": {"module": "pulse_egr"},
    }


def run_silk_mount(spec: dict[str, Any]) -> dict[str, Any]:
    gain = float(spec["active"]["isolation_db_at_idle"]) - float(
        spec["passive"]["isolation_db_at_idle"]
    )
    return {
        "isolation_db": float(spec["active"]["isolation_db_at_idle"]),
        "isolation_gain_db": round(gain, 1),
        "power_w": float(spec["active"]["nexus_power_w"]),
        "bandwidth_hz": float(spec["active"]["bandwidth_hz"]),
        "meta": {"module": "silk_mount"},
    }


def run_range_bridge(spec: dict[str, Any]) -> dict[str, Any]:
    s = spec["series_mode"]
    dc = float(s["engine_kw_cruise"]) * float(s["generator_eta"])
    return {
        "engine_kw": float(s["engine_kw_cruise"]),
        "generator_eta": float(s["generator_eta"]),
        "dc_bus_kw": round(dc, 2),
        "battery_buffer_kwh": float(s["battery_buffer_kwh"]),
        "meta": {"module": "range_bridge"},
    }


def run_kers_blend(spec: dict[str, Any]) -> dict[str, Any]:
    e = spec["event"]
    captured = float(e["recoverable_kj"]) * float(e["blend_capture_frac"])
    return {
        "captured_kj": round(captured, 1),
        "capture_frac": float(e["blend_capture_frac"]),
        "motor_kw": float(e["motor_peak_kw"]),
        "fade_compensation": bool(e["fade_compensation"]),
        "meta": {"module": "kers_blend"},
    }


def run_all() -> dict[str, Any]:
    root = specs_dir()
    return {
        "dry_sump_x": run_dry_sump(load_yaml(root / "dry_sump_x.yaml")),
        "pulse_egr": run_pulse_egr(load_yaml(root / "pulse_egr.yaml")),
        "silk_mount": run_silk_mount(load_yaml(root / "silk_mount.yaml")),
        "range_bridge": run_range_bridge(load_yaml(root / "range_bridge.yaml")),
        "kers_blend": run_kers_blend(load_yaml(root / "kers_blend.yaml")),
        "meta": {"module": "addon_features", "version": "1.4.0"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE addon features")
    parser.parse_args(argv)
    print(dumps_result(run_all()))


if __name__ == "__main__":
    main()
