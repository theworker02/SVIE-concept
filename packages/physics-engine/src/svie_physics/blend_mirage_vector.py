"""BLEND brake fill + MIRAGE thermal ROM + VECTOR HCP reporters."""

from __future__ import annotations

import argparse
import math
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir

G = 9.81


def run_blend(spec: dict[str, Any]) -> dict[str, Any]:
    d = spec["decel_model"]
    t = spec["timing"]
    force = float(d["vehicle_mass_kg"]) * float(d["target_decel_g"]) * G
    return {
        "shift_ms": float(t["gdsa_shift_ms"]),
        "continuity_window_ms": float(t["total_decel_continuity_window_ms"]),
        "target_brake_force_n": force,
        "vs_typical_amt_shift_hole_ms": float(spec["golden"]["vs_typical_amt_shift_hole_ms"]),
        "hole_reduction_factor": float(spec["golden"]["vs_typical_amt_shift_hole_ms"])
        / float(t["gdsa_shift_ms"]),
        "meta": {"module": "blend_brake"},
    }


def mirage_step_response(
    t_s: float,
    t0_c: float,
    t_inf_c: float,
    tau_s: float,
) -> float:
    return t_inf_c + (t0_c - t_inf_c) * math.exp(-t_s / tau_s)


def run_mirage(spec: dict[str, Any], *, t_s: float = 12.0) -> dict[str, Any]:
    nodes = []
    for n in spec["nodes"]:
        # Example: ambient 90 → approach limit under load
        t0 = 90.0
        t_inf = float(n["limit_c"]) - float(spec["control"]["derate_margin_c"])
        temp = mirage_step_response(t_s, t0, t_inf, float(n["tau_s"]))
        nodes.append(
            {
                "id": n["id"],
                "tau_s": float(n["tau_s"]),
                "limit_c": float(n["limit_c"]),
                "temp_c_at_t": temp,
                "headroom_c": float(n["limit_c"]) - temp,
            }
        )
    return {
        "t_s": t_s,
        "update_hz": float(spec["control"]["update_hz"]),
        "node_count": len(nodes),
        "nodes": nodes,
        "meta": {"module": "mirage_twin"},
    }


def run_vector(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "domain_count": len(spec["domains"]),
        "domains": spec["domains"],
        "cycle_ms": float(spec["cycle_time_ms"]),
        "failsafe": spec["failsafe"],
        "meta": {"module": "vector_hcp"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="BLEND / MIRAGE / VECTOR")
    parser.add_argument("--which", choices=["blend", "mirage", "vector", "all"], default="all")
    parser.add_argument("--t", type=float, default=12.0, help="MIRAGE time horizon seconds")
    args = parser.parse_args(argv)
    out: dict[str, Any] = {}
    if args.which in ("blend", "all"):
        out["blend"] = run_blend(load_yaml(specs_dir() / "blend_brake.yaml"))
    if args.which in ("mirage", "all"):
        out["mirage"] = run_mirage(load_yaml(specs_dir() / "mirage_twin.yaml"), t_s=args.t)
    if args.which in ("vector", "all"):
        out["vector"] = run_vector(load_yaml(specs_dir() / "vector_hcp.yaml"))
    print(dumps_result(out))


if __name__ == "__main__":
    main()
