import { formatTime } from "../../utils/formatTime";

const MessageTime = ({ time }) => (
  <span className="text-xs text-white/40 mt-1 block">
    {formatTime(time)}
  </span>
);

export default MessageTime;
