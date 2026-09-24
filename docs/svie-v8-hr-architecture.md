# SVIE-V8-HR — High-RPM Honda-Evolved Hydrogen DI Architecture

**Spec:** [`specs/svie_v8_hr_357.yaml`](../specs/svie_v8_hr_357.yaml)  
**Module:** `python -m svie_physics.engine_architecture`  
**Relation to 5.2 L baseline:** This is a **separate** high-RPM H₂ DI family (3.57 L), not a replacement of `svie_v8_52L` gasoline SFV WOT models.

---

## Design intent

Take Honda K20 / B16 principles — high volumetric efficiency, long rod ratio, integrated main girdle, RPM-tolerant stock-class internals — and evolve them for **direct-injection hydrogen** at **10,000+ RPM** with hybrid additive manufacturing.

```
[ DOHC 32V LPBF Cylinder Head ]
   conformal jackets + dual sequential H2 DI
              │
[ High-tumble pentroof chamber ]
              │
[ A356-T6 deep-skirt + PTWA bores ]
   1.84:1 rods │ 6-bolt ladder girdle
              │
[ 180° flat-plane forged micro-alloy crank ]
```

## Locked geometry

| Parameter | Value |
|-----------|-------|
| Bore × stroke | 87.0 × 75.0 mm |
| Rod length | 138.0 mm |
| Rod / stroke | **1.840** (B16 reference 1.74) |
| Displacement | **3,567.3 cc (3.57 L)** |
| Bank / pitch / deck | 90° / 98 mm / 202.50 mm |
| CR / chamber | 12.5:1 / 38.2 cc |
| MPS @ 10,000 RPM | **25.0 m/s** |
| Side-load cut vs short-rod 1.32:1 | **≈ 28%** |
| Side-load cut vs B16 1.74:1 | ≈ 5.4% (geometric) |
| PTWA weight save | 18 lb vs iron liners |

## Manufacturing hybrid

| Part | Process | Material |
|------|---------|----------|
| Block | Binder-jet sand mold → LP A356-T6 cast | A356-T6 (310 MPa) |
| Heads | LPBF / DMLS | Scalmalloy / AlSi10Mg (520 MPa) |
| Rods | Powder-forged fracture-split | 4600 steel (950 MPa) |
| Crank | Precision forged 180° | 4340 micro-alloy (1,100 MPa) |
| Valves | CNC | Na-filled Inconel 718 |

**Head LPBF specifics:** conformal coolant at 1.2 mm injector/plug clearance; integrated 40 bar H₂ rail; +1.2% Scalmalloy shrink scale; 30 µm layers.

**Block sand print:** 3.5 mm structural walls / 6.0 mm ribs; +3.0 mm bore/deck/main stock for CNC finish.

## CAD master skeleton (parametric)

1. Define bore/stroke/rod equations; place valve vectors at 12.5° IN / 11.0° EX.  
2. Loft high-tumble ports (35° entrance) for H₂ mixing.  
3. Topology-optimize webs (SIMP); export sand negatives (.STL/.3MF).  
4. Export head STEP → apply shrink → slice LPBF.

## Honda diligence note

Integrated girdle and long-rod philosophy are explicitly K/B-series lessons. PTWA sleeveless bores and LPBF conformal heads are the cost/thermal leap for H₂ pre-ignition control — not present on production K20/B16.
