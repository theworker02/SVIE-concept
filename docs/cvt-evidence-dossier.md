# CVT Evidence Dossier — Why SVIE Deletes the Belt

**Spec:** [`specs/cvt_evidence.yaml`](../specs/cvt_evidence.yaml)  
**Model:** `python -m svie_physics.cvt_comparison`  
**Audience:** Honda R&D / transmission IP evaluation

---

## 1. Mechanical efficiency evidence

| Source class | Finding |
|--------------|---------|
| ICCT transmission working paper | CVTs suffer **greater losses than DCTs/ATs** from clamp friction + high-pressure hydraulics; engine-optima tracking can offset this in *some* cycles — not a free lunch |
| Springer / CVT slip literature | Cited target band **75–90%** often **not reached**; clamp margin and belt slip destroy efficiency |
| EV-CVT clamp studies | Fuzzy slip control can cut clamp force ~13–22% and still only partially closes the gap |
| Dog / AMT literature | Dry single-clutch / dog paths sit near **~94–97%** mesh efficiency |

**SVIE locked comparison @ 100 kW shaft in:**

| Path | η_mech (cycle) | Parasitics | Mesh out |
|------|----------------|------------|----------|
| Typical belt CVT | **0.82** | **13.5 kW** clamp/pump/belt | 82 kW |
| HERT-12 / AXIOM dog | **0.965** | **2.6 kW** | 96.5 kW |
| **Delta** | +14.5 pt | **−10.9 kW** | **+14.5 kW** |

---

## 2. Torque ceiling & sports-car mismatch

Metal-belt passenger CVTs typically top out ~250–400 Nm. SVIE V8-HR / HERT input class is **850 Nm** design. A belt cannot be the answer for a high-RPM hydrogen DI V8 without derate — dog clutches scale.

Fretting/wear literature shows steel-ring safety margin collapsing above ~130 Nm in some belt studies — another reason not to hang a supercar torque curve on a push-belt.

---

## 3. Honda field evidence (not rumor)

| ID | Fact |
|----|------|
| **SB 21-047 / HR-V** | Warranty extension for **2016–2020 HR-V premature CVT belt deterioration** (7 yr / 150k mi); risk of **no propulsion**; belt debris magnet inspection |
| **Civic CVT noise TSB** | Hot-restart grinding from valve-body vibration; HCF-2 fluid strictness |
| Product update 21-046 | Software lacked adequate belt-failure monitoring (DTC P271E added) |

This is public service documentation — diligence teams already know it. SVIE’s pitch: **do not re-litigate belt durability on a 10k-RPM H2 V8.**

---

## 4. Honda’s *current* answer is still “CVT-shaped”

Next-gen **e:HEV** (Dec 2024 briefing) renews:

- 1.5 / 2.0 DI Atkinson engines  
- **Electric CVT** dual-motor front drive units  
- **S+ Shift** — software that *fakes* gear steps on an eCVT  
- Electric AWD + FC / tank AE / space electrolysis (Vol.37)

S+ Shift proves Honda feels the **engagement deficit** of continuous ratio devices — and is solving it with **simulation**, not fixed gears.

---

## 5. SVIE counter-systems (new)

| System | Counter to Honda |
|--------|------------------|
| **AXIOM** | Real 12-speed dog ratios + 4 ms GDSA — rubber-band index **0** |
| **e:HEV Bridge** | Dual-motor hybrid mate **without** belt/eCVT cones |
| **HERT turbine rev-match** | Physical RPM management vs S+ software RPM theatre |

See [`axiom-anti-cvt.md`](axiom-anti-cvt.md) and [`honda-rd-gap-map.md`](honda-rd-gap-map.md).
