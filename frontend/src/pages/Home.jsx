import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import Header from "../components/Header/Header";
import RoomListPanel from "../components/RoomListPanel";
import RoomDetailPanel from "../components/RoomDetailPanel";
import { useAuth } from "../context/AuthContext";
import roomApi from "../api/rooms";

const Home = () => {
  const { user, loading, logout } = useAuth();

  const [rooms, setRooms] = useState([]);
  const [selectedRoomId, setSelectedRoomId] = useState(null);
  const [selectedRoom, setSelectedRoom] = useState(null);

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
  // Fetch all rooms on load
  // ─────────────────────────────────────────────
  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const data = await roomApi.listRooms();

        setRooms(data);

        // Auto-select latest room
        if (data.length > 0) {
          setSelectedRoomId(data[0].id);
        }
      } catch (err) {
        console.error("Failed to fetch rooms", err);
      }
    };

    fetchRooms();
  }, []);

  // ─────────────────────────────────────────────
  // Fetch selected room details
  // ─────────────────────────────────────────────
  useEffect(() => {
    if (!selectedRoomId) {
      setSelectedRoom(null);
      return;
    }

    const fetchRoomDetail = async () => {
      try {
        const room = await roomApi.getRoomById(selectedRoomId);
        setSelectedRoom(room);
      } catch (err) {
        console.error("Failed to fetch room detail", err);
      }
    };

    fetchRoomDetail();
  }, [selectedRoomId]);

  // ─────────────────────────────────────────────
  // Derived permissions
  // ─────────────────────────────────────────────
  const canDeleteRoom =
    selectedRoom && selectedRoom.owner_id === user.id;

  // ─────────────────────────────────────────────
  // Handlers
  // ─────────────────────────────────────────────
  const handleRoomSelect = (roomId) => {
    setSelectedRoomId(roomId);
  };

  const handleCreateRoom = () => {
    // Create Room modal will be added later
    console.log("Create Room clicked");
  };

  const handleDeleteRoom = () => {
    // Delete logic will be wired later
    console.log("Delete Room clicked");
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-black via-slate-900 to-black">
      {/* Header */}
      <Header
        onCreateRoom={handleCreateRoom}
        onDeleteRoom={handleDeleteRoom}
        onLogout={handleLogout}
        canDeleteRoom={!!canDeleteRoom}
      />

      {/* Main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left sidebar */}
        <RoomListPanel
          rooms={rooms}
          selectedRoomId={selectedRoomId}
          onRoomSelect={handleRoomSelect}
        />

        {/* Right panel */}
        <RoomDetailPanel room={selectedRoom} />
      </div>
    </div>
  );
};

export default Home;
