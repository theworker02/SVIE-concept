# DEVA — Digital Electromagnetic Valve Actuation

**Spec:** [`specs/deva_valvetrain.yaml`](../specs/deva_valvetrain.yaml)  
**Model:** `python -m svie_physics.deva_power`

## Summary

Camless dual-solenoid actuation with optional PM latch, soft-landing control, and per-cycle Otto / Miller / Atkinson switching. Electrical power scales with engine speed (literature: EMVT demand ≈ proportional to RPM for fixed transition energy).

| Condition | Assumption | Electrical power |
|-----------|------------|------------------|
| 8500 RPM WOT | 3.2 J/transition, PM latch (no hold) | **≈ 7.26 kW** |
| 3000 RPM cruise | 2.0 J/transition + hold | **≈ 1.86 kW** |

Cruise modes use longer transitions and partial valve deactivation to cut copper loss — matching published EMVT optimization findings.
