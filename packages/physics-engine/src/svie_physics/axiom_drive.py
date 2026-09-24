"""AXIOM drive KPIs and e:HEV bridge beltless check."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_axiom(spec: dict[str, Any]) -> dict[str, Any]:
    p = spec["performance_claims"]
    return {
        "name": spec["meta"]["name"],
        "mech_efficiency": float(p["mech_efficiency"]),
        "shift_ms": float(p["shift_ms"]),
        "max_input_nm": float(p["max_input_nm"]),
        "rubber_band_index": float(p["rubber_band_index"]),
        "vs_s_plus": spec["comparison_to_honda_s_plus"],
        "meta": {"module": "axiom_drive"},
    }


def run_bridge(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": spec["meta"]["name"],
        "removes": spec["architecture"]["removes"],
        "modes": spec["architecture"]["modes"],
        "engine_direct_eta": float(spec["efficiency_targets"]["engine_direct_path_eta"]),
        "no_belt": "metal pushing V-belt" in spec["architecture"]["removes"],
        "meta": {"module": "ehe_v_bridge"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="AXIOM / e:HEV bridge reporter")
    parser.add_argument("--which", choices=["axiom", "bridge", "both"], default="both")
    args = parser.parse_args(argv)
    out: dict[str, Any] = {}
    if args.which in ("axiom", "both"):
        out["axiom"] = run_axiom(load_yaml(specs_dir() / "axiom_drive.yaml"))
    if args.which in ("bridge", "both"):
        out["bridge"] = run_bridge(load_yaml(specs_dir() / "ehe_v_bridge.yaml"))
    print(dumps_result(out))


if __name__ == "__main__":
    main()
