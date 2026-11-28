import React from "react";

interface SettingsGroupProps {
  title?: string;
  description?: string;
  children: React.ReactNode;
}

export const SettingsGroup: React.FC<SettingsGroupProps> = ({
  title,
  description,
  children,
}) => {
  return (
    <div className="space-y-2">
      {title && (
        <div className="px-1">
          <h2 className="text-[13px] font-medium text-text tracking-[-0.006em]">
            {title}
          </h2>
          {description && (
            <p className="text-[12px] text-ink-2 mt-0.5 leading-snug">
              {description}
            </p>
          )}
        </div>
      )}
      <div className="bg-card border border-edge rounded-[8px] overflow-visible">
        <div className="divide-y divide-line">{children}</div>
      </div>
    </div>
  );
};
