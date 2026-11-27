import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  variant?: "default" | "compact";
}

export const Input: React.FC<InputProps> = ({
  className = "",
  variant = "default",
  disabled,
  ...props
}) => {
  const baseClasses =
    "h-[30px] px-2.5 text-[13px] font-medium bg-control border border-edge rounded-[6px] text-start text-text transition-colors duration-150";

  const interactiveClasses = disabled
    ? "opacity-50 cursor-not-allowed"
    : "hover:border-edge-strong focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent";

  const variantClasses = {
    default: "",
    compact: "h-6 px-2 text-[12px]",
  } as const;

  return (
    <input
      className={`${baseClasses} ${variantClasses[variant]} ${interactiveClasses} ${className}`}
      disabled={disabled}
      {...props}
    />
  );
};
