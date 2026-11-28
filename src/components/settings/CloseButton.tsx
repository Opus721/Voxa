import React from "react";
import { useTranslation } from "react-i18next";
import { Dropdown } from "../ui/Dropdown";
import { SettingContainer } from "../ui/SettingContainer";
import { useSettings } from "../../hooks/useSettings";
import type { CloseButtonBehavior } from "@/bindings";

interface CloseButtonProps {
  descriptionMode?: "inline" | "tooltip";
  grouped?: boolean;
}

export const CloseButtonSetting: React.FC<CloseButtonProps> = React.memo(
  ({ descriptionMode = "inline", grouped = false }) => {
    const { t } = useTranslation();
    const { getSetting, updateSetting, isUpdating } = useSettings();
    const selected = (getSetting("close_button") ??
      "hide") as CloseButtonBehavior;

    return (
      <SettingContainer
        title={t("settings.general.closeButton.title")}
        description={t("settings.general.closeButton.description")}
        descriptionMode={descriptionMode}
        grouped={grouped}
      >
        <Dropdown
          options={[
            {
              value: "hide",
              label: t("settings.general.closeButton.options.hide"),
            },
            {
              value: "quit",
              label: t("settings.general.closeButton.options.quit"),
            },
          ]}
          selectedValue={selected}
          onSelect={(value) =>
            updateSetting("close_button", value as CloseButtonBehavior)
          }
          disabled={isUpdating("close_button")}
        />
      </SettingContainer>
    );
  },
);
