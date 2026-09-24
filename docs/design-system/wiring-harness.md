# Wiring Harness Design

**Spec:** [`specs/wiring_harness.yaml`](../../specs/wiring_harness.yaml)

Production-intent harness architecture for the SVIE vehicle design package. Zone topology, gauges, and connector families — suitable for Tier-1 quoting.

---

## Topology

```text
[ Front PDU / Lighting ECU ]
        │
   ┌────┴────┐
   │  Backbone trunk (sills)  │
   └────┬────┘
        ├── Zone A: Front power + lamps + HEX fans
        ├── Zone B: Cabin HMI + HVAC + SENTINEL cabin
        ├── Zone C: Engine DEVA / SFV / ignition / sensors
        ├── Zone D: Transaxle AXIOM / FLUX / GDSA
        ├── Zone E: Vault + NEXUS-48 + H₂ / HV
        └── Zone F: Rear aero + lamps + camera
```

Star points at **firewall** and **rear bulkhead** sealed pass-throughs. No daisy-chain through CELL-VAULT without conduit.

---

## Power domains

| Domain | Voltage | Feeds |
|--------|---------|-------|
| LV always | 12 V | Lamps, locks, SENTINEL wake |
| LV switched | 12 V | Cabin, HVAC, accessories |
| NEXUS | 48 V | DEVA, SILK-MOUNT, AERO actuators, ISG |
| HV / H₂ sense | Isolated | Vault, tank AE (CASMIR), contactors |

---

## Cable & connector classes

| Class | Gauge / type | Use |
|-------|--------------|-----|
| Signal | 0.35–0.5 mm² TXL / FLRY | Sensors, CAN/FD |
| Power LV | 1.5–6 mm² | Fans, pumps |
| 48 V | 6–16 mm² | DEVA rails, actuators |
| Shielded twisted | CAN-FD / Ethernet | Backbone data |
| HV orange (if battery vault) | Per ISO 6469 | Contactors |

Connectors: sealed USCAR / OEM family; coding by zone color ring (graphite body, amber latch for 48 V).

---

## Data buses

| Bus | Role |
|-----|------|
| CAN-FD Powertrain | Engine, AXIOM, VECTOR |
| CAN-FD Body | Lamps, locks, HVAC |
| Ethernet backbone | HMI, cameras, diagnostics |
| LIN | Switches, simple actuators |

---

## Length & mass budget (design)

| Item | Target |
|------|--------|
| Total copper length (agg.) | ≤ 1.8 km |
| Harness mass | ≤ 38 kg |
| Max voltage drop (48 V DEVA feed) | ≤ 2% at peak |
| Bend radius | ≥ 5× OD |

---

## Manufacturing

1. Formboard layout per zone  
2. Automated cut/crimp; ultrasonic weld splices where approved  
3. 100% continuity + HiPot on 48 V / HV  
4. Coverings: PET braid in cabin; convoluted conduit in engine / vault  
5. Build breakouts match service panels in packaging doc  

---

## Validation hooks

Harness design KPIs are golden-locked in YAML and checked by `svie_physics.design_system`.
