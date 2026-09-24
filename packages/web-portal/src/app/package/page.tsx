import Link from "next/link";

const PACKAGES = [
  {
    id: "SFV-CORE",
    title: "Supercritical flash fuel path",
    body: "Air/fuel WOT, HEX recuperation, HEM orifice, piezo stroke and GaN driver — the 5.2 L golden baseline.",
  },
  {
    id: "DEVA-HR",
    title: "Camless DEVA + V8-HR H2",
    body: "Electromagnetic valvetrain power budgets and the 3.57 L high-RPM hydrogen DI architecture.",
  },
  {
    id: "AXIOM-DRIVE",
    title: "Anti-CVT discrete drive",
    body: "AXIOM rubber-band index 0, e:HEV bridge without belt, HERT expansion and GDSA shifts.",
  },
  {
    id: "OPS-STACK",
    title: "Ops · NVH · safety · TRL",
    body: "NEXUS-48 bus, SONIC imbalance index, SENTINEL isolation, CHRONOS cold-start, TRL roadmap.",
  },
  {
    id: "CONTROL",
    title: "BLEND · MIRAGE · VECTOR",
    body: "Brake blending, twin-path torque coordination, and hybrid control policy layer.",
  },
  {
    id: "STRUCTURE",
    title: "Chassis · breakthrough · BOM",
    body: "Monocoque torsion nodes, CCD/DKIS breakthroughs, and order-of-magnitude cost envelope.",
  },
  {
    id: "ENGINE-PLUS",
    title: "CRYO-RAIL · RING-ZERO · OIL-SPINE · AETHER-IGN",
    body: "Buffered SFV rail, PTWA low-friction rings, structural oil spine, adaptive plasma ignition.",
  },
  {
    id: "TRANS-PLUS",
    title: "FLUX-SHIFT · GEAR-MESH-AM · JET-BEARING",
    body: "Zero-interrupt preselect, AM lattice carriers, HERT bearing oil jets.",
  },
  {
    id: "BODY-PLUS",
    title: "NODE-CAST · AERO-SKIN · CELL-VAULT · THERMAL-SKIN",
    body: "Hybrid CFRP/Al body, active aero, structural energy vault, body heat rejection.",
  },
  {
    id: "MFG-PLAN",
    title: "Manufacturing master",
    body: "15 process routes, PTWA/LPBF/CFRP cells, 5k units/year diligence capacity — see docs/manufacturing-master-plan.md.",
  },
{
    id: "ADDONS",
    title: "DRY-SUMP · PULSE-EGR · SILK · RANGE · KERS",
    body: "Scavenge oil control, pulsed EGR, active mounts, series RE mode, and kinetic recovery blend — validated via svie_physics.validate.",
  },
{
    id: "DESIGN",
    title: "Design · AETHER-OS · CarPlay Ultra",
    body: "Exterior, lamps, packaging, harness — plus analog-first AETHER-OS with Apple CarPlay Ultra as a guest layer. Hardware is truth.",
  },
  {
    id: "COMPLIANCE",
    title: "Homologation · 26262 · 21434 · OTA",
    body: "Regulatory path, SENTINEL ASIL draft map, AETHER cyber policy, durability gates, Tier-1 supply map — design intent, not certificates.",
  },
  {
    id: "ACQUIRE",
    title: "Readiness · deal · data room",
    body: "Weighted acquisition scorecard, preferred FOU+option structure, escrow, earnout gates, and virtual data-room index.",
  },
];

export default function PackagePage() {
  return (
    <div className="space-y-10">
      <header>
        <p className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-[0.3em] text-[var(--amber)]">
          LICENSING MODULES · v1.3.0
        </p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight">Package map</h1>
        <p className="mt-3 max-w-2xl text-[var(--muted)]">
          Fourteen modules — powertrain through design, compliance paths, and the acquisition desk.
        </p>
      </header>

      <div className="grid gap-4 md:grid-cols-2">
        {PACKAGES.map((pkg) => (
          <article key={pkg.id} className="panel p-5">
            <div className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-wider text-[var(--amber)]">
              {pkg.id}
            </div>
            <h2 className="mt-2 text-lg font-medium">{pkg.title}</h2>
            <p className="mt-2 text-sm leading-relaxed text-[var(--muted)]">{pkg.body}</p>
          </article>
        ))}
      </div>

      <section className="panel p-6">
        <h2 className="panel-title">Verify the map</h2>
        <pre className="mt-4 overflow-x-auto border border-[var(--line)] bg-[var(--bg)] p-3 font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--amber)]">
          {`python -m svie_physics.inventory
python -m svie_physics.validate
python -m svie_physics.addon_features
python -m svie_physics.manufacturing`}
        </pre>
        <div className="mt-5 flex flex-wrap gap-3">
          <Link href="/acquisition" className="btn">
            Acquisition desk
          </Link>
          <Link href="/design" className="btn" style={{ opacity: 0.85 }}>
            Design system
          </Link>
          <Link href="/hmi" className="btn" style={{ opacity: 0.8 }}>
            AETHER-OS
          </Link>
          <Link href="/demo" className="btn" style={{ opacity: 0.7 }}>
            Guided demo
          </Link>
        </div>
      </section>
    </div>
  );
}
