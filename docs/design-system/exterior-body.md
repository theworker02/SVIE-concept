# Exterior Body Design

**Spec:** [`specs/body_exterior.yaml`](../../specs/body_exterior.yaml)  
**Renders:** `design/renders/svie-exterior-front.png`, `svie-exterior-rear.png`

---

## Silhouette

Mid-engine 2-seat coupe on the NODE-CAST tub (wheelbase **2.692 m**, track **1.60 m**). Long hood visual (front trunk + HEX/radiator volume), cabin set rearward, short rear deck over AXIOM/HERT.

| Dimension | Value |
|-----------|-------|
| Overall length | 4.52 m |
| Overall width (mirrors folded) | 1.94 m |
| Overall height | 1.18 m |
| Ground clearance (static) | 110 mm |
| Cd (DRS closed) | 0.32 target |
| Cd (DRS open) | 0.295 (AERO-SKIN) |

---

## Surface language

1. **Primary character line** — continuous crease from headlamp brow → door → rear haunch.  
2. **Negative volumes** — HEX intake behind front wheel; engine bay NACA / blade intakes on rear quarters.  
3. **Diffuser** — full-width venturi integrating AERO-SKIN flaps; CELL-VAULT underside stays flat ahead of venturi throat.  
4. **Shutlines** — frunk, doors, engine cover, charge/fuel doors; minimum 3 mm gaps, 1 mm flush tolerance class.

---

## Materials (production intent)

| Zone | Material | Finish |
|------|----------|--------|
| Outer skins | Aluminum 6016 / SMC options | Graphite paint |
| Hood / engine cover | CFRP or Al | Painted or clear-carbon option |
| Diffuser / splitter | CFRP | Matte |
| NODE-CAST nodes | A356 | Powder / e-coat visible at pickups |
| Glass | Laminated / tempered | Acoustic laminate windshield |

---

## Manufacturing notes

- Class-A stamped Al for volume path; RTM CFRP for halo.  
- AERO-SKIN actuators sealed at diffuser hinge (see manufacturing master §4.2).  
- Paint: 3-coat graphite; amber is lighting only — **no** painted racing stripes as default.

---

## Design idea vs main plan

This exterior is a **production-ready design proposal** for diligence storytelling. Structural numbers remain owned by `chassis_monocoque` + NODE-CAST; aero deltas by `aero_skin`.
