// components/chat/ChatInput.jsx
import { Paperclip, Send } from "lucide-react";

const ChatInput = () => {
  return (
    <div className="border-t border-white/10 bg-black/30 backdrop-blur-xl px-6 py-4">
      <div className="flex items-center gap-3">
        {/* Upload (RAG later) */}
        <button
          className="p-2 rounded-lg bg-white/5 hover:bg-white/10 text-white/70"
          title="Upload (coming soon)"
        >
          <Paperclip size={18} />
        </button>

        {/* Input */}
        <input
          type="text"
          placeholder="Type a message..."
          className="
            flex-1
            bg-white/5
            border border-white/10
            rounded-xl
            px-4 py-2
            text-white
            placeholder:text-white/40
            outline-none
            focus:border-indigo-500
          "
        />

        {/* Send */}
        <button
          className="p-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
