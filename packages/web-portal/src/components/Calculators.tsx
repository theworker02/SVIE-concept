"use client";

import { useCallback, useEffect, useState } from "react";
import {
  API_BASE,
  type AirFuelResult,
  type DriverResult,
  type HemResult,
  type HexResult,
  type PiezoResult,
  type WotBundle,
  fetchDriver,
  fetchHem,
  fetchHex,
  fetchPiezo,
  fetchWotBundle,
  postAirFuel,
} from "@/lib/api";
import { Metric, fmt } from "./Metric";

type Tab =
  | "wot"
  | "hex"
  | "orifice"
  | "driver"
  | "chassis"
  | "hert"
  | "breakthrough"
  | "hr"
  | "deva"
  | "h2"
  | "bom"
  | "cvt"
  | "axiom"
  | "nexus"
  | "ops"
  | "control"
  | "platform"
  | "mfg"
  | "addons"
  | "validate";

const API =
  process.env.NEXT_PUBLIC_SVIE_API_URL?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

async function apiGet(path: string) {
  const res = await fetch(`${API}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`API ${path} failed: ${res.status}`);
  return res.json();
}

export function Calculators() {
  const [tab, setTab] = useState<Tab>("wot");
  const [error, setError] = useState<string | null>(null);
  const [bundle, setBundle] = useState<WotBundle | null>(null);
  const [rpm, setRpm] = useState(8500);
  const [afr, setAfr] = useState(16.2);
  const [etaV, setEtaV] = useState(1.05);
  const [airFuel, setAirFuel] = useState<AirFuelResult | null>(null);
  const [hex, setHex] = useState<HexResult | null>(null);
  const [hem, setHem] = useState<HemResult | null>(null);
  const [piezo, setPiezo] = useState<PiezoResult | null>(null);
  const [driver, setDriver] = useState<DriverResult | null>(null);
  const [chassis, setChassis] = useState<Record<string, unknown> | null>(null);
  const [hert, setHert] = useState<Record<string, unknown> | null>(null);
  const [gdsa, setGdsa] = useState<Record<string, unknown> | null>(null);
  const [gears, setGears] = useState<Record<string, unknown> | null>(null);
  const [breakthrough, setBreakthrough] = useState<Record<string, unknown> | null>(null);
  const [hrArch, setHrArch] = useState<Record<string, unknown> | null>(null);
  const [deva, setDeva] = useState<Record<string, unknown> | null>(null);
  const [h2, setH2] = useState<Record<string, unknown> | null>(null);
  const [bom, setBom] = useState<Record<string, unknown> | null>(null);
  const [cvt, setCvt] = useState<Record<string, unknown> | null>(null);
  const [axiomPack, setAxiomPack] = useState<Record<string, unknown> | null>(null);
  const [nexus, setNexus] = useState<Record<string, unknown> | null>(null);
  const [ops, setOps] = useState<Record<string, unknown> | null>(null);
  const [control, setControl] = useState<Record<string, unknown> | null>(null);
  const [platform, setPlatform] = useState<Record<string, unknown> | null>(null);
  const [mfg, setMfg] = useState<Record<string, unknown> | null>(null);
  const [addons, setAddons] = useState<Record<string, unknown> | null>(null);
  const [validation, setValidation] = useState<Record<string, unknown> | null>(null);
  const [h2Lambda, setH2Lambda] = useState(1.05);
  const [h2Water, setH2Water] = useState(0.15);

  const loadBaseline = useCallback(async () => {
    setError(null);
    try {
      const b = await fetchWotBundle();
      setBundle(b);
      setAirFuel(b.air_fuel);
      setHex(b.heat_exchanger);
      setHem(b.hem);
      setPiezo(b.piezo);
      setDriver(b.driver);
    } catch (e) {
      setError(
        e instanceof Error
          ? `${e.message}. Start API: npm run dev:api. Expected ${API_BASE}`
          : "API unavailable",
      );
    }
  }, []);

  useEffect(() => {
    void loadBaseline();
  }, [loadBaseline]);

  // Live WOT recompute — no button required
  useEffect(() => {
    if (tab !== "wot") return;
    const handle = window.setTimeout(() => {
      void postAirFuel({
        displacement_m3: 0.005204,
        rpm,
        volumetric_efficiency: etaV,
        afr,
        air_density_kg_m3: 1.184,
      })
        .then(setAirFuel)
        .catch(() => {
          /* keep last good / offline */
        });
    }, 80);
    return () => window.clearTimeout(handle);
  }, [tab, rpm, afr, etaV]);

  const tabs: { id: Tab; label: string }[] = [
    { id: "wot", label: "WOT Mass Flow" },
    { id: "hex", label: "HEX Recuperation" },
    { id: "orifice", label: "Orifice / Piezo" },
    { id: "driver", label: "GaN Driver" },
    { id: "chassis", label: "Chassis Kθ" },
    { id: "hert", label: "HERT / GDSA" },
    { id: "breakthrough", label: "Breakthrough" },
    { id: "hr", label: "V8-HR 3.57L" },
    { id: "deva", label: "DEVA Power" },
    { id: "h2", label: "H2 Combustion" },
    { id: "bom", label: "BOM Cost" },
    { id: "cvt", label: "Anti-CVT" },
    { id: "axiom", label: "AXIOM" },
    { id: "nexus", label: "NEXUS-48" },
    { id: "ops", label: "CHRONOS/TRL" },
    { id: "control", label: "BLEND/MIRAGE" },
    { id: "platform", label: "Platform+" },
    { id: "mfg", label: "Manufacturing" },
    { id: "addons", label: "Add-ons" },
    { id: "validate", label: "Validate" },
  ];

  const cold = hert?.cold as Record<string, number> | undefined;
  const ceb = hert?.ceb as Record<string, number> | undefined;
  const ccd = breakthrough?.ccd as Record<string, number> | undefined;
  const dkis = breakthrough?.dkis_tff as Record<string, number> | undefined;
  const shiftSteps =
    (gears?.shift_steps as { frm: string; to: string; rpm_drop: number }[] | undefined) ??
    [];

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-2">
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            className="btn"
            style={{
              opacity: tab === t.id ? 1 : 0.65,
              borderColor: tab === t.id ? "var(--amber)" : undefined,
            }}
            onClick={() => {
              setTab(t.id);
              if (t.id === "chassis") void apiGet("/calc/chassis").then(setChassis).catch((e) => setError(String(e)));
              if (t.id === "hert")
                void Promise.all([
                  apiGet("/calc/hert"),
                  apiGet("/calc/gdsa"),
                  apiGet("/calc/gears"),
                ])
                  .then(([h, g, gr]) => {
                    setHert(h);
                    setGdsa(g);
                    setGears(gr);
                  })
                  .catch((e) => setError(String(e)));
              if (t.id === "breakthrough")
                void apiGet("/calc/breakthrough").then(setBreakthrough).catch((e) => setError(String(e)));
              if (t.id === "hr")
                void apiGet("/calc/architecture-hr").then(setHrArch).catch((e) => setError(String(e)));
              if (t.id === "deva")
                void apiGet("/calc/deva?rpm=8500&mode=wot").then(setDeva).catch((e) => setError(String(e)));
              if (t.id === "h2")
                void apiGet(`/calc/h2?lambda=${h2Lambda}&water_ratio=${h2Water}`)
                  .then(setH2)
                  .catch((e) => setError(String(e)));
              if (t.id === "bom")
                void apiGet("/calc/bom?with_chassis=true").then(setBom).catch((e) => setError(String(e)));
              if (t.id === "cvt")
                void apiGet("/calc/cvt-compare?shaft_kw=100").then(setCvt).catch((e) => setError(String(e)));
              if (t.id === "axiom")
                void apiGet("/calc/axiom").then(setAxiomPack).catch((e) => setError(String(e)));
              if (t.id === "nexus")
                void apiGet("/calc/nexus?rpm=8500&mode=wot").then(setNexus).catch((e) => setError(String(e)));
              if (t.id === "ops")
                void apiGet("/calc/ops").then(setOps).catch((e) => setError(String(e)));
              if (t.id === "control")
                void apiGet("/calc/control").then(setControl).catch((e) => setError(String(e)));
              if (t.id === "platform")
                void apiGet("/calc/platform?domain=all").then(setPlatform).catch((e) => setError(String(e)));
              if (t.id === "mfg")
                void apiGet("/calc/manufacturing").then(setMfg).catch((e) => setError(String(e)));
              if (t.id === "addons")
                void apiGet("/calc/addons").then(setAddons).catch((e) => setError(String(e)));
              if (t.id === "validate")
                void apiGet("/calc/validate").then(setValidation).catch((e) => setError(String(e)));
            }}
          >
            {t.label}
          </button>
        ))}
        <button type="button" className="btn" onClick={() => void loadBaseline()}>
          Reload Baseline
        </button>
      </div>

      {error ? (
        <div className="panel border-[var(--danger)] px-4 py-3 text-sm text-[var(--danger)]">
          {error}
        </div>
      ) : null}

      {tab === "wot" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">V8 WOT Air / Fuel</h2>
          <div className="grid gap-4 md:grid-cols-3">
            <label className="block text-sm">
              <span className="panel-title">RPM</span>
              <input className="slider mt-2" type="range" min={2000} max={9000} step={50} value={rpm} onChange={(e) => setRpm(Number(e.target.value))} />
              <div className="data-value mt-1 text-sm">{rpm}</div>
            </label>
            <label className="block text-sm">
              <span className="panel-title">AFR</span>
              <input className="slider mt-2" type="range" min={12} max={35} step={0.1} value={afr} onChange={(e) => setAfr(Number(e.target.value))} />
              <div className="data-value mt-1 text-sm">{afr.toFixed(1)}:1</div>
            </label>
            <label className="block text-sm">
              <span className="panel-title">ηv</span>
              <input className="slider mt-2" type="range" min={0.85} max={1.15} step={0.01} value={etaV} onChange={(e) => setEtaV(Number(e.target.value))} />
              <div className="data-value mt-1 text-sm">{etaV.toFixed(2)}</div>
            </label>
          </div>
          <p className="text-xs text-[var(--steel)]">Live recompute on drag · full coupled lab at /lab</p>
          {airFuel ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              <Metric label="m_dot air" value={fmt(airFuel.m_dot_air_kg_s, 4)} unit="kg/s" />
              <Metric label="m_dot fuel" value={fmt(airFuel.m_dot_fuel_g_s, 2)} unit="g/s" />
              <Metric label="Per injector" value={fmt(airFuel.m_dot_per_injector_g_s, 3)} unit="g/s" />
              <Metric label="mg / stroke" value={fmt(airFuel.mg_per_stroke, 2)} unit="mg" />
              <Metric label="E_in" value={fmt(airFuel.e_in_kw, 1)} unit="kW" />
              <Metric label="Liquid equiv." value={fmt(airFuel.liquid_equiv_L_h, 1)} unit="L/h" />
            </div>
          ) : null}
        </section>
      )}

      {tab === "hex" && hex && (
        <section className="panel space-y-5 p-5">
          <button type="button" className="btn" onClick={() => void fetchHex().then(setHex)}>Refresh</button>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <Metric label="Q_HEX" value={fmt(hex.q_hex_kw, 2)} unit="kW" />
            <Metric label="Exhaust energy" value={fmt(hex.exhaust_energy_kw, 1)} unit="kW" />
            <Metric label="Recovery" value={fmt(hex.exhaust_recovery_ratio * 100, 2)} unit="%" />
          </div>
        </section>
      )}

      {tab === "orifice" && hem && piezo && (
        <section className="panel space-y-5 p-5">
          <button
            type="button"
            className="btn"
            onClick={() =>
              void Promise.all([fetchHem(), fetchPiezo()]).then(([h, p]) => {
                setHem(h);
                setPiezo(p);
              })
            }
          >
            Refresh
          </button>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <Metric label="P2/P1" value={fmt(hem.pressure_ratio, 3)} />
            <Metric label="sigma_c" value={fmt(hem.sigma_c, 3)} />
            <Metric label="A_o required" value={fmt(hem.a_o_required_mm2, 3)} unit="mm2" />
            <Metric label="A_o max" value={fmt(piezo.a_o_mm2, 3)} unit="mm2" />
            <Metric label="dz max" value={fmt(piezo.delta_z_um, 1)} unit="um" />
          </div>
        </section>
      )}

      {tab === "driver" && driver && (
        <section className="panel space-y-5 p-5">
          <button type="button" className="btn" onClick={() => void fetchDriver().then(setDriver)}>Refresh</button>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <Metric label="E_c" value={fmt(driver.e_c_mj, 4)} unit="mJ" />
            <Metric label="P_raw" value={fmt(driver.p_raw_w, 2)} unit="W" />
            <Metric label="L_r" value={fmt(driver.l_r_uh, 2)} unit="uH" />
            <Metric label="I_peak" value={fmt(driver.i_peak_a, 2)} unit="A" />
          </div>
        </section>
      )}

      {tab === "chassis" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">Monocoque Torsion / Bending</h2>
          {chassis ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <Metric label="T_twist" value={fmt(Number(chassis.t_twist_nm), 1)} unit="Nm" />
              <Metric label="K_theta design" value={fmt(Number(chassis.k_theta_design_nm_per_deg), 0)} unit="Nm/deg" />
              <Metric label="M_b max" value={fmt(Number(chassis.m_b_max_nm), 0)} unit="Nm" />
              <Metric label="Min node SF" value={fmt(Number(chassis.min_node_sf), 2)} />
            </div>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load chassis results.</p>
          )}
        </section>
      )}

      {tab === "hert" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">HERT Turbine + GDSA + Gear Map</h2>
          {cold && ceb ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              <Metric label="Cold kW" value={fmt(cold.power_kw, 2)} unit="kW" />
              <Metric label="Cold hp" value={fmt(cold.power_hp, 1)} unit="hp" />
              <Metric label="CEB kW" value={fmt(ceb.power_kw, 2)} unit="kW" />
              <Metric label="CEB hp" value={fmt(ceb.power_hp, 1)} unit="hp" />
            </div>
          ) : null}
          {gdsa ? (
            <div className="grid gap-3 sm:grid-cols-3">
              <Metric label="GDSA force" value={fmt(Number(gdsa.peak_force_n), 0)} unit="N" />
              <Metric label="Shift time" value={fmt(Number(gdsa.total_shift_time_ms), 1)} unit="ms" />
              <Metric label="Piston area" value={fmt(Number(gdsa.piston_area_cm2), 2)} unit="cm2" />
            </div>
          ) : null}
          {shiftSteps.length > 0 ? (
            <table className="w-full text-left font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--steel)]">
              <thead>
                <tr className="text-[var(--amber)]">
                  <th className="py-2">Shift</th>
                  <th>RPM drop</th>
                </tr>
              </thead>
              <tbody>
                {shiftSteps.map((s) => (
                  <tr key={`${s.frm}-${s.to}`} className="border-t border-[var(--line)]">
                    <td className="py-1">
                      {s.frm} to {s.to}
                    </td>
                    <td className="data-value">{fmt(s.rpm_drop, 0)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load HERT results.</p>
          )}
        </section>
      )}

      {tab === "breakthrough" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">Beyond-Horizon Features</h2>
          <p className="text-sm text-[var(--muted)]">
            CCD, CASMIR, PSI, DKIS-TFF, Dual-Rail, Orbital Water — docs/breakthrough-features.md
          </p>
          {ccd && dkis ? (
            <div className="grid gap-3 sm:grid-cols-3">
              <Metric label="CCD density gain" value={fmt(ccd.density_gain_pct, 1)} unit="%" />
              <Metric label="Cold sink" value={fmt(ccd.t_cold_sink_c, 1)} unit="C" />
              <Metric label="DKIS Ktheta/Kphi" value={fmt(dkis.coupling_ratio, 1)} />
            </div>
          ) : null}
          {Array.isArray(breakthrough?.features_catalog) ? (
            <ul className="grid gap-2 sm:grid-cols-3">
              {(breakthrough.features_catalog as string[]).map((f) => (
                <li
                  key={f}
                  className="border border-[var(--line)] px-3 py-2 font-[family-name:var(--font-ibm-mono)] text-xs tracking-wider text-[var(--amber)]"
                >
                  {f}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load breakthrough results.</p>
          )}
        </section>
      )}

      {tab === "hr" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">SVIE-V8-HR Architecture (Honda-Evolved H2 DI)</h2>
          {hrArch ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <Metric label="Displacement" value={fmt(Number(hrArch.displacement_cc), 1)} unit="cc" />
              <Metric label="Rod/Stroke" value={fmt(Number(hrArch.rod_to_stroke), 3)} />
              <Metric label="MPS @ redline" value={fmt(Number(hrArch.mean_piston_speed_m_s), 1)} unit="m/s" />
              <Metric label="Side-load cut" value={fmt(Number(hrArch.side_load_reduction_pct), 1)} unit="%" />
              <Metric label="vs B16 ratio" value={fmt(Number(hrArch.side_load_reduction_pct_vs_b16), 1)} unit="%" />
              <Metric label="PTWA save" value={fmt(Number(hrArch.ptwa_weight_save_lb), 0)} unit="lb" />
              <Metric label="CR" value={fmt(Number(hrArch.compression_ratio), 1)} />
            </div>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load V8-HR results.</p>
          )}
        </section>
      )}

      {tab === "deva" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">DEVA Electrical Power</h2>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              className="btn"
              onClick={() =>
                void apiGet("/calc/deva?rpm=8500&mode=wot").then(setDeva).catch((e) => setError(String(e)))
              }
            >
              8500 WOT
            </button>
            <button
              type="button"
              className="btn"
              onClick={() =>
                void apiGet("/calc/deva?rpm=3000&mode=cruise")
                  .then(setDeva)
                  .catch((e) => setError(String(e)))
              }
            >
              3000 Cruise
            </button>
          </div>
          {deva ? (
            <div className="grid gap-3 sm:grid-cols-3">
              <Metric label="Mode" value={String(deva.mode)} />
              <Metric label="Transition kW" value={fmt(Number(deva.transition_power_kw), 2)} unit="kW" />
              <Metric label="Total electrical" value={fmt(Number(deva.total_electrical_kw), 2)} unit="kW" />
            </div>
          ) : null}
        </section>
      )}

      {tab === "h2" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">H2 Lambda / Water DI</h2>
          <div className="grid gap-4 md:grid-cols-2">
            <label className="block text-sm">
              <span className="panel-title">Lambda</span>
              <input
                className="slider mt-2"
                type="range"
                min={0.8}
                max={3.5}
                step={0.05}
                value={h2Lambda}
                onChange={(e) => setH2Lambda(Number(e.target.value))}
              />
              <div className="data-value mt-1 text-sm">{h2Lambda.toFixed(2)}</div>
            </label>
            <label className="block text-sm">
              <span className="panel-title">Water/Fuel mass ratio</span>
              <input
                className="slider mt-2"
                type="range"
                min={0}
                max={0.4}
                step={0.01}
                value={h2Water}
                onChange={(e) => setH2Water(Number(e.target.value))}
              />
              <div className="data-value mt-1 text-sm">{h2Water.toFixed(2)}</div>
            </label>
          </div>
          <button
            type="button"
            className="btn"
            onClick={() =>
              void apiGet(`/calc/h2?lambda=${h2Lambda}&water_ratio=${h2Water}`)
                .then(setH2)
                .catch((e) => setError(String(e)))
            }
          >
            Recompute
          </button>
          {h2 ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <Metric label="AFR" value={fmt(Number(h2.afr_mass), 2)} />
              <Metric label="NOx index" value={fmt(Number(h2.nox_index), 3)} />
              <Metric label="NOx cut" value={fmt(Number(h2.nox_reduction_pct), 1)} unit="%" />
              <Metric label="After water" value={fmt(Number(h2.nox_index_after_water), 3)} />
              <Metric label="Load extension" value={fmt(Number(h2.load_extension_pct), 1)} unit="%" />
              <Metric label="PI strategy" value="boost+late DI" />
            </div>
          ) : null}
        </section>
      )}

      {tab === "bom" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">BOM Cost Envelope (USD)</h2>
          {bom ? (
            <div className="grid gap-3 sm:grid-cols-2">
              <Metric
                label="Powertrain subtotal"
                value={fmt(Number(bom.powertrain_subtotal_usd), 0)}
                unit="USD"
              />
              <Metric label="With chassis share" value={fmt(Number(bom.total_usd), 0)} unit="USD" />
            </div>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load BOM.</p>
          )}
          <p className="text-xs text-[var(--muted)]">Diligence envelope only — not a supplier quote.</p>
        </section>
      )}

      {tab === "cvt" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">CVT vs AXIOM/HERT @ 100 kW</h2>
          <p className="text-sm text-[var(--muted)]">
            Evidence: ICCT + CVT slip literature + Honda HR-V belt TSB. See docs/cvt-evidence-dossier.md
          </p>
          {cvt ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <Metric label="CVT eta" value={fmt(Number(cvt.cvt_eta), 3)} />
              <Metric label="HERT eta" value={fmt(Number(cvt.hert_eta), 3)} />
              <Metric label="Delta out" value={fmt(Number(cvt.delta_out_kw), 1)} unit="kW" />
              <Metric label="CVT parasitics" value={fmt(Number(cvt.cvt_parasitic_kw), 1)} unit="kW" />
              <Metric label="HERT parasitics" value={fmt(Number(cvt.hert_parasitic_kw), 1)} unit="kW" />
              <Metric label="TQ ceiling edge" value={fmt(Number(cvt.torque_ceiling_advantage_nm), 0)} unit="Nm" />
            </div>
          ) : null}
        </section>
      )}

      {tab === "axiom" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">AXIOM + e:HEV Bridge</h2>
          {axiomPack && axiomPack.axiom && axiomPack.bridge ? (
            <>
              <div className="grid gap-3 sm:grid-cols-3">
                <Metric
                  label="AXIOM eta"
                  value={fmt(Number((axiomPack.axiom as Record<string, number>).mech_efficiency), 3)}
                />
                <Metric
                  label="Shift"
                  value={fmt(Number((axiomPack.axiom as Record<string, number>).shift_ms), 1)}
                  unit="ms"
                />
                <Metric
                  label="Rubber-band"
                  value={fmt(Number((axiomPack.axiom as Record<string, number>).rubber_band_index), 0)}
                />
              </div>
              <p className="text-sm text-[var(--muted)]">
                Bridge removes belt/eCVT · engine-direct eta{" "}
                <span className="data-value">
                  {fmt(Number((axiomPack.bridge as Record<string, number>).engine_direct_eta), 3)}
                </span>
              </p>
            </>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load AXIOM.</p>
          )}
        </section>
      )}

      {tab === "nexus" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">NEXUS-48 vs DEVA Draw</h2>
          {nexus ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <Metric label="DEVA" value={fmt(Number(nexus.deva_kw), 2)} unit="kW" />
              <Metric label="Total draw" value={fmt(Number(nexus.total_draw_kw), 2)} unit="kW" />
              <Metric label="BSG avail" value={fmt(Number(nexus.bsg_available_kw), 1)} unit="kW" />
              <Metric label="Margin" value={fmt(Number(nexus.margin_kw), 2)} unit="kW" />
              <Metric label="Feeds OK" value={nexus.feeds_ok ? "YES" : "NO"} />
            </div>
          ) : null}
        </section>
      )}

      {tab === "ops" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">CHRONOS / SENTINEL / TRL</h2>
          {ops && ops.chronos && ops.sentinel && ops.trl ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <Metric
                label="First fire"
                value={fmt(Number((ops.chronos as Record<string, number>).time_to_first_fire_s), 1)}
                unit="s"
              />
              <Metric
                label="AFT active"
                value={fmt(
                  Number((ops.chronos as Record<string, number>).time_to_aftertreatment_active_s),
                  1,
                )}
                unit="s"
              />
              <Metric
                label="H2 isolation"
                value={fmt(Number((ops.sentinel as Record<string, number>).isolation_ms), 0)}
                unit="ms"
              />
              <Metric
                label="Sensors"
                value={fmt(Number((ops.sentinel as Record<string, number>).sensors_total), 0)}
              />
              <Metric
                label="Current TRL"
                value={fmt(Number((ops.trl as Record<string, number>).current_trl), 0)}
              />
            </div>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load ops pack.</p>
          )}
        </section>
      )}

      {tab === "control" && (
        <section className="panel space-y-5 p-5">
          <h2 className="panel-title">BLEND / MIRAGE / VECTOR</h2>
          {control && control.blend && control.mirage && control.vector ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <Metric
                label="Shift hole"
                value={fmt(Number((control.blend as Record<string, number>).shift_ms), 1)}
                unit="ms"
              />
              <Metric
                label="vs AMT hole"
                value={fmt(Number((control.blend as Record<string, number>).hole_reduction_factor), 0)}
                unit="x"
              />
              <Metric
                label="Brake fill F"
                value={fmt(Number((control.blend as Record<string, number>).target_brake_force_n), 0)}
                unit="N"
              />
              <Metric
                label="MIRAGE nodes"
                value={fmt(Number((control.mirage as Record<string, number>).node_count), 0)}
              />
              <Metric
                label="VECTOR domains"
                value={fmt(Number((control.vector as Record<string, number>).domain_count), 0)}
              />
              <Metric
                label="HCP cycle"
                value={fmt(Number((control.vector as Record<string, number>).cycle_ms), 1)}
                unit="ms"
              />
            </div>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load control pack.</p>
          )}
        </section>
      )}

      {tab === "platform" && (
        <section className="panel space-y-4 p-5">
          <h2 className="panel-title">Platform+ Engine · Trans · Body</h2>
          {platform && platform.engine ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              <Metric
                label="CRYO ΔT"
                value={fmt(
                  Number(
                    ((platform.engine as Record<string, Record<string, number>>).cryo_rail || {})
                      .delta_t_k,
                  ),
                  1,
                )}
                unit="K"
              />
              <Metric
                label="RING FMEP Δ"
                value={fmt(
                  Number(
                    ((platform.engine as Record<string, Record<string, number>>).ring_zero || {})
                      .fmep_delta_frac,
                  ) * 100,
                  1,
                )}
                unit="%"
              />
              <Metric
                label="FLUX interrupt"
                value={fmt(
                  Number(
                    (
                      (platform.transmission as Record<string, Record<string, number>>)
                        .flux_shift || {}
                    ).interrupt_ms,
                  ),
                  1,
                )}
                unit="ms"
              />
              <Metric
                label="NODE torsion"
                value={fmt(
                  Number(
                    ((platform.body as Record<string, Record<string, number>>).node_cast || {})
                      .torsion_nm_per_deg,
                  ),
                  0,
                )}
                unit="Nm/deg"
              />
            </div>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load platform pack.</p>
          )}
        </section>
      )}

      {tab === "mfg" && (
        <section className="panel space-y-4 p-5">
          <h2 className="panel-title">Manufacturing Master</h2>
          {mfg ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              <Metric label="Annual units" value={fmt(Number(mfg.annual_units), 0)} />
              <Metric label="PTWA" value={fmt(Number(mfg.ptwa_mm), 2)} unit="mm" />
              <Metric label="Routes" value={fmt(Number(mfg.route_count), 0)} />
              <Metric label="Cells" value={fmt(Number(mfg.cell_count), 0)} />
            </div>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load manufacturing rollup.</p>
          )}
        </section>
      )}

      {tab === "addons" && (
        <section className="panel space-y-4 p-5">
          <h2 className="panel-title">Add-ons · 1.4.0</h2>
          {addons ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              <Metric
                label="DRY-SUMP flow"
                value={fmt(
                  Number((addons.dry_sump_x as Record<string, number>)?.flow_l_min),
                  0,
                )}
                unit="L/min"
              />
              <Metric
                label="EGR NOx Δ"
                value={fmt(
                  Number((addons.pulse_egr as Record<string, number>)?.nox_reduction_frac) *
                    100,
                  0,
                )}
                unit="%"
              />
              <Metric
                label="SILK gain"
                value={fmt(
                  Number((addons.silk_mount as Record<string, number>)?.isolation_gain_db),
                  0,
                )}
                unit="dB"
              />
              <Metric
                label="RANGE DC bus"
                value={fmt(
                  Number((addons.range_bridge as Record<string, number>)?.dc_bus_kw),
                  1,
                )}
                unit="kW"
              />
            </div>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to load add-ons.</p>
          )}
        </section>
      )}

      {tab === "validate" && (
        <section className="panel space-y-4 p-5">
          <h2 className="panel-title">Cross-spec validation</h2>
          {validation ? (
            <>
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                <Metric
                  label="Passed"
                  value={`${validation.passed}/${validation.total}`}
                />
                <Metric
                  label="Status"
                  value={validation.all_ok ? "ALL OK" : "FAIL"}
                />
                <Metric label="Harness" value="1.4.0" />
              </div>
              <p className="text-sm text-[var(--muted)]">
                Mirrors <code className="text-[var(--amber)]">python -m svie_physics.validate</code>.
                See docs/validation-report.md for literature grounding.
              </p>
            </>
          ) : (
            <p className="text-sm text-[var(--muted)]">Open this tab to run validation.</p>
          )}
        </section>
      )}

      {bundle ? (
        <p className="font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--steel)]">
          Baseline loaded · {API_BASE}
        </p>
      ) : null}
    </div>
  );
}
