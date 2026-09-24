"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

type AcqPayload = {
  readiness: {
    weighted_score: number;
    dimension_count: number;
    gates_pass: boolean;
    gate_results: Record<string, boolean>;
    hardware_trl_ceiling: number;
    package_claim: string;
    production_ready_acquisition: boolean;
  };
  deal: {
    structures: number;
    preferred_structure: string;
    escrow: boolean;
    earnout_gates: number;
  };
  data_room: {
    folders: number;
    access_tiers: number;
    term_sheet_present: boolean;
  };
};

const DOCS = [
  { label: "Acquisition.md", path: "Acquisition.md" },
  { label: "Production readiness", path: "docs/acquisition/PRODUCTION-READINESS.md" },
  { label: "Term sheet", path: "docs/acquisition/TERM-SHEET.md" },
  { label: "Deal structures", path: "docs/acquisition/DEAL-STRUCTURES.md" },
  { label: "Data room", path: "docs/acquisition/DATA-ROOM.md" },
  { label: "Closing checklist", path: "docs/acquisition/CLOSING-CHECKLIST.md" },
];

export function AcquisitionDesk() {
  const [data, setData] = useState<AcqPayload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    void apiGet("/calc/acquisition")
      .then((d) => {
        setData(d as AcqPayload);
        setOffline(false);
      })
      .catch(() => {
        setOffline(true);
        setError("API offline — run npm run dev:api, or use CLI: python -m svie_physics.acquisition_suite");
        setData({
          readiness: {
            weighted_score: 90.15,
            dimension_count: 9,
            gates_pass: true,
            gate_results: {
              score: true,
              specs: true,
              tests: true,
              packages: true,
              routes: true,
            },
            hardware_trl_ceiling: 3,
            package_claim: "acquisition_package_production_ready",
            production_ready_acquisition: true,
          },
          deal: {
            structures: 3,
            preferred_structure: "exclusive_fou_plus_option",
            escrow: true,
            earnout_gates: 3,
          },
          data_room: {
            folders: 8,
            access_tiers: 3,
            term_sheet_present: true,
          },
        });
      });
  }, []);

  const r = data?.readiness;

  return (
    <div className="space-y-10">
      <header>
        <p className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-[0.35em] text-[var(--amber)]">
          ACQUISITION DESK · v1.3.0 · PRODUCTION-READY PACKAGE
        </p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
          Close on verified engineering — not slideware
        </h1>
        <p className="mt-4 max-w-2xl text-base leading-relaxed text-[var(--muted)]">
          Live readiness scorecard for the SVIE monorepo. Hardware stays TRL-3;
          the diligence package is what is production-ready for OEM close.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link href="/pitch" className="btn">
            Pitch
          </Link>
          <Link href="/diligence" className="btn" style={{ opacity: 0.9 }}>
            Diligence hub
          </Link>
          <Link href="/hmi" className="btn" style={{ opacity: 0.8 }}>
            AETHER-OS
          </Link>
        </div>
      </header>

      {error && (
        <p className="text-sm text-[var(--steel)]">
          {offline ? "Showing locked offline snapshot. " : ""}
          {error}
        </p>
      )}

      {r && (
        <section
          className="panel p-6 md:p-8"
          style={{
            background:
              "linear-gradient(165deg, #1a222c 0%, #12161c 55%, #1a1814 100%)",
          }}
        >
          <div className="flex flex-wrap items-end justify-between gap-6">
            <div>
              <p className="panel-title">Weighted readiness</p>
              <div className="data-value mt-2 text-5xl md:text-6xl">
                {r.weighted_score.toFixed(1)}
              </div>
              <p className="mt-2 text-sm text-[var(--muted)]">
                Gate ≥ 85 · {r.dimension_count} dimensions
              </p>
            </div>
            <div className="text-right">
              <div
                className="font-[family-name:var(--font-ibm-mono)] text-sm tracking-wider"
                style={{ color: r.production_ready_acquisition ? "var(--ok)" : "var(--danger)" }}
              >
                {r.production_ready_acquisition
                  ? "PRODUCTION_READY_ACQUISITION"
                  : "GATES_FAILED"}
              </div>
              <p className="mt-2 text-xs text-[var(--steel)]">
                Hardware TRL ceiling: {r.hardware_trl_ceiling}
              </p>
              <p className="mt-1 text-xs text-[var(--steel)]">{r.package_claim}</p>
            </div>
          </div>

          <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
            {Object.entries(r.gate_results).map(([k, ok]) => (
              <div key={k} className="border border-[var(--line)] px-3 py-3">
                <div className="text-[10px] uppercase tracking-wider text-[var(--steel)]">
                  {k}
                </div>
                <div
                  className="mt-1 font-[family-name:var(--font-ibm-mono)] text-sm"
                  style={{ color: ok ? "var(--ok)" : "var(--danger)" }}
                >
                  {ok ? "PASS" : "FAIL"}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {data && (
        <section className="grid gap-4 md:grid-cols-2">
          <article className="panel p-5">
            <h2 className="panel-title">Preferred deal</h2>
            <p className="mt-3 text-lg font-medium text-[var(--ink)]">
              {data.deal.preferred_structure.replaceAll("_", " ")}
            </p>
            <ul className="mt-3 space-y-1 text-sm text-[var(--muted)]">
              <li>{data.deal.structures} structures modeled</li>
              <li>Source escrow: {data.deal.escrow ? "required" : "optional"}</li>
              <li>{data.deal.earnout_gates} earnout gates (G1–G3)</li>
            </ul>
          </article>
          <article className="panel p-5">
            <h2 className="panel-title">Data room</h2>
            <p className="mt-3 text-lg font-medium text-[var(--ink)]">
              {data.data_room.folders} folders · {data.data_room.access_tiers} tiers
            </p>
            <p className="mt-3 text-sm text-[var(--muted)]">
              Term sheet present:{" "}
              {data.data_room.term_sheet_present ? "yes" : "missing"}
            </p>
          </article>
        </section>
      )}

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
          {`python -m svie_physics.acquisition_suite
python -m svie_physics.compliance
python -m svie_physics.validate`}
        </pre>
      </section>
    </div>
  );
}
