"""NEXUS-48 electrical budget vs DEVA draw."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.deva_power import run_from_spec as deva_run
from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_nexus(
    nexus: dict[str, Any],
    *,
    rpm: float = 8500.0,
    mode: str = "wot",
) -> dict[str, Any]:
    budget = nexus["energy_budget_wot_8500"]
    # Live DEVA draw when rpm/mode provided
    deva = deva_run(load_yaml(specs_dir() / "deva_valvetrain.yaml"), rpm=rpm, mode=mode)
    aux = float(budget["auxiliaries_kw"])
    total = float(deva["total_electrical_kw"]) + aux
    available = float(nexus["topology"]["bsg_continuous_kw"])
    return {
        "voltage_v": float(nexus["topology"]["voltage_v"]),
        "battery_kwh": float(nexus["topology"]["battery_kwh"]),
        "deva_kw": float(deva["total_electrical_kw"]),
        "auxiliaries_kw": aux,
        "total_draw_kw": total,
        "bsg_available_kw": available,
        "margin_kw": available - total,
        "feeds_ok": available >= total,
        "topology": nexus["topology"]["machine_position"],
        "meta": {"module": "nexus_48"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="NEXUS-48 electrical budget")
    parser.add_argument("--spec", default=str(specs_dir() / "nexus_48.yaml"))
    parser.add_argument("--rpm", type=float, default=8500.0)
    parser.add_argument("--mode", choices=["wot", "cruise"], default="wot")
    args = parser.parse_args(argv)
    print(dumps_result(run_nexus(load_yaml(args.spec), rpm=args.rpm, mode=args.mode)))


if __name__ == "__main__":
    main()
