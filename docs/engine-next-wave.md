# Engine Next Wave — CRYO-RAIL · RING-ZERO · OIL-SPINE · AETHER-IGN

**Release:** 1.3.0  
**Manufacturing:** [`manufacturing-master-plan.md`](manufacturing-master-plan.md) §2  
**Specs:** `engine_cryo_rail.yaml`, `ring_zero.yaml`, `oil_spine.yaml`, `aether_ign.yaml`

---

## 1. CRYO-RAIL — thermal-buffered supercritical rail

**Problem:** SFV rails see exhaust-HEX heat + injector sink; pressure/temperature wander kills orifice HEM assumptions.

**Feature:** Dual-wall rail with phase-change material (PCM) jacket that absorbs HEX transients, holding rail fluid near design supercritical window.

| KPI | Target |
|-----|--------|
| Rail ΔT under step load | ≤ **8 K** (vs 22 K unbuffered) |
| Pressure droop @ WOT tip-in | ≤ **0.15 MPa** |
| PCM melt class | 290–310 °C paraffin / salt hydrate blend |

**Manufacturing:** Drawn 316L rail + welded PCM jackets; helium leak test; see master plan §2.3.

---

## 2. RING-ZERO — low-friction pack for PTWA bores

**Problem:** High-RPM H₂ DI and SFV gasoline both punish ring tension and bore oil.

**Feature:** Low-tension ring pack + DLC top ring optimized for **PTWA nanocrystalline ferrous** bores (Ford Shelby-class ~150 µm coating precedent).

| KPI | Target |
|-----|--------|
| FMEP delta vs baseline pack | **−12%** |
| Oil consumption index | ≤ 0.85× baseline |
| Top-ring DLC thickness | 1.5–3 µm |

**Manufacturing:** Nitrided steel + PVD DLC; plateau hone matched to PTWA porosity (§2.1, §2.4).

---

## 3. OIL-SPINE — structural girdle oil gallery

**Problem:** High MPS (25 m/s class) and HERT bearing jets fight for oil pressure.

**Feature:** Ladder girdle cast with **structural oil spine** — main gallery doubles as stiffener; dedicated jets to pistons and HERT feed.

| KPI | Target |
|-----|--------|
| Gallery pressure @ 10k RPM | ≥ **4.5 bar** |
| Jet flow per piston | ≥ **1.2 L/min** |
| Spine bending contribution | +**6%** block stiffness index |

**Manufacturing:** Cast-in spine + gun-drill jets; ISO cleanliness gate (§2.5).

---

## 4. AETHER-IGN — adaptive plasma / spark hybrid

**Problem:** Ultra-lean SFV cruise and H₂ DI need different ignition energy & timing agility than fixed coils.

**Feature:** Dual-mode coil: conventional spark for stoichiometric / light load; pulsed plasma assist for λ > 1.8 and H₂ stratified events (extends PSI breakthrough).

| KPI | Target |
|-----|--------|
| Lean limit extension | **+0.3 λ** vs spark-only |
| Energy per event (plasma) | 80–120 mJ budgeted |
| Coil thermal | NEXUS-48 cooled boss |

**Manufacturing:** Tier-1 ignition module; conformal boss cooling from hybrid head.

---

## Executable

```bash
python -m svie_physics.platform_features --domain engine
```
