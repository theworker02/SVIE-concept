"use client";

import { useEffect, useMemo, useState } from "react";
import { computePoint, computeSweep, type LabPoint } from "@/lib/physicsLab";

function Sparkline({
  series,
  accessor,
  color = "var(--amber)",
  label,
}: {
  series: LabPoint[];
  accessor: (p: LabPoint) => number;
  color?: string;
  label: string;
}) {
  const w = 320;
  const h = 96;
  const pad = 8;
  const values = series.map(accessor);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  const pts = series
    .map((_, i) => {
      const x = pad + (i / (series.length - 1)) * (w - pad * 2);
      const y = h - pad - ((values[i] - min) / span) * (h - pad * 2);
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <div className="border border-[var(--line)] bg-[var(--bg)] p-3">
      <div className="flex items-baseline justify-between">
        <span className="text-[10px] uppercase tracking-wider text-[var(--steel)]">{label}</span>
        <span className="data-value text-sm">{values[values.length - 1]?.toFixed(1)}</span>
      </div>
      <svg viewBox={`0 0 ${w} ${h}`} className="mt-2 h-24 w-full" role="img" aria-label={label}>
        <polyline fill="none" stroke={color} strokeWidth="2" points={pts} />
        <line x1={pad} x2={w - pad} y1={h - pad} y2={h - pad} stroke="var(--line)" strokeWidth="1" />
      </svg>
      <div className="mt-1 flex justify-between font-[family-name:var(--font-ibm-mono)] text-[9px] text-[var(--steel)]">
        <span>{series[0]?.rpm.toFixed(0)} rpm</span>
        <span>{series[series.length - 1]?.rpm.toFixed(0)} rpm</span>
      </div>
    </div>
  );
}

function Gauge({
  label,
  value,
  unit,
  warn,
}: {
  label: string;
  value: string;
  unit?: string;
  warn?: boolean;
}) {
  return (
    <div className="border border-[var(--line)] px-3 py-3" style={{ borderColor: warn ? "var(--danger)" : undefined }}>
      <div className="text-[10px] uppercase tracking-wider text-[var(--steel)]">{label}</div>
      <div className="data-value mt-1 text-xl" style={{ color: warn ? "var(--danger)" : undefined }}>
        {value}
        {unit ? <span className="ml-1 text-xs text-[var(--steel)]">{unit}</span> : null}
      </div>
    </div>
  );
}

function Slider({
  label,
  value,
  min,
  max,
  step,
  unit,
  onChange,
  digits = 0,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  unit: string;
  onChange: (n: number) => void;
  digits?: number;
}) {
  return (
    <label className="block">
      <span className="text-[10px] uppercase tracking-wider text-[var(--steel)]">{label}</span>
      <input
        className="slider mt-2"
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
      <div className="data-value mt-1 text-sm">
        {digits ? value.toFixed(digits) : value}
        {unit ? ` ${unit}` : ""}
      </div>
    </label>
  );
}

export function PhysicsLab() {
  const [rpm, setRpm] = useState(8500);
  const [afr, setAfr] = useState(16.2);
  const [load, setLoad] = useState(1);
  const [tempC, setTempC] = useState(25);
  const [pressure, setPressure] = useState(101.3);
  const [boost, setBoost] = useState(0);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    if (!playing) return;
    let current = 2000;
    const id = window.setInterval(() => {
      current += 150;
      if (current > 9000) current = 2000;
      setRpm(current);
    }, 100);
    return () => window.clearInterval(id);
  }, [playing]);

  const base = useMemo(
    () => ({ afr, load, tempC, pressureKpa: pressure, boostKpa: boost }),
    [afr, load, tempC, pressure, boost],
  );
  const point = useMemo(() => computePoint({ ...base, rpm }), [base, rpm]);
  const sweep = useMemo(() => computeSweep(base, 1500, 9000, 48), [base]);

  return (
    <div className="space-y-8">
      <header>
        <p className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-[0.35em] text-[var(--amber)]">
          PHYSICS LAB · LIVE · CLIENT-SIDE MAPS
        </p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
          Runnable physics you can drive
        </h1>
        <p className="mt-3 max-w-2xl text-[var(--muted)]">
          Coupled air/fuel, RPM-dependent volumetric efficiency, BTE map, brake
          torque/power, SFV HEX duty, and injector pulse — updates instantly as
          you move the controls. Works offline on GitHub Pages.
        </p>
      </header>

      <section
        className="panel p-5 md:p-7"
        style={{
          background: "linear-gradient(165deg, #1a222c 0%, #12161c 55%, #1a1814 100%)",
        }}
      >
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="panel-title">Live operating point</p>
            <div className="data-value mt-2 text-4xl md:text-5xl">
              {point.brake_power_hp}
              <span className="ml-2 text-lg text-[var(--steel)]">hp</span>
            </div>
            <p className="mt-1 text-sm text-[var(--muted)]">
              {point.brake_power_kw.toFixed(1)} kW · {point.torque_nm.toFixed(0)} N·m · BTE{" "}
              {(point.bte * 100).toFixed(1)}% · {rpm} rpm
            </p>
          </div>
          <button type="button" className="btn" onClick={() => setPlaying((p) => !p)}>
            {playing ? "Stop RPM tour" : "Play RPM tour"}
          </button>
        </div>

        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Gauge label="Fuel flow" value={point.m_dot_fuel_g_s.toFixed(2)} unit="g/s" />
          <Gauge label="Air flow" value={point.m_dot_air_kg_s.toFixed(3)} unit="kg/s" />
          <Gauge label="HEX duty" value={point.q_hex_kw.toFixed(1)} unit="kW" />
          <Gauge
            label="Injector duty"
            value={(point.injector_duty * 100).toFixed(0)}
            unit="%"
            warn={point.injector_duty > 0.8}
          />
          <Gauge label="ηv map" value={point.eta_v.toFixed(3)} />
          <Gauge label="ρ air" value={point.air_density_kg_m3.toFixed(3)} unit="kg/m³" />
          <Gauge label="mg / stroke" value={point.mg_per_stroke.toFixed(1)} unit="mg" />
          <Gauge label="Pulse width" value={point.injector_pw_ms.toFixed(2)} unit="ms" />
        </div>
      </section>

      <section className="panel space-y-5 p-5">
        <h2 className="panel-title">Controls — drag for live recompute</h2>
        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          <Slider label="Engine speed" value={rpm} min={1500} max={9000} step={50} unit="rpm" onChange={setRpm} />
          <Slider label="AFR" value={afr} min={12} max={22} step={0.1} unit=":1" onChange={setAfr} digits={1} />
          <Slider label="Load" value={load} min={0.2} max={1} step={0.01} unit="" onChange={setLoad} digits={2} />
          <Slider label="Ambient temp" value={tempC} min={-20} max={50} step={1} unit="°C" onChange={setTempC} />
          <Slider
            label="Ambient pressure"
            value={pressure}
            min={70}
            max={105}
            step={0.1}
            unit="kPa"
            onChange={setPressure}
            digits={1}
          />
          <Slider label="Boost (MAP add)" value={boost} min={0} max={120} step={1} unit="kPa" onChange={setBoost} />
        </div>
        <div className="flex flex-wrap gap-2">
          {(
            [
              { label: "WOT design", rpm: 8500, afr: 16.2, load: 1, boost: 0, temp: 25, p: 101.3 },
              { label: "Cruise", rpm: 2800, afr: 18, load: 0.35, boost: 0, temp: 25, p: 101.3 },
              { label: "Boosted", rpm: 7000, afr: 15.5, load: 1, boost: 80, temp: 25, p: 101.3 },
              { label: "Cold dense", rpm: 8500, afr: 16.2, load: 1, boost: 0, temp: -10, p: 102 },
            ] as const
          ).map((preset) => (
            <button
              key={preset.label}
              type="button"
              className="btn"
              style={{ opacity: 0.85 }}
              onClick={() => {
                setPlaying(false);
                setRpm(preset.rpm);
                setAfr(preset.afr);
                setLoad(preset.load);
                setBoost(preset.boost);
                setTempC(preset.temp);
                setPressure(preset.p);
              }}
            >
              {preset.label}
            </button>
          ))}
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <Sparkline series={sweep} accessor={(p) => p.brake_power_kw} label="Brake power vs RPM (kW)" />
        <Sparkline
          series={sweep}
          accessor={(p) => p.torque_nm}
          label="Torque vs RPM (N·m)"
          color="var(--steel)"
        />
        <Sparkline series={sweep} accessor={(p) => p.m_dot_fuel_g_s} label="Fuel flow vs RPM (g/s)" />
      </section>

      <section className="panel p-5 text-sm text-[var(--muted)]">
        <h2 className="panel-title">Model notes (honest)</h2>
        <ul className="mt-3 list-disc space-y-1 pl-5">
          <li>ηv is a design intake-tuning map peaked at 8500 rpm — not dyno-measured.</li>
          <li>BTE uses the locked 42% WOT anchor and soft AFR/load derates.</li>
          <li>HEX uses SFV enthalpy rise (~820 kJ/kg); recovery vs 30% exhaust share.</li>
          <li>Injector PW is a calibrated timing proxy for duty-horizon checks.</li>
          <li>
            CLI:{" "}
            <code className="text-[var(--amber)]">
              python -m svie_physics.physics_lab --rpm {rpm} --afr {afr}
            </code>
          </li>
        </ul>
      </section>
    </div>
  );
}
