"""SVIE package inventory — counts specs, docs, modules, and tests for diligence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from svie_physics.io_util import repo_root

__version__ = "1.3.0"

PHYSICS_MODULES = [
    "air_fuel",
    "heat_exchanger",
    "hem_choked_flow",
    "piezo_dynamics",
    "piezo_driver",
    "chassis_torsion",
    "hert_expansion",
    "gdsa_shift",
    "gear_map",
    "breakthrough",
    "engine_architecture",
    "deva_power",
    "h2_combustion",
    "bom_cost",
    "cvt_comparison",
    "axiom_drive",
    "nexus_48",
    "sonic_nvh",
    "chronos_sentinel",
    "blend_mirage_vector",
    "demo",
    "inventory",
    "platform_features",
    "manufacturing",
    "validate",
    "addon_features",
    "design_system",
    "aether_os",
    "acquisition_suite",
    "compliance",
    "supply_chain",
]

LICENSING_PACKAGES = [
    {
        "id": "SFV-CORE",
        "name": "Supercritical Flash-Vaporization fuel path",
        "includes": ["air_fuel", "heat_exchanger", "hem_choked_flow", "piezo_dynamics", "piezo_driver"],
        "specs": ["svie_v8_52L.yaml", "sfv_fuel_system.yaml", "piezo_injector.yaml"],
    },
    {
        "id": "DEVA-HR",
        "name": "Camless DEVA + V8-HR H2 architecture",
        "includes": ["deva_power", "engine_architecture", "h2_combustion"],
        "specs": ["deva_valvetrain.yaml", "svie_v8_hr_357.yaml", "h2_combustion_control.yaml"],
    },
    {
        "id": "AXIOM-DRIVE",
        "name": "Anti-CVT discrete drive + e:HEV bridge",
        "includes": ["axiom_drive", "cvt_comparison", "hert_expansion", "gdsa_shift", "gear_map"],
        "specs": ["axiom_drive.yaml", "ehe_v_bridge.yaml", "cvt_evidence.yaml", "hert_transaxle.yaml"],
    },
    {
        "id": "OPS-STACK",
        "name": "NEXUS / SONIC / SENTINEL / CHRONOS",
        "includes": ["nexus_48", "sonic_nvh", "chronos_sentinel"],
        "specs": ["nexus_48.yaml", "sonic_nvh.yaml", "sentinel_safety.yaml", "chronos_cold_start.yaml", "trl_roadmap.yaml"],
    },
    {
        "id": "CONTROL",
        "name": "BLEND / MIRAGE / VECTOR control layer",
        "includes": ["blend_mirage_vector"],
        "specs": ["blend_brake.yaml", "mirage_twin.yaml", "vector_hcp.yaml"],
    },
    {
        "id": "STRUCTURE",
        "name": "Chassis + breakthrough + BOM",
        "includes": ["chassis_torsion", "breakthrough", "bom_cost"],
        "specs": ["chassis_monocoque.yaml", "breakthrough_subsystems.yaml", "bom_cost_estimate.yaml", "thermal_oil_system.yaml"],
    },
    {
        "id": "ENGINE-PLUS",
        "name": "CRYO-RAIL / RING-ZERO / OIL-SPINE / AETHER-IGN",
        "includes": ["platform_features"],
        "specs": ["engine_cryo_rail.yaml", "ring_zero.yaml", "oil_spine.yaml", "aether_ign.yaml"],
    },
    {
        "id": "TRANS-PLUS",
        "name": "FLUX-SHIFT / GEAR-MESH-AM / JET-BEARING",
        "includes": ["platform_features"],
        "specs": ["flux_shift.yaml", "gear_mesh_am.yaml", "jet_bearing.yaml"],
    },
    {
        "id": "BODY-PLUS",
        "name": "NODE-CAST / AERO-SKIN / CELL-VAULT / THERMAL-SKIN",
        "includes": ["platform_features"],
        "specs": ["node_cast_body.yaml", "aero_skin.yaml", "cell_vault.yaml", "thermal_skin.yaml"],
    },
    {
        "id": "MFG-PLAN",
        "name": "Manufacturing master routes and cells",
        "includes": ["manufacturing"],
        "specs": ["manufacturing_master.yaml"],
    },
    {
        "id": "ADDONS",
        "name": "DRY-SUMP / PULSE-EGR / SILK / RANGE / KERS",
        "includes": ["addon_features"],
        "specs": [
            "dry_sump_x.yaml",
            "pulse_egr.yaml",
            "silk_mount.yaml",
            "range_bridge.yaml",
            "kers_blend.yaml",
            "validation_matrix.yaml",
        ],
    },
    {
        "id": "DESIGN",
        "name": "Vehicle design + AETHER-OS / CarPlay Ultra / analog HMI",
        "includes": ["design_system", "aether_os"],
        "specs": [
            "body_exterior.yaml",
            "lighting_headlamp.yaml",
            "cabin_layout.yaml",
            "packaging_layout.yaml",
            "wiring_harness.yaml",
            "design_system.yaml",
            "aether_os.yaml",
            "carplay_ultra.yaml",
            "analog_hmi.yaml",
        ],
    },
    {
        "id": "COMPLIANCE",
        "name": "Homologation · ISO 26262 · ISO 21434 · OTA · durability",
        "includes": ["compliance"],
        "specs": [
            "homologation_path.yaml",
            "iso26262_sentinel.yaml",
            "iso21434_aether.yaml",
            "ota_fleet_policy.yaml",
            "durability_gate.yaml",
            "supply_chain_tier1.yaml",
        ],
    },
    {
        "id": "ACQUIRE",
        "name": "Acquisition readiness · deal structures · data room",
        "includes": ["acquisition_suite", "supply_chain"],
        "specs": [
            "acquisition_readiness.yaml",
            "deal_structure.yaml",
            "data_room_index.yaml",
        ],
    },
]


def _list_files(directory: Path, pattern: str) -> list[str]:
    if not directory.is_dir():
        return []
    return sorted(p.name for p in directory.glob(pattern) if p.is_file())


def build_inventory() -> dict[str, Any]:
    root = repo_root()
    specs = _list_files(root / "specs", "*.yaml")
    docs = _list_files(root / "docs", "*.md")
    acq_docs = _list_files(root / "docs" / "acquisition", "*.md")
    tests = _list_files(root / "packages" / "physics-engine" / "tests", "test_*.py")
    brand = _list_files(root / "brand", "*")
    portal_routes = [
        "/",
        "/pitch",
        "/demo",
        "/diligence",
        "/package",
        "/calculators",
        "/specs",
        "/architecture",
        "/design",
        "/hmi",
        "/acquisition",
    ]

    return {
        "product": "SVIE",
        "version": __version__,
        "counts": {
            "specs_yaml": len(specs),
            "docs_md": len(docs),
            "acquisition_docs": len(acq_docs),
            "physics_modules": len(PHYSICS_MODULES),
            "test_files": len(tests),
            "licensing_packages": len(LICENSING_PACKAGES),
            "brand_assets": len([b for b in brand if not b.startswith(".")]),
            "portal_routes": len(portal_routes),
        },
        "specs": specs,
        "docs": docs,
        "acquisition_docs": acq_docs,
        "physics_modules": PHYSICS_MODULES,
        "test_files": tests,
        "licensing_packages": LICENSING_PACKAGES,
        "portal_routes": portal_routes,
        "brand_assets": brand,
        "headline_metrics": {
            "m_dot_fuel_g_s": 28.28,
            "q_hex_kw": 23.2,
            "a_o_required_mm2": 0.431,
            "rubber_band_index": 0,
            "trl_in_repo": 3,
        },
        "meta": {"module": "inventory", "repo_root": str(root)},
    }


def render_text(inv: dict[str, Any]) -> str:
    c = inv["counts"]
    hm = inv["headline_metrics"]
    lines = [
        "=" * 64,
        f"  SVIE PACKAGE INVENTORY  ·  v{inv['version']}",
        "=" * 64,
        "",
        f"  Specs (YAML):          {c['specs_yaml']}",
        f"  Technical docs:        {c['docs_md']}",
        f"  Acquisition docs:      {c['acquisition_docs']}",
        f"  Physics modules:       {c['physics_modules']}",
        f"  Test files:            {c['test_files']}",
        f"  Licensing packages:    {c['licensing_packages']}",
        f"  Brand assets:          {c['brand_assets']}",
        f"  Portal routes:         {c['portal_routes']}",
        "",
        "  Licensing packages:",
    ]
    for pkg in inv["licensing_packages"]:
        lines.append(f"    [{pkg['id']}] {pkg['name']}")
    lines.extend(
        [
            "",
            "  Headline metrics:",
            f"    m_dot fuel: {hm['m_dot_fuel_g_s']} g/s",
            f"    Q_dot HEX:  {hm['q_hex_kw']} kW",
            f"    AXIOM RBI: {hm['rubber_band_index']}",
            f"    TRL: {hm['trl_in_repo']}",
            "-" * 64,
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SVIE package inventory")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args(argv)
    inv = build_inventory()
    out = json.dumps(inv, indent=2) if args.json else render_text(inv)
    sys.stdout.write(out + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
