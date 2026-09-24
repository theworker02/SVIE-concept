"""BOM cost rollup for hybrid-AM SVIE-V8-HR diligence envelope."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_from_spec(spec: dict[str, Any], *, include_chassis: bool = False) -> dict[str, Any]:
    items = {k: float(v) for k, v in spec["line_items_usd"].items()}
    chassis = items.pop("chassis_monocoque_share", 0.0)
    subtotal = sum(items.values())
    total = subtotal + (chassis if include_chassis else 0.0)
    return {
        "currency": spec["meta"]["currency"],
        "volume_assumption_upy": spec["meta"]["volume_assumption_units_per_year"],
        "line_items_usd": items,
        "powertrain_subtotal_usd": subtotal,
        "chassis_share_usd": chassis,
        "total_usd": total,
        "include_chassis": include_chassis,
        "disclaimer": spec["meta"]["disclaimer"],
        "meta": {"module": "bom_cost"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE BOM cost envelope")
    parser.add_argument("--spec", default=str(specs_dir() / "bom_cost_estimate.yaml"))
    parser.add_argument("--with-chassis", action="store_true")
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec(load_yaml(args.spec), include_chassis=args.with_chassis)))


if __name__ == "__main__":
    main()
