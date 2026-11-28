import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?:
    | "primary"
    | "primary-soft"
    | "secondary"
    | "outline"
    | "warning"
    | "danger"
    | "danger-ghost"
    | "ghost";
  size?: "sm" | "md" | "lg";
}

export const Button: React.FC<ButtonProps> = ({
  children,
  className = "",
  variant = "primary",
  size = "md",
  ...props
}) => {
  const baseClasses =
    "font-medium rounded-[6px] border border-transparent transition-colors duration-150 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer";

  const variantClasses = {
    primary: "text-white bg-accent hover:bg-accent-hover",
    "primary-soft":
      "text-accent-text bg-accent/15 hover:bg-accent/20 focus-visible:ring-accent",
    secondary:
      "text-text bg-control border-edge hover:bg-hover hover:border-edge-strong",
    outline:
      "text-text bg-panel border-edge hover:border-edge-strong focus-visible:ring-accent",
    warning:
      "text-text bg-control border-edge hover:bg-warning-wash hover:border-warning",
    danger: "text-white bg-error border-error hover:bg-error/80",
    "danger-ghost": "text-error hover:bg-error-wash",
    ghost: "text-ink-2 hover:bg-hover hover:text-text",
  };

  const sizeClasses = {
    sm: "h-6 px-2 text-[12px]",
    md: "h-[30px] px-2.5 text-[13px]",
    lg: "h-8 px-3 text-[13px]",
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};
