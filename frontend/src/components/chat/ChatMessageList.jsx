// components/chat/ChatMessageList.jsx
import { useEffect,useRef } from "react";
const ChatMessageList = ({ children }) => {

  const bottomRef=useRef(null);
  useEffect(()=>{
    bottomRef.current?.scrollIntoView({behavior:"smooth"});
  },[children]);
  return (
    <div className="flex-1 overflow-y-auto px-8 py-6 space-y-6">
      {children}
      <div ref={bottomRef}/>
    </div>
  );
};

export default ChatMessageList;
