import { useCallback, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FileUp, FileText, X } from "lucide-react";

interface PdfUploaderProps {
  onUpload: (file: File) => void;
  isProcessing: boolean;
}

const PdfUploader = ({ onUpload, isProcessing }: PdfUploaderProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFile = useCallback(
    (f: File) => {
      if (f.type === "application/pdf") {
        setFile(f);
        onUpload(f);
      }
    },
    [onUpload]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      const f = e.dataTransfer.files[0];
      if (f) handleFile(f);
    },
    [handleFile]
  );

  const removeFile = () => {
    if (!isProcessing) setFile(null);
  };

  return (
    <div className="glass-panel p-4">
      <div className="flex items-center gap-2 mb-3">
        <FileUp className="w-4 h-4 text-neon-cyan" />
        <span className="text-sm font-semibold text-foreground">Upload PDF</span>
      </div>

      <AnimatePresence mode="wait">
        {!file ? (
          <motion.label
            key="dropzone"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            className={`flex flex-col items-center justify-center gap-3 p-8 rounded-lg border-2 border-dashed cursor-pointer transition-all duration-200 ${
              dragOver
                ? "border-neon-cyan bg-neon-cyan/5"
                : "border-border hover:border-muted-foreground/40"
            }`}
          >
            <div className="w-12 h-12 rounded-full bg-muted/50 flex items-center justify-center">
              <FileUp className="w-6 h-6 text-muted-foreground" />
            </div>
            <div className="text-center">
              <p className="text-sm font-medium text-foreground">Drop your PDF here</p>
              <p className="text-xs text-muted-foreground mt-1">or click to browse</p>
            </div>
            <input
              type="file"
              accept=".pdf"
              className="hidden"
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) handleFile(f);
              }}
            />
          </motion.label>
        ) : (
          <motion.div
            key="file-info"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="flex items-center gap-3 p-3 rounded-lg bg-muted/30 border border-border/50"
          >
            <div className="w-10 h-10 rounded-lg bg-neon-cyan/10 flex items-center justify-center shrink-0">
              <FileText className="w-5 h-5 text-neon-cyan" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground truncate">{file.name}</p>
              <p className="text-xs text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
            {!isProcessing && (
              <button onClick={removeFile} className="text-muted-foreground hover:text-foreground transition-colors">
                <X className="w-4 h-4" />
              </button>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default PdfUploader;
