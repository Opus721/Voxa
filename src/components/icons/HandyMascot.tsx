import HandyHand from "./HandyHand";

/** Product mark standing in for the old mascot illustration. */
const HandyMascot = ({ className = "" }: { className?: string }) => (
  <HandyHand className={`text-text ${className}`} width="100%" height="100%" />
);

export default HandyMascot;
