"""FastAPI bridge exposing SVIE physics modules to the web portal."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from svie_physics.air_fuel import AirFuelInputs, compute_air_fuel, inputs_from_spec, run_from_spec_path
from svie_physics.breakthrough import run_breakthrough_bundle
from svie_physics.chassis_torsion import run_from_spec as chassis_run
from svie_physics.gdsa_shift import run_from_spec as gdsa_run
from svie_physics.gear_map import run_from_spec as gear_run
from svie_physics.heat_exchanger import run_coupled as hex_coupled
from svie_physics.hem_choked_flow import run_coupled as hem_coupled
from svie_physics.hert_expansion import run_from_spec as hert_run
from svie_physics.io_util import load_yaml, specs_dir
from svie_physics.piezo_driver import run_from_spec as driver_run
from svie_physics.piezo_dynamics import run_from_spec as piezo_run

app = FastAPI(
    title="SVIE Physics API",
    description="Thin HTTP bridge over validated SVIE thermodynamic models",
    version="1.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AirFuelRequest(BaseModel):
    displacement_m3: float = Field(0.005204)
    rpm: float = Field(8500)
    volumetric_efficiency: float = Field(1.05)
    afr: float = Field(16.2)
    air_density_kg_m3: float = Field(1.184)
    cylinders: int = Field(8)
    fuel_density_kg_L: float = Field(0.745)
    lhv_kj_kg: float = Field(44000.0)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "svie-physics", "version": "1.3.0"}


@app.get("/demo")
def demo_bundle() -> dict[str, Any]:
    """Acquisition walkthrough metrics (same as `python -m svie_physics.demo --json`)."""
    from dataclasses import asdict

    from svie_physics.demo import __version__, build_steps

    return {
        "product": "SVIE",
        "version": __version__,
        "steps": [asdict(s) for s in build_steps()],
    }


@app.get("/inventory")
def inventory_bundle() -> dict[str, Any]:
    """Package inventory for diligence hub (same as `python -m svie_physics.inventory --json`)."""
    from svie_physics.inventory import build_inventory

    return build_inventory()


@app.get("/specs/{name}")
def get_spec(name: str) -> dict[str, Any]:
    path = specs_dir() / name
    if not path.suffix:
        path = path.with_suffix(".yaml")
    try:
        return load_yaml(path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/specs")
def list_specs() -> dict[str, list[str]]:
    files = sorted(p.name for p in specs_dir().glob("*.yaml"))
    return {"specs": files}


@app.get("/calc/air-fuel")
def calc_air_fuel_baseline() -> dict[str, Any]:
    return run_from_spec_path(specs_dir() / "svie_v8_52L.yaml")


@app.post("/calc/air-fuel")
def calc_air_fuel(body: AirFuelRequest) -> dict[str, Any]:
    result = compute_air_fuel(
        AirFuelInputs(
            displacement_m3=body.displacement_m3,
            rpm=body.rpm,
            volumetric_efficiency=body.volumetric_efficiency,
            afr=body.afr,
            air_density_kg_m3=body.air_density_kg_m3,
            cylinders=body.cylinders,
            fuel_density_kg_L=body.fuel_density_kg_L,
            lhv_kj_kg=body.lhv_kj_kg,
        )
    )
    return result.__dict__


@app.get("/calc/heat-exchanger")
def calc_hex() -> dict[str, Any]:
    return hex_coupled(
        load_yaml(specs_dir() / "svie_v8_52L.yaml"),
        load_yaml(specs_dir() / "sfv_fuel_system.yaml"),
    )


@app.get("/calc/hem")
def calc_hem() -> dict[str, Any]:
    return hem_coupled(
        load_yaml(specs_dir() / "svie_v8_52L.yaml"),
        load_yaml(specs_dir() / "piezo_injector.yaml"),
    )


@app.get("/calc/piezo")
def calc_piezo() -> dict[str, Any]:
    return piezo_run(load_yaml(specs_dir() / "piezo_injector.yaml"))


@app.get("/calc/driver")
def calc_driver(injectors: int = Query(8, ge=1, le=16)) -> dict[str, Any]:
    return driver_run(load_yaml(specs_dir() / "piezo_injector.yaml"), n_injectors=injectors)


@app.get("/calc/wot-bundle")
def calc_wot_bundle() -> dict[str, Any]:
    """Full WOT baseline bundle for portal dashboards."""
    engine = load_yaml(specs_dir() / "svie_v8_52L.yaml")
    sfv = load_yaml(specs_dir() / "sfv_fuel_system.yaml")
    piezo = load_yaml(specs_dir() / "piezo_injector.yaml")
    return {
        "air_fuel": compute_air_fuel(inputs_from_spec(engine)).__dict__,
        "heat_exchanger": hex_coupled(engine, sfv),
        "hem": hem_coupled(engine, piezo),
        "piezo": piezo_run(piezo),
        "driver": driver_run(piezo, n_injectors=int(engine["geometry"]["cylinders"])),
    }


@app.get("/calc/chassis")
def calc_chassis() -> dict[str, Any]:
    return chassis_run(load_yaml(specs_dir() / "chassis_monocoque.yaml"))


@app.get("/calc/hert")
def calc_hert() -> dict[str, Any]:
    return hert_run(load_yaml(specs_dir() / "hert_transaxle.yaml"))


@app.get("/calc/gdsa")
def calc_gdsa() -> dict[str, Any]:
    return gdsa_run(load_yaml(specs_dir() / "hert_transaxle.yaml"))


@app.get("/calc/gears")
def calc_gears(rpm: float = Query(8500, ge=1000, le=10000)) -> dict[str, Any]:
    return gear_run(load_yaml(specs_dir() / "hert_transaxle.yaml"), rpm_pre=rpm)


@app.get("/calc/breakthrough")
def calc_breakthrough() -> dict[str, Any]:
    return run_breakthrough_bundle(
        load_yaml(specs_dir() / "hert_transaxle.yaml"),
        load_yaml(specs_dir() / "chassis_monocoque.yaml"),
        load_yaml(specs_dir() / "breakthrough_subsystems.yaml"),
    )


@app.get("/calc/architecture-hr")
def calc_architecture_hr(rpm: float = Query(10000, ge=1000, le=15000)) -> dict[str, Any]:
    from svie_physics.engine_architecture import run_from_spec as arch_run

    return arch_run(load_yaml(specs_dir() / "svie_v8_hr_357.yaml"), rpm=rpm)


@app.get("/calc/deva")
def calc_deva(
    rpm: float = Query(8500, ge=500, le=12000),
    mode: str = Query("wot", pattern="^(wot|cruise)$"),
) -> dict[str, Any]:
    from svie_physics.deva_power import run_from_spec as deva_run

    return deva_run(load_yaml(specs_dir() / "deva_valvetrain.yaml"), rpm=rpm, mode=mode)


@app.get("/calc/h2")
def calc_h2(
    lambda_value: float = Query(1.05, ge=0.5, le=4.0, alias="lambda"),
    water_ratio: float = Query(0.15, ge=0.0, le=0.5),
) -> dict[str, Any]:
    from svie_physics.h2_combustion import run_case

    return run_case(
        load_yaml(specs_dir() / "h2_combustion_control.yaml"),
        lambda_value=lambda_value,
        water_fuel_ratio=water_ratio,
    )


@app.get("/calc/bom")
def calc_bom(with_chassis: bool = Query(False)) -> dict[str, Any]:
    from svie_physics.bom_cost import run_from_spec as bom_run

    return bom_run(
        load_yaml(specs_dir() / "bom_cost_estimate.yaml"),
        include_chassis=with_chassis,
    )


@app.get("/calc/cvt-compare")
def calc_cvt_compare(shaft_kw: float = Query(100.0, ge=10, le=500)) -> dict[str, Any]:
    from svie_physics.cvt_comparison import run_from_specs

    return run_from_specs(
        load_yaml(specs_dir() / "cvt_evidence.yaml"),
        load_yaml(specs_dir() / "axiom_drive.yaml"),
        shaft_in_kw=shaft_kw,
    )


@app.get("/calc/axiom")
def calc_axiom() -> dict[str, Any]:
    from svie_physics.axiom_drive import run_axiom, run_bridge

    return {
        "axiom": run_axiom(load_yaml(specs_dir() / "axiom_drive.yaml")),
        "bridge": run_bridge(load_yaml(specs_dir() / "ehe_v_bridge.yaml")),
    }


@app.get("/calc/nexus")
def calc_nexus(
    rpm: float = Query(8500, ge=500, le=12000),
    mode: str = Query("wot", pattern="^(wot|cruise)$"),
) -> dict[str, Any]:
    from svie_physics.nexus_48 import run_nexus

    return run_nexus(load_yaml(specs_dir() / "nexus_48.yaml"), rpm=rpm, mode=mode)


@app.get("/calc/sonic")
def calc_sonic() -> dict[str, Any]:
    from svie_physics.sonic_nvh import run_from_spec as sonic_run

    return sonic_run(load_yaml(specs_dir() / "sonic_nvh.yaml"))


@app.get("/calc/ops")
def calc_ops() -> dict[str, Any]:
    from svie_physics.chronos_sentinel import run_chronos, run_sentinel, run_trl

    return {
        "chronos": run_chronos(load_yaml(specs_dir() / "chronos_cold_start.yaml")),
        "sentinel": run_sentinel(load_yaml(specs_dir() / "sentinel_safety.yaml")),
        "trl": run_trl(load_yaml(specs_dir() / "trl_roadmap.yaml")),
    }


@app.get("/calc/control")
def calc_control(t: float = Query(12.0, ge=0.1, le=120)) -> dict[str, Any]:
    from svie_physics.blend_mirage_vector import run_blend, run_mirage, run_vector

    return {
        "blend": run_blend(load_yaml(specs_dir() / "blend_brake.yaml")),
        "mirage": run_mirage(load_yaml(specs_dir() / "mirage_twin.yaml"), t_s=t),
        "vector": run_vector(load_yaml(specs_dir() / "vector_hcp.yaml")),
    }


@app.get("/calc/platform")
def calc_platform(
    domain: str = Query("all", pattern="^(engine|transmission|body|all)$"),
) -> dict[str, Any]:
    from svie_physics.platform_features import (
        run_all,
        run_body_bundle,
        run_engine_bundle,
        run_transmission_bundle,
    )

    if domain == "engine":
        return run_engine_bundle()
    if domain == "transmission":
        return run_transmission_bundle()
    if domain == "body":
        return run_body_bundle()
    return run_all()


@app.get("/calc/manufacturing")
def calc_manufacturing() -> dict[str, Any]:
    from svie_physics.manufacturing import run_manufacturing

    return run_manufacturing()


@app.get("/calc/addons")
def calc_addons() -> dict[str, Any]:
    from svie_physics.addon_features import run_all as addon_all

    return addon_all()


@app.get("/calc/validate")
def calc_validate() -> dict[str, Any]:
    from svie_physics.validate import run_validation

    return run_validation()


@app.get("/calc/design")
def calc_design() -> dict[str, Any]:
    from svie_physics.design_system import run_all as design_all

    return design_all()


@app.get("/calc/aether")
def calc_aether() -> dict[str, Any]:
    from svie_physics.aether_os import run_all as aether_all

    return aether_all()


@app.get("/calc/acquisition")
def calc_acquisition() -> dict[str, Any]:
    from svie_physics.acquisition_suite import run_all as acq_all

    return acq_all()


@app.get("/calc/compliance")
def calc_compliance() -> dict[str, Any]:
    from svie_physics.compliance import run_all as compliance_all

    return compliance_all()


@app.get("/calc/supply")
def calc_supply() -> dict[str, Any]:
    from svie_physics.supply_chain import run_all as supply_all

    return supply_all()
