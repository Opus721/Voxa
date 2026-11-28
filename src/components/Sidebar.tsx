import React from "react";
import { useTranslation } from "react-i18next";
import {
  Cog,
  FlaskConical,
  History,
  Info,
  SlidersHorizontal,
  Sparkles,
  Cpu,
} from "lucide-react";
import { VoxaMark } from "./icons/VoxaMark";
import { useSettings } from "../hooks/useSettings";
import {
  GeneralSettings,
  AdvancedSettings,
  HistorySettings,
  AboutSettings,
  PostProcessingSettings,
  ModelsSettings,
} from "./settings";

export type SidebarSection = keyof typeof SECTIONS_CONFIG;

interface IconProps {
  width?: number | string;
  height?: number | string;
  size?: number | string;
  className?: string;
  strokeWidth?: number | string;
  [key: string]: unknown;
}

interface SectionConfig {
  labelKey: string;
  icon: React.ComponentType<IconProps>;
  /** `null` when App renders the section itself (Debug, with its handlers). */
  component: React.ComponentType | null;
  enabled: (settings: unknown) => boolean;
}

export const SECTIONS_CONFIG = {
  general: {
    labelKey: "sidebar.general",
    icon: SlidersHorizontal,
    component: GeneralSettings,
    enabled: () => true,
  },
  history: {
    labelKey: "sidebar.history",
    icon: History,
    component: HistorySettings,
    enabled: () => true,
  },
  models: {
    labelKey: "sidebar.models",
    icon: Cpu,
    component: ModelsSettings,
    enabled: () => true,
  },
  advanced: {
    labelKey: "sidebar.advanced",
    icon: Cog,
    component: AdvancedSettings,
    enabled: () => true,
  },
  postprocessing: {
    labelKey: "sidebar.postProcessing",
    icon: Sparkles,
    component: PostProcessingSettings,
    enabled: (settings) =>
      (settings as { post_process_enabled?: boolean } | null)
        ?.post_process_enabled ?? false,
  },
  debug: {
    labelKey: "sidebar.debug",
    icon: FlaskConical,
    component: null,
    enabled: (settings) =>
      (settings as { debug_mode?: boolean } | null)?.debug_mode ?? false,
  },
  about: {
    labelKey: "sidebar.about",
    icon: Info,
    component: AboutSettings,
    enabled: () => true,
  },
} as const satisfies Record<string, SectionConfig>;

interface SidebarProps {
  activeSection: SidebarSection;
  onSectionChange: (section: SidebarSection) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeSection,
  onSectionChange,
}) => {
  const { t } = useTranslation();
  const { settings } = useSettings();

  const availableSections = Object.entries(SECTIONS_CONFIG)
    .filter(([_, config]) => config.enabled(settings))
    .map(([id, config]) => ({ id: id as SidebarSection, ...config }));

  return (
    <nav className="flex flex-col w-[220px] shrink-0 h-full bg-frame px-2 py-3">
      <div className="flex items-center gap-2 px-2 h-8 mb-3">
        <VoxaMark size={20} />
        <span className="text-[13px] font-semibold tracking-[-0.02em] text-emphasis">
          {t("app.name")}
        </span>
      </div>
      <div className="flex flex-col gap-px">
        {availableSections.map((section) => {
          const Icon = section.icon;
          const isActive = activeSection === section.id;

          return (
            <button
              key={section.id}
              type="button"
              className={`flex gap-2 items-center h-7 px-2 w-full rounded-[6px] cursor-pointer transition-colors duration-150 text-start ${
                isActive
                  ? "bg-control text-emphasis"
                  : "text-ink-2 hover:bg-hover hover:text-emphasis"
              }`}
              onClick={() => onSectionChange(section.id)}
            >
              <Icon
                width={16}
                height={16}
                size={16}
                strokeWidth={1.5}
                className="shrink-0"
              />
              <span className="text-[13px] font-medium truncate">
                {t(section.labelKey)}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
