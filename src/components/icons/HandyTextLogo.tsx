import { useTranslation } from "react-i18next";
import HandyHand from "./HandyHand";

/** Wordmark: the V mark plus the product name. */
const HandyTextLogo = ({
  width,
  className = "",
}: {
  width?: number | string;
  className?: string;
}) => {
  const { t } = useTranslation();
  return (
    <span
      className={`inline-flex items-center gap-2 text-emphasis ${className}`}
      style={{ width }}
    >
      <HandyHand width={18} height={18} className="shrink-0" />
      <span className="text-[15px] font-semibold tracking-[-0.02em] leading-none">
        {t("app.name")}
      </span>
    </span>
  );
};

export default HandyTextLogo;
