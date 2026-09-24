"""DEVA camless valvetrain electrical power model."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class DevaInputs:
    valves: int
    rpm: float
    energy_per_transition_j: float
    hold_power_w_per_valve: float
    hold_duty: float  # 0..1 fraction of time valves draw hold current


@dataclass(frozen=True)
class DevaResult:
    events_per_s_per_valve: float
    transition_power_kw: float
    hold_power_kw: float
    total_electrical_kw: float


def compute_deva(inp: DevaInputs) -> DevaResult:
    events = inp.rpm / 120.0
    p_trans = inp.valves * events * inp.energy_per_transition_j / 1000.0
    p_hold = inp.valves * inp.hold_power_w_per_valve * inp.hold_duty / 1000.0
    return DevaResult(
        events_per_s_per_valve=events,
        transition_power_kw=p_trans,
        hold_power_kw=p_hold,
        total_electrical_kw=p_trans + p_hold,
    )


def run_from_spec(
    spec: dict[str, Any],
    *,
    rpm: float,
    mode: str = "wot",
) -> dict[str, Any]:
    kin = spec["kinematics"]
    n = int(spec["architecture"]["valves_total"])
    if mode == "cruise":
        e = float(kin["energy_per_transition_j_cruise"])
        hold = 1.0
    else:
        e = float(kin["energy_per_transition_j_wot"])
        hold = 0.0  # PM latch holds at WOT; transitions dominate
    result = compute_deva(
        DevaInputs(
            valves=n,
            rpm=rpm,
            energy_per_transition_j=e,
            hold_power_w_per_valve=float(kin["hold_power_w_per_valve"]),
            hold_duty=hold,
        )
    )
    out = asdict(result)
    out["mode"] = mode
    out["cycle_modes"] = list(spec["cycle_modes"].keys())
    out["meta"] = {"module": "deva_power"}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="DEVA electrical power calculator")
    parser.add_argument("--spec", default=str(specs_dir() / "deva_valvetrain.yaml"))
    parser.add_argument("--rpm", type=float, default=8500.0)
    parser.add_argument("--mode", choices=["wot", "cruise"], default="wot")
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec(load_yaml(args.spec), rpm=args.rpm, mode=args.mode)))


if __name__ == "__main__":
    main()
