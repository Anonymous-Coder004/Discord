import AvatarBubble from "./AvatarBubble";
import MessageTime from "./MessageTime";
import BotAvatar from "./BotAvatar";
const MessageLLM = ({ message }) => {
  return (
    <div className="flex justify-start mb-4">
      <div className="flex items-start gap-3 max-w-[70%]">
        {/* Bot Avatar */}
        <BotAvatar />

        {/* Message bubble */}
        <div className="flex flex-col items-start">
          <div className="text-xs text-slate-400 mb-1">
            LLM Assistant
          </div>

          <div
            className="bg-slate-800 text-slate-100
                       px-4 py-2 rounded-2xl rounded-tl-sm
                       border border-slate-700"
          >
            <div className="whitespace-pre-wrap text-sm leading-relaxed">
              {message.content}
            </div>
          </div>

          <MessageTime time={message.created_at} />
        </div>
      </div>
    </div>
  );
};

export default MessageLLM;
