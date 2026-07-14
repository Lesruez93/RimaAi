// Shared types mirroring the RimaAI backend schemas.

export interface DistrictRisk {
  region_name: string;
  outbreak_type: string;
  score: number;
  level: "low" | "moderate" | "high";
  report_count: number;
  latitude: number;
  longitude: number;
}

export interface OutbreakReport {
  id: number;
  region_name: string;
  outbreak_type: string;
  description: string | null;
  reporter_trust: number;
  created_at: string;
}

export interface Alert {
  id: number;
  category: string;
  region_name: string | null;
  channel: string;
  body: string;
  recipients: number;
  trigger: "manual" | "auto";
  created_at: string;
}

export interface GuardEvent {
  id: number;
  camera_id: string;
  label: string;
  confidence: number;
  is_intrusion: boolean;
  created_at: string;
}

export interface DashboardData {
  risks: DistrictRisk[];
  reports: OutbreakReport[];
  alerts: Alert[];
  guardEvents: GuardEvent[];
  live: boolean; // true when fetched from a live backend, false for mock data
}
