"""Exhaust-counterflow heat exchanger duty for supercritical fuel heating.

  Q_HEX = m_dot_fuel * delta_h_total
  recovery_ratio = Q_HEX / E_exhaust
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from svie_physics.air_fuel import compute_air_fuel, inputs_from_spec
from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class HexInputs:
    m_dot_fuel_kg_s: float
    delta_h_total_kj_kg: float
    delta_h_sensible_kj_kg: float
    delta_h_phase_kj_kg: float
    e_in_kw: float
    exhaust_fraction: float
    banks: int = 2
    bank_surface_area_m2: float = 0.14


@dataclass(frozen=True)
class HexResult:
    delta_h_total_kj_kg: float
    q_hex_kw: float
    q_hex_per_bank_kw: float
    combined_surface_area_m2: float
    exhaust_energy_kw: float
    exhaust_recovery_ratio: float
    brake_power_kw: float
    coolant_kw: float


def compute_heat_exchanger(inp: HexInputs) -> HexResult:
    q_hex = inp.m_dot_fuel_kg_s * inp.delta_h_total_kj_kg
    exhaust_kw = inp.e_in_kw * inp.exhaust_fraction
    # Match blueprint thermal breakdown when e_in is known
    brake_frac = 0.42
    coolant_frac = 0.28
    return HexResult(
        delta_h_total_kj_kg=inp.delta_h_total_kj_kg,
        q_hex_kw=q_hex,
        q_hex_per_bank_kw=q_hex / inp.banks,
        combined_surface_area_m2=inp.bank_surface_area_m2 * inp.banks,
        exhaust_energy_kw=exhaust_kw,
        exhaust_recovery_ratio=q_hex / exhaust_kw if exhaust_kw else float("nan"),
        brake_power_kw=inp.e_in_kw * brake_frac,
        coolant_kw=inp.e_in_kw * coolant_frac,
    )


def run_coupled(
    engine_spec: dict[str, Any],
    sfv_spec: dict[str, Any],
) -> dict[str, Any]:
    af = compute_air_fuel(inputs_from_spec(engine_spec))
    hex_cfg = sfv_spec["heat_exchanger"]
    breakdown = engine_spec["thermal_breakdown_fraction"]
    result = compute_heat_exchanger(
        HexInputs(
            m_dot_fuel_kg_s=af.m_dot_fuel_kg_s,
            delta_h_total_kj_kg=float(hex_cfg["delta_h_total_kj_kg"]),
            delta_h_sensible_kj_kg=float(hex_cfg["delta_h_sensible_kj_kg"]),
            delta_h_phase_kj_kg=float(hex_cfg["delta_h_phase_kj_kg"]),
            e_in_kw=af.e_in_kw,
            exhaust_fraction=float(breakdown["exhaust"]),
            banks=int(engine_spec["geometry"].get("banks", 2)),
            bank_surface_area_m2=float(hex_cfg["bank_surface_area_m2"]),
        )
    )
    out = asdict(result)
    out["m_dot_fuel_kg_s"] = af.m_dot_fuel_kg_s
    out["e_in_kw"] = af.e_in_kw
    out["meta"] = {"module": "heat_exchanger"}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE heat-exchanger duty calculator")
    parser.add_argument("--spec", default=str(specs_dir() / "svie_v8_52L.yaml"))
    parser.add_argument("--sfv", default=str(specs_dir() / "sfv_fuel_system.yaml"))
    args = parser.parse_args(argv)
    out = run_coupled(load_yaml(args.spec), load_yaml(args.sfv))
    print(dumps_result(out))


if __name__ == "__main__":
    main()
