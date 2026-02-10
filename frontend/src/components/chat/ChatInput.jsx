import React, { useState, useRef } from "react";
import { Paperclip, Send } from "lucide-react";

const ChatInput = ({ onSend, onUpload }) => {
  const [text, setText] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef(null);

  const handleSend = () => {
    const message = text.trim();
    if (!message || isUploading) return;

    onSend(message);
    setText("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      setIsUploading(true);
      await onUpload(file);
    } finally {
      setIsUploading(false);
      e.target.value = null;
    }
  };

  const isTextPresent = text.trim().length > 0;

  return (
    <div className="px-6 py-4 border-t border-white/10 bg-black/30 backdrop-blur-xl">
      <div className="flex items-center gap-3">

        {/* Hidden file input */}
        <input
          type="file"
          accept="application/pdf"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="hidden"
        />

        {/* Upload */}
        <button
          onClick={() => fileInputRef.current.click()}
          disabled={isTextPresent || isUploading}
          className="p-2 rounded-full hover:bg-white/10 text-gray-400 disabled:opacity-40 disabled:cursor-not-allowed"
          title="Upload PDF"
        >
          <Paperclip size={18} />
        </button>

        {/* Input */}
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={isUploading ? "Uploading PDF..." : "Type a message..."}
          rows={1}
          disabled={isUploading}
          className="
            flex-1 resize-none
            bg-white/5 text-white
            rounded-xl px-4 py-3
            outline-none
            border border-white/10
            focus:border-indigo-500
            disabled:opacity-50
          "
        />

        {/* Send */}
        <button
          onClick={handleSend}
          disabled={!text.trim() || isUploading}
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
