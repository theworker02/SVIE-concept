"""AETHER-OS / analog HMI / CarPlay Ultra policy models."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_aether_os(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "aether_os.yaml")
    return {
        "analog_primacy": bool(spec["philosophy"]["analog_primacy"]),
        "max_screens": int(spec["philosophy"]["max_primary_screens"]),
        "center_in": float(spec["displays"]["center_glass_in"]),
        "modules": len(spec["modules"]),
        "door_screens": int(spec["displays"]["door_screens"]),
        "retractable_cover": bool(spec["glass"]["retractable_cover"]),
        "meta": {"module": "aether_os"},
    }


def run_carplay_ultra(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "carplay_ultra.yaml")
    theme_colors = [k for k in ("field", "accent", "caption") if k in spec.get("theme", {})]
    return {
        "door_screens": 0 if not spec["surfaces"]["door_panels"] else 1,
        "physical_wins": spec["conflict_policy"] == "physical_wins",
        "wireless": bool(spec["requirements"]["wireless"]),
        "theme_tokens": len(theme_colors),
        "oem_theme": bool(spec["theme"]["oem_look_and_feel"]),
        "meta": {"module": "carplay_ultra"},
    }


def run_analog_hmi(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "analog_hmi.yaml")
    c = spec["counts"]
    physical = c["gauges"] + c["rotaries"] + c["toggles"] + c["rollers"]
    return {
        "gauges": int(c["gauges"]),
        "rotaries": int(c["rotaries"]),
        "toggles": int(c["toggles"]),
        "physical_controls": physical,
        "screens_in_stack": 0,
        "meta": {"module": "analog_hmi"},
    }


def run_all() -> dict[str, Any]:
    return {
        "aether_os": run_aether_os(),
        "carplay_ultra": run_carplay_ultra(),
        "analog_hmi": run_analog_hmi(),
        "meta": {"module": "aether_os_bundle", "version": "1.3.0"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="AETHER-OS / CarPlay Ultra / analog HMI")
    parser.parse_args(argv)
    print(dumps_result(run_all()))


if __name__ == "__main__":
    main()
