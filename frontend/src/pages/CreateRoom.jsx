import React, { useEffect, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import Header from "../components/Header/Header";
import RoomListPanel from "../components/RoomListPanel";
import CreateRoomForm from "../components/CreateRoom/CreateRoom";
import { useAuth } from "../context/AuthContext";
import roomApi from "../api/rooms";

const CreateRoom = () => {
  const { user, loading, logout } = useAuth();
  const navigate = useNavigate();

  const [rooms, setRooms] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  // ─────────────────────────────────────────────
  // Auth guard
  // ─────────────────────────────────────────────
  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center text-white">
        Loading...
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // ─────────────────────────────────────────────
  // Fetch rooms for left panel
  // ─────────────────────────────────────────────
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

  // ─────────────────────────────────────────────
  // Create Room handler (IMPORTANT PART)
  // ─────────────────────────────────────────────
  const handleCreateRoomSubmit = async (form) => {
  try {
    setSubmitting(true);
    setError("");

    // 1️⃣ Create room
    const room = await roomApi.createRoom({
      name: form.name,
      password: form.password || null,
      has_llm: form.has_llm,
      llm_username: form.has_llm ? form.llm_username : null,
    });

    // 2️⃣ Join room (creator becomes member)
    await roomApi.joinRoom(room.id, {
      password: form.password || null,
    });

    // 3️⃣ Redirect to chat
    navigate(`/rooms/${room.id}/chat`);
  } catch (err) {
    console.error(err);
    setError(
      err.response?.data?.detail ||
      "Failed to create and join room"
    );
  } finally {
    setSubmitting(false);
  }
};

  // ─────────────────────────────────────────────
  // Header handlers
  // ─────────────────────────────────────────────
  const handleRoomSelect = (roomId) => {
    navigate("/", { state: { selectedRoomId: roomId } });
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-black via-slate-900 to-black">
      {/* Header */}
      <Header
        onLogout={handleLogout} showHome
        onHome={() => navigate("/")}
      />

      {/* Main layout */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left panel */}
        <RoomListPanel
          rooms={rooms}
          selectedRoomId={null}
          onRoomSelect={handleRoomSelect}
        />

        {/* Right panel → Create Room */}
        <div className="flex-1 flex items-center justify-center">
          <CreateRoomForm
            onSubmit={handleCreateRoomSubmit}
            loading={submitting}
            error={error}
          />
        </div>
      </div>
    </div>
  );
};

export default CreateRoom;
