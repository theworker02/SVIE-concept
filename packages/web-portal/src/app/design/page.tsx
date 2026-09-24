import Image from "next/image";
import Link from "next/link";

const GALLERY = [
  {
    src: "/design/svie-exterior-front.png",
    title: "Exterior — front three-quarter",
    blurb: "Graphite body, single character line, vertical instrument lamps.",
  },
  {
    src: "/design/svie-exterior-rear.png",
    title: "Exterior — rear",
    blurb: "Light-bar signature, venturi diffuser, AERO-SKIN integration.",
  },
  {
    src: "/design/svie-headlight-detail.png",
    title: "Headlamp detail",
    blurb: "Vertical LED stack + amber DRL filament.",
  },
  {
    src: "/design/svie-cabin-interior.png",
    title: "Cabin",
    blurb: "Driver cockpit, physical toggles, exposed sill.",
  },
  {
    src: "/design/svie-hmi-cabin-analog.png",
    title: "AETHER-OS — analog-first cabin",
    blurb: "Round gauges, milled rotaries, one guest glass for CarPlay Ultra.",
  },
  {
    src: "/design/svie-hmi-analog-stack.png",
    title: "Analog control stack",
    blurb: "CNC Al dials, jewels, zero stack screens.",
  },
  {
    src: "/design/svie-packaging-cutaway.png",
    title: "Packaging cutaway",
    blurb: "Z0–Z6 zones, mid engine, vault, harness backbone.",
  },
];

const DOCS = [
  { href: "#", label: "Design system README", path: "docs/design-system/README.md" },
  { href: "#", label: "AETHER-OS", path: "docs/design-system/aether-os.md" },
  { href: "#", label: "Exterior body", path: "docs/design-system/exterior-body.md" },
  { href: "#", label: "Lighting", path: "docs/design-system/lighting.md" },
  { href: "#", label: "Cabin", path: "docs/design-system/cabin.md" },
  { href: "#", label: "Packaging", path: "docs/design-system/packaging.md" },
  { href: "#", label: "Wiring harness", path: "docs/design-system/wiring-harness.md" },
];

export default function DesignPage() {
  return (
    <div className="space-y-12">
      <header>
        <p className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-[0.35em] text-[var(--amber)]">
          VEHICLE DESIGN SYSTEM · v1.3.0
        </p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
          How the car looks, wires, and packages
        </h1>
        <p className="mt-4 max-w-2xl text-[var(--muted)]">
          Production-ready design package — exterior, lighting, cabin, internals
          placement, zone harness, and analog-first AETHER-OS with CarPlay Ultra
          as guest. Parallel to the powertrain plan, not a replacement for
          Acquisition.md thermodynamics.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link href="/hmi" className="btn">
            AETHER-OS live mock
          </Link>
          <Link href="/architecture" className="btn" style={{ opacity: 0.9 }}>
            Powertrain architecture
          </Link>
          <Link href="/package" className="btn" style={{ opacity: 0.85 }}>
            Licensing packages
          </Link>
        </div>
      </header>

      <section className="grid gap-6">
        {GALLERY.map((item) => (
          <article key={item.src} className="panel overflow-hidden">
            <div className="relative aspect-[16/9] w-full bg-[var(--bg)]">
              <Image
                src={item.src}
                alt={item.title}
                fill
                className="object-cover"
                sizes="(max-width: 1200px) 100vw, 1100px"
              />
            </div>
            <div className="p-5">
              <h2 className="text-lg font-medium">{item.title}</h2>
              <p className="mt-1 text-sm text-[var(--muted)]">{item.blurb}</p>
            </div>
          </article>
        ))}
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {[
          ["Harness", "6 zones · ≤1.8 km copper · ≤38 kg", "/calculators"],
          ["Lamps", "≥1100 lm low beam · ≤45 W pair", "/calculators"],
          ["Packaging", "7 longitudinal zones · 48/52 balance", "/architecture"],
        ].map(([t, b, href]) => (
          <Link key={t} href={href} className="panel block p-5 hover:border-[var(--amber-dim)]">
            <h2 className="panel-title">{t}</h2>
            <p className="mt-2 text-sm text-[var(--muted)]">{b}</p>
          </Link>
        ))}
      </section>

      <section className="panel p-5">
        <h2 className="panel-title">Repo documents</h2>
        <ul className="mt-3 space-y-2 text-sm text-[var(--muted)]">
          {DOCS.map((d) => (
            <li key={d.path}>
              <span className="text-[var(--amber)]">{d.label}</span>
              {" — "}
              <code className="text-xs text-[var(--steel)]">{d.path}</code>
            </li>
          ))}
        </ul>
        <pre className="mt-4 overflow-x-auto border border-[var(--line)] bg-[var(--bg)] p-3 font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--amber)]">
          {`python -m svie_physics.design_system
python -m svie_physics.aether_os`}
        </pre>
      </section>
    </div>
  );
}
