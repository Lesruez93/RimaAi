import { riskClasses } from "@/lib/ui";

/** A small coloured pill showing a risk level. */
export function RiskPill({ level }: { level: string }) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-bold uppercase tracking-wide ${riskClasses(
        level,
      )}`}
    >
      {level}
    </span>
  );
}
