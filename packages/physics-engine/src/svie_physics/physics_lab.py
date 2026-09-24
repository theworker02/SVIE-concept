"""Interactive coupled physics lab — realistic maps + RPM sweeps for the portal."""

from __future__ import annotations

import argparse
import math
from typing import Any

from svie_physics.io_util import dumps_result, load_yaml, specs_dir

R_AIR = 287.05  # J/(kg·K)
DELTA_H_SFV_KJ_KG = 820.0  # supercritical enthalpy rise (spec-aligned order)
GOLDEN_RPM = 8500.0
GOLDEN_ETA_V = 1.05
GOLDEN_AFR = 16.2
GOLDEN_BTE = 0.42


def air_density_kg_m3(temp_c: float, pressure_kpa: float) -> float:
    """Ideal-gas dry air density from ambient T/P."""
    t_k = temp_c + 273.15
    return (pressure_kpa * 1000.0) / (R_AIR * t_k)


def volumetric_efficiency(rpm: float, peak_eta: float = GOLDEN_ETA_V, peak_rpm: float = GOLDEN_RPM) -> float:
    """Intake wave-tuning map — peaks at design RPM, falls off at low/high speed."""
    span = 2400.0
    x = (rpm - peak_rpm) / span
    # Soft floors so idle/redline stay physical
    eta = peak_eta * math.exp(-0.5 * x * x)
    return max(0.72, min(1.18, eta))


def brake_thermal_efficiency(afr: float, load: float = 1.0) -> float:
    """BTE peaks near the lean homogeneous design AFR; drops off-stoich and at light load."""
    afr_term = math.exp(-(((afr - GOLDEN_AFR) / 7.5) ** 2))
    load_term = 0.78 + 0.22 * max(0.2, min(1.0, load))
    return GOLDEN_BTE * afr_term * load_term


def compute_point(
    *,
    rpm: float,
    afr: float,
    displacement_m3: float = 0.005204,
    cylinders: int = 8,
    temp_c: float = 25.0,
    pressure_kpa: float = 101.325,
    load: float = 1.0,
    boost_kpa: float = 0.0,
    lhv_kj_kg: float = 44000.0,
    peak_eta_v: float = GOLDEN_ETA_V,
    delta_h_kj_kg: float = DELTA_H_SFV_KJ_KG,
) -> dict[str, Any]:
    """Coupled operating point: air/fuel + BTE power/torque + HEX + injector timing."""
    p_intake = pressure_kpa + boost_kpa
    rho = air_density_kg_m3(temp_c, p_intake)
    eta_v = volumetric_efficiency(rpm, peak_eta=peak_eta_v)
    # Part-load throttle proxy: scale air with load (simplified)
    eta_eff = eta_v * max(0.15, min(1.0, load))

    cps = rpm / 120.0
    v_dot = displacement_m3 * cps * eta_eff
    m_air = v_dot * rho
    m_fuel = m_air / afr
    m_fuel_g_s = m_fuel * 1000.0
    e_in_kw = m_fuel * lhv_kj_kg
    bte = brake_thermal_efficiency(afr, load)
    p_brake_kw = e_in_kw * bte
    # τ (N·m) = P(W) * 60 / (2π n)
    torque_nm = (p_brake_kw * 1000.0 * 60.0) / (2.0 * math.pi * rpm) if rpm > 1 else 0.0
    q_hex_kw = m_fuel * delta_h_kj_kg
    exhaust_kw = e_in_kw * 0.30
    recovery = q_hex_kw / exhaust_kw if exhaust_kw > 0 else 0.0

    per_inj_g_s = m_fuel_g_s / cylinders
    mg_stroke = (per_inj_g_s / cps) * 1000.0 if cps > 0 else 0.0
    cycle_ms = (120.0 / rpm) * 1000.0 if rpm > 0 else 0.0
    # Calibrated so ~50 mg ≈ ~4.2 ms at WOT (≈30% duty at 8500)
    pw_ms = mg_stroke * 0.084
    duty = pw_ms / cycle_ms if cycle_ms > 0 else 0.0

    return {
        "rpm": rpm,
        "afr": afr,
        "load": load,
        "temp_c": temp_c,
        "pressure_kpa": p_intake,
        "air_density_kg_m3": round(rho, 4),
        "eta_v": round(eta_v, 4),
        "eta_v_effective": round(eta_eff, 4),
        "m_dot_air_kg_s": round(m_air, 5),
        "m_dot_fuel_g_s": round(m_fuel_g_s, 3),
        "mg_per_stroke": round(mg_stroke, 2),
        "e_in_kw": round(e_in_kw, 1),
        "bte": round(bte, 4),
        "brake_power_kw": round(p_brake_kw, 1),
        "brake_power_hp": round(p_brake_kw / 0.7457, 0),
        "torque_nm": round(torque_nm, 1),
        "q_hex_kw": round(q_hex_kw, 2),
        "exhaust_kw": round(exhaust_kw, 1),
        "hex_recovery": round(recovery, 4),
        "injector_pw_ms": round(pw_ms, 2),
        "injector_duty": round(duty, 3),
        "choked_orifice_ok": duty < 0.85 and mg_stroke > 0,
        "meta": {"module": "physics_lab", "version": "1.3.1"},
    }


def run_sweep(
    *,
    rpm_min: float = 1500,
    rpm_max: float = 9000,
    points: int = 40,
    afr: float = GOLDEN_AFR,
    load: float = 1.0,
    temp_c: float = 25.0,
    pressure_kpa: float = 101.325,
    boost_kpa: float = 0.0,
) -> dict[str, Any]:
    """RPM sweep series for interactive charts."""
    n = max(5, min(80, int(points)))
    step = (rpm_max - rpm_min) / (n - 1)
    series: list[dict[str, Any]] = []
    for i in range(n):
        rpm = rpm_min + step * i
        series.append(
            compute_point(
                rpm=rpm,
                afr=afr,
                load=load,
                temp_c=temp_c,
                pressure_kpa=pressure_kpa,
                boost_kpa=boost_kpa,
            )
        )
    peak = max(series, key=lambda p: p["brake_power_kw"])
    return {
        "series": series,
        "peak_power_kw": peak["brake_power_kw"],
        "peak_power_rpm": peak["rpm"],
        "peak_torque_nm": max(p["torque_nm"] for p in series),
        "meta": {"module": "physics_lab_sweep", "points": n},
    }


def run_wot_anchor() -> dict[str, Any]:
    """Design WOT point — should stay near golden locked metrics."""
    return compute_point(rpm=GOLDEN_RPM, afr=GOLDEN_AFR, load=1.0, temp_c=25.0)


def run_all() -> dict[str, Any]:
    return {
        "wot": run_wot_anchor(),
        "sweep": run_sweep(),
        "meta": {"module": "physics_lab", "version": "1.3.1"},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SVIE interactive physics lab")
    parser.add_argument("--rpm", type=float, default=8500)
    parser.add_argument("--afr", type=float, default=16.2)
    parser.add_argument("--load", type=float, default=1.0)
    parser.add_argument("--sweep", action="store_true")
    args = parser.parse_args(argv)
    if args.sweep:
        print(dumps_result(run_sweep(afr=args.afr, load=args.load)))
    else:
        print(dumps_result(compute_point(rpm=args.rpm, afr=args.afr, load=args.load)))


if __name__ == "__main__":
    main()
