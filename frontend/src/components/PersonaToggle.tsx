import { motion } from "framer-motion";
import { Users, FlaskConical, BookOpen, BarChart3 } from "lucide-react";

export interface Persona {
  id: string;
  label: string;
  host1: string;
  host2: string;
  icon: React.ElementType;
}

export const personas: Persona[] = [
  { id: "expert-skeptic", label: "Expert & Skeptic", host1: "The Expert", host2: "The Skeptic", icon: FlaskConical },
  { id: "storyteller-scientist", label: "Storyteller & Data Scientist", host1: "The Storyteller", host2: "The Data Scientist", icon: BookOpen },
  { id: "analyst-creative", label: "Analyst & Creative", host1: "The Analyst", host2: "The Creative", icon: BarChart3 },
];

interface PersonaToggleProps {
  selected: string;
  onSelect: (id: string) => void;
}

const PersonaToggle = ({ selected, onSelect }: PersonaToggleProps) => {
  return (
    <div className="glass-panel p-4">
      <div className="flex items-center gap-2 mb-3">
        <Users className="w-4 h-4 text-neon-cyan" />
        <span className="text-sm font-semibold text-foreground">Host Personas</span>
      </div>
      <div className="grid gap-2">
        {personas.map((p) => {
          const isSelected = selected === p.id;
          const Icon = p.icon;
          return (
            <motion.button
              key={p.id}
              onClick={() => onSelect(p.id)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className={`relative flex items-center gap-3 p-3 rounded-lg border text-left transition-all duration-200 ${
                isSelected
                  ? "border-neon-cyan/50 bg-neon-cyan/10"
                  : "border-border/50 bg-muted/30 hover:border-muted-foreground/30"
              }`}
            >
              <Icon className={`w-4 h-4 shrink-0 ${isSelected ? "text-neon-cyan" : "text-muted-foreground"}`} />
              <div>
                <div className={`text-sm font-medium ${isSelected ? "text-neon-cyan" : "text-foreground"}`}>
                  {p.label}
                </div>
                <div className="text-xs text-muted-foreground">
                  {p.host1} + {p.host2}
                </div>
              </div>
              {isSelected && (
                <motion.div
                  layoutId="persona-indicator"
                  className="absolute right-3 w-2 h-2 rounded-full bg-neon-cyan"
                  transition={{ type: "spring", stiffness: 500, damping: 30 }}
                />
              )}
            </motion.button>
          );
        })}
      </div>
    </div>
  );
};

export default PersonaToggle;
