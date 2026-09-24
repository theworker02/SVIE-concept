"""Air and fuel mass-flow models for the SVIE V8 at WOT.

Formulation (4-stroke):
  cycles/s = N_rpm / 120
  V_dot_air = V_d * (N/2) * eta_v   with N in rev/s  ≡  V_d * cycles/s * eta_v
  m_dot_air = V_dot_air * rho_air
  m_dot_fuel = m_dot_air / AFR
"""

from __future__ import annotations

import argparse
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class AirFuelInputs:
    displacement_m3: float
    rpm: float
    volumetric_efficiency: float
    afr: float
    air_density_kg_m3: float
    cylinders: int = 8
    fuel_density_kg_L: float = 0.745
    lhv_kj_kg: float = 44000.0


@dataclass(frozen=True)
class AirFuelResult:
    cycles_per_s: float
    v_dot_air_m3_s: float
    m_dot_air_kg_s: float
    m_dot_air_g_s: float
    m_dot_fuel_kg_s: float
    m_dot_fuel_g_s: float
    m_dot_fuel_kg_h: float
    liquid_equiv_L_h: float
    m_dot_fuel_per_bank_g_s: float
    m_dot_per_injector_g_s: float
    mg_per_stroke: float
    e_in_kw: float


def cycles_per_second(rpm: float) -> float:
    """Four-stroke induction events per second for the whole engine."""
    return rpm / 120.0


def compute_air_fuel(inp: AirFuelInputs) -> AirFuelResult:
    cps = cycles_per_second(inp.rpm)
    v_dot = inp.displacement_m3 * cps * inp.volumetric_efficiency
    m_air = v_dot * inp.air_density_kg_m3
    m_fuel = m_air / inp.afr
    m_fuel_g_s = m_fuel * 1000.0
    m_fuel_kg_h = m_fuel * 3600.0
    liquid_L_h = m_fuel_kg_h / inp.fuel_density_kg_L
    per_injector = m_fuel_g_s / inp.cylinders
    # mg per combustion event at one cylinder: (g/s per cyl) / (cycles/s) * 1000
    mg_stroke = (per_injector / cps) * 1000.0
    e_in_kw = m_fuel * inp.lhv_kj_kg  # kJ/s = kW

    return AirFuelResult(
        cycles_per_s=cps,
        v_dot_air_m3_s=v_dot,
        m_dot_air_kg_s=m_air,
        m_dot_air_g_s=m_air * 1000.0,
        m_dot_fuel_kg_s=m_fuel,
        m_dot_fuel_g_s=m_fuel_g_s,
        m_dot_fuel_kg_h=m_fuel_kg_h,
        liquid_equiv_L_h=liquid_L_h,
        m_dot_fuel_per_bank_g_s=m_fuel_g_s / 2.0,
        m_dot_per_injector_g_s=per_injector,
        mg_per_stroke=mg_stroke,
        e_in_kw=e_in_kw,
    )


def inputs_from_spec(spec: dict[str, Any]) -> AirFuelInputs:
    geo = spec["geometry"]
    op = spec["operating_point_wot"]
    fuel = spec["fuel"]
    return AirFuelInputs(
        displacement_m3=float(geo["displacement_m3"]),
        rpm=float(op["rpm"]),
        volumetric_efficiency=float(op["volumetric_efficiency"]),
        afr=float(op["afr"]),
        air_density_kg_m3=float(op["air_density_kg_m3"]),
        cylinders=int(geo.get("cylinders", 8)),
        fuel_density_kg_L=float(fuel.get("density_liquid_kg_L", 0.745)),
        lhv_kj_kg=float(fuel["lhv_kj_kg"]),
    )


def run_from_spec_path(path: str | Path) -> dict[str, Any]:
    spec = load_yaml(path)
    result = compute_air_fuel(inputs_from_spec(spec))
    out = asdict(result)
    out["meta"] = {"module": "air_fuel", "spec": str(path)}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE air/fuel mass-flow calculator")
    parser.add_argument(
        "--spec",
        default=str(specs_dir() / "svie_v8_52L.yaml"),
        help="Path to engine YAML spec",
    )
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec_path(args.spec)))


if __name__ == "__main__":
    main()
