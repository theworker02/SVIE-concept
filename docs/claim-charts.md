# SVIE Proposed Patent Claim Charts (Engineering Drafts)

> **Not legal advice.** These are **proposed claim sets for patent counsel**. They are engineering articulation of inventive concepts present in the SVIE monorepo. Do not file without attorney review. Prior-art search has not been completed in this repository.

**Document version:** 0.1.0  
**Brand / assignee posture:** SVIE Advanced Engineering Research (independent powertrain IP)

---

## Claim Set 1 — Supercritical Flash-Vaporization (SFV) Fuel Path

### Independent claim (draft)

1. A method of preparing a hydrocarbon fuel charge for an internal combustion engine, comprising:
   - (a) pressurizing liquid fuel to a pressure substantially above the fuel’s critical pressure;
   - (b) heating said pressurized fuel, using heat recovered from engine exhaust, to a temperature at or above the fuel’s critical temperature such that the fuel exists as a supercritical fluid;
   - (c) expanding said supercritical fluid across a controllable orifice into a lower-pressure chamber such that the fluid flashes into a substantially dry gaseous vapor substantially free of liquid droplets; and
   - (d) metering said dry gaseous vapor into an intake runner or combustion chamber for mixing with intake air.

### Dependent claims (draft)

2. The method of claim 1, wherein step (a) pressurizes gasoline to about 6.5–7.5 MPa and step (b) heats to about 280–320 °C.  
3. The method of claim 1, wherein exhaust recuperation extracts less than about 10% of available exhaust enthalpy at peak power while maintaining supercritical conditions.  
4. The method of claim 1, further comprising dual banking of microchannel heat exchangers, one per cylinder bank.  
5. An apparatus comprising a lift pump, high-pressure pump, exhaust-coupled microchannel heat exchanger, flash orifice, and gaseous injector configured to perform the method of claim 1.

### Evidence map (this repo)

| Element | Spec / model |
|---------|----------------|
| Pressure ladder | [`specs/sfv_fuel_system.yaml`](../specs/sfv_fuel_system.yaml) |
| HEX duty / recovery | `svie_physics.heat_exchanger` |
| WOT fuel flow | `svie_physics.air_fuel` |

---

## Claim Set 2 — Piezoelectric Acoustic Flash Orifice

### Independent claim (draft)

1. A fuel conditioning valve comprising:
   - a pintle cooperating with a seat to define a variable orifice;
   - a multilayer piezoelectric actuator coupled to the pintle;
   - a driver configured to vibrate the pintle at an ultrasonic frequency while modulating mean orifice area; and
   - a fluid path arranged such that supercritical or near-critical fuel upstream of the orifice expands to a pressure below local saturation pressure, inducing flash boiling,
   - wherein the ultrasonic vibration superimposes an acoustic pressure ripple that promotes homogeneous vaporization of the fuel to a dry gas downstream of the orifice.

### Dependent claims (draft)

2. The valve of claim 1, wherein the ultrasonic frequency is between about 20–40 kHz.  
3. The valve of claim 1, wherein the actuator stroke provides a maximum geometric orifice area greater than the HEM-predicted choked area required for peak engine fuel mass flow.  
4. The valve of claim 1, further comprising a resonant inductive energy-recovery half-bridge driver recovering a majority of capacitive reactive power of the piezoelectric stack.  
5. The valve of claim 4, wherein the resonant half-period is tuned to about 3–7 µs for soft charge/discharge of the stack.

### Evidence map

| Element | Spec / model |
|---------|----------------|
| Orifice / cavitation \(\sigma_c\) | `svie_physics.hem_choked_flow` |
| Stroke / \(A_o\) / \(\Delta P_{ac}\) | `svie_physics.piezo_dynamics` |
| Resonant \(L_r\), \(E_c\), \(P_{raw}\) | `svie_physics.piezo_driver` |
| Parameters | [`specs/piezo_injector.yaml`](../specs/piezo_injector.yaml) |

---

## Claim Set 3 — Camless Cycle Switching with Variable Compression

### Independent claim (draft)

1. An internal combustion engine control system comprising:
   - electromagnetic actuators individually operable to open and close intake and exhaust valves without a camshaft;
   - a controller configured to select, on a per-combustion-cycle basis, among Otto, Miller, and Atkinson valve timing schedules as a function of load; and
   - a variable compression mechanism adjustable between a first compression ratio suitable for boosted operation and a second, higher compression ratio suitable for light-load lean operation,
   - wherein the controller coordinates valve schedule and compression ratio with metering of a dry gaseous fuel charge.

### Dependent claims (draft)

2. The system of claim 1, wherein the compression ratio is continuously adjustable between about 10:1 and about 18:1.  
3. The system of claim 1, wherein the gaseous fuel charge is produced by the method of Claim Set 1.  
4. The system of claim 1, wherein lean operation targets air–fuel ratios greater than about 20:1 under homogeneous charge conditions.

### Evidence map

Documented in [`docs/whitepaper.md`](whitepaper.md) §§2.2–2.3; mechanical FEM out of scope for v1 models.

---

## Claim Set 4 — Ultra-Lean Efficiency Island Transmission Coupling

### Independent claim (draft)

1. A powertrain comprising:
   - an internal combustion engine configured for ultra-lean gaseous homogeneous combustion within a narrow preferred engine-speed band; and
   - a multi-ratio transmission selected from:
     - (i) a manual gearbox having a main multi-speed gate and an electro-pneumatic splitter providing two ranges per main gear, or
     - (ii) a multi-clutch planetary automatic lacking a hydrodynamic torque converter and having a wet multi-plate launch clutch,
   - wherein transmission ratios are spaced such that sequential ratio steps keep engine speed changes within a predetermined RPM drop bound during upshifts while the engine remains in said preferred band.

### Dependent claims (draft)

2. The powertrain of claim 1(i), wherein the splitter is thumb-actuated from the shift knob and provides twelve forward ratios from a six-speed main box.  
3. The powertrain of claim 1(ii), wherein clutch-to-clutch shifts complete in less than about 50 milliseconds and permit skip-shift downshifts.  
4. The powertrain of claim 1, wherein the predetermined RPM drop bound is about 250 RPM or less between adjacent split ratios.

### Evidence map

| Element | Spec |
|---------|------|
| 12M-DS ratios | [`specs/12m_ds_transmission.yaml`](../specs/12m_ds_transmission.yaml) |
| 9A-MC ratios | [`specs/9a_mc_transmission.yaml`](../specs/9a_mc_transmission.yaml) |

---

## Chart vs prior art categories (counsel checklist)

| Claim set | Prior-art categories to search |
|-----------|--------------------------------|
| SFV | Supercritical fuel injection, exhaust-heated fuel rails, flash-boiling DI |
| Piezo acoustic orifice | Piezo GDI injectors, ultrasonic atomizers, HEM flashing nozzles |
| DEVA + VCR | Camless EM valves, Fiat Multiair-class, VCR pistons/rods |
| Splitter / multi-clutch | Heavy-duty splitter manuals, DCT / multi-clutch automatics |

---

## Claim Set 5 — Cryogenic Charge Densification from Fuel Expansion

### Independent claim (draft)

1. A method of increasing intake charge density in a gaseous-fuel internal combustion engine, comprising expanding a compressed gaseous fuel through a work-extracting expander to produce shaft work and a cold expanded stream, and transferring heat from an intake airflow to said cold expanded stream prior to admitting the airflow and/or scavenged fuel into the engine, thereby increasing intake density without a mechanically driven compressor.

## Claim Set 6 — Acoustic Structural Health Linked to Suspension Interconnect

### Independent claim (draft)

1. A vehicle control system comprising acoustic-emission sensors disposed at chassis structural nodes, a controller configured to detect AE burst signatures indicative of structural distress, and an interconnected suspension actuator system whose roll-stiffness distribution is derated or redistributed in response to said signatures.

## Claim Set 7 — Dual-Mode Supercritical Hydrocarbon / Hydrogen Co-Rail

### Independent claim (draft)

1. A fuel delivery apparatus comprising a gaseous fuel rail and injectors operable to meter either (i) a dry vapor produced by supercritical flash expansion of a liquid hydrocarbon fuel or (ii) hydrogen gas conditioned by a pressure-recovery expander, wherein selection between (i) and (ii) is performed without exchanging the injector hardware.

---

## Licensing note

These claim charts support **OEM / Tier-1 diligence** of the SVIE monorepo. Executable models and YAML specs are the technical enablement corpus; counsel should refine claim language to jurisdiction-specific practice after a formal prior-art search.

## Claim Set 8 — Boosted Late-DI Hydrogen Pre-Ignition Control with Conformal Cooling

1. A method of operating a hydrogen direct-injection engine comprising boosting intake pressure above a threshold, injecting hydrogen late in the compression stroke, and actively cooling injector and spark-plug bosses via conformal coolant passages integrally formed in an additively manufactured cylinder head, thereby reducing hot-spot induced pre-ignition.

## Claim Set 10 — Beltless Fixed-Ratio Exergy Drive Replacing CVT

1. A vehicle powertrain comprising an internal combustion engine and a multi-speed dog-clutch transmission with electro-pneumatic ratio actuation, wherein the powertrain excludes any belt or chain continuously variable ratio device, and wherein shift energy is at least partially supplied by expanded gaseous fuel from a pressure-recovery expander.

## Claim Set 12 — 48V Integrated Supply Dedicated to Camless Valvetrain

1. A mild-hybrid electrical architecture comprising a crank-integrated 48 V machine and energy store configured to supply electromagnetic valve actuators as a primary load, wherein recuperated energy is preferentially allocated to valvetrain transitions during deceleration.

## Claim Set 14 — Ultra-Short Shift Regen Continuity via Brake-by-Wire

1. A method of maintaining vehicle deceleration continuity during a multi-speed dog-clutch ratio change lasting less than about 10 milliseconds, comprising anticipating the ratio change, temporarily substituting friction brake torque for unavailable regenerative motor torque via a brake-by-wire actuator, and releasing the friction torque upon completion of the ratio change.

## Claim Set 15 — Multi-Node ECU Thermal Digital Twin for Camless H2 Powertrain

1. A control system comprising reduced-order thermal models of at least an injector boss, a fuel heat exchanger outlet, a coated cylinder bore, and an electromagnetic valve actuator coil, executing on a vehicle controller at a rate sufficient to derate combustion or valvetrain parameters before a temperature limit is reached.
