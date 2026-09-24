# SVIE Technical White Paper

**Document status:** Concept engineering baseline (not production-validated)  
**Architecture:** Supercritical Vapor-Injection Engine (SVIE)  
**Reference model:** SVIE-V8 5.204 L @ 8,500 RPM WOT  
**Machine-readable sources:** [`specs/`](../specs/), [`packages/physics-engine`](../packages/physics-engine/)

---

## 1. Abstract

The SVIE platform replaces liquid droplet fuel delivery (GDI/PFI) with **Supercritical Flash-Vaporization (SFV)**: gasoline is pressurized above its critical pressure, heated with exhaust recuperation past the critical temperature, then expanded through a piezoelectric sonic orifice into a dry gaseous charge. Camshafts are eliminated in favor of **Digital Electromagnetic Valve Actuation (DEVA)** with on-the-fly Otto/Miller/Atkinson switching and variable compression (10:1–18:1). The powertrain couples to either a **12-speed splitter manual (12M-DS)** or a **9-speed multi-clutch automatic (9A-MC)**—explicitly non-CVT—to hold the ultra-lean efficiency island.

This paper summarizes architecture, governing equations, and the **executable** baseline models that reproduce the published WOT mass-flow, heat-exchanger, orifice, and piezo-driver figures.

> **Disclaimer:** All performance targets (including ~48–52% BTE) are engineering *targets* derived from first-principles energy balances and literature analogies. They are not dyno-validated results. Independent OEM verification is required before any licensing commitment.

---

## 2. System architecture

### 2.1 SFV fuel path

```
Lift pump (0.6 MPa) → HP pump (7.0 MPa) → Exhaust counter-flow HEX
  → Piezo sonic flash orifice (7→1 MPa) → Port/Direct vapor injectors
```

**Intent:** Eliminate liquid wall wetting, oil dilution, and heterogeneous soot pathways by ingesting a molecular-scale gaseous mixture. Full-load AFR in the baseline is **16.2:1** (lean vs stoichiometric 14.7:1); ultra-lean cruise targets up to **35:1** under HCCI/SPCCI-compatible valvetrain control.

### 2.2 DEVA valvetrain

Each valve uses dual-solenoid electromagnetic positioners with digital lift, timing, and duration. Cycle mode and compression ratio are scheduled per combustion event from load/RPM maps (VCR via eccentric wrist-pin bearings).

### 2.3 Transmissions

| Option | Layout | Role |
|--------|--------|------|
| 12M-DS | 6-speed H-gate + electro-pneumatic 2-speed splitter | Close ratios, driver engagement |
| 9A-MC | 3 planetaries, 6 clutches, wet launch clutch | &lt;40 ms shifts, no torque converter |

Specs: [`specs/12m_ds_transmission.yaml`](../specs/12m_ds_transmission.yaml), [`specs/9a_mc_transmission.yaml`](../specs/9a_mc_transmission.yaml).

---

## 3. Governing models (WOT baseline)

### 3.1 Air / fuel mass flow

For a four-stroke engine:

\[
\dot{V}_{\mathrm{air}} = V_d \cdot \frac{N_{\mathrm{rpm}}}{120} \cdot \eta_v
\]

\[
\dot{m}_{\mathrm{air}} = \dot{V}_{\mathrm{air}} \cdot \rho_{\mathrm{air}}, \quad
\dot{m}_{\mathrm{fuel}} = \frac{\dot{m}_{\mathrm{air}}}{\mathrm{AFR}}
\]

**Baseline:** \(V_d=0.005204\,\mathrm{m}^3\), \(N=8500\,\mathrm{rpm}\), \(\eta_v=1.05\), \(\mathrm{AFR}=16.2\), \(\rho_{\mathrm{air}}=1.184\,\mathrm{kg/m}^3\).

| Quantity | Value |
|----------|-------|
| \(\dot{m}_{\mathrm{air}}\) | ≈ 0.458 kg/s |
| \(\dot{m}_{\mathrm{fuel}}\) | ≈ 28.28 g/s |
| Fuel chemical input \(\dot{E}_{\mathrm{in}}\) | ≈ 1,244 kW |
| Per-injector fuel | ≈ 3.535 g/s (≈ 49.9 mg/stroke) |

Executable: `python -m svie_physics.air_fuel --spec specs/svie_v8_52L.yaml`

### 3.2 Heat exchanger duty

Fuel heated from 25 °C to 310 °C at 7.0 MPa with \(\Delta h_{\mathrm{total}} \approx 820\,\mathrm{kJ/kg}\):

\[
\dot{Q}_{\mathrm{HEX}} = \dot{m}_{\mathrm{fuel}} \cdot \Delta h_{\mathrm{total}} \approx 23.2\,\mathrm{kW}
\]

With a 30% exhaust energy share of \(\dot{E}_{\mathrm{in}}\) (≈ 373 kW), recovery ≈ **6.2%**—thermally feasible at redline without starvation.

Executable: `python -m svie_physics.heat_exchanger`

### 3.3 HEM choked flash orifice

Pressure ratio \(P_2/P_1 = 1.0/7.0 = 0.143 < 0.54\) ⇒ choked. Cavitation number:

\[
\sigma_c = \frac{P_2 - P_{\mathrm{sat}}}{P_1 - P_{\mathrm{sat}}} \approx -0.579 < 0
\]

⇒ continuous flash boiling (spinodal expansion), not classic cavitation collapse. Required throat area at \(G_{\mathrm{crit}} \approx 8200\,\mathrm{kg/(m^2\cdot s)}\):

\[
A_{o,\mathrm{req}} \approx 0.431\,\mathrm{mm}^2
\]

Executable: `python -m svie_physics.hem_choked_flow`

### 3.4 Piezo pintle envelope

\[
\Delta z = d_{33}\, n\, V, \quad
A_o = \pi D_{\mathrm{pintle}}\, \Delta z\, \sin\theta_{\mathrm{seat}}
\]

At 150 V: \(\Delta z_{\max} = 81\,\mu\mathrm{m}\), \(A_{o,\max} \approx 0.630\,\mathrm{mm}^2 > A_{o,\mathrm{req}}\).

30 kHz acoustic modulation imposes \(\Delta P_{\mathrm{acoustic}} \approx 0.95\,\mathrm{MPa}\) to force homogeneous vaporization.

### 3.5 Resonant GaN driver

Piezo stack \(C_p=50\,\mathrm{nF}\), \(V=150\,\mathrm{V}\), \(f_s=30\,\mathrm{kHz}\):

\[
E_c = \tfrac12 C_p V^2 = 0.5625\,\mathrm{mJ}, \quad
P_{\mathrm{raw}} = E_c f_s \approx 16.88\,\mathrm{W/valve}
\]

Resonant inductor for 5 µs half-period: \(L_r \approx 50.66\,\mu\mathrm{H}\), \(I_{\mathrm{peak}} \approx 5.02\,\mathrm{A}\). Energy recovery cuts dissipation to &lt; 2.2 W/valve.

---

## 4. Competitive positioning (summary)

| Feature | SVIE concept | Conventional (Honda K20 / L15 class) |
|---------|--------------|--------------------------------------|
| Fuel delivery | Dry supercritical flash vapor | Liquid DI / port spray |
| Peak AFR | Up to 35:1 (cruise target) | ~14.7:1 stoichiometric |
| Valvetrain | Camless DEVA | Camshaft + VTEC/VTC |
| Compression | 10:1–18:1 continuous | Fixed ~10.5–11.5:1 |
| Transmission | 12M-DS or 9A-MC | CVT or 6MT |
| Target BTE | ~50% (target) | ~38–41% |

Detailed teardown: [`docs/honda-e-hev-teardown.md`](honda-e-hev-teardown.md).

---

## 5. Verification

Golden-vector tests lock the numbers above:

```bash
pip install -e "./packages/physics-engine[dev]"
pytest packages/physics-engine/tests -v
```

Portal calculators call the same Python modules via the FastAPI bridge—UI and CLI cannot diverge for identical inputs.

---

## 6. Open work for OEM diligence

1. Multi-component gasoline surrogate (Cantera) for accurate \(T_c, P_c, h(T,P)\).
2. Transient cold-start HEX warmup strategy and catalyst light-off coupling.
3. DEVA actuator force/thermal FEM and fail-safe limp modes.
4. Materials / coking study for 310 °C fuel-wetted stainless microchannels.
5. Dyno map of lean stability limits with gaseous charge.

---

## 7. Licensing posture

SVIE is positioned as **independent powertrain IP** for evaluation by OEM R&D and Tier-1 partners. Claim drafts for counsel review: [`docs/claim-charts.md`](claim-charts.md).

## 8. Extended vehicle systems

- Chassis torsion / stress nodes: [`chassis-structural.md`](chassis-structural.md)
- HERT-12 hydrogen expansion transaxle: [`hert-transaxle.md`](hert-transaxle.md)
- Beyond-horizon breakthrough features: [`breakthrough-features.md`](breakthrough-features.md)
- High-RPM H₂ DI architecture (3.57 L): [`svie-v8-hr-architecture.md`](svie-v8-hr-architecture.md)
- DEVA camless power: [`deva-valvetrain.md`](deva-valvetrain.md)
- H₂ combustion / PI / NOx: [`h2-combustion-control.md`](h2-combustion-control.md)
- Thermal + BOM envelope: [`thermal-bom.md`](thermal-bom.md)
- **CVT evidence dossier (delete the belt):** [`cvt-evidence-dossier.md`](cvt-evidence-dossier.md)
- **AXIOM anti-CVT + e:HEV bridge:** [`axiom-anti-cvt.md`](axiom-anti-cvt.md)
- **Honda R&D gap map:** [`honda-rd-gap-map.md`](honda-rd-gap-map.md)
- **NEXUS-48 / SONIC / SENTINEL / CHRONOS / TRL:** [`nexus-sonic-chronos.md`](nexus-sonic-chronos.md)
- **BLEND / MIRAGE / VECTOR:** [`blend-mirage-vector.md`](blend-mirage-vector.md)
