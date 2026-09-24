# Chassis Torsional Rigidity & Structural Nodes

**Vehicle:** 3,250 lb (1,474 kg), 106 in WB, 63 in track, 48:52 F/R  
**Target \(K_\theta\):** **35,000 Nm/deg (35 kNm/deg)**  
**Spec:** [`specs/chassis_monocoque.yaml`](../specs/chassis_monocoque.yaml)

## Design criteria

1. **Suspension coupling:** \(K_\theta \ge 12 \times K_{\phi,\mathrm{susp}} = 12 \times 2500 = 30{,}000\,\mathrm{Nm/deg}\)
2. **Single-wheel 2.5G bump twist:** \(T = 8676 \times 0.8 = 6940.8\,\mathrm{Nm}\); with \(\theta_{max}=0.20^\circ\) ⇒ \(K_\theta=34{,}704\,\mathrm{Nm/deg}\)
3. **Design target:** round to **35 kNm/deg** (Glickenhaus-class carbon monocoque territory)

## Bending

\(F_{z,\mathrm{total}} = 2.0\times14460 + 1779 = 30699\,\mathrm{N}\)  
\(M_{b,\max} \approx F L / 8 = 10330\,\mathrm{Nm}\)

## Node safety factors

| Node | Peak | Limit | SF |
|------|------|-------|----|
| A Rear diffuser/transaxle | 245 MPa VM | 503 MPa | 2.05 |
| B Engine/tub (shear) | 32.5 MPa | 65 MPa | 2.00 |
| C Tunnel web | 185 MPa VM | 450 MPa | 2.43 |
| D Front DKIS towers | 162 MPa VM | 276 MPa | 1.70 |

Executable: `python -m svie_physics.chassis_torsion`
