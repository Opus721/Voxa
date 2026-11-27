/** Italic V from Instrument Serif, outlined. Named HandyHand so existing imports keep working. */
const HandyHand = ({
  width,
  height,
  className = "",
}: {
  width?: number | string;
  height?: number | string;
  className?: string;
}) => (
  <svg
    width={width || 16}
    height={height || 16}
    viewBox="0 0 508 746"
    fill="currentColor"
    className={className}
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    <path d="M88.0 738.0Q84.0 738.0 80.0 735.0Q76.0 732.0 76.0 722.0L65.0 88.0Q64.0 60.0 58.0 49.0Q52.0 38.0 33.0 34.0L20.0 31.0Q8.0 28.0 8.0 19.0Q8.0 8.0 25.0 8.0L190.0 8.0Q203.0 8.0 203.0 18.0Q203.0 29.0 183.0 31.0L163.0 33.0Q146.0 34.0 139.5 43.5Q133.0 53.0 133.0 75.0L138.0 548.0Q138.0 558.0 144.0 559.0Q150.0 560.0 154.0 552.0L373.0 96.0Q401.0 39.0 355.0 33.0L341.0 31.0Q326.0 28.0 326.0 19.0Q326.0 8.0 343.0 8.0L488.0 8.0Q500.0 8.0 500.0 18.0Q500.0 27.0 484.0 31.0L468.0 34.0Q448.0 38.0 434.0 53.5Q420.0 69.0 406.0 97.0L107.0 722.0Q103.0 732.0 97.5 735.0Q92.0 738.0 88.0 738.0Z" />
  </svg>
);

export default HandyHand;
