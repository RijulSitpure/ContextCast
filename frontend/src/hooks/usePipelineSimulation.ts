import { useState, useCallback, useRef } from "react";
import type { PipelineStep } from "@/components/StatusStepper";
import type { LogEntry } from "@/components/ProcessingLog";

const makeLog = (message: string, type: LogEntry["type"] = "info"): LogEntry => ({
  id: crypto.randomUUID(),
  timestamp: new Date().toLocaleTimeString("en-US", { hour12: false }),
  message,
  type,
});

export function usePipelineSimulation() {
  const [step, setStep] = useState<PipelineStep>("idle");
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [streamingText, setStreamingText] = useState("");
  const [mediaReady, setMediaReady] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string | undefined>(undefined); // NEW: State for the real video link
  const abortRef = useRef(false);

  const addLog = useCallback((msg: string, type: LogEntry["type"] = "info") => {
    setLogs((prev) => [...prev, makeLog(msg, type)]);
  }, []);

  const startPipeline = useCallback(async (file: File, topic: string, persona: string) => {
    abortRef.current = false;
    setMediaReady(false);
    setVideoUrl(undefined); // Reset previous video
    setLogs([]);
    setStreamingText("");
    setStep("uploading");

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("topic", topic);
      formData.append("persona", persona); // Now sending persona to backend!

      const response = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(`Server responded with ${response.status}`);

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) throw new Error("Failed to read response stream");

      while (true) {
        const { value, done } = await reader.read();
        if (done || abortRef.current) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const jsonString = line.replace("data: ", "").trim();
            if (!jsonString) continue;

            try {
              const data = JSON.parse(jsonString);
              
              setStep(data.step);

              if (data.step === "error") {
                addLog(data.msg, "error");
                return;
              }

              if (data.step === "thinking") {
                addLog(data.msg, "thinking");
              } else {
                addLog(data.msg, data.step === "complete" ? "success" : "info");
              }

              if (data.step === "complete") {
                // IMPORTANT: This replaces the 'Rabbit' with your real video
                setVideoUrl(data.video_url);
                setMediaReady(true);
              }
            } catch (e) {
              console.error("Error parsing JSON chunk:", e);
            }
          }
        }
      }
    } catch (err) {
      addLog(`Connection Error: ${err instanceof Error ? err.message : String(err)}`, "error");
      setStep("idle");
    }
  }, [addLog]);

  const reset = useCallback(() => {
    abortRef.current = true;
    setStep("idle");
    setLogs([]);
    setStreamingText("");
    setMediaReady(false);
    setVideoUrl(undefined);
  }, []);

  // Ensure videoUrl is included in the return object
  return { step, logs, streamingText, mediaReady, videoUrl, startPipeline, reset };
}