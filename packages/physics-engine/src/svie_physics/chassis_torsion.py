"""Chassis torsional rigidity, bump twist, and bending load cases."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class ChassisInputs:
    track_m: float
    wheelbase_m: float
    f_static_total_n: float
    f_bump_front_n: float
    k_phi_total_nm_per_deg: float
    coupling_multiplier: float
    theta_max_deg: float
    venturi_total_n: float
    vertical_g: float


@dataclass(frozen=True)
class ChassisResult:
    t_twist_nm: float
    k_theta_min_coupling_nm_per_deg: float
    k_theta_from_bump_nm_per_deg: float
    k_theta_design_nm_per_deg: float
    f_z_total_n: float
    m_b_max_nm: float


def compute_chassis(inp: ChassisInputs) -> ChassisResult:
    t_twist = inp.f_bump_front_n * (inp.track_m / 2.0)
    k_coup = inp.coupling_multiplier * inp.k_phi_total_nm_per_deg
    k_bump = t_twist / inp.theta_max_deg
    # Design target: round up bump-derived value to nearest 1000 (blueprint 35,000)
    k_design = max(k_coup, k_bump)
    k_design = float(int((k_design + 999) // 1000 * 1000))
    f_z = inp.vertical_g * inp.f_static_total_n + inp.venturi_total_n
    m_b = (f_z * inp.wheelbase_m) / 8.0
    return ChassisResult(
        t_twist_nm=t_twist,
        k_theta_min_coupling_nm_per_deg=k_coup,
        k_theta_from_bump_nm_per_deg=k_bump,
        k_theta_design_nm_per_deg=k_design,
        f_z_total_n=f_z,
        m_b_max_nm=m_b,
    )


def node_safety_factors(spec: dict[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    for key, node in spec["nodes"].items():
        out[key] = float(node["limit_mpa"]) / float(node["peak_stress_mpa"])
    return out


def run_from_spec(spec: dict[str, Any]) -> dict[str, Any]:
    v = spec["vehicle"]
    bump = spec["bump"]
    roll = spec["suspension_roll_stiffness_nm_per_deg"]
    vent = spec["venturi_downforce_n"]
    axle = spec["axle_loads_1g_n"]
    tor = spec["torsion"]
    bend = spec["bending"]
    result = compute_chassis(
        ChassisInputs(
            track_m=float(v["track_m"]),
            wheelbase_m=float(v["wheelbase_m"]),
            f_static_total_n=float(axle["total"]),
            f_bump_front_n=float(bump["front_single_wheel_n"]),
            k_phi_total_nm_per_deg=float(roll["total"]),
            coupling_multiplier=float(tor["coupling_multiplier_min"]),
            theta_max_deg=float(tor["theta_max_deg"]),
            venturi_total_n=float(vent["total"]),
            vertical_g=float(bend["vertical_g"]),
        )
    )
    out = asdict(result)
    sfs = node_safety_factors(spec)
    out["node_safety_factors"] = sfs
    out["min_node_sf"] = min(sfs.values())
    out["meta"] = {"module": "chassis_torsion"}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE chassis torsion / bending calculator")
    parser.add_argument("--spec", default=str(specs_dir() / "chassis_monocoque.yaml"))
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec(load_yaml(args.spec))))


if __name__ == "__main__":
    main()
