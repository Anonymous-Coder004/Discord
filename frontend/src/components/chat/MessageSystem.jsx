import { formatTime } from "../../utils/formatTime";

const MessageSystem = ({ message }) => {
  return (
    <div className="flex justify-center my-4">
      <div className="text-xs text-white/40 bg-white/5 px-3 py-1 rounded-full">
        {message.content} • {formatTime(message.created_at)}
      </div>
    </div>
  );
};

export default MessageSystem;
