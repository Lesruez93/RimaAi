import Link from "next/link";
import { Sprout } from "lucide-react";

/** Top navigation bar shared by the landing page and dashboard. */
export function Navbar({ active }: { active?: "home" | "dashboard" }) {
  return (
    <header className="sticky top-0 z-20 border-b border-black/5 bg-[var(--background)]/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-3">
        <Link href="/" className="flex items-center gap-2 font-bold">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-rima text-white">
            <Sprout size={18} />
          </span>
          <span className="text-lg">RimaAI</span>
        </Link>
        <nav className="flex items-center gap-1 text-sm">
          <Link
            href="/"
            className={`rounded-lg px-3 py-2 hover:bg-black/5 ${
              active === "home" ? "font-semibold text-rima" : ""
            }`}
          >
            Home
          </Link>
          <Link
            href="/dashboard"
            className={`rounded-lg px-3 py-2 hover:bg-black/5 ${
              active === "dashboard" ? "font-semibold text-rima" : ""
            }`}
          >
            Officer dashboard
          </Link>
        </nav>
      </div>
    </header>
  );
}
