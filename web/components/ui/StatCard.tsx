import { LucideIcon } from "lucide-react";

interface StatCardProps {
  icon: LucideIcon;
  label: string;
  value: string | number;
  hint?: string;
  accent?: string; // tailwind text/border color class, e.g. "text-risk-high"
}

/** A KPI tile with a leading icon. */
export function StatCard({ icon: Icon, label, value, hint, accent = "text-rima" }: StatCardProps) {
  return (
    <div className="rounded-2xl border border-black/5 bg-white/60 p-5 shadow-sm dark:bg-white/5">
      <div className="flex items-center justify-between">
        <span className="text-sm text-black/60 dark:text-white/60">{label}</span>
        <Icon size={20} className={accent} />
      </div>
      <div className="mt-2 text-3xl font-bold">{value}</div>
      {hint && <div className="mt-1 text-xs text-black/50 dark:text-white/40">{hint}</div>}
    </div>
  );
}
