"use client";

import { useEffect, useState } from "react";

type Inventory = {
  version: string;
  counts: Record<string, number>;
  licensing_packages: { id: string; name: string; includes: string[]; specs: string[] }[];
  headline_metrics: Record<string, number>;
  portal_routes: string[];
};

const API =
  process.env.NEXT_PUBLIC_SVIE_API_URL?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

const CHECKLIST = [
  "Open /pitch (exec path) or VIEWER-GUIDE.md",
  "Run pytest golden suite",
  "Run python -m svie_physics.demo",
  "Run python -m svie_physics.inventory",
  "Review VALUE-THESIS + EXECUTIVE-BRIEF + IP-INVENTORY",
  "Walk claim charts vs YAML",
  "Review RISK-REGISTER + HARDWARE-ROADMAP + COMPETITIVE-MATRIX",
  "Counsel: FTO / assignment schedule",
];

export function DiligenceHub() {
  const [inv, setInv] = useState<Inventory | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [checked, setChecked] = useState<Record<number, boolean>>({});

  useEffect(() => {
    void (async () => {
      try {
        const res = await fetch(`${API}/inventory`, { cache: "no-store" });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        setInv((await res.json()) as Inventory);
        setError(null);
      } catch (e) {
        setError(
          e instanceof Error
            ? `${e.message}. Start API: npm run dev:api`
            : "API unavailable",
        );
      }
    })();
  }, []);

  return (
    <div className="space-y-10">
      <header>
        <p className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-[0.3em] text-[var(--amber)]">
          ACQUISITION DILIGENCE
        </p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight">Diligence hub</h1>
        <p className="mt-3 max-w-2xl text-[var(--muted)]">
          Live package inventory, licensing modules, and a buyer checklist. Mirror
          of Acquisition.md for on-screen review.
        </p>
      </header>

      {error && (
        <p className="border border-[var(--danger)] px-4 py-3 text-sm text-[var(--danger)]">
          {error}
        </p>
      )}

      {inv && (
        <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {Object.entries(inv.counts).map(([k, v]) => (
            <div key={k} className="panel px-4 py-3">
              <div className="text-[10px] uppercase tracking-wider text-[var(--steel)]">
                {k.replace(/_/g, " ")}
              </div>
              <div className="data-value mt-1 text-2xl">{v}</div>
            </div>
          ))}
        </section>
      )}

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="panel p-5">
          <h2 className="panel-title">Buyer checklist</h2>
          <ul className="mt-4 space-y-2">
            {CHECKLIST.map((item, i) => (
              <li key={item} className="flex items-start gap-3 text-sm">
                <input
                  type="checkbox"
                  className="mt-1 accent-[var(--amber)]"
                  checked={!!checked[i]}
                  onChange={() =>
                    setChecked((prev) => ({ ...prev, [i]: !prev[i] }))
                  }
                />
                <span className={checked[i] ? "text-[var(--steel)] line-through" : ""}>
                  {item}
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div className="panel p-5">
          <h2 className="panel-title">Headline metrics</h2>
          {inv ? (
            <div className="mt-4 grid gap-2 sm:grid-cols-2">
              {Object.entries(inv.headline_metrics).map(([k, v]) => (
                <div key={k} className="border border-[var(--line)] px-3 py-2">
                  <div className="text-[10px] uppercase tracking-wider text-[var(--steel)]">
                    {k.replace(/_/g, " ")}
                  </div>
                  <div className="data-value mt-1">{v}</div>
                </div>
              ))}
            </div>
          ) : (
            <p className="mt-4 text-sm text-[var(--muted)]">Waiting for API…</p>
          )}
        </div>
      </section>

      <section className="panel p-5">
        <h2 className="panel-title">Licensing packages</h2>
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          {(inv?.licensing_packages ?? []).map((pkg) => (
            <article key={pkg.id} className="border border-[var(--line)] p-4">
              <div className="font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--amber)]">
                {pkg.id}
              </div>
              <h3 className="mt-1 font-medium">{pkg.name}</h3>
              <p className="mt-2 text-xs text-[var(--muted)]">
                Modules: {pkg.includes.join(", ")}
              </p>
              <p className="mt-1 text-xs text-[var(--steel)]">
                Specs: {pkg.specs.join(", ")}
              </p>
            </article>
          ))}
          {!inv && (
            <p className="text-sm text-[var(--muted)]">
              Start the physics API to load package definitions.
            </p>
          )}
        </div>
      </section>

      <section className="panel p-5">
        <h2 className="panel-title">Document pointers</h2>
        <p className="mt-3 text-sm text-[var(--muted)]">
          In the repo: Acquisition.md · docs/acquisition/* · docs/INDEX.md ·
          SECURITY.md · specs/CATALOG.md. Portal routes include{" "}
          {(inv?.portal_routes ?? ["/demo", "/package"]).join(", ")}.
        </p>
        {inv && (
          <p className="mt-2 font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--steel)]">
            inventory API v{inv.version}
          </p>
        )}
      </section>
    </div>
  );
}
