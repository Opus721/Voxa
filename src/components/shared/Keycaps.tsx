import React from "react";
import {
  bindingKeys,
  isOnlyModifiers,
  keycapLabel,
  keycapLabels,
  type OSType,
} from "@/lib/utils/keyboard";

interface KeycapsProps {
  /** The binding to draw, e.g. "option+space". */
  binding: string;
  osType: OSType;
  /** sm: standalone; screen: Demo's drawn screen; line: inline in body text. */
  size?: "sm" | "screen" | "line";
  /** Draw every key as held down. */
  pressed?: boolean;
  /** A combination still being captured: dashed, no drop. */
  partial?: boolean;
  /** Raise the keys on hover/focus of a parent `group/keycaps` control. */
  lift?: boolean;
  className?: string;
}

const SIZES = {
  sm: "h-[22px] min-w-[22px] px-1.5 rounded-[5px] text-[12px]",
  screen: "h-[22px] min-w-[22px] px-1.5 rounded-[5px] text-[11px]",
  line: "h-[20px] min-w-[20px] px-1.5 rounded-[5px] text-[12px]",
};

/** A shortcut binding drawn as physical keycaps. */
export const Keycaps: React.FC<KeycapsProps> = ({
  binding,
  osType,
  size = "sm",
  pressed = false,
  partial = false,
  lift = false,
  className = "",
}) => {
  const labels = keycapLabels(binding, osType);
  const state = pressed
    ? "bg-hover text-emphasis border-edge-strong"
    : partial
      ? "border-dashed bg-transparent text-ink-2 border-edge"
      : `bg-control text-text border-edge ${
          lift
            ? "group-hover/keycaps:bg-hover group-hover/keycaps:text-emphasis"
            : ""
        }`;

  return (
    <span
      className={`inline-flex items-center gap-[4px] align-middle ${className}`}
      role="img"
      aria-label={keycapLabel(binding, osType)}
    >
      {labels.map((label, i) => (
        <span
          key={i}
          aria-hidden="true"
          className={`relative inline-flex items-center justify-center border font-ui font-medium leading-none select-none transition-colors duration-150 ${SIZES[size]} ${state}`}
        >
          {label}
        </span>
      ))}
    </span>
  );
};

const SLOT_SIZES = {
  sm: "h-[30px] min-w-[88px] px-[9px] rounded-[7px] text-small",
  line: "h-[25px] min-w-[64px] px-[8px] rounded-[6px] text-[13px]",
};

/** Placeholder key shown while a shortcut is being captured. */
export const KeySlot: React.FC<
  React.HTMLAttributes<HTMLSpanElement> & { size?: "sm" | "line" }
> = ({ size = "sm", className = "", children, ...rest }) => (
  <span
    aria-hidden={children ? undefined : true}
    {...rest}
    className={`inline-flex translate-y-[3px] items-center justify-center whitespace-nowrap border border-dashed border-plum-pick font-display font-semibold leading-none text-ink-2 animate-key-slot motion-reduce:animate-none ${SLOT_SIZES[size]} ${className}`}
  >
    {children}
  </span>
);

/** The instruction while capturing: modifiers alone still need a key. */
export const captureHintKey = (partial: string) =>
  isOnlyModifiers(bindingKeys(partial))
    ? "onboarding.demo.addKey"
    : "onboarding.demo.pressKeys";

/** While capturing: the keys pressed so far, dashed, or an empty slot before any. */
export const CapturedKeys: React.FC<{
  partial: string;
  osType: OSType;
  size?: "sm" | "line";
  /** On the keys and the slot alike. */
  className?: string;
  keysClassName?: string;
  slotClassName?: string;
  /** Words in the empty slot, announced. */
  slotLabel?: string;
}> = ({
  partial,
  osType,
  size = "sm",
  className = "",
  keysClassName = "",
  slotClassName = "",
  slotLabel,
}) =>
  bindingKeys(partial).length ? (
    <Keycaps
      binding={partial}
      osType={osType}
      size={size}
      partial
      className={`${className} ${keysClassName}`}
    />
  ) : (
    <KeySlot
      size={size}
      role={slotLabel ? "status" : undefined}
      className={`${className} ${slotClassName}`}
    >
      {slotLabel}
    </KeySlot>
  );
