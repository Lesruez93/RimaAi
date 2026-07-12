import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RimaAI — Smart Farming Companion for Zimbabwe",
  description:
    "AI-powered crop & livestock disease scanning, triage, forecasts, multi-channel alerts, and community outbreak mapping for Zimbabwean farmers.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
