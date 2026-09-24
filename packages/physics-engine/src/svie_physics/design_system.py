"""Vehicle design system — body, lighting, cabin, packaging, harness KPIs."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_body(spec: dict[str, Any]) -> dict[str, Any]:
    v = spec["vehicle"]
    return {
        "length_m": float(v["length_m"]),
        "height_m": float(v["height_m"]),
        "cd_closed": float(v["cd_drs_closed"]),
        "character_lines": int(spec["surfaces"]["character_lines"]),
        "meta": {"module": "body_exterior"},
    }


def run_lighting(spec: dict[str, Any]) -> dict[str, Any]:
    p = spec["photometry"]
    return {
        "low_beam_lm": float(p["low_beam_lm"]),
        "power_w": float(p["power_both_drl_low_w"]),
        "ok": float(p["low_beam_lm"]) >= float(p["min_low_beam_lm"])
        and float(p["power_both_drl_low_w"]) <= float(p["max_power_w"]),
        "modules_vertical": 4,
        "meta": {"module": "lighting"},
    }


def run_cabin(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "seats": int(spec["occupancy"]["seats"]),
        "cluster_in": float(spec["hmi"]["cluster_in"]),
        "toggles": bool(spec["hmi"]["physical_toggles"]),
        "meta": {"module": "cabin"},
    }


def run_packaging(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "zone_count": len(spec["zones"]),
        "frunk_l": float(next(z["volume_l"] for z in spec["zones"] if z["id"] == "Z1")),
        "weight_front": float(spec["balance"]["weight_dist_front"]),
        "meta": {"module": "packaging"},
    }


def run_harness(spec: dict[str, Any]) -> dict[str, Any]:
    b = spec["budgets"]
    return {
        "zone_count": len(spec["zones"]),
        "copper_km": float(b["copper_length_km"]),
        "mass_kg": float(b["mass_kg"]),
        "bus_count": len(spec["buses"]),
        "ok": float(b["copper_length_km"]) <= float(b["max_copper_km"])
        and float(b["mass_kg"]) <= float(b["max_mass_kg"]),
        "meta": {"module": "wiring_harness"},
    }


def run_design_rollup(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "design_system.yaml")
    return {
        "render_count": len(spec["renders"]),
        "token_count": len(spec["tokens"]),
        "tokens": spec["tokens"],
        "meta": {"module": "design_system", "version": "1.3.0"},
    }


def run_all() -> dict[str, Any]:
    root = specs_dir()
    return {
        "body": run_body(load_yaml(root / "body_exterior.yaml")),
        "lighting": run_lighting(load_yaml(root / "lighting_headlamp.yaml")),
        "cabin": run_cabin(load_yaml(root / "cabin_layout.yaml")),
        "packaging": run_packaging(load_yaml(root / "packaging_layout.yaml")),
        "harness": run_harness(load_yaml(root / "wiring_harness.yaml")),
        "system": run_design_rollup(),
        "meta": {"module": "design_system", "version": "1.3.0"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE vehicle design system")
    parser.parse_args(argv)
    print(dumps_result(run_all()))


if __name__ == "__main__":
    main()
