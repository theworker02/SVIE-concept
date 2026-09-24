"""HERT-12 master gear map and RPM drop calculations."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir

GEAR_ORDER = [
    "1L", "1H", "2L", "2H", "3L", "3H", "4L", "4H", "5L", "5H", "6L", "6H"
]


@dataclass(frozen=True)
class ShiftStep:
    frm: str
    to: str
    delta_r: float
    rpm_pre: float
    rpm_post: float
    rpm_drop: float


def build_ratio_table(spec: dict[str, Any]) -> dict[str, float]:
    return {k: float(v["r_total"]) for k, v in spec["twelve_speed_map"].items()}


def shift_steps(ratios: dict[str, float], rpm_pre: float = 8500.0) -> list[ShiftStep]:
    steps: list[ShiftStep] = []
    for i in range(len(GEAR_ORDER) - 1):
        a, b = GEAR_ORDER[i], GEAR_ORDER[i + 1]
        delta = ratios[a] / ratios[b]
        rpm_post = rpm_pre / delta
        steps.append(
            ShiftStep(
                frm=a,
                to=b,
                delta_r=delta,
                rpm_pre=rpm_pre,
                rpm_post=rpm_post,
                rpm_drop=rpm_pre - rpm_post,
            )
        )
    return steps


def verify_main_ratios(spec: dict[str, Any], tol: float = 2e-3) -> bool:
    for g in spec["main_gears"].values():
        expected = float(g["driven"]) / float(g["drive"])
        if abs(expected - float(g["ratio"])) > tol:
            return False
    return True


def run_from_spec(spec: dict[str, Any], rpm_pre: float = 8500.0) -> dict[str, Any]:
    ratios = build_ratio_table(spec)
    steps = [asdict(s) for s in shift_steps(ratios, rpm_pre=rpm_pre)]
    splitter_drops = [s["rpm_drop"] for s in steps if s["frm"].endswith("L")]
    return {
        "ratios": ratios,
        "final_drive": float(spec["final_drive"]["ratio"]),
        "shift_steps": steps,
        "mean_splitter_rpm_drop": sum(splitter_drops) / len(splitter_drops),
        "main_ratios_consistent": verify_main_ratios(spec),
        "meta": {"module": "gear_map"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="HERT-12 gear map / RPM drop calculator")
    parser.add_argument("--spec", default=str(specs_dir() / "hert_transaxle.yaml"))
    parser.add_argument("--rpm", type=float, default=8500.0)
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec(load_yaml(args.spec), rpm_pre=args.rpm)))


if __name__ == "__main__":
    main()
