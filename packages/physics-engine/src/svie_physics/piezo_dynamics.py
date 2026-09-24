"""Piezoelectric pintle stroke, orifice area, and acoustic pressure ripple.

  Δz = d33 * n_layers * V
  A_o = π * D_pintle * Δz * sin(θ_seat)
  ΔP_acoustic ≈ ρ * c * ω * δz
"""

from __future__ import annotations

import argparse
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class PiezoInputs:
    diameter_m: float
    d33_m_per_v: float
    n_layers: int
    seat_angle_deg: float
    voltage_v: float
    density_kg_m3: float
    speed_of_sound_m_s: float
    piezo_freq_hz: float
    acoustic_amplitude_m: float


@dataclass(frozen=True)
class PiezoResult:
    delta_z_m: float
    delta_z_um: float
    a_o_m2: float
    a_o_mm2: float
    omega_rad_s: float
    delta_p_acoustic_mpa: float
    delta_p_acoustic_bar: float


def compute_piezo(inp: PiezoInputs) -> PiezoResult:
    delta_z = inp.d33_m_per_v * inp.n_layers * inp.voltage_v
    theta = math.radians(inp.seat_angle_deg)
    a_o = math.pi * inp.diameter_m * delta_z * math.sin(theta)
    omega = 2.0 * math.pi * inp.piezo_freq_hz
    dp_pa = (
        inp.density_kg_m3
        * inp.speed_of_sound_m_s
        * omega
        * inp.acoustic_amplitude_m
    )
    dp_mpa = dp_pa / 1e6
    return PiezoResult(
        delta_z_m=delta_z,
        delta_z_um=delta_z * 1e6,
        a_o_m2=a_o,
        a_o_mm2=a_o * 1e6,
        omega_rad_s=omega,
        delta_p_acoustic_mpa=dp_mpa,
        delta_p_acoustic_bar=dp_mpa * 10.0,
    )


def inputs_from_spec(spec: dict[str, Any]) -> PiezoInputs:
    p = spec["pintle"]
    up = spec["upstream_state"]
    return PiezoInputs(
        diameter_m=float(p["diameter_m"]),
        d33_m_per_v=float(p["d33_m_per_v"]),
        n_layers=int(p["n_layers"]),
        seat_angle_deg=float(p["seat_angle_deg"]),
        voltage_v=float(p["v_max"]),
        density_kg_m3=float(up["density_kg_m3"]),
        speed_of_sound_m_s=float(up["speed_of_sound_m_s"]),
        piezo_freq_hz=float(p["piezo_freq_hz"]),
        acoustic_amplitude_m=float(p["acoustic_amplitude_m"]),
    )


def run_from_spec(spec: dict[str, Any]) -> dict[str, Any]:
    result = compute_piezo(inputs_from_spec(spec))
    out = asdict(result)
    out["meta"] = {"module": "piezo_dynamics"}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE piezo pintle / orifice calculator")
    parser.add_argument("--piezo", default=str(specs_dir() / "piezo_injector.yaml"))
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec(load_yaml(args.piezo))))


if __name__ == "__main__":
    main()
