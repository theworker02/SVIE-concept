"""Platform next-wave features — engine, transmission, body KPIs from YAML."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_cryo_rail(spec: dict[str, Any]) -> dict[str, Any]:
    unbuf = float(spec["rail"]["unbuffered_delta_t_k"])
    target = float(spec["rail"]["target_delta_t_k"])
    pulse = float(spec["step_load"]["heat_pulse_kj"])
    latent = float(spec["pcm"]["latent_kj_kg"]) * float(spec["pcm"]["mass_kg"])
    # Effectiveness: fraction of unbuffered swing removed
    effectiveness = (unbuf - target) / unbuf
    droop = float(spec["rail"]["pressure_droop_mpa"])
    return {
        "delta_t_k": target,
        "buffer_effectiveness": round(effectiveness, 3),
        "pressure_droop_mpa": round(droop, 3),
        "pcm_capacity_kj": round(latent, 1),
        "heat_pulse_kj": pulse,
        "within_max_droop": droop <= float(spec["rail"]["pressure_droop_mpa_max"]),
        "meta": {"module": "cryo_rail"},
    }


def run_ring_zero(spec: dict[str, Any]) -> dict[str, Any]:
    base = float(spec["baseline"]["fmep_bar"])
    rz = float(spec["ring_zero"]["fmep_bar"])
    delta = (rz - base) / base
    return {
        "fmep_bar": rz,
        "fmep_delta_frac": round(delta, 4),
        "oil_index": float(spec["ring_zero"]["oil_consumption_index"]),
        "ptwa_bore_mm": float(spec["ring_zero"]["ptwa_bore_mm"]),
        "meta": {"module": "ring_zero"},
    }


def run_oil_spine(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "pressure_bar": float(spec["gallery"]["pressure_bar_at_10k"]),
        "jet_l_min": float(spec["gallery"]["jet_flow_l_min_per_piston"]),
        "stiffness_gain": float(spec["stiffness"]["spine_bending_gain_frac"]),
        "meets_pressure": float(spec["gallery"]["pressure_bar_at_10k"])
        >= float(spec["gallery"]["min_pressure_bar"]),
        "meta": {"module": "oil_spine"},
    }


def run_aether_ign(spec: dict[str, Any]) -> dict[str, Any]:
    spark = float(spec["spark_only"]["lean_limit_lambda"])
    plasma = float(spec["plasma_assist"]["lean_limit_lambda"])
    return {
        "lean_limit_lambda": plasma,
        "lean_extension_lambda": round(plasma - spark, 2),
        "energy_mj": float(spec["plasma_assist"]["energy_mj"]),
        "meta": {"module": "aether_ign"},
    }


def run_flux_shift(spec: dict[str, Any]) -> dict[str, Any]:
    s = spec["shift"]
    return {
        "interrupt_ms": float(s["torque_interrupt_ms"]),
        "overlap_kj": float(s["overlap_kj"]),
        "rubber_band_index": float(s["rubber_band_index"]),
        "within_gate": float(s["torque_interrupt_ms"]) <= float(s["max_interrupt_ms"]),
        "meta": {"module": "flux_shift"},
    }


def run_gear_mesh_am(spec: dict[str, Any]) -> dict[str, Any]:
    solid_m = float(spec["solid_carrier"]["mass_kg"])
    lat_m = float(spec["lattice"]["mass_kg"])
    solid_h = float(spec["solid_carrier"]["mesh_harmonic_amp"])
    lat_h = float(spec["lattice"]["mesh_harmonic_amp"])
    return {
        "mass_delta_frac": round((lat_m - solid_m) / solid_m, 4),
        "harmonic_delta_frac": round((lat_h - solid_h) / solid_h, 4),
        "fatigue_sf": float(spec["lattice"]["fatigue_sf"]),
        "meta": {"module": "gear_mesh_am"},
    }


def run_jet_bearing(spec: dict[str, Any]) -> dict[str, Any]:
    j = spec["jet"]
    return {
        "velocity_m_s": float(j["velocity_m_s"]),
        "delta_t_k": float(j["bearing_delta_t_k"]),
        "sigma": float(j["cavitation_sigma"]),
        "ok": float(j["velocity_m_s"]) >= float(j["min_velocity_m_s"])
        and float(j["bearing_delta_t_k"]) <= float(j["max_delta_t_k"]),
        "meta": {"module": "jet_bearing"},
    }


def run_node_cast(spec: dict[str, Any]) -> dict[str, Any]:
    t = float(spec["structure"]["torsion_nm_per_deg"])
    prior = float(spec["structure"]["prior_target_nm_per_deg"])
    return {
        "torsion_nm_per_deg": t,
        "torsion_gain_frac": round((t - prior) / prior, 4),
        "node_sf": float(spec["structure"]["node_safety_factor"]),
        "meta": {"module": "node_cast"},
    }


def run_aero_skin(spec: dict[str, Any]) -> dict[str, Any]:
    a = spec["at_200_kmh"]
    return {
        "delta_downforce_n": float(a["delta_downforce_n"]),
        "delta_cd": float(a["delta_cd"]),
        "actuation_ms": float(a["actuation_ms"]),
        "meta": {"module": "aero_skin"},
    }


def run_cell_vault(spec: dict[str, Any]) -> dict[str, Any]:
    v = spec["vault"]
    return {
        "energy_kj": float(v["absorbed_energy_kj"]),
        "intrusion_m": float(v["intrusion_m"]),
        "mass_kg": float(v["mass_kg"]),
        "ok": float(v["absorbed_energy_kj"]) >= float(v["min_energy_kj"]),
        "meta": {"module": "cell_vault"},
    }


def run_thermal_skin(spec: dict[str, Any]) -> dict[str, Any]:
    c = spec["cruise"]
    return {
        "rejection_kw": float(c["extra_rejection_kw"]),
        "surface_delta_t_k": float(c["surface_delta_t_k"]),
        "mass_kg": float(c["mass_penalty_kg"]),
        "meta": {"module": "thermal_skin"},
    }


def run_engine_bundle() -> dict[str, Any]:
    root = specs_dir()
    return {
        "cryo_rail": run_cryo_rail(load_yaml(root / "engine_cryo_rail.yaml")),
        "ring_zero": run_ring_zero(load_yaml(root / "ring_zero.yaml")),
        "oil_spine": run_oil_spine(load_yaml(root / "oil_spine.yaml")),
        "aether_ign": run_aether_ign(load_yaml(root / "aether_ign.yaml")),
    }


def run_transmission_bundle() -> dict[str, Any]:
    root = specs_dir()
    return {
        "flux_shift": run_flux_shift(load_yaml(root / "flux_shift.yaml")),
        "gear_mesh_am": run_gear_mesh_am(load_yaml(root / "gear_mesh_am.yaml")),
        "jet_bearing": run_jet_bearing(load_yaml(root / "jet_bearing.yaml")),
    }


def run_body_bundle() -> dict[str, Any]:
    root = specs_dir()
    return {
        "node_cast": run_node_cast(load_yaml(root / "node_cast_body.yaml")),
        "aero_skin": run_aero_skin(load_yaml(root / "aero_skin.yaml")),
        "cell_vault": run_cell_vault(load_yaml(root / "cell_vault.yaml")),
        "thermal_skin": run_thermal_skin(load_yaml(root / "thermal_skin.yaml")),
    }


def run_all() -> dict[str, Any]:
    return {
        "engine": run_engine_bundle(),
        "transmission": run_transmission_bundle(),
        "body": run_body_bundle(),
        "meta": {"module": "platform_features", "version": "1.3.0"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE platform next-wave features")
    parser.add_argument(
        "--domain",
        choices=["engine", "transmission", "body", "all"],
        default="all",
    )
    args = parser.parse_args(argv)
    if args.domain == "engine":
        out = run_engine_bundle()
    elif args.domain == "transmission":
        out = run_transmission_bundle()
    elif args.domain == "body":
        out = run_body_bundle()
    else:
        out = run_all()
    print(dumps_result(out))


if __name__ == "__main__":
    main()
