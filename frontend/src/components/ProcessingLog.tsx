import { useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Terminal } from "lucide-react";

export interface LogEntry {
  id: string;
  timestamp: string;
  message: string;
  type: "info" | "success" | "error" | "thinking";
}

interface ProcessingLogProps {
  logs: LogEntry[];
  streamingText?: string;
}

const typeColors: Record<LogEntry["type"], string> = {
  info: "text-muted-foreground",
  success: "text-terminal-green",
  error: "text-destructive",
  thinking: "text-neon-violet",
};

const ProcessingLog = ({ logs, streamingText }: ProcessingLogProps) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs, streamingText]);

  return (
    <div className="glass-panel flex flex-col flex-1 min-h-0">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border/50">
        <Terminal className="w-4 h-4 text-neon-cyan" />
        <span className="text-sm font-semibold text-foreground">Processing Log</span>
        <div className="ml-auto flex gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-destructive/60" />
          <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/60" />
          <div className="w-2.5 h-2.5 rounded-full bg-terminal-green/60" />
        </div>
      </div>
      <div className="flex-1 overflow-y-auto scrollbar-thin p-4 bg-terminal-bg/50 rounded-b-xl">
        <div className="space-y-1 terminal-font text-xs leading-relaxed">
          {logs.map((log) => (
            <motion.div
              key={log.id}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.2 }}
              className="flex gap-2"
            >
              <span className="text-muted-foreground/50 shrink-0">[{log.timestamp}]</span>
              <span className={typeColors[log.type]}>{log.message}</span>
            </motion.div>
          ))}
          {streamingText && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex gap-2 text-neon-violet"
            >
              <span className="text-muted-foreground/50 shrink-0">[stream]</span>
              <span>
                {streamingText}
                <span className="animate-pulse-glow">▌</span>
              </span>
            </motion.div>
          )}
          <div ref={bottomRef} />
        </div>
      </div>
    </div>
  );
};

export default ProcessingLog;
