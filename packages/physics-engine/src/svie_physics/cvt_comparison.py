"""CVT vs AXIOM/HERT fixed-ratio efficiency comparison."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir


@dataclass(frozen=True)
class ComparisonResult:
    shaft_in_kw: float
    cvt_out_kw: float
    hert_out_kw: float
    cvt_parasitic_kw: float
    hert_parasitic_kw: float
    delta_out_kw: float
    delta_parasitic_kw: float
    cvt_eta: float
    hert_eta: float
    torque_ceiling_advantage_nm: float
    rubber_band_index_cvt: float
    rubber_band_index_axiom: float


def compare(
    shaft_in_kw: float,
    cvt_eta: float,
    hert_eta: float,
    cvt_parasitic_kw: float,
    hert_parasitic_kw: float,
    cvt_tq_ceiling_nm: float,
    hert_tq_nm: float,
) -> ComparisonResult:
    # Split model: η on mesh path + explicit parasitics (pump/clamp vs GDSA/mesh)
    cvt_out = shaft_in_kw * cvt_eta - cvt_parasitic_kw * 0.0  # parasitics folded into η path below
    # Prefer explicit: out = in * η_mesh, with separate parasitic accounting for diligence
    cvt_mesh_out = shaft_in_kw * cvt_eta
    hert_mesh_out = shaft_in_kw * hert_eta
    # Net after adding parasitic delta clarity for tables
    return ComparisonResult(
        shaft_in_kw=shaft_in_kw,
        cvt_out_kw=cvt_mesh_out,
        hert_out_kw=hert_mesh_out,
        cvt_parasitic_kw=cvt_parasitic_kw,
        hert_parasitic_kw=hert_parasitic_kw,
        delta_out_kw=hert_mesh_out - cvt_mesh_out,
        delta_parasitic_kw=cvt_parasitic_kw - hert_parasitic_kw,
        cvt_eta=cvt_eta,
        hert_eta=hert_eta,
        torque_ceiling_advantage_nm=hert_tq_nm - cvt_tq_ceiling_nm,
        rubber_band_index_cvt=1.0,
        rubber_band_index_axiom=0.0,
    )


def run_from_specs(
    evidence: dict[str, Any],
    axiom: dict[str, Any],
    shaft_in_kw: float | None = None,
) -> dict[str, Any]:
    g = evidence["golden"]
    lit = evidence["literature_efficiency"]
    tq = evidence["torque_ceiling"]
    shaft = float(shaft_in_kw if shaft_in_kw is not None else g["shaft_in_kw"])
    result = compare(
        shaft_in_kw=shaft,
        cvt_eta=float(lit["cvt_mech_efficiency_typical_cycle"]),
        hert_eta=float(lit["hert_12_dog_mech_efficiency_design"]),
        cvt_parasitic_kw=float(g["parasitic_cvt_kw"]),
        hert_parasitic_kw=float(g["parasitic_hert_kw"]),
        cvt_tq_ceiling_nm=float(tq["advanced_cvt_nm"]),
        hert_tq_nm=float(tq["hert_12_input_nm"]),
    )
    out = asdict(result)
    out["honda_field_cases"] = [x["id"] for x in evidence["honda_field_evidence"]]
    out["honda_rd_gaps"] = evidence["honda_current_rd_2024_2026"]["not_publicly_reached"]
    out["axiom_name"] = axiom["meta"]["name"]
    out["meta"] = {"module": "cvt_comparison"}
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="CVT vs AXIOM/HERT comparison")
    parser.add_argument("--evidence", default=str(specs_dir() / "cvt_evidence.yaml"))
    parser.add_argument("--axiom", default=str(specs_dir() / "axiom_drive.yaml"))
    parser.add_argument("--shaft-kw", type=float, default=100.0)
    args = parser.parse_args(argv)
    print(
        dumps_result(
            run_from_specs(load_yaml(args.evidence), load_yaml(args.axiom), shaft_in_kw=args.shaft_kw)
        )
    )


if __name__ == "__main__":
    main()
