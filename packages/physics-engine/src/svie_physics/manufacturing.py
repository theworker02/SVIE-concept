"""Manufacturing master rollup — routes, cells, capacity."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_manufacturing(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "manufacturing_master.yaml")
    engine = spec["engine_routes"]
    body = spec["body_routes"]
    trans = spec["transmission_routes"]
    routes = list(engine.keys()) + list(trans.keys()) + list(body.keys())
    return {
        "annual_units": int(spec["meta"]["annual_units_assumption"]),
        "ptwa_mm": float(engine["block"]["ptwa_thickness_mm"]),
        "route_keys": sorted(routes),
        "route_count": len(routes),
        "cell_count": len(spec["cells"]),
        "cells": [c["id"] for c in spec["cells"]],
        "philosophy": spec["philosophy"],
        "meta": {"module": "manufacturing", "version": "1.3.0"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE manufacturing master rollup")
    parser.parse_args(argv)
    print(dumps_result(run_manufacturing()))


if __name__ == "__main__":
    main()
