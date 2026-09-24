"""Critical Tier-1 supply-chain design map."""

from __future__ import annotations

import argparse
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


def run_supply_chain(spec: dict[str, Any] | None = None) -> dict[str, Any]:
    spec = spec or load_yaml(specs_dir() / "supply_chain_tier1.yaml")
    parts = spec["critical_parts"]
    dual = sum(1 for p in parts if p.get("dual_source_target"))
    max_lead = max(int(p["lead_weeks"]) for p in parts)
    return {
        "critical_parts": len(parts),
        "max_lead_weeks": max_lead,
        "dual_source_targets": dual,
        "risks": len(spec["risks"]),
        "meta": {"module": "supply_chain", "version": "1.3.0"},
    }


def run_all() -> dict[str, Any]:
    return {
        "supply_chain": run_supply_chain(),
        "meta": {"module": "supply_chain_bundle", "version": "1.3.0"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE supply-chain map")
    parser.parse_args(argv)
    print(dumps_result(run_all()))


if __name__ == "__main__":
    main()
