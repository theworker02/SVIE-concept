# SVIE Breakthrough Subsystems — Beyond Production Horizon

**Audience:** Honda R&D / Tier-1 IP evaluation  
**Status:** Concept research — deliberately more aggressive than production Earth Dreams packaging  
**Sources:** Honda FC Technical Review Vol.37, Honda ISS electrolysis program, published H₂ expansion patents (Ford et al.), chassis torsion literature (Glickenhaus 35 kNm/deg class)

---

## Why these features exist

Honda’s 2024–2025 public R&D weight is on **hydrogen fuel cells**, **high-ΔP electrolysis** (including ISS/lunar regenerative systems), and **acoustic-emission (AE) damage analysis of high-pressure containers**. Production ICE teams still optimize liquid DI + VTEC/VTC.

SVIE already proposes supercritical flash gasoline vaporization. The breakthrough layer asks: *what becomes possible if we treat the car as a hydrogen-aware, structurally instrumented, cryogenically assisted lean-burn platform?*

These features are designed so Honda diligence teams recognize **their own technology themes** applied in combinations that do not exist on a showroom vehicle today.

---

## Feature catalog

### 1. CCD — Cryogenic Charge Densification

HERT cold expansion exits near **130 K** isentropically. Published expanders (Ford US6516615, recent FC-truck expanders) recover **shaft or electric work only**.

CCD routes that cold sink through a charge-air jacket **before** GDSA scavenge / intake feed:

| Effect | Value |
|--------|-------|
| Shaft recovery (cold mode) | ≈ 52 kW (70 hp) |
| Intake density gain (capped diligence target) | **+8.5%** |
| Turbo lag | None (no compressor spool) |

**Honda appeal:** Free volumetric efficiency without electrical compressor load — complements high-BTE lean maps.

Executable: `python -m svie_physics.breakthrough`

---

### 2. CASMIR — Chassis Acoustic Structural Modal Integrity Relay

Honda R&D has published **AE technology for high-pressure H₂ container damage analysis**. CASMIR transplants that sensing philosophy onto monocoque **Nodes A–D** (rear diffuser bulkhead, engine tub interface, tunnel web, DKIS shock towers).

- 500 kHz AE sampling at four stress nodes  
- Burst detection triggers DKIS hydraulic derate + torque limit  
- Closes the loop between the **35 kNm/deg** torsional target and live structural health  

**Honda appeal:** Reuses a competence Honda already funded for tanks; applying it to *chassis load paths* is unexpected on a sports car.

---

### 3. PSI — Plasma Spear Ignition

Nanosecond pulsed plasma (~80 ns, ~15 mJ) stabilizes **dry gaseous** SVIE charges at AFR up to **35:1**, where conventional spark kernels quench.

**Honda appeal:** Earth Dreams BTE ceilings are mixture + ignition limited. Plasma + dry SFV gas + DEVA Miller/Atkinson is a package Honda has not productized.

---

### 4. DKIS-TFF — Torsion Feedforward Interconnected Suspension

Literature shows interconnected suspensions raise roll stiffness without proportional warp stiffness. DKIS-TFF schedules hydraulic gains from **measured twist rate** (CASMIR + IMU) so roll distribution tracks the design \(K_\theta / K_{\phi} \ge 12\) criterion (SVIE target ratio = **14.0** at 35,000 / 2,500 Nm/deg).

**Honda appeal:** Handling calibrators usually treat chassis twist as a static assumption. Live feedforward is a new control degree of freedom.

---

### 5. Dual-Mode SFV / H₂ Co-Rail

Shared gaseous injectors accept either supercritical gasoline vapor **or** HERT-conditioned hydrogen (0.8–4.2 MPa). Aligns with Honda’s hydrogen business (CR-V e:FCEV, FC module manufacturing) while preserving gasoline SFV for non-H₂ markets.

**Honda appeal:** One injector/rail architecture for two fuel futures.

---

### 6. Orbital Water Buffer — Regenerative Electrolysis Micro-Stack

Honda’s ISS / lunar regenerative FC work centers on **high-differential-pressure electrolysis**. A 40 g H₂ micro-buffer from recovered condensate supports **CEB catalyst light-off** and cold-start HEX assist for ~12 s.

**Honda appeal:** Terrestrial crossover of a space tech theme Honda publicly champions — unexpected in a roadster/GT package.

---

## Differentiation vs known prior art

| Concept | Known in literature? | SVIE unique combination |
|---------|----------------------|-------------------------|
| H₂ tank expansion turbine | Yes (Ford, FC expanders) | + GDSA pneumatic shifts + intake scavenge + CCD |
| AE on H₂ tanks | Yes (Honda) | AE on chassis nodes + DKIS derate |
| Plasma ignition | Academic | + dry SFV gas + 35:1 + DEVA |
| Interconnected suspension | Yes | + live \(K_\theta\) feedforward |
| Dual fuel rails | Partial (DI+PFI) | Same rail for SFV gasoline vapor **and** H₂ |

---

## Machine-readable source

[`specs/breakthrough_subsystems.yaml`](../specs/breakthrough_subsystems.yaml)

Claim-chart additions: see [`claim-charts.md`](claim-charts.md) Claim Sets 5–7.
