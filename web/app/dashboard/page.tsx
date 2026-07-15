import {
  Activity,
  AlertTriangle,
  BellRing,
  MapPinned,
  Megaphone,
  Radio,
  ShieldAlert,
  Video,
  Wifi,
  WifiOff,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { StatCard } from "@/components/ui/StatCard";
import { Panel } from "@/components/ui/Card";
import { RiskPill } from "@/components/ui/RiskPill";
import { CameraPanel } from "@/components/CameraPanel";
import { loadDashboard } from "@/lib/api";
import { categoryIcon, outbreakIcon, prettyLabel, timeAgo } from "@/lib/ui";
import type { Alert, DistrictRisk, GuardEvent, OutbreakReport } from "@/lib/types";

// Always render on request so the officer sees current backend data.
export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const data = await loadDashboard();
  const highRisk = data.risks.filter((r) => r.level === "high");
  const autoAlerts = data.alerts.filter((a) => a.trigger === "auto");
  const totalRecipients = data.alerts.reduce((sum, a) => sum + a.recipients, 0);

  return (
    <main>
      <Navbar active="dashboard" />

      <div className="mx-auto max-w-6xl px-5 py-8">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl font-bold">AGRITEX officer dashboard</h1>
            <p className="text-sm text-black/60 dark:text-white/60">
              District risk, community reports, dispatched alerts and Guard events.
            </p>
          </div>
          <DataSourceBadge live={data.live} />
        </div>

        {/* KPI row */}
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            icon={AlertTriangle}
            label="High-risk districts"
            value={highRisk.length}
            hint="Auto-alerting threshold crossed"
            accent="text-risk-high"
          />
          <StatCard icon={MapPinned} label="Community reports" value={data.reports.length} hint="Most recent window" />
          <StatCard icon={Megaphone} label="Alerts dispatched" value={data.alerts.length} hint={`${totalRecipients} recipients reached`} />
          <StatCard icon={Video} label="Guard intrusions" value={data.guardEvents.length} hint="Flagged by AI detection" accent="text-risk-high" />
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <Panel title="District risk" icon={ShieldAlert}>
              <RiskTable risks={data.risks} />
            </Panel>
          </div>

          <Panel
            title="Auto-triggered alerts"
            icon={BellRing}
            action={<span className="text-xs text-black/50">{autoAlerts.length} auto</span>}
          >
            <AlertsFeed alerts={data.alerts} />
          </Panel>

          <div className="lg:col-span-2">
            <Panel title="Community outbreak reports" icon={Radio}>
              <ReportsFeed reports={data.reports} />
            </Panel>
          </div>

          <Panel title="RimaAI Guard camera" icon={Video}>
            <CameraPanel />
          </Panel>

          <Panel title="RimaAI Guard events" icon={Video}>
            <GuardFeed events={data.guardEvents} />
          </Panel>
        </div>
      </div>

      <Footer />
    </main>
  );
}

function DataSourceBadge({ live }: { live: boolean }) {
  return (
    <span
      className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold ${
        live
          ? "border-risk-low bg-risk-low/10 text-risk-low"
          : "border-rima-gold bg-rima-gold/10 text-rima-gold"
      }`}
    >
      {live ? <Wifi size={14} /> : <WifiOff size={14} />}
      {live ? "Live backend" : "Demo data (backend offline)"}
    </span>
  );
}

function RiskTable({ risks }: { risks: DistrictRisk[] }) {
  if (risks.length === 0) return <Empty label="No district risk data yet." />;
  const sorted = [...risks].sort((a, b) => b.score - a.score);
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-black/50 dark:text-white/50">
            <th className="pb-2 font-medium">District</th>
            <th className="pb-2 font-medium">Outbreak</th>
            <th className="pb-2 font-medium">Reports</th>
            <th className="pb-2 font-medium">Score</th>
            <th className="pb-2 font-medium">Risk</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((r) => {
            const Icon = outbreakIcon(r.outbreak_type);
            return (
              <tr key={`${r.region_name}-${r.outbreak_type}`} className="border-t border-black/5">
                <td className="py-2.5 font-medium">{r.region_name}</td>
                <td className="py-2.5">
                  <span className="inline-flex items-center gap-1.5 text-black/70 dark:text-white/70">
                    <Icon size={15} /> {prettyLabel(r.outbreak_type)}
                  </span>
                </td>
                <td className="py-2.5">{r.report_count}</td>
                <td className="py-2.5">{r.score.toFixed(1)}</td>
                <td className="py-2.5">
                  <RiskPill level={r.level} />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function ReportsFeed({ reports }: { reports: OutbreakReport[] }) {
  if (reports.length === 0) return <Empty label="No community reports yet." />;
  return (
    <ul className="space-y-3">
      {reports.map((r) => {
        const Icon = outbreakIcon(r.outbreak_type);
        return (
          <li key={r.id} className="flex gap-3">
            <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-rima/10 text-rima">
              <Icon size={16} />
            </span>
            <div className="min-w-0">
              <div className="flex items-center gap-2 text-sm">
                <span className="font-medium">{r.region_name}</span>
                <span className="text-black/40">·</span>
                <span className="text-black/60 dark:text-white/60">{prettyLabel(r.outbreak_type)}</span>
                <span className="text-black/40">·</span>
                <span className="text-xs text-black/40">{timeAgo(r.created_at)}</span>
              </div>
              {r.description && (
                <p className="truncate text-sm text-black/60 dark:text-white/60">{r.description}</p>
              )}
            </div>
          </li>
        );
      })}
    </ul>
  );
}

function AlertsFeed({ alerts }: { alerts: Alert[] }) {
  if (alerts.length === 0) return <Empty label="No alerts dispatched yet." />;
  return (
    <ul className="space-y-3">
      {alerts.map((a) => {
        const Icon = categoryIcon(a.category);
        return (
          <li key={a.id} className="rounded-xl border border-black/5 p-3">
            <div className="flex items-center gap-2 text-sm">
              <Icon size={15} className="text-rima" />
              <span className="font-medium capitalize">{a.category}</span>
              {a.region_name && <span className="text-black/50">· {a.region_name}</span>}
              {a.trigger === "auto" && (
                <span className="ml-auto inline-flex items-center gap-1 rounded-full bg-risk-high/10 px-2 py-0.5 text-xs font-semibold text-risk-high">
                  <Activity size={12} /> auto
                </span>
              )}
            </div>
            <p className="mt-1 line-clamp-2 text-sm text-black/60 dark:text-white/60">{a.body}</p>
            <div className="mt-1 text-xs text-black/40">
              {a.recipients} recipients · {a.channel.toUpperCase()} · {timeAgo(a.created_at)}
            </div>
          </li>
        );
      })}
    </ul>
  );
}

function GuardFeed({ events }: { events: GuardEvent[] }) {
  if (events.length === 0) return <Empty label="No Guard events." />;
  return (
    <ul className="space-y-3">
      {events.map((e) => (
        <li key={e.id} className="flex items-center gap-3">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-risk-high/10 text-risk-high">
            <ShieldAlert size={16} />
          </span>
          <div className="text-sm">
            <span className="font-medium capitalize">{e.label}</span> at {e.camera_id}
            <div className="text-xs text-black/40">
              {Math.round(e.confidence * 100)}% · {timeAgo(e.created_at)}
            </div>
          </div>
        </li>
      ))}
    </ul>
  );
}

function Empty({ label }: { label: string }) {
  return <p className="py-4 text-center text-sm text-black/40">{label}</p>;
}
