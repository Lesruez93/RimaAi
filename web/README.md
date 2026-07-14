# RimaAI Web

Next.js (App Router) web front-end: a public **landing page** and an **AGRITEX
officer dashboard**. Icons are `lucide-react` components (no emoji). Styling is
Tailwind CSS.

## Pages

| Route | Description |
|-------|-------------|
| `/` | Landing page — problem, features, and a call-to-action into the dashboard. |
| `/dashboard` | Officer dashboard — district risk table, community reports, dispatched alerts (auto vs. manual), and Guard events. |

The dashboard reads live data from the FastAPI backend (`/outbreaks/map`,
`/outbreaks/reports`, `/alerts`, `/guard/events`). If the backend is unreachable
it renders bundled **demo data** and shows a "Demo data" badge, so the page never
breaks in a review.

## Run

```bash
cd web
npm install
# point at the backend (defaults to http://localhost:8000):
echo "NEXT_PUBLIC_API_BASE=http://localhost:8000" > .env.local
npm run dev        # http://localhost:3000
```

Production build:
```bash
npm run build && npm start
```

## Stack
- Next.js 14 (App Router, TypeScript), React 18
- Tailwind CSS 3
- lucide-react icons

## Security note
Next.js is pinned to the latest 14.2.x patch (14.2.35). A production deployment
should track upstream Next.js security releases (and consider the Next 15 line);
the remaining low-severity advisories concern DoS/cache scenarios that do not
apply to this internal, non-public demo.
