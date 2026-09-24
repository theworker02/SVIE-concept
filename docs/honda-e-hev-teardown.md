# Competitive Teardown: SVIE vs Honda Earth Dreams / VTEC Architectures

**Audience:** Honda R&D powertrain & IP evaluation  
**Scope:** Structured engineering comparison — not a product claim against Honda Motor Co.  
**SVIE baseline:** 5.204 L V8 concept @ 8,500 RPM WOT ([`specs/svie_v8_52L.yaml`](../specs/svie_v8_52L.yaml))

---

## 1. Purpose

Honda’s Earth Dreams family (exemplified by L15 turbo and K-series derivatives) and mechanical VTEC/VTC valvetrains represent state-of-the-art *production* gasoline efficiency and transient response. SVIE proposes a **different fuel-phase and valvetrain paradigm**. This document maps where SVIE claims differentiation versus where Honda already leads, so diligence teams can separate novelty from marketing.

---

## 2. Side-by-side feature matrix

| Domain | Honda K20 / L15-class benchmark | SVIE concept |
|--------|----------------------------------|--------------|
| Fuel metering | Liquid DI / PFI / dual injection | Supercritical flash → dry gas (SFV) |
| Mixture formation | Droplet evaporation in-cylinder / port | Pre-vaporized molecular mix |
| Wall wetting / oil dilution | Managed by spray targeting & timing | Architecturally eliminated (target) |
| Stoichiometric AFR | ~14.7:1 | Full-load baseline 16.2:1; cruise to 35:1 |
| Peak published BTE (hybrid ICE) | ~38–41% class | Target 48–52% (unvalidated) |
| Valvetrain | Camshafts + VTEC/VTC | Camless DEVA |
| Cycle modes | Cam profile / VTC limited | Per-cycle Otto / Miller / Atkinson |
| Compression | Fixed (~10.5–11.5:1 typical) | Continuous 10:1–18:1 VCR |
| Transmission pairing | CVT or 6MT common | 12M-DS splitter MT or 9A-MC DCT-like auto |
| Production maturity | High | Concept / simulation only |

---

## 3. Fuel delivery: Earth Dreams DI vs SFV

### Honda strengths
- Mature multi-hole GDI hardware, emissions aftertreatment, and cold-start strategies.
- Dual injection (DI+PFI) mitigates particulate and wall film in many Earth Dreams calibrations.
- Proven supply-chain cost and durability.

### SVIE differentiation hypothesis
- Latent-heat and heterogeneous combustion losses from liquid spray are removed by flashing fuel **before** cylinder entry.
- Executable WOT balance shows HEX duty (~23 kW) is only ~6% of exhaust enthalpy at redline — energy is available; the open question is **packaging, coking, and cold-start**.

### Diligence questions for Honda R&D
1. Can SFV heat-up time meet LEV/SULEV cold-start HC limits without auxiliary heaters?
2. How does gasoline surrogate critical-point variability affect HEX control authority?
3. Does gaseous port/direct injection require new injector sealing and metering IP vs CNG/H2 injectors?

---

## 4. Valvetrain: VTEC/VTC vs DEVA

| Aspect | VTEC / VTC | DEVA |
|--------|------------|------|
| Actuation | Mechanical cam + oil-pressure switching | Dual-solenoid electromagnetic |
| Lift profiles | Discrete (or limited continuous via VTC) | Fully digital lift/timing/duration |
| Failure modes | Well understood limp-home | Requires electrical redundancy design |
| Parasitic cost | Low electrical | High peak electrical / thermal |
| Cycle switching | Constrained by cam events | Per-cycle Miller/Atkinson/Otto |

**Honest assessment:** Honda’s mechanical systems win on cost, durability pedigree, and NVH. DEVA wins on degrees of freedom for lean HCCI/SPCCI. SVIE’s value proposition only holds if lean gaseous combustion **needs** that freedom to reach the claimed BTE band.

---

## 5. Efficiency island & transmission philosophy

Honda hybrids often pair high-BTE Atkinson engines with e-CVT / dual-motor layouts. SVIE deliberately **rejects CVT** for two non-CVT boxes:

- **12M-DS:** keeps ultra-lean RPM band with &lt;250 RPM drops (enthusiast + efficiency).
- **9A-MC:** &lt;40 ms shifts, skip-shift, wet launch clutch — closer to DCT character without a torque converter.

This is a product philosophy choice (engagement + narrow island) rather than a pure efficiency maximum. An OEM could still mate SFV+DEVA to an e-axle hybrid; the monorepo includes discrete gearboxes as the *default* pairing.

---

## 6. What SVIE does *not* claim

- Superiority in production cost, NVH, or emissions certification readiness.
- Dyno-proven 50% BTE.
- Drop-in replacement for any Honda engine family without vehicle integration work.

---

## 7. Suggested OEM evaluation path

1. Reproduce golden tests in [`packages/physics-engine/tests`](../packages/physics-engine/tests).
2. Replace gasoline \(\Delta h\) tables with Honda’s preferred surrogate / Cantera mechanism.
3. Bench a single-cylinder SFV head with gaseous injectors under controlled HEX inlet temperature.
4. Compare indicated thermal efficiency vs L15-class DI at matched IMEP and AFR.
5. Review claim drafts in [`claim-charts.md`](claim-charts.md) with counsel.

---

## 8. References (public benchmarks)

- Honda Earth Dreams published thermal-efficiency communications (~40%+ class for select hybrid engines).
- Public literature on supercritical gasoline injection and flash-boiling sprays (academic / SAE).
- Camless electromagnetic valvetrain research programs (OEM + university).

*Exact Honda internal numbers should be substituted by Honda reviewers; public ~38–41% BTE is used only as a literature-facing benchmark in this concept package.*
