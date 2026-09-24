# Thermal / Oil System & BOM Cost Envelope

## Thermal & dry-sump ([`specs/thermal_oil_system.yaml`](../specs/thermal_oil_system.yaml))

Dry-sump 3-stage scavenge sized for 10,000 RPM aeration control; piston oil jets support H2 hotspot suppression. Head-priority conformal cooling targets ≤140 °C injector boss metal.

## BOM diligence envelope ([`specs/bom_cost_estimate.yaml`](../specs/bom_cost_estimate.yaml))

```bash
python -m svie_physics.bom_cost
python -m svie_physics.bom_cost --with-chassis
```

| Scope | ≈ USD @ 5k UPY |
|-------|----------------|
| Powertrain subtotal | **14,710** |
| With chassis monocoque share | **26,710** |

Not a supplier quote — order-of-magnitude for OEM licensing conversations. LPBF heads and DEVA actuators dominate the bill.
