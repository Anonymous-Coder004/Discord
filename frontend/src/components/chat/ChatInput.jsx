import React, { useState } from "react";
import { Paperclip, Send } from "lucide-react";

const ChatInput = ({ onSend }) => {
  const [text, setText] = useState("");

  const handleSend = () => {
    const message = text.trim();
    if (!message) return;

    onSend(message);   // 🔑 backend handles everything after this
    setText("");       // clear input immediately
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="px-6 py-4 border-t border-white/10 bg-black/30 backdrop-blur-xl">
      <div className="flex items-center gap-3">
        {/* Upload (RAG later) */}
        <button
          className="p-2 rounded-full hover:bg-white/10 text-gray-400"
          title="Upload (coming soon)"
        >
          <Paperclip size={18} />
        </button>

        {/* Input */}
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message..."
          rows={1}
          className="
            flex-1 resize-none
            bg-white/5 text-white
            rounded-xl px-4 py-3
            outline-none
            border border-white/10
            focus:border-indigo-500
          "
        />

        {/* Send */}
        <button
          onClick={handleSend}
          disabled={!text.trim()}
          className="
            p-3 rounded-xl
            bg-indigo-600 hover:bg-indigo-700
            disabled:opacity-40 disabled:cursor-not-allowed
            text-white
          "
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
