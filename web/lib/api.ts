import { mockDashboard } from "./mockData";
import type { Alert, CameraSettings, DashboardData, DistrictRisk, GuardEvent, OutbreakReport } from "./types";

// Built-in demo footage shown in "demo" mode, so Guard looks alive before a
// real camera is configured. Mirrors the backend's seeded default and the
// mobile app's `kGuardDemoStreamUrl`.
export const GUARD_DEMO_STREAM_URL =
  "https://hls-harbor-livepush.akamaized.net/live_cdn/nsqIStpj8PaG-Ev/emcQJ0pGpremocy/index.m3u8";

// In production the backend is deployed alongside the site on Vercel and
// reached same-origin at /api (see vercel.json), so there is no CORS or
// separate host to configure. NEXT_PUBLIC_API_BASE overrides this; local
// `next dev` defaults to a backend on localhost:8000.
const DEFAULT_API_BASE =
  process.env.NODE_ENV === "production" ? "/api" : "http://localhost:8000";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE?.replace(/\/$/, "") ?? DEFAULT_API_BASE;

/** API base usable from server components, where a relative URL can't be fetched. */
function serverApiBase(): string {
  if (!API_BASE.startsWith("/")) return API_BASE;
  const host = process.env.VERCEL_PROJECT_PRODUCTION_URL ?? process.env.VERCEL_URL;
  return host ? `https://${host}${API_BASE}` : `http://localhost:3000${API_BASE}`;
}

async function getJson<T>(path: string): Promise<T> {
  const base = typeof window === "undefined" ? serverApiBase() : API_BASE;
  const res = await fetch(`${base}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`${path} -> ${res.status}`);
  return (await res.json()) as T;
}

/** Fetch a camera's stream configuration (client-side; used by CameraPanel). */
export async function getCameraSettings(cameraId: string): Promise<CameraSettings> {
  return getJson<CameraSettings>(`/guard/camera?camera_id=${encodeURIComponent(cameraId)}`);
}

/** Configure a camera's stream URL and demo/live mode. */
export async function updateCameraSettings(settings: CameraSettings): Promise<CameraSettings> {
  const res = await fetch(`${API_BASE}/guard/camera`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(settings),
  });
  if (!res.ok) throw new Error(`/guard/camera -> ${res.status}`);
  return (await res.json()) as CameraSettings;
}

/**
 * Load all data the officer dashboard needs from the live backend. If any call
 * fails (e.g. backend offline), falls back to bundled mock data so the page
 * always renders. The returned `live` flag reflects which source was used.
 */
export async function loadDashboard(): Promise<DashboardData> {
  try {
    const [risks, reports, alerts, guardEvents] = await Promise.all([
      getJson<DistrictRisk[]>("/outbreaks/map"),
      getJson<OutbreakReport[]>("/outbreaks/reports?limit=20"),
      getJson<Alert[]>("/alerts?limit=20"),
      getJson<GuardEvent[]>("/guard/events?limit=20"),
    ]);
    return { risks, reports, alerts, guardEvents, live: true };
  } catch {
    return mockDashboard;
  }
}
