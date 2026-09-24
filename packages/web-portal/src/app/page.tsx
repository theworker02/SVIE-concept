import Image from "next/image";
import Link from "next/link";

export default function HomePage() {
  return (
    <div className="space-y-12">
      <section className="relative overflow-hidden border border-[var(--line)] bg-[linear-gradient(135deg,#1a222c_0%,#12161c_55%,#1e1820_100%)] px-6 py-14 md:px-12 md:py-20">
        <div
          className="pointer-events-none absolute inset-0 opacity-40"
          style={{
            backgroundImage:
              "repeating-linear-gradient(90deg, transparent, transparent 47px, rgba(122,138,154,0.08) 48px), repeating-linear-gradient(0deg, transparent, transparent 47px, rgba(122,138,154,0.06) 48px)",
          }}
        />
        <div
          className="pointer-events-none absolute -right-20 top-10 h-64 w-64 rounded-full opacity-20"
          style={{
            background:
              "radial-gradient(circle, rgba(212,160,23,0.35), transparent 70%)",
            animation: "demo-rise 1.2s ease-out both",
          }}
        />
        <div className="relative flex flex-col gap-10 md:flex-row md:items-center md:justify-between">
          <div className="max-w-2xl">
            <p className="font-[family-name:var(--font-ibm-mono)] text-sm tracking-[0.35em] text-[var(--amber)]">
              SVIE · v1.3.1 · PRODUCTION-READY ACQUISITION
            </p>
            <h1 className="mt-4 text-4xl font-semibold tracking-tight text-[var(--ink)] md:text-5xl">
              Supercritical Vapor-Injection Engine
            </h1>
            <p className="mt-5 max-w-xl text-lg text-[var(--muted)]">
              Close-ready powertrain IP monorepo — runnable physics, deal room,
              analog-first HMI, compliance paths — verified before lunch, not
              slideware.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/lab" className="btn">
                Physics lab
              </Link>
              <Link href="/acquisition" className="btn" style={{ opacity: 0.95 }}>
                Acquisition desk
              </Link>
              <Link href="/demo" className="btn" style={{ opacity: 0.9 }}>
                Live demo
              </Link>
              <Link href="/pitch" className="btn" style={{ opacity: 0.9 }}>
                Pitch
              </Link>
              <Link href="/hmi" className="btn" style={{ opacity: 0.9 }}>
                AETHER-OS HMI
              </Link>
              <Link href="/design" className="btn" style={{ opacity: 0.85 }}>
                Vehicle design
              </Link>
              <Link href="/demo" className="btn" style={{ opacity: 0.75 }}>
                Guided demo
              </Link>
            </div>
          </div>
          <Image
            src="/brand/svie-logo.png"
            alt="SVIE official mark"
            width={180}
            height={180}
            className="brand-mark mx-auto border border-[var(--line)] shadow-[0_0_60px_rgba(212,160,23,0.08)] md:mx-0"
            priority
          />
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {[
          {
            title: "For viewers",
            body: "Start at /pitch — three audience paths (exec, engineer, counsel) with timed walkthroughs.",
            href: "/pitch",
          },
          {
            title: "For diligence",
            body: "Live inventory, six licensing modules, buyer checklist, and Acquisition.md library.",
            href: "/diligence",
          },
          {
            title: "For engineers",
            body: "pytest golden vectors, CLI demo, YAML specs, and interactive calculators on FastAPI.",
            href: "/calculators",
          },
        ].map((card) => (
          <Link key={card.title} href={card.href} className="panel block p-5 transition-colors hover:border-[var(--amber-dim)]">
            <h2 className="panel-title">{card.title}</h2>
            <p className="mt-3 text-sm leading-relaxed text-[var(--muted)]">{card.body}</p>
            <span className="nav-link mt-4 inline-block">Open →</span>
          </Link>
        ))}
      </section>

      <section className="panel p-6">
        <h2 className="panel-title">WOT Baseline Snapshot — Golden Locked</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {[
            ["Displacement", "5.204 L"],
            ["Peak target", "≈ 700 hp @ 8500"],
            ["ṁ fuel", "28.28 g/s"],
            ["Q̇ HEX", "23.2 kW"],
            ["Recovery", "≈ 6.2% exhaust"],
            ["A_o req / max", "0.431 / 0.630 mm²"],
            ["Piezo drive", "16.88 W/valve raw"],
            ["AXIOM RBI", "0 (no belt)"],
          ].map(([k, v]) => (
            <div key={k} className="border border-[var(--line)] px-3 py-3">
              <div className="text-xs uppercase tracking-wider text-[var(--steel)]">{k}</div>
              <div className="data-value mt-1 text-sm">{v}</div>
            </div>
          ))}
        </div>
        <p className="mt-4 text-sm text-[var(--muted)]">
          Reproduce: <code className="text-[var(--amber)]">python -m svie_physics.demo</code>
          {" · "}
          BTE 48–52% is a design target, not a dyno measurement.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <article className="panel p-5">
          <h2 className="panel-title">Honest TRL</h2>
          <p className="mt-3 text-sm leading-relaxed text-[var(--muted)]">
            Thermo models: <span className="text-[var(--amber)]">TRL-3</span> in-repo.
            Hardware: TRL-1–2 concept. Portal software: locally runnable.
            Acquisition value is architecture acceleration — then fund G1 spray-rig.
          </p>
        </article>
        <article className="panel p-5">
          <h2 className="panel-title">Suggested deal frame</h2>
          <p className="mt-3 text-sm leading-relaxed text-[var(--muted)]">
            Exclusive automotive field-of-use license with buyout option, or full
            asset purchase. Modular packages available (SFV-CORE, AXIOM-DRIVE, …).
          </p>
        </article>
      </section>
    </div>
  );
}
