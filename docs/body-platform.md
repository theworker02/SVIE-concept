# Body & Platform — NODE-CAST · AERO-SKIN · CELL-VAULT · THERMAL-SKIN

**Release:** 1.3.0  
**Manufacturing:** [`manufacturing-master-plan.md`](manufacturing-master-plan.md) §4  
**Specs:** `node_cast_body.yaml`, `aero_skin.yaml`, `cell_vault.yaml`, `thermal_skin.yaml`

---

## 1. NODE-CAST — hybrid CFRP tub + cast aluminum nodes

**Problem:** Full carbon hard-points are expensive and crash-repair hostile; full aluminum loses torsion.

**Feature:** CFRP monocoque tub with **cast Al structural nodes** at suspension, crash, and powertrain mounts — adhesive + mechanical join.

| KPI | Target |
|-----|--------|
| Torsion | ≥ **38,000** Nm/deg (above prior 35k class target) |
| Node safety factor | ≥ **1.8** at 2.5 g bump |
| Repair | Bolt-on node replace without tub scrap |

**Manufacturing:** Autoclave/RTM tub + A356 node castings (§4.1).

---

## 2. AERO-SKIN — active diffuser / DRS

**Problem:** Fixed venturi downforce in chassis spec cannot trade Cd on cruise vs grip on corner exit.

**Feature:** 48 V actuated rear diffuser flap + DRS wing element commanded by VECTOR HCP.

| KPI | Target |
|-----|--------|
| Δ downforce (flap closed→open) | **+420 N** @ 200 km/h |
| Δ Cd | **−0.025** in DRS open |
| Actuation time | ≤ 180 ms |

**Manufacturing:** Prepreg carbon skins, foam core, sealed linear actuators (§4.2).

---

## 3. CELL-VAULT — structural energy vault

**Problem:** H₂ tanks or hybrid batteries fight for crash volume under a mid-engine sports architecture.

**Feature:** Under-floor **structural vault** — crush cans + shear panels — cradles Type IV H₂ or battery modules; CASMIR AE pads on tank option.

| KPI | Target |
|-----|--------|
| Absorbed energy (frontal conceptual) | ≥ **85 kJ** vault share |
| Intrusion index | ≤ 0.12 m at barrier case |
| Mass | ≤ 48 kg structure |

**Manufacturing:** Al extrusions + CFRP shear; tank cradle per SENTINEL (§4.3).

---

## 4. THERMAL-SKIN — body heat rejection assist

**Problem:** SFV HEX dumps heat; tight aero packaging limits radiator area.

**Feature:** Select body panels with microchannel / PCM layers rejecting low-grade heat; optional thermoelectric assist on NEXUS-48.

| KPI | Target |
|-----|--------|
| Extra heat rejection | **1.8 kW** cruise |
| Panel ΔT surface | ≤ 15 K comfort |
| Mass penalty | ≤ 6 kg |

**Manufacturing:** Laminated aluminum / composite skins with bonded microchannel foils.

---

## Executable

```bash
python -m svie_physics.platform_features --domain body
```
