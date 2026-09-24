"""Acquisition production-readiness scorecard, deal structure, and data-room index."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir
from svie_physics.inventory import build_inventory


def weighted_score(spec: dict[str, Any]) -> float:
    dims = spec["dimensions"]
    total_w = sum(float(d["weight"]) for d in dims)
    if total_w <= 0:
        return 0.0
    return sum(float(d["weight"]) * float(d["score"]) for d in dims) / total_w


def run_readiness(spec: dict[str, Any] | None = None, inv: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "acquisition_readiness.yaml")
    inv = inv or build_inventory()
    score = weighted_score(spec)
    gates = spec["gates"]
    counts = inv["counts"]
    gate_results = {
        "score": score >= float(gates["min_weighted_score"]),
        "specs": counts["specs_yaml"] >= int(gates["min_specs"]),
        "tests": counts["test_files"] >= int(gates["min_test_files"]),
        "packages": counts["licensing_packages"] >= int(gates["min_licensing_packages"]),
        "routes": counts["portal_routes"] >= int(gates["min_portal_routes"]),
    }
    gates_pass = all(gate_results.values())
    return {
        "weighted_score": round(score, 2),
        "dimension_count": len(spec["dimensions"]),
        "gates_pass": gates_pass,
        "gate_results": gate_results,
        "hardware_trl_ceiling": int(gates["hardware_trl_ceiling"]),
        "package_claim": gates["package_trl_claim"],
        "production_ready_acquisition": gates_pass and score >= 85,
        "meta": {"module": "acquisition_readiness", "version": "1.3.0"},
    }


def run_deal(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "deal_structure.yaml")
    preferred = next(s for s in spec["structures"] if s.get("preferred"))
    return {
        "structures": len(spec["structures"]),
        "preferred_structure": preferred["id"],
        "escrow": bool(spec["escrow"]["source_code_escrow"]),
        "earnout_gates": len(spec["earnout_gates"]),
        "nda_required": bool(spec["nda_required"]),
        "meta": {"module": "deal_structure"},
    }


def run_data_room(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "data_room_index.yaml")
    return {
        "folders": len(spec["folders"]),
        "access_tiers": len(spec["access_tiers"]),
        "term_sheet_present": any(
            "TERM-SHEET" in item for f in spec["folders"] for item in f["items"]
        ),
        "meta": {"module": "data_room_index"},
    }


def run_all() -> dict[str, Any]:
    readiness = run_readiness()
    return {
        "readiness": readiness,
        "deal": run_deal(),
        "data_room": run_data_room(),
        "meta": {"module": "acquisition_suite", "version": "1.3.0"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE acquisition readiness suite")
    parser.parse_args(argv)
    print(dumps_result(run_all()))


if __name__ == "__main__":
    main()
