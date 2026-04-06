import { useState } from "react";
import { motion } from "framer-motion";
import { Cpu, Zap, MessageSquare, Play } from "lucide-react"; 
import StatusStepper from "@/components/StatusStepper";
import PersonaToggle from "@/components/PersonaToggle";
import PdfUploader from "@/components/PdfUploader";
import ProcessingLog from "@/components/ProcessingLog";
import MediaGallery from "@/components/MediaGallery";
import { usePipelineSimulation } from "@/hooks/usePipelineSimulation";

const Index = () => {
  const [persona, setPersona] = useState("expert-skeptic");
  const [topic, setTopic] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null); // New state to hold file
  
  const { step, logs, streamingText, mediaReady, videoUrl, startPipeline } = usePipelineSimulation();

  const isProcessing = step !== "idle" && step !== "complete";

  // Now handleUpload only sets the file, doesn't start the engine
  const handleFileSelection = (file: File) => {
    setSelectedFile(file);
  };

  const handleGenerate = () => {
    if (selectedFile && topic) {
      startPipeline(selectedFile, topic, persona);
    }
  };

  const demoBackground = mediaReady ? "podcast_visual.png" : undefined;
  const demoTranscript = mediaReady ? "#" : undefined;

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-neon-cyan/[0.03] blur-[120px]" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-neon-violet/[0.04] blur-[120px]" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 py-6 flex flex-col min-h-screen">
        {/* Header */}
        <header className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl gradient-cyber flex items-center justify-center">
              <Cpu className="w-5 h-5 text-background" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-foreground tracking-tight flex items-center gap-2">
                ContextCast
              </h1>
              <p className="text-xs text-muted-foreground">Multimodal RAG → Video Podcast</p>
            </div>
          </div>
          <div className="flex items-center gap-3 text-xs text-muted-foreground">
            <Zap className="w-3.5 h-3.5 text-neon-cyan" />
            <span>Llama 3 + SDXL + Edge-TTS</span>
          </div>
        </header>

        {/* Status Stepper */}
        <div className="glass-panel px-4 py-3 mb-6">
          <StatusStepper currentStep={step} />
        </div>

        {/* Two-Column Layout */}
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-6 min-h-0">
          
          {/* Left Column (Inputs) */}
          <div className="flex flex-col gap-4 min-h-0">
            
            {/* 1. PDF Uploader (Top) */}
            <PdfUploader onUpload={handleFileSelection} isProcessing={isProcessing} />

            {/* 2. Persona Selection */}
            <PersonaToggle selected={persona} onSelect={setPersona} />

            {/* 3. Discussion Focus (Now Below PDF/Persona) */}
            <div className="glass-panel p-4 space-y-3">
              <div className="flex items-center gap-2 text-sm font-medium text-neon-cyan">
                <MessageSquare className="w-4 h-4" />
                Discussion Focus
              </div>
              <input
                type="text"
                placeholder="What should the hosts discuss from the PDF?"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="w-full bg-background/50 border border-border rounded-lg px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-1 focus:ring-neon-cyan/50 transition-all"
              />
              
              {/* 4. THE GENERATE BUTTON */}
              <button
                onClick={handleGenerate}
                disabled={!selectedFile || !topic || isProcessing}
                className="w-full mt-2 py-3 px-4 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all 
                  disabled:opacity-50 disabled:cursor-not-allowed
                  bg-gradient-to-r from-neon-cyan to-neon-violet text-background hover:scale-[1.02] active:scale-[0.98]"
              >
                <Play className="w-4 h-4 fill-current" />
                {isProcessing ? "Generating..." : "Generate Podcast"}
              </button>
            </div>

            <ProcessingLog logs={logs} streamingText={streamingText} />
          </div>

          {/* Right Column (Media) */}
          <div className="min-h-0">
            <MediaGallery
              videoUrl={videoUrl}
              backgroundUrl={demoBackground}
              transcriptUrl={demoTranscript}
              isReady={mediaReady}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;