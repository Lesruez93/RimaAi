import type { DashboardData } from "./types";

// Fallback data so the dashboard renders standalone when the backend is offline
// (mirrors the backend seed script: Gokwe tips into high tick-disease risk).
const now = Date.now();
const iso = (daysAgo: number) =>
  new Date(now - daysAgo * 86_400_000).toISOString();

export const mockDashboard: DashboardData = {
  live: false,
  risks: [
    { region_name: "Gokwe", outbreak_type: "tick_disease", score: 6.3, level: "high", report_count: 10, latitude: -18.21, longitude: 28.93 },
    { region_name: "Mutare", outbreak_type: "crop_disease", score: 3.4, level: "moderate", report_count: 2, latitude: -18.97, longitude: 32.67 },
    { region_name: "Masvingo", outbreak_type: "armyworm", score: 2.1, level: "low", report_count: 1, latitude: -20.07, longitude: 30.83 },
    { region_name: "Bulawayo", outbreak_type: "flood", score: 1.4, level: "low", report_count: 1, latitude: -20.15, longitude: 28.58 },
  ],
  reports: [
    { id: 14, region_name: "Gokwe", outbreak_type: "tick_disease", description: "Several cattle with heavy tick load and fever.", reporter_trust: 0.9, created_at: iso(0) },
    { id: 13, region_name: "Gokwe", outbreak_type: "tick_disease", description: "Swollen lymph nodes reported in the herd.", reporter_trust: 0.8, created_at: iso(1) },
    { id: 12, region_name: "Mutare", outbreak_type: "crop_disease", description: "Tomato leaves with dark blight spots.", reporter_trust: 0.7, created_at: iso(1) },
    { id: 11, region_name: "Masvingo", outbreak_type: "armyworm", description: "Fall armyworm larvae in maize whorls.", reporter_trust: 0.6, created_at: iso(2) },
  ],
  alerts: [
    { id: 8, category: "disease", region_name: "Gokwe", channel: "sms", body: "RimaAI ALERT: High tick-borne (January) disease risk reported in Gokwe. Inspect your livestock, act early, and contact AGRITEX/your vet.", recipients: 4, trigger: "auto", created_at: iso(0) },
    { id: 7, category: "livestock", region_name: "Gokwe", channel: "sms", body: "Dip cattle weekly this season to prevent January disease.", recipients: 6, trigger: "manual", created_at: iso(2) },
    { id: 6, category: "weather", region_name: "Masvingo", channel: "sms", body: "Erratic rains expected — stagger planting and keep drought-tolerant seed ready.", recipients: 5, trigger: "manual", created_at: iso(3) },
  ],
  guardEvents: [
    { id: 3, camera_id: "kraal-cam-01", label: "person", confidence: 0.91, is_intrusion: true, created_at: iso(0) },
    { id: 2, camera_id: "kraal-cam-01", label: "vehicle", confidence: 0.83, is_intrusion: true, created_at: iso(1) },
  ],
};
