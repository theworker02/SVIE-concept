"use client";

import Image from "next/image";
import { useState } from "react";

type Mode = "analog" | "ultra";

export function AetherOsMock() {
  const [mode, setMode] = useState<Mode>("analog");
  const [temp, setTemp] = useState(22);
  const [fan, setFan] = useState(2);
  const [drive, setDrive] = useState("Tour");
  const [coverOpen, setCoverOpen] = useState(false);
  const [rpm, setRpm] = useState(32);
  const [speed, setSpeed] = useState(45);

  return (
    <div className="space-y-10">
      <header>
        <p className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-[0.35em] text-[var(--amber)]">
          AETHER-OS · v1.3.0 · ANALOG-FIRST
        </p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
          Luxury you feel with your hands
        </h1>
        <p className="mt-4 max-w-2xl text-base leading-relaxed text-[var(--muted)]">
          One guest glass for Apple CarPlay Ultra. Everything that matters —
          climate, volume, drive mode, fuel path — is milled metal, needles, and
          jewels. Hardware is truth; Ultra is a guest.
        </p>
      </header>

      <div className="flex flex-wrap gap-3">
        <button
          type="button"
          className="btn"
          style={{ opacity: mode === "analog" ? 1 : 0.55 }}
          onClick={() => {
            setMode("analog");
            setCoverOpen(false);
          }}
        >
          Pure analog
        </button>
        <button
          type="button"
          className="btn"
          style={{ opacity: mode === "ultra" ? 1 : 0.55 }}
          onClick={() => {
            setMode("ultra");
            setCoverOpen(true);
          }}
        >
          CarPlay Ultra guest
        </button>
        <button
          type="button"
          className="btn"
          style={{ opacity: 0.75 }}
          onClick={() => setCoverOpen((v) => !v)}
        >
          {coverOpen ? "Close glass cover" : "Open glass cover"}
        </button>
      </div>

      {/* Cluster + stack mock */}
      <section
        className="panel relative overflow-hidden p-6 md:p-8"
        style={{
          background:
            "linear-gradient(165deg, #1a1f27 0%, #12151a 50%, #1a1814 100%)",
        }}
      >
        <div className="grid gap-8 lg:grid-cols-[1fr_1.1fr_1fr]">
          {/* Speedo */}
          <div className="flex flex-col items-center">
            <div
              className="relative flex h-40 w-40 items-center justify-center rounded-full border-2 border-[var(--line)]"
              style={{
                background:
                  "radial-gradient(circle at 40% 35%, #2a3038 0%, #12151a 70%)",
                boxShadow: "inset 0 0 40px rgba(0,0,0,0.6)",
              }}
            >
              <div
                className="absolute h-[2px] w-14 origin-right bg-[var(--amber)]"
                style={{
                  transform: `rotate(${-120 + speed * 2.4}deg) translateX(-50%)`,
                  left: "50%",
                  top: "50%",
                }}
              />
              <div className="text-center">
                <div className="data-value text-3xl">{speed}</div>
                <div className="text-[10px] uppercase tracking-widest text-[var(--steel)]">
                  mph
                </div>
              </div>
            </div>
            <p className="mt-3 font-[family-name:var(--font-ibm-mono)] text-[10px] tracking-wider text-[var(--steel)]">
              ANALOG SPEED
            </p>
          </div>

          {/* Center glass / cover */}
          <div className="flex flex-col items-center justify-center">
            <div
              className="relative w-full max-w-sm overflow-hidden border border-[var(--line)]"
              style={{ aspectRatio: "16/10" }}
            >
              {!coverOpen ? (
                <div className="flex h-full flex-col items-center justify-center bg-[linear-gradient(180deg,#3a4554_0%,#2a3038_100%)]">
                  <div className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-[0.4em] text-[var(--ink)]">
                    SVIE
                  </div>
                  <div className="mt-2 text-[10px] tracking-widest text-[var(--steel)]">
                    GLASS STOWED
                  </div>
                </div>
              ) : mode === "ultra" ? (
                <div className="flex h-full flex-col bg-[#12151a] p-4">
                  <div className="flex items-center justify-between">
                    <span className="font-[family-name:var(--font-ibm-mono)] text-[10px] tracking-wider text-[var(--amber)]">
                      CARPLAY ULTRA · GUEST
                    </span>
                    <span className="text-[10px] text-[var(--steel)]">Siri · Maps</span>
                  </div>
                  <div className="mt-4 flex-1 rounded-sm border border-[var(--line)] bg-[rgba(255,255,255,0.03)] p-3">
                    <p className="text-sm text-[var(--ink)]">Now Playing</p>
                    <p className="mt-1 text-xs text-[var(--muted)]">
                      Climate remotes physical dials · dials always win
                    </p>
                    <div className="mt-4 grid grid-cols-3 gap-2 text-center font-[family-name:var(--font-ibm-mono)] text-[10px] text-[var(--steel)]">
                      <div className="border border-[var(--line)] py-2">Nav</div>
                      <div className="border border-[var(--line)] py-2 text-[var(--amber)]">
                        Audio
                      </div>
                      <div className="border border-[var(--line)] py-2">Phone</div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex h-full flex-col items-center justify-center bg-[#12151a]">
                  <div className="data-value text-4xl">
                    {new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                  </div>
                  <div className="mt-2 text-xs text-[var(--steel)]">Native glance · 18°C out</div>
                </div>
              )}
            </div>
            <p className="mt-3 font-[family-name:var(--font-ibm-mono)] text-[10px] tracking-wider text-[var(--steel)]">
              ≤10.25″ GUEST GLASS
            </p>
          </div>

          {/* Tach */}
          <div className="flex flex-col items-center">
            <div
              className="relative flex h-40 w-40 items-center justify-center rounded-full border-2 border-[var(--line)]"
              style={{
                background:
                  "radial-gradient(circle at 40% 35%, #2a3038 0%, #12151a 70%)",
                boxShadow: "inset 0 0 40px rgba(0,0,0,0.6)",
              }}
            >
              <div
                className="absolute h-[2px] w-14 origin-right bg-[var(--amber)]"
                style={{
                  transform: `rotate(${-120 + rpm * 2.4}deg) translateX(-50%)`,
                  left: "50%",
                  top: "50%",
                }}
              />
              <div className="text-center">
                <div className="data-value text-3xl">{(rpm / 10).toFixed(1)}</div>
                <div className="text-[10px] uppercase tracking-widest text-[var(--steel)]">
                  ×1000
                </div>
              </div>
            </div>
            <p className="mt-3 font-[family-name:var(--font-ibm-mono)] text-[10px] tracking-wider text-[var(--steel)]">
              ANALOG TACH
            </p>
          </div>
        </div>

        {/* Physical stack */}
        <div className="mt-10 border-t border-[var(--line)] pt-8">
          <p className="panel-title mb-4">Physical stack — hardware is truth</p>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <label className="block">
              <span className="text-[10px] uppercase tracking-wider text-[var(--steel)]">
                Temp °C
              </span>
              <input
                type="range"
                min={16}
                max={28}
                value={temp}
                onChange={(e) => setTemp(Number(e.target.value))}
                className="slider mt-2"
              />
              <div className="data-value mt-1">{temp}°</div>
            </label>
            <label className="block">
              <span className="text-[10px] uppercase tracking-wider text-[var(--steel)]">
                Fan
              </span>
              <input
                type="range"
                min={0}
                max={6}
                value={fan}
                onChange={(e) => setFan(Number(e.target.value))}
                className="slider mt-2"
              />
              <div className="data-value mt-1">{fan}</div>
            </label>
            <label className="block">
              <span className="text-[10px] uppercase tracking-wider text-[var(--steel)]">
                Drive
              </span>
              <select
                className="mt-2 w-full border border-[var(--line)] bg-[var(--bg)] px-2 py-2 font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--amber)]"
                value={drive}
                onChange={(e) => setDrive(e.target.value)}
              >
                {["Tour", "Sport", "Track", "Series-RE"].map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </label>
            <div>
              <span className="text-[10px] uppercase tracking-wider text-[var(--steel)]">
                Jewels
              </span>
              <div className="mt-3 flex gap-3">
                {["SENT", "OIL", "CHG"].map((j, i) => (
                  <div key={j} className="text-center">
                    <div
                      className="mx-auto h-3 w-3 rounded-full"
                      style={{
                        background: i === 0 ? "var(--amber)" : "var(--line)",
                        boxShadow: i === 0 ? "0 0 8px var(--amber)" : undefined,
                      }}
                    />
                    <div className="mt-1 text-[9px] text-[var(--steel)]">{j}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="mt-6 flex flex-wrap gap-4">
            <label className="flex items-center gap-2 text-xs text-[var(--muted)]">
              Speed demo
              <input
                type="range"
                min={0}
                max={100}
                value={speed}
                onChange={(e) => setSpeed(Number(e.target.value))}
                className="slider w-32"
              />
            </label>
            <label className="flex items-center gap-2 text-xs text-[var(--muted)]">
              RPM demo
              <input
                type="range"
                min={8}
                max={90}
                value={rpm}
                onChange={(e) => setRpm(Number(e.target.value))}
                className="slider w-32"
              />
            </label>
          </div>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-2">
        <article className="panel overflow-hidden">
          <div className="relative aspect-[16/10] bg-[var(--bg)]">
            <Image
              src="/design/svie-hmi-cabin-analog.png"
              alt="Analog-first cabin"
              fill
              className="object-cover"
              sizes="50vw"
            />
          </div>
          <div className="p-4">
            <h2 className="font-medium">Cabin — quiet luxury</h2>
            <p className="mt-1 text-sm text-[var(--muted)]">
              Leather, milled aluminum, one modest glass — not a tablet farm.
            </p>
          </div>
        </article>
        <article className="panel overflow-hidden">
          <div className="relative aspect-[16/10] bg-[var(--bg)]">
            <Image
              src="/design/svie-hmi-analog-stack.png"
              alt="Analog control stack"
              fill
              className="object-cover"
              sizes="50vw"
            />
          </div>
          <div className="p-4">
            <h2 className="font-medium">Stack — watchmaking precision</h2>
            <p className="mt-1 text-sm text-[var(--muted)]">
              Detented rotaries and toggles with amber jewels.
            </p>
          </div>
        </article>
      </section>

      <section className="panel p-5">
        <h2 className="panel-title">Policy</h2>
        <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-[var(--muted)]">
          <li>CarPlay Ultra on center glass (+ optional hybrid cluster aperture only).</li>
          <li>Zero door / mirror / headrest screens.</li>
          <li>Climate, audio, drive mode: physical first; Ultra remotes them.</li>
          <li>Conflict → physical wins. Phone dies → car still drives beautifully.</li>
        </ul>
        <pre className="mt-4 overflow-x-auto border border-[var(--line)] bg-[var(--bg)] p-3 font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--amber)]">
          {`python -m svie_physics.aether_os
# docs/design-system/aether-os.md`}
        </pre>
      </section>
    </div>
  );
}
