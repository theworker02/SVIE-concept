# SVIE Validation Report

**Release:** 1.4.0  
**Scope:** Software diligence package — analytical + golden-vector validation  
**Status:** Concept engineering (TRL-3). Not dyno / EPA certified.

> This report records what has been **measured in-repo** (pytest), what is **literature-grounded**, and what remains **unvalidated hardware**.

Executable rollup:

```bash
python -m pytest packages/physics-engine/tests -q
python -m svie_physics.validate
```

---

## 1. In-repo measurement (software)

| Suite | Result (this release baseline) | Notes |
|-------|--------------------------------|-------|
| Golden WOT / HEX / HEM / piezo | **PASS** | Locks ṁ_fuel 28.28 g/s, Q̇ HEX ≈ 23.2 kW, A_o 0.431 mm² |
| Chassis / HERT / GDSA / gears | **PASS** | Torsion / expansion / shift models |
| V8-HR architecture | **PASS** | Displacement / MPS / rod ratio |
| DEVA / H₂ / BOM | **PASS** | Power / λ / cost envelope |
| CVT / AXIOM | **PASS** | RBI = 0; bridge no belt |
| NEXUS / SONIC / TRL | **PASS** | Bus / NVH index / TRL-3 |
| BLEND / MIRAGE / VECTOR | **PASS** | Control layer |
| Platform+ / MFG | **PASS** | Engine/trans/body next-wave + 15 routes |
| Demo / inventory | **PASS** | Acquisition walkthrough |

**Verdict:** All published golden vectors are currently green. Re-run before any diligence meeting.

---

## 2. Literature / industry grounding

| SVIE claim | Grounding | Confidence | Gap |
|------------|-----------|------------|-----|
| PTWA bore ~**0.15 mm** | Ford Shelby GT500 production PTWA cited at **150 µm**; patents note 25–150 µm finished ranges | **High** (process precedent) | SVIE durability on H₂ DI not proven |
| HEM choked flash orifice | Classical two-phase HEM / cavitation number used in injector literature | **Medium** | Needs spray-vessel calibration |
| Electromagnetic valvetrain power ∝ RPM | WSEAS EMVT study: consumption nearly proportional to speed; transition dominates | **Medium–High** | DEVA absolute watts need bench |
| DCT / dual-clutch overlap shifts | DCT literature: torque + inertia phases; sync often **0.1–1.5 s** class | **High** (context) | FLUX-SHIFT **≤8 ms interrupt** is an **aggressive design target**, not a measured DCT sync time |
| Belt CVT slip / efficiency loss | ICCT / slip literature + public TSB themes in dossier | **Medium** | Vehicle-specific dyno still required |
| Active aero ΔCd / downforce | Production DRS / active diffuser class devices exist (motorsport / hypercars) | **Medium** | SVIE actuator loads unproven |
| LPBF conformal heads | SAE papers on LPBF AlSi10Mg heads surviving high cycle counts | **Medium** | Cost / porosity / HIP gates remain |
| Camless lean / H₂ DI | Research engines exist; production EMVT rare | **Low–Medium** | Full system integration unproven |

---

## 3. Consistency matrix (cross-spec)

Checked by `svie_physics.validate`:

| Check | Expected | Status |
|-------|----------|--------|
| `manufacturing_master.ptwa` == `ring_zero.ptwa` | 0.15 mm | Enforced |
| AXIOM RBI == FLUX RBI | 0 | Enforced |
| NODE torsion > prior chassis class | ≥ 35k → 38k Nm/deg | Enforced |
| Inventory specs ≥ 35 | Live count | Enforced |
| TRL current == 3 | Roadmap golden | Enforced |
| Demo ṁ_fuel matches engine golden | 28.28 g/s | Enforced |

---

## 4. What is *not* validated

- Brake thermal efficiency 48–52% (design **target**)  
- Dyno BSFC / WLTP / EPA certification  
- Injector coking / supercritical gasoline materials endurance  
- DEVA seating fail-safe under oil starvation  
- FLUX-SHIFT 7 ms interrupt on a physical gearbox  
- Crash energy CELL-VAULT under regulatory barriers  
- Production cost at 5k units/year (order-of-magnitude only)  

See [`acquisition/RISK-REGISTER.md`](acquisition/RISK-REGISTER.md) and [`acquisition/HARDWARE-ROADMAP.md`](acquisition/HARDWARE-ROADMAP.md).

---

## 5. Recommended next validation gates (hardware)

1. **G1** — Piezo SFV orifice spray vessel vs HEM model (±5% ṁ)  
2. **G1b** — PTWA coupon ring-pack friction vs RING-ZERO −12% FMEP claim  
3. **G2** — Single DEVA valve energy vs `deva_power`  
4. **G2b** — Dual-clutch overlap rig vs FLUX ≤8 ms *torque hole* (not full sync time)  
5. **G3** — Single-cylinder SFV or H₂ DI  

---

## 6. New features introduced alongside this report (1.4.0)

| ID | Domain | Purpose |
|----|--------|---------|
| **DRY-SUMP-X** | Engine | Dry-sump scavenge tied to OIL-SPINE for high-g oil control |
| **PULSE-EGR** | Engine | Pulsed cooled EGR for lean SFV / H₂ NOx |
| **SILK-MOUNT** | Body / NVH | Active mounts driven by SONIC index |
| **RANGE-BRIDGE** | Hybrid | Series range-extender power budget on e:HEV Bridge |
| **KERS-BLEND** | Controls | Kinetic recovery blend into BLEND brake path |

Each has YAML + golden tests + manufacturing note in the master plan addendum.
