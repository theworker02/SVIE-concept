"""
SVIE guided demo program — walk the acquisition diligence path in one terminal.

Usage:
  python -m svie_physics.demo
  python -m svie_physics.demo --json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from typing import Any

from svie_physics.air_fuel import compute_air_fuel, inputs_from_spec
from svie_physics.acquisition_suite import run_all as acquisition_all
from svie_physics.axiom_drive import run_axiom, run_bridge
from svie_physics.chronos_sentinel import run_trl
from svie_physics.heat_exchanger import run_coupled as hex_coupled
from svie_physics.hem_choked_flow import run_coupled as hem_coupled
from svie_physics.io_util import load_yaml, specs_dir

__version__ = "1.3.0"


@dataclass
class DemoStep:
    id: str
    title: str
    summary: str
    metrics: dict[str, Any]
    module: str


def build_steps() -> list[DemoStep]:
    root = specs_dir()
    engine = load_yaml(root / "svie_v8_52L.yaml")
    sfv = load_yaml(root / "sfv_fuel_system.yaml")
    piezo = load_yaml(root / "piezo_injector.yaml")
    axiom = load_yaml(root / "axiom_drive.yaml")
    bridge = load_yaml(root / "ehe_v_bridge.yaml")
    trl = load_yaml(root / "trl_roadmap.yaml")

    af = compute_air_fuel(inputs_from_spec(engine))
    hex_r = hex_coupled(engine, sfv)
    hem_r = hem_coupled(engine, piezo)
    ax = run_axiom(axiom)
    br = run_bridge(bridge)
    trl_r = run_trl(trl)
    acq = acquisition_all()
    g_engine = engine["golden"]
    g_sfv = sfv["golden"]
    g_piezo = piezo["golden"]

    return [
        DemoStep(
            id="01-sfv-wot",
            title="SFV — WOT air/fuel baseline",
            summary="Supercritical flash fuel delivery sized at wide-open throttle.",
            metrics={
                "m_dot_fuel_g_s": g_engine["m_dot_fuel_g_s"],
                "m_dot_fuel_g_s_computed": round(af.m_dot_fuel_g_s, 4),
                "m_dot_air_kg_s": g_engine["m_dot_air_kg_s"],
                "e_in_kw": round(af.e_in_kw, 1),
                "mg_per_stroke": round(af.mg_per_stroke, 2),
            },
            module="svie_physics.air_fuel",
        ),
        DemoStep(
            id="02-hex",
            title="HEX — exhaust recuperation",
            summary="Heat exchanger duty recovering supercritical enthalpy into the fuel path.",
            metrics={
                "q_hex_kw": round(hex_r["q_hex_kw"], 1),
                "q_hex_kw_spec": g_sfv["q_hex_kw"],
                "exhaust_recovery_ratio": round(hex_r["exhaust_recovery_ratio"], 4),
                "brake_power_kw": round(hex_r["brake_power_kw"], 1),
            },
            module="svie_physics.heat_exchanger",
        ),
        DemoStep(
            id="03-hem",
            title="HEM — choked flash orifice",
            summary="Homogeneous-equilibrium choked flow sets injector orifice area.",
            metrics={
                "a_o_required_mm2": g_piezo["a_o_required_mm2"],
                "is_choked": hem_r["is_choked"],
                "flash_boiling": hem_r["flash_boiling"],
                "sigma_c": round(hem_r["sigma_c"], 3),
            },
            module="svie_physics.hem_choked_flow",
        ),
        DemoStep(
            id="04-axiom",
            title="AXIOM — anti-CVT rubber-band index",
            summary="Discrete multi-ratio path; rubber-band index locked at 0 (no belt).",
            metrics={
                "rubber_band_index": ax["rubber_band_index"],
                "mech_efficiency": ax["mech_efficiency"],
                "shift_ms": ax["shift_ms"],
                "bridge_no_belt": br["no_belt"],
            },
            module="svie_physics.axiom_drive",
        ),
        DemoStep(
            id="05-trl",
            title="TRL roadmap — hardware honesty",
            summary="Hardware remains TRL-3; the acquisition package is what is production-ready.",
            metrics={
                "current_trl": trl_r["current_trl"],
                "current_name": trl_r["current_name"],
                "stages": trl_r["stages"],
            },
            module="svie_physics.chronos_sentinel",
        ),
        DemoStep(
            id="06-acquire",
            title="Acquisition suite — production-ready package",
            summary="Weighted readiness scorecard, deal structure, and data-room index.",
            metrics={
                "weighted_score": acq["readiness"]["weighted_score"],
                "production_ready_acquisition": acq["readiness"]["production_ready_acquisition"],
                "preferred_deal": acq["deal"]["preferred_structure"],
                "data_room_folders": acq["data_room"]["folders"],
            },
            module="svie_physics.acquisition_suite",
        ),
    ]


def render_text(steps: list[DemoStep]) -> str:
    lines = [
        "=" * 64,
        f"  SVIE DEMO  ·  v{__version__}",
        "  Supercritical Vapor-Injection Engine — diligence walkthrough",
        "=" * 64,
        "",
    ]
    for step in steps:
        lines.append(f"[{step.id}] {step.title}")
        lines.append(f"  {step.summary}")
        lines.append(f"  module: {step.module}")
        for k, v in step.metrics.items():
            lines.append(f"    {k}: {v}")
        lines.append("")
    lines.extend(
        [
            "-" * 64,
            "Next: open http://localhost:3000/acquisition  (npm run dev:api && npm run dev:portal)",
            "Docs: Acquisition.md  ·  docs/acquisition/PRODUCTION-READINESS.md",
            "-" * 64,
        ]
    )
    return "\n".join(lines)


def render_json(steps: list[DemoStep]) -> str:
    payload = {
        "product": "SVIE",
        "version": __version__,
        "steps": [asdict(s) for s in steps],
    }
    return json.dumps(payload, indent=2, default=str)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SVIE guided demo program")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of the terminal narrative",
    )
    args = parser.parse_args(argv)
    steps = build_steps()
    out = render_json(steps) if args.json else render_text(steps)
    sys.stdout.write(out + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
