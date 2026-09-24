"""Hydrogen DI combustion control: lambda AFR, water-DI NOx, PI strategy."""

from __future__ import annotations

import argparse
import math
from dataclasses import asdict, dataclass
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class H2CombustionResult:
    lambda_value: float
    afr_mass: float
    nox_index: float
    water_fuel_ratio: float
    nox_reduction_pct: float
    nox_index_after_water: float
    load_extension_pct: float
    pre_ignition_strategy: str


def afr_from_lambda(lambda_value: float, afr_stoich: float) -> float:
    return lambda_value * afr_stoich


def nox_index(lambda_value: float, exponent: float, baseline_at_1: float = 1.0) -> float:
    """Relative thermal NOx index — falls with lean mixture (engineering proxy)."""
    return baseline_at_1 * (1.0 / max(lambda_value, 0.5)) ** exponent


def water_di_nox_reduction(water_fuel_ratio: float, max_pct: float, k: float) -> float:
    return max_pct * (1.0 - math.exp(-k * water_fuel_ratio))


def water_di_load_extension(water_fuel_ratio: float, max_pct: float, k: float) -> float:
    # Same saturating shape, scaled to load-extension ceiling
    return max_pct * (1.0 - math.exp(-k * water_fuel_ratio))


def run_case(
    spec: dict[str, Any],
    *,
    lambda_value: float,
    water_fuel_ratio: float = 0.0,
) -> dict[str, Any]:
    stoich = spec["stoichiometry"]
    water = spec["water_direct_injection"]
    nox = spec["nox_model"]
    afr = afr_from_lambda(lambda_value, float(stoich["afr_stoich_mass"]))
    idx = nox_index(
        lambda_value,
        float(nox["lean_sensitivity_exponent"]),
        float(nox["baseline_index_at_lambda_1"]),
    )
    red = water_di_nox_reduction(
        water_fuel_ratio,
        float(water["max_nox_reduction_pct"]),
        float(water["response_k"]),
    )
    load_ext = water_di_load_extension(
        water_fuel_ratio,
        float(water["max_load_extension_pct"]),
        float(water["response_k"]),
    )
    result = H2CombustionResult(
        lambda_value=lambda_value,
        afr_mass=afr,
        nox_index=idx,
        water_fuel_ratio=water_fuel_ratio,
        nox_reduction_pct=red,
        nox_index_after_water=idx * (1.0 - red / 100.0),
        load_extension_pct=load_ext,
        pre_ignition_strategy=str(spec["pre_ignition_mitigation"]["strategy"]),
    )
    out = asdict(result)
    out["boost_bar_abs_min"] = float(
        spec["pre_ignition_mitigation"]["intake_boost_bar_abs_min"]
    )
    out["aftertreatment_lean"] = spec["aftertreatment"]["lean_path"]
    out["meta"] = {"module": "h2_combustion"}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="H2 combustion control calculator")
    parser.add_argument("--spec", default=str(specs_dir() / "h2_combustion_control.yaml"))
    parser.add_argument("--lambda", dest="lam", type=float, default=1.05)
    parser.add_argument("--water-ratio", type=float, default=0.15)
    args = parser.parse_args(argv)
    print(dumps_result(run_case(load_yaml(args.spec), lambda_value=args.lam, water_fuel_ratio=args.water_ratio)))


if __name__ == "__main__":
    main()
