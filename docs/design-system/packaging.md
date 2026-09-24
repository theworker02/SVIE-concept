# Vehicle Packaging — Internals Placement

**Spec:** [`specs/packaging_layout.yaml`](../../specs/packaging_layout.yaml)  
**Render:** `design/renders/svie-packaging-cutaway.png`

---

## Longitudinal zones (front → rear)

| Zone | Contents |
|------|----------|
| **Z0 Front** | Crash structure, radiators, SFV HEX banks, washer, lighting ECUs |
| **Z1 Frunk** | Soft luggage 80 L, optional 12 V aux |
| **Z2 Cabin** | Occupants, HVAC, HMI, SILK-MOUNT tops |
| **Z3 Mid** | Engine (5.2 L SFV *or* 3.57 L V8-HR), DRY-SUMP-X, OIL-SPINE, DEVA controllers |
| **Z4 Transaxle** | AXIOM / HERT / FLUX-SHIFT, GDSA tanks |
| **Z5 Underfloor** | CELL-VAULT (H₂ or battery), fuel / H₂ lines protected |
| **Z6 Rear** | Diffuser / AERO-SKIN actuators, mufflers / H₂ vents, luggage niche |

---

## Hard points (design)

| System | Location rule |
|--------|---------------|
| SFV rail / CRYO-RAIL | Engine valley → injectors; PCM jackets clear of exhaust |
| NEXUS-48 battery | Ahead of rear bulkhead / vault edge |
| SENTINEL sensors | Cabin + underhood + vault per safety spec |
| Wiring backbone | Left + right sills (zone harness trunk) |
| Exhaust / HEX | Side-exit heat exchangers before turbo/collector path |

---

## Mass / balance intent

Keep ~48/52 front/rear as chassis SoT. Vault mass on wheelbase center; engine slightly ahead of rear axle for mid-ship.

---

## Serviceability

- Engine cover removes for DEVA/rail access  
- Side service panels for FLUX clutch stack  
- Vault inspection ports for SENTINEL / CASMIR pads  

This packaging sheet is the **vehicle integration idea** that ties powertrain specs to the body design system without rewriting physics goldens.
