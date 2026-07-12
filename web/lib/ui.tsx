import {
  Bug,
  CloudRain,
  Droplets,
  Leaf,
  LucideIcon,
  ShieldAlert,
  Sprout,
  Waves,
} from "lucide-react";

/** Prettify a snake_case label, e.g. "tomato_late_blight" -> "Tomato late blight". */
export function prettyLabel(value: string): string {
  const s = value.replace(/_/g, " ");
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Relative time like "2d ago" / "3h ago" from an ISO timestamp. */
export function timeAgo(iso: string): string {
  const then = new Date(iso).getTime();
  const mins = Math.max(0, Math.round((Date.now() - then) / 60_000));
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.round(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.round(hours / 24)}d ago`;
}

/** Tailwind classes for a risk level pill. */
export function riskClasses(level: string): string {
  switch (level) {
    case "high":
      return "bg-risk-high/15 text-risk-high border-risk-high";
    case "moderate":
      return "bg-risk-moderate/15 text-risk-moderate border-risk-moderate";
    default:
      return "bg-risk-low/15 text-risk-low border-risk-low";
  }
}

/** Icon for an outbreak type. */
export function outbreakIcon(type: string): LucideIcon {
  switch (type) {
    case "crop_disease":
      return Sprout;
    case "armyworm":
      return Bug;
    case "locusts":
      return Bug;
    case "tick_disease":
      return ShieldAlert;
    case "flood":
      return Waves;
    default:
      return Leaf;
  }
}

/** Icon for an alert category. */
export function categoryIcon(category: string): LucideIcon {
  switch (category) {
    case "weather":
      return CloudRain;
    case "disease":
      return ShieldAlert;
    case "livestock":
      return ShieldAlert;
    case "insurance":
      return Droplets;
    default:
      return Leaf;
  }
}
