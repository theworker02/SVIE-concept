# BLEND · MIRAGE · VECTOR — Control & Twin Layer

## BLEND ([`specs/blend_brake.yaml`](../specs/blend_brake.yaml))

Dry EMB brake-by-wire fills the regen hole when AXIOM/HERT shifts disconnect gear-coupled e-machines. Literature/patents address this for long AMT/DCT holes (~150 ms). SVIE’s **4 ms GDSA** shrinks the hole by **~37×**, so friction fill is a brief pulse (~8 ms continuity window) at 0.3 g → **≈ 4336 N**.

```bash
python -m svie_physics.blend_mirage_vector --which blend
```

## MIRAGE ([`specs/mirage_twin.yaml`](../specs/mirage_twin.yaml))

ECU-rate (50 Hz) first-order thermal ROMs for injector boss, SFV HEX exit, PTWA bore, DEVA coil, NEXUS ISG — same class of reduced-order twins OEMs now run for e-axles/motors (2024–25). Enables derate before hard limits (λ, CEB, water DI, lift).

## VECTOR ([`specs/vector_hcp.yaml`](../specs/vector_hcp.yaml))

1 ms supervisory HCP spanning 10 domains (DEVA → AETHER) with SENTINEL failsafe dominance — the integration surface Honda’s fragmented e:HEV / FC stacks do not publish as one sports-car plane.
