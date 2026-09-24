"use client";

import { useEffect, useState } from "react";

const API =
  process.env.NEXT_PUBLIC_SVIE_API_URL?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

export function ApiStatus() {
  const [state, setState] = useState<"checking" | "live" | "offline">("checking");
  const [version, setVersion] = useState<string>("");

  useEffect(() => {
    let cancelled = false;
    const ping = async () => {
      try {
        const res = await fetch(`${API}/health`, { cache: "no-store" });
        if (!res.ok) throw new Error("bad");
        const data = (await res.json()) as { version?: string };
        if (!cancelled) {
          setState("live");
          setVersion(data.version ?? "");
        }
      } catch {
        if (!cancelled) setState("offline");
      }
    };
    void ping();
    const id = window.setInterval(ping, 15000);
    return () => {
      cancelled = true;
      window.clearInterval(id);
    };
  }, []);

  const color =
    state === "live"
      ? "var(--ok)"
      : state === "offline"
        ? "var(--danger)"
        : "var(--steel)";

  return (
    <div
      className="flex items-center gap-2 font-[family-name:var(--font-ibm-mono)] text-[10px] tracking-wider uppercase"
      title={
        state === "live"
          ? `Physics API ${version} at ${API}`
          : `Start API: npm run dev:api (${API})`
      }
    >
      <span
        className="inline-block h-1.5 w-1.5 rounded-full"
        style={{ background: color, boxShadow: `0 0 8px ${color}` }}
      />
      <span style={{ color }}>
        {state === "checking" && "API…"}
        {state === "live" && `API live${version ? ` ${version}` : ""}`}
        {state === "offline" && "API offline"}
      </span>
    </div>
  );
}
