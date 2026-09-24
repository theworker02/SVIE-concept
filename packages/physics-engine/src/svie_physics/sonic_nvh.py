"""SONIC flat-plane secondary vibration index and pulse spacing."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def secondary_index(stroke_mm: float, ref_stroke_mm: float = 93.0) -> float:
    """Second-order shake scales roughly with stroke² at equal reciprocating mass."""
    return (stroke_mm / ref_stroke_mm) ** 2


def run_from_spec(spec: dict[str, Any]) -> dict[str, Any]:
    nvh = spec["nvh_mitigation"]
    stroke = float(nvh["short_stroke_mm"])
    idx = secondary_index(stroke)
    return {
        "pulse_spacing_deg": float(spec["firing"]["exhaust_pulse_spacing_deg"]),
        "mean_piston_speed_m_s": float(nvh["mean_piston_speed_at_10k_m_s"]),
        "secondary_index_vs_93mm_stroke": idx,
        "reduction_pct_vs_gt350_stroke_class": (1.0 - idx) * 100.0,
        "aether": spec["aether_exhaust"]["name"],
        "meta": {"module": "sonic_nvh"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SONIC flat-plane NVH metrics")
    parser.add_argument("--spec", default=str(specs_dir() / "sonic_nvh.yaml"))
    args = parser.parse_args(argv)
    print(dumps_result(run_from_spec(load_yaml(args.spec))))


if __name__ == "__main__":
    main()
