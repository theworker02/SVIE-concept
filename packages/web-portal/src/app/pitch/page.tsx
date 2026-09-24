import Image from "next/image";
import Link from "next/link";

const AUDIENCES = [
  {
    title: "Executives / BD",
    time: "8 min",
    steps: ["Open /acquisition scorecard", "Read pitch below", "Open /demo"],
    href: "/acquisition",
  },
  {
    title: "Powertrain engineers",
    time: "15 min",
    steps: ["pytest green", "CLI demo + acquisition_suite", "/calculators"],
    href: "/calculators",
  },
  {
    title: "Counsel / IP",
    time: "20 min",
    steps: ["Term sheet", "Claim charts", "IP inventory"],
    href: "/diligence",
  },
];

const WHY = [
  {
    k: "Production-ready package",
    v: "v1.3 acquisition desk, deal room, and scorecard — close hygiene, not PDFs.",
  },
  {
    k: "Runnable, not slideware",
    v: "Every headline number maps to a pytest golden vector and a YAML SoT file.",
  },
  {
    k: "Fourteen licensable modules",
    v: "SFV through DESIGN, COMPLIANCE, and ACQUIRE — inventory exposes the map.",
  },
  {
    k: "Honest TRL",
    v: "Hardware TRL-3. The monorepo is what is production-ready for close.",
  },
];

export default function PitchPage() {
  return (
    <div className="space-y-12">
      <section className="relative overflow-hidden border border-[var(--line)] px-6 py-14 md:px-12 md:py-16"
        style={{
          background:
            "linear-gradient(135deg, #161b22 0%, #12151a 45%, #1a1814 100%)",
        }}
      >
        <div className="relative flex flex-col gap-8 md:flex-row md:items-center md:justify-between">
          <div className="max-w-2xl">
            <p className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-[0.35em] text-[var(--amber)]">
              ACQUISITION PITCH · v1.3.0
            </p>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight md:text-4xl">
              Powertrain IP you can verify before lunch
            </h1>
            <p className="mt-4 text-lg leading-relaxed text-[var(--muted)]">
              SVIE 1.3 is a production-ready acquisition package: supercritical
              fuel, camless valvetrain, belt-free drive, analog-first HMI,
              compliance paths, and a deal room — with physics, specs, tests,
              and an OEM portal in one archive.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/acquisition" className="btn">
                Acquisition desk
              </Link>
              <Link href="/demo" className="btn" style={{ opacity: 0.9 }}>
                See it work
              </Link>
              <Link href="/diligence" className="btn" style={{ opacity: 0.8 }}>
                Diligence hub
              </Link>
              <Link href="/package" className="btn" style={{ opacity: 0.7 }}>
                Licensing modules
              </Link>
            </div>
          </div>
          <Image
            src="/brand/svie-wordmark.svg"
            alt="SVIE"
            width={320}
            height={72}
            className="border border-[var(--line)] bg-[var(--bg)] p-4"
            priority
          />
        </div>
      </section>

      <section>
        <h2 className="panel-title">Why this is valuable to acquire</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          {WHY.map((item) => (
            <article key={item.k} className="panel p-5">
              <h3 className="font-medium text-[var(--ink)]">{item.k}</h3>
              <p className="mt-2 text-sm leading-relaxed text-[var(--muted)]">
                {item.v}
              </p>
            </article>
          ))}
        </div>
      </section>

      <section className="panel p-6">
        <h2 className="panel-title">The one-sentence deal</h2>
        <p className="mt-4 text-lg leading-relaxed text-[var(--ink)]">
          Exclusive automotive field-of-use license (or full asset purchase) for
          a TRL-3 software diligence package that accelerates architecture,
          claim drafting, and Phase-1 hardware gates — priced on{" "}
          <em className="text-[var(--amber)] not-italic">acceleration</em>, not
          on unproven BTE.
        </p>
      </section>

      <section>
        <h2 className="panel-title">Choose your viewing path</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          {AUDIENCES.map((a) => (
            <article key={a.title} className="panel flex flex-col p-5">
              <div className="font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--amber)]">
                {a.time}
              </div>
              <h3 className="mt-2 font-medium">{a.title}</h3>
              <ol className="mt-3 flex-1 list-decimal space-y-1 pl-4 text-sm text-[var(--muted)]">
                {a.steps.map((s) => (
                  <li key={s}>{s}</li>
                ))}
              </ol>
              <Link href={a.href} className="nav-link mt-4 inline-block">
                Continue →
              </Link>
            </article>
          ))}
        </div>
      </section>

      <section className="panel p-6">
        <h2 className="panel-title">Locked proof points</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {[
            ["ṁ fuel", "28.28 g/s"],
            ["HEX", "23.2 kW"],
            ["Orifice", "0.431 mm²"],
            ["AXIOM RBI", "0"],
          ].map(([k, v]) => (
            <div key={k} className="border border-[var(--line)] px-3 py-3">
              <div className="text-xs uppercase tracking-wider text-[var(--steel)]">
                {k}
              </div>
              <div className="data-value mt-1 text-lg">{v}</div>
            </div>
          ))}
        </div>
        <p className="mt-4 text-sm text-[var(--muted)]">
          Reproduce with <code className="text-[var(--amber)]">pytest</code> and{" "}
          <code className="text-[var(--amber)]">python -m svie_physics.demo</code>.
          BTE 48–52% remains a design target — not a dyno result.
        </p>
      </section>
    </div>
  );
}
