import Link from "next/link";
import {
  ArrowRight,
  Camera,
  CloudRain,
  Languages,
  LayoutDashboard,
  MapPin,
  MessageSquare,
  ShieldAlert,
  Smartphone,
  Stethoscope,
  Video,
  WifiOff,
} from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";

const features = [
  { icon: Camera, title: "Crop disease scanner", body: "Photograph a leaf and get an offline, on-device diagnosis with treatment advice in English, Shona and Ndebele." },
  { icon: Stethoscope, title: "Livestock advisor", body: "Photo health checks plus a symptom triage chat — tuned to catch tick-borne January disease early." },
  { icon: CloudRain, title: "Forecasts & alerts", body: "Localized planting windows and rainfall guidance, delivered even on low-bandwidth channels." },
  { icon: MessageSquare, title: "USSD / SMS / WhatsApp", body: "Feature-phone farmers dial *123# or subscribe by SMS to weather, disease, livestock and insurance alerts." },
  { icon: Video, title: "RimaAI Guard", body: "For commercial farms: AI camera surveillance that flags human and vehicle intrusion near kraals at night." },
  { icon: MapPin, title: "Outbreak heat map", body: "Community reports aggregate into a district risk map that auto-triggers targeted alerts to nearby subscribers." },
];

const problems = [
  { stat: "100,000s", label: "cattle lost to January disease (2017–2021) — a preventable, treatable tick-borne illness." },
  { stat: "1 : 100s", label: "AGRITEX extension officer to farmer ratio — first-line advice rarely arrives in time." },
  { stat: "3", label: "languages throughout (EN / SN / ND) — most agricultural content is English-only." },
];

export default function LandingPage() {
  return (
    <main>
      <Navbar active="home" />

      {/* Hero */}
      <section className="mx-auto max-w-6xl px-5 pb-8 pt-16 text-center">
        <span className="inline-flex items-center gap-2 rounded-full border border-rima/30 bg-rima/10 px-3 py-1 text-sm font-medium text-rima">
          <Smartphone size={15} /> Offline-first · Multi-channel · Trilingual
        </span>
        <h1 className="mx-auto mt-6 max-w-3xl text-4xl font-extrabold leading-tight sm:text-5xl">
          An agricultural extension officer in every farmer&apos;s pocket
        </h1>
        <p className="mx-auto mt-5 max-w-2xl text-lg text-black/70 dark:text-white/70">
          RimaAI puts AI-powered crop and livestock diagnosis, forecasts, and
          outbreak alerts into the hands of Zimbabwean farmers — online or off,
          on a smartphone or a feature phone.
        </p>
        <div className="mt-8 flex items-center justify-center gap-3">
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 rounded-xl bg-rima px-5 py-3 font-semibold text-white shadow-sm transition hover:bg-rima-dark"
          >
            <LayoutDashboard size={18} /> Open officer dashboard
          </Link>
          <a
            href="#features"
            className="inline-flex items-center gap-2 rounded-xl border border-black/10 px-5 py-3 font-semibold transition hover:bg-black/5"
          >
            Explore features <ArrowRight size={18} />
          </a>
        </div>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm text-black/60 dark:text-white/60">
          <span className="inline-flex items-center gap-2"><WifiOff size={16} /> Works offline</span>
          <span className="inline-flex items-center gap-2"><Languages size={16} /> English · chiShona · isiNdebele</span>
          <span className="inline-flex items-center gap-2"><ShieldAlert size={16} /> Human-oversight by design</span>
        </div>
      </section>

      {/* Problem */}
      <section className="mx-auto max-w-6xl px-5 py-12">
        <div className="grid gap-4 sm:grid-cols-3">
          {problems.map((p) => (
            <div key={p.label} className="rounded-2xl border border-black/5 bg-white/60 p-6 dark:bg-white/5">
              <div className="text-3xl font-extrabold text-rima">{p.stat}</div>
              <p className="mt-2 text-sm text-black/70 dark:text-white/70">{p.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section id="features" className="mx-auto max-w-6xl px-5 py-8">
        <h2 className="text-2xl font-bold">One companion, six capabilities</h2>
        <p className="mt-2 max-w-2xl text-black/60 dark:text-white/60">
          Built where AI genuinely helps — and honest about where plain rules do
          the job instead.
        </p>
        <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((f) => (
            <div key={f.title} className="rounded-2xl border border-black/5 bg-white/60 p-6 shadow-sm dark:bg-white/5">
              <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-rima/10 text-rima">
                <f.icon size={22} />
              </span>
              <h3 className="mt-4 text-lg font-semibold">{f.title}</h3>
              <p className="mt-2 text-sm text-black/70 dark:text-white/70">{f.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-6xl px-5 py-12">
        <div className="rounded-3xl bg-rima px-8 py-12 text-center text-white">
          <h2 className="text-2xl font-bold sm:text-3xl">See the early-warning loop in action</h2>
          <p className="mx-auto mt-3 max-w-2xl text-white/80">
            The officer dashboard shows live district risk, community outbreak
            reports, dispatched alerts and Guard events — the same data farmers
            generate from the field.
          </p>
          <Link
            href="/dashboard"
            className="mt-6 inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 font-semibold text-rima-dark transition hover:bg-white/90"
          >
            <LayoutDashboard size={18} /> Open the dashboard
          </Link>
        </div>
      </section>

      <Footer />
    </main>
  );
}
