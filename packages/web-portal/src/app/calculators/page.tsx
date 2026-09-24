import Link from "next/link";
import { Calculators } from "@/components/Calculators";

export default function CalculatorsPage() {
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight">Engineering Calculators</h1>
        <p className="mt-2 max-w-2xl text-[var(--muted)]">
          Module browsers over the SVIE physics API. For the fully interactive coupled
          lab (live sliders + power/torque curves), open{" "}
          <Link href="/lab" className="text-[var(--amber)] underline">
            /lab
          </Link>
          .
        </p>
      </header>
      <Calculators />
    </div>
  );
}
