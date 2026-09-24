"""Gas-Dynamic Shift Actuation (GDSA) force and timing."""

from __future__ import annotations

import argparse
import math
from dataclasses import asdict, dataclass
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class GdsaInputs:
    supply_pressure_pa: float
    piston_bore_m: float
    stroke_m: float
    total_shift_time_ms: float


@dataclass(frozen=True)
class GdsaResult:
    piston_area_m2: float
    piston_area_cm2: float
    peak_force_n: float
    stroke_mm: float
    total_shift_time_ms: float
    work_per_shift_j: float


def compute_gdsa(inp: GdsaInputs) -> GdsaResult:
    area = math.pi * (inp.piston_bore_m / 2.0) ** 2
    force = inp.supply_pressure_pa * area
    work = force * inp.stroke_m
    return GdsaResult(
        piston_area_m2=area,
        piston_area_cm2=area * 1e4,
        peak_force_n=force,
        stroke_mm=inp.stroke_m * 1000.0,
        total_shift_time_ms=inp.total_shift_time_ms,
        work_per_shift_j=work,
    )


def run_from_spec(spec: dict[str, Any]) -> dict[str, Any]:
    g = spec["gdsa_actuation_system"]
    result = compute_gdsa(
        GdsaInputs(
            supply_pressure_pa=float(g["supply_pressure_bar"]) * 1e5,
            piston_bore_m=float(g["piston_bore_mm"]) / 1000.0,
            stroke_m=float(g["stroke_mm"]) / 1000.0,
            total_shift_time_ms=float(g["total_shift_time_ms"]),
        )
    )
    out = asdict(result)
    out["meta"] = {"module": "gdsa_shift"}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="HERT GDSA shift force calculator")
    parser.add_argument("--spec", default=str(specs_dir() / "hert_transaxle.yaml"))
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec(load_yaml(args.spec))))


if __name__ == "__main__":
    main()
