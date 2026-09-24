# AXIOM Drive & e:HEV Bridge — Beltless by Design

## AXIOM ([`specs/axiom_drive.yaml`](../specs/axiom_drive.yaml))

**Absolute eXergy Indexed Orthogonal Mechanism** — fixed-ratio exergy path:

- HERT-12 dog + splitter primary  
- Optional 25 kW e-fill (HAMT-class) for torque hole fill  
- **Rubber-band index = 0**  
- Shift 4 ms; η 0.965; 850 Nm input class  

**Vs Honda S+ Shift:** they shape RPM in software on an electric CVT. AXIOM drops real ratios (measured 1,011–1,629 RPM @ 8500 upshifts) with turbine pulse rev-match.

```bash
python -m svie_physics.axiom_drive
python -m svie_physics.cvt_comparison
```

## e:HEV Bridge ([`specs/ehe_v_bridge.yaml`](../specs/ehe_v_bridge.yaml))

Lets Honda evaluate a **dual-motor hybrid** that still speaks their e:HEV language (EV / series / engine-direct) while **removing**:

- metal pushing V-belt  
- pulley clamp hydraulics  
- eCVT rubber-band unit  

Engine-direct uses AXIOM ratios + DEVA Atkinson — efficiency target **0.965** on the mechanical path.
