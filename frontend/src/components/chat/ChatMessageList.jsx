// components/chat/ChatMessageList.jsx
const ChatMessageList = ({ children }) => {
  return (
    <div className="flex-1 overflow-y-auto px-8 py-6 space-y-6">
      {children}
    </div>
  );
};

export default ChatMessageList;
