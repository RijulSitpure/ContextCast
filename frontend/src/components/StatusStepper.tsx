import { motion } from "framer-motion";
import { Upload, Database, Brain, Film, Check } from "lucide-react";

export type PipelineStep = "idle" | "uploading" | "vectorizing" | "thinking" | "rendering" | "complete";

const steps = [
  { id: "uploading" as const, label: "Uploading", icon: Upload },
  { id: "vectorizing" as const, label: "Vectorizing", icon: Database },
  { id: "thinking" as const, label: "Thinking", icon: Brain },
  { id: "rendering" as const, label: "Rendering", icon: Film },
];

const stepIndex = (step: PipelineStep) => {
  if (step === "idle") return -1;
  if (step === "complete") return steps.length;
  return steps.findIndex((s) => s.id === step);
};

interface StatusStepperProps {
  currentStep: PipelineStep;
}

const StatusStepper = ({ currentStep }: StatusStepperProps) => {
  const activeIdx = stepIndex(currentStep);

  return (
    <div className="flex items-center gap-2 w-full">
      {steps.map((step, i) => {
        const isComplete = activeIdx > i;
        const isActive = activeIdx === i;
        const Icon = isComplete ? Check : step.icon;

        return (
          <div key={step.id} className="flex items-center gap-2 flex-1">
            <motion.div
              className={`relative flex items-center justify-center w-9 h-9 rounded-full border-2 shrink-0 transition-colors duration-300 ${
                isComplete
                  ? "border-neon-cyan bg-neon-cyan/20"
                  : isActive
                  ? "border-neon-violet bg-neon-violet/20"
                  : "border-muted-foreground/30 bg-muted/50"
              }`}
              animate={isActive ? { scale: [1, 1.1, 1] } : {}}
              transition={{ repeat: Infinity, duration: 1.5 }}
            >
              <Icon className={`w-4 h-4 ${
                isComplete ? "text-neon-cyan" : isActive ? "text-neon-violet" : "text-muted-foreground"
              }`} />
              {isActive && (
                <motion.div
                  className="absolute inset-0 rounded-full border-2 border-neon-violet"
                  animate={{ opacity: [0.5, 0, 0.5], scale: [1, 1.4, 1] }}
                  transition={{ repeat: Infinity, duration: 2 }}
                />
              )}
            </motion.div>
            <span className={`text-xs font-medium hidden sm:block ${
              isComplete ? "text-neon-cyan" : isActive ? "text-neon-violet" : "text-muted-foreground"
            }`}>
              {step.label}
            </span>
            {i < steps.length - 1 && (
              <div className={`flex-1 h-px transition-colors duration-500 ${
                activeIdx > i ? "bg-neon-cyan/50" : "bg-muted-foreground/20"
              }`} />
            )}
          </div>
        );
      })}
    </div>
  );
};

export default StatusStepper;
