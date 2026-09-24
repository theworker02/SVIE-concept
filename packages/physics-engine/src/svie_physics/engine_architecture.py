"""High-RPM SVIE-V8-HR architecture metrics (Honda K/B-evolved H2 DI).

Computes displacement, rod-to-stroke, mean piston speed, and relative
side-load reduction vs B16 (1.74) and short-rod (1.32) baselines.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import asdict, dataclass
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class ArchitectureInputs:
    bore_mm: float
    stroke_mm: float
    rod_length_mm: float
    cylinders: int
    rpm: float
    reference_rod_to_stroke: float = 1.74
    short_rod_to_stroke: float = 1.32


@dataclass(frozen=True)
class ArchitectureResult:
    displacement_cc: float
    displacement_l: float
    rod_to_stroke: float
    mean_piston_speed_m_s: float
    side_load_index: float
    reference_side_load_index: float
    side_load_reduction_pct_vs_b16: float
    side_load_reduction_pct: float


def displacement_cc(bore_mm: float, stroke_mm: float, cylinders: int) -> float:
    return cylinders * math.pi * (bore_mm / 2.0) ** 2 * stroke_mm / 1000.0


def mean_piston_speed_m_s(stroke_mm: float, rpm: float) -> float:
    return 2.0 * (stroke_mm / 1000.0) * rpm / 60.0


def side_load_index(stroke_mm: float, rod_mm: float) -> float:
    """First-order obliquity proxy: max sin(φ) ≈ S/(2R)."""
    return (stroke_mm / 2.0) / rod_mm


def compute_architecture(inp: ArchitectureInputs) -> ArchitectureResult:
    disp = displacement_cc(inp.bore_mm, inp.stroke_mm, inp.cylinders)
    r_s = inp.rod_length_mm / inp.stroke_mm
    mps = mean_piston_speed_m_s(inp.stroke_mm, inp.rpm)
    sli = side_load_index(inp.stroke_mm, inp.rod_length_mm)
    ref_rod = inp.reference_rod_to_stroke * inp.stroke_mm
    sli_ref = side_load_index(inp.stroke_mm, ref_rod)
    short_rod = inp.short_rod_to_stroke * inp.stroke_mm
    sli_short = side_load_index(inp.stroke_mm, short_rod)
    return ArchitectureResult(
        displacement_cc=disp,
        displacement_l=disp / 1000.0,
        rod_to_stroke=r_s,
        mean_piston_speed_m_s=mps,
        side_load_index=sli,
        reference_side_load_index=sli_ref,
        side_load_reduction_pct_vs_b16=(1.0 - sli / sli_ref) * 100.0,
        side_load_reduction_pct=(1.0 - sli / sli_short) * 100.0,
    )


def run_from_spec(spec: dict[str, Any], rpm: float | None = None) -> dict[str, Any]:
    geo = spec["geometry"]
    bottom = spec["bottom_end"]
    b16 = spec.get("b16_reference", {})
    result = compute_architecture(
        ArchitectureInputs(
            bore_mm=float(geo["bore_mm"]),
            stroke_mm=float(geo["stroke_mm"]),
            rod_length_mm=float(geo["rod_length_mm"]),
            cylinders=int(geo["cylinders"]),
            rpm=float(rpm if rpm is not None else bottom["target_redline_rpm"]),
            reference_rod_to_stroke=float(b16.get("rod_to_stroke", 1.74)),
            short_rod_to_stroke=1.32,
        )
    )
    out = asdict(result)
    out["ptwa_weight_save_lb"] = float(bottom["ptwa_weight_save_lb"])
    out["compression_ratio"] = float(spec["valvetrain_head"]["compression_ratio"])
    out["chamber_volume_cc"] = float(spec["valvetrain_head"]["chamber_volume_cc"])
    out["manufacturing"] = {
        "block": spec["manufacturing"]["block"]["method"],
        "head": spec["manufacturing"]["head"]["method"],
        "head_material": spec["manufacturing"]["head"]["material"],
    }
    out["meta"] = {"module": "engine_architecture", "id": spec["meta"]["id"]}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE-V8-HR architecture calculator")
    parser.add_argument("--spec", default=str(specs_dir() / "svie_v8_hr_357.yaml"))
    parser.add_argument("--rpm", type=float, default=None)
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec(load_yaml(args.spec), rpm=args.rpm)))


if __name__ == "__main__":
    main()
