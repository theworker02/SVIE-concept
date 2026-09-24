"""Homogeneous Equilibrium Model (HEM) choked flash-orifice sizing.

Choked when P2/P1 < critical pressure ratio (~0.54 for γ≈1.3 gases).
Cavitation parameter:
  σ_c = (P2 - P_sat) / (P1 - P_sat)
Required orifice area:
  A_o = m_dot / (C_d * G_crit)
"""

from __future__ import annotations

import argparse
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from svie_physics.air_fuel import compute_air_fuel, inputs_from_spec
from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class HemInputs:
    p1_mpa: float
    p2_mpa: float
    p_sat_mpa: float
    m_dot_kg_s: float
    g_crit_kg_m2_s: float
    cd: float = 1.0  # blueprint area uses G_crit directly with effective flux
    gamma_crit_ratio: float = 0.54


@dataclass(frozen=True)
class HemResult:
    pressure_ratio: float
    is_choked: bool
    sigma_c: float
    flash_boiling: bool
    a_o_required_m2: float
    a_o_required_mm2: float
    g_crit_kg_m2_s: float
    m_dot_kg_s: float


def cavitation_number(p1_mpa: float, p2_mpa: float, p_sat_mpa: float) -> float:
    return (p2_mpa - p_sat_mpa) / (p1_mpa - p_sat_mpa)


def compute_hem(inp: HemInputs) -> HemResult:
    pr = inp.p2_mpa / inp.p1_mpa
    choked = pr < inp.gamma_crit_ratio
    sigma = cavitation_number(inp.p1_mpa, inp.p2_mpa, inp.p_sat_mpa)
    # Blueprint: A_req = m_dot / G_crit (Cd absorbed into effective G usage)
    a_m2 = inp.m_dot_kg_s / (inp.cd * inp.g_crit_kg_m2_s)
    return HemResult(
        pressure_ratio=pr,
        is_choked=choked,
        sigma_c=sigma,
        flash_boiling=sigma < 0.0,
        a_o_required_m2=a_m2,
        a_o_required_mm2=a_m2 * 1e6,
        g_crit_kg_m2_s=inp.g_crit_kg_m2_s,
        m_dot_kg_s=inp.m_dot_kg_s,
    )


def run_coupled(
    engine_spec: dict[str, Any],
    piezo_spec: dict[str, Any],
    *,
    per_injector: bool = True,
) -> dict[str, Any]:
    af = compute_air_fuel(inputs_from_spec(engine_spec))
    m = af.m_dot_fuel_kg_s
    if per_injector:
        m = m / int(engine_spec["geometry"]["cylinders"])
    up = piezo_spec["upstream_state"]
    down = piezo_spec["downstream_state"]
    throat = piezo_spec["throat_state"]
    flow = piezo_spec["flow"]
    result = compute_hem(
        HemInputs(
            p1_mpa=float(up["p1_mpa"]),
            p2_mpa=float(down["p2_mpa"]),
            p_sat_mpa=float(throat["p_sat_mpa"]),
            m_dot_kg_s=m,
            g_crit_kg_m2_s=float(flow["g_crit_kg_m2_s"]),
            cd=1.0,
            gamma_crit_ratio=float(flow["gamma_critical_pressure_ratio"]),
        )
    )
    out = asdict(result)
    out["meta"] = {"module": "hem_choked_flow", "scope": "per_injector" if per_injector else "total"}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE HEM choked-flow orifice calculator")
    parser.add_argument("--spec", default=str(specs_dir() / "svie_v8_52L.yaml"))
    parser.add_argument("--piezo", default=str(specs_dir() / "piezo_injector.yaml"))
    args = parser.parse_args(argv)
    print(dumps_result(run_coupled(load_yaml(args.spec), load_yaml(args.piezo))))


if __name__ == "__main__":
    main()
