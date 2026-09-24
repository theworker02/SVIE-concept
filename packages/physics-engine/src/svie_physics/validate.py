"""Cross-spec validation harness for SVIE diligence."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from svie_physics.air_fuel import compute_air_fuel, inputs_from_spec
from svie_physics.axiom_drive import run_axiom
from svie_physics.chronos_sentinel import run_trl
from svie_physics.io_util import load_yaml, specs_dir
from svie_physics.inventory import build_inventory
from svie_physics.manufacturing import run_manufacturing
from svie_physics.platform_features import run_flux_shift, run_node_cast, run_ring_zero

__version__ = "1.3.0"


def _check(name: str, ok: bool, detail: str) -> dict[str, Any]:
    return {"id": name, "ok": ok, "detail": detail}


def run_validation() -> dict[str, Any]:
    root = specs_dir()
    matrix = load_yaml(root / "validation_matrix.yaml")
    engine = load_yaml(root / "svie_v8_52L.yaml")
    mfg = run_manufacturing()
    ring = run_ring_zero(load_yaml(root / "ring_zero.yaml"))
    axiom = run_axiom(load_yaml(root / "axiom_drive.yaml"))
    flux = run_flux_shift(load_yaml(root / "flux_shift.yaml"))
    node = run_node_cast(load_yaml(root / "node_cast_body.yaml"))
    trl = run_trl(load_yaml(root / "trl_roadmap.yaml"))
    af = compute_air_fuel(inputs_from_spec(engine))
    inv = build_inventory()

    checks = [
        _check(
            "ptwa_consistency",
            abs(mfg["ptwa_mm"] - ring["ptwa_bore_mm"]) < 1e-9,
            f"mfg={mfg['ptwa_mm']} ring={ring['ptwa_bore_mm']}",
        ),
        _check(
            "rbi_consistency",
            axiom["rubber_band_index"] == 0 and flux["rubber_band_index"] == 0,
            f"axiom={axiom['rubber_band_index']} flux={flux['rubber_band_index']}",
        ),
        _check(
            "node_torsion_gain",
            node["torsion_nm_per_deg"] >= 35000,
            f"torsion={node['torsion_nm_per_deg']}",
        ),
        _check(
            "inventory_specs",
            inv["counts"]["specs_yaml"] >= 35,
            f"specs={inv['counts']['specs_yaml']}",
        ),
        _check(
            "trl_current",
            trl["current_trl"] == int(matrix["in_repo"]["trl"]),
            f"trl={trl['current_trl']}",
        ),
        _check(
            "demo_fuel_golden",
            abs(af.m_dot_fuel_g_s - float(engine["golden"]["m_dot_fuel_g_s"]))
            / float(engine["golden"]["m_dot_fuel_g_s"])
            < 2e-3,
            f"computed={af.m_dot_fuel_g_s:.4f} golden={engine['golden']['m_dot_fuel_g_s']}",
        ),
        _check(
            "flux_interrupt_gate",
            flux["interrupt_ms"] <= 8.0,
            f"interrupt_ms={flux['interrupt_ms']} (design target; see validation-report)",
        ),
        _check(
            "mfg_routes",
            mfg["route_count"] >= 15,
            f"routes={mfg['route_count']}",
        ),
        _check(
            "acquisition_ready",
            True,  # filled below after suite import
            "pending",
        ),
    ]

    from svie_physics.acquisition_suite import run_readiness

    ready = run_readiness(inv=inv)
    checks[-1] = _check(
        "acquisition_ready",
        bool(ready["production_ready_acquisition"]),
        f"score={ready['weighted_score']} gates={ready['gates_pass']}",
    )
    checks.append(
        _check(
            "inventory_specs_v27",
            inv["counts"]["specs_yaml"] >= 55,
            f"specs={inv['counts']['specs_yaml']}",
        )
    )
    checks.append(
        _check(
            "licensing_packages_v27",
            inv["counts"]["licensing_packages"] >= 14,
            f"packages={inv['counts']['licensing_packages']}",
        )
    )

    passed = sum(1 for c in checks if c["ok"])
    return {
        "product": "SVIE",
        "version": __version__,
        "passed": passed,
        "total": len(checks),
        "all_ok": passed == len(checks),
        "checks": checks,
        "literature_notes": matrix.get("literature_confidence", {}),
        "meta": {"module": "validate"},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SVIE cross-spec validation")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = run_validation()
    if args.json:
        sys.stdout.write(json.dumps(result, indent=2) + "\n")
    else:
        lines = [
            "=" * 64,
            f"  SVIE VALIDATE  ·  v{result['version']}",
            f"  {result['passed']}/{result['total']} checks passed",
            "=" * 64,
            "",
        ]
        for c in result["checks"]:
            mark = "OK" if c["ok"] else "FAIL"
            lines.append(f"  [{mark}] {c['id']}: {c['detail']}")
        lines.append("-" * 64)
        lines.append(
            "  See docs/validation-report.md for literature grounding."
            if result["all_ok"]
            else "  VALIDATION FAILED — fix failing checks before diligence."
        )
        lines.append("-" * 64)
        sys.stdout.write("\n".join(lines) + "\n")
    return 0 if result["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
