"""HERT hydrogen impulse-turbine expansion (cold + CEB modes)."""

from __future__ import annotations

import argparse
import math
from dataclasses import asdict, dataclass
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir

KW_TO_HP = 1.34102


@dataclass(frozen=True)
class HertInputs:
    m_dot_kg_s: float
    p_in_pa: float
    p_out_pa: float
    t_in_k: float
    cp_j_kg_k: float
    gamma: float
    eta_cold: float
    eta_ceb: float
    t_ceb_k: float


@dataclass(frozen=True)
class ExpansionResult:
    mode: str
    t_out_ideal_k: float
    t_out_ideal_c: float
    delta_h_kj_kg: float
    power_ideal_kw: float
    power_kw: float
    power_hp: float


def _expand(t_in_k: float, inp: HertInputs, eta: float, mode: str) -> ExpansionResult:
    k = (inp.gamma - 1.0) / inp.gamma
    t_out = t_in_k * math.pow(inp.p_out_pa / inp.p_in_pa, k)
    dh = inp.cp_j_kg_k * (t_in_k - t_out)  # J/kg
    p_ideal_kw = (inp.m_dot_kg_s * dh) / 1000.0
    p_act = p_ideal_kw * eta
    return ExpansionResult(
        mode=mode,
        t_out_ideal_k=t_out,
        t_out_ideal_c=t_out - 273.15,
        delta_h_kj_kg=dh / 1000.0,
        power_ideal_kw=p_ideal_kw,
        power_kw=p_act,
        power_hp=p_act * KW_TO_HP,
    )


def compute_cold(inp: HertInputs) -> ExpansionResult:
    return _expand(inp.t_in_k, inp, inp.eta_cold, "Cold Gas Expansion")


def compute_ceb(inp: HertInputs) -> ExpansionResult:
    return _expand(inp.t_ceb_k, inp, inp.eta_ceb, "Catalytic Exothermic Boost")


def inputs_from_spec(spec: dict[str, Any]) -> HertInputs:
    t = spec["expansion_turbine_stage"]
    return HertInputs(
        m_dot_kg_s=float(t["design_mass_flow_g_s"]) / 1000.0,
        p_in_pa=float(t["inlet_pressure_bar"]) * 1e5,
        p_out_pa=float(t["outlet_pressure_bar"]) * 1e5,
        t_in_k=float(t["t_in_c"]) + 273.15,
        cp_j_kg_k=float(t["cp_kj_kg_k"]) * 1000.0,
        gamma=float(t["gamma"]),
        eta_cold=float(t["isentropic_efficiency_cold"]),
        eta_ceb=float(t["isentropic_efficiency_ceb"]),
        t_ceb_k=float(t["t_ceb_c"]) + 273.15,
    )


def run_from_spec(spec: dict[str, Any]) -> dict[str, Any]:
    inp = inputs_from_spec(spec)
    cold = compute_cold(inp)
    ceb = compute_ceb(inp)
    return {
        "cold": asdict(cold),
        "ceb": asdict(ceb),
        "meta": {"module": "hert_expansion"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="HERT turbine expansion calculator")
    parser.add_argument("--spec", default=str(specs_dir() / "hert_transaxle.yaml"))
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec(load_yaml(args.spec))))


if __name__ == "__main__":
    main()
