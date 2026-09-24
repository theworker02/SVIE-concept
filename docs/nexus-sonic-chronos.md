# NEXUS-48, SONIC, SENTINEL, CHRONOS — Next System Wave

## NEXUS-48 ([`specs/nexus_48.yaml`](../specs/nexus_48.yaml))

48V P1 ISG spine sized so **BSG continuous 12 kW > DEVA+aux ≈ 9.06 kW @ 8500 WOT** (≈2.9 kW margin). Recuperation feeds DEVA directly — literature P0/P1 mild-hybrid pattern, crank-integrated for 10k RPM (no accessory belt at redline).

```bash
python -m svie_physics.nexus_48
```

## SONIC + AETHER ([`specs/sonic_nvh.yaml`](../specs/sonic_nvh.yaml))

Flat-plane L-R firing, **180° exhaust pulses**, no bundle-of-snakes. Secondary shake index vs 93 mm GT350-class stroke: **(75/93)² ≈ 0.65** (~35% lower geometric second-order). AETHER active exhaust ties bark blips to AXIOM/GDSA upshifts.

## SENTINEL ([`specs/sentinel_safety.yaml`](../specs/sentinel_safety.yaml))

9 H2/AE sensors, **50 ms** isolation (tank solenoid, HERT bypass, 48V contactors). Tank AE channels borrow Honda’s published container AE theme — applied to *vehicle safety envelope*, not just tanks in the lab.

## CHRONOS ([`specs/chronos_cold_start.yaml`](../specs/chronos_cold_start.yaml))

Orchestrated cold start: NEXUS precharge → Orbital H2/CEB → ISG crank + late DI/PSI → H2-SCR light-off → lean/AXIOM ready. **First fire 3.7 s**, aftertreatment active **11.7 s**.

## TRL roadmap ([`specs/trl_roadmap.yaml`](../specs/trl_roadmap.yaml))

Repo locks **TRL-3** (analytical proof). Path to TRL-9 licensing packages listed for OEM staging.
