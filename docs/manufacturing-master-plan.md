# SVIE Manufacturing Master Plan

**Status:** Concept engineering — process routes for OEM diligence, not a quoted factory SOW  
**Release:** 1.3.0  
**Companion SoT:** [`specs/manufacturing_master.yaml`](../specs/manufacturing_master.yaml)

> Every new engine, transmission, and body feature in this release has an explicit **process route**, **critical characteristics**, **capacity assumption**, and **gate** back to YAML golden numbers.

---

## 1. Manufacturing philosophy

| Principle | Practice |
|-----------|----------|
| Cast / forge where volume wins | A356 block, AlSi head bulk, steel gear blanks |
| Add where geometry wins | LPBF conformal heads, lattice carriers, cooling inserts |
| Coat where friction wins | PTWA bores (~150 µm), DLC rings/pins |
| Bond where mass wins | CFRP tub + cast Al nodes (NODE-CAST) |
| Instrument where safety wins | CASMIR AE nodes co-cured / co-bonded |

Annual diligence capacity assumption for cost models: **5,000 units/year** (halo / specialty), not 200k mainstream.

---

## 2. Engine manufacturing routes

### 2.1 Block — sand / semi-permanent mold + PTWA

| Step | Detail |
|------|--------|
| Alloy | A356-T6 deep-skirt |
| Process | Cosworth-class or SPMC; integrated 6-bolt ladder girdle |
| Bore prep | Rough hone → PTWA ferrous wire spray → finish plateau hone |
| PTWA thickness | **0.15 mm** nominal (Ford GT500-class precedent) |
| Critical CC | Bore cylindricity ≤ 8 µm; interbore bridge temp map |
| Gate | Matches `svie_v8_hr_357` / RING-ZERO friction model |

### 2.2 Heads — hybrid cast + LPBF inserts (CRYO-RAIL / conformal cool)

| Step | Detail |
|------|--------|
| Bulk | Gravity / semi-permanent AlSi10Mg or A356 |
| Inserts | LPBF conformal coolant + dual H₂ DI bosses (or full LPBF halo) |
| Join | Shrink-fit / HIP / braze per OEM materials board |
| Post | HIP optional; CNC decks; seat/guide press |
| Gate | DEVA boss stiffness + injector tip ΔT within H₂ DI map |

### 2.3 CRYO-RAIL fuel rail

| Step | Detail |
|------|--------|
| Tube | Stainless 316L drawn or LPBF manifold for prototype |
| Phase buffer | Welded PCM capsule jacket (paraffin / salt hydrate class) |
| Sensors | Rail P/T ports machined; SENTINEL-compatible H₂ variant |
| Leak test | Helium 1×10⁻⁶ mbar·L/s class target |
| Gate | Rail ΔT stability in `engine_cryo_rail` golden |

### 2.4 RING-ZERO pack

| Step | Detail |
|------|--------|
| Rings | Steel nitrided + DLC top; low-tension oil ring |
| Pins | DLC wrist pins; fracture-split rods 4340/4600 |
| Honing | Plateau finish matched to PTWA porosity |
| Gate | FMEP delta locked in `ring_zero` model |

### 2.5 OIL-SPINE girdle gallery

| Step | Detail |
|------|--------|
| Casting | Ladder girdle with cast-in oil spine + jet galleries |
| Machining | Gun-drill jets toward piston undersides / turbine feed |
| Cleanliness | ISO 4406 16/14/11 target before build |
| Gate | Oil pressure / jet flow in `oil_spine` golden |

**Detail doc:** [`engine-next-wave.md`](engine-next-wave.md)

---

## 3. Transmission manufacturing routes

### 3.1 AXIOM / HERT case

| Step | Detail |
|------|--------|
| Case | A380 HPDC or sand Al; ribbed for GDSA pneumatics |
| Shafts | Forged steel; shot peen fillets |
| Gears | Cut → carburize → grind; optional AM lattice *carriers* only |

### 3.2 FLUX-SHIFT dual-path preselect

| Step | Detail |
|------|--------|
| Clutches | Wet multiplate; paper / sintered OEM stack |
| Actuation | Electro-hydraulic valves; shared NEXUS-48 pump |
| Controls | MIRAGE twin-path firmware flash |
| Gate | Torque interrupt ≤ 8 ms in `flux_shift` model |

### 3.3 GEAR-MESH-AM carriers

| Step | Detail |
|------|--------|
| Process | LPBF 17-4PH or Ti-6Al-4V lattice carrier (halo) |
| Post | HIP + CNC spline interfaces |
| NVH | Lattice tuned to kill 1st mesh harmonic |
| Gate | Mesh force / NVH index in `gear_mesh_am` |

**Detail doc:** [`transmission-next-wave.md`](transmission-next-wave.md)

---

## 4. Body / chassis manufacturing routes

### 4.1 NODE-CAST hybrid body

| Step | Detail |
|------|--------|
| Tub | Autoclave or RTM CFRP monocoque |
| Nodes | Cast Al (A356) front/rear crash + suspension pickups |
| Join | Structural adhesive + rivets / flow-drill screws |
| Tolerance | Hard-point ±0.5 mm after cure |
| Gate | Torsion ≥ monocoque golden + node SF ≥ 1.8 |

### 4.2 AERO-SKIN active surfaces

| Step | Detail |
|------|--------|
| Panels | Prepreg carbon + foam core diffuser / DRS wing |
| Actuators | 48 V linear; sealed against stone spray |
| Seals | PTFE / silicone aero gaps |
| Gate | Δ downforce / Cd in `aero_skin` |

### 4.3 CELL-VAULT structural energy vault

| Step | Detail |
|------|--------|
| Structure | Al extrusions + CFRP shear panels under floor |
| H₂ option | Type IV tank cradle with CASMIR AE pads |
| Battery option | Module trays with crush cans |
| Crash | IIHS / FMVSS conceptual load paths (sim only) |
| Gate | Intrusion / energy absorption indices in `cell_vault` |

**Detail doc:** [`body-platform.md`](body-platform.md)

---

## 5. Factory cells (indicative)

| Cell | Capex order* | Notes |
|------|--------------|-------|
| Block cast + PTWA | High | Shared with OEM PTWA line if partnered |
| Head hybrid / LPBF | High | Low volume; 2-laser large envelope |
| Trans gear / clutch | Medium | Conventional Tier-1 |
| CFRP tub + NODE-CAST | High | Aerospace-auto hybrid |
| Final assembly | Medium | Specialty sports line |

\*Order-of-magnitude only — rebuild bottoms-up in buyer cost eng.

---

## 6. Quality & gates

1. Every process route above maps to a **YAML golden** and a **pytest**.  
2. Hardware G1–G4 in [`acquisition/HARDWARE-ROADMAP.md`](acquisition/HARDWARE-ROADMAP.md) must re-lock YAML on pass/fail.  
3. Cleanliness, NDT (PTWA UT / LPBF CT sample), and adhesive bond coupons are **non-negotiable** before mule build.

## 7. Addendum — 1.4.0 addon manufacturing notes

| Feature | Process note |
|---------|--------------|
| DRY-SUMP-X | External 3-stage scavenge; share OIL-SPINE galleries |
| PULSE-EGR | Fast solenoid + stainless EGR cooler; NOx map calibration cell |
| SILK-MOUNT | Buy Tier-1 active mounts; NEXUS-48 harness |
| RANGE-BRIDGE | Generator/inverter shared with e:HEV Bridge BOM |
| KERS-BLEND | Controls calibration on existing motor; BLEND firmware |

Validation before mule: `python -m svie_physics.validate` must be green.
