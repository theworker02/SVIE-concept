# Competitive Matrix (Public Diligence)

Comparative posture vs common production / public architectures.  
**Not** an assertion of superiority on measured dyno data — SVIE remains TRL-3 software.

| Dimension | Typical GDI V8 | Belt CVT hybrid | Honda-class e:HEV / S+ (public) | **SVIE package** |
|-----------|----------------|-----------------|----------------------------------|------------------|
| Fuel preparation | Liquid spray | Liquid / Atkinson maps | Liquid + electric path | **SFV dry gas flash** |
| Valvetrain | Cam / VTEC-class | Cam | Cam + electrified drive | **DEVA camless** |
| Ratio device | DCT / AT / MT | Belt CVT | e-CVT / S+ discrete assist | **AXIOM RBI = 0** |
| Exhaust recuperation to fuel | Rare at supercritical | N/A | Limited | **HEX → SFV ladder** |
| H₂ DI high-RPM V8 concept | Uncommon | N/A | Fuel-cell / ICE H₂ research | **V8-HR 3.57 L pack** |
| Runnable OEM portal | Rare | Rare | Internal tools | **Ships in-repo** |
| Golden-locked thermo | Varies | Varies | Internal | **pytest suite** |
| Claim charts ↔ code map | Often missing | Often missing | Confidential | **In-repo drafts** |
| Belt slip / TSB evidence dossier | N/A | Known issues | Public TSBs exist | **Documented** |

## Decision guide for buyers

| If your priority is… | Start with package |
|----------------------|--------------------|
| Fuel-path differentiation | `SFV-CORE` |
| Camless / H₂ ICE | `DEVA-HR` |
| Kill CVT rubber-band | `AXIOM-DRIVE` |
| 48V / NVH / H₂ safety ops | `OPS-STACK` |
| Controls coordination | `CONTROL` |
| Structures + BOM envelope | `STRUCTURE` |
| Everything | Full monorepo asset deal |

Sources for comparative claims: [`cvt-evidence-dossier.md`](../cvt-evidence-dossier.md), [`honda-rd-gap-map.md`](../honda-rd-gap-map.md), [`honda-e-hev-teardown.md`](../honda-e-hev-teardown.md).
