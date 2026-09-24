# Hardware TRL Roadmap (post-software package)

This monorepo delivers **software TRL-3** thermo/systems models. Hardware advancement is a separate funded program.

---

## Stage gates

| Gate | TRL | Deliverable | Approx. duration* |
|------|-----|-------------|-------------------|
| G0 | 3 | This repo accepted; golden CI green | 0 (done) |
| G1 | 4 | Piezo SFV orifice spray vessel + HEX breadboard | 3–6 mo |
| G2 | 4–5 | DEVA single-valve actuator dyno | 4–8 mo |
| G3 | 5 | Single-cylinder SFV or H₂ DI optical engine | 9–15 mo |
| G4 | 6 | Multi-cylinder mule (5.2 L SFV *or* 3.57 L H₂ HR) | 12–24 mo |
| G5 | 7 | Vehicle demonstrator + AXIOM/HERT integration | 18–36 mo |

\*Order-of-magnitude; OEM calendars and supplier lead times dominate.

## Parallel workstreams

1. **Fuel path** — materials for 7 MPa / ~310 °C gasoline supercritical; seal & injector durability  
2. **Valvetrain** — DEVA force/stroke/thermal; fail-safe seating  
3. **Drive** — AXIOM clutch thermal; GDSA pneumatics; belt-elimination validation vs e:HEV bridge  
4. **H₂ safety** — SENTINEL sensor suite → ISO 26262 / H₂ vehicle regs  
5. **NVH** — SONIC secondary index → balance shaft / mount strategy  

## Budget framing (indicative only)

| Phase | Rough order |
|-------|-------------|
| G1–G2 benches | Low–mid seven figures USD |
| G3 single-cylinder | Mid seven → low eight figures |
| G4–G5 mule / demo | Program-scale (OEM dependent) |

These are **not quotes**. Buyer cost engineering must rebuild bottoms-up.

## Stop / go criteria (examples)

- G1 go: measured orifice ṁ within ±5% of HEM model at design ΔP  
- G2 go: DEVA cycle energy within ±10% of `deva_power` budget at target RPM  
- G3 go: indicated efficiency trend compatible with white-paper BTE *direction* (not absolute target)  
- G4 go: AXIOM shift < published ms band under dyno inertia  

## Relationship to software

Every hardware gate should **re-lock or revise** YAML golden blocks. Divergences become change-controlled engineering change orders, not silent doc edits.
