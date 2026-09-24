# SVIE Risk Register

Concept-engineering risks visible from the software package. Severity is qualitative for diligence, not a quantitative FMEA.

| ID | Risk | Severity | Likelihood | Mitigation in-repo / next |
|----|------|----------|------------|---------------------------|
| R01 | BTE targets unmet on dyno | High | Medium | Treat as targets; gate hardware on indicated trends; revise YAML |
| R02 | Supercritical gasoline materials / seals fail | High | Medium | G1 spray-rig materials DoE; thermal oil spec as starting point |
| R03 | Piezo orifice coking / durability | High | Medium | Flash-boiling regime locked; endurance not modeled — bench required |
| R04 | DEVA energy / thermal exceed budget | Medium | Medium | `deva_power` budgets; fail-safe seating in SENTINEL narrative |
| R05 | H₂ DI backfire / NOx | High | Medium | λ / water-DI models; SENTINEL isolation timing |
| R06 | AXIOM / FLUX shift harshness | Medium | Medium | FLUX ≤8 ms is *design target* for torque hole — DCT literature sync is often 0.1–1.5 s; validate on clutch rig |
| R06b | Over-claiming FLUX as measured DCT time | Medium | Medium | Documented in validation-report.md |
| R07 | Patent landscape blocking FOU | High | Unknown | Buyer FTO search; claim charts are *proposed*, not granted |
| R08 | Docs drift from YAML | Medium | Medium | Golden tests + inventory CLI; handoff checklist |
| R09 | Export-control misclassification | Medium | Low | SECURITY.md; buyer trade counsel |
| R10 | Over-claiming vs Honda public tech | Medium | Low | Explicit non-affiliation; gap map cites public sources only |
| R11 | Portal mistaken for production ECU | Low | Medium | UI disclaimers; TRL badges |
| R12 | BOM cost optimism | Medium | High | Marked order-of-magnitude; exclude from deal pricing |

## Residual statement

Accepting this package means accepting **analytical risk** until G3+. The acquisition value is acceleration of architecture + verifiable math — not elimination of powertrain development risk.
