import AvatarBubble from "./AvatarBubble";
import MessageTime from "./MessageTime";

const MessageOther = ({ message }) => {
  return (
    <div className="flex gap-3 items-start max-w-[70%]">
      <AvatarBubble name={message.sender_username} />

      <div>
        <div className="text-sm text-white/70 mb-1">
          {message.sender_username}
        </div>

        <div className="bg-white/10 px-4 py-2 rounded-xl text-white">
          {message.content}
        </div>

        <MessageTime time={message.created_at} />
      </div>
    </div>
  );
};

export default MessageOther;
