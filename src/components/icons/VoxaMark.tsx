import mark from "../../../design/voxa-mark-bodoni-bleed-2.svg";

export const VoxaMark = ({
  size,
  className,
}: {
  size: number | string;
  className?: string;
}) => (
  <img
    src={mark}
    alt=""
    width={size}
    height={size}
    className={className}
    draggable={false}
  />
);
