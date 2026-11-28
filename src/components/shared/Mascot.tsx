import React from "react";
import { VoxaMark } from "../icons/VoxaMark";

interface MascotProps {
  /** Height in px. */
  size: number;
  /** Wave once on arrival, or high-five (re-key it to play again). */
  animation?: "wave" | "slap" | null;
}

/** The onboarding mark keeps the existing wave and completion animations. */
export const Mascot: React.FC<MascotProps> = ({ size, animation = null }) => (
  <VoxaMark
    size={size}
    className={`block shrink-0 origin-[50%_90%] select-none ${animation === "wave" ? "animate-wave" : animation === "slap" ? "animate-slap" : ""}`}
  />
);
