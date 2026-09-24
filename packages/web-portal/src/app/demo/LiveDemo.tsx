"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";

type DemoStep = {
  id: string;
  title: string;
  summary: string;
  metrics: Record<string, unknown>;
  module: string;
};

type DemoPayload = {
  version: string;
  steps: DemoStep[];
};

const API =
  process.env.NEXT_PUBLIC_SVIE_API_URL?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

const BASE = process.env.NEXT_PUBLIC_BASE_PATH || "";

const FALLBACK: DemoPayload = {
  version: "1.3.0",
  steps: [
    {
      id: "01-sfv-wot",
      title: "SFV — WOT air/fuel baseline",
      summary: "Supercritical flash fuel delivery sized at wide-open throttle.",
      metrics: { m_dot_fuel_g_s: 28.28, e_in_kw: 1280.7 },
      module: "svie_physics.air_fuel",
    },
    {
      id: "02-hex",
      title: "HEX — exhaust recuperation",
      summary: "Heat exchanger duty recovering supercritical enthalpy into the fuel path.",
      metrics: { q_hex_kw: 23.2 },
      module: "svie_physics.heat_exchanger",
    },
    {
      id: "03-hem",
      title: "HEM — choked flash orifice",
      summary: "Homogeneous-equilibrium choked flow sets injector orifice area.",
      metrics: { a_o_required_mm2: 0.431, is_choked: true },
      module: "svie_physics.hem_choked_flow",
    },
    {
      id: "04-axiom",
      title: "AXIOM — anti-CVT rubber-band index",
      summary: "Discrete multi-ratio path; rubber-band index locked at 0 (no belt).",
      metrics: { rubber_band_index: 0 },
      module: "svie_physics.axiom_drive",
    },
    {
      id: "05-trl",
      title: "TRL roadmap — hardware honesty",
      summary: "Hardware remains TRL-3; the acquisition package is production-ready.",
      metrics: { current_trl: 3 },
      module: "svie_physics.chronos_sentinel",
    },
    {
      id: "06-acquire",
      title: "Acquisition suite — package readiness",
      summary: "Weighted readiness scorecard for OEM close.",
      metrics: { weighted_score: 90.15, production_ready_acquisition: true },
      module: "svie_physics.acquisition_suite",
    },
  ],
};

function primaryMetric(metrics: Record<string, unknown>): { label: string; value: string } {
  const keys = Object.keys(metrics);
  const prefer = [
    "m_dot_fuel_g_s",
    "q_hex_kw",
    "a_o_required_mm2",
    "rubber_band_index",
    "current_trl",
    "weighted_score",
    "production_ready_acquisition",
  ];
  const key = prefer.find((k) => k in metrics) ?? keys[0];
  if (!key) return { label: "—", value: "—" };
  return { label: key.replace(/_/g, " "), value: String(metrics[key]) };
}

export function LiveDemo() {
  const [steps, setSteps] = useState<DemoStep[]>(FALLBACK.steps);
  const [version, setVersion] = useState(FALLBACK.version);
  const [source, setSource] = useState<"api" | "pages" | "embedded">("embedded");
  const [error, setError] = useState<string | null>(null);
  const [active, setActive] = useState(0);
  const [playing, setPlaying] = useState(true);

  useEffect(() => {
    void (async () => {
      try {
        const res = await fetch(`${API}/demo`, { cache: "no-store" });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = (await res.json()) as DemoPayload;
        setSteps(data.steps);
        setVersion(data.version);
        setSource("api");
        setError(null);
        return;
      } catch {
        /* try static Pages asset */
      }
      try {
        const res = await fetch(`${BASE}/demo/golden.json`, { cache: "force-cache" });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = (await res.json()) as DemoPayload;
        setSteps(data.steps);
        setVersion(data.version);
        setSource("pages");
        setError(null);
      } catch (e) {
        setSource("embedded");
        setError(
          e instanceof Error
            ? `Using embedded golden narrative (${e.message}).`
            : "Using embedded golden narrative.",
        );
      }
    })();
  }, []);

  useEffect(() => {
    if (!playing || steps.length === 0) return;
    const id = window.setInterval(() => {
      setActive((i) => (i + 1) % steps.length);
    }, 3200);
    return () => window.clearInterval(id);
  }, [playing, steps.length]);

  const modeLabel =
    source === "api" ? "LIVE API" : source === "pages" ? "LIVE PAGES" : "EMBEDDED";

  return (
    <div className="space-y-12">
      <section className="relative overflow-hidden border border-[var(--line)] bg-[linear-gradient(160deg,#141820_0%,#1a1520_50%,#12161c_100%)] px-6 py-12 md:px-12">
        <div
          className="pointer-events-none absolute inset-0 opacity-30"
          style={{
            backgroundImage:
              "radial-gradient(circle at 20% 40%, rgba(212,160,23,0.15), transparent 45%), radial-gradient(circle at 80% 20%, rgba(122,138,154,0.12), transparent 40%)",
          }}
        />
        <div className="relative flex flex-col gap-8 md:flex-row md:items-end md:justify-between">
          <div className="max-w-2xl">
            <p className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-[0.35em] text-[var(--amber)]">
              LIVE DEMO · v{version} · {modeLabel}
            </p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-[var(--ink)] md:text-4xl">
              How SVIE works
            </h1>
            <p className="mt-4 text-base leading-relaxed text-[var(--muted)]">
              Six diligence stops from supercritical fuel to acquisition readiness —
              each figure maps to pytest golden vectors. Works on GitHub Pages without
              a local API.
            </p>
            {error && <p className="mt-3 text-sm text-[var(--steel)]">{error}</p>}
            <div className="mt-6 flex flex-wrap gap-3">
              <button type="button" className="btn" onClick={() => setPlaying((p) => !p)}>
                {playing ? "Pause tour" : "Play tour"}
              </button>
              <Link href="/acquisition" className="btn" style={{ opacity: 0.85 }}>
                Acquisition desk
              </Link>
              <Link href="/hmi" className="btn" style={{ opacity: 0.75 }}>
                AETHER-OS
              </Link>
            </div>
          </div>
          <div className="flex shrink-0 items-center gap-4">
            <Image
              src="/brand/svie-logo.png"
              alt="SVIE"
              width={72}
              height={72}
              className="border border-[var(--line)]"
            />
            <code className="font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--steel)]">
              python -m svie_physics.demo
            </code>
          </div>
        </div>
      </section>

      {/* Active spotlight */}
      {steps[active] && (
        <section
          className="panel p-6 md:p-8"
          style={{
            background:
              "linear-gradient(165deg, #1a222c 0%, #12161c 55%, #1a1814 100%)",
          }}
        >
          <p className="panel-title">
            Step {String(active + 1).padStart(2, "0")} / {String(steps.length).padStart(2, "0")}
          </p>
          <h2 className="mt-3 text-2xl font-semibold tracking-tight">{steps[active].title}</h2>
          <p className="mt-3 max-w-2xl text-[var(--muted)]">{steps[active].summary}</p>
          <div className="mt-6 flex flex-wrap gap-4">
            {Object.entries(steps[active].metrics).map(([k, v]) => (
              <div key={k} className="border border-[var(--line)] px-4 py-3">
                <div className="text-[10px] uppercase tracking-wider text-[var(--steel)]">
                  {k.replace(/_/g, " ")}
                </div>
                <div className="data-value mt-1 text-xl">{String(v)}</div>
              </div>
            ))}
          </div>
          <div className="mt-6 flex flex-wrap gap-2">
            {steps.map((_, i) => (
              <button
                key={steps[i].id}
                type="button"
                aria-label={`Go to step ${i + 1}`}
                onClick={() => {
                  setActive(i);
                  setPlaying(false);
                }}
                className="h-2 w-8 border border-[var(--line)]"
                style={{
                  background: i === active ? "var(--amber)" : "transparent",
                }}
              />
            ))}
          </div>
        </section>
      )}

      <ol className="space-y-4">
        {steps.map((step, i) => {
          const metric = primaryMetric(step.metrics);
          const on = i === active;
          return (
            <li
              key={step.id}
              className="demo-step panel grid gap-4 p-5 md:grid-cols-[auto_1fr_auto] md:items-center"
              style={{
                animationDelay: `${i * 80}ms`,
                borderColor: on ? "var(--amber-dim)" : undefined,
                opacity: on ? 1 : 0.72,
              }}
            >
              <button
                type="button"
                className="font-[family-name:var(--font-ibm-mono)] text-2xl text-[var(--amber)]"
                onClick={() => {
                  setActive(i);
                  setPlaying(false);
                }}
              >
                {String(i + 1).padStart(2, "0")}
              </button>
              <div>
                <h2 className="text-lg font-medium text-[var(--ink)]">{step.title}</h2>
                <p className="mt-1 text-sm leading-relaxed text-[var(--muted)]">{step.summary}</p>
                <p className="mt-2 font-[family-name:var(--font-ibm-mono)] text-[10px] tracking-wider text-[var(--steel)]">
                  {step.module}
                </p>
              </div>
              <div className="border border-[var(--line)] px-4 py-3 text-right md:min-w-[8rem]">
                <div className="text-[10px] uppercase tracking-wider text-[var(--steel)]">
                  {metric.label}
                </div>
                <div className="data-value mt-1 text-lg">{metric.value}</div>
              </div>
            </li>
          );
        })}
      </ol>

      <section className="panel p-6">
        <h2 className="panel-title">Run it yourself</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <div>
            <p className="text-sm text-[var(--muted)]">CLI program</p>
            <pre className="mt-2 overflow-x-auto border border-[var(--line)] bg-[var(--bg)] p-3 font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--amber)]">
              {`python -m pip install -e "./packages/physics-engine[dev]"
python -m svie_physics.demo
python -m svie_physics.acquisition_suite`}
            </pre>
          </div>
          <div>
            <p className="text-sm text-[var(--muted)]">Local portal + API</p>
            <pre className="mt-2 overflow-x-auto border border-[var(--line)] bg-[var(--bg)] p-3 font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--amber)]">
              {`npm run dev:api
npm run dev:portal
# /demo · /acquisition · /hmi`}
            </pre>
          </div>
        </div>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link href="/acquisition" className="btn">
            Acquisition desk
          </Link>
          <Link href="/calculators" className="btn" style={{ opacity: 0.85 }}>
            Calculators
          </Link>
          <Link href="/package" className="btn" style={{ opacity: 0.7 }}>
            Package map
          </Link>
        </div>
      </section>
    </div>
  );
}
