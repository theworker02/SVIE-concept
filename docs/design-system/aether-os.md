# AETHER-OS — Analog-First Vehicle Operating System

**Release:** 1.3.0  
**Posture:** Production-ready *HMI / OS design package* (parallel to powertrain IP)  
**Specs:** [`aether_os.yaml`](../../specs/aether_os.yaml) · [`carplay_ultra.yaml`](../../specs/carplay_ultra.yaml) · [`analog_hmi.yaml`](../../specs/analog_hmi.yaml)

> **Design law:** The car must feel luxurious with **hands on metal**, not a glass tablet farm.  
> Screens exist to *host* **Apple CarPlay Ultra** and sparse legal telltales — never to replace dials, toggles, or needles.

---

## 1. Philosophy

| Principle | Meaning |
|-----------|---------|
| **Analog primacy** | Speed, tach, temp, fuel/H₂, HVAC, volume, drive mode = physical |
| **One guest glass** | A single recessed center display for CarPlay Ultra / sparse native map |
| **Hardware is truth** | Turning a climate dial always works — even if the phone dies |
| **Ultra as guest** | CarPlay Ultra may *mirror* climate / gauges / audio; it does not own them |
| **Quiet luxury** | Graphite · brushed Al · leather · amber jewels — watchmaking, not smartphone |

Inspired by grand-touring craft and the industry move to **CarPlay Ultra** (deep vehicle integration across cluster + center, OEM look-and-feel, climate / audio / vehicle settings via Siri and UI — first shipped with Aston Martin, 2025). SVIE’s twist: **keep the cabin analog** while still supporting Ultra’s depth.

---

## 2. System architecture

```text
┌─────────────────────────────────────────────────────────┐
│                    AETHER-OS Kernel                     │
│  Safety · SENTINEL · VECTOR · power modes · telltales   │
└───────────────┬─────────────────────┬───────────────────┘
                │                     │
     ┌──────────▼──────────┐   ┌──────▼──────────────┐
     │  Analog HMI Plane   │   │  Glass Guest Plane  │
     │  needles · dials    │   │  CarPlay Ultra      │
     │  toggles · rollers  │   │  (when iPhone linked)│
     │  jewel lamps        │   │  + thin native strip │
     └──────────┬──────────┘   └──────┬──────────────┘
                │                     │
                └──────────┬──────────┘
                           │
              Vehicle services (NEXUS-48, CAN-FD, Ethernet)
```

- **Kernel** always runs on the vehicle ECU domain (ASIL-minded partitioning for SENTINEL).  
- **Analog plane** is hardwired / local MCU — no cloud, no phone required.  
- **Glass plane** hosts CarPlay Ultra wirelessly (iPhone 12+, OS per Apple requirements) with SVIE graphite/amber theme.

---

## 3. Physical control map (luxury stack)

| Control | Type | Function |
|---------|------|----------|
| Speedometer | Analog needle + laser-etched dial | Primary speed |
| Tachometer | Analog needle | Engine / motor revs |
| Temp / oil / vault | Small analog or jeweled strips | Critical temps |
| HVAC L/R | Milled dual rotary | Temperature |
| Fan | Detented rotary | Airflow |
| Face/foot/defrost | 3-position metal toggle or rotary | Mode |
| Volume | Knurled roller | Audio |
| Drive mode | Rotary: Tour · Sport · Track · Series-RE | VECTOR / RANGE-BRIDGE |
| SFV / H₂ | Guarded metal toggle | Fuel path |
| AXIOM map | Toggle + stalk | Shift strategy |
| Hazard / SENTINEL | Hard red / amber jewels | Never menu-only |
| Light stalk | Traditional | Lamps / wipers |

Center glass: **≤ 10.25″** recessed, low-gloss, can **motor-retract** to a closed Al panel for pure analog evenings.

---

## 4. CarPlay Ultra integration (SVIE policy)

| Capability (Ultra class) | SVIE behavior |
|--------------------------|---------------|
| Instrument cluster themes | Optional when linked — **native analog needles remain visible** via hybrid cluster (physical dials + Ultra content in center aperture only) |
| Climate / audio / vehicle settings in Ultra | Allowed as *remote* of physical dials; dials always win on conflict |
| Navigation / media / messages | Center glass only |
| Siri vehicle control | Mapped to same services as dials |
| OEM look-and-feel | Graphite field, amber ticks, IBM-Plex-like mono captions |
| No phone | Analog plane + legal telltales only; glass shows clock / blank Al cover |

**We do not** put Ultra on door panels, mirrors, or seatbacks. **We do not** replace HVAC with touch-only.

---

## 5. Native AETHER UI (when Ultra idle)

Sparse content on the small glass (if open):

1. Clock + outside temp  
2. Optional map glance (offline tile cache)  
3. Maintenance / SENTINEL messages as typography, not cartoons  

Cluster native mode: analog faces with a **thin OLED caption** under the tach for gear / mode — not a full reconfigurable TFT wall.

---

## 6. Luxury materials & craft

| Element | Spec |
|---------|------|
| Dial faces | Lacquered graphite, sapphire optional on Signature trim |
| Needles | Counterweighted, amber tip illumination |
| Rotaries | CNC 6061 Al, diamond-knurl, soft magnetic detents |
| Toggles | Aircraft-grade guarded switches, jeweled LED caps |
| Surrounds | Full-grain leather + open-pore wood *or* technical Al (buyer trim) |
| Stow glass cover | Brushed Al with SVIE wordmark laser |

---

## 7. Software modules (AETHER-OS)

| Module | Role |
|--------|------|
| `aether.kernel` | Boot, watchdogs, power domains |
| `aether.safety` | SENTINEL, telltales, limp |
| `aether.analog` | Digitize dials, drive steppers/needles |
| `aether.guest` | CarPlay Ultra host / theme bridge |
| `aether.audio` | Mixer; Ultra media + vehicle chimes |
| `aether.vehicle` | VECTOR, BLEND, AXIOM, SFV services |

Versioned with vehicle: see YAML goldens.

---

## 8. Manufacturing / suppliers

- Analog cluster: Tier-1 gauge house (stepper or air-core)  
- Rotaries / toggles: Swiss or Japanese switch specialists  
- Glass: single OLED/LCD module, optical bonding, anti-reflection  
- CarPlay Ultra: Apple MFi / Ultra certification program with OEM theme pack  

---

## 9. Renders

- `design/renders/svie-hmi-cabin-analog.png` — full cabin  
- `design/renders/svie-hmi-analog-stack.png` — physical stack detail  

Portal: **`/hmi`** live mock of AETHER-OS.

---

## 10. Relationship to main plan

AETHER-OS is a **design / HMI package**. It does not replace thermodynamics, harness power domains, or Acquisition.md. It *consumes* NEXUS-48, SENTINEL, VECTOR, and cabin packaging as services.
