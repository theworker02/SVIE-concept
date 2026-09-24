"use client";

import { useEffect, useMemo, useState } from "react";
import { API_BASE, fetchSpec, fetchSpecList } from "@/lib/api";

/** Static fallback so viewers can browse names when API is down */
const CATALOG: { name: string; pack: string; blurb: string }[] = [
  { name: "svie_v8_52L", pack: "SFV-CORE", blurb: "5.2 L SFV V8 WOT baseline" },
  { name: "sfv_fuel_system", pack: "SFV-CORE", blurb: "Pressure ladder + HEX golden" },
  { name: "piezo_injector", pack: "SFV-CORE", blurb: "Piezo stroke / orifice / driver" },
  { name: "svie_v8_hr_357", pack: "DEVA-HR", blurb: "3.57 L high-RPM H2 DI V8-HR" },
  { name: "deva_valvetrain", pack: "DEVA-HR", blurb: "Camless electromagnetic valves" },
  { name: "h2_combustion_control", pack: "DEVA-HR", blurb: "Lambda / water-DI / NOx" },
  { name: "axiom_drive", pack: "AXIOM-DRIVE", blurb: "Anti-CVT KPIs (RBI = 0)" },
  { name: "ehe_v_bridge", pack: "AXIOM-DRIVE", blurb: "Belt-free hybrid bridge" },
  { name: "cvt_evidence", pack: "AXIOM-DRIVE", blurb: "Slip / efficiency evidence" },
  { name: "hert_transaxle", pack: "AXIOM-DRIVE", blurb: "HERT + GDSA + gears" },
  { name: "12m_ds_transmission", pack: "AXIOM-DRIVE", blurb: "12-speed splitter manual" },
  { name: "9a_mc_transmission", pack: "AXIOM-DRIVE", blurb: "9-speed multi-clutch auto" },
  { name: "nexus_48", pack: "OPS-STACK", blurb: "48 V energy bus budget" },
  { name: "sonic_nvh", pack: "OPS-STACK", blurb: "Secondary imbalance index" },
  { name: "sentinel_safety", pack: "OPS-STACK", blurb: "H2 leak / isolation sensing" },
  { name: "chronos_cold_start", pack: "OPS-STACK", blurb: "Cold-start phase timeline" },
  { name: "trl_roadmap", pack: "OPS-STACK", blurb: "TRL stages + license packs" },
  { name: "blend_brake", pack: "CONTROL", blurb: "Brake blending" },
  { name: "mirage_twin", pack: "CONTROL", blurb: "Twin-path torque" },
  { name: "vector_hcp", pack: "CONTROL", blurb: "Hybrid control policy" },
  { name: "chassis_monocoque", pack: "STRUCTURE", blurb: "Torsion / bending nodes" },
  { name: "breakthrough_subsystems", pack: "STRUCTURE", blurb: "CCD / DKIS / CASMIR" },
  { name: "bom_cost_estimate", pack: "STRUCTURE", blurb: "Order-of-magnitude BOM" },
  { name: "thermal_oil_system", pack: "STRUCTURE", blurb: "Oil / thermal circuit" },
  { name: "engine_cryo_rail", pack: "ENGINE-PLUS", blurb: "CRYO-RAIL buffered SFV rail" },
  { name: "ring_zero", pack: "ENGINE-PLUS", blurb: "RING-ZERO PTWA ring pack" },
  { name: "oil_spine", pack: "ENGINE-PLUS", blurb: "OIL-SPINE girdle gallery" },
  { name: "aether_ign", pack: "ENGINE-PLUS", blurb: "AETHER-IGN plasma/spark" },
  { name: "flux_shift", pack: "TRANS-PLUS", blurb: "FLUX-SHIFT preselect" },
  { name: "gear_mesh_am", pack: "TRANS-PLUS", blurb: "GEAR-MESH-AM lattice" },
  { name: "jet_bearing", pack: "TRANS-PLUS", blurb: "JET-BEARING HERT cooling" },
  { name: "node_cast_body", pack: "BODY-PLUS", blurb: "NODE-CAST hybrid body" },
  { name: "aero_skin", pack: "BODY-PLUS", blurb: "AERO-SKIN active aero" },
  { name: "cell_vault", pack: "BODY-PLUS", blurb: "CELL-VAULT energy vault" },
  { name: "thermal_skin", pack: "BODY-PLUS", blurb: "THERMAL-SKIN rejection" },
  { name: "manufacturing_master", pack: "MFG-PLAN", blurb: "Process routes & cells" },
  { name: "dry_sump_x", pack: "ADDONS", blurb: "DRY-SUMP-X scavenge" },
  { name: "pulse_egr", pack: "ADDONS", blurb: "PULSE-EGR NOx control" },
  { name: "silk_mount", pack: "ADDONS", blurb: "SILK-MOUNT active NVH" },
  { name: "range_bridge", pack: "ADDONS", blurb: "RANGE-BRIDGE series RE" },
  { name: "kers_blend", pack: "ADDONS", blurb: "KERS-BLEND recovery" },
  { name: "validation_matrix", pack: "ADDONS", blurb: "Validation SoT matrix" },
];

export default function SpecsPage() {
  const [names, setNames] = useState<string[]>([]);
  const [active, setActive] = useState<string | null>(null);
  const [doc, setDoc] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState("");
  const [pack, setPack] = useState<string>("ALL");

  useEffect(() => {
    void (async () => {
      try {
        const { specs } = await fetchSpecList();
        const normalized = specs.map((s) => s.replace(/\.yaml$/, ""));
        setNames(normalized);
        if (normalized[0]) setActive(normalized[0]);
        setError(null);
      } catch (e) {
        setNames(CATALOG.map((c) => c.name));
        setActive(CATALOG[0]?.name ?? null);
        setError(
          e instanceof Error
            ? `${e.message}. Showing catalog names — start API at ${API_BASE} to load YAML bodies.`
            : "API offline — catalog only",
        );
      }
    })();
  }, []);

  useEffect(() => {
    if (!active) return;
    const file = active.endsWith(".yaml") ? active : `${active}.yaml`;
    void (async () => {
      try {
        const data = await fetchSpec(file.replace(/\.yaml$/, ""));
        setDoc(JSON.stringify(data, null, 2));
      } catch {
        const meta = CATALOG.find(
          (c) => c.name === active.replace(/\.yaml$/, ""),
        );
        setDoc(
          meta
            ? JSON.stringify(
                {
                  _note: "API offline — metadata only. Start npm run dev:api.",
                  file: `${meta.name}.yaml`,
                  licensing_package: meta.pack,
                  summary: meta.blurb,
                },
                null,
                2,
              )
            : "// Unable to load spec",
        );
      }
    })();
  }, [active]);

  const filtered = useMemo(() => {
    const q = filter.toLowerCase();
    return CATALOG.filter((c) => {
      const inPack = pack === "ALL" || c.pack === pack;
      const inQ =
        !q ||
        c.name.includes(q) ||
        c.blurb.toLowerCase().includes(q) ||
        c.pack.toLowerCase().includes(q);
      return inPack && inQ;
    });
  }, [filter, pack]);

  const packs = ["ALL", ...Array.from(new Set(CATALOG.map((c) => c.pack)))];

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight">Machine-Readable Specs</h1>
        <p className="mt-2 max-w-2xl text-[var(--muted)]">
          Twenty-four YAML sources of truth, tagged by licensing package. Bodies
          load from the physics API so the portal never invents numbers.
        </p>
      </header>

      {error ? (
        <div className="panel border-[var(--line)] px-4 py-3 text-sm text-[var(--steel)]">
          {error}
        </div>
      ) : null}

      <div className="flex flex-wrap gap-3">
        <input
          type="search"
          placeholder="Filter specs…"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="min-w-[12rem] flex-1 border border-[var(--line)] bg-[var(--bg)] px-3 py-2 font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--ink)] outline-none focus:border-[var(--amber)]"
        />
        <div className="flex flex-wrap gap-2">
          {packs.map((p) => (
            <button
              key={p}
              type="button"
              className="btn"
              style={{
                opacity: pack === p ? 1 : 0.55,
                padding: "0.4rem 0.7rem",
                fontSize: "0.65rem",
              }}
              onClick={() => setPack(p)}
            >
              {p}
            </button>
          ))}
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[280px_1fr]">
        <aside className="panel max-h-[70vh] overflow-auto p-3">
          <div className="panel-title mb-3 px-2">
            Files ({filtered.length}
            {names.length ? ` · API ${names.length}` : ""})
          </div>
          <ul className="space-y-1">
            {filtered.map((item) => {
              const key = item.name;
              const selected = active?.replace(/\.yaml$/, "") === key;
              return (
                <li key={key}>
                  <button
                    type="button"
                    className="w-full px-2 py-2 text-left hover:bg-[rgba(255,255,255,0.04)]"
                    style={{
                      borderLeft: selected
                        ? "2px solid var(--amber)"
                        : "2px solid transparent",
                    }}
                    onClick={() => setActive(key)}
                  >
                    <div
                      className="font-[family-name:var(--font-ibm-mono)] text-xs"
                      style={{ color: selected ? "var(--amber)" : "var(--ink)" }}
                    >
                      {key}
                    </div>
                    <div className="mt-0.5 text-[10px] text-[var(--steel)]">
                      {item.pack} · {item.blurb}
                    </div>
                  </button>
                </li>
              );
            })}
          </ul>
        </aside>
        <pre className="panel max-h-[70vh] overflow-auto p-4 font-[family-name:var(--font-ibm-mono)] text-xs leading-relaxed text-[var(--steel)]">
          {doc || "Select a spec…"}
        </pre>
      </div>
    </div>
  );
}
