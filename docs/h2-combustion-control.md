# Hydrogen DI Combustion & Emissions Control

**Spec:** [`specs/h2_combustion_control.yaml`](../specs/h2_combustion_control.yaml)  
**Model:** `python -m svie_physics.h2_combustion`  
**Engine family:** SVIE-V8-HR 3.57 L

## Research basis

- SAE / optical H2 DI work: hot-spot pre-ignition prefers **low pressure / early compression**; ignition delay lengthens as pressure rises → **boost + late compression DI** mitigation (with mixing discipline).
- Water DI experiments: up to **~80% NOx cut** and **~16% load extension**.
- Aftertreatment reviews: lean → **H2-SCR / urea-SCR**; stoich → **TWC**; mode-switching is hard — HR maps prefer lean + H2-SCR.

## SVIE packaging ties

| Hardware | Role in H2 control |
|----------|--------------------|
| PTWA bores + conformal LPBF jackets | Cut injector/plug hot spots that seed PI |
| Dual sequential H2 DI @ 40 bar | Late DI window without PFI backfire path |
| Water DI | NOx + knock/PI margin |
| PSI plasma ignition | Ultra-lean kernel at λ → 3.5 |
| Orbital water / CEB buffer | Cold-start reductant + light-off assist |

## Executable examples

```bash
python -m svie_physics.h2_combustion --lambda 1.05 --water-ratio 0.15
python -m svie_physics.h2_combustion --lambda 2.8 --water-ratio 0.0
```
