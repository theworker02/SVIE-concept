# Transmission Next Wave — FLUX-SHIFT · GEAR-MESH-AM · JET-BEARING

**Release:** 1.3.0  
**Manufacturing:** [`manufacturing-master-plan.md`](manufacturing-master-plan.md) §3  
**Specs:** `flux_shift.yaml`, `gear_mesh_am.yaml`, `jet_bearing.yaml`

---

## 1. FLUX-SHIFT — zero-interrupt preselect

**Problem:** Even discrete AXIOM ratios show a torque hole if a single clutch opens before the next closes.

**Feature:** Dual wet-clutch **preselect** path (DCT DNA without a belt): next gear pre-armed; overlap controlled by MIRAGE twin-path.

| KPI | Target |
|-----|--------|
| Torque interrupt | ≤ **8 ms** |
| Overlap energy | ≤ 1.2 kJ per shift |
| Rubber-band index | Remains **0** |

**Manufacturing:** Conventional wet clutch stacks + EH valves on shared 48 V pump (§3.2).

---

## 2. GEAR-MESH-AM — lattice carriers

**Problem:** Mesh whine and carrier mass fight high-RPM HERT/AXIOM NVH (SONIC stack).

**Feature:** LPBF lattice gear carriers — stiffness where teeth need it, compliance tuned to kill 1st mesh harmonic.

| KPI | Target |
|-----|--------|
| Carrier mass | **−18%** vs solid |
| 1st mesh harmonic amplitude | **−25%** |
| Safety factor (fatigue) | ≥ 1.6 at peak torque |

**Manufacturing:** LPBF 17-4PH/Ti + HIP + CNC splines (§3.3). Halo volumes only until cost falls.

---

## 3. JET-BEARING — directed oil for HERT turbine

**Problem:** HERT impulse turbine bearings starve under cold expansion + high shaft speed.

**Feature:** Dedicated oil jets from OIL-SPINE feed with temperature-scheduled flow (CHRONOS cold-start aware).

| KPI | Target |
|-----|--------|
| Bearing ΔT above oil | ≤ **35 K** |
| Jet velocity | ≥ 12 m/s at orifice |
| Cavitation margin | σ > 0.3 |

**Manufacturing:** Gun-drilled case galleries; replaceable jet orifices.

---

## Executable

```bash
python -m svie_physics.platform_features --domain transmission
```
