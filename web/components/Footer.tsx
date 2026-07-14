import Image from "next/image";

/** Shared page footer. */
export function Footer() {
  return (
    <footer className="mt-16 border-t border-black/5">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-5 py-8 text-sm text-black/60 sm:flex-row dark:text-white/50">
        <div className="flex items-center gap-2">
          <Image src="/logo.png" alt="RimaAI logo" width={20} height={20} className="rounded-full" />
          <span>RimaAI — Smart Farming Companion for Zimbabwe</span>
        </div>
        <p>AI4I 2026 · Track 3: Development · Advice is guidance only — consult AGRITEX / a vet.</p>
      </div>
    </footer>
  );
}
