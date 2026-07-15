"use client";

import { useEffect, useRef, useState } from "react";
import { Settings2, VideoOff } from "lucide-react";
import { GUARD_DEMO_STREAM_URL, getCameraSettings, updateCameraSettings } from "@/lib/api";
import type { CameraSettings } from "@/lib/types";

const CAMERA_ID = "kraal-cam-01";

/** RimaAI Guard's live/demo camera view, with a V380-Pro-style stream setup form. */
export function CameraPanel() {
  const [settings, setSettings] = useState<CameraSettings | null>(null);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    getCameraSettings(CAMERA_ID)
      .then(setSettings)
      .catch(() => setSettings(null));
  }, []);

  const effectiveUrl = settings
    ? settings.mode === "live"
      ? settings.stream_url
      : GUARD_DEMO_STREAM_URL
    : null;

  return (
    <div>
      <div className="relative aspect-video overflow-hidden rounded-xl bg-[#04120a]">
        {effectiveUrl ? (
          <StreamVideo url={effectiveUrl} />
        ) : (
          <div className="flex h-full w-full items-center justify-center text-white/30">
            <VideoOff size={28} />
          </div>
        )}
        <span className="absolute left-2.5 top-2 flex items-center gap-1.5 text-xs text-white/70">
          <span className="h-2 w-2 rounded-full bg-red-500" />
          {settings?.mode === "live" ? "LIVE" : "DEMO"} · {CAMERA_ID}
        </span>
      </div>

      <button
        onClick={() => setShowSettings((v) => !v)}
        className="mt-2 inline-flex items-center gap-1.5 text-xs text-black/50 hover:text-rima dark:text-white/50"
      >
        <Settings2 size={13} /> Camera settings
      </button>

      {showSettings && (
        <CameraSettingsForm
          initial={settings}
          onSaved={(updated) => {
            setSettings(updated);
            setShowSettings(false);
          }}
        />
      )}
    </div>
  );
}

function StreamVideo({ url }: { url: string }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [errored, setErrored] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    setErrored(false);

    // Safari plays HLS natively; everywhere else needs hls.js.
    if (video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = url;
      return;
    }

    let hls: import("hls.js").default | undefined;
    let cancelled = false;
    import("hls.js").then(({ default: Hls }) => {
      if (cancelled) return;
      if (!Hls.isSupported()) {
        setErrored(true);
        return;
      }
      hls = new Hls();
      hls.on(Hls.Events.ERROR, (_event, data) => {
        if (data.fatal) setErrored(true);
      });
      hls.loadSource(url);
      hls.attachMedia(video);
    });

    return () => {
      cancelled = true;
      hls?.destroy();
    };
  }, [url]);

  if (errored) {
    return (
      <div className="flex h-full w-full flex-col items-center justify-center gap-2 text-white/30">
        <VideoOff size={28} />
        <span className="text-xs">Stream unavailable</span>
      </div>
    );
  }

  return (
    <video
      ref={videoRef}
      className="h-full w-full object-cover"
      autoPlay
      muted
      loop
      playsInline
      onError={() => setErrored(true)}
    />
  );
}

function CameraSettingsForm({
  initial,
  onSaved,
}: {
  initial: CameraSettings | null;
  onSaved: (settings: CameraSettings) => void;
}) {
  const [mode, setMode] = useState<"demo" | "live">(initial?.mode ?? "demo");
  const [streamUrl, setStreamUrl] = useState(initial?.stream_url ?? "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function save(e: React.FormEvent) {
    e.preventDefault();
    if (mode === "live" && !streamUrl.trim()) {
      setError("Enter a stream URL.");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      const updated = await updateCameraSettings({
        camera_id: CAMERA_ID,
        mode,
        stream_url: mode === "live" ? streamUrl.trim() : null,
      });
      onSaved(updated);
    } catch {
      setError("Could not save camera settings.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={save} className="mt-3 space-y-2.5 rounded-xl border border-black/5 p-3">
      <div className="flex gap-1.5">
        {(["demo", "live"] as const).map((m) => (
          <button
            key={m}
            type="button"
            onClick={() => setMode(m)}
            className={`rounded-full px-3 py-1 text-xs font-semibold capitalize ${
              mode === m ? "bg-rima text-white" : "bg-black/5 text-black/60 dark:bg-white/10 dark:text-white/60"
            }`}
          >
            {m === "live" ? "Live camera" : "Demo"}
          </button>
        ))}
      </div>
      <input
        value={streamUrl}
        onChange={(e) => setStreamUrl(e.target.value)}
        disabled={mode !== "live"}
        placeholder="https://your-camera/live/index.m3u8"
        className="w-full rounded-lg border border-black/10 bg-transparent px-2.5 py-1.5 text-xs outline-none disabled:opacity-40 dark:border-white/15"
      />
      {error && <p className="text-xs text-risk-high">{error}</p>}
      <button
        type="submit"
        disabled={saving}
        className="rounded-lg bg-rima px-3 py-1.5 text-xs font-semibold text-white disabled:opacity-60"
      >
        {saving ? "Saving…" : "Save"}
      </button>
    </form>
  );
}
