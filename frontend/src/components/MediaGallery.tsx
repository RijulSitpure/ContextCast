import { motion, AnimatePresence } from "framer-motion";
import { Play, Image, FileText, Download, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";

interface MediaGalleryProps {
  videoUrl?: string;
  backgroundUrl?: string;
  transcriptUrl?: string;
  isReady: boolean;
}

const MediaGallery = ({ videoUrl, backgroundUrl, transcriptUrl, isReady }: MediaGalleryProps) => {
  return (
    <div className="glass-panel-glow flex flex-col h-full">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border/50">
        <Play className="w-4 h-4 text-neon-cyan" />
        <span className="text-sm font-semibold text-foreground">Media Gallery</span>
      </div>

      <div className="flex-1 p-4 space-y-4 overflow-y-auto scrollbar-thin">
        <AnimatePresence mode="wait">
          {!isReady ? (
            <motion.div
              key="placeholder"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center h-full gap-4 py-16"
            >
              <div className="relative w-20 h-20">
                <div className="absolute inset-0 rounded-2xl bg-muted/30 border border-border/50" />
                <div className="absolute inset-0 flex items-center justify-center">
                  <Play className="w-8 h-8 text-muted-foreground/40" />
                </div>
                <div className="absolute inset-0 rounded-2xl overflow-hidden">
                  <div className="absolute inset-0 bg-gradient-to-b from-neon-cyan/5 to-transparent animate-scan-line" />
                </div>
              </div>
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Awaiting generation</p>
                <p className="text-xs text-muted-foreground/60 mt-1">Upload a PDF to begin</p>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, staggerChildren: 0.1 }}
              className="space-y-4"
            >
              {/* Video Player */}
              {videoUrl && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="rounded-lg overflow-hidden border border-border/50 bg-muted/20"
                >
                  <video
                    src={videoUrl}
                    controls
                    className="w-full aspect-video bg-background"
                    poster={backgroundUrl}
                  />
                  <div className="flex items-center justify-between p-3">
                    <span className="text-xs text-muted-foreground">Generated Podcast</span>
                    <a href={videoUrl} download>
                      <Button variant="ghost" size="sm" className="h-7 text-xs text-neon-cyan hover:text-neon-cyan hover:bg-neon-cyan/10">
                        <Download className="w-3 h-3 mr-1" /> Download
                      </Button>
                    </a>
                  </div>
                </motion.div>
              )}

              {/* Background Image */}
              {backgroundUrl && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="rounded-lg overflow-hidden border border-border/50 bg-muted/20"
                >
                  <div className="relative group">
                    <img src={backgroundUrl} alt="Generated background" className="w-full aspect-video object-cover" />
                    <div className="absolute inset-0 bg-background/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-3">
                      <a href={backgroundUrl} target="_blank" rel="noopener noreferrer">
                        <Button variant="ghost" size="sm" className="h-8 text-xs text-neon-cyan hover:bg-neon-cyan/10">
                          <ExternalLink className="w-3 h-3 mr-1" /> View
                        </Button>
                      </a>
                      <a href={backgroundUrl} download>
                        <Button variant="ghost" size="sm" className="h-8 text-xs text-neon-cyan hover:bg-neon-cyan/10">
                          <Download className="w-3 h-3 mr-1" /> Save
                        </Button>
                      </a>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 p-3">
                    <Image className="w-3.5 h-3.5 text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">Generated Background</span>
                  </div>
                </motion.div>
              )}

              {/* Transcript */}
              {transcriptUrl && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="flex items-center gap-3 p-3 rounded-lg border border-border/50 bg-muted/20"
                >
                  <div className="w-10 h-10 rounded-lg bg-neon-violet/10 flex items-center justify-center shrink-0">
                    <FileText className="w-5 h-5 text-neon-violet" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground">Transcript</p>
                    <p className="text-xs text-muted-foreground">Full podcast transcript</p>
                  </div>
                  <a href={transcriptUrl} download>
                    <Button variant="ghost" size="sm" className="h-8 text-xs text-neon-cyan hover:bg-neon-cyan/10">
                      <Download className="w-3 h-3 mr-1" /> Download
                    </Button>
                  </a>
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default MediaGallery;
