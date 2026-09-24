"""CHRONOS cold-start timeline and SENTINEL / TRL reporters."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_chronos(spec: dict[str, Any]) -> dict[str, Any]:
    phases = spec["phases"]
    timed = [p for p in phases if float(p["duration_s"]) > 0]
    cumulative = 0.0
    timeline = []
    for p in timed:
        cumulative += float(p["duration_s"])
        timeline.append({"id": p["id"], "ends_s": cumulative, "actions": p["actions"]})
    return {
        "phase_count": len(phases),
        "time_to_first_fire_s": float(spec["totals"]["time_to_first_fire_s"]),
        "time_to_aftertreatment_active_s": float(spec["totals"]["time_to_aftertreatment_active_s"]),
        "timeline": timeline,
        "meta": {"module": "chronos"},
    }


def run_sentinel(spec: dict[str, Any]) -> dict[str, Any]:
    s = spec["sensing"]
    return {
        "sensors_total": int(s["cabin_h2_sensors"]) + int(s["underhood_h2_sensors"]) + int(s["tank_ae_channels"]),
        "isolation_ms": float(s["isolation_time_ms"]),
        "lel_threshold_pct": float(s["leak_threshold_pct_lel"]),
        "meta": {"module": "sentinel"},
    }


def run_trl(spec: dict[str, Any]) -> dict[str, Any]:
    current = next(s for s in spec["stages"] if s["status"] == "complete_in_repo")
    return {
        "current_trl": int(current["trl"]),
        "current_name": current["name"],
        "stages": len(spec["stages"]),
        "licensing_packages": spec["licensing_packages"],
        "meta": {"module": "trl_roadmap"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="CHRONOS / SENTINEL / TRL")
    parser.add_argument("--which", choices=["chronos", "sentinel", "trl", "all"], default="all")
    args = parser.parse_args(argv)
    out: dict[str, Any] = {}
    if args.which in ("chronos", "all"):
        out["chronos"] = run_chronos(load_yaml(specs_dir() / "chronos_cold_start.yaml"))
    if args.which in ("sentinel", "all"):
        out["sentinel"] = run_sentinel(load_yaml(specs_dir() / "sentinel_safety.yaml"))
    if args.which in ("trl", "all"):
        out["trl"] = run_trl(load_yaml(specs_dir() / "trl_roadmap.yaml"))
    print(dumps_result(out))


if __name__ == "__main__":
    main()
