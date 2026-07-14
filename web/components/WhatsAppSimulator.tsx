"use client";

import { useRef, useState } from "react";
import { Send } from "lucide-react";
import { API_BASE } from "@/lib/api";

type Bubble = { text: string; who: "bot" | "me"; time: string };

function timeNow(): string {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

// One random phone per page load so concurrent visitors don't share the
// backend's in-memory conversation state (keyed by phone number).
function randomPhone(): string {
  const suffix = Math.floor(1_000_000 + Math.random() * 8_999_999);
  return `+2637${suffix}`;
}

/** Embedded, phone-mockup WhatsApp chat that talks to the live RimaAI bot. */
export function WhatsAppSimulator() {
  const [messages, setMessages] = useState<Bubble[]>([
    { text: "Say hi to start the RimaAI WhatsApp menu.", who: "bot", time: timeNow() },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const phoneRef = useRef(randomPhone());
  const listRef = useRef<HTMLDivElement>(null);

  function scrollToBottom() {
    requestAnimationFrame(() => {
      listRef.current?.scrollTo({ top: listRef.current.scrollHeight });
    });
  }

  async function send() {
    const value = input.trim();
    if (!value || sending) return;
    setInput("");
    setMessages((m) => [...m, { text: value, who: "me", time: timeNow() }]);
    scrollToBottom();
    setSending(true);
    try {
      const form = new URLSearchParams({ From: `whatsapp:${phoneRef.current}`, Body: value });
      const res = await fetch(`${API_BASE}/whatsapp/webhook`, { method: "POST", body: form });
      const reply = await res.text();
      setMessages((m) => [...m, { text: reply, who: "bot", time: timeNow() }]);
    } catch {
      setMessages((m) => [
        ...m,
        { text: `Network error — is the backend reachable at ${API_BASE} ?`, who: "bot", time: timeNow() },
      ]);
    } finally {
      setSending(false);
      scrollToBottom();
    }
  }

  function reset() {
    phoneRef.current = randomPhone();
    setMessages([{ text: "Say hi to start the RimaAI WhatsApp menu.", who: "bot", time: timeNow() }]);
  }

  return (
    <div className="mx-auto w-full max-w-[320px]">
      <div className="overflow-hidden rounded-[28px] border border-black/10 bg-[#111] p-2 shadow-lg">
        <div className="flex h-[480px] flex-col overflow-hidden rounded-[20px] bg-[#e5ddd5]">
          <div className="flex flex-shrink-0 items-center gap-2.5 bg-[#075E54] px-3.5 py-3 text-white">
            <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[#128C7E] text-sm font-bold">
              R
            </span>
            <div>
              <div className="text-sm font-semibold leading-tight">RimaAI</div>
              <div className="text-[11px] leading-tight opacity-80">business account</div>
            </div>
          </div>
          <div ref={listRef} className="flex flex-1 flex-col gap-1.5 overflow-y-auto px-2.5 py-3">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`max-w-[80%] whitespace-pre-wrap rounded-lg px-2.5 py-1.5 text-[13px] leading-snug shadow-sm ${
                  m.who === "me"
                    ? "self-end rounded-tr-none bg-[#dcf8c6] text-black"
                    : "self-start rounded-tl-none bg-white text-black"
                }`}
              >
                {m.text}
                <span className="mt-0.5 block text-right text-[10px] text-black/40">{m.time}</span>
              </div>
            ))}
          </div>
          <form
            className="flex flex-shrink-0 gap-1.5 bg-[#f0f0f0] p-2"
            onSubmit={(e) => {
              e.preventDefault();
              send();
            }}
          >
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message"
              className="flex-1 rounded-full border-none px-3 py-2 text-sm text-black outline-none"
            />
            <button
              type="submit"
              disabled={sending}
              className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full bg-[#25D366] text-white disabled:opacity-60"
              aria-label="Send"
            >
              <Send size={16} />
            </button>
          </form>
        </div>
      </div>
      <div className="mt-2 flex items-center justify-between text-xs text-black/50 dark:text-white/50">
        <span>No phone or Twilio needed.</span>
        <button onClick={reset} className="underline hover:text-rima">
          Reset chat
        </button>
      </div>
    </div>
  );
}
