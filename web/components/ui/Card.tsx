import { LucideIcon } from "lucide-react";

/** A titled panel with an icon header, used across the dashboard. */
export function Panel({
  title,
  icon: Icon,
  children,
  action,
}: {
  title: string;
  icon: LucideIcon;
  children: React.ReactNode;
  action?: React.ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-black/5 bg-white/60 shadow-sm dark:bg-white/5">
      <div className="flex items-center justify-between border-b border-black/5 px-5 py-3">
        <h2 className="flex items-center gap-2 font-semibold">
          <Icon size={18} className="text-rima" />
          {title}
        </h2>
        {action}
      </div>
      <div className="p-5">{children}</div>
    </section>
  );
}
