# Lighting Design — Headlamps & Signature

**Spec:** [`specs/lighting_headlamp.yaml`](../../specs/lighting_headlamp.yaml)  
**Render:** `design/renders/svie-headlight-detail.png`

---

## Signature concept

Vertical **instrument-stack** lamps: stacked optical modules read like monospace tick marks. A thin **amber DRL filament** echoes the brand vapor line. Smoked outer lens, machined heatsink edge.

| Function | Technology | Notes |
|----------|------------|-------|
| DRL | Amber LED filament | Always-on signature |
| Low beam | LED projector | Adaptive matrix optional |
| High beam | LED / matrix | Auto-leveling |
| Turn | Sequential tick LEDs | Vertical cascade |
| Side marker | Integrated | ECE / FMVSS variants |

---

## Photometry targets (design)

| Metric | Target |
|--------|--------|
| Low-beam luminous flux (assembly) | ≥ 1100 lm |
| DRL intensity (per side) | ECE R87 / FMVSS compliant class |
| Power draw (both sides, DRL+low) | ≤ 45 W |
| Aim adjust | Manual + auto-level |

---

## Construction

1. Die-cast Al heatsink housing  
2. Multi-board LED PCBs (NEXUS-48 feed via lighting ECU)  
3. Optical stack: projector + reflector + light-guide filament  
4. Two-shot polycarbonate outer lens (hardcoat)  
5. Hermetic seal; IP6K9K wash target  

**Mfg:** Tier-1 lighting module; SVIE owns signature CAD and ECU calibration maps.

---

## Rear lamp

Thin horizontal amber/red light-bar spanning decklid; center brake emphasis; reverse white ticks at outboard. Same instrument grammar as the front.
