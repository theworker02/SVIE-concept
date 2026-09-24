# Addon Features — DRY-SUMP-X · PULSE-EGR · SILK-MOUNT · RANGE-BRIDGE · KERS-BLEND

**Release:** 1.4.0  
**Validation context:** [`validation-report.md`](validation-report.md)

---

## DRY-SUMP-X (engine)

Three-stage scavenge pump holding crankcase ≤ −5 kPa at 10k RPM, feeding **OIL-SPINE**. Enables sustained lateral-g oil control for sports body loads.

**Mfg:** External scavenge pump + windage tray; galleries shared with OIL-SPINE gun-drills.

## PULSE-EGR (engine / emissions)

Pulsed cooled EGR (~18% mass at lean cruise) targeting ~42% NOx index reduction vs no-EGR lean map — complements AETHER-IGN and H₂ water-DI.

**Mfg:** Fast solenoid EGR valve + stainless cooler; CHRONOS-aware scheduling.

## SILK-MOUNT (body / NVH)

Active hydraulic mounts: +10 dB idle isolation vs passive, ≤45 W on NEXUS-48, triggered when SONIC index exceeds 0.65.

**Mfg:** Tier-1 active mount modules; CASMIR-compatible wiring harness.

## RANGE-BRIDGE (hybrid add-on)

Series range-extender mode on e:HEV Bridge path: 55 kW engine → 0.93 η gen → **51.15 kW** DC bus with 8 kWh buffer. AXIOM mechanical path disabled in series.

**Mfg:** Shared generator / inverter with existing hybrid bridge BOM.

## KERS-BLEND (controls)

Kinetic recovery event captures 62% of 180 kJ recoverable → **111.6 kJ** into motor path with brake fade compensation via BLEND.

**Mfg:** Software + existing motor; no new rotating hardware beyond RANGE-BRIDGE class.

---

```bash
python -m svie_physics.addon_features
python -m svie_physics.validate
```
