# SVIE Executive Brief

**One page for OEM / strategic leadership**  
**Release:** 1.3.0 · **Package:** production-ready acquisition · **Hardware TRL:** 3

---

## The offer

A complete, **reproducible** powertrain IP monorepo — not a slide deck. Acquirers receive runnable physics, YAML specs, golden tests, SAE-style docs, vehicle design + AETHER-OS, compliance *paths*, supply-chain map, deal room, brand, CLI demo, and an OEM portal with a live readiness scorecard.

```text
Verify in <10 minutes:
  pytest              →  golden vectors green
  acquisition_suite   →  production_ready_acquisition: true
  portal              →  /acquisition + /pitch + /hmi
```

## Why it matters

| Gap in public ICE / hybrid posture | SVIE answer |
|------------------------------------|-------------|
| Liquid GDI wetting / dilution | SFV dry gaseous charge |
| Cam-limited cycle agility | DEVA camless + VCR scheduling |
| CVT rubber-band / belt slip | AXIOM discrete drive, RBI = **0** |
| Fragmented ops / NVH / H₂ safety | NEXUS · SONIC · SENTINEL · CHRONOS |
| Screen-farm cabins | AETHER-OS analog-first + CarPlay Ultra guest |
| Diligence as PDFs | Close-ready data room + term sheet outline |

## Headline locked metrics

| Metric | Value | Proof |
|--------|-------|-------|
| ṁ fuel @ WOT | 28.28 g/s | `test_air_fuel_wot_baseline` |
| HEX duty | 23.2 kW | `test_heat_exchanger_duty` |
| Orifice required | 0.431 mm² | `test_hem_choked_and_orifice` |
| AXIOM rubber-band | 0 | `test_axiom_kills_rubber_band` |
| Acquisition score | ≥85 + gates | `test_acquisition_suite` |

## Commercial framing (recommended)

**Exclusive automotive field-of-use license + buyout option**, escrow at `v1.3.*`, optional earnout on hardware/IP gates. See [TERM-SHEET.md](TERM-SHEET.md) · [Acquisition.md](../../Acquisition.md).

## What you are *not* buying (yet)

Dyno certificates, EPA/WLTP homologation, ASIL/21434 certificates, production tooling, or firm supplier quotes. Those follow the **hardware roadmap** after close.

## Next 48 hours for a serious buyer

1. NDA → archive `v1.3.0`  
2. Run `pytest` + `python -m svie_physics.acquisition_suite`  
3. Open `/acquisition` then `/pitch` on the portal  
4. Schedule 2-day technical walkthrough + term-sheet mark-up  

**Contact:** update commercial channel before external circulation.
