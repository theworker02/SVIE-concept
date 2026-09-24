"""Resonant energy-recovery piezo driver sizing (GaN half-bridge).

  E_c = 1/2 * C_p * V^2
  P_raw = C_p * V^2 * f_s
  t_r = π √(L_r C_p)  →  L_r = t_r² / (π² C_p)
  I_peak = V_bus * √(C_p / L_r)
"""

from __future__ import annotations

import argparse
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class DriverInputs:
    capacitance_f: float
    v_max: float
    f_s_hz: float
    slew_time_s: float
    bus_voltage_v: float
    n_injectors: int = 8
    recovery_efficiency: float = 0.875


@dataclass(frozen=True)
class DriverResult:
    e_c_j: float
    e_c_mj: float
    p_raw_w: float
    p_total_w: float
    l_r_h: float
    l_r_uh: float
    i_peak_a: float
    p_dissipated_estimate_w: float


def compute_driver(inp: DriverInputs) -> DriverResult:
    e_c = 0.5 * inp.capacitance_f * inp.v_max**2
    # Non-resonant average power = energy per cycle × frequency (½ C V² f)
    p_raw = e_c * inp.f_s_hz
    l_r = (inp.slew_time_s**2) / (math.pi**2 * inp.capacitance_f)
    i_peak = inp.bus_voltage_v * math.sqrt(inp.capacitance_f / l_r)
    # Recovered fraction leaves residual dissipation
    p_diss = p_raw * (1.0 - inp.recovery_efficiency)
    return DriverResult(
        e_c_j=e_c,
        e_c_mj=e_c * 1000.0,
        p_raw_w=p_raw,
        p_total_w=p_raw * inp.n_injectors,
        l_r_h=l_r,
        l_r_uh=l_r * 1e6,
        i_peak_a=i_peak,
        p_dissipated_estimate_w=p_diss,
    )


def inputs_from_spec(spec: dict[str, Any], n_injectors: int = 8) -> DriverInputs:
    d = spec["driver"]
    return DriverInputs(
        capacitance_f=float(d["capacitance_f"]),
        v_max=float(d["v_max"]),
        f_s_hz=float(d["f_s_hz"]),
        slew_time_s=float(d["slew_time_s"]),
        bus_voltage_v=float(d["bus_voltage_v"]),
        n_injectors=n_injectors,
        recovery_efficiency=float(d.get("recovery_efficiency", 0.875)),
    )


def run_from_spec(spec: dict[str, Any], n_injectors: int = 8) -> dict[str, Any]:
    result = compute_driver(inputs_from_spec(spec, n_injectors=n_injectors))
    out = asdict(result)
    out["meta"] = {"module": "piezo_driver"}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE resonant piezo driver calculator")
    parser.add_argument("--piezo", default=str(specs_dir() / "piezo_injector.yaml"))
    parser.add_argument("--injectors", type=int, default=8)
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec(load_yaml(args.piezo), n_injectors=args.injectors)))


if __name__ == "__main__":
    main()
