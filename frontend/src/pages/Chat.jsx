import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Header from "../components/Header/Header";
import RoomListPanel from "../components/RoomListPanel";
import ChatMessage from "../components/chat/ChatMessage";
import ChatMessageList from "../components/chat/ChatMessageList";
import ChatInput from "../components/chat/ChatInput";

import useChatSocket from "../hooks/useChatSocket";
import { useAuth } from "../context/AuthContext";
import roomApi from "../api/rooms";
import uploadApi from "../api/uploadApi";
import RoomDetailPanel from "../components/RoomDetailPanel";
const Chat = () => {
  const { user, logout } = useAuth();
  const { roomId } = useParams();
  const [room, setRoom] = useState(null);
  const navigate = useNavigate();
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [viewMode, setViewMode] = useState("CHAT"); 
  /* ───────────── ROOMS STATE (same as Home) ───────────── */
  const [rooms, setRooms] = useState([]);
  const [isUploading, setIsUploading] = useState(false);

  /* ───────────── FETCH ROOMS ───────────── */
  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const data = await roomApi.listRooms();
        setRooms(data);
      } catch (err) {
        console.error("Failed to fetch rooms", err);
      }
    };

    fetchRooms();
  }, []);

  useEffect(() => {
    const fetchRoom = async () => {
      try {
        const res = await roomApi.checkAccess(roomId);
        setRoom(res.room);
      } catch (err) {
        console.error("Failed to fetch room", err);
      }
    };

    fetchRoom();
  }, [roomId]);

  /* ───────────── CHAT SOCKET ───────────── */
  const { messages, sendMessage, disconnect } = useChatSocket({
    roomId,
    token: localStorage.getItem("access_token"),
  });

  /* ───────────── ACTIONS ───────────── */
  const handleLeaveRoom = async () => {
    try {
      await roomApi.leaveRoom(roomId);
    } catch (err) {
      console.error("Failed to leave room", err);
    } finally {
      disconnect();                    
      navigate("/");                  
    }
  };


  const handleLogout = () => {
    disconnect();
    logout();
  };

  const handleRoomSelect = async (roomId) => {
    try {
      const res = await roomApi.checkAccess(roomId);

      if (res.is_member) {
        navigate(`/rooms/${roomId}/Chat`);
        setSelectedRoom(res.room);
        setViewMode("CHAT");
      } else {
        setSelectedRoom(res.room);
        setViewMode("JOIN");
      }
    } catch (err) {
      console.error("Room access check failed", err);
    }
  };

  const handledeleteRoom=async ()=>{
    try {
      await roomApi.deleteRoom(roomId);
    } catch (err) {
      console.error("Failed to delete room", err);
    } finally {
      disconnect();                    
      navigate("/");                  
    }
  };

  const handleUpload = async (file) => {
    if (!roomId) return;

    try {
      setIsUploading(true);

      await uploadApi.uploadPdf(roomId, file);

      // DO NOT add any message manually
      // Backend will broadcast indexing_started + indexing_completed

    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setIsUploading(false);
    }
  };


  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-black via-slate-900 to-black">
      <Header
        showHome
        showCreate
        showLeave
        showDelete={room&&room.owner_id===user.id}
        onHome={() => {
          disconnect();
          navigate("/");
        }}
        onCreateRoom={() => navigate("/rooms/create")}
        onLeaveRoom={handleLeaveRoom}
        onDeleteRoom={handledeleteRoom}
        onLogout={handleLogout}
        canDeleteRoom={room&&room.owner_id===user.id}
      />

      <div className="flex flex-1 overflow-hidden">
        {/* ───────── LEFT PANEL (same pattern as Home) ───────── */}
        <RoomListPanel
          rooms={rooms}
          selectedRoomId={Number(roomId)}
          onRoomSelect={handleRoomSelect}
        />

        {/* ───────── CHAT AREA ───────── */}
        {viewMode==="CHAT" && <div className="flex flex-col flex-1">
          <ChatMessageList>
            {messages.map((msg, idx) => (
              <ChatMessage
                key={msg.id ?? idx}
                message={msg}
                currentUserId={user.id}
              />
            ))}
          </ChatMessageList>

          <ChatInput
            onSend={sendMessage}
            onUpload={handleUpload}
            isUploading={isUploading}
          />

        </div>}
        {viewMode === "JOIN" && (
          <RoomDetailPanel room={selectedRoom} />
        )}
        
      </div>
    </div>
  );
};

export default Chat;
