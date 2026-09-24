# SVIE Vehicle Design System

**Status:** Production-ready *design package* (parallel to powertrain IP)  
**Release:** 1.3.0  
**Posture:** Design intent + manufacturable specs — **not** a substitute for the main acquisition / physics plan in `Acquisition.md`.

> Use this system when diligence asks “what does the car look like, how is it wired, how is it packaged, how does the cabin feel?”  
> Powertrain truth remains `specs/` thermodynamics + golden tests.

---

## Hierarchy

| Layer | Owns | Entry |
|-------|------|-------|
| **Brand / UI tokens** | Graphite · ink · amber | [`brand/`](../../brand/) |
| **Vehicle design language** | Form, lighting signature, materials | this folder |
| **Exterior body** | Surfaces, aero skins, shutlines | [`exterior-body.md`](exterior-body.md) |
| **Lighting** | Headlamp / DRL / tail | [`lighting.md`](lighting.md) |
| **Cabin** | Interior ergonomics & HMI | [`cabin.md`](cabin.md) |
| **AETHER-OS** | Analog-first OS + CarPlay Ultra guest | [`aether-os.md`](aether-os.md) |
| **Packaging** | Hard-point layout of systems | [`packaging.md`](packaging.md) |
| **Wiring harness** | Backbone, zones, gauges | [`wiring-harness.md`](wiring-harness.md) |
| **Renders** | Concept visuals for diligence | [`../../design/renders/`](../../design/renders/) |

Machine SoT: `specs/design_*.yaml`, `specs/wiring_harness.yaml`, `specs/lighting_headlamp.yaml`, `specs/body_exterior.yaml`, `specs/cabin_layout.yaml`, `specs/packaging_layout.yaml`, `specs/aether_os.yaml`, `specs/carplay_ultra.yaml`, `specs/analog_hmi.yaml`.

---

## Design principles (production)

1. **Instrument, not theater** — amber is a measurement accent, never neon decoration.  
2. **One character line** — a single hard shoulder crease carries brand recognition.  
3. **See the machine** — HEX ducts, NODE-CAST nodes, and CELL-VAULT edges may read as designed structure, not covered shame.  
4. **Harness as architecture** — zone harnesses follow sill / bulkhead logic; no spaghetti under carpets.  
5. **Lighting as typography** — vertical LED stacks read like mono ticks, matching portal UI.  
6. **Analog primacy** — one guest glass max; milled metal and needles beat menu trees. CarPlay Ultra is a guest.

---

## Palette (vehicle)

| Token | Hex | Use on car |
|-------|-----|------------|
| Graphite body | `#12151A` | Primary paint |
| Steel trim | `#7A8A9A` | Bezels, mesh |
| Ink highlight | `#E8ECF1` | Badges, stitch |
| Amber signal | `#D4A017` | DRL filament, interior ticks |
| Carbon naked | woven 2×2 | Tub sill, diffuser |

---

## Portal

View interactively: **`/design`** · **`/hmi`** (AETHER-OS live mock).
