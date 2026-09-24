export default function ArchitecturePage() {
  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight">System Architecture</h1>
        <p className="mt-2 max-w-2xl text-[var(--muted)]">
          SFV fuel path, DEVA valvetrain context, and monorepo data flow.
        </p>
      </header>

      <section className="panel p-6">
        <h2 className="panel-title">SFV Fuel Path</h2>
        <pre className="mt-4 overflow-x-auto font-[family-name:var(--font-ibm-mono)] text-xs leading-7 text-[var(--steel)]">{`
[In-Tank Lift 0.6 MPa]
        │
        ▼
[HP Pump 7.0 MPa] ──► [Exhaust Counter-Flow HEX] ──► [6.8 MPa / 310 °C]
        │                                              │
        │                                              ▼
        │                              [Piezo Sonic Flash Orifice]
        │                                      7.0 → 1.0 MPa
        │                                              │
        │                                              ▼
        │                              [Dry Gas → PVI / DVI Injectors]
`}</pre>
      </section>

      <section className="panel p-6">
        <h2 className="panel-title">Monorepo Data Flow</h2>
        <pre className="mt-4 overflow-x-auto font-[family-name:var(--font-ibm-mono)] text-xs leading-7 text-[var(--steel)]">{`
specs/*.yaml  ──►  packages/physics-engine (Python)
                         │
                         ├── pytest golden vectors
                         └── FastAPI :8000
                                   │
                                   ▼
                     packages/web-portal (Next.js)
`}</pre>
      </section>

      <section className="panel p-6">
        <h2 className="panel-title">Transmission Options</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <div className="border border-[var(--line)] p-4">
            <h3 className="font-medium text-[var(--ink)]">12M-DS / HERT-12</h3>
            <p className="mt-2 text-sm text-[var(--muted)]">
              6-speed dog-clutch + pneumatic splitter. HERT adds H2 impulse
              turbine recovery (70 hp cold / 208 hp CEB) and 4 ms GDSA shifts
              scavenged into the intake.
            </p>
          </div>
          <div className="border border-[var(--line)] p-4">
            <h3 className="font-medium text-[var(--ink)]">9A-MC Automatic</h3>
            <p className="mt-2 text-sm text-[var(--muted)]">
              Three planetaries, six clutches, wet launch clutch (no torque
              converter). Shift execution under 40 ms with skip-shift kickdown.
            </p>
          </div>
        </div>
      </section>

      <section className="panel p-6">
        <h2 className="panel-title">SVIE-V8-HR High-RPM H2 DI (3.57 L)</h2>
        <pre className="mt-4 overflow-x-auto font-[family-name:var(--font-ibm-mono)] text-xs leading-7 text-[var(--steel)]">{`
[ DOHC 32V LPBF Head — conformal cool + dual H2 DI ]
                      │
[ High-tumble pentroof — CR 12.5:1 ]
                      │
[ A356-T6 deep-skirt + PTWA 0.15 mm bores ]
   87×75 mm · rod 138 mm · R/S 1.84 · MPS 25 m/s @ 10k
                      │
[ Fracture-split 4600 rods · 180° flat-plane 4340 crank ]
[ Integrated 6-bolt ladder girdle ]
`}</pre>
        <p className="mt-3 text-sm text-[var(--muted)]">
          Honda K20/B16-evolved: long-rod, girdled bottom end, sleeveless PTWA,
          hybrid sand-cast block + LPBF Scalmalloy heads. Distinct from the
          5.2 L gasoline SFV WOT baseline.
        </p>
      </section>

      <section className="panel p-6">
        <h2 className="panel-title">Anti-CVT — AXIOM Fixed-Ratio Exergy</h2>
        <p className="mt-3 text-sm text-[var(--muted)]">
          Belt CVTs lose ~14.5 efficiency points vs dog paths and carry clamp/pump
          parasitics (~13.5 kW class). Honda HR-V belt TSBs and next-gen e:HEV
          electric CVT + S+ Shift still preserve continuous-ratio DNA. AXIOM
          deletes the belt; e:HEV Bridge keeps dual-motor hybrid modes without
          cones.
        </p>
      </section>

      <section className="panel p-6">
        <h2 className="panel-title">NEXUS-48 · SONIC · SENTINEL · CHRONOS</h2>
        <p className="mt-3 text-sm text-[var(--muted)]">
          48V P1 ISG powers DEVA with margin; flat-plane 180° pulses + AETHER
          bark on AXIOM shifts; H2 SENTINEL 50 ms isolation; CHRONOS cold-start
          to first fire in 3.7 s. Repo TRL-3 with staged licensing packages.
        </p>
      </section>

      <section className="panel p-6">
        <h2 className="panel-title">Breakthrough Layer</h2>
        <p className="mt-3 text-sm text-[var(--muted)]">
          CCD cryogenic densification, CASMIR acoustic chassis health (Honda AE
          tech transfer), PSI plasma ignition for 35:1 AFR, DKIS torsion
          feedforward, dual SFV/H2 co-rail, and orbital water electrolysis buffer.
        </p>
      </section>

      <section className="panel p-6">
        <h2 className="panel-title">Licensing package stack</h2>
        <pre className="mt-4 overflow-x-auto font-[family-name:var(--font-ibm-mono)] text-xs leading-7 text-[var(--steel)]">{`
SFV-CORE ──► DEVA-HR ──► AXIOM-DRIVE
                │              │
                ▼              ▼
            OPS-STACK ◄── CONTROL
                │
                ▼
            STRUCTURE
                │
     ENGINE-PLUS · TRANS-PLUS · BODY-PLUS
                │
            MFG-PLAN (routes for all)
`}</pre>
        <p className="mt-3 text-sm text-[var(--muted)]">
          Next-wave docs: engine-next-wave · transmission-next-wave · body-platform ·
          manufacturing-master-plan. Calculators → Platform+ / Manufacturing tabs.
        </p>
      </section>
    </div>
  );
}
