import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import Header from "../components/Header/Header";
import RoomListPanel from "../components/RoomListPanel";
import ChatMessage from "../components/chat/ChatMessage";
import ChatMessageList from "../components/chat/ChatMessageList";
import ChatInput from "../components/chat/ChatInput";
import useChatSocket from "../hooks/useChatSocket";
import { useAuth } from "../context/AuthContext";

const Chat = () => {
  const { user, logout } = useAuth();
  const { roomId } = useParams();
  const navigate = useNavigate();

  const { messages, sendMessage, disconnect } = useChatSocket({
    roomId,
    token: localStorage.getItem("access_token"),
  });

  const handleLeaveRoom = () => {
    disconnect();
    navigate("/");
  };

  const handleLogout = () => {
    disconnect();
    logout();
  };

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-black via-slate-900 to-black">
      <Header
        showHome
        showCreate
        showLeave
        showDelete
        onHome={() => {
          disconnect();
          navigate("/");
        }}
        onCreateRoom={() => navigate("/rooms/create")}
        onLeaveRoom={handleLeaveRoom}
        onDeleteRoom={() => alert("Delete later")}
        onLogout={handleLogout}
      />

      <div className="flex flex-1 overflow-hidden">
        <RoomListPanel
          rooms={[]}
          selectedRoomId={Number(roomId)}
          onRoomSelect={(id) => {
            disconnect();
            navigate(`/rooms/${id}/chat`);
          }}
        />

        <div className="flex flex-col flex-1">
          <ChatMessageList>
            {messages.map((msg, idx) => (
              <ChatMessage
                key={idx}
                message={msg}
                currentUserId={user.id}
              />
            ))}
          </ChatMessageList>

          <ChatInput onSend={sendMessage} />
        </div>
      </div>
    </div>
  );
};

export default Chat;
