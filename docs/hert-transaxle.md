# HERT-12 Hydrogen-Expanded Reactive Transaxle

**Spec:** [`specs/hert_transaxle.yaml`](../specs/hert_transaxle.yaml)

## Expansion recovery

| Mode | \(T_{in}\) | \(\eta_{turb}\) | Shaft power |
|------|------------|-----------------|-------------|
| Cold gas | 25 °C | 0.78 | **52.23 kW (70 hp)** |
| CEB | 650 °C | 0.75 | **155.51 kW (208.5 hp)** |

Energy normally destroyed in a pressure regulator becomes impulse-turbine shaft work. GDSA shift gas is scavenged into the SVIE intake (zero mass loss).

## GDSA

4.0 ms total: piezo pilot → 1,256 N pneumatic stroke (20 mm bore @ 40 bar) → detent lock → intake scavenge.

## 12-speed map

\(R_{total} = R_{main} \times R_{split}\) with \(S_L=1.2273\), \(S_H=1.0\), FD = 3.1538.  
Splitter upshifts at 8,500 RPM drop ≈ **1,574 RPM**.

```bash
python -m svie_physics.hert_expansion
python -m svie_physics.gdsa_shift
python -m svie_physics.gear_map
```
