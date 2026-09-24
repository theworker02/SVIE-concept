"use client";

type MetricProps = {
  label: string;
  value: string;
  unit?: string;
};

export function Metric({ label, value, unit }: MetricProps) {
  return (
    <div className="border border-[var(--line)] bg-[rgba(0,0,0,0.2)] px-3 py-3">
      <div className="panel-title">{label}</div>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="data-value text-xl">{value}</span>
        {unit ? (
          <span className="font-[family-name:var(--font-ibm-mono)] text-xs text-[var(--muted)]">
            {unit}
          </span>
        ) : null}
      </div>
    </div>
  );
}

export function fmt(n: number, digits = 3): string {
  if (!Number.isFinite(n)) return "—";
  return n.toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: 0,
  });
}
