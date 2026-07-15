import Link from "next/link";
import Image from "next/image";
import {
  ArrowRight,
  Camera,
  CloudRain,
  Download,
  Github,
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
import { WhatsAppSimulator } from "@/components/WhatsAppSimulator";
import { UssdSimulator } from "@/components/UssdSimulator";

const GITHUB_URL = "https://github.com/Lesruez93/RimaAi";

const evaluatorLinks = [
  {
    icon: LayoutDashboard,
    title: "UI demo",
    body: "The officer dashboard on this site — live district risk, alerts and Guard events, no install needed.",
    href: "/dashboard",
    cta: "Open dashboard",
    external: false,
  },
  {
    icon: Download,
    title: "Android APK",
    body: "Release build, points at the live backend by default — install directly on a test device.",
    href: "/downloads/RimaAI.apk",
    cta: "Download APK",
    external: false,
  },
  {
    icon: Github,
    title: "Source code",
    body: "Backend, Flutter app, web dashboard, docs and tests — everything behind this demo.",
    href: GITHUB_URL,
    cta: "View on GitHub",
    external: true,
  },
  {
    icon: MessageSquare,
    title: "USSD simulator",
    body: "Feature-phone flow in the browser — dial *123# against the live backend, no telco needed.",
    href: "#simulators",
    cta: "Try it below",
    external: false,
  },
  {
    icon: Smartphone,
    title: "WhatsApp simulator",
    body: "Chat with the real RimaAI WhatsApp bot in the browser — subscribe, check symptoms, no phone needed.",
    href: "#simulators",
    cta: "Try it below",
    external: false,
  },
];

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
      <section className="mx-auto max-w-6xl px-5 pb-8 pt-14 text-center">
        <Image
          src="/logo.png"
          alt="RimaAI logo"
          width={132}
          height={132}
          priority
          className="mx-auto mb-6 drop-shadow-sm"
        />
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

      {/* Evaluator links — everything a judge needs, from this one page */}
      <section className="mx-auto max-w-6xl px-5 py-8">
        <div className="rounded-2xl border border-rima/20 bg-rima/5 p-6">
          <h2 className="text-center text-lg font-bold">
            For judges &amp; evaluators — everything is here
          </h2>
          <p className="mx-auto mt-1 max-w-2xl text-center text-sm text-black/60 dark:text-white/60">
            This page is the single hub for the AI4I submission: the UI demo,
            the Android APK, the GitHub source and the USSD and WhatsApp
            simulators are all linked below.
          </p>
          <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
            {evaluatorLinks.map((l) => (
              <div
                key={l.title}
                className="flex flex-col rounded-xl border border-black/5 bg-white/70 p-5 dark:bg-white/5"
              >
                <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-rima/10 text-rima">
                  <l.icon size={20} />
                </span>
                <h3 className="mt-3 font-semibold">{l.title}</h3>
                <p className="mt-1 flex-1 text-sm text-black/60 dark:text-white/60">{l.body}</p>
                <a
                  href={l.href}
                  target={l.external ? "_blank" : undefined}
                  rel={l.external ? "noopener noreferrer" : undefined}
                  className="mt-4 inline-flex items-center gap-1.5 text-sm font-semibold text-rima hover:underline"
                >
                  {l.cta} <ArrowRight size={14} />
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Simulators — live, embedded, no install */}
      <section id="simulators" className="mx-auto max-w-6xl px-5 py-12">
        <h2 className="text-center text-2xl font-bold">Try it right here</h2>
        <p className="mx-auto mt-2 max-w-2xl text-center text-black/60 dark:text-white/60">
          Both talk to the same live backend a real farmer would reach over
          USSD or WhatsApp — no telco, no Twilio, no install.
        </p>
        <div className="mt-8 grid gap-10 sm:grid-cols-2">
          <WhatsAppSimulator />
          <UssdSimulator />
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

      {/* Screenshots */}
      <section className="mx-auto max-w-6xl px-5 py-8">
        <h2 className="text-2xl font-bold">See it, not just read about it</h2>
        <p className="mt-2 max-w-2xl text-black/60 dark:text-white/60">
          Real captures from this live deployment — not mockups.
        </p>
        <div className="mt-8 grid gap-6">
          <figure className="overflow-hidden rounded-2xl border border-black/5 bg-white/60 shadow-sm dark:bg-white/5">
            <Image
              src="/screenshots/dashboard.png"
              alt="AGRITEX officer dashboard showing district risk, community reports, alerts and Guard events"
              width={2560}
              height={1520}
              className="w-full"
            />
            <figcaption className="border-t border-black/5 px-5 py-3 text-sm text-black/60 dark:text-white/60">
              Officer dashboard — live district risk, alerts and Guard events.
            </figcaption>
          </figure>
          <figure className="overflow-hidden rounded-2xl border border-black/5 bg-white/60 shadow-sm dark:bg-white/5">
            <Image
              src="/screenshots/simulators.png"
              alt="WhatsApp and USSD simulators mid-conversation, subscribing a farmer to disease outbreak alerts"
              width={2224}
              height={1044}
              className="w-full"
            />
            <figcaption className="border-t border-black/5 px-5 py-3 text-sm text-black/60 dark:text-white/60">
              The WhatsApp and USSD simulators above, mid-conversation.
            </figcaption>
          </figure>
        </div>

        <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-4 lg:grid-cols-7">
          {[
            { src: "/screenshots/app_onboarding.png", alt: "RimaAI onboarding screen with language selection: English, chiShona, isiNdebele", caption: "Onboarding" },
            { src: "/screenshots/app_home.png", alt: "RimaAI Android app home screen with planting-window forecast, Scan a crop, Livestock and Guard cards", caption: "Home" },
            { src: "/screenshots/app_scan.png", alt: "Scan a crop screen with camera and gallery capture options", caption: "Scan a crop" },
            { src: "/screenshots/app_livestock.png", alt: "Livestock health check screen with photo check and symptom chat", caption: "Livestock" },
            { src: "/screenshots/app_outbreak_report.png", alt: "Report an outbreak screen with outbreak type, district and description fields", caption: "Report outbreak" },
            { src: "/screenshots/app_outbreak_map.png", alt: "Outbreak map screen with Zimbabwe district risk markers", caption: "Outbreak map" },
            { src: "/screenshots/app_alerts.png", alt: "Subscribe to alerts screen with phone number, district and consent", caption: "Alerts" },
          ].map((s) => (
            <figure key={s.src} className="overflow-hidden rounded-2xl border border-black/5 bg-white/60 shadow-sm dark:bg-white/5">
              <Image
                src={s.src}
                alt={s.alt}
                width={1080}
                height={2412}
                className="w-full"
              />
              <figcaption className="border-t border-black/5 px-3 py-2 text-center text-xs font-medium text-black/60 dark:text-white/60">
                {s.caption}
              </figcaption>
            </figure>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-6xl px-5 py-12">
        <div className="rounded-3xl bg-gradient-to-r from-rima to-rima-blue px-8 py-12 text-center text-white">
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
