"use client";

import { useRef, useState } from "react";
import { API_BASE } from "@/lib/api";

const IDLE_SCREEN = "Dial *123# and press Send to begin.";

// One random phone per page load so concurrent visitors don't share
// backend-side subscription state.
function randomPhone(): string {
  const suffix = Math.floor(1_000_000 + Math.random() * 8_999_999);
  return `+2637${suffix}`;
}

/** Embedded feature-phone mockup that drives the live RimaAI /ussd endpoint. */
export function UssdSimulator() {
  const [screen, setScreen] = useState(IDLE_SCREEN);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const startedRef = useRef(false);
  const sessionTextRef = useRef("");
  const phoneRef = useRef(randomPhone());

  async function post() {
    const form = new URLSearchParams({
      phoneNumber: phoneRef.current,
      text: sessionTextRef.current,
      sessionId: "web-sim",
      serviceCode: "*123#",
    });
    setBusy(true);
    try {
      const res = await fetch(`${API_BASE}/ussd`, { method: "POST", body: form });
      const raw = await res.text();
      const ended = raw.startsWith("END");
      setScreen(raw.replace(/^(CON|END)\s?/, ""));
      if (ended) {
        startedRef.current = false;
        sessionTextRef.current = "";
      }
    } catch {
      setScreen(`Network error — is the backend reachable at ${API_BASE} ?`);
      startedRef.current = false;
      sessionTextRef.current = "";
    } finally {
      setBusy(false);
    }
  }

  function send() {
    const value = input.trim();
    if (!value || busy) return;
    setInput("");
    if (!startedRef.current) {
      if (value.replace(/\s/g, "") !== "*123#") {
        setScreen("Dial *123# to start the RimaAI menu.");
        return;
      }
      startedRef.current = true;
      sessionTextRef.current = "";
    } else {
      sessionTextRef.current = sessionTextRef.current
        ? `${sessionTextRef.current}*${value}`
        : value;
    }
    post();
  }

  function reset() {
    startedRef.current = false;
    sessionTextRef.current = "";
    phoneRef.current = randomPhone();
    setScreen(IDLE_SCREEN);
  }

  return (
    <div className="mx-auto w-full max-w-[320px]">
      <div className="rounded-[28px] border border-black/10 bg-[#111] p-[18px] shadow-lg">
        <div className="min-h-[230px] whitespace-pre-wrap rounded-xl bg-[#0b0b0b] p-3.5 font-mono text-sm leading-relaxed text-[#d7ffd7]">
          <span className="mb-2 block font-bold text-[#8bc34a]">RimaAI USSD Simulator</span>
          {screen}
        </div>
        <form
          className="mt-3 flex gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            send();
          }}
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type reply, e.g. *123# then 1"
            className="flex-1 rounded-lg border-none px-2.5 py-2 text-[15px] text-black outline-none"
          />
          <button
            type="submit"
            disabled={busy}
            className="rounded-lg bg-[#2e7d32] px-3.5 py-2 font-semibold text-white disabled:opacity-60"
          >
            Send
          </button>
        </form>
      </div>
      <div className="mt-2 flex items-center justify-between text-xs text-black/50 dark:text-white/50">
        <span>Feature-phone flow — no data connection needed.</span>
        <button onClick={reset} className="underline hover:text-rima">
          Reset
        </button>
      </div>
    </div>
  );
}
