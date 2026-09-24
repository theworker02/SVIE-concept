"""Homologation, ISO 26262, ISO 21434, OTA, and durability design packages."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_homologation(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "homologation_path.yaml")
    return {
        "markets": len(spec["markets"]),
        "fuels": len(spec["fuels"]),
        "blockers": len(spec["blockers_today"]),
        "path_documented": True,
        "meta": {"module": "homologation"},
    }


def run_iso26262(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "iso26262_sentinel.yaml")
    asil_rank = {"QM": 0, "A": 1, "B": 2, "C": 3, "D": 4}
    max_asil = max(spec["items"], key=lambda i: asil_rank.get(i["asil_target"], 0))["asil_target"]
    return {
        "items": len(spec["items"]),
        "max_asil": max_asil,
        "certificate": bool(spec["process"]["certificate"]),
        "draft_ready": spec["process"]["hara_status"].startswith("draft"),
        "meta": {"module": "iso26262"},
    }


def run_iso21434(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "iso21434_aether.yaml")
    return {
        "threats": len(spec["threats"]),
        "zones": len(spec["zones"]),
        "certificate": bool(spec["certificate"]),
        "guest_untrusted": "phone_untrusted" in spec["zones"],
        "meta": {"module": "iso21434"},
    }


def run_ota(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "ota_fleet_policy.yaml")
    return {
        "signed_only": bool(spec["rules"]["signed_only"]),
        "rollback": bool(spec["rules"]["rollback_required"]),
        "channels": len(spec["channels"]),
        "forbidden": len(spec["forbidden"]),
        "meta": {"module": "ota_fleet"},
    }


def run_durability(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "durability_gate.yaml")
    g3 = next(g for g in spec["gates"] if g["id"] == "G3_mule")
    return {
        "gates": len(spec["gates"]),
        "environments": len(spec["environments"]),
        "g3_hours": int(g3["hours"]),
        "meta": {"module": "durability"},
    }


def run_all() -> dict[str, Any]:
    return {
        "homologation": run_homologation(),
        "iso26262": run_iso26262(),
        "iso21434": run_iso21434(),
        "ota": run_ota(),
        "durability": run_durability(),
        "meta": {"module": "compliance", "version": "1.3.0"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE compliance design packages")
    parser.parse_args(argv)
    print(dumps_result(run_all()))


if __name__ == "__main__":
    main()
