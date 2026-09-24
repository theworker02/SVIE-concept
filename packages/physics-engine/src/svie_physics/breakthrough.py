"""Breakthrough feature models: CCD density gain, DKIS torsion coupling."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from typing import Any

from svie_physics.hert_expansion import compute_cold, inputs_from_spec as hert_inputs
from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class CcdResult:
    t_cold_sink_k: float
    t_cold_sink_c: float
    # Ideal-gas density ratio vs ambient for cooled charge path (engineering estimate)
    density_gain_pct: float
    shaft_power_kw: float


def cryogenic_charge_densification(
    t_ambient_k: float,
    t_sink_k: float,
    shaft_power_kw: float,
    *,
    heat_exchanger_effectiveness: float = 0.55,
    target_cap_pct: float = 8.5,
) -> CcdResult:
    """Estimate intake density gain from routing charge air past HERT cold sink.

    ρ2/ρ1 ≈ T1/T2 for isobaric cooling. Effectiveness blends toward sink temperature.
    Capped at blueprint target for diligence reporting.
    """
    t_charge = t_ambient_k - heat_exchanger_effectiveness * (t_ambient_k - t_sink_k)
    # Prevent non-physical sub-cryogenic charge temps for the estimate
    t_charge = max(t_charge, 250.0)
    gain = (t_ambient_k / t_charge - 1.0) * 100.0
    gain = min(gain, target_cap_pct)
    return CcdResult(
        t_cold_sink_k=t_sink_k,
        t_cold_sink_c=t_sink_k - 273.15,
        density_gain_pct=gain,
        shaft_power_kw=shaft_power_kw,
    )


def dkis_torsion_margin(
    k_theta_nm_per_deg: float,
    k_phi_nm_per_deg: float,
) -> dict[str, float]:
    """Chassis/suspension coupling ratio — target ≥ 12 for DKIS calibration integrity."""
    ratio = k_theta_nm_per_deg / k_phi_nm_per_deg if k_phi_nm_per_deg else float("nan")
    return {
        "k_theta_nm_per_deg": k_theta_nm_per_deg,
        "k_phi_nm_per_deg": k_phi_nm_per_deg,
        "coupling_ratio": ratio,
        "meets_12x_criterion": float(ratio >= 12.0),
    }


def run_breakthrough_bundle(
    hert_spec: dict[str, Any],
    chassis_spec: dict[str, Any],
    breakthrough_spec: dict[str, Any],
) -> dict[str, Any]:
    cold = compute_cold(hert_inputs(hert_spec))
    ccd_cfg = breakthrough_spec["features"]["CCD"]["metrics"]
    ccd = cryogenic_charge_densification(
        t_ambient_k=298.15,
        t_sink_k=cold.t_out_ideal_k,
        shaft_power_kw=cold.power_kw,
        target_cap_pct=float(ccd_cfg["target_intake_density_gain_pct"]),
    )
    dkis = dkis_torsion_margin(
        k_theta_nm_per_deg=float(chassis_spec["torsion"]["design_target_nm_per_deg"]),
        k_phi_nm_per_deg=float(
            chassis_spec["suspension_roll_stiffness_nm_per_deg"]["total"]
        ),
    )
    return {
        "ccd": asdict(ccd),
        "dkis_tff": dkis,
        "features_catalog": list(breakthrough_spec["features"].keys()),
        "meta": {"module": "breakthrough"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE breakthrough feature calculator")
    parser.add_argument("--hert", default=str(specs_dir() / "hert_transaxle.yaml"))
    parser.add_argument("--chassis", default=str(specs_dir() / "chassis_monocoque.yaml"))
    parser.add_argument(
        "--breakthrough",
        default=str(specs_dir() / "breakthrough_subsystems.yaml"),
    )
    args = parser.parse_args(argv)
    print(
        dumps_result(
            run_breakthrough_bundle(
                load_yaml(args.hert),
                load_yaml(args.chassis),
                load_yaml(args.breakthrough),
            )
        )
    )


if __name__ == "__main__":
    main()
