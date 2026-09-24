import { Calculators } from "@/components/Calculators";

export default function CalculatorsPage() {
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight">Engineering Calculators</h1>
        <p className="mt-2 max-w-2xl text-[var(--muted)]">
          Thin UI over the SVIE physics API. Results must match CLI outputs for
          identical inputs.
        </p>
      </header>
      <Calculators />
    </div>
  );
}
