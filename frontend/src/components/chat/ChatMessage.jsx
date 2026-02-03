import MessageOther from "./MessageOther";
import MessageSelf from "./MessageSelf";
import MessageSystem from "./MessageSystem";

const ChatMessage = ({ message, currentUserId }) => {
  if (message.sender_type === "system") {
    return <MessageSystem message={message} />;
  }

  if (message.sender_user_id === currentUserId) {
    return <MessageSelf message={message} />;
  }

  return <MessageOther message={message} />;
};

export default ChatMessage;
